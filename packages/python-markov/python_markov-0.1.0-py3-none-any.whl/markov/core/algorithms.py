"""
Core Hidden Markov Model algorithms implementation.
"""

from typing import List, Tuple

import numpy as np
from numpy.typing import NDArray

from ..utils.math_utils import (
    EPSILON,
    LOG_ZERO,
    log_sum_exp,
    normalize_log_probs_axis,
    safe_exp,
    safe_log,
)


def forward_algorithm(
    log_start_probs: NDArray[np.float64],
    log_transition_probs: NDArray[np.float64],
    log_emission_probs: NDArray[np.float64],
) -> Tuple[NDArray[np.float64], float]:
    """
    Forward algorithm for computing observation sequence probability.

    Args:
        log_start_probs: Log initial state probabilities [n_states]
        log_transition_probs: Log transition probabilities [n_states, n_states]
        log_emission_probs: Log emission probabilities [T, n_states]

    Returns:
        Tuple of (forward probabilities [T, n_states], log-likelihood)
    """
    T, n_states = log_emission_probs.shape

    # Initialize forward probabilities
    log_forward = np.full((T, n_states), LOG_ZERO, dtype=np.float64)

    # Initial step: π_i * b_i(o_1)
    log_forward[0] = log_start_probs + log_emission_probs[0]

    # Forward recursion
    for t in range(1, T):
        for j in range(n_states):
            # Sum over all previous states
            log_forward[t, j] = (
                log_sum_exp(log_forward[t - 1] + log_transition_probs[:, j])
                + log_emission_probs[t, j]
            )

    # Compute log-likelihood
    log_likelihood = log_sum_exp(log_forward[T - 1])

    return log_forward, log_likelihood


def backward_algorithm(
    log_transition_probs: NDArray[np.float64], log_emission_probs: NDArray[np.float64]
) -> NDArray[np.float64]:
    """
    Backward algorithm for computing backward probabilities.

    Args:
        log_transition_probs: Log transition probabilities [n_states, n_states]
        log_emission_probs: Log emission probabilities [T, n_states]

    Returns:
        Backward probabilities [T, n_states]
    """
    T, n_states = log_emission_probs.shape

    # Initialize backward probabilities
    log_backward = np.full((T, n_states), LOG_ZERO, dtype=np.float64)

    # Terminal step: β_T(i) = 1 for all i
    log_backward[T - 1] = 0.0  # log(1) = 0

    # Backward recursion
    for t in range(T - 2, -1, -1):
        for i in range(n_states):
            # Sum over all next states
            log_backward[t, i] = log_sum_exp(
                log_transition_probs[i]
                + log_emission_probs[t + 1]
                + log_backward[t + 1]
            )

    return log_backward


def viterbi_algorithm(
    log_start_probs: NDArray[np.float64],
    log_transition_probs: NDArray[np.float64],
    log_emission_probs: NDArray[np.float64],
) -> Tuple[NDArray[np.int32], float]:
    """
    Viterbi algorithm for finding most likely state sequence.

    Args:
        log_start_probs: Log initial state probabilities [n_states]
        log_transition_probs: Log transition probabilities [n_states, n_states]
        log_emission_probs: Log emission probabilities [T, n_states]

    Returns:
        Tuple of (most likely state sequence [T], log probability)
    """
    T, n_states = log_emission_probs.shape

    # Initialize Viterbi probabilities and path
    log_viterbi = np.full((T, n_states), LOG_ZERO, dtype=np.float64)
    path = np.zeros((T, n_states), dtype=np.int32)

    # Initial step
    log_viterbi[0] = log_start_probs + log_emission_probs[0]

    # Forward pass
    for t in range(1, T):
        for j in range(n_states):
            # Find most likely previous state
            transition_scores = log_viterbi[t - 1] + log_transition_probs[:, j]
            best_prev_state = np.argmax(transition_scores)

            log_viterbi[t, j] = (
                transition_scores[best_prev_state] + log_emission_probs[t, j]
            )
            path[t, j] = best_prev_state

    # Find best final state
    best_final_state = np.argmax(log_viterbi[T - 1])
    best_log_prob = log_viterbi[T - 1, best_final_state]

    # Backward pass to reconstruct path
    states = np.zeros(T, dtype=np.int32)
    states[T - 1] = best_final_state

    for t in range(T - 2, -1, -1):
        states[t] = path[t + 1, states[t + 1]]

    return states, best_log_prob


def forward_backward_algorithm(
    log_start_probs: NDArray[np.float64],
    log_transition_probs: NDArray[np.float64],
    log_emission_probs: NDArray[np.float64],
) -> Tuple[NDArray[np.float64], NDArray[np.float64], float]:
    """
    Forward-backward algorithm for computing posterior state probabilities.

    Args:
        log_start_probs: Log initial state probabilities [n_states]
        log_transition_probs: Log transition probabilities [n_states, n_states]
        log_emission_probs: Log emission probabilities [T, n_states]

    Returns:
        Tuple of (gamma [T, n_states], xi [T-1, n_states, n_states], log_likelihood)
    """
    T, n_states = log_emission_probs.shape

    # Run forward and backward algorithms
    log_forward, log_likelihood = forward_algorithm(
        log_start_probs, log_transition_probs, log_emission_probs
    )
    log_backward = backward_algorithm(log_transition_probs, log_emission_probs)

    # Compute gamma (posterior state probabilities)
    log_gamma = log_forward + log_backward
    log_gamma = normalize_log_probs_axis(log_gamma, axis=1)

    # Compute xi (posterior transition probabilities)
    log_xi = np.full((T - 1, n_states, n_states), LOG_ZERO, dtype=np.float64)

    for t in range(T - 1):
        for i in range(n_states):
            for j in range(n_states):
                log_xi[t, i, j] = (
                    log_forward[t, i]
                    + log_transition_probs[i, j]
                    + log_emission_probs[t + 1, j]
                    + log_backward[t + 1, j]
                    - log_likelihood
                )

    return safe_exp(log_gamma), safe_exp(log_xi), log_likelihood


def baum_welch_step(
    sequences: List[NDArray],
    log_start_probs: NDArray[np.float64],
    log_transition_probs: NDArray[np.float64],
    emission_model: object,
) -> Tuple[NDArray[np.float64], NDArray[np.float64], float]:
    """
    Single step of Baum-Welch algorithm (E-step + M-step).

    Args:
        sequences: List of observation sequences
        log_start_probs: Current log start probabilities
        log_transition_probs: Current log transition probabilities
        emission_model: Emission model (handles its own updates)

    Returns:
        Tuple of (new log_start_probs, new log_transition_probs, total_log_likelihood)
    """
    n_states = len(log_start_probs)
    n_sequences = len(sequences)

    # Accumulators for parameter updates
    start_counts = np.zeros(n_states)
    transition_counts = np.zeros((n_states, n_states))
    total_log_likelihood = 0.0

    # E-step: compute statistics for each sequence
    all_gammas = []
    all_xis = []

    for seq in sequences:
        # Get emission probabilities from model
        log_emission_probs = emission_model.log_probability_matrix(seq)

        # Forward-backward
        gamma, xi, log_likelihood = forward_backward_algorithm(
            log_start_probs, log_transition_probs, log_emission_probs
        )

        all_gammas.append(gamma)
        all_xis.append(xi)
        total_log_likelihood += log_likelihood

        # Accumulate counts
        start_counts += gamma[0]
        transition_counts += np.sum(xi, axis=0)

    # M-step: update parameters

    # Update start probabilities
    new_start_probs = start_counts / n_sequences
    new_start_probs = np.maximum(new_start_probs, EPSILON)
    new_start_probs /= np.sum(new_start_probs)

    # Update transition probabilities
    row_sums = np.sum(transition_counts, axis=1, keepdims=True)
    row_sums = np.maximum(row_sums, EPSILON)
    new_transition_probs = transition_counts / row_sums

    # Update emission parameters (delegated to emission model)
    emission_model.update_parameters(sequences, all_gammas)

    return (
        safe_log(new_start_probs),
        safe_log(new_transition_probs),
        total_log_likelihood,
    )


def fit_hmm_baum_welch(
    sequences: List[NDArray],
    initial_start_probs: NDArray[np.float64],
    initial_transition_probs: NDArray[np.float64],
    emission_model: object,
    n_iter: int = 100,
    tol: float = 1e-6,
    verbose: bool = False,
) -> Tuple[NDArray[np.float64], NDArray[np.float64], List[float]]:
    """
    Fit HMM parameters using Baum-Welch algorithm.

    Args:
        sequences: Training sequences
        initial_start_probs: Initial start probabilities
        initial_transition_probs: Initial transition probabilities
        emission_model: Emission model to train
        n_iter: Maximum iterations
        tol: Convergence tolerance
        verbose: Print progress

    Returns:
        Tuple of (final_start_probs, final_transition_probs, log_likelihood_history)
    """
    log_start_probs = safe_log(initial_start_probs)
    log_transition_probs = safe_log(initial_transition_probs)

    log_likelihood_history = []
    prev_log_likelihood = LOG_ZERO

    for iteration in range(n_iter):
        # Baum-Welch step
        log_start_probs, log_transition_probs, log_likelihood = baum_welch_step(
            sequences, log_start_probs, log_transition_probs, emission_model
        )

        log_likelihood_history.append(log_likelihood)

        if verbose:
            print(f"Iteration {iteration + 1}: Log-likelihood = {log_likelihood:.6f}")

        # Check convergence
        if iteration > 0:
            ll_change = abs(log_likelihood - prev_log_likelihood)
            if ll_change < tol:
                if verbose:
                    print(f"Converged after {iteration + 1} iterations")
                break

        prev_log_likelihood = log_likelihood

    return (
        safe_exp(log_start_probs),
        safe_exp(log_transition_probs),
        log_likelihood_history,
    )


def sample_hmm(
    start_probs: NDArray[np.float64],
    transition_probs: NDArray[np.float64],
    emission_model: object,
    n_samples: int,
    random_state: int = None,
) -> Tuple[NDArray, NDArray[np.int32]]:
    """
    Generate samples from an HMM.

    Args:
        start_probs: Initial state probabilities
        transition_probs: State transition probabilities
        emission_model: Emission model for generating observations
        n_samples: Number of samples to generate
        random_state: Random seed

    Returns:
        Tuple of (observations, states)
    """
    if random_state is not None:
        np.random.seed(random_state)

    n_states = len(start_probs)
    states = np.zeros(n_samples, dtype=np.int32)
    observations = []

    # Sample initial state
    states[0] = np.random.choice(n_states, p=start_probs)

    # Sample remaining states and observations
    for t in range(n_samples):
        if t > 0:
            states[t] = np.random.choice(n_states, p=transition_probs[states[t - 1]])

        # Sample observation from emission model
        obs = emission_model.sample(states[t])
        observations.append(obs)

    return np.array(observations), states
