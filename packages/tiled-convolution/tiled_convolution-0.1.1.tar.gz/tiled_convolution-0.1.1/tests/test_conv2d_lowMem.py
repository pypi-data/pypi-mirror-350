from typing import Union, Tuple

import torch
import numpy as np
from hypothesis import given, settings, assume
import hypothesis.strategies as st
import hypothesis.extra.numpy as hnp

from tiled_convolution import conv2D_lowMem, compute_padding

# Assume that conv2D_lowMem and compute_padding have been defined as provided earlier.
# They should be imported from the module where they are implemented.
# from your_module import conv2D_lowMem, compute_padding

# Helper function for running the global convolution reference.
def global_conv2d_reference(input_tensor: torch.Tensor,
                            kernel_tensor: torch.Tensor,
                            pad_mode: Union[str, int, Tuple[int, int]],
                            stride: Union[Tuple[int, int], int],
                            dilation: Union[Tuple[int, int], int]) -> torch.Tensor:
    """
    Compute the reference convolution output using torch.nn.functional.conv2d applied to the full padded input.
    This function uses our compute_padding helper to obtain the effective global padding.
    """
    # Ensure stride and dilation are tuples.
    if isinstance(stride, int):
        stride = (stride, stride)
    if isinstance(dilation, int):
        dilation = (dilation, dilation)
    
    # Get the kernel dimensions.
    if kernel_tensor.ndim == 2:
        kH, kW = kernel_tensor.shape
    else:
        # For this reference, we assume kernel_tensor is provided as a 2D tensor.
        raise ValueError("Reference convolution expects a 2D kernel")
    
    # Get the effective padding amounts using compute_padding.
    (pad_top, pad_bottom), (pad_left, pad_right) = compute_padding((kH, kW), dilation, pad_mode)
    
    # Pad the input globally.
    # torch.nn.functional.pad expects pad values as (pad_left, pad_right, pad_top, pad_bottom).
    padded_input = torch.nn.functional.pad(input_tensor, (pad_left, pad_right, pad_top, pad_bottom))
    
    # Prepare tensor shapes.
    # conv2d in PyTorch expects (N, C, H, W)
    # If input_tensor is 2D (grayscale), add channel dimensions.
    if padded_input.ndim == 2:
        padded_input = padded_input[None, None, :, :]
    elif padded_input.ndim == 3:
        padded_input = padded_input[None, :, :, :]
    
    # Expand kernel: if kernel is 2D, assume depthwise convolution.
    # For a multi-channel input, the reference kernel is repeated for each channel.
    if kernel_tensor.ndim == 2:
        C = padded_input.shape[1]
        kernel_expanded = kernel_tensor[None, None, :, :].repeat(C, 1, 1, 1)
        groups = C
    else:
        kernel_expanded = kernel_tensor
        groups = 1

    # Run the convolution with no extra padding (since we've already padded the input).
    out = torch.nn.functional.conv2d(padded_input, kernel_expanded, stride=stride, padding=0, dilation=dilation, groups=groups)
    # Remove the batch dimension.
    return out[0]

# Test 1: Test for multi-channel inputs (with input shape (C, H, W))
@given(
    h=st.integers(min_value=16, max_value=32),
    w=st.integers(min_value=16, max_value=32),
    c=st.integers(min_value=1, max_value=3),
    k_h=st.integers(min_value=3, max_value=7),
    k_w=st.integers(min_value=3, max_value=7),
    pad_mode=st.sampled_from(['same', 'valid', 'full', (1, 1), 2]),
    stride=st.one_of(st.integers(min_value=1, max_value=3),
                      st.tuples(st.integers(min_value=1, max_value=3),
                                st.integers(min_value=1, max_value=3))),
    dilation=st.one_of(st.integers(min_value=1, max_value=2),
                        st.tuples(st.integers(min_value=1, max_value=2),
                                  st.integers(min_value=1, max_value=2))),
    tile_h=st.integers(min_value=8, max_value=16),
    tile_w=st.integers(min_value=8, max_value=16)
)
@settings(max_examples=20)
def test_conv2D_lowMem_multichannel(h, w, c, k_h, k_w, pad_mode, stride, dilation, tile_h, tile_w):
    # Create random multi-channel input.
    np_input = np.random.randn(c, h, w).astype(np.float32)
    input_tensor = torch.from_numpy(np_input)
    
    # Create random kernel.
    np_kernel = np.random.randn(k_h, k_w).astype(np.float32)
    kernel_tensor = torch.from_numpy(np_kernel)
    
    # Compute output from the low-memory convolution.
    output_lowMem = conv2D_lowMem(input_tensor, kernel_tensor, 
                                  batch_size=(tile_h, tile_w),
                                  stride=stride, dilation=dilation, padding=pad_mode)
    
    # Compute reference global convolution.
    expected = global_conv2d_reference(input_tensor, kernel_tensor, pad_mode, stride, dilation)
    
    # Verify that the outputs are close within tolerance.
    torch.testing.assert_close(output_lowMem, expected, atol=1e-4, rtol=1e-3)

# Test 2: Test for grayscale inputs (with input shape (H, W))
@given(
    h=st.integers(min_value=16, max_value=32),
    w=st.integers(min_value=16, max_value=32),
    k=st.integers(min_value=3, max_value=7),
)
@settings(max_examples=20)
def test_conv2D_lowMem_grayscale(h, w, k):
    np_input = np.random.randn(h, w).astype(np.float32)
    input_tensor = torch.from_numpy(np_input)
    
    np_kernel = np.random.randn(k, k).astype(np.float32)
    kernel_tensor = torch.from_numpy(np_kernel)
    
    # Use a fixed tile size for testing.
    output_lowMem = conv2D_lowMem(input_tensor, kernel_tensor, 
                                  batch_size=(8, 8),
                                  stride=1, dilation=1, padding='same')
    
    # Convert global input for reference convolution.
    expected = global_conv2d_reference(input_tensor, kernel_tensor, 'same', stride=1, dilation=1)
    
    torch.testing.assert_close(output_lowMem.squeeze(0), expected, atol=1e-4, rtol=1e-3)

# Test 3: Explicit test for even kernel dimensions.
def test_conv2D_lowMem_even_kernel():
    # Create a small multi-channel input.
    c, h, w = 2, 20, 20
    input_tensor = torch.randn(c, h, w, dtype=torch.float32)
    # Use an even kernel size.
    kH, kW = 4, 4
    kernel_tensor = torch.randn(kH, kW, dtype=torch.float32)
    
    output_lowMem = conv2D_lowMem(input_tensor, kernel_tensor, 
                                  batch_size=(10, 10),
                                  stride=1, dilation=1, padding='same')
    expected = global_conv2d_reference(input_tensor, kernel_tensor, 'same', stride=1, dilation=1)
    torch.testing.assert_close(output_lowMem, expected, atol=1e-4, rtol=1e-3)

# Test 4: Test with non-unit stride and dilation.
@given(
    h=st.integers(min_value=16, max_value=32),
    w=st.integers(min_value=16, max_value=32),
    c=st.integers(min_value=1, max_value=3),
    k_h=st.integers(min_value=3, max_value=7),
    k_w=st.integers(min_value=3, max_value=7),
    stride=st.tuples(st.integers(min_value=1, max_value=3), st.integers(min_value=1, max_value=3)),
    dilation=st.tuples(st.integers(min_value=1, max_value=2), st.integers(min_value=1, max_value=2)),
    pad_mode=st.sampled_from(['same', 'valid', 'full', (1, 1)]),
    tile_h=st.integers(min_value=8, max_value=16),
    tile_w=st.integers(min_value=8, max_value=16)
)
@settings(max_examples=20)
def test_conv2D_lowMem_stride_dilation(h, w, c, k_h, k_w, stride, dilation, pad_mode, tile_h, tile_w):
    np_input = np.random.randn(c, h, w).astype(np.float32)
    input_tensor = torch.from_numpy(np_input)
    np_kernel = np.random.randn(k_h, k_w).astype(np.float32)
    kernel_tensor = torch.from_numpy(np_kernel)

    output_lowMem = conv2D_lowMem(input_tensor, kernel_tensor, 
                                  batch_size=(tile_h, tile_w),
                                  stride=stride, dilation=dilation, padding=pad_mode)
    
    expected = global_conv2d_reference(input_tensor, kernel_tensor, pad_mode, stride, dilation)
    torch.testing.assert_close(output_lowMem, expected, atol=1e-4, rtol=1e-3)