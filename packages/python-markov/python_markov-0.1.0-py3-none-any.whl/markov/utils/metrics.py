"""
Evaluation metrics
"""

from typing import List

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from .math_utils import safe_log


def compute_aic(log_likelihood: float, n_parameters: int) -> float:
    """
    Compute Akaike Information Criterion (AIC).

    AIC = 2k - 2ln(L)
    where k is the number of parameters and L is the likelihood.

    Args:
        log_likelihood: Log-likelihood of the model
        n_parameters: Number of model parameters

    Returns:
        AIC value (lower is better)
    """
    return 2 * n_parameters - 2 * log_likelihood


def compute_bic(log_likelihood: float, n_parameters: int, n_samples: int) -> float:
    """
    Compute Bayesian Information Criterion (BIC).

    BIC = ln(n)k - 2ln(L)
    where n is the number of samples, k is parameters, L is likelihood.

    Args:
        log_likelihood: Log-likelihood of the model
        n_parameters: Number of model parameters
        n_samples: Number of training samples

    Returns:
        BIC value (lower is better)
    """
    return np.log(n_samples) * n_parameters - 2 * log_likelihood


def compute_perplexity(log_likelihood: float, n_observations: int) -> float:
    """
    Compute perplexity of the model.

    Perplexity = exp(-log_likelihood / n_observations)

    Args:
        log_likelihood: Log-likelihood of test data
        n_observations: Total number of observations

    Returns:
        Perplexity (lower is better)
    """
    if n_observations == 0:
        return np.inf

    return np.exp(-log_likelihood / n_observations)


def log_likelihood_ratio_test(
    ll_null: float, ll_alt: float, df_diff: int, alpha: float = 0.05
) -> dict:
    """
    Perform log-likelihood ratio test between nested models.

    Tests the null hypothesis that the simpler model is adequate
    against the alternative that the more complex model is better.

    Args:
        ll_null: Log-likelihood of null (simpler) model
        ll_alt: Log-likelihood of alternative (complex) model
        df_diff: Difference in degrees of freedom (parameters)
        alpha: Significance level

    Returns:
        Dictionary with test results
    """
    # Compute test statistic
    lr_statistic = 2 * (ll_alt - ll_null)

    # P-value from chi-squared distribution
    p_value = 1 - stats.chi2.cdf(lr_statistic, df_diff)

    # Critical value
    critical_value = stats.chi2.ppf(1 - alpha, df_diff)

    # Decision
    reject_null = lr_statistic > critical_value

    return {
        "lr_statistic": lr_statistic,
        "p_value": p_value,
        "critical_value": critical_value,
        "reject_null": reject_null,
        "alpha": alpha,
        "df_diff": df_diff,
        "conclusion": (
            "Reject null model (complex model is significantly better)"
            if reject_null
            else "Fail to reject null model (simpler model is adequate)"
        ),
    }


def compute_cross_entropy(
    true_probs: NDArray[np.float64], pred_probs: NDArray[np.float64]
) -> float:
    """
    Compute cross-entropy between true and predicted probability distributions.

    Args:
        true_probs: True probability distribution
        pred_probs: Predicted probability distribution

    Returns:
        Cross-entropy value
    """
    # Avoid log(0) by adding small epsilon
    epsilon = 1e-12
    pred_probs = np.clip(pred_probs, epsilon, 1 - epsilon)

    return -np.sum(true_probs * safe_log(pred_probs))


def compute_kl_divergence(p: NDArray[np.float64], q: NDArray[np.float64]) -> float:
    """
    Compute Kullback-Leibler divergence between two distributions.

    KL(P||Q) = sum(P * log(P/Q))

    Args:
        p: First probability distribution
        q: Second probability distribution

    Returns:
        KL divergence (non-negative, 0 if distributions are identical)
    """
    epsilon = 1e-12
    p = np.clip(p, epsilon, 1 - epsilon)
    q = np.clip(q, epsilon, 1 - epsilon)

    return np.sum(p * safe_log(p / q))


def compute_model_complexity(n_states: int, n_observations: int) -> int:
    """
    Compute number of free parameters in a discrete HMM.

    Args:
        n_states: Number of hidden states
        n_observations: Number of observable symbols

    Returns:
        Number of free parameters
    """
    # Start probabilities: n_states - 1 (sum to 1 constraint)
    start_params = n_states - 1

    # Transition probabilities: n_states * (n_states - 1)
    transition_params = n_states * (n_states - 1)

    # Emission probabilities: n_states * (n_observations - 1)
    emission_params = n_states * (n_observations - 1)

    return start_params + transition_params + emission_params


def evaluate_model_fit(
    hmm_model, train_sequences: List[NDArray], test_sequences: List[NDArray]
) -> dict:
    """
    Comprehensive evaluation of HMM model fit.

    Args:
        hmm_model: Trained HMM model
        train_sequences: Training sequences
        test_sequences: Test sequences

    Returns:
        Dictionary with evaluation metrics
    """
    # Training metrics
    train_ll = sum(hmm_model.score(seq) for seq in train_sequences)
    train_n_obs = sum(len(seq) for seq in train_sequences)

    # Test metrics
    test_ll = sum(hmm_model.score(seq) for seq in test_sequences)
    test_n_obs = sum(len(seq) for seq in test_sequences)

    # Model complexity
    n_params = compute_model_complexity(hmm_model.n_states, hmm_model.n_observations)

    # Information criteria
    train_aic = compute_aic(train_ll, n_params)
    train_bic = compute_bic(train_ll, n_params, train_n_obs)

    test_aic = compute_aic(test_ll, n_params)
    test_bic = compute_bic(test_ll, n_params, test_n_obs)

    # Perplexity
    train_perplexity = compute_perplexity(train_ll, train_n_obs)
    test_perplexity = compute_perplexity(test_ll, test_n_obs)

    return {
        "training": {
            "log_likelihood": train_ll,
            "n_observations": train_n_obs,
            "aic": train_aic,
            "bic": train_bic,
            "perplexity": train_perplexity,
        },
        "test": {
            "log_likelihood": test_ll,
            "n_observations": test_n_obs,
            "aic": test_aic,
            "bic": test_bic,
            "perplexity": test_perplexity,
        },
        "model": {
            "n_states": hmm_model.n_states,
            "n_observations": hmm_model.n_observations,
            "n_parameters": n_params,
        },
    }


def compare_models(models: List, test_sequences: List[NDArray]) -> dict:
    """
    Compare multiple HMM models using information criteria.

    Args:
        models: List of trained HMM models
        test_sequences: Test sequences for evaluation

    Returns:
        Dictionary with model comparison results
    """
    results = []

    for i, model in enumerate(models):
        # Compute test log-likelihood
        test_ll = sum(model.score(seq) for seq in test_sequences)
        test_n_obs = sum(len(seq) for seq in test_sequences)

        # Model complexity
        n_params = compute_model_complexity(model.n_states, model.n_observations)

        # Information criteria
        aic = compute_aic(test_ll, n_params)
        bic = compute_bic(test_ll, n_params, test_n_obs)
        perplexity = compute_perplexity(test_ll, test_n_obs)

        results.append(
            {
                "model_index": i,
                "n_states": model.n_states,
                "log_likelihood": test_ll,
                "n_parameters": n_params,
                "aic": aic,
                "bic": bic,
                "perplexity": perplexity,
            }
        )

    # Find best models
    best_aic_idx = np.argmin([r["aic"] for r in results])
    best_bic_idx = np.argmin([r["bic"] for r in results])
    best_ll_idx = np.argmax([r["log_likelihood"] for r in results])

    return {
        "results": results,
        "best_aic_model": best_aic_idx,
        "best_bic_model": best_bic_idx,
        "best_likelihood_model": best_ll_idx,
    }
