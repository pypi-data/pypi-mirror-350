"""Load the example datasets."""

from pathlib import Path

import networkx as nx

from tno.quantum.problems.n_minus_1.io import load_gml


def load_small_dataset() -> nx.Graph:
    """Load a small sized dataset with 7 nodes and 8 edges.

    Returns:
        Networkx Graph representation of the dataset.
    """
    dataset_path = Path(__file__).parent / "_data" / "small_dataset.gml.gz"
    return load_gml(dataset_path)


def load_medium_dataset() -> nx.Graph:
    """Load a medium sized dataset with 2380 nodes and 2507 edges.

    Returns:
        Networkx Graph representation of the dataset.
    """
    dataset_path = Path(__file__).parent / "_data" / "medium_dataset.gml.gz"
    return load_gml(dataset_path)


def load_dataset(name: str) -> nx.Graph:
    """Load the small or medium sized dataset.

    Args:
        name: Name of the dataset. Choose from ``"small`` or ``"medium"``.

    Returns:
        Networkx Graph representation of the dataset.
    """
    if name.lower().strip() == "small":
        return load_small_dataset()
    if name.lower().strip() == "medium":
        return load_small_dataset()
    error_msg = "'name' must be 'small' or 'medium'"
    raise ValueError(error_msg)
