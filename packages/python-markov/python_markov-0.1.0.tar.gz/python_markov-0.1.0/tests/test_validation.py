"""
Tests for input validation utilities.
"""

import numpy as np
import pytest

from markov.exceptions import IncompatibleShapeError, ValidationError
from markov.utils.validation import (
    check_array_finite,
    check_compatible_shapes,
    validate_hmm_parameters,
    validate_n_observations,
    validate_n_states,
    validate_probability_matrix,
    validate_probability_vector,
    validate_sample_parameters,
    validate_sequence,
    validate_sequences,
    validate_training_parameters,
)


class TestValidateNStates:
    """Test n_states parameter validation."""

    def test_valid_n_states(self):
        """Test valid n_states values."""
        validate_n_states(1)
        validate_n_states(5)
        validate_n_states(100)

    def test_invalid_type(self):
        """Test invalid type for n_states."""
        with pytest.raises(ValidationError, match="n_states must be an integer"):
            validate_n_states(3.5)

        with pytest.raises(ValidationError, match="n_states must be an integer"):
            validate_n_states("3")

    def test_invalid_value(self):
        """Test invalid values for n_states."""
        with pytest.raises(ValidationError, match="n_states must be positive"):
            validate_n_states(0)

        with pytest.raises(ValidationError, match="n_states must be positive"):
            validate_n_states(-1)


class TestValidateNObservations:
    """Test n_observations parameter validation."""

    def test_valid_n_observations(self):
        """Test valid n_observations values."""
        validate_n_observations(None)
        validate_n_observations(1)
        validate_n_observations(10)

    def test_invalid_type(self):
        """Test invalid type for n_observations."""
        with pytest.raises(ValidationError, match="n_observations must be an integer"):
            validate_n_observations(3.5)

    def test_invalid_value(self):
        """Test invalid values for n_observations."""
        with pytest.raises(ValidationError, match="n_observations must be positive"):
            validate_n_observations(0)

        with pytest.raises(ValidationError, match="n_observations must be positive"):
            validate_n_observations(-1)


class TestValidateSequence:
    """Test single sequence validation."""

    def test_valid_sequence(self):
        """Test valid sequences."""
        # Valid discrete sequence
        seq = np.array([0, 1, 2, 1])
        validate_sequence(seq, n_observations=3)

        # Valid continuous sequence
        seq = np.array([1.5, 2.3, -0.7])
        validate_sequence(seq)

    def test_invalid_type(self):
        """Test invalid sequence types."""
        with pytest.raises(ValidationError, match="Sequence must be numpy array"):
            validate_sequence([0, 1, 2])

        with pytest.raises(ValidationError, match="Sequence must be numpy array"):
            validate_sequence("abc")

    def test_invalid_dimensions(self):
        """Test invalid sequence dimensions."""
        # 2D array
        seq = np.array([[0, 1], [2, 3]])
        with pytest.raises(ValidationError, match="Sequence must be 1-dimensional"):
            validate_sequence(seq)

        # 0D array
        seq = np.array(5)
        with pytest.raises(ValidationError, match="Sequence must be 1-dimensional"):
            validate_sequence(seq)

    def test_empty_sequence(self):
        """Test empty sequence."""
        seq = np.array([])
        with pytest.raises(ValidationError, match="Sequence cannot be empty"):
            validate_sequence(seq)

    def test_discrete_validation(self):
        """Test discrete sequence specific validation."""
        # Non-integer values
        seq = np.array([0.5, 1.2, 2.8])
        with pytest.raises(
            ValidationError, match="Discrete sequences must contain integers"
        ):
            validate_sequence(seq, n_observations=3)

        # Out of range values
        seq = np.array([0, 1, 3])  # 3 is out of range for n_observations=3
        with pytest.raises(ValidationError, match="Observations must be in range"):
            validate_sequence(seq, n_observations=3)

        # Negative values
        seq = np.array([-1, 0, 1])
        with pytest.raises(ValidationError, match="Observations must be in range"):
            validate_sequence(seq, n_observations=3)


class TestValidateSequences:
    """Test multiple sequences validation."""

    def test_valid_sequences_list(self):
        """Test valid sequence lists."""
        sequences = [np.array([0, 1, 2]), np.array([2, 1, 0, 1])]
        result = validate_sequences(sequences, n_observations=3)
        assert len(result) == 2
        assert np.array_equal(result[0], np.array([0, 1, 2]))

    def test_valid_sequences_2d_array(self):
        """Test valid 2D array input."""
        # This should work for sequences of equal length
        sequences = np.array([[0, 1, 2], [2, 1, 0]])
        result = validate_sequences(sequences, n_observations=3)
        assert len(result) == 2

    def test_valid_sequences_1d_array(self):
        """Test valid 1D array input (single sequence)."""
        sequences = np.array([0, 1, 2])
        result = validate_sequences(sequences, n_observations=3)
        assert len(result) == 1
        assert np.array_equal(result[0], sequences)

    def test_invalid_type(self):
        """Test invalid sequence types."""
        with pytest.raises(
            ValidationError, match="Sequences must be list or numpy array"
        ):
            validate_sequences("invalid")

        with pytest.raises(
            ValidationError, match="Sequences must be list or numpy array"
        ):
            validate_sequences(123)

    def test_invalid_dimensions(self):
        """Test invalid array dimensions."""
        # 3D array
        sequences = np.array([[[0, 1], [2, 3]], [[1, 2], [3, 4]]])
        with pytest.raises(ValidationError, match="Array sequences must be 1D or 2D"):
            validate_sequences(sequences)

    def test_empty_sequences(self):
        """Test empty sequence list."""
        with pytest.raises(ValidationError, match="Must provide at least one sequence"):
            validate_sequences([])

    def test_invalid_individual_sequence(self):
        """Test error in individual sequence."""
        sequences = [np.array([0, 1, 2]), np.array([0, 1, 5])]  # 5 is out of range
        with pytest.raises(ValidationError, match="Sequence 1"):
            validate_sequences(sequences, n_observations=3)


class TestValidateProbabilityVector:
    """Test probability vector validation."""

    def test_valid_vector(self):
        """Test valid probability vectors."""
        probs = np.array([0.3, 0.7])
        validate_probability_vector(probs)

        probs = np.array([0.2, 0.3, 0.5])
        validate_probability_vector(probs)

    def test_invalid_type(self):
        """Test invalid types."""
        with pytest.raises(ValidationError, match="probabilities must be numpy array"):
            validate_probability_vector([0.3, 0.7])

    def test_invalid_dimensions(self):
        """Test invalid dimensions."""
        probs = np.array([[0.3, 0.7], [0.4, 0.6]])
        with pytest.raises(
            ValidationError, match="probabilities must be 1-dimensional"
        ):
            validate_probability_vector(probs)

    def test_negative_values(self):
        """Test negative probability values."""
        probs = np.array([0.3, -0.1, 0.8])
        with pytest.raises(ValidationError, match="probabilities must be non-negative"):
            validate_probability_vector(probs)

    def test_not_sum_to_one(self):
        """Test probabilities that don't sum to 1."""
        probs = np.array([0.3, 0.5])  # sums to 0.8
        with pytest.raises(ValidationError, match="probabilities must sum to 1"):
            validate_probability_vector(probs)

        probs = np.array([0.6, 0.6])  # sums to 1.2
        with pytest.raises(ValidationError, match="probabilities must sum to 1"):
            validate_probability_vector(probs)

    def test_custom_name(self):
        """Test custom parameter name in error messages."""
        probs = np.array([0.3, 0.5])
        with pytest.raises(ValidationError, match="start_probs must sum to 1"):
            validate_probability_vector(probs, name="start_probs")


class TestValidateProbabilityMatrix:
    """Test probability matrix validation."""

    def test_valid_matrix(self):
        """Test valid probability matrices."""
        # Row stochastic
        matrix = np.array([[0.3, 0.7], [0.6, 0.4]])
        validate_probability_matrix(matrix, axis=1)

        # Column stochastic
        matrix = np.array([[0.3, 0.6], [0.7, 0.4]])
        validate_probability_matrix(matrix, axis=0)

    def test_invalid_type(self):
        """Test invalid types."""
        with pytest.raises(
            ValidationError, match="probability matrix must be numpy array"
        ):
            validate_probability_matrix([[0.3, 0.7], [0.6, 0.4]])

    def test_invalid_dimensions(self):
        """Test invalid dimensions."""
        matrix = np.array([0.3, 0.7])  # 1D
        with pytest.raises(
            ValidationError, match="probability matrix must be 2-dimensional"
        ):
            validate_probability_matrix(matrix)

    def test_negative_values(self):
        """Test negative values."""
        matrix = np.array([[0.3, 0.7], [-0.1, 1.1]])
        with pytest.raises(
            ValidationError, match="probability matrix must be non-negative"
        ):
            validate_probability_matrix(matrix)

    def test_not_sum_to_one(self):
        """Test rows/columns that don't sum to 1."""
        matrix = np.array([[0.3, 0.5], [0.6, 0.4]])  # first row sums to 0.8
        with pytest.raises(
            ValidationError, match="probability matrix rows/columns must sum to 1"
        ):
            validate_probability_matrix(matrix, axis=1)

    def test_custom_name(self):
        """Test custom parameter name in error messages."""
        matrix = np.array([[0.3, 0.5], [0.6, 0.4]])
        with pytest.raises(
            ValidationError, match="transition_matrix rows/columns must sum to 1"
        ):
            validate_probability_matrix(matrix, axis=1, name="transition_matrix")


class TestValidateHMMParameters:
    """Test complete HMM parameter validation."""

    def test_valid_parameters(self):
        """Test valid HMM parameters."""
        start_probs = np.array([0.3, 0.7])
        transition_probs = np.array([[0.8, 0.2], [0.4, 0.6]])
        emission_probs = np.array([[0.5, 0.5], [0.3, 0.7]])

        validate_hmm_parameters(start_probs, transition_probs, emission_probs)

    def test_valid_without_emission(self):
        """Test valid parameters without emission probabilities."""
        start_probs = np.array([0.3, 0.7])
        transition_probs = np.array([[0.8, 0.2], [0.4, 0.6]])

        validate_hmm_parameters(start_probs, transition_probs)

    def test_incompatible_transition_shape(self):
        """Test incompatible transition matrix shape."""
        start_probs = np.array([0.3, 0.7])  # 2 states
        transition_probs = np.array(
            [[0.5, 0.3, 0.2], [0.4, 0.3, 0.3], [0.2, 0.3, 0.5]]
        )  # 3x3

        with pytest.raises(
            IncompatibleShapeError, match="transition_probs shape.*incompatible"
        ):
            validate_hmm_parameters(start_probs, transition_probs)

    def test_incompatible_emission_shape(self):
        """Test incompatible emission matrix shape."""
        start_probs = np.array([0.3, 0.7])  # 2 states
        transition_probs = np.array([[0.8, 0.2], [0.4, 0.6]])
        emission_probs = np.array([[0.5, 0.5], [0.3, 0.7], [0.4, 0.6]])  # 3 states

        with pytest.raises(
            IncompatibleShapeError, match="emission_probs has 3 states, expected 2"
        ):
            validate_hmm_parameters(start_probs, transition_probs, emission_probs)


class TestValidateTrainingParameters:
    """Test training parameter validation."""

    def test_valid_parameters(self):
        """Test valid training parameters."""
        validate_training_parameters(100, 1e-6, True)
        validate_training_parameters(50, 0.001, False)

    def test_invalid_n_iter(self):
        """Test invalid n_iter values."""
        with pytest.raises(ValidationError, match="n_iter must be positive integer"):
            validate_training_parameters(0, 1e-6, True)

        with pytest.raises(ValidationError, match="n_iter must be positive integer"):
            validate_training_parameters(3.5, 1e-6, True)

    def test_invalid_tol(self):
        """Test invalid tolerance values."""
        with pytest.raises(ValidationError, match="tol must be positive number"):
            validate_training_parameters(100, 0, True)

        with pytest.raises(ValidationError, match="tol must be positive number"):
            validate_training_parameters(100, -1e-6, True)

    def test_invalid_verbose(self):
        """Test invalid verbose values."""
        with pytest.raises(ValidationError, match="verbose must be boolean"):
            validate_training_parameters(100, 1e-6, "True")


class TestValidateSampleParameters:
    """Test sampling parameter validation."""

    def test_valid_parameters(self):
        """Test valid sampling parameters."""
        validate_sample_parameters(1)
        validate_sample_parameters(100)

    def test_invalid_n_samples(self):
        """Test invalid n_samples values."""
        with pytest.raises(ValidationError, match="n_samples must be positive integer"):
            validate_sample_parameters(0)

        with pytest.raises(ValidationError, match="n_samples must be positive integer"):
            validate_sample_parameters(3.5)


class TestCheckArrayFinite:
    """Test finite array validation."""

    def test_finite_array(self):
        """Test finite arrays."""
        arr = np.array([1.0, 2.0, 3.0])
        check_array_finite(arr)  # Should not raise

    def test_infinite_values(self):
        """Test arrays with infinite values."""
        arr = np.array([1.0, np.inf, 3.0])
        with pytest.raises(ValidationError, match="array contains non-finite values"):
            check_array_finite(arr)

    def test_nan_values(self):
        """Test arrays with NaN values."""
        arr = np.array([1.0, np.nan, 3.0])
        with pytest.raises(ValidationError, match="array contains non-finite values"):
            check_array_finite(arr)

    def test_custom_name(self):
        """Test custom array name in error messages."""
        arr = np.array([1.0, np.inf, 3.0])
        with pytest.raises(
            ValidationError, match="probabilities contains non-finite values"
        ):
            check_array_finite(arr, name="probabilities")


class TestCheckCompatibleShapes:
    """Test shape compatibility validation."""

    def test_compatible_shapes_axis0(self):
        """Test compatible shapes along axis 0."""
        arr1 = np.zeros((5, 3))
        arr2 = np.zeros((5, 4))
        arr3 = np.zeros((5, 2))
        check_compatible_shapes(arr1, arr2, arr3, axis=0)  # Should not raise

    def test_compatible_shapes_axis1(self):
        """Test compatible shapes along axis 1."""
        arr1 = np.zeros((3, 5))
        arr2 = np.zeros((4, 5))
        arr3 = np.zeros((2, 5))
        check_compatible_shapes(arr1, arr2, arr3, axis=1)  # Should not raise

    def test_incompatible_shapes(self):
        """Test incompatible shapes."""
        arr1 = np.zeros((5, 3))
        arr2 = np.zeros((4, 3))  # Different size along axis 0

        with pytest.raises(IncompatibleShapeError, match="Array 1 shape.*incompatible"):
            check_compatible_shapes(arr1, arr2, axis=0)

    def test_single_array(self):
        """Test with single array (should not raise)."""
        arr1 = np.zeros((5, 3))
        check_compatible_shapes(arr1, axis=0)  # Should not raise

    def test_no_arrays(self):
        """Test with no arrays (should not raise)."""
        check_compatible_shapes(axis=0)  # Should not raise


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_small_probabilities(self):
        """Test very small but valid probabilities."""
        probs = np.array([1e-10, 1.0 - 1e-10])
        validate_probability_vector(probs)  # Should not raise

    def test_probability_tolerance(self):
        """Test probability sum tolerance."""
        # Just within tolerance
        probs = np.array([0.3, 0.7 + 1e-6])  # Sum = 1.000001
        validate_probability_vector(probs)  # Should not raise

        # Just outside tolerance
        probs = np.array([0.3, 0.7 + 1e-4])  # Sum = 1.0001
        with pytest.raises(ValidationError):
            validate_probability_vector(probs)

    def test_large_sequences(self):
        """Test validation with large sequences."""
        large_seq = np.zeros(10000, dtype=int)
        validate_sequence(large_seq, n_observations=1)  # Should not raise

    def test_extreme_values(self):
        """Test with extreme but valid values."""
        # Very large sequence values
        seq = np.array([999, 998, 997])
        validate_sequence(seq, n_observations=1000)  # Should not raise

        # Very large number of states/observations
        validate_n_states(10000)
        validate_n_observations(10000)
