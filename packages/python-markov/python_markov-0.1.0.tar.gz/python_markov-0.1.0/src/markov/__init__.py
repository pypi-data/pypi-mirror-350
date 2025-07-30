"""
python-markov

This library provides implementations of Hidden Markov Models with support for
discrete and continuous observations, along with all fundamental algorithms
including Forward, Backward, Viterbi, and Baum-Welch.

Basic Usage:
    >>> from markov import DiscreteHMM
    >>> import numpy as np
    >>>
    >>> # Create and train a model
    >>> hmm = DiscreteHMM(n_states=3, n_observations=4)
    >>> sequences = [np.array([0, 1, 2, 1]), np.array([2, 0, 1, 0])]
    >>> hmm.fit(sequences)
    >>>
    >>> # Make predictions
    >>> test_seq = np.array([0, 1, 2])
    >>> states = hmm.predict(test_seq)
    >>> log_likelihood = hmm.score(test_seq)
"""

from .core.base import BaseHMM, EmissionModel

# Core model classes
from .core.discrete import DiscreteHMM

# Custom exceptions
from .exceptions import (
    ConvergenceError,
    HMMError,
    IncompatibleShapeError,
    ModelNotFittedError,
    NumericalInstabilityError,
    ValidationError,
)

# Utility functions
from .utils.metrics import (
    compute_aic,
    compute_bic,
    compute_perplexity,
    log_likelihood_ratio_test,
)

__version__ = "0.1.0"
__author__ = "Tuan Pham"
__email__ = "me@tuanph.am"

# Public API
__all__ = [
    # Core models
    "DiscreteHMM",
    "BaseHMM",
    "EmissionModel",
    # Metrics
    "compute_aic",
    "compute_bic",
    "compute_perplexity",
    "log_likelihood_ratio_test",
    # Exceptions
    "HMMError",
    "ValidationError",
    "ConvergenceError",
    "ModelNotFittedError",
    "IncompatibleShapeError",
    "NumericalInstabilityError",
    # Version info
    "__version__",
]
