import numpy as np

from hmm.viterbi_algorithm import find_most_likely_path

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

    viterbi_output = find_most_likely_path(x, A, B, initial)
    v_matrix, back_pointer_matrix, probable_seq = viterbi_output

    probable_seq = states[probable_seq]

    print("Observation sequence: {}".format(str(observations[x])))

    print("Viterbi trellis matrix:")
    print(v_matrix.T)

    print("Backpointer matrix:")
    print(back_pointer_matrix.T)

    print("The most probable state sequence: {}".format(str(probable_seq)))
