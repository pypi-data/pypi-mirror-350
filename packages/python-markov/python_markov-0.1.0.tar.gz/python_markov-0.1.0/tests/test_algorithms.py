"""
Tests for core HMM algorithms.

This module contains comprehensive tests for all algorithms in algorithms.py,
including forward, backward, Viterbi, forward-backward, Baum-Welch, and sampling.
"""

import numpy as np
import pytest
from numpy.testing import assert_allclose, assert_array_equal

from markov.core.algorithms import (
    backward_algorithm,
    baum_welch_step,
    fit_hmm_baum_welch,
    forward_algorithm,
    forward_backward_algorithm,
    sample_hmm,
    viterbi_algorithm,
)
from markov.utils.math_utils import LOG_ZERO, safe_log


class MockEmissionModel:
    """Mock emission model for testing."""

    def __init__(self, emission_probs):
        """Initialize with given emission probabilities."""
        self.emission_probs = emission_probs
        self.n_states, self.n_observations = emission_probs.shape

    def log_probability_matrix(self, sequence):
        """Get log emission probabilities for sequence."""
        T = len(sequence)
        log_emission_probs = np.zeros((T, self.n_states))
        for t, obs in enumerate(sequence):
            # Handle both scalar and array observations
            if np.isscalar(obs):
                log_emission_probs[t] = safe_log(self.emission_probs[:, obs])
            else:
                log_emission_probs[t] = safe_log(self.emission_probs[:, obs[0]])
        return log_emission_probs

    def update_parameters(self, sequences, gammas):
        """Update emission parameters (mock implementation)."""
        # Initialize emission counts
        emission_counts = np.zeros((self.n_states, self.n_observations))

        # Accumulate counts across all sequences
        for seq, gamma in zip(sequences, gammas):
            T = len(seq)
            for t in range(T):
                obs = seq[t]
                emission_counts[:, obs] += gamma[t]

        # Normalize to get probabilities
        row_sums = np.sum(emission_counts, axis=1, keepdims=True)
        row_sums = np.maximum(row_sums, 1e-12)
        self.emission_probs = emission_counts / row_sums

    def sample(self, state, n_samples=1):
        """Sample observations from given state."""
        samples = np.random.choice(
            self.n_observations, size=n_samples, p=self.emission_probs[state]
        )
        if n_samples == 1:
            return samples[0]  # Return scalar for single sample
        return samples


@pytest.fixture
def simple_hmm_params():
    """Simple 2-state, 2-observation HMM for testing."""
    start_probs = np.array([0.6, 0.4])
    transition_probs = np.array([[0.7, 0.3], [0.4, 0.6]])
    emission_probs = np.array(
        [
            [0.9, 0.1],  # State 0: mostly emits symbol 0
            [0.2, 0.8],  # State 1: mostly emits symbol 1
        ]
    )
    return start_probs, transition_probs, emission_probs


@pytest.fixture
def test_sequence():
    """Test observation sequence."""
    return np.array([0, 1, 0, 1])


@pytest.fixture
def weather_hmm_params():
    """Classic weather HMM example."""
    # States: 0=Sunny, 1=Rainy
    start_probs = np.array([0.8, 0.2])
    transition_probs = np.array(
        [[0.7, 0.3], [0.4, 0.6]]  # Sunny -> [Sunny, Rainy]  # Rainy -> [Sunny, Rainy]
    )
    # Observations: 0=Walk, 1=Shop, 2=Clean
    emission_probs = np.array(
        [
            [0.6, 0.3, 0.1],  # Sunny -> [Walk, Shop, Clean]
            [0.1, 0.4, 0.5],  # Rainy -> [Walk, Shop, Clean]
        ]
    )
    return start_probs, transition_probs, emission_probs


class TestForwardAlgorithm:
    """Tests for forward algorithm."""

    def test_forward_basic(self, simple_hmm_params, test_sequence):
        """Test basic forward algorithm functionality."""
        start_probs, transition_probs, emission_probs = simple_hmm_params

        # Convert to log space
        log_start_probs = safe_log(start_probs)
        log_transition_probs = safe_log(transition_probs)

        # Get log emission probabilities
        T = len(test_sequence)
        log_emission_probs = np.zeros((T, 2))
        for t, obs in enumerate(test_sequence):
            log_emission_probs[t] = safe_log(emission_probs[:, obs])

        # Run forward algorithm
        log_forward, log_likelihood = forward_algorithm(
            log_start_probs, log_transition_probs, log_emission_probs
        )

        # Check shapes
        assert log_forward.shape == (T, 2)
        assert isinstance(log_likelihood, float)

        # Check that probabilities are finite
        assert np.all(np.isfinite(log_forward))
        assert np.isfinite(log_likelihood)

        # Check that log-likelihood is reasonable (negative)
        assert log_likelihood < 0

    def test_forward_known_values(self):
        """Test forward algorithm with known values."""
        # Simple example where we can compute by hand
        start_probs = np.array([1.0, 0.0])  # Always start in state 0
        transition_probs = np.array([[0.5, 0.5], [0.5, 0.5]])
        emission_probs = np.array(
            [[1.0, 0.0], [0.0, 1.0]]  # State 0 always emits 0  # State 1 always emits 1
        )
        sequence = np.array([0])  # Single observation

        log_start_probs = safe_log(start_probs)
        log_transition_probs = safe_log(transition_probs)
        log_emission_probs = np.array([safe_log(emission_probs[:, 0])]).reshape(1, -1)

        log_forward, log_likelihood = forward_algorithm(
            log_start_probs, log_transition_probs, log_emission_probs
        )

        # At t=0, only state 0 can emit observation 0
        expected_forward = np.array([[0.0, LOG_ZERO]])  # log([1.0, 0.0])
        assert_allclose(log_forward, expected_forward, rtol=1e-10)

        # Log-likelihood should be log(1.0) = 0.0
        assert_allclose(log_likelihood, 0.0, rtol=1e-10)

    def test_forward_empty_sequence(self, simple_hmm_params):
        """Test forward algorithm with empty sequence."""
        start_probs, transition_probs, _ = simple_hmm_params
        log_start_probs = safe_log(start_probs)
        log_transition_probs = safe_log(transition_probs)
        log_emission_probs = np.zeros((0, 2))  # Empty sequence

        with pytest.raises(IndexError):
            forward_algorithm(log_start_probs, log_transition_probs, log_emission_probs)


class TestBackwardAlgorithm:
    """Tests for backward algorithm."""

    def test_backward_basic(self, simple_hmm_params, test_sequence):
        """Test basic backward algorithm functionality."""
        _, transition_probs, emission_probs = simple_hmm_params

        log_transition_probs = safe_log(transition_probs)

        # Get log emission probabilities
        T = len(test_sequence)
        log_emission_probs = np.zeros((T, 2))
        for t, obs in enumerate(test_sequence):
            log_emission_probs[t] = safe_log(emission_probs[:, obs])

        # Run backward algorithm
        log_backward = backward_algorithm(log_transition_probs, log_emission_probs)

        # Check shape
        assert log_backward.shape == (T, 2)

        # Check that probabilities are finite
        assert np.all(np.isfinite(log_backward))

        # Check that final backward probabilities are 0 (log(1))
        assert_allclose(log_backward[-1], [0.0, 0.0], rtol=1e-10)

    def test_backward_single_observation(self):
        """Test backward algorithm with single observation."""
        transition_probs = np.array([[0.5, 0.5], [0.5, 0.5]])
        emission_probs = np.array([[0.8, 0.2], [0.3, 0.7]])

        log_transition_probs = safe_log(transition_probs)
        log_emission_probs = np.array([safe_log(emission_probs[:, 0])]).reshape(1, -1)

        log_backward = backward_algorithm(log_transition_probs, log_emission_probs)

        # For single observation, backward should be [0, 0] (log(1))
        expected_backward = np.array([[0.0, 0.0]])
        assert_allclose(log_backward, expected_backward, rtol=1e-10)


class TestViterbiAlgorithm:
    """Tests for Viterbi algorithm."""

    def test_viterbi_basic(self, simple_hmm_params, test_sequence):
        """Test basic Viterbi algorithm functionality."""
        start_probs, transition_probs, emission_probs = simple_hmm_params

        log_start_probs = safe_log(start_probs)
        log_transition_probs = safe_log(transition_probs)

        # Get log emission probabilities
        T = len(test_sequence)
        log_emission_probs = np.zeros((T, 2))
        for t, obs in enumerate(test_sequence):
            log_emission_probs[t] = safe_log(emission_probs[:, obs])

        # Run Viterbi algorithm
        states, log_prob = viterbi_algorithm(
            log_start_probs, log_transition_probs, log_emission_probs
        )

        # Check shapes and types
        assert states.shape == (T,)
        assert states.dtype == np.int32
        assert isinstance(log_prob, float)

        # Check that states are valid
        assert np.all((states >= 0) & (states < 2))

        # Check that log probability is finite and negative
        assert np.isfinite(log_prob)
        assert log_prob < 0

    def test_viterbi_known_sequence(self):
        """Test Viterbi with a sequence that has known optimal path."""
        # Create HMM where state 0 always emits 0, state 1 always emits 1
        start_probs = np.array([0.5, 0.5])
        transition_probs = np.array(
            [
                [0.9, 0.1],  # State 0 prefers to stay
                [0.1, 0.9],  # State 1 prefers to stay
            ]
        )
        emission_probs = np.array(
            [[1.0, 0.0], [0.0, 1.0]]  # State 0 always emits 0  # State 1 always emits 1
        )

        sequence = np.array([0, 0, 1, 1])

        log_start_probs = safe_log(start_probs)
        log_transition_probs = safe_log(transition_probs)

        T = len(sequence)
        log_emission_probs = np.zeros((T, 2))
        for t, obs in enumerate(sequence):
            log_emission_probs[t] = safe_log(emission_probs[:, obs])

        states, log_prob = viterbi_algorithm(
            log_start_probs, log_transition_probs, log_emission_probs
        )

        # Optimal path should be [0, 0, 1, 1]
        expected_states = np.array([0, 0, 1, 1])
        assert_array_equal(states, expected_states)

    def test_viterbi_single_observation(self, simple_hmm_params):
        """Test Viterbi with single observation."""
        start_probs, transition_probs, emission_probs = simple_hmm_params

        log_start_probs = safe_log(start_probs)
        log_transition_probs = safe_log(transition_probs)
        log_emission_probs = np.array([safe_log(emission_probs[:, 0])]).reshape(1, -1)

        states, log_prob = viterbi_algorithm(
            log_start_probs, log_transition_probs, log_emission_probs
        )

        assert states.shape == (1,)
        assert states[0] in [0, 1]
        assert np.isfinite(log_prob)


class TestForwardBackwardAlgorithm:
    """Tests for forward-backward algorithm."""

    def test_forward_backward_basic(self, simple_hmm_params, test_sequence):
        """Test basic forward-backward functionality."""
        start_probs, transition_probs, emission_probs = simple_hmm_params

        log_start_probs = safe_log(start_probs)
        log_transition_probs = safe_log(transition_probs)

        T = len(test_sequence)
        log_emission_probs = np.zeros((T, 2))
        for t, obs in enumerate(test_sequence):
            log_emission_probs[t] = safe_log(emission_probs[:, obs])

        gamma, xi, log_likelihood = forward_backward_algorithm(
            log_start_probs, log_transition_probs, log_emission_probs
        )

        # Check shapes
        assert gamma.shape == (T, 2)
        assert xi.shape == (T - 1, 2, 2)
        assert isinstance(log_likelihood, float)

        # Check that probabilities are valid
        assert np.all((gamma >= 0) & (gamma <= 1))
        assert np.all((xi >= 0) & (xi <= 1))

        # Check that gamma rows sum to 1
        assert_allclose(np.sum(gamma, axis=1), np.ones(T), rtol=1e-10)

        # Check that xi sums correctly
        for t in range(T - 1):
            assert_allclose(np.sum(xi[t]), 1.0, rtol=1e-10)

    def test_forward_backward_consistency(self, simple_hmm_params, test_sequence):
        """Test consistency between forward-backward and separate algorithms."""
        start_probs, transition_probs, emission_probs = simple_hmm_params

        log_start_probs = safe_log(start_probs)
        log_transition_probs = safe_log(transition_probs)

        T = len(test_sequence)
        log_emission_probs = np.zeros((T, 2))
        for t, obs in enumerate(test_sequence):
            log_emission_probs[t] = safe_log(emission_probs[:, obs])

        # Run forward-backward
        gamma, xi, log_likelihood_fb = forward_backward_algorithm(
            log_start_probs, log_transition_probs, log_emission_probs
        )

        # Run forward algorithm separately
        _, log_likelihood_f = forward_algorithm(
            log_start_probs, log_transition_probs, log_emission_probs
        )

        # Log-likelihoods should match
        assert_allclose(log_likelihood_fb, log_likelihood_f, rtol=1e-10)


class TestBaumWelchAlgorithm:
    """Tests for Baum-Welch algorithm."""

    def test_baum_welch_step(self, simple_hmm_params):
        """Test single Baum-Welch step."""
        start_probs, transition_probs, emission_probs = simple_hmm_params

        # Create mock emission model
        emission_model = MockEmissionModel(emission_probs)

        # Test sequences
        sequences = [np.array([0, 1, 0]), np.array([1, 0, 1])]

        log_start_probs = safe_log(start_probs)
        log_transition_probs = safe_log(transition_probs)

        new_log_start, new_log_trans, total_ll = baum_welch_step(
            sequences, log_start_probs, log_transition_probs, emission_model
        )

        # Check shapes
        assert new_log_start.shape == (2,)
        assert new_log_trans.shape == (2, 2)
        assert isinstance(total_ll, float)

        # Check that probabilities are valid (after exp)
        new_start = np.exp(new_log_start)
        new_trans = np.exp(new_log_trans)

        assert np.all((new_start >= 0) & (new_start <= 1))
        assert np.all((new_trans >= 0) & (new_trans <= 1))
        assert_allclose(np.sum(new_start), 1.0, rtol=1e-10)
        assert_allclose(np.sum(new_trans, axis=1), np.ones(2), rtol=1e-10)

    def test_fit_hmm_baum_welch(self, simple_hmm_params):
        """Test complete Baum-Welch training."""
        start_probs, transition_probs, emission_probs = simple_hmm_params

        # Create mock emission model
        emission_model = MockEmissionModel(emission_probs.copy())

        # Test sequences
        sequences = [
            np.array([0, 1, 0, 1]),
            np.array([1, 0, 1, 0]),
            np.array([0, 0, 1, 1]),
        ]

        final_start, final_trans, ll_history = fit_hmm_baum_welch(
            sequences=sequences,
            initial_start_probs=start_probs,
            initial_transition_probs=transition_probs,
            emission_model=emission_model,
            n_iter=10,
            tol=1e-4,
            verbose=False,
        )

        # Check shapes
        assert final_start.shape == (2,)
        assert final_trans.shape == (2, 2)
        assert len(ll_history) > 0

        # Check that probabilities are valid
        assert np.all((final_start >= 0) & (final_start <= 1))
        assert np.all((final_trans >= 0) & (final_trans <= 1))
        assert_allclose(np.sum(final_start), 1.0, rtol=1e-10)
        assert_allclose(np.sum(final_trans, axis=1), np.ones(2), rtol=1e-10)

        # Check that log-likelihood is non-decreasing
        ll_array = np.array(ll_history)
        assert np.all(np.diff(ll_array) >= -1e-10)  # Allow small numerical errors

    def test_baum_welch_convergence(self):
        """Test that Baum-Welch converges on simple example."""
        # Simple HMM that should converge quickly
        start_probs = np.array([0.5, 0.5])
        transition_probs = np.array([[0.7, 0.3], [0.4, 0.6]])
        emission_probs = np.array([[0.9, 0.1], [0.1, 0.9]])

        emission_model = MockEmissionModel(emission_probs.copy())

        # Generate sequences from true model for testing
        np.random.seed(42)
        sequences = []
        for i in range(5):
            seq = []
            state = np.random.choice(2, p=start_probs)
            for _ in range(20):
                obs = np.random.choice(2, p=emission_probs[state])
                seq.append(obs)
                state = np.random.choice(2, p=transition_probs[state])
            sequences.append(np.array(seq))

        # Train with reasonable tolerance
        final_start, final_trans, ll_history = fit_hmm_baum_welch(
            sequences=sequences,
            initial_start_probs=np.array([0.6, 0.4]),  # Different from true
            initial_transition_probs=np.array([[0.8, 0.2], [0.3, 0.7]]),
            emission_model=emission_model,
            n_iter=100,
            tol=1e-6,  # More reasonable tolerance
            verbose=False,
        )

        # Check that training completed and likelihood improved
        assert len(ll_history) > 0
        if len(ll_history) > 1:
            # Check that likelihood improved
            assert ll_history[-1] >= ll_history[0]


class TestSampling:
    """Tests for HMM sampling."""

    def test_sample_hmm_basic(self, simple_hmm_params):
        """Test basic HMM sampling functionality."""
        start_probs, transition_probs, emission_probs = simple_hmm_params
        emission_model = MockEmissionModel(emission_probs)

        np.random.seed(42)
        observations, states = sample_hmm(
            start_probs, transition_probs, emission_model, n_samples=10, random_state=42
        )

        # Check shapes and types
        assert len(observations) == 10
        assert len(states) == 10
        assert states.dtype == np.int32

        # Check that states are valid
        assert np.all((states >= 0) & (states < 2))

        # Check that observations are valid
        assert np.all((observations >= 0) & (observations < 2))

    def test_sample_hmm_deterministic(self):
        """Test sampling with deterministic emissions."""
        start_probs = np.array([1.0, 0.0])  # Always start in state 0
        transition_probs = np.array([[1.0, 0.0], [0.0, 1.0]])  # Always stay in state 0
        emission_probs = np.array([[1.0, 0.0], [0.0, 1.0]])  # State 0 always emits 0

        emission_model = MockEmissionModel(emission_probs)

        observations, states = sample_hmm(
            start_probs, transition_probs, emission_model, n_samples=5, random_state=42
        )

        # All states should be 0, all observations should be 0
        assert_array_equal(states, np.zeros(5, dtype=np.int32))
        assert_array_equal(observations, np.zeros(5, dtype=int))

    def test_sample_hmm_random_seed(self, simple_hmm_params):
        """Test that random seed produces reproducible results."""
        start_probs, transition_probs, emission_probs = simple_hmm_params
        emission_model = MockEmissionModel(emission_probs)

        # Sample twice with same seed
        obs1, states1 = sample_hmm(
            start_probs,
            transition_probs,
            emission_model,
            n_samples=20,
            random_state=123,
        )

        obs2, states2 = sample_hmm(
            start_probs,
            transition_probs,
            emission_model,
            n_samples=20,
            random_state=123,
        )

        # Results should be identical
        assert_array_equal(obs1, obs2)
        assert_array_equal(states1, states2)


class TestIntegration:
    """Integration tests combining multiple algorithms."""

    def test_weather_example(self, weather_hmm_params):
        """Test with classic weather example."""
        start_probs, transition_probs, emission_probs = weather_hmm_params
        emission_model = MockEmissionModel(emission_probs)

        # Observation sequence: Walk, Shop, Clean
        sequence = np.array([0, 1, 2])

        log_start_probs = safe_log(start_probs)
        log_transition_probs = safe_log(transition_probs)
        log_emission_probs = emission_model.log_probability_matrix(sequence)

        # Test all algorithms work together
        log_forward, ll_forward = forward_algorithm(
            log_start_probs, log_transition_probs, log_emission_probs
        )

        log_backward = backward_algorithm(log_transition_probs, log_emission_probs)

        states, ll_viterbi = viterbi_algorithm(
            log_start_probs, log_transition_probs, log_emission_probs
        )

        gamma, xi, ll_fb = forward_backward_algorithm(
            log_start_probs, log_transition_probs, log_emission_probs
        )

        # Check consistency
        assert_allclose(ll_forward, ll_fb, rtol=1e-10)
        assert ll_viterbi <= ll_forward  # Viterbi gives max path, not total prob

        # Check shapes
        assert log_forward.shape == (3, 2)
        assert log_backward.shape == (3, 2)
        assert states.shape == (3,)
        assert gamma.shape == (3, 2)
        assert xi.shape == (2, 2, 2)

    def test_algorithm_consistency(self, simple_hmm_params):
        """Test consistency between different algorithm implementations."""
        start_probs, transition_probs, emission_probs = simple_hmm_params
        emission_model = MockEmissionModel(emission_probs)

        # Generate test sequences
        np.random.seed(42)
        sequences = []
        for _ in range(3):
            obs, _ = sample_hmm(
                start_probs,
                transition_probs,
                emission_model,
                n_samples=15,
                random_state=42 + _,
            )
            sequences.append(obs)

        # Train model using Baum-Welch
        final_start, final_trans, _ = fit_hmm_baum_welch(
            sequences=sequences,
            initial_start_probs=start_probs,
            initial_transition_probs=transition_probs,
            emission_model=emission_model,
            n_iter=10,
            tol=1e-6,
            verbose=False,
        )

        # Test trained model on first sequence
        test_seq = sequences[0]
        log_start = safe_log(final_start)
        log_trans = safe_log(final_trans)
        log_emission = emission_model.log_probability_matrix(test_seq)

        # All algorithms should work without errors
        _, ll1 = forward_algorithm(log_start, log_trans, log_emission)
        _ = backward_algorithm(log_trans, log_emission)
        _, ll2 = viterbi_algorithm(log_start, log_trans, log_emission)
        _, _, ll3 = forward_backward_algorithm(log_start, log_trans, log_emission)

        # Forward and forward-backward should give same likelihood
        assert_allclose(ll1, ll3, rtol=1e-10)

        # Viterbi likelihood should be <= forward likelihood
        assert ll2 <= ll1 + 1e-10
