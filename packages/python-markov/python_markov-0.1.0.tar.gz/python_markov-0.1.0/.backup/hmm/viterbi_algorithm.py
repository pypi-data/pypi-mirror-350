import numpy as np


def compute_v(t, x_t, A, B, v_matrix):
    """
    Compute list of Viterbi Trellises of x_t.

    Arguments:
    t               -- Time t.
    x_t             -- The observation at time t.
    A               -- State Transaction Matrix.
    B               -- Emission Matrix.
    v_matrix        -- Represents the Viterbi trellis (in log space)

    Return:
    viterbi_output  -- A tuple that contains computed v_t and back_pointer.
    """

    n_states = A.shape[0]
    v_t = np.full((1, n_states), -np.inf)
    back_pointer = np.ndarray((1, n_states))

    for y_t in range(n_states):
        # Skip if emission probability is zero
        if B[y_t, x_t] <= 0:
            continue

        log_emission = np.log(B[y_t, x_t])

        for previous_y_t in range(n_states):
            # Skip if transition probability is zero or previous state had -inf probability
            if A[previous_y_t, y_t] <= 0 or v_matrix[t - 1, previous_y_t] == -np.inf:
                continue

            # Calculate in log space (addition instead of multiplication)
            temp_v = (
                v_matrix[t - 1, previous_y_t]
                + np.log(A[previous_y_t, y_t])
                + log_emission
            )

            if temp_v > v_t[0, y_t]:
                v_t[0, y_t] = temp_v
                back_pointer[0, y_t] = previous_y_t

    return (v_t, back_pointer)


def find_most_likely_path(x, A, B, init_prob):
    """
    An implementation of Viterbi algorithm that finds the most probable
    sequence of states of a known observation sequence.

    Arguments:
    x               -- A sequence of observations.
    A               -- State Transition Matrix.
    B               -- Emission Matrix.
    init_prob       -- The initial probability of the Viterbi trellis matrix.

    Return:
    viterbi_output  -- A tuple that contains:
                       - log probability of the most likely path
                       - most likely state sequence
    """
    # Validate input dimensions
    n_states = A.shape[0]
    seq_length = len(x)

    if A.shape[1] != n_states:
        raise ValueError("Transition matrix must be square")
    if B.shape[0] != n_states:
        raise ValueError("Emission matrix rows must match number of states")
    if init_prob.shape[0] != n_states:
        raise ValueError("Initial probabilities length must match number of states")

    # v_matrix stores log probabilities
    v_matrix = np.full((seq_length, n_states), -np.inf)

    # Initialize the first step with log probabilities
    for i in range(n_states):
        if init_prob[i] > 0 and B[i, x[0]] > 0:
            v_matrix[0, i] = np.log(init_prob[i]) + np.log(B[i, x[0]])

    back_pointer_matrix = np.ndarray(v_matrix.shape)
    back_pointer_matrix[0, :] = 0

    for t in range(1, seq_length):
        # Build Viterbi matrix
        v_t, back_pointer = compute_v(t, x[t], A, B, v_matrix)
        v_matrix[t, :] = v_t
        back_pointer_matrix[t, :] = back_pointer

    # Find most likely final state
    max_final_val = np.max(v_matrix[-1, :])

    # Check if no valid path was found
    if max_final_val == -np.inf:
        raise RuntimeError("No valid state sequence found for the given observations")

    # Backtrace process
    probable_seq = np.zeros(seq_length, dtype=int)
    probable_seq[-1] = np.argmax(v_matrix[-1, :])

    for t in range(seq_length - 1, 0, -1):
        probable_seq[t - 1] = int(back_pointer_matrix[t, probable_seq[t]])

    return (max_final_val, probable_seq)
