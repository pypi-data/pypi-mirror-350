"""This module contains utility functions for the loadflow computations."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    import networkx as nx

LOGGER = logging.getLogger(__name__)


def check_graph_attributes(graph: nx.Graph) -> None:
    """Checks if a graph has the required attributes to describe a loadflow problem.

    All nodes must have the attributes 'type', 'U_min', 'U_max', 'P_low' and 'U_ref'.
    All edges must have the attributes 'Z', 'active', 'I_max' and 'edge_idx'.

    Args:
        graph: Graph to check.

    Raises:
        ValueError: If the graph is missing one ore more attributes.
    """
    for node in graph.nodes:
        for attribute in ["type", "U_min", "U_max", "P_low", "U_ref"]:
            if attribute not in graph.nodes[node]:
                error_msg = f"Node {node} is missing attribute {attribute}"
                raise ValueError(error_msg)

    for edge in graph.edges:
        for attribute in ["Z", "active", "I_max", "edge_idx"]:
            if attribute not in graph.edges[edge]:
                error_msg = f"Edge {edge} is missing attribute {attribute}"
                raise ValueError(error_msg)


def check_ordering(graph: nx.Graph) -> None:
    """Check ordering of loadflow model.

    Checks if a `graph` describing a loadflow model orders its nodes by having the
    OS nodes at the end of the node list.

    Args:
        graph: Graph to check.

    Raises:
        ValueError: If there is any OS node before a MSR node.
    """
    found_os = False
    for node in graph.nodes:
        if graph.nodes[node]["type"] == "OS":
            found_os = True
        elif found_os:
            error_msg = "OS node found before the last MSR node."
            raise ValueError(error_msg)


def make_linear_system(
    graph: nx.Graph,
) -> tuple[NDArray[np.complex128], NDArray[np.complex128]]:
    """Write the load flow equations of `graph` in the form Ax=b.

    Args:
        graph: Graph representing a load-flow problem.

    Returns:
        A and b.
    """
    check_graph_attributes(graph)

    # Note, this algorithm assumes the OS nodes are the last nodes in graph.nodes. So we
    # check for that first.
    check_ordering(graph)

    n_msr = 0
    for node in graph.nodes:
        if graph.nodes[node]["type"] == "MSR":
            n_msr += 1

    A = np.zeros((n_msr, n_msr), dtype=complex)
    b = np.zeros(n_msr, dtype=complex)
    for n, m in graph.edges:
        if not graph.edges[n, m]["active"]:
            continue

        Z_nm = graph.edges[n, m]["Z"]
        if graph.nodes[n]["type"] == "MSR":
            A[n, n] += 1 / Z_nm
        else:
            b[m] += graph.nodes[n]["U_min"] / Z_nm

        if graph.nodes[m]["type"] == "MSR":
            A[m, m] += 1 / Z_nm
        else:
            b[n] += graph.nodes[m]["U_min"] / Z_nm

        if graph.nodes[n]["type"] == "MSR" and graph.nodes[m]["type"] == "MSR":
            A[n, m] -= 1 / Z_nm
            A[m, n] -= 1 / Z_nm

    for n in range(n_msr):
        load = graph.nodes[n]["P_low"] + 1000
        U_ref = graph.nodes[n]["U_ref"]
        A[n, n] += abs(load) ** 2 / (U_ref**2 * load.real)

    return A, b


def is_loadflow_compliant(graph: nx.Graph) -> bool:
    """Check if loadflow is compliant.

    Args:
        graph: Graph representing a load-flow problem.

    Returns:
        Whether loadflow is compliant.
    """
    solution = np.linalg.solve(*make_linear_system(graph))
    for node, volt in zip(graph.nodes, solution):
        node_info = graph.nodes[node]
        if abs(volt) < node_info["U_min"] or abs(volt) > node_info["U_max"]:
            LOGGER.error("Loadflow failed in node %s, U=%s", node, volt)
            return False

    volt_os = [
        graph.nodes[node]["U_min"]
        for node in graph.nodes
        if graph.nodes[node]["type"] == "OS"
    ]
    volts: NDArray[np.complex128] = np.concatenate((solution, volt_os))
    for n, m in graph.edges:
        if not graph.edges[n, m]["active"]:
            continue
        current = (volts[n] - volts[m]) / graph.edges[n, m]["Z"]
        if abs(current) > graph.edges[n, m]["I_max"]:
            LOGGER.error("Loadflow failed in edge %s,%s, I=%s", n, m, current)
            return False

    return True
