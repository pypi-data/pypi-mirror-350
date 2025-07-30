#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
#include <nanobind/stl/pair.h>
#include <nanobind/stl/tuple.h>
#include <nanobind/stl/vector.h>

namespace nb = nanobind;

/**
 * Forward algorithm for Hidden Markov Models
 *
 * @param transition_matrix Matrix of transition probabilities (A), shape (n_states, n_states)
 * @param emission_matrix Matrix of emission probabilities (B), shape (n_states, n_symbols)
 * @param initial_probabilities Vector of initial state probabilities (π), shape (n_states)
 * @param observations Vector of observation indices, shape (seq_length)
 * @return Tuple containing:
 *         - Log likelihood of the observation sequence
 *         - Forward variables matrix, shape (seq_length, n_states)
 */
std::pair<double, nb::ndarray<double, nb::numpy>> forward_algorithm(
    nb::ndarray<double, nb::ndim<2>, nb::c_contig> transition_matrix,
    nb::ndarray<double, nb::ndim<2>, nb::c_contig> emission_matrix,
    nb::ndarray<double, nb::ndim<1>, nb::c_contig> initial_probabilities,
    nb::ndarray<int, nb::ndim<1>, nb::c_contig> observations
) {
    // Get dimensions
    size_t n_states = transition_matrix.shape(0);
    size_t seq_length = observations.shape(0);

    // Validate input dimensions
    if (transition_matrix.shape(1) != n_states) {
        throw std::invalid_argument("Transition matrix must be square");
    }
    if (emission_matrix.shape(0) != n_states) {
        throw std::invalid_argument("Emission matrix rows must match number of states");
    }
    if (initial_probabilities.shape(0) != n_states) {
        throw std::invalid_argument("Initial probabilities length must match number of states");
    }

    // Create scaled forward variables matrix - alpha(t,i) = P(O_1, O_2, ..., O_t, q_t = i | λ)
    std::vector<std::vector<double>> forward(seq_length, std::vector<double>(n_states));
    std::vector<double> scaling_factors(seq_length, 0.0);

    // Get views for fast access
    auto trans_view = transition_matrix.view();
    auto emit_view = emission_matrix.view();
    auto init_view = initial_probabilities.view();
    auto obs_view = observations.view();

    // Initialize forward variables for t=0
    for (size_t i = 0; i < n_states; i++) {
        // alpha_0(i) = π_i * b_i(O_0)
        forward[0][i] = init_view(i) * emit_view(i, obs_view(0));
        scaling_factors[0] += forward[0][i];
    }

    // Apply scaling to t=0
    if (scaling_factors[0] > 0) {
        for (size_t i = 0; i < n_states; i++) {
            forward[0][i] /= scaling_factors[0];
        }
    }

    // Induction step
    for (size_t t = 1; t < seq_length; t++) {
        for (size_t j = 0; j < n_states; j++) {
            forward[t][j] = 0.0;

            // alpha_t(j) = [sum_i alpha_{t-1}(i) * a_ij] * b_j(O_t)
            for (size_t i = 0; i < n_states; i++) {
                forward[t][j] += forward[t - 1][i] * trans_view(i, j);
            }
            forward[t][j] *= emit_view(j, obs_view(t));

            // Accumulate scaling factor
            scaling_factors[t] += forward[t][j];
        }

        // Apply scaling
        if (scaling_factors[t] > 0) {
            for (size_t j = 0; j < n_states; j++) {
                forward[t][j] /= scaling_factors[t];
            }
        }
    }

    // Calculate log-likelihood from scaling factors
    double log_likelihood = 0.0;
    for (size_t t = 0; t < seq_length; t++) {
        log_likelihood += std::log(scaling_factors[t]);
    }
    log_likelihood = -log_likelihood; // Due to how we applied scaling

    // Create data for result and copy values
    double *result_data = new double[seq_length * n_states];
    for (size_t t = 0; t < seq_length; t++) {
        for (size_t i = 0; i < n_states; i++) {
            result_data[t * n_states + i] = forward[t][i];
        }
    }

    // Create the capsule with a deleter for the allocated data
    nb::capsule owner(result_data, [](void *p) noexcept { delete[] static_cast<double *>(p); });

    // Create NumPy array that owns the data via the capsule
    nb::ndarray<double, nb::numpy> result(result_data, {seq_length, n_states}, owner);

    return std::make_pair(log_likelihood, result);
}

/**
 * Viterbi algorithm for Hidden Markov Models
 *
 * @param transition_matrix Matrix of transition probabilities (A), shape (n_states, n_states)
 * @param emission_matrix Matrix of emission probabilities (B), shape (n_states, n_symbols)
 * @param initial_probabilities Vector of initial state probabilities (π), shape (n_states)
 * @param observations Vector of observation indices, shape (seq_length)
 * @return Tuple containing:
 *         - Log probability of the most likely path
 *         - Most likely state sequence, shape (seq_length)
 */
std::pair<double, nb::ndarray<int, nb::numpy>> viterbi_algorithm(
    nb::ndarray<double, nb::ndim<2>, nb::c_contig> transition_matrix,
    nb::ndarray<double, nb::ndim<2>, nb::c_contig> emission_matrix,
    nb::ndarray<double, nb::ndim<1>, nb::c_contig> initial_probabilities,
    nb::ndarray<int, nb::ndim<1>, nb::c_contig> observations
) {
    // Get dimensions
    size_t n_states = transition_matrix.shape(0);
    size_t seq_length = observations.shape(0);

    // Validate input dimensions
    if (transition_matrix.shape(1) != n_states) {
        throw std::invalid_argument("Transition matrix must be square");
    }
    if (emission_matrix.shape(0) != n_states) {
        throw std::invalid_argument("Emission matrix rows must match number of states");
    }
    if (initial_probabilities.shape(0) != n_states) {
        throw std::invalid_argument("Initial probabilities length must match number of states");
    }

    // Get views for fast access
    auto trans_view = transition_matrix.view();
    auto emit_view = emission_matrix.view();
    auto init_view = initial_probabilities.view();
    auto obs_view = observations.view();

    // Use log probabilities to avoid numerical underflow
    std::vector<std::vector<double>> log_delta(
        seq_length,
        std::vector<double>(n_states, -std::numeric_limits<double>::infinity())
    );
    std::vector<std::vector<size_t>> psi(seq_length, std::vector<size_t>(n_states, 0));

    // Initialize Viterbi variables for t=0
    for (size_t i = 0; i < n_states; i++) {
        // Handle zero probabilities in log space
        if (init_view(i) > 0 && emit_view(i, obs_view(0)) > 0) {
            log_delta[0][i] = std::log(init_view(i)) + std::log(emit_view(i, obs_view(0)));
        }
        psi[0][i] = 0; // No predecessor for the first time step
    }

    // Recursion step
    for (size_t t = 1; t < seq_length; t++) {
        for (size_t j = 0; j < n_states; j++) {
            // Find most likely previous state
            double max_val = -std::numeric_limits<double>::infinity();
            size_t max_idx = 0;

            for (size_t i = 0; i < n_states; i++) {
                if (log_delta[t - 1][i] > -std::numeric_limits<double>::infinity() && trans_view(i, j) > 0) {
                    double val = log_delta[t - 1][i] + std::log(trans_view(i, j));
                    if (val > max_val) {
                        max_val = val;
                        max_idx = i;
                    }
                }
            }

            // Update Viterbi variables if we found a valid path
            if (max_val > -std::numeric_limits<double>::infinity() && emit_view(j, obs_view(t)) > 0) {
                log_delta[t][j] = max_val + std::log(emit_view(j, obs_view(t)));
                psi[t][j] = max_idx;
            }
        }
    }

    // Termination: find the most likely end state
    double max_final_val = -std::numeric_limits<double>::infinity();
    size_t max_final_idx = 0;

    for (size_t i = 0; i < n_states; i++) {
        if (log_delta[seq_length - 1][i] > max_final_val) {
            max_final_val = log_delta[seq_length - 1][i];
            max_final_idx = i;
        }
    }

    // If no valid path was found, throw an exception
    if (max_final_val == -std::numeric_limits<double>::infinity()) {
        throw std::runtime_error("No valid state sequence found for the given observations");
    }

    // Backtracking: find the most likely state sequence
    std::vector<int> state_sequence(seq_length);
    state_sequence[seq_length - 1] = static_cast<int>(max_final_idx);

    for (int t = seq_length - 2; t >= 0; t--) {
        state_sequence[t] = static_cast<int>(psi[t + 1][state_sequence[t + 1]]);
    }

    // Create result array for the state sequence
    int *result_data = new int[seq_length];
    for (size_t t = 0; t < seq_length; t++) {
        result_data[t] = state_sequence[t];
    }

    // Create the capsule with a deleter for the allocated data
    nb::capsule owner(result_data, [](void *p) noexcept { delete[] static_cast<int *>(p); });

    // Create NumPy array that owns the data via the capsule
    nb::ndarray<int, nb::numpy> result(result_data, {seq_length}, owner);

    return std::make_pair(max_final_val, result);
}

/**
 * Backward algorithm for Hidden Markov Models - helper for Baum-Welch
 *
 * @param transition_matrix Matrix of transition probabilities (A), shape (n_states, n_states)
 * @param emission_matrix Matrix of emission probabilities (B), shape (n_states, n_symbols)
 * @param observations Vector of observation indices, shape (seq_length)
 * @param scaling_factors Scaling factors from forward algorithm, shape (seq_length)
 * @return Backward variables matrix, shape (seq_length, n_states)
 */
nb::ndarray<double, nb::numpy> backward_algorithm(
    nb::ndarray<double, nb::ndim<2>, nb::c_contig> transition_matrix,
    nb::ndarray<double, nb::ndim<2>, nb::c_contig> emission_matrix,
    nb::ndarray<int, nb::ndim<1>, nb::c_contig> observations,
    const std::vector<double> &scaling_factors
) {
    // Get dimensions
    size_t n_states = transition_matrix.shape(0);
    size_t seq_length = observations.shape(0);

    // Create scaled backward variables matrix - beta(t,i) = P(O_{t+1}, O_{t+2}, ..., O_T | q_t = i, λ)
    std::vector<std::vector<double>> backward(seq_length, std::vector<double>(n_states));

    // Get views for fast access
    auto trans_view = transition_matrix.view();
    auto emit_view = emission_matrix.view();
    auto obs_view = observations.view();

    // Initialize backward variables for t=T-1 (last time step)
    for (size_t i = 0; i < n_states; i++) {
        backward[seq_length - 1][i] = 1.0;
        // Scale using the same factor as the forward algorithm at this time step
        backward[seq_length - 1][i] /= scaling_factors[seq_length - 1];
    }

    // Recursion step - backward in time
    for (int t = seq_length - 2; t >= 0; t--) {
        for (size_t i = 0; i < n_states; i++) {
            backward[t][i] = 0.0;

            // beta_t(i) = sum_j [a_ij * b_j(O_{t+1}) * beta_{t+1}(j)]
            for (size_t j = 0; j < n_states; j++) {
                backward[t][i] += trans_view(i, j) * emit_view(j, obs_view(t + 1)) * backward[t + 1][j];
            }

            // Apply the same scaling as used in forward algorithm
            backward[t][i] /= scaling_factors[t];
        }
    }

    // Create result array
    double *result_data = new double[seq_length * n_states];
    for (size_t t = 0; t < seq_length; t++) {
        for (size_t i = 0; i < n_states; i++) {
            result_data[t * n_states + i] = backward[t][i];
        }
    }

    // Create the capsule with a deleter
    nb::capsule owner(result_data, [](void *p) noexcept { delete[] static_cast<double *>(p); });

    // Create NumPy array that owns the data via the capsule
    return nb::ndarray<double, nb::numpy>(result_data, {seq_length, n_states}, owner);
}

/**
 * Baum-Welch algorithm for training Hidden Markov Models
 *
 * @param transition_matrix Initial transition probabilities (A), shape (n_states, n_states)
 * @param emission_matrix Initial emission probabilities (B), shape (n_states, n_symbols)
 * @param initial_probabilities Initial state probabilities (π), shape (n_states)
 * @param observations Training observation sequences, shape (n_sequences, seq_length)
 * @param n_iterations Maximum number of iterations for training
 * @param tolerance Convergence threshold for log likelihood improvement
 * @return Tuple containing:
 *         - Updated transition matrix
 *         - Updated emission matrix
 *         - Updated initial probabilities
 *         - Final log likelihood
 *         - Number of iterations performed
 */
std::tuple<nb::ndarray<double, nb::numpy>, nb::ndarray<double, nb::numpy>, nb::ndarray<double, nb::numpy>, double, int>
baum_welch_algorithm(
    nb::ndarray<double, nb::ndim<2>, nb::c_contig> transition_matrix,
    nb::ndarray<double, nb::ndim<2>, nb::c_contig> emission_matrix,
    nb::ndarray<double, nb::ndim<1>, nb::c_contig> initial_probabilities,
    nb::ndarray<int, nb::ndim<2>, nb::c_contig> observations,
    int n_iterations = 100,
    double tolerance = 1e-6
) {
    // Get dimensions
    size_t n_states = transition_matrix.shape(0);
    size_t n_symbols = emission_matrix.shape(1);
    size_t n_sequences = observations.shape(0);
    size_t seq_length = observations.shape(1);

    // Validate input dimensions
    if (transition_matrix.shape(1) != n_states) {
        throw std::invalid_argument("Transition matrix must be square");
    }
    if (emission_matrix.shape(0) != n_states) {
        throw std::invalid_argument("Emission matrix rows must match number of states");
    }
    if (initial_probabilities.shape(0) != n_states) {
        throw std::invalid_argument("Initial probabilities length must match number of states");
    }

    // Create working copies of the model parameters
    std::vector<std::vector<double>> A(n_states, std::vector<double>(n_states));
    std::vector<std::vector<double>> B(n_states, std::vector<double>(n_symbols));
    std::vector<double> pi(n_states);

    // Extract initial parameters
    for (size_t i = 0; i < n_states; i++) {
        pi[i] = initial_probabilities(i);
        for (size_t j = 0; j < n_states; j++) {
            A[i][j] = transition_matrix(i, j);
        }
        for (size_t k = 0; k < n_symbols; k++) {
            B[i][k] = emission_matrix(i, k);
        }
    }

    // Training loop
    double prev_log_likelihood = -std::numeric_limits<double>::infinity();
    double log_likelihood = 0.0;
    int iter;

    for (iter = 0; iter < n_iterations; iter++) {
        // Reset accumulators for model parameter updates
        std::vector<double> pi_num(n_states, 0.0);
        std::vector<std::vector<double>> A_num(n_states, std::vector<double>(n_states, 0.0));
        std::vector<std::vector<double>> B_num(n_states, std::vector<double>(n_symbols, 0.0));

        std::vector<double> gamma_sum(n_states, 0.0);

        log_likelihood = 0.0;

        // Process each observation sequence
        for (size_t seq = 0; seq < n_sequences; seq++) {
            // Create observation sequence vector for this sequence
            std::vector<int> seq_observations(seq_length);
            for (size_t t = 0; t < seq_length; t++) {
                seq_observations[t] = observations(seq, t);
            }

            // Create temporary arrays with correct types for algorithm calls
            // For transition matrix
            double *A_data = new double[n_states * n_states];
            for (size_t i = 0; i < n_states; i++) {
                for (size_t j = 0; j < n_states; j++) {
                    A_data[i * n_states + j] = A[i][j];
                }
            }
            nb::capsule A_capsule(A_data, [](void *p) noexcept { delete[] static_cast<double *>(p); });
            nb::ndarray<double, nb::ndim<2>, nb::c_contig> A_temp(A_data, {n_states, n_states}, A_capsule);

            // For emission matrix
            double *B_data = new double[n_states * n_symbols];
            for (size_t i = 0; i < n_states; i++) {
                for (size_t k = 0; k < n_symbols; k++) {
                    B_data[i * n_symbols + k] = B[i][k];
                }
            }
            nb::capsule B_capsule(B_data, [](void *p) noexcept { delete[] static_cast<double *>(p); });
            nb::ndarray<double, nb::ndim<2>, nb::c_contig> B_temp(B_data, {n_states, n_symbols}, B_capsule);

            // For initial probabilities
            double *pi_data = new double[n_states];
            for (size_t i = 0; i < n_states; i++) {
                pi_data[i] = pi[i];
            }
            nb::capsule pi_capsule(pi_data, [](void *p) noexcept { delete[] static_cast<double *>(p); });
            nb::ndarray<double, nb::ndim<1>, nb::c_contig> pi_temp(pi_data, {n_states}, pi_capsule);

            // For observations
            int *obs_data = new int[seq_length];
            for (size_t t = 0; t < seq_length; t++) {
                obs_data[t] = seq_observations[t];
            }
            nb::capsule obs_capsule(obs_data, [](void *p) noexcept { delete[] static_cast<int *>(p); });
            nb::ndarray<int, nb::ndim<1>, nb::c_contig> obs_temp(obs_data, {seq_length}, obs_capsule);

            // Forward pass - with proper types
            std::pair<double, nb::ndarray<double, nb::numpy>> forward_result =
                forward_algorithm(A_temp, B_temp, pi_temp, obs_temp);

            double seq_log_likelihood = forward_result.first;
            nb::ndarray<double, nb::numpy> alpha = forward_result.second;

            // Extract scaling factors (in the forward algorithm they're applied to alpha)
            std::vector<double> scaling_factors(seq_length, 1.0);

            // Backward pass
            nb::ndarray<double, nb::numpy> beta = backward_algorithm(A_temp, B_temp, obs_temp, scaling_factors);

            // Compute xi and gamma for parameter updates
            std::vector<std::vector<std::vector<double>>> xi(
                seq_length - 1,
                std::vector<std::vector<double>>(n_states, std::vector<double>(n_states, 0.0))
            );
            std::vector<std::vector<double>> gamma(seq_length, std::vector<double>(n_states, 0.0));

            // Compute gamma values
            for (size_t t = 0; t < seq_length; t++) {
                double sum = 0.0;
                for (size_t i = 0; i < n_states; i++) {
                    // Convert to 2D index for accessing alpha and beta arrays
                    size_t idx = t * n_states + i;
                    double *alpha_data = static_cast<double *>(alpha.data());
                    double *beta_data = static_cast<double *>(beta.data());

                    gamma[t][i] = alpha_data[idx] * beta_data[idx];
                    sum += gamma[t][i];
                }

                // Normalize gamma values
                if (sum > 0) {
                    for (size_t i = 0; i < n_states; i++) {
                        gamma[t][i] /= sum;
                    }
                }
            }

            // Compute xi values
            for (size_t t = 0; t < seq_length - 1; t++) {
                double sum = 0.0;

                // Calculate xi values
                for (size_t i = 0; i < n_states; i++) {
                    for (size_t j = 0; j < n_states; j++) {
                        double *alpha_data = static_cast<double *>(alpha.data());
                        double *beta_data = static_cast<double *>(beta.data());

                        double alpha_ti = alpha_data[t * n_states + i];
                        double beta_tj1 = beta_data[(t + 1) * n_states + j];

                        xi[t][i][j] = alpha_ti * A[i][j] * B[j][seq_observations[t + 1]] * beta_tj1;
                        sum += xi[t][i][j];
                    }
                }

                // Normalize xi values
                if (sum > 0) {
                    for (size_t i = 0; i < n_states; i++) {
                        for (size_t j = 0; j < n_states; j++) {
                            xi[t][i][j] /= sum;
                        }
                    }
                }
            }

            // Accumulate statistics for model updates
            for (size_t i = 0; i < n_states; i++) {
                // Update initial probabilities
                pi_num[i] += gamma[0][i];

                // Accumulate gamma values for each state (except last time step)
                for (size_t t = 0; t < seq_length - 1; t++) {
                    gamma_sum[i] += gamma[t][i];

                    // Update transition probabilities numerator
                    for (size_t j = 0; j < n_states; j++) {
                        A_num[i][j] += xi[t][i][j];
                    }
                }

                // Update emission probabilities numerator
                for (size_t t = 0; t < seq_length; t++) {
                    B_num[i][seq_observations[t]] += gamma[t][i];
                }
            }

            // Accumulate log likelihood
            log_likelihood += seq_log_likelihood;
        }

        // Update model parameters
        // Initial probabilities
        double pi_sum = 0.0;
        for (size_t i = 0; i < n_states; i++) {
            pi_sum += pi_num[i];
        }
        if (pi_sum > 0) {
            for (size_t i = 0; i < n_states; i++) {
                pi[i] = pi_num[i] / pi_sum;
            }
        }

        // Transition probabilities
        for (size_t i = 0; i < n_states; i++) {
            if (gamma_sum[i] > 0) {
                for (size_t j = 0; j < n_states; j++) {
                    A[i][j] = A_num[i][j] / gamma_sum[i];
                }
            }
        }

        // Emission probabilities
        for (size_t i = 0; i < n_states; i++) {
            double state_total = 0.0;
            for (size_t k = 0; k < n_symbols; k++) {
                state_total += B_num[i][k];
            }

            if (state_total > 0) {
                for (size_t k = 0; k < n_symbols; k++) {
                    B[i][k] = B_num[i][k] / state_total;
                }
            }
        }

        // Check for convergence
        double improvement = log_likelihood - prev_log_likelihood;
        if (iter > 0 && std::abs(improvement) < tolerance) {
            break;
        }

        prev_log_likelihood = log_likelihood;
    }

    // Create result arrays
    double *A_data = new double[n_states * n_states];
    double *B_data = new double[n_states * n_symbols];
    double *pi_data = new double[n_states];

    for (size_t i = 0; i < n_states; i++) {
        pi_data[i] = pi[i];
        for (size_t j = 0; j < n_states; j++) {
            A_data[i * n_states + j] = A[i][j];
        }
        for (size_t k = 0; k < n_symbols; k++) {
            B_data[i * n_symbols + k] = B[i][k];
        }
    }

    // Create capsules with deleters
    nb::capsule A_owner(A_data, [](void *p) noexcept { delete[] static_cast<double *>(p); });
    nb::capsule B_owner(B_data, [](void *p) noexcept { delete[] static_cast<double *>(p); });
    nb::capsule pi_owner(pi_data, [](void *p) noexcept { delete[] static_cast<double *>(p); });

    // Create NumPy arrays
    nb::ndarray<double, nb::numpy> A_result(A_data, {n_states, n_states}, A_owner);
    nb::ndarray<double, nb::numpy> B_result(B_data, {n_states, n_symbols}, B_owner);
    nb::ndarray<double, nb::numpy> pi_result(pi_data, {n_states}, pi_owner);

    // Return the updated model parameters and training information
    return std::make_tuple(A_result, B_result, pi_result, log_likelihood, iter + 1);
}

// Python bindings
NB_MODULE(cpp_markov_algorithms, m) {
    m.doc() = "HMM Implementation";

    m.def(
        "forward",
        &forward_algorithm,
        "Forward algorithm for HMMs",
        nb::arg("transition_matrix"),
        nb::arg("emission_matrix"),
        nb::arg("initial_probabilities"),
        nb::arg("observations")
    );

    m.def(
        "viterbi",
        &viterbi_algorithm,
        "Viterbi algorithm for HMMs",
        nb::arg("transition_matrix"),
        nb::arg("emission_matrix"),
        nb::arg("initial_probabilities"),
        nb::arg("observations")
    );

    m.def(
        "baum_welch",
        &baum_welch_algorithm,
        "Baum-Welch algorithm for training HMMs",
        nb::arg("transition_matrix"),
        nb::arg("emission_matrix"),
        nb::arg("initial_probabilities"),
        nb::arg("observations"),
        nb::arg("n_iterations") = 100,
        nb::arg("tolerance") = 1e-6
    );
}
