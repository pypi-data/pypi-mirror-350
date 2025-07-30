import numpy as np

from hmm.hidden_markov_model import train

if __name__ == "__main__":
    states = np.array(["F", "B"])
    observations = np.array(["H", "T"])

    # Same data as in your example
    data = np.array(
        [
            [0, 0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1, 0],
            [1, 0, 0, 1, 1, 0],
            [1, 0, 1, 1, 1, 0],
            [1, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 1],
            [0, 0, 1, 1, 0, 1],
            [0, 1, 1, 1, 0, 0],
        ],
        dtype=int,
    )

    # Try both algorithms and compare
    viterbi_output = train(2, data, algorithm="viterbi")
    baum_welch_output = train(2, data, algorithm="baum-welch")

    print("=== Viterbi Training Results ===")
    print("Trained A matrix:")
    print(viterbi_output["A"])
    print("Trained B matrix:")
    print(viterbi_output["B"])
    print("Initial probability distribution:")
    print(viterbi_output["start_prob"])
    print("Iterations required:", viterbi_output["iterations"])
    print("Final state sequences from Viterbi:")
    print(viterbi_output["state_seq_logs"][-1][0])  # Just showing the first sequence

    print("\n=== Baum-Welch Training Results ===")
    print("Trained A matrix:")
    print(baum_welch_output["A"])
    print("Trained B matrix:")
    print(baum_welch_output["B"])
    print("Initial probability distribution:")
    print(baum_welch_output["start_prob"])
    print("Iterations required:", baum_welch_output["iterations"])
    print("Final state sequences from Viterbi decoding:")
    print(baum_welch_output["state_seq_logs"][-1][0])  # Just showing the first sequence

    # Also run several times with different initializations
    print("\n=== Multiple Random Initializations with Baum-Welch ===")
    best_likelihood = -np.inf
    best_output = None

    from hmm.forward_algorithm import compute_forward_prob

    for run in range(5):
        output = train(2, data, algorithm="baum-welch")

        # Compute likelihood of all sequences
        total_likelihood = 0
        for sequence in data:
            _, seq_likelihood = compute_forward_prob(
                sequence, output["A"], output["B"], output["start_prob"]
            )
            total_likelihood += np.log(seq_likelihood + 1e-10)  # Log likelihood

        print(f"Run {run+1} likelihood: {total_likelihood:.6f}")

        if total_likelihood > best_likelihood:
            best_likelihood = total_likelihood
            best_output = output

    print("\nBest model parameters:")
    print("A:", best_output["A"])
    print("B:", best_output["B"])
    print("start_prob:", best_output["start_prob"])
