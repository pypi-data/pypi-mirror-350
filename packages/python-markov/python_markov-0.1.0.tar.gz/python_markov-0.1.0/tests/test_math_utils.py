"""
Tests for mathematical utilities module.
"""

import warnings

import numpy as np
import pytest

from markov.utils.math_utils import (
    EPSILON,
    LOG_ZERO,
    MAX_LOG_EXP,
    check_probability_matrix,
    log_dot_product,
    log_likelihood_change,
    log_sum_exp,
    log_sum_exp_axis,
    make_stochastic,
    normalize_log_probs,
    normalize_log_probs_axis,
    random_stochastic_matrix,
    safe_exp,
    safe_log,
    weighted_average,
)


class TestLogSumExp:
    """Tests for log_sum_exp function."""

    def test_empty_array(self):
        """Test log_sum_exp with empty array."""
        result = log_sum_exp(np.array([]))
        assert result == LOG_ZERO

    def test_single_value(self):
        """Test log_sum_exp with single value."""
        x = 2.5
        result = log_sum_exp(np.array([x]))
        assert np.isclose(result, x)

    def test_two_values(self):
        """Test log_sum_exp with two values."""
        x1, x2 = 1.0, 2.0
        expected = np.log(np.exp(x1) + np.exp(x2))
        result = log_sum_exp(np.array([x1, x2]))
        assert np.isclose(result, expected)

    def test_all_zero_log_probs(self):
        """Test with all -inf (zero probabilities)."""
        log_probs = np.array([LOG_ZERO, LOG_ZERO, LOG_ZERO])
        result = log_sum_exp(log_probs)
        assert result == LOG_ZERO

    def test_numerical_stability(self):
        """Test numerically challenging case."""
        # Large values that would overflow without stability measures
        log_probs = np.array([1000.0, 1001.0, 999.0])
        result = log_sum_exp(log_probs)

        # Should not be inf or nan
        assert np.isfinite(result)

        # Should be dominated by largest value
        assert result > 1001.0

    def test_mixed_finite_infinite(self):
        """Test mix of finite and -inf values."""
        log_probs = np.array([1.0, LOG_ZERO, 2.0, LOG_ZERO])
        expected = np.log(np.exp(1.0) + np.exp(2.0))
        result = log_sum_exp(log_probs)
        assert np.isclose(result, expected)

    def test_warning_on_large_values(self):
        """Test warning is issued for very large values."""
        log_probs = np.array([800.0, 801.0])

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            log_sum_exp(log_probs)
            assert len(w) == 1
            assert "Large log probabilities" in str(w[0].message)


class TestLogSumExpAxis:
    """Tests for log_sum_exp_axis function."""

    def test_2d_array_axis_0(self):
        """Test log_sum_exp along axis 0."""
        log_probs = np.array([[1.0, 2.0], [3.0, 4.0]])
        result = log_sum_exp_axis(log_probs, axis=0)

        expected = np.array(
            [log_sum_exp(np.array([1.0, 3.0])), log_sum_exp(np.array([2.0, 4.0]))]
        )

        assert np.allclose(result, expected)

    def test_2d_array_axis_1(self):
        """Test log_sum_exp along axis 1."""
        log_probs = np.array([[1.0, 2.0], [3.0, 4.0]])
        result = log_sum_exp_axis(log_probs, axis=1)

        expected = np.array(
            [log_sum_exp(np.array([1.0, 2.0])), log_sum_exp(np.array([3.0, 4.0]))]
        )

        assert np.allclose(result, expected)

    def test_with_infinite_values(self):
        """Test handling of -inf values."""
        log_probs = np.array([[LOG_ZERO, 1.0], [2.0, LOG_ZERO]])
        result = log_sum_exp_axis(log_probs, axis=1)

        expected = np.array([1.0, 2.0])
        assert np.allclose(result, expected)

    def test_all_infinite_row(self):
        """Test row with all -inf values."""
        log_probs = np.array([[LOG_ZERO, LOG_ZERO], [1.0, 2.0]])
        result = log_sum_exp_axis(log_probs, axis=1)

        assert result[0] == LOG_ZERO
        assert np.isfinite(result[1])


class TestNormalizeLogProbs:
    """Tests for log probability normalization functions."""

    def test_normalize_log_probs_basic(self):
        """Test basic log probability normalization."""
        log_probs = np.array([1.0, 2.0, 3.0])
        result = normalize_log_probs(log_probs)

        # Check that probabilities sum to 1
        probs = np.exp(result)
        assert np.isclose(np.sum(probs), 1.0)

        # Check relative ordering preserved
        assert result[0] < result[1] < result[2]

    def test_normalize_all_zero_probs(self):
        """Test normalization when all probabilities are zero."""
        log_probs = np.array([LOG_ZERO, LOG_ZERO, LOG_ZERO])
        result = normalize_log_probs(log_probs)

        # Should return uniform distribution
        expected = -np.log(3.0)
        assert np.allclose(result, expected)

    def test_normalize_log_probs_axis(self):
        """Test axis-wise normalization."""
        log_probs = np.array([[1.0, 2.0], [3.0, 4.0]])
        result = normalize_log_probs_axis(log_probs, axis=1)

        # Each row should sum to 1 in probability space
        for i in range(2):
            row_probs = np.exp(result[i])
            assert np.isclose(np.sum(row_probs), 1.0)


class TestSafeOperations:
    """Tests for safe mathematical operations."""

    def test_safe_log_positive(self):
        """Test safe_log with positive values."""
        x = np.array([1.0, 2.0, np.e])
        result = safe_log(x)
        expected = np.log(x)
        assert np.allclose(result, expected)

    def test_safe_log_zero(self):
        """Test safe_log with zero values."""
        result = safe_log(0.0)
        assert result == LOG_ZERO

        x = np.array([1.0, 0.0, 2.0])
        result = safe_log(x)
        assert result[1] == LOG_ZERO
        assert np.isfinite(result[0])
        assert np.isfinite(result[2])

    def test_safe_log_negative(self):
        """Test safe_log with negative values."""
        result = safe_log(-1.0)
        assert result == LOG_ZERO

        x = np.array([1.0, -0.5, 2.0])
        result = safe_log(x)
        assert result[1] == LOG_ZERO

    def test_safe_exp_normal(self):
        """Test safe_exp with normal values."""
        x = np.array([0.0, 1.0, 2.0])
        result = safe_exp(x)
        expected = np.exp(x)
        assert np.allclose(result, expected)

    def test_safe_exp_large_values(self):
        """Test safe_exp with very large values."""
        x = 1000.0
        result = safe_exp(x)
        assert np.isfinite(result)

        # Should be clipped to prevent overflow
        assert result == np.exp(MAX_LOG_EXP)

    def test_safe_exp_small_values(self):
        """Test safe_exp with very small values."""
        x = -1000.0
        result = safe_exp(x)
        assert result == np.exp(-MAX_LOG_EXP)


class TestProbabilityMatrixOps:
    """Tests for probability matrix operations."""

    def test_check_probability_matrix_valid(self):
        """Test validation of valid probability matrix."""
        matrix = np.array([[0.6, 0.4], [0.3, 0.7]])
        # Should not raise exception
        check_probability_matrix(matrix, axis=1)

    def test_check_probability_matrix_negative(self):
        """Test detection of negative values."""
        matrix = np.array([[0.6, -0.1], [0.3, 0.7]])
        with pytest.raises(ValueError, match="contains negative values"):
            check_probability_matrix(matrix)

    def test_check_probability_matrix_values_too_large(self):
        """Test detection of values > 1."""
        matrix = np.array([[1.5, 0.4], [0.3, 0.7]])
        with pytest.raises(ValueError, match="contains values > 1"):
            check_probability_matrix(matrix)

    def test_check_probability_matrix_not_stochastic(self):
        """Test detection of non-stochastic matrix."""
        matrix = np.array([[0.5, 0.3], [0.2, 0.8]])  # Rows don't sum to 1
        with pytest.raises(ValueError, match="do not sum to 1"):
            check_probability_matrix(matrix, axis=1)

    def test_make_stochastic_rows(self):
        """Test making matrix row-stochastic."""
        matrix = np.array([[2.0, 1.0], [3.0, 6.0]])
        result = make_stochastic(matrix, axis=1)

        # Check rows sum to 1
        row_sums = np.sum(result, axis=1)
        assert np.allclose(row_sums, 1.0)

        # Check relative proportions preserved
        assert np.isclose(result[0, 0] / result[0, 1], 2.0)
        assert np.isclose(result[1, 0] / result[1, 1], 0.5)

    def test_make_stochastic_columns(self):
        """Test making matrix column-stochastic."""
        matrix = np.array([[2.0, 1.0], [3.0, 6.0]])
        result = make_stochastic(matrix, axis=0)

        # Check columns sum to 1
        col_sums = np.sum(result, axis=0)
        assert np.allclose(col_sums, 1.0)

    def test_make_stochastic_zero_rows(self):
        """Test handling of zero rows."""
        matrix = np.array([[0.0, 0.0], [3.0, 6.0]])
        result = make_stochastic(matrix, axis=1)

        # Zero row should become uniform
        assert np.allclose(result[0], 0.5)
        # Non-zero row should be normalized
        assert np.allclose(np.sum(result[1]), 1.0)


class TestRandomStochasticMatrix:
    """Tests for random stochastic matrix generation."""

    def test_shape(self):
        """Test output shape."""
        n_rows, n_cols = 3, 4
        matrix = random_stochastic_matrix(n_rows, n_cols)
        assert matrix.shape == (n_rows, n_cols)

    def test_stochastic_property(self):
        """Test that output is row-stochastic."""
        matrix = random_stochastic_matrix(5, 3)
        row_sums = np.sum(matrix, axis=1)
        assert np.allclose(row_sums, 1.0)

    def test_random_state_reproducibility(self):
        """Test reproducibility with random state."""
        matrix1 = random_stochastic_matrix(3, 3, random_state=42)
        matrix2 = random_stochastic_matrix(3, 3, random_state=42)
        assert np.allclose(matrix1, matrix2)

    def test_positive_values(self):
        """Test all values are positive."""
        matrix = random_stochastic_matrix(4, 4)
        assert np.all(matrix > 0)


class TestLogDotProduct:
    """Tests for log-space dot product."""

    def test_simple_case(self):
        """Test simple matrix-vector product."""
        # A = [[0.5, 0.3], [0.2, 0.7]]
        # B = [0.6, 0.4]
        log_A = safe_log(np.array([[0.5, 0.3], [0.2, 0.7]]))
        log_B = safe_log(np.array([0.6, 0.4]))

        result = log_dot_product(log_A, log_B)

        # Compare with direct computation
        A = np.exp(log_A)
        B = np.exp(log_B)
        expected = safe_log(A @ B)

        assert np.allclose(result, expected)

    def test_with_zeros(self):
        """Test handling of zero probabilities."""
        log_A = np.array([[safe_log(0.5), LOG_ZERO], [LOG_ZERO, safe_log(0.7)]])
        log_B = np.array([safe_log(0.6), safe_log(0.4)])

        result = log_dot_product(log_A, log_B)

        # First element should be log(0.5 * 0.6) = log(0.3)
        # Second element should be log(0.7 * 0.4) = log(0.28)
        expected = np.array([safe_log(0.3), safe_log(0.28)])

        assert np.allclose(result, expected)


class TestUtilityFunctions:
    """Tests for utility functions."""

    def test_log_likelihood_change_normal(self):
        """Test log-likelihood change calculation."""
        old_ll = -100.0
        new_ll = -95.0
        change = log_likelihood_change(old_ll, new_ll)
        expected = abs(new_ll - old_ll) / abs(old_ll)
        assert np.isclose(change, expected)

    def test_log_likelihood_change_both_zero(self):
        """Test when both log-likelihoods are -inf."""
        change = log_likelihood_change(LOG_ZERO, LOG_ZERO)
        assert change == 0.0

    def test_log_likelihood_change_old_zero(self):
        """Test when old log-likelihood is -inf."""
        change = log_likelihood_change(LOG_ZERO, -50.0)
        assert change == np.inf

    def test_weighted_average_basic(self):
        """Test basic weighted average."""
        values = np.array([1.0, 2.0, 3.0])
        weights = np.array([0.5, 0.3, 0.2])

        result = weighted_average(values, weights)
        expected = np.sum(values * weights)

        assert np.isclose(result, expected)

    def test_weighted_average_normalization(self):
        """Test weighted average with unnormalized weights."""
        values = np.array([2.0, 4.0])
        weights = np.array([2.0, 3.0])  # Sum to 5, not 1

        result = weighted_average(values, weights)
        expected = (2.0 * 2.0 + 4.0 * 3.0) / 5.0

        assert np.isclose(result, expected)

    def test_weighted_average_zero_weights(self):
        """Test weighted average with some zero weights."""
        values = np.array([1.0, 2.0, 3.0])
        weights = np.array([0.0, 0.6, 0.4])

        result = weighted_average(values, weights)
        expected = 2.0 * 0.6 + 3.0 * 0.4  # First value ignored

        assert np.isclose(result, expected)


class TestConstants:
    """Tests for mathematical constants."""

    def test_log_zero(self):
        """Test LOG_ZERO constant."""
        assert LOG_ZERO == -np.inf

    def test_epsilon(self):
        """Test EPSILON constant."""
        assert EPSILON > 0
        assert EPSILON < 1e-10

    def test_max_log_exp(self):
        """Test MAX_LOG_EXP prevents overflow."""
        # Should be safe to exponentiate
        result = np.exp(MAX_LOG_EXP)
        assert np.isfinite(result)

        # Should prevent overflow for larger values
        large_val = MAX_LOG_EXP + 100
        clipped = np.clip(large_val, -MAX_LOG_EXP, MAX_LOG_EXP)
        assert clipped == MAX_LOG_EXP


class TestEdgeCases:
    """Tests for edge cases and error conditions."""

    def test_empty_arrays(self):
        """Test functions with empty arrays where applicable."""
        empty = np.array([])

        assert log_sum_exp(empty) == LOG_ZERO

        # Other functions should handle empty arrays gracefully
        result = safe_log(empty)
        assert len(result) == 0

        result = safe_exp(empty)
        assert len(result) == 0

    def test_single_element_arrays(self):
        """Test functions with single-element arrays."""
        single = np.array([2.5])

        assert np.isclose(log_sum_exp(single), 2.5)
        assert np.isclose(safe_log(np.exp(single[0])), single[0])
        assert np.isclose(safe_exp(single[0]), np.exp(single[0]))

    def test_very_large_matrices(self):
        """Test with reasonably large matrices."""
        # Test that functions work with larger inputs
        large_matrix = random_stochastic_matrix(100, 50, random_state=42)

        # Should be stochastic
        row_sums = np.sum(large_matrix, axis=1)
        assert np.allclose(row_sums, 1.0)

        # Should pass validation
        check_probability_matrix(large_matrix, axis=1)

    def test_numerical_precision(self):
        """Test numerical precision with challenging cases."""
        # Very small probabilities
        small_probs = np.array([1e-10, 1e-12, 1e-8])
        log_probs = safe_log(small_probs)

        # Should not be -inf
        assert np.all(np.isfinite(log_probs))

        # Should maintain relative ordering
        assert log_probs[1] < log_probs[0] < log_probs[2]
