"""
Mathematical utilities for numerical stability in HMM computations.
"""

import warnings
from typing import Union

import numpy as np
from numpy.typing import NDArray

# Constants for numerical stability
LOG_ZERO = -np.inf
EPSILON = 1e-12
MAX_LOG_EXP = 700.0  # Prevents overflow in exp()


def log_sum_exp(log_probs: NDArray[np.float64]) -> float:
    """
    Compute log(sum(exp(x))) in a numerically stable way.

    Args:
        log_probs: Array of log probabilities

    Returns:
        Log of sum of exponentials
    """
    if len(log_probs) == 0:
        return LOG_ZERO

    max_log = np.max(log_probs)

    # Handle case where all probabilities are zero
    if max_log == LOG_ZERO:
        return LOG_ZERO

    # Prevent overflow by subtracting max
    if max_log > MAX_LOG_EXP:
        warnings.warn("Large log probabilities detected, potential numerical issues")

    return max_log + np.log(np.sum(np.exp(log_probs - max_log)))


def log_sum_exp_axis(log_probs: NDArray[np.float64], axis: int) -> NDArray[np.float64]:
    """
    Compute log(sum(exp(x))) along specified axis in numerically stable way.

    Args:
        log_probs: Array of log probabilities
        axis: Axis along which to compute

    Returns:
        Log of sum of exponentials along axis
    """
    max_log = np.max(log_probs, axis=axis, keepdims=True)

    # Handle -inf values
    inf_mask = np.isinf(max_log)
    max_log = np.where(inf_mask, 0, max_log)

    result = max_log.squeeze(axis) + np.log(
        np.sum(np.exp(log_probs - max_log), axis=axis)
    )

    # Set -inf where all inputs were -inf
    if np.any(inf_mask):
        result = np.where(inf_mask.squeeze(axis), LOG_ZERO, result)

    return result


def normalize_log_probs(log_probs: NDArray[np.float64]) -> NDArray[np.float64]:
    """
    Normalize log probabilities to sum to 1 in probability space.

    Args:
        log_probs: Array of log probabilities

    Returns:
        Normalized log probabilities
    """
    log_sum = log_sum_exp(log_probs)
    if log_sum == LOG_ZERO:
        # If all probabilities are zero, return uniform
        return np.full_like(log_probs, -np.log(len(log_probs)))

    return log_probs - log_sum


def normalize_log_probs_axis(
    log_probs: NDArray[np.float64], axis: int
) -> NDArray[np.float64]:
    """
    Normalize log probabilities along specified axis.

    Args:
        log_probs: Array of log probabilities
        axis: Axis along which to normalize

    Returns:
        Normalized log probabilities
    """
    log_sum = log_sum_exp_axis(log_probs, axis)
    return log_probs - np.expand_dims(log_sum, axis)


def safe_log(x: Union[float, NDArray[np.float64]]) -> Union[float, NDArray[np.float64]]:
    """
    Compute log while avoiding log(0).

    Args:
        x: Input value(s)

    Returns:
        Log of input, with log(0) = -inf
    """
    x = np.asarray(x)
    return np.where(x > 0, np.log(x), LOG_ZERO)


def safe_exp(
    log_x: Union[float, NDArray[np.float64]],
) -> Union[float, NDArray[np.float64]]:
    """
    Compute exp while preventing overflow.

    Args:
        log_x: Log values

    Returns:
        Exponential, clipped to prevent overflow
    """
    log_x = np.asarray(log_x)
    return np.exp(np.clip(log_x, -MAX_LOG_EXP, MAX_LOG_EXP))


def log_dot_product(
    log_A: NDArray[np.float64], log_B: NDArray[np.float64]
) -> NDArray[np.float64]:
    """
    Compute log(A @ exp(B)) in numerically stable way.

    This is useful for matrix-vector products in log space.

    Args:
        log_A: Log of matrix A
        log_B: Log of vector B

    Returns:
        Log of matrix-vector product
    """
    # Add dimensions for broadcasting
    log_A_expanded = log_A[:, :, np.newaxis]
    log_B_expanded = log_B[np.newaxis, :, np.newaxis]

    # Compute log(A * B) for each element
    log_products = log_A_expanded + log_B_expanded

    # Sum along middle dimension in log space
    return log_sum_exp_axis(log_products, axis=1).squeeze()


def check_probability_matrix(
    matrix: NDArray[np.float64], axis: int = 1, name: str = "matrix"
) -> None:
    """
    Validate that matrix rows/columns sum to 1 and are non-negative.

    Args:
        matrix: Probability matrix to check
        axis: Axis along which probabilities should sum to 1
        name: Name for error messages
    """
    if np.any(matrix < 0):
        raise ValueError(f"{name} contains negative values")

    if np.any(matrix > 1):
        raise ValueError(f"{name} contains values > 1")

    sums = np.sum(matrix, axis=axis)
    if not np.allclose(sums, 1.0, rtol=1e-10):
        raise ValueError(f"{name} rows/columns do not sum to 1")


def make_stochastic(matrix: NDArray[np.float64], axis: int = 1) -> NDArray[np.float64]:
    """
    Normalize matrix to make it row/column stochastic.

    Args:
        matrix: Input matrix
        axis: Axis along which to normalize

    Returns:
        Normalized stochastic matrix
    """
    matrix = np.maximum(matrix, EPSILON)  # Prevent division by zero
    sums = np.sum(matrix, axis=axis, keepdims=True)
    return matrix / sums


def log_likelihood_change(old_ll: float, new_ll: float) -> float:
    """
    Compute relative change in log-likelihood for convergence checking.

    Args:
        old_ll: Previous log-likelihood
        new_ll: Current log-likelihood

    Returns:
        Relative change in log-likelihood
    """
    if old_ll == LOG_ZERO and new_ll == LOG_ZERO:
        return 0.0

    if old_ll == LOG_ZERO:
        return np.inf

    return abs(new_ll - old_ll) / abs(old_ll)


def random_stochastic_matrix(
    n_rows: int, n_cols: int, random_state: int = None
) -> NDArray[np.float64]:
    """
    Generate random row-stochastic matrix.

    Args:
        n_rows: Number of rows
        n_cols: Number of columns
        random_state: Random seed

    Returns:
        Random stochastic matrix
    """
    if random_state is not None:
        np.random.seed(random_state)

    matrix = np.random.random((n_rows, n_cols))
    return make_stochastic(matrix, axis=1)


def weighted_average(
    values: NDArray[np.float64], weights: NDArray[np.float64]
) -> float:
    """
    Compute weighted average with numerical stability.

    Args:
        values: Values to average
        weights: Weights (should sum to 1)

    Returns:
        Weighted average
    """
    weights = np.maximum(weights, EPSILON)
    weights = weights / np.sum(weights)
    return np.sum(values * weights)
