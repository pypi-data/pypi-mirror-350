"""Functions for solving the the n-1 problem with gate based quantum computing."""

from tno.quantum.problems.n_minus_1.gate_based._utils.encode_graph import (
    encode_graph,
    encode_network_edges,
    set_active_edges,
    toggle_edge,
)

__all__ = [
    "encode_graph",
    "encode_network_edges",
    "set_active_edges",
    "toggle_edge",
]
