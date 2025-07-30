"""
Custom exceptions
"""


class HMMError(Exception):
    """Base exception class for all HMM-related errors."""


class ValidationError(HMMError):
    """Raised when input validation fails."""


class ConvergenceError(HMMError):
    """Raised when training fails to converge."""


class ModelNotFittedError(HMMError):
    """Raised when attempting to use an unfitted model."""


class IncompatibleShapeError(HMMError):
    """Raised when array shapes are incompatible."""


class NumericalInstabilityError(HMMError):
    """Raised when numerical computations become unstable."""
