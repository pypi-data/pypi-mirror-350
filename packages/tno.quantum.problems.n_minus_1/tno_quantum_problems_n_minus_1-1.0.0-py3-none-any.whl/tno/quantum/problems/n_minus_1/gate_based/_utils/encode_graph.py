"""Encode graphs in a quantum circuits."""

from __future__ import annotations

from collections.abc import Hashable
from math import ceil, log2
from typing import TYPE_CHECKING

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library.standard_gates import XGate

from tno.quantum.problems.n_minus_1.gate_based._gates import get_bitstring_rep

if TYPE_CHECKING:
    import networkx as nx


def encode_graph(
    circuit: QuantumCircuit, graph: nx.Graph, *, exact_superposition: bool
) -> None:
    """Initialize the circuit in such a way that the graph is encoded.

    We encode every node in the node_register as well as in the edge_register. For every
    node-neighbor edge a node in the node_register is entangled with the neighbor in the
    edge_register. The circuit is altered inplace.

    Args:
        circuit: Quantum circuit to initialize.
        graph: Netwrokx representation fo the graph to encode.
        exact_superposition: Whether to compute the exact superposition or not.

    Returns:
        The circuit with the initialized to represent the graph.
    """
    log_num_nodes = ceil(log2(len(graph)))

    length_single_register = 2 ** (log_num_nodes)
    initial_vector = np.zeros(length_single_register**2)

    for node in graph.nodes():
        for neighbor in graph[node]:
            idx = node * length_single_register + neighbor
            initial_vector[idx] += 1 / np.sqrt(len(graph[node]))
    if exact_superposition:
        initial_vector /= np.sqrt(len(graph))
    else:
        for i_node in range(len(graph.nodes), length_single_register):
            initial_vector[i_node * length_single_register] += 1
        initial_vector /= np.sqrt(length_single_register)

    circuit.initialize(initial_vector)
    circuit = circuit.reverse_bits()


def set_active_edges(circuit: QuantumCircuit, graph: nx.Graph) -> None:
    """Entangles the activity status register to the edges of the encoded graph.

    For every edge, we flip the active_register_qubit for both (node-neighbor)
    and (neighbor-node) if the edge is active.

    The activeness of an edge is for now given by the weight of a graph.

    Args:
        circuit: Circuit to add the operations too.
        graph: Networkx graph representation.
    """
    log_num_nodes = ceil(log2(len(graph)))

    active_register = QuantumRegister(1, "a")
    circuit.add_register(active_register)

    for current_edge in graph.edges:
        if graph[current_edge[0]][current_edge[1]]["weight"] == 1:
            (vertex, neighbor) = current_edge

            # vertex-neighbor
            toggle_edge(log_num_nodes, vertex, neighbor, circuit)

            # neighbor-vertex
            toggle_edge(log_num_nodes, neighbor, vertex, circuit)


def toggle_edge(
    log_num_nodes: int, vertex: int, neighbor: int, circuit: QuantumCircuit
) -> QuantumCircuit:
    """Toggle the active register for a given edge.

    Args:
        log_num_nodes: The logarithm of the number of nodes in the graph.
        vertex: The source vertex of the edge.
        neighbor: The target vertex of the edge.
        circuit: The quantum circuit to modify.

    Returns:
        The modified quantum circuit.
    """
    control_state = get_bitstring_rep(neighbor, log_num_nodes)
    control_state += get_bitstring_rep(vertex, log_num_nodes)
    sub_routine = XGate().control(len(control_state), ctrl_state=control_state)
    circuit.append(sub_routine, list(range(2 * log_num_nodes + 1)))
    return circuit


def encode_network_edges(
    graph: nx.Graph,
) -> tuple[list[tuple[Hashable, Hashable]], list[tuple[Hashable, Hashable]]]:
    """Get the active and inactive edges from the graph.

    Args:
        graph: Networkx representation of the graph. Each edge should have the "weight"
            attribute.

    Returns:
        A tuple of the active and inactive edges.
    """
    active_edges = []
    inactive_edges = []
    for edge in graph.edges(data=True):
        if edge[2]["weight"] == 1:
            active_edges.append(edge[:2])
        else:
            inactive_edges.append(edge[:2])

    if len(active_edges) != len(graph) - 1:
        error_msg = (
            f"Number of active edges is {len(active_edges)}, "
            f"should be {len(graph) - 1}."
        )
        raise ValueError(error_msg)
    return active_edges, inactive_edges
