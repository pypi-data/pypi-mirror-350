import numpy as np

from hmm.hidden_markov_model import compute_initial_prob, train

if __name__ == "__main__":

    states = np.array(["F", "B"])
    observations = np.array(["H", "T"])

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

    output = train(2, data, algorithm="baum-welch")

    print("Initial matrix A:")
    print(output["initial_A"])
    print("Initial matrix B:")
    print(output["initial_B"])

    print("The trained matrix A:")
    print(output["A"])
    print("The trained matrix B:")
    print(output["B"])

    print("Initial probability distribution: {}".format(output["start_prob"]))
    print("Diff log: {}".format(output["diff_logs"]))

    print("State sequence: {}".format(output["state_seq_logs"][-1]))
