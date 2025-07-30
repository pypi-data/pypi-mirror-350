from collections.abc import Sequence
from typing import TypeAlias, TypeVar, cast

import numpy as np
from numpy.typing import NDArray

_ScalarT = TypeVar('_ScalarT', bound=np.generic)

ComplexOrReal = np.complex128 | np.complex64 | np.float64 | np.float32
Array1D: TypeAlias = np.ndarray[tuple[int], np.dtype[_ScalarT]]
Array2D: TypeAlias = np.ndarray[tuple[int, int], np.dtype[_ScalarT]]

def cast1D(a: NDArray[_ScalarT]) -> Array1D[_ScalarT]:
    """Cast a 1D array to the Array1D type."""
    assert a.ndim == 1, "Input must be a 1D array."
    return cast(Array1D[_ScalarT], a)

def slice1D(a: Array1D[_ScalarT], sl: slice) -> Array1D[_ScalarT]:
    """Slice a 1D array and preserve the shape."""
    assert a.ndim == 1, "Input must be a 1D array."
    result = a[sl]
    return cast1D(result)

def concat1D(arrays: Sequence[Array1D[_ScalarT] | Sequence[_ScalarT]]) -> Array1D[_ScalarT]:
    """Concatenate a list of 1D arrays."""
    result = np.concatenate(arrays)
    return cast1D(result)