# import numpy as np
# from .viterbi_algorithm import find_most_likely_path


# def initialize_params(n_states, n_observations, same_prob=False):

#     if same_prob:
#         A = np.ndarray((n_states, n_states))
#         A[:, :] = 1 / n_states
#         B = np.ndarray((n_states, n_observations))
#         B[:, :] = 1 / n_observations
#     else:
#         A = np.random.rand(n_states, n_states)
#         A = A / np.sum(A, axis=1, keepdims=True)
#         B = np.random.rand(n_states, n_observations)
#         B = B / np.sum(B, axis=1, keepdims=True)

#     return (A, B)


# def count_transition_pairs(state_sequences, start_, next_=None):

#     count = 0
#     for state_seq in state_sequences:
#         # The last state of each sequence will be ignored
#         for i in range(len(state_seq) - 1):

#             if (state_seq[i] == start_
#                     and (state_seq[i + 1] == next_ or next_ is None)):
#                 count += 1

#     return count


# def count_emission_pairs(state_sequences, obs, y, x=None):

#     state_seq = np.array(state_sequences).flatten()
#     ob_seq = np.array(obs).flatten()

#     count = 0
#     for i in range(state_seq.shape[0]):
#         if state_seq[i] == y and (ob_seq[i] == x or x is None):
#             count += 1

#     return count


# def compute_initial_prob(n_states, state_sequences):

#     start_prob = np.zeros(n_states)
#     for state_seq in state_sequences:
#         start_prob[state_seq[0]] += 1

#     start_prob = start_prob / sum(start_prob)

#     return start_prob


# def update_params(n_states, n_observations, y, x):

#     A = np.zeros((n_states, n_states))
#     B = np.zeros((n_states, n_observations))
#     start_prob = compute_initial_prob(n_states, y)

#     for i in range(n_states):
#         n_trans_start_with_i = count_transition_pairs(y, i)
#         n_emis_start_with_i = count_emission_pairs(y, x, i)

#         # Update Transition Matrix A
#         for j in range(n_states):
#             if n_trans_start_with_i != 0:
#                 A[i, j] = count_transition_pairs(y, i, j) / n_trans_start_with_i

#         # Update Emission Matrix B
#         for j in range(n_observations):
#             if n_emis_start_with_i != 0:
#                 B[i, j] = count_emission_pairs(y, x, i, j) / n_emis_start_with_i

#     return (A, B, start_prob)


# def diff_of_params(param_1, param_2):

#     A_1, B_1, start_prob_1 = param_1
#     A_2, B_2, start_prob_2 = param_2

#     flat_param_1 = np.concatenate([A_1.flatten(), B_1.flatten(),
#                                    start_prob_1.flatten()])
#     flat_param_2 = np.concatenate([A_2.flatten(), B_2.flatten(),
#                                    start_prob_2.flatten()])

#     diff = (1 / len(flat_param_1)) * np.sqrt(np.sum(np.power(flat_param_1 - flat_param_2, 2)))

#     return diff


# def train(n_states, obs, n_iter=50):

#     n_observations = np.unique(obs).shape[0]

#     # Initialization step:
#     A, B = initialize_params(n_states, n_observations)
#     initial_A, initial_B = A, B
#     start_prob = np.ndarray(n_states)
#     start_prob[:] = 1 / n_states

#     param_logs = []
#     state_seq_logs = []
#     diff_logs = []

#     for i in range(n_iter):

#         # Find the most likely state sequences corresponding to {A, B}
#         state_sequences = []
#         for o in obs:
#             initial_prob = start_prob * B[:, o[0]]
#             _, _, probable_seq = find_most_likely_path(o, A, B, initial_prob)
#             state_sequences.append(probable_seq)

#         A_next, B_next, start_prob_next = update_params(n_states, n_observations, state_sequences, obs)
#         diff = diff_of_params((A, B, start_prob),
#                               (A_next, B_next, start_prob_next))
#         A, B, start_prob = A_next, B_next, start_prob_next

#         param_logs.append((A_next, B_next, start_prob))
#         state_seq_logs.append(state_sequences)
#         diff_logs.append(diff)

#         if diff == 0:
#             break

#     return {"initial_A": initial_A,
#             "initial_B": initial_B,
#             "A": A, "B": B,
#             "start_prob": start_prob,
#             "param_logs": param_logs,
#             "state_seq_logs":state_seq_logs,
#             "diff_logs": diff_logs}

import numpy as np

from .viterbi_algorithm import find_most_likely_path


def initialize_params(n_states, n_observations, same_prob=False):
    """Initialize HMM parameters either uniformly or randomly."""
    if same_prob:
        A = np.full((n_states, n_states), 1 / n_states)
        B = np.full((n_states, n_observations), 1 / n_observations)
    else:
        A = np.random.rand(n_states, n_states)
        A = A / np.sum(A, axis=1, keepdims=True)  # Normalize rows
        B = np.random.rand(n_states, n_observations)
        B = B / np.sum(B, axis=1, keepdims=True)  # Normalize rows

    return (A, B)


def count_transition_pairs(state_sequences, start_, next_=None):
    """Count transitions from start_ to next_ (or all transitions from start_ if next_ is None)."""
    count = 0
    for state_seq in state_sequences:
        for i in range(len(state_seq) - 1):
            if state_seq[i] == start_ and (next_ is None or state_seq[i + 1] == next_):
                count += 1
    return count


def count_emission_pairs(state_sequences, obs, y, x=None):
    """Count emissions of x (or all emissions) when in state y."""
    count = 0
    # Process sequences individually to maintain alignment
    for seq_idx in range(len(state_sequences)):
        state_seq = state_sequences[seq_idx]
        ob_seq = obs[seq_idx]

        for i in range(len(state_seq)):
            if state_seq[i] == y and (x is None or ob_seq[i] == x):
                count += 1
    return count


def compute_initial_prob(n_states, state_sequences):
    """Compute initial state probabilities from sequences."""
    start_prob = np.zeros(n_states)
    for state_seq in state_sequences:
        start_prob[state_seq[0]] += 1

    # Avoid division by zero
    if np.sum(start_prob) > 0:
        start_prob = start_prob / np.sum(start_prob)
    else:
        # If no valid sequences, use uniform distribution
        start_prob = np.full(n_states, 1 / n_states)

    return start_prob


def update_params(n_states, n_observations, y, x):
    """Update HMM parameters based on state and observation sequences."""
    A = np.zeros((n_states, n_states))
    B = np.zeros((n_states, n_observations))
    start_prob = compute_initial_prob(n_states, y)

    # Small value to avoid zeros in probability matrices
    epsilon = 1e-10

    for i in range(n_states):
        n_trans_start_with_i = count_transition_pairs(y, i)
        n_emis_start_with_i = count_emission_pairs(y, x, i)

        # Update Transition Matrix A
        for j in range(n_states):
            transitions_i_to_j = count_transition_pairs(y, i, j)
            if n_trans_start_with_i > 0:
                A[i, j] = transitions_i_to_j / n_trans_start_with_i
            else:
                # If no transitions from state i, use uniform distribution
                A[i, j] = 1 / n_states

        # Update Emission Matrix B
        for j in range(n_observations):
            emissions_i_of_j = count_emission_pairs(y, x, i, j)
            if n_emis_start_with_i > 0:
                B[i, j] = emissions_i_of_j / n_emis_start_with_i
            else:
                # If no emissions from state i, use uniform distribution
                B[i, j] = 1 / n_observations

    # Ensure matrices have no zeros (for log calculations in Viterbi)
    A = np.maximum(A, epsilon)
    A = A / np.sum(A, axis=1, keepdims=True)

    B = np.maximum(B, epsilon)
    B = B / np.sum(B, axis=1, keepdims=True)

    return (A, B, start_prob)


def diff_of_params(param_1, param_2):
    """Calculate difference between two parameter sets."""
    A_1, B_1, start_prob_1 = param_1
    A_2, B_2, start_prob_2 = param_2

    flat_param_1 = np.concatenate(
        [A_1.flatten(), B_1.flatten(), start_prob_1.flatten()]
    )
    flat_param_2 = np.concatenate(
        [A_2.flatten(), B_2.flatten(), start_prob_2.flatten()]
    )

    diff = np.sqrt(np.mean(np.power(flat_param_1 - flat_param_2, 2)))
    return diff


def train(n_states, obs, n_iter=50, convergence_threshold=1e-6):
    """
    Train an HMM using the Viterbi training algorithm.

    Args:
        n_states: Number of hidden states
        obs: List of observation sequences
        n_iter: Maximum number of iterations
        convergence_threshold: Stop when parameter difference is below this value

    Returns:
        Dictionary with trained parameters and training logs
    """
    # Check if observations are encoded as integers
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

    # Initialization step
    A, B = initialize_params(n_states, n_observations)
    initial_A, initial_B = A.copy(), B.copy()
    start_prob = np.full(n_states, 1 / n_states)

    param_logs = []
    state_seq_logs = []
    diff_logs = []

    for i in range(n_iter):
        # Find the most likely state sequences corresponding to {A, B}
        state_sequences = []
        for o in obs:
            # Use modified Viterbi from updated implementation
            # which returns (log_prob, state_sequence)
            _, probable_seq = find_most_likely_path(o, A, B, start_prob)
            state_sequences.append(probable_seq)

        A_next, B_next, start_prob_next = update_params(
            n_states, n_observations, state_sequences, obs
        )
        diff = diff_of_params((A, B, start_prob), (A_next, B_next, start_prob_next))

        A, B, start_prob = A_next, B_next, start_prob_next

        param_logs.append((A_next.copy(), B_next.copy(), start_prob.copy()))
        state_seq_logs.append([seq.copy() for seq in state_sequences])
        diff_logs.append(diff)

        if diff < convergence_threshold:
            break

    return {
        "initial_A": initial_A,
        "initial_B": initial_B,
        "A": A,
        "B": B,
        "start_prob": start_prob,
        "param_logs": param_logs,
        "state_seq_logs": state_seq_logs,
        "diff_logs": diff_logs,
        "iterations": i + 1,
    }
