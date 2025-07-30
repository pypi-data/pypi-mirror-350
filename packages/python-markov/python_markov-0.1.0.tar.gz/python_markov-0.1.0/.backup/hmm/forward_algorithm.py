import numpy as np


def compute_alpha(t, x_t, A, B, alpha_matrix):
    """
    Compute the joint probability of each state and observation x_t at time t.
    x_t is a index of 'observations' list.

    Arguments:
    t            -- Time t.
    x_t          -- The observation at time t.
    A            -- State Transition Matrix.
    B            -- Emission Matrix.
    alpha_matrix -- Alpha Matrix

    Return:
    alphas       -- A list of alpha values corresponding to each state y_t
    """

    n_states = A.shape[0]
    alphas = np.zeros((1, n_states))

    for y_t in range(n_states):
        s = 0
        for previous_y_t in range(n_states):
            s += A[previous_y_t, y_t] * alpha_matrix[t - 1, previous_y_t]

        alphas[0, y_t] = B[y_t, x_t] * s

    # alphas is a matrix with size (1, n_states)
    return alphas


def compute_alpha_vec(t, x_t, A, B, alpha_matrix):
    """
    This is vectorized version of function 'compute_alpha'. It requires the same
    arguments and generates the same output also.

    Arguments:
    t            -- Time t.
    x_t          -- The observation at time t.
    A            -- State Transition Matrix.
    B            -- Emission Matrix.
    alpha_matrix -- Alpha Matrix

    Return:
    alphas       -- A list of alpha values corresponding to each state y_t
    """

    # alphas is a matrix with size (1, n_states)
    alphas = B[:, x_t].T * np.dot(alpha_matrix[t - 1, :], A)

    return alphas


def compute_forward_prob(x, A, B, init_prob):
    """
    An implementation of Forward algorithm that computes the forward probability
    of the observation sequence.

    Arguments:
    x               -- A sequence of observations.
    A               -- State Transition Matrix.
    B               -- Emission Matrix.
    init_prob       -- The initial probability of Forward trellis matrix.

    Return:
    forward_output  -- A tuple that contains the computed forward trellis matrix
    and the probability of the observation sequence.
    """

    # alpha_matrix[i, j] is the probability of the state_j at time t_i, given by x_0,.. x_t
    alpha_matrix = np.ndarray((len(x), A.shape[0]))

    # Initialize with initial probabilities * emission probabilities
    alpha_matrix[0, :] = init_prob * B[:, x[0]]

    for t, x_t in enumerate(x):
        # We don't compute alpha for t = 0
        if t == 0:
            continue

        # Build Alpha trellis matrix.
        alphas = compute_alpha_vec(t, x_t, A, B, alpha_matrix).round(6)
        alpha_matrix[t, :] = alphas

    sequence_prob = np.sum(alpha_matrix[-1, :])

    return (alpha_matrix, sequence_prob)
