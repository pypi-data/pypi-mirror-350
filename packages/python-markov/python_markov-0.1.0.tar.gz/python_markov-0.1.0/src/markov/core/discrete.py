"""
Implementation of HMMs with discrete observations
"""

from typing import List, Optional, Tuple, Union

import numpy as np
from numpy.typing import NDArray

from ..exceptions import ModelNotFittedError
from ..utils.math_utils import (
    EPSILON,
    make_stochastic,
    random_stochastic_matrix,
    safe_log,
)
from ..utils.validation import (
    validate_n_observations,
    validate_n_states,
    validate_sample_parameters,
    validate_sequences,
    validate_training_parameters,
)
from .algorithms import (
    fit_hmm_baum_welch,
    forward_algorithm,
    forward_backward_algorithm,
    sample_hmm,
    viterbi_algorithm,
)
from .base import BaseHMM, EmissionModel


class DiscreteEmissionModel(EmissionModel):
    """
    Discrete emission model for HMMs with categorical observations.

    This model assumes each state emits discrete symbols according to
    a categorical distribution.
    """

    def __init__(self, n_states: int, n_observations: int):
        """
        Initialize discrete emission model.

        Args:
            n_states: Number of hidden states
            n_observations: Number of observable symbols
        """
        self.n_states = n_states
        self.n_observations = n_observations
        self.emission_probs: Optional[NDArray[np.float64]] = None

    def initialize_parameters(self, random_state: Optional[int] = None) -> None:
        """Initialize emission parameters randomly."""
        self.emission_probs = random_stochastic_matrix(
            self.n_states, self.n_observations, random_state
        )

    def log_probability(self, observations: NDArray, state: int) -> NDArray[np.float64]:
        """
        Compute log probability of observations given state.

        Args:
            observations: Observation sequence
            state: Hidden state

        Returns:
            Log probabilities for each observation
        """
        if self.emission_probs is None:
            raise ValueError("Model parameters not initialized")

        return safe_log(self.emission_probs[state, observations])

    def log_probability_matrix(self, sequence: NDArray) -> NDArray[np.float64]:
        """
        Compute log emission probabilities for entire sequence.

        Args:
            sequence: Observation sequence

        Returns:
            Log emission probabilities [T, n_states]
        """
        if self.emission_probs is None:
            raise ValueError("Model parameters not initialized")

        T = len(sequence)
        log_emission_probs = np.zeros((T, self.n_states))

        for t in range(T):
            for state in range(self.n_states):
                log_emission_probs[t, state] = safe_log(
                    self.emission_probs[state, sequence[t]]
                )

        return log_emission_probs

    def sample(self, state: int, n_samples: int = 1) -> NDArray:
        """
        Sample observations from the emission distribution.

        Args:
            state: Hidden state
            n_samples: Number of samples

        Returns:
            Sampled observations
        """
        if self.emission_probs is None:
            raise ValueError("Model parameters not initialized")

        samples = np.random.choice(
            self.n_observations, size=n_samples, p=self.emission_probs[state]
        )

        if n_samples == 1:
            return samples[0]  # Return scalar for single sample
        return samples

    def fit(self, observations: NDArray, posterior_probs: NDArray[np.float64]) -> None:
        """
        Update emission parameters given observations and posterior probabilities.

        Args:
            observations: Training observations
            posterior_probs: Posterior state probabilities [T, n_states]
        """
        T = len(observations)

        # Initialize emission counts
        emission_counts = np.zeros((self.n_states, self.n_observations))

        # Accumulate weighted counts
        for t in range(T):
            obs = observations[t]
            emission_counts[:, obs] += posterior_probs[t]

        # Normalize to get probabilities
        row_sums = np.sum(emission_counts, axis=1, keepdims=True)
        row_sums = np.maximum(row_sums, EPSILON)
        self.emission_probs = emission_counts / row_sums

    def update_parameters(
        self, sequences: List[NDArray], gammas: List[NDArray[np.float64]]
    ) -> None:
        """
        Update emission parameters using Baum-Welch statistics.

        Args:
            sequences: Training sequences
            gammas: Posterior state probabilities for each sequence
        """
        # Initialize emission counts
        emission_counts = np.zeros((self.n_states, self.n_observations))

        # Accumulate counts across all sequences
        for seq, gamma in zip(sequences, gammas):
            T = len(seq)
            for t in range(T):
                obs = seq[t]
                emission_counts[:, obs] += gamma[t]

        # Normalize to get probabilities
        row_sums = np.sum(emission_counts, axis=1, keepdims=True)
        row_sums = np.maximum(row_sums, EPSILON)
        self.emission_probs = emission_counts / row_sums


class DiscreteHMM(BaseHMM):
    """
    Hidden Markov Model with discrete observations.

    This class implements a complete discrete HMM with categorical emission
    distributions. It supports training via Baum-Welch algorithm and various
    inference tasks.

    Examples:
        >>> # Create and train a 3-state, 4-observation HMM
        >>> hmm = DiscreteHMM(n_states=3, n_observations=4)
        >>> sequences = [[0, 1, 2, 1], [2, 0, 1, 0]]
        >>> hmm.fit(sequences)
        >>>
        >>> # Make predictions
        >>> test_seq = np.array([0, 1, 2])
        >>> states = hmm.predict(test_seq)
        >>> log_prob = hmm.score(test_seq)
    """

    def __init__(
        self, n_states: int, n_observations: int, random_state: Optional[int] = None
    ):
        """
        Initialize discrete HMM.

        Args:
            n_states: Number of hidden states
            n_observations: Number of observable symbols
            random_state: Random seed for reproducibility
        """
        # Validate parameters
        validate_n_states(n_states)
        validate_n_observations(n_observations)

        super().__init__(n_states, n_observations, random_state)

        # Initialize emission model
        self.emission_model = DiscreteEmissionModel(n_states, n_observations)

        # Training history
        self.log_likelihood_history_: List[float] = []

    def _initialize_parameters(self, sequences: Union[List[NDArray], NDArray]) -> None:
        """
        Initialize model parameters before training.

        Args:
            sequences: Training sequences used for initialization
        """
        # Set random seed if provided for consistent initialization
        if self.random_state is not None:
            np.random.seed(self.random_state)

        # Initialize start probabilities (uniform + noise)
        self.start_probs = np.ones(self.n_states) / self.n_states
        self.start_probs += np.random.random(self.n_states) * 0.1
        self.start_probs = make_stochastic(self.start_probs.reshape(1, -1), axis=1)[0]

        # Initialize transition probabilities (random stochastic)
        self.transition_probs = random_stochastic_matrix(
            self.n_states, self.n_states, self.random_state
        )

        # Initialize emission parameters
        self.emission_model.initialize_parameters(self.random_state)
        self.emission_probs = self.emission_model.emission_probs

    def fit(
        self,
        sequences: Union[List[NDArray], NDArray],
        n_iter: int = 100,
        tol: float = 1e-6,
        verbose: bool = False,
    ) -> "DiscreteHMM":
        """
        Fit the HMM to training sequences using Baum-Welch algorithm.

        Args:
            sequences: Training sequences (list of arrays or 2D array)
            n_iter: Maximum number of EM iterations
            tol: Convergence tolerance
            verbose: Whether to print training progress

        Returns:
            self: Fitted model instance
        """
        # Validate inputs
        validate_training_parameters(n_iter, tol, verbose)
        sequences = validate_sequences(sequences, self.n_observations)

        # Initialize parameters
        self._initialize_parameters(sequences)

        # Run Baum-Welch training
        (self.start_probs, self.transition_probs, self.log_likelihood_history_) = (
            fit_hmm_baum_welch(
                sequences=sequences,
                initial_start_probs=self.start_probs,
                initial_transition_probs=self.transition_probs,
                emission_model=self.emission_model,
                n_iter=n_iter,
                tol=tol,
                verbose=verbose,
            )
        )

        # Update emission probabilities reference
        self.emission_probs = self.emission_model.emission_probs

        # Mark as fitted
        self._is_fitted = True

        return self

    def predict(self, sequence: NDArray) -> NDArray[np.int32]:
        """
        Find the most likely state sequence using Viterbi algorithm.

        Args:
            sequence: Observation sequence

        Returns:
            Most likely state sequence
        """
        self._validate_fitted()
        self._validate_sequence(sequence)

        # Get log emission probabilities
        log_emission_probs = self.emission_model.log_probability_matrix(sequence)

        # Run Viterbi algorithm
        states, _ = viterbi_algorithm(
            safe_log(self.start_probs),
            safe_log(self.transition_probs),
            log_emission_probs,
        )

        return states

    def predict_proba(self, sequence: NDArray) -> NDArray[np.float64]:
        """
        Compute posterior state probabilities using Forward-Backward algorithm.

        Args:
            sequence: Observation sequence

        Returns:
            Posterior probabilities for each state at each time step [T, n_states]
        """
        self._validate_fitted()
        self._validate_sequence(sequence)

        # Get log emission probabilities
        log_emission_probs = self.emission_model.log_probability_matrix(sequence)

        # Run Forward-Backward algorithm
        gamma, _, _ = forward_backward_algorithm(
            safe_log(self.start_probs),
            safe_log(self.transition_probs),
            log_emission_probs,
        )

        return gamma

    def score(self, sequence: NDArray) -> float:
        """
        Compute log-likelihood of observation sequence.

        Args:
            sequence: Observation sequence

        Returns:
            Log-likelihood of the sequence
        """
        self._validate_fitted()
        self._validate_sequence(sequence)

        # Get log emission probabilities
        log_emission_probs = self.emission_model.log_probability_matrix(sequence)

        # Run forward algorithm
        _, log_likelihood = forward_algorithm(
            safe_log(self.start_probs),
            safe_log(self.transition_probs),
            log_emission_probs,
        )

        return log_likelihood

    def sample(self, n_samples: int) -> Tuple[NDArray, NDArray]:
        """
        Generate samples from the HMM.

        Args:
            n_samples: Number of samples to generate

        Returns:
            Tuple of (observations, states)
        """
        self._validate_fitted()
        validate_sample_parameters(n_samples)

        observations, states = sample_hmm(
            self.start_probs,
            self.transition_probs,
            self.emission_model,
            n_samples,
            self.random_state,
        )

        return observations, states

    def _validate_fitted(self) -> None:
        """Check if model is fitted and raise error if not."""
        if not self.is_fitted:
            raise ModelNotFittedError("Model must be fitted before making predictions")

    def _validate_sequence(self, sequence: NDArray) -> None:
        """
        Validate input sequence format and content.

        Args:
            sequence: Input sequence to validate
        """
        # Use validation utility instead of base class method
        from ..utils.validation import validate_sequence

        validate_sequence(sequence, self.n_observations)

    def get_params(self) -> dict:
        """
        Get model parameters as a dictionary.

        Returns:
            Dictionary containing model parameters
        """
        params = super().get_params()
        params.update(
            {
                "log_likelihood_history": self.log_likelihood_history_,
                "n_observations": self.n_observations,
            }
        )
        return params

    def fit_transform(
        self, sequences: Union[List[NDArray], NDArray], **fit_params
    ) -> List[NDArray[np.float64]]:
        """
        Fit model and return posterior probabilities for all sequences.

        Args:
            sequences: Training sequences
            **fit_params: Parameters passed to fit()

        Returns:
            List of posterior probability arrays for each sequence
        """
        self.fit(sequences, **fit_params)

        # Validate and convert sequences
        sequences = validate_sequences(sequences, self.n_observations)

        # Get posterior probabilities for all sequences
        posterior_probs = [self.predict_proba(seq) for seq in sequences]

        return posterior_probs

    def __repr__(self) -> str:
        """String representation of the model."""
        return (
            f"DiscreteHMM(n_states={self.n_states}, "
            f"n_observations={self.n_observations}, "
            f"fitted={self.is_fitted})"
        )
