import time

import numpy as np

import cpp_markov_algorithms as hmm


def python_forward(A, B, pi, observations):
    """
    Pure Python implementation of the Forward algorithm for comparison
    """
    n_states = A.shape[0]
    seq_length = len(observations)

    # Initialize forward variables
    forward = np.zeros((seq_length, n_states))
    scaling = np.zeros(seq_length)

    # Initialize for t=0
    forward[0] = pi * B[:, observations[0]]
    scaling[0] = np.sum(forward[0])
    forward[0] /= scaling[0]

    # Induction
    for t in range(1, seq_length):
        for j in range(n_states):
            forward[t, j] = np.sum(forward[t - 1] * A[:, j]) * B[j, observations[t]]

        scaling[t] = np.sum(forward[t])
        forward[t] /= scaling[t]

    # Calculate log-likelihood
    log_likelihood = -np.sum(np.log(scaling))

    return log_likelihood, forward


def test_hmm(print_details=True):
    """Test the HMM Forward algorithm implementation"""

    # Define a simple HMM model
    # Transition matrix (A)
    A = np.array(
        [[0.7, 0.3], [0.4, 0.6]],  # State 0 transitions  # State 1 transitions
        dtype=np.float64,
    )

    # Emission matrix (B)
    B = np.array(
        [
            [0.1, 0.4, 0.5],  # State 0 emissions for symbols 0,1,2
            [0.6, 0.3, 0.1],  # State 1 emissions for symbols 0,1,2
        ],
        dtype=np.float64,
    )

    # Initial state probabilities (π)
    pi = np.array([0.6, 0.4], dtype=np.float64)

    # Observation sequence
    obs = np.array([0, 1, 2, 1, 0], dtype=np.int32)

    if print_details:
        print("HMM Model:")
        print(f"Transition Matrix (A):\n{A}")
        print(f"Emission Matrix (B):\n{B}")
        print(f"Initial Probabilities (π):\n{pi}")
        print(f"Observation Sequence:\n{obs}")
        print("-" * 50)

    # Run C++ implementation
    start_time = time.time()
    cpp_log_likelihood, cpp_forward = hmm.forward(A, B, pi, obs)
    cpp_time = time.time() - start_time

    # Run Python implementation
    start_time = time.time()
    py_log_likelihood, py_forward = python_forward(A, B, pi, obs)
    py_time = time.time() - start_time

    # Compare results
    log_likelihood_diff = abs(cpp_log_likelihood - py_log_likelihood)
    forward_diff = np.max(np.abs(cpp_forward - py_forward))

    if print_details:
        print("Results:")
        print(f"C++ Log-Likelihood: {cpp_log_likelihood}")
        print(f"Python Log-Likelihood: {py_log_likelihood}")
        print(f"Log-Likelihood Difference: {log_likelihood_diff}")
        print(f"Max Forward Variable Difference: {forward_diff}")
        print(f"C++ Time: {cpp_time:.6f} seconds")
        print(f"Python Time: {py_time:.6f} seconds")
        print(f"Speedup: {py_time/cpp_time:.2f}x")

        print("\nC++ Forward Variables:")
        print(cpp_forward)
        print("\nPython Forward Variables:")
        print(py_forward)

    # Test passes if differences are small
    passed = log_likelihood_diff < 1e-10 and forward_diff < 1e-10

    if print_details:
        print(f"\nTest {'PASSED' if passed else 'FAILED'}")

    return passed


if __name__ == "__main__":
    test_hmm()
