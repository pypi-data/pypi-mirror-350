import numpy as np

from hmm.forward_algorithm import compute_forward_prob

if __name__ == "__main__":

    # Distinct states of Markov process
    states = np.array(["TV", "Pub", "Party", "Study"])
    # Set of possible observations
    observations = np.array(["Tired", "Hungover", "Scared", "Fine"])

    # State Transition Matrix A has size (n_states, n_states)
    #
    # A = {a_ij} with i, j belong to {0, 1, ..., n_states-1}
    #
    # a_ij is the probability of state j given by previous state i,
    # that is P(states[j] | states[i])
    A = np.array(
        [
            [0.4, 0.3, 0.1, 0.2],
            [0.6, 0.05, 0.1, 0.25],
            [0.7, 0.05, 0.05, 0.2],
            [0.3, 0.4, 0.25, 0.05],
        ]
    )

    # Emission Matrix B has size (n_states, n_observations)
    #
    # B = {b_ij} with:
    #   i belongs to {0, 1, ..., n_states-1}
    #   j belongs to {0, 1, ..., n_observations-1}
    #
    # b_ij is the probability of observations j given by current state i,
    # that is P(observations[j] | states[i])
    B = np.array(
        [
            [0.2, 0.1, 0.2, 0.5],
            [0.4, 0.2, 0.1, 0.3],
            [0.3, 0.4, 0.2, 0.1],
            [0.3, 0.05, 0.3, 0.35],
        ]
    )

    # The sequence of observations {Tired, Tired, Scared}
    x = [0, 0, 2]

    # Initial probabilities
    initial = [0.05, 0.1, 0.075, 0.075]

    alpha_matrix, sequence_prob = compute_forward_prob(x, A, B, initial)

    print("Observation sequence: {}".format(str(observations[x])))

    print("Alpha matrix:")
    print(alpha_matrix.T)
    print("The probability of the observation sequence: {}".format(sequence_prob))
