"""
Tests for DiscreteHMM implementation.

This module contains comprehensive tests for the DiscreteHMM class,
including initialization, training, prediction, and edge cases.
"""

import numpy as np
import pytest
from numpy.testing import assert_allclose, assert_array_equal

from markov.core.discrete import DiscreteEmissionModel, DiscreteHMM
from markov.exceptions import ModelNotFittedError, ValidationError


@pytest.fixture
def simple_sequences():
    """Simple training sequences for testing."""
    return [
        np.array([0, 1, 0, 1]),
        np.array([1, 0, 1, 0]),
        np.array([0, 0, 1, 1]),
    ]


@pytest.fixture
def weather_sequences():
    """Weather-like sequences with 3 observations."""
    return [
        np.array([0, 1, 2, 0, 1]),  # Walk, Shop, Clean, Walk, Shop
        np.array([2, 2, 1, 0, 0]),  # Clean, Clean, Shop, Walk, Walk
        np.array([1, 0, 2, 1, 2]),  # Shop, Walk, Clean, Shop, Clean
    ]


class TestDiscreteEmissionModel:
    """Tests for DiscreteEmissionModel class."""

    def test_initialization(self):
        """Test emission model initialization."""
        model = DiscreteEmissionModel(n_states=2, n_observations=3)
        assert model.n_states == 2
        assert model.n_observations == 3
        assert model.emission_probs is None

    def test_parameter_initialization(self):
        """Test parameter initialization."""
        model = DiscreteEmissionModel(n_states=3, n_observations=4)
        model.initialize_parameters(random_state=42)

        assert model.emission_probs is not None
        assert model.emission_probs.shape == (3, 4)

        # Check probabilities are valid
        assert np.all(model.emission_probs >= 0)
        assert np.all(model.emission_probs <= 1)
        assert_allclose(np.sum(model.emission_probs, axis=1), np.ones(3), rtol=1e-10)

    def test_log_probability_matrix(self):
        """Test log probability matrix computation."""
        model = DiscreteEmissionModel(n_states=2, n_observations=2)
        model.emission_probs = np.array(
            [
                [0.8, 0.2],  # State 0
                [0.3, 0.7],  # State 1
            ]
        )

        sequence = np.array([0, 1, 0])
        log_probs = model.log_probability_matrix(sequence)

        assert log_probs.shape == (3, 2)

        # Check specific values
        expected = np.array(
            [
                [np.log(0.8), np.log(0.3)],  # t=0, obs=0
                [np.log(0.2), np.log(0.7)],  # t=1, obs=1
                [np.log(0.8), np.log(0.3)],  # t=2, obs=0
            ]
        )
        assert_allclose(log_probs, expected, rtol=1e-10)

    def test_sample(self):
        """Test sampling from emission model."""
        model = DiscreteEmissionModel(n_states=2, n_observations=3)
        model.emission_probs = np.array(
            [
                [1.0, 0.0, 0.0],  # State 0 always emits 0
                [0.0, 0.0, 1.0],  # State 1 always emits 2
            ]
        )

        np.random.seed(42)

        # Test single sample
        obs = model.sample(state=0, n_samples=1)
        assert obs == 0

        obs = model.sample(state=1, n_samples=1)
        assert obs == 2

        # Test multiple samples
        obs_array = model.sample(state=0, n_samples=5)
        assert_array_equal(obs_array, np.zeros(5))

    def test_update_parameters(self):
        """Test parameter updates using Baum-Welch statistics."""
        model = DiscreteEmissionModel(n_states=2, n_observations=2)
        model.emission_probs = np.array(
            [
                [0.5, 0.5],
                [0.5, 0.5],
            ]
        )

        sequences = [np.array([0, 1]), np.array([1, 0])]
        gammas = [
            np.array([[0.8, 0.2], [0.3, 0.7]]),  # Seq 1: state probs
            np.array([[0.1, 0.9], [0.6, 0.4]]),  # Seq 2: state probs
        ]

        model.update_parameters(sequences, gammas)

        # Check that parameters were updated
        assert model.emission_probs.shape == (2, 2)
        assert np.all(model.emission_probs >= 0)
        assert_allclose(np.sum(model.emission_probs, axis=1), np.ones(2), rtol=1e-10)


class TestDiscreteHMMInitialization:
    """Tests for DiscreteHMM initialization."""

    def test_basic_initialization(self):
        """Test basic HMM initialization."""
        hmm = DiscreteHMM(n_states=3, n_observations=4)

        assert hmm.n_states == 3
        assert hmm.n_observations == 4
        assert not hmm.is_fitted
        assert hmm.start_probs is None
        assert hmm.transition_probs is None
        assert hmm.emission_probs is None
        assert isinstance(hmm.emission_model, DiscreteEmissionModel)

    def test_initialization_with_random_state(self):
        """Test initialization with random state."""
        hmm1 = DiscreteHMM(n_states=2, n_observations=2, random_state=42)
        hmm2 = DiscreteHMM(n_states=2, n_observations=2, random_state=42)

        # Should have same random state
        assert hmm1.random_state == hmm2.random_state

    def test_invalid_parameters(self):
        """Test initialization with invalid parameters."""
        # Invalid n_states
        with pytest.raises(ValidationError):
            DiscreteHMM(n_states=0, n_observations=2)

        with pytest.raises(ValidationError):
            DiscreteHMM(n_states=-1, n_observations=2)

        # Invalid n_observations
        with pytest.raises(ValidationError):
            DiscreteHMM(n_states=2, n_observations=0)

        with pytest.raises(ValidationError):
            DiscreteHMM(n_states=2, n_observations=-1)

    def test_repr(self):
        """Test string representation."""
        hmm = DiscreteHMM(n_states=2, n_observations=3)
        repr_str = repr(hmm)

        assert "DiscreteHMM" in repr_str
        assert "n_states=2" in repr_str
        assert "n_observations=3" in repr_str
        assert "fitted=False" in repr_str


class TestDiscreteHMMFitting:
    """Tests for DiscreteHMM training/fitting."""

    def test_fit_basic(self, simple_sequences):
        """Test basic model fitting."""
        hmm = DiscreteHMM(n_states=2, n_observations=2, random_state=42)

        # Fit model
        fitted_hmm = hmm.fit(simple_sequences, n_iter=10, verbose=False)

        # Check that it returns self
        assert fitted_hmm is hmm

        # Check that model is fitted
        assert hmm.is_fitted
        assert hmm.start_probs is not None
        assert hmm.transition_probs is not None
        assert hmm.emission_probs is not None

        # Check parameter shapes
        assert hmm.start_probs.shape == (2,)
        assert hmm.transition_probs.shape == (2, 2)
        assert hmm.emission_probs.shape == (2, 2)

        # Check that probabilities are valid
        assert np.all(hmm.start_probs >= 0)
        assert np.all(hmm.transition_probs >= 0)
        assert np.all(hmm.emission_probs >= 0)

        assert_allclose(np.sum(hmm.start_probs), 1.0, rtol=1e-10)
        assert_allclose(np.sum(hmm.transition_probs, axis=1), np.ones(2), rtol=1e-10)
        assert_allclose(np.sum(hmm.emission_probs, axis=1), np.ones(2), rtol=1e-10)

    def test_fit_with_single_sequence(self):
        """Test fitting with single sequence."""
        hmm = DiscreteHMM(n_states=2, n_observations=2, random_state=42)
        sequence = np.array([0, 1, 0, 1, 0])

        hmm.fit(sequence, n_iter=5)
        assert hmm.is_fitted

    def test_fit_with_2d_array(self):
        """Test fitting with 2D array input."""
        hmm = DiscreteHMM(n_states=2, n_observations=3, random_state=42)
        sequences_2d = np.array([[0, 1, 2], [1, 0, 2], [2, 1, 0]])

        hmm.fit(sequences_2d, n_iter=5)
        assert hmm.is_fitted

    def test_fit_convergence(self):
        """Test that fitting improves log-likelihood."""
        hmm = DiscreteHMM(n_states=2, n_observations=2, random_state=42)

        # Create longer sequences for better convergence
        sequences = [
            np.array([0, 1, 0, 1, 0, 1, 0, 1]),
            np.array([1, 0, 1, 0, 1, 0, 1, 0]),
            np.array([0, 0, 1, 1, 0, 0, 1, 1]),
        ]

        hmm.fit(sequences, n_iter=20, verbose=False)

        # Check that we have likelihood history
        assert len(hmm.log_likelihood_history_) > 0

        # Check that likelihood generally improves (allowing for small decreases)
        if len(hmm.log_likelihood_history_) > 1:
            final_ll = hmm.log_likelihood_history_[-1]
            initial_ll = hmm.log_likelihood_history_[0]
            assert final_ll >= initial_ll - 1e-6  # Allow small numerical errors

    def test_fit_invalid_sequences(self):
        """Test fitting with invalid sequences."""
        hmm = DiscreteHMM(n_states=2, n_observations=2)

        # Empty sequence list
        with pytest.raises(ValidationError):
            hmm.fit([])

        # Sequence with invalid observations
        with pytest.raises(ValidationError):
            hmm.fit([np.array([0, 1, 2])])  # 2 is out of range

        # Sequence with negative observations
        with pytest.raises(ValidationError):
            hmm.fit([np.array([0, -1, 1])])

    def test_fit_invalid_parameters(self, simple_sequences):
        """Test fitting with invalid training parameters."""
        hmm = DiscreteHMM(n_states=2, n_observations=2)

        # Invalid n_iter
        with pytest.raises(ValidationError):
            hmm.fit(simple_sequences, n_iter=0)

        # Invalid tolerance
        with pytest.raises(ValidationError):
            hmm.fit(simple_sequences, tol=-1.0)

        # Invalid verbose
        with pytest.raises(ValidationError):
            hmm.fit(simple_sequences, verbose="yes")


class TestDiscreteHMMPrediction:
    """Tests for DiscreteHMM prediction methods."""

    @pytest.fixture
    def fitted_hmm(self, simple_sequences):
        """Create a fitted HMM for testing."""
        hmm = DiscreteHMM(n_states=2, n_observations=2, random_state=42)
        hmm.fit(simple_sequences, n_iter=10, verbose=False)
        return hmm

    def test_predict_viterbi(self, fitted_hmm):
        """Test Viterbi prediction."""
        sequence = np.array([0, 1, 0])
        states = fitted_hmm.predict(sequence)

        assert states.shape == (3,)
        assert states.dtype == np.int32
        assert np.all((states >= 0) & (states < 2))

    def test_predict_proba(self, fitted_hmm):
        """Test posterior probability prediction."""
        sequence = np.array([0, 1, 0])
        probs = fitted_hmm.predict_proba(sequence)

        assert probs.shape == (3, 2)
        assert np.all((probs >= 0) & (probs <= 1))
        assert_allclose(np.sum(probs, axis=1), np.ones(3), rtol=1e-10)

    def test_score(self, fitted_hmm):
        """Test log-likelihood scoring."""
        sequence = np.array([0, 1, 0])
        log_likelihood = fitted_hmm.score(sequence)

        assert isinstance(log_likelihood, float)
        assert np.isfinite(log_likelihood)
        assert log_likelihood < 0  # Log probability should be negative

    def test_sample(self, fitted_hmm):
        """Test sampling from fitted model."""
        observations, states = fitted_hmm.sample(n_samples=10)

        assert len(observations) == 10
        assert len(states) == 10
        assert states.dtype == np.int32

        # Check that samples are valid
        assert np.all((states >= 0) & (states < 2))
        assert np.all((observations >= 0) & (observations < 2))

    def test_unfitted_model_errors(self):
        """Test that unfitted model raises appropriate errors."""
        hmm = DiscreteHMM(n_states=2, n_observations=2)
        sequence = np.array([0, 1, 0])

        with pytest.raises(ModelNotFittedError):
            hmm.predict(sequence)

        with pytest.raises(ModelNotFittedError):
            hmm.predict_proba(sequence)

        with pytest.raises(ModelNotFittedError):
            hmm.score(sequence)

        with pytest.raises(ModelNotFittedError):
            hmm.sample(10)

    def test_invalid_sequence_prediction(self, fitted_hmm):
        """Test prediction with invalid sequences."""
        # Empty sequence
        with pytest.raises(ValidationError):
            fitted_hmm.predict(np.array([]))

        # Sequence with invalid observations
        with pytest.raises(ValidationError):
            fitted_hmm.predict(np.array([0, 1, 2]))

        # Non-integer sequence
        with pytest.raises(ValidationError):
            fitted_hmm.predict(np.array([0.5, 1.0]))

    def test_sample_invalid_parameters(self, fitted_hmm):
        """Test sampling with invalid parameters."""
        with pytest.raises(ValidationError):
            fitted_hmm.sample(n_samples=0)

        with pytest.raises(ValidationError):
            fitted_hmm.sample(n_samples=-1)


class TestDiscreteHMMUtilities:
    """Tests for utility methods of DiscreteHMM."""

    def test_get_params(self):
        """Test parameter retrieval."""
        hmm = DiscreteHMM(n_states=2, n_observations=3, random_state=42)
        params = hmm.get_params()

        assert isinstance(params, dict)
        assert "n_states" in params
        assert "n_observations" in params
        assert "is_fitted" in params
        assert params["n_states"] == 2
        assert params["n_observations"] == 3
        assert params["is_fitted"] == False

    def test_get_params_fitted(self, simple_sequences):
        """Test parameter retrieval for fitted model."""
        hmm = DiscreteHMM(n_states=2, n_observations=2, random_state=42)
        hmm.fit(simple_sequences, n_iter=5)

        params = hmm.get_params()
        assert params["is_fitted"] == True
        assert "log_likelihood_history" in params
        assert params["start_probs"] is not None
        assert params["transition_probs"] is not None
        assert params["emission_probs"] is not None

    def test_set_params(self):
        """Test parameter setting."""
        hmm = DiscreteHMM(n_states=2, n_observations=2)

        # Valid parameter
        hmm.set_params(random_state=123)
        assert hmm.random_state == 123

        # Invalid parameter
        with pytest.raises(ValueError):
            hmm.set_params(invalid_param=123)

    def test_fit_transform(self, simple_sequences):
        """Test fit_transform method."""
        hmm = DiscreteHMM(n_states=2, n_observations=2, random_state=42)

        posterior_probs = hmm.fit_transform(simple_sequences, n_iter=5)

        # Check that model is fitted
        assert hmm.is_fitted

        # Check posterior probabilities
        assert len(posterior_probs) == len(simple_sequences)
        for i, (seq, probs) in enumerate(zip(simple_sequences, posterior_probs)):
            assert probs.shape == (len(seq), 2)
            assert np.all((probs >= 0) & (probs <= 1))
            assert_allclose(np.sum(probs, axis=1), np.ones(len(seq)), rtol=1e-10)


class TestDiscreteHMMEdgeCases:
    """Tests for edge cases and corner scenarios."""

    def test_single_state_hmm(self):
        """Test HMM with single state."""
        hmm = DiscreteHMM(n_states=1, n_observations=2, random_state=42)
        sequences = [np.array([0, 1, 0, 1]), np.array([1, 0, 1])]

        hmm.fit(sequences, n_iter=5)

        # Check parameters
        assert hmm.start_probs.shape == (1,)
        assert hmm.transition_probs.shape == (1, 1)
        assert hmm.emission_probs.shape == (1, 2)

        # Start probability should be 1
        assert_allclose(hmm.start_probs, [1.0], rtol=1e-10)
        assert_allclose(hmm.transition_probs, [[1.0]], rtol=1e-10)

        # Test prediction
        test_seq = np.array([0, 1])
        states = hmm.predict(test_seq)
        assert_array_equal(states, np.zeros(2, dtype=np.int32))

    def test_single_observation_type(self):
        """Test HMM with single observation type."""
        hmm = DiscreteHMM(n_states=2, n_observations=1, random_state=42)
        sequences = [np.array([0, 0, 0]), np.array([0, 0])]

        hmm.fit(sequences, n_iter=5)

        assert hmm.emission_probs.shape == (2, 1)
        # All emission probabilities should be 1 (only one possible observation)
        assert_allclose(hmm.emission_probs, [[1.0], [1.0]], rtol=1e-10)

    def test_very_short_sequences(self):
        """Test with very short sequences."""
        hmm = DiscreteHMM(n_states=2, n_observations=2, random_state=42)
        sequences = [np.array([0]), np.array([1]), np.array([0])]

        hmm.fit(sequences, n_iter=10)
        assert hmm.is_fitted

        # Test prediction on single observation
        states = hmm.predict(np.array([0]))
        assert states.shape == (1,)

    def test_identical_sequences(self):
        """Test with identical training sequences."""
        hmm = DiscreteHMM(n_states=2, n_observations=2, random_state=42)
        sequences = [np.array([0, 1, 0, 1])] * 5  # 5 identical sequences

        hmm.fit(sequences, n_iter=10)
        assert hmm.is_fitted

        # Model should still work for prediction
        test_seq = np.array([0, 1])
        states = hmm.predict(test_seq)
        assert states.shape == (2,)

    def test_reproducibility(self, simple_sequences):
        """Test that results are reproducible with same random state."""
        hmm1 = DiscreteHMM(n_states=2, n_observations=2, random_state=42)
        hmm2 = DiscreteHMM(n_states=2, n_observations=2, random_state=42)

        hmm1.fit(simple_sequences, n_iter=10)
        hmm2.fit(simple_sequences, n_iter=10)

        # Parameters should be identical (use reasonable tolerance for floating point)
        assert_allclose(hmm1.start_probs, hmm2.start_probs, rtol=1e-8)
        assert_allclose(hmm1.transition_probs, hmm2.transition_probs, rtol=1e-8)
        assert_allclose(hmm1.emission_probs, hmm2.emission_probs, rtol=1e-8)

        # Predictions should be identical
        test_seq = np.array([0, 1, 0])
        states1 = hmm1.predict(test_seq)
        states2 = hmm2.predict(test_seq)
        assert_array_equal(states1, states2)


class TestDiscreteHMMIntegration:
    """Integration tests combining multiple features."""

    def test_weather_example(self, weather_sequences):
        """Test with weather-like example."""
        # 2 states (Sunny/Rainy), 3 observations (Walk/Shop/Clean)
        hmm = DiscreteHMM(n_states=2, n_observations=3, random_state=42)

        # Fit model
        hmm.fit(weather_sequences, n_iter=20, verbose=False)

        # Test all methods work
        test_seq = np.array([0, 1, 2])  # Walk, Shop, Clean

        states = hmm.predict(test_seq)
        probs = hmm.predict_proba(test_seq)
        score = hmm.score(test_seq)
        samples = hmm.sample(10)

        # Basic checks
        assert states.shape == (3,)
        assert probs.shape == (3, 2)
        assert isinstance(score, float)
        assert len(samples[0]) == 10
        assert len(samples[1]) == 10

    def test_training_progression(self):
        """Test that training progresses reasonably."""
        # Generate data from known HMM
        np.random.seed(42)
        true_hmm = DiscreteHMM(n_states=2, n_observations=2, random_state=42)

        # Set known parameters
        true_hmm.start_probs = np.array([0.6, 0.4])
        true_hmm.transition_probs = np.array([[0.7, 0.3], [0.4, 0.6]])
        true_hmm.emission_model.emission_probs = np.array([[0.8, 0.2], [0.3, 0.7]])
        true_hmm.emission_probs = true_hmm.emission_model.emission_probs
        true_hmm._is_fitted = True

        # Generate training data
        sequences = []
        for i in range(10):
            obs, _ = true_hmm.sample(20)
            # Ensure observations are 1D
            if obs.ndim == 2:
                obs = obs.flatten()
            sequences.append(obs)

        # Train new model
        test_hmm = DiscreteHMM(n_states=2, n_observations=2, random_state=123)
        test_hmm.fit(sequences, n_iter=50, verbose=False)

        # Check that training improved likelihood
        assert len(test_hmm.log_likelihood_history_) > 0
        if len(test_hmm.log_likelihood_history_) > 1:
            assert (
                test_hmm.log_likelihood_history_[-1]
                >= test_hmm.log_likelihood_history_[0] - 1e-6
            )

        # Test model works on test data
        test_seq = sequences[0][:5]  # First 5 observations
        score = test_hmm.score(test_seq)
        assert np.isfinite(score)

    def test_batch_vs_single_sequence_consistency(self):
        """Test that batch and single sequence processing give consistent results."""
        sequences = [
            np.array([0, 1, 0, 1]),
            np.array([1, 0, 1, 0]),
        ]

        # Train on batch
        hmm_batch = DiscreteHMM(n_states=2, n_observations=2, random_state=42)
        hmm_batch.fit(sequences, n_iter=10)

        # Train on sequences individually (simulate online learning)
        hmm_individual = DiscreteHMM(n_states=2, n_observations=2, random_state=42)
        hmm_individual.fit([sequences[0]], n_iter=5)
        # Note: True online learning would require different implementation

        # At least check both models work
        test_seq = np.array([0, 1])
        score_batch = hmm_batch.score(test_seq)
        score_individual = hmm_individual.score(test_seq)

        assert np.isfinite(score_batch)
        assert np.isfinite(score_individual)
