import matplotlib.pyplot as plt
import numpy as np

import cpp_markov_algorithms as hmm


def generate_sample_observations(
    n_sequences=10, seq_length=100, n_states=3, n_symbols=4, seed=42
):
    """Generate sample observation sequences from a random HMM for testing."""
    np.random.seed(seed)

    # Create random HMM parameters
    # Make sure rows sum to 1
    transition_matrix = np.random.rand(n_states, n_states)
    transition_matrix = transition_matrix / transition_matrix.sum(axis=1, keepdims=True)

    emission_matrix = np.random.rand(n_states, n_symbols)
    emission_matrix = emission_matrix / emission_matrix.sum(axis=1, keepdims=True)

    initial_probabilities = np.random.rand(n_states)
    initial_probabilities = initial_probabilities / initial_probabilities.sum()

    # Generate observation sequences
    observations = np.zeros((n_sequences, seq_length), dtype=np.int32)

    for s in range(n_sequences):
        # Choose initial state
        current_state = np.random.choice(n_states, p=initial_probabilities)

        # Generate sequence
        for t in range(seq_length):
            # Generate observation from current state
            observations[s, t] = np.random.choice(
                n_symbols, p=emission_matrix[current_state]
            )

            # Transition to next state
            current_state = np.random.choice(
                n_states, p=transition_matrix[current_state]
            )

    return observations, transition_matrix, emission_matrix, initial_probabilities


def print_model_params(name, transition_matrix, emission_matrix, initial_probs):
    """Helper function to print model parameters."""
    print(f"\n{name} Model Parameters:")
    print(f"Transition Matrix:\n{transition_matrix}")
    print(f"Emission Matrix:\n{emission_matrix}")
    print(f"Initial Probabilities:\n{initial_probs}")


def plot_convergence(log_likelihoods, title="Training Convergence"):
    """Plot the log-likelihood convergence."""
    plt.figure(figsize=(10, 6))
    plt.plot(log_likelihoods, "b-")
    plt.title(title)
    plt.xlabel("Iteration")
    plt.ylabel("Log-Likelihood")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def train_hmm_example():
    # Parameters
    n_states = 3
    n_symbols = 4
    n_sequences = 20
    seq_length = 10000
    max_iterations = 100

    print("Generating sample data...")
    observations, true_A, true_B, true_pi = generate_sample_observations(
        n_sequences=n_sequences,
        seq_length=seq_length,
        n_states=n_states,
        n_symbols=n_symbols,
    )

    # Print true model parameters
    print_model_params("True", true_A, true_B, true_pi)

    # Initialize with random values (starting point for training)
    np.random.seed(42)

    # Random initialization (ensure rows sum to 1)
    init_A = np.random.rand(n_states, n_states)
    init_A = init_A / init_A.sum(axis=1, keepdims=True)

    init_B = np.random.rand(n_states, n_symbols)
    init_B = init_B / init_B.sum(axis=1, keepdims=True)

    init_pi = np.random.rand(n_states)
    init_pi = init_pi / init_pi.sum()

    # Print initial model parameters
    print_model_params("Initial", init_A, init_B, init_pi)

    # Track log-likelihood progress
    log_likelihoods = []
    current_A = init_A.copy()
    current_B = init_B.copy()
    current_pi = init_pi.copy()

    print("\nTraining HMM using Baum-Welch algorithm...")

    # Manual iteration to track log-likelihood
    for i in range(max_iterations):
        # Run one iteration of Baum-Welch
        current_A, current_B, current_pi, current_ll, _ = hmm.baum_welch(
            transition_matrix=current_A,
            emission_matrix=current_B,
            initial_probabilities=current_pi,
            observations=observations,
            n_iterations=1,
            tolerance=0,  # Disable early stopping
        )

        log_likelihoods.append(current_ll)
        print(f"Iteration {i+1}/{max_iterations}: Log-Likelihood = {current_ll:.4f}")

        # Check for convergence
        if i > 0 and abs(log_likelihoods[-1] - log_likelihoods[-2]) < 1e-4:
            print(f"Converged after {i+1} iterations.")
            break

    A_trained, B_trained, pi_trained = current_A, current_B, current_pi
    final_log_likelihood = log_likelihoods[-1]
    iterations = len(log_likelihoods)

    print(f"\nTraining completed in {iterations} iterations")
    print(f"Final log-likelihood: {final_log_likelihood:.4f}")

    # Print trained model parameters
    print_model_params("Trained", A_trained, B_trained, pi_trained)

    # Calculate parameter recovery accuracy
    # Note: Due to label switching, the states may not correspond exactly to the true states
    # This is a simplified metric for demonstration
    A_error = np.mean(np.abs(A_trained - true_A))
    B_error = np.mean(np.abs(B_trained - true_B))
    pi_error = np.mean(np.abs(pi_trained - true_pi))

    print("\nParameter Recovery Mean Absolute Error:")
    print(f"Transition Matrix MAE: {A_error:.4f}")
    print(f"Emission Matrix MAE: {B_error:.4f}")
    print(f"Initial Probabilities MAE: {pi_error:.4f}")

    # Test the model with the Viterbi algorithm on a sample sequence
    test_seq = observations[0]
    log_prob, state_sequence = hmm.viterbi(A_trained, B_trained, pi_trained, test_seq)

    print(f"\nViterbi decoding log probability: {log_prob:.4f}")
    print(f"First 10 decoded states: {state_sequence[:10]}")

    # Plot log-likelihood convergence
    if iterations > 1:
        plot_convergence(log_likelihoods)


if __name__ == "__main__":
    train_hmm_example()
