"""
For saving and loading trained HMM models
"""

import json
import pickle
from pathlib import Path
from typing import Any, Dict, Union

import numpy as np

from ..exceptions import ValidationError


def save_model_pickle(model, filepath: Union[str, Path]) -> None:
    """
    Save HMM model using pickle format.

    Args:
        model: Trained HMM model
        filepath: Path to save the model
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "wb") as f:
        pickle.dump(model, f)


def load_model_pickle(filepath: Union[str, Path]):
    """
    Load HMM model from pickle format.

    Args:
        filepath: Path to the saved model

    Returns:
        Loaded HMM model
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Model file not found: {filepath}")

    with open(filepath, "rb") as f:
        return pickle.load(f)


def save_model_json(model, filepath: Union[str, Path]) -> None:
    """
    Save HMM model parameters in JSON format.

    Args:
        model: Trained HMM model
        filepath: Path to save the model
    """
    if not model.is_fitted:
        raise ValidationError("Cannot save unfitted model")

    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Convert numpy arrays to lists for JSON serialization
    model_data = {
        "model_type": model.__class__.__name__,
        "n_states": model.n_states,
        "n_observations": model.n_observations,
        "start_probs": model.start_probs.tolist(),
        "transition_probs": model.transition_probs.tolist(),
        "emission_probs": model.emission_probs.tolist(),
        "random_state": model.random_state,
        "is_fitted": model.is_fitted,
    }

    # Add training history if available
    if hasattr(model, "log_likelihood_history_"):
        model_data["log_likelihood_history"] = model.log_likelihood_history_

    with open(filepath, "w") as f:
        json.dump(model_data, f, indent=2)


def load_model_json(filepath: Union[str, Path]) -> Dict[str, Any]:
    """
    Load HMM model parameters from JSON format.

    Args:
        filepath: Path to the saved model

    Returns:
        Dictionary containing model parameters
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Model file not found: {filepath}")

    with open(filepath, "r") as f:
        model_data = json.load(f)

    # Convert lists back to numpy arrays
    for key in ["start_probs", "transition_probs", "emission_probs"]:
        if key in model_data:
            model_data[key] = np.array(model_data[key])

    return model_data


def export_model_parameters(model, filepath: Union[str, Path]) -> None:
    """
    Export model parameters to a human-readable text file.

    Args:
        model: Trained HMM model
        filepath: Path to save the parameters
    """
    if not model.is_fitted:
        raise ValidationError("Cannot export unfitted model")

    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w") as f:
        f.write(f"HMM Model Parameters\n")
        f.write(f"{'='*50}\n\n")

        f.write(f"Model Type: {model.__class__.__name__}\n")
        f.write(f"Number of States: {model.n_states}\n")
        f.write(f"Number of Observations: {model.n_observations}\n")
        f.write(f"Random State: {model.random_state}\n\n")

        f.write("Start Probabilities:\n")
        for i, prob in enumerate(model.start_probs):
            f.write(f"  State {i}: {prob:.6f}\n")
        f.write("\n")

        f.write("Transition Probabilities:\n")
        for i in range(model.n_states):
            f.write(f"  From State {i}:\n")
            for j in range(model.n_states):
                f.write(f"    To State {j}: {model.transition_probs[i, j]:.6f}\n")
        f.write("\n")

        f.write("Emission Probabilities:\n")
        for i in range(model.n_states):
            f.write(f"  State {i}:\n")
            for j in range(model.n_observations):
                f.write(f"    Observation {j}: {model.emission_probs[i, j]:.6f}\n")

        if hasattr(model, "log_likelihood_history_"):
            f.write(f"\nTraining History:\n")
            f.write(
                f"  Final Log-Likelihood: {model.log_likelihood_history_[-1]:.6f}\n"
            )
            f.write(f"  Training Iterations: {len(model.log_likelihood_history_)}\n")


def create_model_from_parameters(model_class, parameters: Dict[str, Any]):
    """
    Create HMM model instance from parameter dictionary.

    Args:
        model_class: HMM model class
        parameters: Dictionary containing model parameters

    Returns:
        HMM model instance with loaded parameters
    """
    # Create model instance
    model = model_class(
        n_states=parameters["n_states"],
        n_observations=parameters["n_observations"],
        random_state=parameters.get("random_state"),
    )

    # Set parameters
    model.start_probs = parameters["start_probs"]
    model.transition_probs = parameters["transition_probs"]
    model.emission_probs = parameters["emission_probs"]

    # Set emission model parameters if it exists
    if hasattr(model, "emission_model"):
        model.emission_model.emission_probs = parameters["emission_probs"]

    # Set fitted status
    model._is_fitted = parameters.get("is_fitted", True)

    # Set training history if available
    if "log_likelihood_history" in parameters:
        model.log_likelihood_history_ = parameters["log_likelihood_history"]

    return model


def save_sequences(sequences, filepath: Union[str, Path], format: str = "npz") -> None:
    """
    Save observation sequences to file.

    Args:
        sequences: List of observation sequences
        filepath: Path to save the sequences
        format: File format ('npz', 'txt', 'json')
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    if format == "npz":
        # Save as compressed numpy archive
        np.savez_compressed(filepath, *sequences)
    elif format == "txt":
        # Save as text file
        with open(filepath, "w") as f:
            for i, seq in enumerate(sequences):
                f.write(f"# Sequence {i}\n")
                f.write(" ".join(map(str, seq)) + "\n")
    elif format == "json":
        # Save as JSON
        sequences_list = [
            seq.tolist() if isinstance(seq, np.ndarray) else seq for seq in sequences
        ]
        with open(filepath, "w") as f:
            json.dump(sequences_list, f, indent=2)
    else:
        raise ValueError(f"Unsupported format: {format}")


def load_sequences(filepath: Union[str, Path]):
    """
    Load observation sequences from file.

    Args:
        filepath: Path to the saved sequences

    Returns:
        List of observation sequences
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Sequences file not found: {filepath}")

    if filepath.suffix == ".npz":
        # Load from numpy archive
        data = np.load(filepath)
        return [data[key] for key in sorted(data.keys())]
    elif filepath.suffix == ".txt":
        # Load from text file
        sequences = []
        with open(filepath, "r") as f:
            for line in f:
                if not line.startswith("#") and line.strip():
                    seq = np.array([int(x) for x in line.strip().split()])
                    sequences.append(seq)
        return sequences
    elif filepath.suffix == ".json":
        # Load from JSON
        with open(filepath, "r") as f:
            sequences_list = json.load(f)
        return [np.array(seq) for seq in sequences_list]
    else:
        raise ValueError(f"Unsupported file format: {filepath.suffix}")
