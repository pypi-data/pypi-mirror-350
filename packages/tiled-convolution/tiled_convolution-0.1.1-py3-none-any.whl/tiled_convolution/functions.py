from typing import Tuple, Union, Optional, List

import math

import torch
import numpy as np
import zarr
import zarr.storage
from tqdm.auto import tqdm

def conv2d_tiled(
    input: Union[torch.Tensor, np.ndarray, zarr.Array],
    kernel: torch.Tensor,
    size_tile: Tuple[int, int],
    padding: Union[str, int, Tuple[int, int]] = 'same',    
    stride: Tuple[int, int] = (1, 1),
    dilation: Tuple[int, int] = (1, 1),
    output: Optional[Union[torch.Tensor, np.ndarray, zarr.Array]] = None,
    device_compute: Optional[torch.device] = None,
    device_return: Optional[torch.device] = None,
    dtype_compute: Optional[torch.dtype] = torch.float32,
    dtype_return: Optional[torch.dtype] = None,
    kind_return: Optional[str] = None,
    verbose: bool = False,
) -> Union[torch.Tensor, np.ndarray, zarr.Array]:
    ndim_input = input.ndim
    if ndim_input == 2:
        input = input[None, :, :]
    size_input = (input.shape[-2], input.shape[-1])
    size_kernel = (kernel.shape[-2], kernel.shape[-1])
    
    device_compute = device_compute if device_compute is not None else input.device
    device_return = device_return if device_return is not None else device_compute

    dtype_compute = dtype_compute if dtype_compute is not None else input.dtype
    dtype_return = dtype_return if dtype_return is not None else dtype_compute

    # print(f'kernel shape: {kernel.shape}')
    # print(f'padding: {padding}')

    padding_val = compute_padding_amount(
        size_input=size_input,
        size_kernel=size_kernel,
        stride=stride,
        dilation=dilation,
        padding=padding,
    )
    # print(f'padding_val: {padding_val}')

    shape_out = conv2d_output_size(
        size_input=size_input,
        size_kernel=size_kernel,
        padding=padding_val,
        stride=stride,
        dilation=dilation,
    )
    shape_out = (input.shape[0],) + shape_out
    # print(f'shape_out: {shape_out}')

    ## Figure out return object type
    if output is None:
        if kind_return is not None:
            assert kind_return in ['zarr', 'numpy', 'torch'], "kind_return must be one of ['zarr', 'numpy', 'torch']"
            if kind_return == 'zarr':
                output = zarr.create_array(
                    store=zarr.storage.MemoryStore(),
                    shape=shape_out,
                    dtype=torch_dtype_to_numpy_dtype(dtype_return),
                    chunks=size_tile,
                    overwrite=True,
                    order='C',
                )
            elif kind_return == 'numpy':
                output = np.empty(
                    shape=shape_out,
                    dtype=torch_dtype_to_numpy_dtype(dtype_return),
                )
            elif kind_return == 'torch':
                output = torch.empty(
                    size=shape_out,
                    dtype=dtype_return,
                    device=device_return,
                )
        else:
            output = torch.empty(
                size=shape_out,
                dtype=dtype_return,
                device=device_return,
            )

    if isinstance(output, zarr.Array):
        kind_return = 'zarr'
    elif isinstance(output, np.ndarray):
        kind_return = 'numpy'
    elif isinstance(output, torch.Tensor):
        kind_return = 'torch'
    else:
        raise ValueError("Output must be a zarr.Array, numpy.ndarray, or torch.Tensor")

    assert output.shape == shape_out, f"Output shape {output.shape} does not match expected shape {shape_out}"

    ## Move the kernel to the correct device
    kernel = torch.as_tensor(kernel).type(dtype_compute).to(device_compute)

    ## Make tiles_out indices
    # idx_tiles_out = [(ii, min(ii+size_tile[0], shape_out[0])-1, jj, min(jj+size_tile[1], shape_out[1])-1) for ii in range(0, shape_out[0], size_tile[0]) for jj in range(0, shape_out[1], size_tile[1])]
    idx_tiles_out: List[Tuple[int, int, int, int]] = []
    for ii in range(0, shape_out[-2], size_tile[0]):
        for jj in range(0, shape_out[-1], size_tile[1]):
            idx_out_top = int(ii)
            idx_out_bottom = int(min(ii + size_tile[0], shape_out[-2]) - 1)
            idx_out_left = int(jj)
            idx_out_right = int(min(jj + size_tile[1], shape_out[-1]) - 1)
            idx_tiles_out.append((idx_out_top, idx_out_bottom, idx_out_left, idx_out_right))

    ## loop over the tiles
    for i_tile, (idx_out_top, idx_out_bottom, idx_out_left, idx_out_right) in tqdm(enumerate(idx_tiles_out), total=len(idx_tiles_out), desc="Processing tiles", disable=not verbose):
        # print(f"Tile: {i_tile} / {len(idx_tiles)}")
        # print(f"idx_out: {idx_out_top, idx_out_bottom, idx_out_left, idx_out_right}")

        ## get the input indices for the tile
        idx_in_top, _, idx_in_left, _ = get_receptive_field_indices(
            indices=(idx_out_top, idx_out_left),
            padding=padding_val,
            size_kernel=size_kernel,
            stride=stride,
            dilation=dilation,
        )
        _, idx_in_bottom, _, idx_in_right = get_receptive_field_indices(
            indices=(idx_out_bottom, idx_out_right),
            padding=padding_val,
            size_kernel=size_kernel,
            stride=stride,
            dilation=dilation,
        )
        # print(f"idx_in: {idx_in_top, idx_in_bottom, idx_in_left, idx_in_right}")

        idx_in_top_clip, idx_in_bottom_clip = max(0, idx_in_top), min(size_input[0] - 1, idx_in_bottom)
        idx_in_left_clip, idx_in_right_clip = max(0, idx_in_left), min(size_input[1] - 1, idx_in_right)
        # print(f"idx_in_clip: {idx_in_top_clip, idx_in_bottom_clip, idx_in_left_clip, idx_in_right_clip}")

        ## get the tile
        tile_in = torch.as_tensor(input[..., idx_in_top_clip:idx_in_bottom_clip + 1, idx_in_left_clip:idx_in_right_clip + 1])
        # print(f'tile in shape: {tile.shape}')
        
        # get the padding for the tile
        padding_for_tile = indices_to_padding(
            indices=(idx_in_top, idx_in_bottom, idx_in_left, idx_in_right),
            size_input_full=size_input,
        )
        # print(f'padding for tile: {padding_for_tile}')

        ## pad the tile
        tile_in_padded = pad_tile(
            tile=tile_in,
            padding=padding_for_tile,
        )
        # print(f'tile padded shape: {tile_in_padded.shape}')

        ## move the tile to the correct device
        tile_in_padded = tile_in_padded.type(dtype_compute).to(device_compute)
        # print(f'tile padded device: {tile_in_padded.device}, dtype: {tile_in_padded.dtype}')

        ## compute the output for the tile
        out_custom = torch.nn.functional.conv2d(
            input=tile_in_padded[:, None, :, :],
            weight=kernel[None, None, :, :],
            stride=stride,
            padding='valid',
            dilation=dilation,
        )
        # print(f'out_custom shape: {out_custom.shape}')
        # print(f'target indices: {slice(idx_out_top, idx_out_bottom + 1)}, {slice(idx_out_left, idx_out_right + 1)}')
        # print(f'target shape: {out_custom[slice(idx_out_top, idx_out_bottom + 1), slice(idx_out_left, idx_out_right + 1)].shape}')

        # assign the output to the correct location
        out_custom = out_custom.type(dtype_return).to(device_return)
        if ndim_input == 2:
            out_custom = out_custom[0, 0, :, :]
        elif ndim_input == 3:
            out_custom = out_custom[:, 0, :, :]
        
        if kind_return in ['numpy', 'zarr']:
            out_custom = out_custom.cpu().numpy()
        elif kind_return == 'torch':
            out_custom = out_custom.to(device_return)

        output[:, slice(idx_out_top, idx_out_bottom + 1), slice(idx_out_left, idx_out_right + 1)] = out_custom
    
    return output
        

#######################################################################################################
############################################### HELPERS ###############################################
#######################################################################################################


def get_receptive_field_indices(
    indices: Tuple[int, int],
    padding: Tuple[int, int, int, int],
    size_kernel: Tuple[int, int],
    stride: Tuple[int, int],
    dilation: Tuple[int, int],
):
    """
    Requests indices (slices) from the image based on desired output indices.

    Given convolution parameters (padding, kernel size, stride, and dilation)
    and the input image size, get_indices returns the slice objects
    corresponding to the receptive field for a desired output element.

    For a given output position (i_out, j_out), the receptive field (in the
    padded coordinate system) is:
        i_in_start = i_out * stride[0] - pad_top j_in_start = j_out * stride[1]
        - pad_left i_in_end   = i_in_start + effective_kernel_height j_in_end
        = j_in_start + effective_kernel_width
    where:
        effective_kernel_height = (kernel_height - 1) * dilation[0] + 1
        effective_kernel_width  = (kernel_width  - 1) * dilation[1] + 1

    Since the actual input is unpadded, the computed indices fall outside the
    range of the input tensor shape (<0 to >H or >W)

    Args:
        indices (Tuple[int, int]): 
            A tuple (i_out, j_out) representing the desired output indices.
        padding (Tuple[int, int, int, int]): 
            A tuple (pad_top, pad_bottom, pad_left, pad_right) specifying the
            amount of padding added to the input tensor.
        size_kernel (Tuple[int, int]): 
            The size of the kernel (height, width).
        stride (Tuple[int, int]): 
            The stride of the convolution (vertical, horizontal).
        dilation (Tuple[int, int]): 
            The dilation of the kernel (vertical, horizontal).

    Returns:
        Tuple[int, int, int, int]:
            A tuple (i_in_start, i_in_end, j_in_start, j_in_end)
            representing the start and end indices for the input tensor
            (top, bottom, left, right).
    """
    i_out, j_out = indices

    # Determine effective kernel size.
    effective_kernel_height = (size_kernel[0] - 1) * dilation[0] + 1
    effective_kernel_width = (size_kernel[1] - 1) * dilation[1] + 1

    # Compute corresponding start and end indices in the padded input space.
    i_in_start = i_out * stride[0] - padding[0]
    j_in_start = j_out * stride[1] - padding[2]
    i_in_end = i_in_start + effective_kernel_height - 1
    j_in_end = j_in_start + effective_kernel_width - 1

    # Return slices for the input tensor.
    return (
        i_in_start,  # top / start_i
        i_in_end,    # bottom / end_i
        j_in_start,  # left / start_j
        j_in_end,     # right / end_j
    )
    

def indices_to_padding(
    indices: Tuple[int, int, int, int],
    size_input_full: Tuple[int, int],
):
    """
    Find the amount of padding needed based on the overhang of the indices past
    the input tensor shape.

    Args:
        indices (Tuple[int, int, int, int]): 
            A tuple (i_in_start, i_in_end, j_in_start, j_in_end) representing
            the start and end indices for the input tensor. (top, bottom, left, right)
        size_input_full (Tuple[int, int]): 
            The full size of the input tensor.

    Returns:
        Tuple[int, int]: 
            The computed padding values.
    """
    top, bottom, left, right = indices
    h, w = size_input_full

    # Compute padding values.
    pad_top = max(0, -top)
    pad_bottom = max(0, bottom + 1 - h)
    pad_left = max(0, -left)
    pad_right = max(0, right + 1 - w)

    return (
        pad_top,
        pad_bottom,
        pad_left,
        pad_right
    )

    
def pad_tile(
    tile: torch.Tensor,
    padding: Tuple[int, int, int, int],
):
    """
    Pad the tile tensor.

    Args:
        tile (torch.Tensor): 
            The tile tensor to be padded.
        padding (Tuple[int, int, int, int]): 
            The padding values (top, bottom, left, right).

    Returns:
        torch.Tensor: 
            The padded tile tensor.
    """
    pad_top, pad_bottom, pad_left, pad_right = padding
    return torch.nn.functional.pad(tile, (pad_left, pad_right, pad_top, pad_bottom), mode='constant', value=float(0.0))



def conv2d_output_size(
    size_input: Tuple[int, int],
    size_kernel: Tuple[int, int],
    padding: Tuple[int, int, int, int],
    stride: Tuple[int, int],
    dilation: Tuple[int, int]
) -> Tuple[int, int]:
    """
    Computes the output spatial dimensions (height, width) for a 2D convolution.

    The output size is computed using the formula:
        output = floor((input + 2 * padding - dilation * (size_kernel - 1) - 1)
        / stride + 1)

    This function assumes that the given padding is applied symmetrically. In
    other words, if padding = (pad_h, pad_w), pad_h is applied to both the top
    and bottom of the input, and pad_w to both the left and right.

    Args:
        size_input (Tuple[int, int]):
            A tuple (H_in, W_in) specifying the height and width of the input.
        size_kernel (Tuple[int, int]):
            A tuple (kH, kW) specifying the height and width of the convolution
            kernel.
        padding (Tuple[int, int, int, int]):
            A tuple (pad_top, pad_bottom, pad_left, pad_right) specifying the
            amount of padding added to the input tensor.
        stride (Tuple[int, int]):
            A tuple (stride_h, stride_w) specifying the vertical and horizontal
            strides.
        dilation (Tuple[int, int]):
            A tuple (dil_h, dil_w) specifying the dilation factors along the
            height and width.

    Returns:
        Tuple[int, int]:
            A tuple (H_out, W_out) representing the height and width of the
            output feature map.
    """
    H_in, W_in = size_input
    kH, kW = size_kernel
    pad_top, pad_bottom, pad_left, pad_right = padding
    stride_h, stride_w = stride
    dil_h, dil_w = dilation

    # Compute effective kernel dimensions after dilation.
    kernel_eff_h = (kH - 1) * dil_h + 1
    kernel_eff_w = (kW - 1) * dil_w + 1

    # Compute output dimensions based on the convolution formula.
    H_out = ((H_in + pad_top + pad_bottom - kernel_eff_h) // stride_h) + 1
    W_out = ((W_in + pad_left + pad_right - kernel_eff_w) // stride_w) + 1

    return (H_out, W_out)


def compute_padding_amount(
    size_input: Tuple[int, int],
    size_kernel: Tuple[int, int],
    stride: Tuple[int, int],
    dilation: Tuple[int, int],
    padding: Union[str, int, Tuple[int, int]]
) -> Tuple[int, int, int, int]:
    """
    Computes the padding amounts for a 2D convolution given the input size, kernel size,
    stride, dilation, and padding mode/amount.

    Supported padding modes are:
      - "same": Pads such that output size is ceil(size_input/stride) for each axis.
      - "valid": No padding (all zeros).
      - "full": Pads so that every possible overlap is computed (total padding = effective_kernel_size - 1 on each side).
      - A single integer: applied symmetrically on both dimensions.
      - A tuple (pad_h, pad_w): applied symmetrically along the height and width.

    The effective kernel size (taking dilation into account) is computed as:
        effective_kernel = (kernel_size - 1) * dilation + 1

    For "same" padding, the total padding needed in one dimension is:
    
        total_pad = max((ceil(input / stride) - 1)*stride + effective_kernel - input, 0)
    
    This is then split as:
    
        pad_front = total_pad // 2
        pad_back = total_pad - pad_front

    Args:
        size_input (Tuple[int, int]): (H, W) dimensions of the input.
        size_kernel (Tuple[int, int]): (kH, kW) dimensions of the kernel.
        stride (Tuple[int, int]): (stride_h, stride_w) for the convolution.
        dilation (Tuple[int, int]): (dil_h, dil_w) dilation factors.
        padding (Union[str, int, Tuple[int, int]]): Padding mode or explicit amount.

    Returns:
        Tuple[int, int, int, int]:
            A tuple ((pad_top, pad_bottom), (pad_left, pad_right)) specifying the number
            of pixels to pad along each dimension.
    """
    H, W = size_input
    kH, kW = size_kernel
    stride_h, stride_w = stride
    dil_h, dil_w = dilation

    # Effective kernel sizes.
    eff_kH = (kH - 1) * dil_h + 1
    eff_kW = (kW - 1) * dil_w + 1

    # Determine padding amounts.
    if isinstance(padding, str):
        mode = padding.lower()
        if mode == 'same':
            # Compute desired output dimensions.
            out_h = math.ceil(H / stride_h)
            out_w = math.ceil(W / stride_w)
            # Compute total required padding.
            total_pad_h = max((out_h - 1) * stride_h + eff_kH - H, 0)
            total_pad_w = max((out_w - 1) * stride_w + eff_kW - W, 0)
            pad_top = total_pad_h // 2
            pad_bottom = total_pad_h - pad_top
            pad_left = total_pad_w // 2
            pad_right = total_pad_w - pad_left
        elif mode == 'valid':
            pad_top = pad_bottom = pad_left = pad_right = 0
        elif mode == 'full':
            pad_top = pad_bottom = eff_kH - 1
            pad_left = pad_right = eff_kW - 1
        else:
            raise ValueError(f"Unsupported padding mode: {padding}")
    elif isinstance(padding, int):
        pad_top = pad_bottom = pad_left = pad_right = padding
    elif isinstance(padding, tuple):
        if len(padding) != 2:
            raise ValueError("Padding tuple must have exactly two values (pad_h, pad_w).")
        pad_h, pad_w = padding
        pad_top = pad_bottom = pad_h
        pad_left = pad_right = pad_w
    else:
        raise ValueError("Padding must be 'same', 'valid', 'full', an integer, or a tuple of two integers.")

    return (
        pad_top,
        pad_bottom,
        pad_left,
        pad_right
    )

def torch_dtype_to_numpy_dtype(dtype):
    return torch.empty(size=(0,), dtype=dtype).numpy().dtype