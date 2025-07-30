"""
Tests for evaluation metrics module.
"""

from unittest.mock import Mock

import numpy as np
import pytest

from markov.utils.metrics import (
    compare_models,
    compute_aic,
    compute_bic,
    compute_cross_entropy,
    compute_kl_divergence,
    compute_model_complexity,
    compute_perplexity,
    evaluate_model_fit,
    log_likelihood_ratio_test,
)


class TestBasicMetrics:
    """Test basic information criteria and metrics."""

    def test_compute_aic(self):
        """Test AIC computation."""
        # Standard case
        ll = -100.0
        n_params = 10
        aic = compute_aic(ll, n_params)
        expected_aic = 2 * 10 - 2 * (-100.0)  # 20 + 200 = 220
        assert aic == expected_aic

        # Edge case: zero log-likelihood
        aic_zero = compute_aic(0.0, 5)
        assert aic_zero == 10.0

        # Edge case: positive log-likelihood (should be rare but possible)
        aic_pos = compute_aic(50.0, 3)
        assert aic_pos == 6.0 - 100.0  # 6 - 100 = -94

    def test_compute_bic(self):
        """Test BIC computation."""
        # Standard case
        ll = -100.0
        n_params = 10
        n_samples = 1000
        bic = compute_bic(ll, n_params, n_samples)
        expected_bic = np.log(1000) * 10 - 2 * (-100.0)
        assert bic == expected_bic

        # Small sample size
        bic_small = compute_bic(-50.0, 5, 10)
        expected_small = np.log(10) * 5 - 2 * (-50.0)
        assert bic_small == expected_small

        # Single sample (edge case)
        bic_one = compute_bic(-10.0, 2, 1)
        expected_one = np.log(1) * 2 - 2 * (-10.0)  # 0 + 20 = 20
        assert bic_one == expected_one

    def test_compute_perplexity(self):
        """Test perplexity computation."""
        # Standard case
        ll = -100.0
        n_obs = 50
        perplexity = compute_perplexity(ll, n_obs)
        expected_perplexity = np.exp(-(-100.0) / 50)  # exp(2.0)
        assert perplexity == expected_perplexity

        # Perfect model (ll = 0)
        perplexity_perfect = compute_perplexity(0.0, 100)
        assert perplexity_perfect == 1.0

        # Zero observations (edge case)
        perplexity_zero = compute_perplexity(-50.0, 0)
        assert perplexity_zero == np.inf

        # Single observation
        perplexity_one = compute_perplexity(-2.0, 1)
        assert perplexity_one == np.exp(2.0)


class TestStatisticalTests:
    """Test statistical testing functions."""

    def test_log_likelihood_ratio_test_basic(self):
        """Test basic LLR test functionality."""
        # Case where alternative model is significantly better
        ll_null = -150.0
        ll_alt = -100.0
        df_diff = 5

        result = log_likelihood_ratio_test(ll_null, ll_alt, df_diff)

        # Check structure
        assert "lr_statistic" in result
        assert "p_value" in result
        assert "critical_value" in result
        assert "reject_null" in result
        assert "conclusion" in result

        # Check calculations
        expected_lr = 2 * (-100.0 - (-150.0))  # 2 * 50 = 100
        assert result["lr_statistic"] == expected_lr
        assert result["df_diff"] == df_diff
        assert isinstance(result["reject_null"], (bool, np.bool_))
        assert isinstance(result["p_value"], float)
        assert 0 <= result["p_value"] <= 1

    def test_log_likelihood_ratio_test_edge_cases(self):
        """Test LLR test edge cases."""
        # Case where models are identical
        result_identical = log_likelihood_ratio_test(-100.0, -100.0, 3)
        assert result_identical["lr_statistic"] == 0.0
        assert result_identical["p_value"] == 1.0
        assert not result_identical["reject_null"]

        # Case with very small difference
        result_small = log_likelihood_ratio_test(-100.0, -99.99, 1)
        assert np.isclose(result_small["lr_statistic"], 0.02)
        assert result_small["p_value"] > 0.5  # Should not be significant

        # Different alpha levels
        result_strict = log_likelihood_ratio_test(-150.0, -100.0, 5, alpha=0.01)
        result_lenient = log_likelihood_ratio_test(-150.0, -100.0, 5, alpha=0.10)
        assert result_strict["alpha"] == 0.01
        assert result_lenient["alpha"] == 0.10
        assert result_strict["critical_value"] > result_lenient["critical_value"]


class TestDistributionMetrics:
    """Test distribution comparison metrics."""

    def test_compute_cross_entropy(self):
        """Test cross-entropy computation."""
        # Identical distributions
        p = np.array([0.5, 0.3, 0.2])
        q = np.array([0.5, 0.3, 0.2])
        ce_identical = compute_cross_entropy(p, q)
        # Should equal entropy of p
        entropy_p = -np.sum(p * np.log(p))
        assert np.isclose(ce_identical, entropy_p)

        # Different distributions
        p1 = np.array([0.7, 0.2, 0.1])
        q1 = np.array([0.4, 0.4, 0.2])
        ce_diff = compute_cross_entropy(p1, q1)
        # Cross-entropy should be >= entropy of the true distribution (p1)
        entropy_p1 = -np.sum(p1 * np.log(p1))
        assert ce_diff >= entropy_p1  # Cross-entropy >= entropy

        # Extreme case: one distribution has near-zero probability
        p2 = np.array([1.0, 0.0, 0.0])
        q2 = np.array([0.1, 0.8, 0.1])
        ce_extreme = compute_cross_entropy(p2, q2)
        assert ce_extreme > 0  # Should handle gracefully

    def test_compute_kl_divergence(self):
        """Test KL divergence computation."""
        # Identical distributions
        p = np.array([0.5, 0.3, 0.2])
        q = np.array([0.5, 0.3, 0.2])
        kl_identical = compute_kl_divergence(p, q)
        assert np.isclose(kl_identical, 0.0, atol=1e-10)

        # Different distributions
        p1 = np.array([0.7, 0.2, 0.1])
        q1 = np.array([0.4, 0.4, 0.2])
        kl_diff = compute_kl_divergence(p1, q1)
        assert kl_diff > 0  # KL divergence is non-negative

        # Asymmetry test
        kl_reverse = compute_kl_divergence(q1, p1)
        assert not np.isclose(kl_diff, kl_reverse)  # KL is asymmetric

        # Extreme distributions
        p2 = np.array([0.99, 0.005, 0.005])
        q2 = np.array([0.33, 0.33, 0.34])
        kl_extreme = compute_kl_divergence(p2, q2)
        assert kl_extreme > 0
        assert np.isfinite(kl_extreme)

    def test_distribution_metrics_edge_cases(self):
        """Test edge cases for distribution metrics."""
        # Empty arrays - should handle gracefully or raise appropriate errors
        try:
            result = compute_cross_entropy(np.array([]), np.array([]))
            # If it doesn't raise an error, result should be reasonable
            assert np.isfinite(result) or result == 0
        except (ValueError, IndexError):
            # This is also acceptable behavior
            pass

        # Mismatched dimensions
        with pytest.raises((ValueError, IndexError, AssertionError)):
            compute_kl_divergence(np.array([0.5, 0.5]), np.array([0.33, 0.33, 0.34]))

        # Arrays with zeros (should be handled by epsilon clipping)
        p_zero = np.array([1.0, 0.0, 0.0])
        q_zero = np.array([0.0, 1.0, 0.0])
        ce_zero = compute_cross_entropy(p_zero, q_zero)
        kl_zero = compute_kl_divergence(p_zero, q_zero)
        assert np.isfinite(ce_zero)
        assert np.isfinite(kl_zero)


class TestModelComplexity:
    """Test model complexity calculations."""

    def test_compute_model_complexity_basic(self):
        """Test basic model complexity computation."""
        # Simple 2-state, 3-observation model
        n_states = 2
        n_obs = 3
        complexity = compute_model_complexity(n_states, n_obs)

        # Expected: (2-1) + 2*(2-1) + 2*(3-1) = 1 + 2 + 4 = 7
        expected = (n_states - 1) + n_states * (n_states - 1) + n_states * (n_obs - 1)
        assert complexity == expected
        assert complexity == 7

    def test_compute_model_complexity_various_sizes(self):
        """Test complexity for various model sizes."""
        test_cases = [
            (1, 1, 0),  # Minimal case: (1-1) + 1*(1-1) + 1*(1-1) = 0
            (2, 2, 5),  # (2-1) + 2*(2-1) + 2*(2-1) = 1 + 2 + 2 = 5
            (3, 4, 17),  # (3-1) + 3*(3-1) + 3*(4-1) = 2 + 6 + 9 = 17
            (5, 10, 69),  # (5-1) + 5*(5-1) + 5*(10-1) = 4 + 20 + 45 = 69
        ]

        for n_states, n_obs, expected in test_cases:
            complexity = compute_model_complexity(n_states, n_obs)
            # Recalculate expected to be sure
            calculated_expected = (
                (n_states - 1) + n_states * (n_states - 1) + n_states * (n_obs - 1)
            )
            assert (
                complexity == calculated_expected
            ), f"Failed for {n_states} states, {n_obs} obs: got {complexity}, expected {calculated_expected}"
            assert (
                complexity == expected
            ), f"Failed for {n_states} states, {n_obs} obs: got {complexity}, expected {expected}"


class TestModelEvaluation:
    """Test comprehensive model evaluation functions."""

    def create_mock_hmm(self, n_states=3, n_obs=4, scores=None):
        """Create a mock HMM for testing."""
        mock_hmm = Mock()
        mock_hmm.n_states = n_states
        mock_hmm.n_observations = n_obs

        if scores is None:
            scores = [-10.0, -15.0, -12.0]  # Default scores for 3 sequences

        mock_hmm.score = Mock(side_effect=scores)
        return mock_hmm

    def test_evaluate_model_fit_basic(self):
        """Test basic model evaluation."""
        # Create mock model
        hmm = self.create_mock_hmm(n_states=3, n_obs=4)

        # Mock sequences
        train_sequences = [np.array([0, 1, 2]), np.array([1, 2, 0, 1])]
        test_sequences = [np.array([2, 0, 1])]

        # Set up score method to return different values for different calls
        scores = [-10.0, -15.0, -12.0]  # Train seq 1, train seq 2, test seq 1
        hmm.score.side_effect = scores

        result = evaluate_model_fit(hmm, train_sequences, test_sequences)

        # Check structure
        assert "training" in result
        assert "test" in result
        assert "model" in result

        # Check training metrics
        train_metrics = result["training"]
        assert "log_likelihood" in train_metrics
        assert "n_observations" in train_metrics
        assert "aic" in train_metrics
        assert "bic" in train_metrics
        assert "perplexity" in train_metrics

        # Check test metrics
        test_metrics = result["test"]
        assert all(
            key in test_metrics
            for key in ["log_likelihood", "aic", "bic", "perplexity"]
        )

        # Check model info
        model_info = result["model"]
        assert model_info["n_states"] == 3
        assert model_info["n_observations"] == 4
        assert "n_parameters" in model_info

    def test_compare_models_basic(self):
        """Test basic model comparison."""
        # Create multiple mock models
        models = [
            self.create_mock_hmm(n_states=2, n_obs=3, scores=[-20.0]),
            self.create_mock_hmm(n_states=3, n_obs=3, scores=[-15.0]),
            self.create_mock_hmm(n_states=4, n_obs=3, scores=[-12.0]),
        ]

        test_sequences = [np.array([0, 1, 2])]

        result = compare_models(models, test_sequences)

        # Check structure
        assert "results" in result
        assert "best_aic_model" in result
        assert "best_bic_model" in result
        assert "best_likelihood_model" in result

        # Check results for each model
        assert len(result["results"]) == 3
        for i, model_result in enumerate(result["results"]):
            assert model_result["model_index"] == i
            assert "n_states" in model_result
            assert "log_likelihood" in model_result
            assert "aic" in model_result
            assert "bic" in model_result
            assert "perplexity" in model_result

        # Best likelihood model should be the one with highest LL
        best_ll_idx = result["best_likelihood_model"]
        best_ll = result["results"][best_ll_idx]["log_likelihood"]
        for model_result in result["results"]:
            assert model_result["log_likelihood"] <= best_ll

    def test_compare_models_edge_cases(self):
        """Test model comparison edge cases."""
        # Single model
        models = [self.create_mock_hmm(n_states=2, n_obs=3, scores=[-10.0])]
        test_sequences = [np.array([0, 1, 2])]

        result = compare_models(models, test_sequences)
        assert len(result["results"]) == 1
        assert result["best_aic_model"] == 0
        assert result["best_bic_model"] == 0
        assert result["best_likelihood_model"] == 0

        # Models with identical performance
        identical_models = [
            self.create_mock_hmm(n_states=2, n_obs=3, scores=[-15.0]),
            self.create_mock_hmm(n_states=2, n_obs=3, scores=[-15.0]),
        ]

        result_identical = compare_models(identical_models, test_sequences)
        # Should still work, first model wins ties
        assert len(result_identical["results"]) == 2
        for key in ["best_aic_model", "best_bic_model", "best_likelihood_model"]:
            assert result_identical[key] in [0, 1]


class TestMetricsIntegration:
    """Integration tests combining multiple metrics."""

    def test_metrics_consistency(self):
        """Test that metrics are consistent with each other."""
        # AIC and BIC should have specific relationships
        ll = -100.0
        n_params = 10
        n_samples = 1000

        aic = compute_aic(ll, n_params)
        bic = compute_bic(ll, n_params, n_samples)

        # For large sample sizes, BIC should penalize complexity more than AIC
        assert bic > aic  # BIC has stronger penalty for large n

        # Perplexity should be consistent
        n_obs = 50
        perplexity = compute_perplexity(ll, n_obs)

        # Perplexity should be > 1 for negative log-likelihood
        assert perplexity > 1.0

        # Better model (higher LL) should have lower perplexity
        better_ll = -80.0
        better_perplexity = compute_perplexity(better_ll, n_obs)
        assert better_perplexity < perplexity

    def test_probability_metrics_properties(self):
        """Test mathematical properties of probability metrics."""
        # Create test distributions
        uniform = np.array([0.25, 0.25, 0.25, 0.25])
        peaked = np.array([0.7, 0.1, 0.1, 0.1])

        # Cross-entropy and KL divergence properties
        ce_uniform_uniform = compute_cross_entropy(uniform, uniform)
        ce_peaked_uniform = compute_cross_entropy(peaked, uniform)

        kl_uniform_uniform = compute_kl_divergence(uniform, uniform)
        kl_peaked_uniform = compute_kl_divergence(peaked, uniform)

        # KL divergence should be 0 for identical distributions
        assert np.isclose(kl_uniform_uniform, 0.0, atol=1e-10)

        # KL divergence should be positive for different distributions
        assert kl_peaked_uniform > 0

        # Cross-entropy should be >= entropy
        entropy_peaked = -np.sum(peaked * np.log(peaked))
        assert ce_peaked_uniform >= entropy_peaked

    @pytest.mark.parametrize("n_states,n_obs", [(2, 3), (3, 4), (5, 10), (1, 1)])
    def test_complexity_scaling(self, n_states, n_obs):
        """Test that model complexity scales appropriately."""
        complexity = compute_model_complexity(n_states, n_obs)

        # Complexity should be non-negative
        assert complexity >= 0

        # Complexity should increase with number of states
        if n_states > 1:
            smaller_complexity = compute_model_complexity(n_states - 1, n_obs)
            assert complexity > smaller_complexity

        # Complexity should increase with number of observations
        if n_obs > 1:
            smaller_complexity = compute_model_complexity(n_states, n_obs - 1)
            assert complexity > smaller_complexity
