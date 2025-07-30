"""
Base classes and interfaces for Hidden Markov Models.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
from numpy.typing import NDArray


class BaseHMM(ABC):
    """
    Abstract base class for all Hidden Markov Model implementations.
    """

    def __init__(
        self,
        n_states: int,
        n_observations: Optional[int] = None,
        random_state: Optional[int] = None,
    ) -> None:
        """
        Initialize the HMM with basic parameters.

        Args:
            n_states: Number of hidden states
            n_observations: Number of observable symbols (for discrete HMMs)
            random_state: Random seed for reproducibility
        """
        self.n_states = n_states
        self.n_observations = n_observations
        self.random_state = random_state

        # Initialize parameters to None - subclasses will set these
        self.start_probs: Optional[NDArray[np.float64]] = None
        self.transition_probs: Optional[NDArray[np.float64]] = None
        self.emission_probs: Optional[NDArray[np.float64]] = None

        # Model state
        self._is_fitted = False

        # Set random seed if provided
        if random_state is not None:
            np.random.seed(random_state)

    @property
    def is_fitted(self) -> bool:
        """Check if the model has been fitted."""
        return self._is_fitted

    @abstractmethod
    def fit(
        self,
        sequences: Union[List[NDArray], NDArray],
        n_iter: int = 100,
        tol: float = 1e-6,
        verbose: bool = False,
    ) -> "BaseHMM":
        """
        Fit the HMM to training sequences using Baum-Welch algorithm.

        Args:
            sequences: Training sequences
            n_iter: Maximum number of EM iterations
            tol: Convergence tolerance
            verbose: Whether to print training progress

        Returns:
            self: Fitted model instance
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def predict(self, sequence: NDArray) -> NDArray[np.int32]:
        """
        Find the most likely state sequence using Viterbi algorithm.

        Args:
            sequence: Observation sequence

        Returns:
            Most likely state sequence
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def predict_proba(self, sequence: NDArray) -> NDArray[np.float64]:
        """
        Compute posterior state probabilities using Forward-Backward algorithm.

        Args:
            sequence: Observation sequence

        Returns:
            Posterior probabilities for each state at each time step
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def score(self, sequence: NDArray) -> float:
        """
        Compute log-likelihood of observation sequence.

        Args:
            sequence: Observation sequence

        Returns:
            Log-likelihood of the sequence
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def sample(self, n_samples: int) -> Tuple[NDArray, NDArray]:
        """
        Generate samples from the HMM.

        Args:
            n_samples: Number of samples to generate

        Returns:
            Tuple of (observations, states)
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def _initialize_parameters(self, sequences: Union[List[NDArray], NDArray]) -> None:
        """
        Initialize model parameters before training.

        Args:
            sequences: Training sequences used for initialization
        """
        raise NotImplementedError("Subclasses must implement this method")

    def _validate_fitted(self) -> None:
        """Check if model is fitted and raise error if not."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")

    def _validate_sequence(self, sequence: NDArray) -> None:
        """
        Validate input sequence format and content.

        Args:
            sequence: Input sequence to validate
        """
        if not isinstance(sequence, np.ndarray):
            raise TypeError("Sequence must be a numpy array")

        if sequence.ndim != 1:
            raise ValueError("Sequence must be 1-dimensional")

        if len(sequence) == 0:
            raise ValueError("Sequence cannot be empty")

    def get_params(self) -> Dict[str, Any]:
        """
        Get model parameters as a dictionary.

        Returns:
            Dictionary containing model parameters
        """
        return {
            "start_probs": self.start_probs,
            "transition_probs": self.transition_probs,
            "emission_probs": self.emission_probs,
            "n_states": self.n_states,
            "n_observations": self.n_observations,
            "is_fitted": self.is_fitted,
        }

    def set_params(self, **params: Any) -> "BaseHMM":
        """
        Set model parameters from a dictionary.

        Args:
            **params: Parameters to set

        Returns:
            self: Model instance
        """
        for key, value in params.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Invalid parameter: {key}")
        return self


class AlgorithmMixin:
    """
    Mixin class providing core HMM algorithms.

    This mixin contains implementations of the fundamental HMM algorithms
    that can be shared across different model types.
    """

    @staticmethod
    def forward_algorithm(
        start_probs: NDArray[np.float64],
        transition_probs: NDArray[np.float64],
        emission_probs: NDArray[np.float64],
        sequence: NDArray,
    ) -> Tuple[NDArray[np.float64], float]:
        """
        Forward algorithm implementation.

        Args:
            start_probs: Initial state probabilities
            transition_probs: State transition probabilities
            emission_probs: Emission probabilities for the sequence
            sequence: Observation sequence

        Returns:
            Tuple of (forward probabilities, log-likelihood)
        """
        # Implementation will be in algorithms.py
        raise NotImplementedError("Will be implemented in algorithms.py")

    @staticmethod
    def backward_algorithm(
        transition_probs: NDArray[np.float64], emission_probs: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """
        Backward algorithm implementation.

        Args:
            transition_probs: State transition probabilities
            emission_probs: Emission probabilities for the sequence

        Returns:
            Backward probabilities
        """
        # Implementation will be in algorithms.py
        raise NotImplementedError("Will be implemented in algorithms.py")

    @staticmethod
    def viterbi_algorithm(
        start_probs: NDArray[np.float64],
        transition_probs: NDArray[np.float64],
        emission_probs: NDArray[np.float64],
    ) -> Tuple[NDArray[np.int32], float]:
        """
        Viterbi algorithm implementation.

        Args:
            start_probs: Initial state probabilities
            transition_probs: State transition probabilities
            emission_probs: Emission probabilities for the sequence

        Returns:
            Tuple of (most likely state sequence, log-probability)
        """
        # Implementation will be in algorithms.py
        raise NotImplementedError("Will be implemented in algorithms.py")


class EmissionModel(ABC):
    """
    Abstract base class for emission models.

    This allows for different types of emission distributions
    (discrete, Gaussian, mixture models, etc.)
    """

    @abstractmethod
    def log_probability(self, observations: NDArray, state: int) -> NDArray[np.float64]:
        """
        Compute log probability of observations given state.

        Args:
            observations: Observation sequence
            state: Hidden state

        Returns:
            Log probabilities
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def sample(self, state: int, n_samples: int = 1) -> NDArray:
        """
        Sample observations from the emission distribution.

        Args:
            state: Hidden state
            n_samples: Number of samples

        Returns:
            Sampled observations
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def fit(self, observations: NDArray, posterior_probs: NDArray[np.float64]) -> None:
        """
        Update emission parameters given observations and posterior probabilities.

        Args:
            observations: Training observations
            posterior_probs: Posterior state probabilities
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def log_probability_matrix(self, sequence: NDArray) -> NDArray[np.float64]:
        """
        Compute log emission probabilities for entire sequence.

        Args:
            sequence: Observation sequence

        Returns:
            Log emission probabilities [T, n_states]
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def update_parameters(
        self, sequences: List[NDArray], gammas: List[NDArray[np.float64]]
    ) -> None:
        """
        Update emission parameters using Baum-Welch statistics.

        Args:
            sequences: Training sequences
            gammas: Posterior state probabilities for each sequence
        """
        raise NotImplementedError("Subclasses must implement this method")
