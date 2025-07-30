import numpy as np


def compute_beta(t, x_tp1, A, B, beta_matrix):
    """
    Compute the backward probability at time t.

    Arguments:
    t           -- Time t.
    x_tp1       -- The observation at time t+1.
    A           -- State Transition Matrix.
    B           -- Emission Matrix.
    beta_matrix -- Beta Matrix

    Return:
    betas       -- A list of beta values corresponding to each state y_t
    """
    n_states = A.shape[0]
    betas = np.zeros((1, n_states))

    for y_t in range(n_states):
        s = 0
        for next_y_t in range(n_states):
            s += A[y_t, next_y_t] * B[next_y_t, x_tp1] * beta_matrix[t + 1, next_y_t]
        betas[0, y_t] = s

    return betas


def compute_beta_vec(t, x_tp1, A, B, beta_matrix):
    """
    Vectorized version of compute_beta.

    Arguments:
    t           -- Time t.
    x_tp1       -- The observation at time t+1.
    A           -- State Transition Matrix.
    B           -- Emission Matrix.
    beta_matrix -- Beta Matrix

    Return:
    betas       -- A list of beta values corresponding to each state y_t
    """
    return np.dot(A, B[:, x_tp1] * beta_matrix[t + 1, :])


def compute_backward_prob(x, A, B):
    """
    Compute backward probabilities for the given observation sequence.

    Arguments:
    x          -- A sequence of observations.
    A          -- State Transition Matrix.
    B          -- Emission Matrix.

    Return:
    beta_matrix -- Matrix of backward probabilities
    """
    n_states = A.shape[0]
    seq_length = len(x)

    beta_matrix = np.zeros((seq_length, n_states))
    # Initialize the last step with 1s
    beta_matrix[seq_length - 1, :] = 1.0

    # Work backwards from T-2 to 0
    for t in range(seq_length - 2, -1, -1):
        beta_t = compute_beta_vec(t, x[t + 1], A, B, beta_matrix)
        beta_matrix[t, :] = beta_t

    return beta_matrix


def compute_xi(t, x, A, B, alpha_matrix, beta_matrix):
    """
    Compute the joint probability of being in state i at time t and state j at time t+1.

    Arguments:
    t            -- Time t.
    x            -- Observation sequence.
    A            -- State Transition Matrix.
    B            -- Emission Matrix.
    alpha_matrix -- Alpha Matrix.
    beta_matrix  -- Beta Matrix.

    Return:
    xi           -- Matrix of probabilities P(y_t=i, y_{t+1}=j | x, model)
    """
    n_states = A.shape[0]
    xi = np.zeros((n_states, n_states))

    # Calculate denominator (probability of observation sequence)
    denom = np.sum(alpha_matrix[t, :] * beta_matrix[t, :])

    for i in range(n_states):
        for j in range(n_states):
            if t + 1 < len(x):  # Make sure we're not at the end of the sequence
                numer = (
                    alpha_matrix[t, i]
                    * A[i, j]
                    * B[j, x[t + 1]]
                    * beta_matrix[t + 1, j]
                )
                xi[i, j] = numer / (
                    denom + 1e-10
                )  # Add small value to avoid division by zero

    return xi


def compute_gamma(t, alpha_matrix, beta_matrix):
    """
    Compute the probability of being in state i at time t.

    Arguments:
    t            -- Time t.
    alpha_matrix -- Alpha Matrix.
    beta_matrix  -- Beta Matrix.

    Return:
    gamma        -- Array of probabilities P(y_t=i | x, model)
    """
    gamma = alpha_matrix[t, :] * beta_matrix[t, :]
    return gamma / (np.sum(gamma) + 1e-10)  # Add small value to avoid division by zero


def train_baum_welch(
    n_states, obs, n_iter=50, convergence_threshold=1e-6, same_prob=False
):
    """
    Train an HMM using the Baum-Welch algorithm.

    Args:
        n_states: Number of hidden states
        obs: List of observation sequences
        n_iter: Maximum number of iterations
        convergence_threshold: Stop when parameter difference is below this value
        same_prob: Whether to initialize parameters uniformly

    Returns:
        Dictionary with trained parameters and training logs
    """
    from .hidden_markov_model import diff_of_params, initialize_params

    # Process observations like in your original implementation
    all_obs = []
    for seq in obs:
        all_obs.extend(seq)
    unique_obs = np.unique(all_obs)
    n_observations = len(unique_obs)

    # Map observations to integers if they aren't already
    if not np.all(np.equal(np.sort(unique_obs), np.arange(n_observations))):
        obs_map = {o: i for i, o in enumerate(unique_obs)}
        mapped_obs = []
        for seq in obs:
            mapped_obs.append(np.array([obs_map[o] for o in seq]))
        obs = mapped_obs

    # Initialization
    A, B = initialize_params(n_states, n_observations, same_prob)
    initial_A, initial_B = A.copy(), B.copy()
    start_prob = np.full(n_states, 1 / n_states)

    param_logs = []
    diff_logs = []

    # Main training loop
    for iteration in range(n_iter):
        A_num = np.zeros((n_states, n_states))
        A_denom = np.zeros(n_states)
        B_num = np.zeros((n_states, n_observations))
        B_denom = np.zeros(n_states)
        start_prob_new = np.zeros(n_states)

        # Process each observation sequence
        for seq_idx, sequence in enumerate(obs):
            seq_length = len(sequence)

            # Forward pass
            from .forward_algorithm import compute_forward_prob

            alpha_matrix, _ = compute_forward_prob(sequence, A, B, start_prob)

            # Backward pass
            beta_matrix = compute_backward_prob(sequence, A, B)

            # Compute expected counts
            for t in range(seq_length):
                gamma_t = compute_gamma(t, alpha_matrix, beta_matrix)

                # Update expected initial state distribution (only from t=0)
                if t == 0:
                    start_prob_new += gamma_t

                # Update emission expectations
                for j in range(n_states):
                    B_denom[j] += gamma_t[j]
                    if t < seq_length:
                        B_num[j, sequence[t]] += gamma_t[j]

                # Update transition expectations
                if t < seq_length - 1:
                    xi_t = compute_xi(t, sequence, A, B, alpha_matrix, beta_matrix)
                    A_num += xi_t
                    A_denom += gamma_t

        # Re-estimate parameters
        # Re-estimate A
        for i in range(n_states):
            if A_denom[i] > 0:
                A[i, :] = A_num[i, :] / A_denom[i]
            else:
                A[i, :] = 1.0 / n_states  # Uniform if no observations

        # Re-estimate B
        for i in range(n_states):
            if B_denom[i] > 0:
                B[i, :] = B_num[i, :] / B_denom[i]
            else:
                B[i, :] = 1.0 / n_observations  # Uniform if no observations

        # Re-estimate start_prob
        if np.sum(start_prob_new) > 0:
            start_prob = start_prob_new / np.sum(start_prob_new)

        # Ensure no zeros (for numerical stability)
        epsilon = 1e-10
        A = np.maximum(A, epsilon)
        A = A / np.sum(A, axis=1, keepdims=True)

        B = np.maximum(B, epsilon)
        B = B / np.sum(B, axis=1, keepdims=True)

        # Log parameters
        param_logs.append((A.copy(), B.copy(), start_prob.copy()))

        # Check for convergence
        if iteration > 0:
            diff = diff_of_params(
                (param_logs[-2][0], param_logs[-2][1], param_logs[-2][2]),
                (A, B, start_prob),
            )
            diff_logs.append(diff)

            if diff < convergence_threshold:
                break
        else:
            diff_logs.append(1.0)  # Just a placeholder for the first iteration

    # Generate some state sequences using Viterbi for consistency with original interface
    from .viterbi_algorithm import find_most_likely_path

    state_sequences = []
    for sequence in obs:
        _, probable_seq = find_most_likely_path(sequence, A, B, start_prob)
        state_sequences.append(probable_seq)

    return {
        "initial_A": initial_A,
        "initial_B": initial_B,
        "A": A,
        "B": B,
        "start_prob": start_prob,
        "param_logs": param_logs,
        "state_seq_logs": [state_sequences],  # Just returning the final state sequences
        "diff_logs": diff_logs,
        "iterations": iteration + 1,
    }
