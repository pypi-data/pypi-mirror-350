"""Input and output functions for the n-1 problem.

This module contains functions to load and save graphs in gml format.
"""

from __future__ import annotations

from pathlib import Path

import networkx as nx


def write_gml(
    graph: nx.Graph, filepath: str | Path, *, compressed: bool = False
) -> None:
    """Write NetworkX graph into as a gml file.

    Args:
        graph: graph of the system to convert
        filepath: name or path of file to save it to
        compressed: compress the save file
    Returns:
        Written .gml file of graph object.
    """
    filename = f"{filepath}.gz" if compressed else str(filepath)
    nx.write_gml(graph, filename, str)


def load_gml(filename: str | Path) -> nx.Graph:
    """Convert .gml file into a NetworkX graph.

    Args:
        filename: name or path of file to save it to.

    Returns:
        A NetworkX graph.
    """
    filename = Path(filename)
    return nx.read_gml(filename, destringizer=_destringizer)


def _destringizer(string: str) -> str | complex | int | float:
    if string.strip("()").endswith("j"):
        try:
            return complex(string)
        except ValueError:
            pass
    if string.isnumeric():
        return int(string)
    try:
        return float(string)
    except ValueError:
        return string
