"""
Input validation utilities for HMM models.
"""

from typing import List, Optional, Union

import numpy as np
from numpy.typing import NDArray

from ..exceptions import IncompatibleShapeError, ValidationError


def validate_n_states(n_states: int) -> None:
    """Validate number of states parameter."""
    if not isinstance(n_states, int):
        raise ValidationError("n_states must be an integer")
    if n_states < 1:
        raise ValidationError("n_states must be positive")


def validate_n_observations(n_observations: Optional[int]) -> None:
    """Validate number of observations parameter."""
    if n_observations is not None:
        if not isinstance(n_observations, int):
            raise ValidationError("n_observations must be an integer")
        if n_observations < 1:
            raise ValidationError("n_observations must be positive")


def validate_sequence(sequence: NDArray, n_observations: Optional[int] = None) -> None:
    """Validate single observation sequence."""
    if not isinstance(sequence, np.ndarray):
        raise ValidationError("Sequence must be numpy array")

    if sequence.ndim != 1:
        raise ValidationError("Sequence must be 1-dimensional")

    if len(sequence) == 0:
        raise ValidationError("Sequence cannot be empty")

    if n_observations is not None:
        if not np.issubdtype(sequence.dtype, np.integer):
            raise ValidationError("Discrete sequences must contain integers")

        if np.any((sequence < 0) | (sequence >= n_observations)):
            raise ValidationError(
                f"Observations must be in range [0, {n_observations-1}]"
            )


def validate_sequences(
    sequences: Union[List[NDArray], NDArray], n_observations: Optional[int] = None
) -> List[NDArray]:
    """Validate and convert sequences to list format."""
    if isinstance(sequences, np.ndarray):
        if sequences.ndim == 1:
            sequences = [sequences]
        elif sequences.ndim == 2:
            sequences = [sequences[i] for i in range(len(sequences))]
        else:
            raise ValidationError("Array sequences must be 1D or 2D")

    if not isinstance(sequences, list):
        raise ValidationError("Sequences must be list or numpy array")

    if len(sequences) == 0:
        raise ValidationError("Must provide at least one sequence")

    validated = []
    for i, seq in enumerate(sequences):
        try:
            seq = np.asarray(seq)
            validate_sequence(seq, n_observations)
            validated.append(seq)
        except ValidationError as e:
            raise ValidationError(f"Sequence {i}: {str(e)}") from e

    return validated


def validate_probability_vector(
    probs: NDArray[np.float64], name: str = "probabilities"
) -> None:
    """Validate probability vector sums to 1 and is non-negative."""
    if not isinstance(probs, np.ndarray):
        raise ValidationError(f"{name} must be numpy array")

    if probs.ndim != 1:
        raise ValidationError(f"{name} must be 1-dimensional")

    if np.any(probs < 0):
        raise ValidationError(f"{name} must be non-negative")

    if not np.isclose(np.sum(probs), 1.0, rtol=1e-5):
        raise ValidationError(f"{name} must sum to 1")


def validate_probability_matrix(
    matrix: NDArray[np.float64], axis: int = 1, name: str = "probability matrix"
) -> None:
    """Validate probability matrix rows/columns sum to 1."""
    if not isinstance(matrix, np.ndarray):
        raise ValidationError(f"{name} must be numpy array")

    if matrix.ndim != 2:
        raise ValidationError(f"{name} must be 2-dimensional")

    if np.any(matrix < 0):
        raise ValidationError(f"{name} must be non-negative")

    sums = np.sum(matrix, axis=axis)
    if not np.allclose(sums, 1.0, rtol=1e-5):
        raise ValidationError(f"{name} rows/columns must sum to 1")


def validate_hmm_parameters(
    start_probs: NDArray[np.float64],
    transition_probs: NDArray[np.float64],
    emission_probs: Optional[NDArray[np.float64]] = None,
) -> None:
    """Validate complete HMM parameter set."""
    n_states = len(start_probs)

    validate_probability_vector(start_probs, "start_probs")
    validate_probability_matrix(transition_probs, axis=1, name="transition_probs")

    if transition_probs.shape != (n_states, n_states):
        raise IncompatibleShapeError(
            f"transition_probs shape {transition_probs.shape} "
            f"incompatible with n_states={n_states}"
        )

    if emission_probs is not None:
        validate_probability_matrix(emission_probs, axis=1, name="emission_probs")
        if emission_probs.shape[0] != n_states:
            raise IncompatibleShapeError(
                f"emission_probs has {emission_probs.shape[0]} states, "
                f"expected {n_states}"
            )


def validate_training_parameters(n_iter: int, tol: float, verbose: bool) -> None:
    """Validate training parameters."""
    if not isinstance(n_iter, int) or n_iter < 1:
        raise ValidationError("n_iter must be positive integer")

    if not isinstance(tol, (int, float)) or tol <= 0:
        raise ValidationError("tol must be positive number")

    if not isinstance(verbose, bool):
        raise ValidationError("verbose must be boolean")


def validate_sample_parameters(n_samples: int) -> None:
    """Validate sampling parameters."""
    if not isinstance(n_samples, int) or n_samples < 1:
        raise ValidationError("n_samples must be positive integer")


def check_array_finite(array: NDArray, name: str = "array") -> None:
    """Check array contains only finite values."""
    if not np.all(np.isfinite(array)):
        raise ValidationError(f"{name} contains non-finite values")


def check_compatible_shapes(*arrays: NDArray, axis: int = 0) -> None:
    """Check arrays have compatible shapes along specified axis."""
    if len(arrays) < 2:
        return

    reference_shape = arrays[0].shape
    for i, arr in enumerate(arrays[1:], 1):
        if arr.shape[axis] != reference_shape[axis]:
            raise IncompatibleShapeError(
                f"Array {i} shape {arr.shape} incompatible with "
                f"reference shape {reference_shape} along axis {axis}"
            )
