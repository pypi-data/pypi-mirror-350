"""Parameters for testing for testing."""

from ._binary_testing_inputs import binary_error_test_inputs, binary_testing_inputs
from ._dummy_bff import dummy_bff
from ._multi_testing_inputs import (
    binary_vs_multi_test_inputs,
    multi3_vs_multi4_test_inputs,
    multi_error_test_inputs,
    multi_testing_inputs,
)
from ._unary_testing_inputs import unary_error_test_inputs, unary_testing_inputs


__all__ = [
    "binary_error_test_inputs",
    "binary_testing_inputs",
    "binary_vs_multi_test_inputs",
    "dummy_bff",
    "multi3_vs_multi4_test_inputs",
    "multi_error_test_inputs",
    "multi_testing_inputs",
    "unary_error_test_inputs",
    "unary_testing_inputs",
]
