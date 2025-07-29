"""
Test module for validating the custom compute_padding function from tiled_convolution.
These tests ensure that the computed padding, when applied before a 'valid' convolution,
produces the expected output shape. Both random (via Hypothesis) and explicit cases for
all supported padding types are covered, and invalid inputs are tested for proper error raising.
"""

from typing import Tuple, Union

import torch
import pytest
from hypothesis import given, assume, settings, HealthCheck, strategies as st

from tiled_convolution import compute_padding

# Define a cleaner strategy with only unique cases for supported padding.
unique_padding_types = st.one_of(
    st.sampled_from(["same", "valid", "full", (0, 0), (1, 1), (2, 2),
                      (1, 2), (2, 1), (1, 0), (0, 1), (4, 13)]),
    st.integers(min_value=0, max_value=5),
    st.tuples(st.integers(min_value=0, max_value=5), st.integers(min_value=0, max_value=5))
)

def compute_expected_output_size(input_size: int, pad_before: int, pad_after: int, k_eff: int) -> int:
    """
    Compute the expected output dimension for one axis given the input size,
    total padding and effective kernel size for a stride-1 valid convolution.
    """
    return input_size + pad_before + pad_after - k_eff + 1

@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
@given(
    # Kernel sizes between 1 and 10.
    kernel_size=st.tuples(st.integers(min_value=1, max_value=10),
                          st.integers(min_value=1, max_value=10)),
    # Dilation factors between 1 and 4.
    dilation=st.tuples(st.integers(min_value=1, max_value=4),
                       st.integers(min_value=1, max_value=4)),
    # Input height and width between 1 and 50.
    input_size=st.tuples(st.integers(min_value=1, max_value=50),
                         st.integers(min_value=1, max_value=50)),
    # Padding parameter from our defined strategy.
    padding=unique_padding_types,
)
def test_compute_padding_matches_conv2d(kernel_size, dilation, input_size, padding):
    """
    Test that compute_padding produces pad amounts that yield the expected output
    shape from a 2D convolution (with stride 1) when applied via torch.nn.functional.pad.
    """
    k_h, k_w = kernel_size
    d_h, d_w = dilation
    # Compute effective kernel sizes.
    k_h_eff = (k_h - 1) * d_h + 1
    k_w_eff = (k_w - 1) * d_w + 1

    # Get computed padding.
    (pad_top, pad_bottom), (pad_left, pad_right) = compute_padding(kernel_size, dilation, padding)
    
    input_h, input_w = input_size

    # Ensure padded input is big enough.
    assume(input_h + pad_top + pad_bottom >= k_h_eff)
    assume(input_w + pad_left + pad_right >= k_w_eff)

    expected_output_h = compute_expected_output_size(input_h, pad_top, pad_bottom, k_h_eff)
    expected_output_w = compute_expected_output_size(input_w, pad_left, pad_right, k_w_eff)

    # Create dummy input and weight tensors.
    input_tensor = torch.randn(1, 1, input_h, input_w)
    weight = torch.ones(1, 1, k_h, k_w)
    
    # The pad order is (left, right, top, bottom) per PyTorch's API.
    pad_tuple = (pad_left, pad_right, pad_top, pad_bottom)
    padded_input = torch.nn.functional.pad(input_tensor, pad_tuple)

    conv_out = torch.nn.functional.conv2d(
        padded_input, weight, bias=None, stride=1, dilation=dilation, padding=0
    )
    
    output_h, output_w = conv_out.shape[2], conv_out.shape[3]

    assert output_h == expected_output_h, (
        f"Expected output height {expected_output_h}, got {output_h} "
        f"with Kernel: {kernel_size}, Dilation: {dilation}, Padding: {padding}"
    )
    assert output_w == expected_output_w, (
        f"Expected output width {expected_output_w}, got {output_w} "
        f"with Kernel: {kernel_size}, Dilation: {dilation}, Padding: {padding}"
    )

@pytest.mark.parametrize("padding", [
    "same", "valid", "full", 0, (0, 0), (1, 1), (2, 2),
    (1, 2), (2, 1), (1, 0), (0, 1), (4, 13)
])
def test_compute_padding_explicit(padding: Union[str, Tuple[int, int]]):
    """
    Parameterized test for compute_padding, ensuring every supported padding type is explicitly checked.
    """
    kernel_size = (3, 3)
    dilation = (1, 1)
    input_size = (10, 10)
    
    k_h, k_w = kernel_size
    d_h, d_w = dilation
    k_h_eff = (k_h - 1) * d_h + 1
    k_w_eff = (k_w - 1) * d_w + 1

    (pad_top, pad_bottom), (pad_left, pad_right) = compute_padding(kernel_size, dilation, padding)
    
    input_h, input_w = input_size

    # Validate that padded dimensions are sufficient.
    assert input_h + pad_top + pad_bottom >= k_h_eff, "Padded height is too small."
    assert input_w + pad_left + pad_right >= k_w_eff, "Padded width is too small."

    expected_output_h = compute_expected_output_size(input_h, pad_top, pad_bottom, k_h_eff)
    expected_output_w = compute_expected_output_size(input_w, pad_left, pad_right, k_w_eff)

    input_tensor = torch.randn(1, 1, input_h, input_w)
    weight = torch.ones(1, 1, k_h, k_w)
    pad_tuple = (pad_left, pad_right, pad_top, pad_bottom)
    padded_input = torch.nn.functional.pad(input_tensor, pad_tuple)
    
    conv_out = torch.nn.functional.conv2d(padded_input, weight, bias=None, stride=1, dilation=dilation, padding=0)
    
    output_h, output_w = conv_out.shape[2], conv_out.shape[3]

    assert output_h == expected_output_h, (
        f"Explicit test: Expected output height {expected_output_h}, got {output_h} for Padding: {padding}"
    )
    assert output_w == expected_output_w, (
        f"Explicit test: Expected output width {expected_output_w}, got {output_w} for Padding: {padding}"
    )

def test_unsupported_padding():
    """
    Test that compute_padding raises a ValueError for an unsupported padding value.
    """
    with pytest.raises(ValueError):
        compute_padding((3, 3), (1, 1), "unsupported_mode")
