"""this module contains tests for the encode_graph module."""

import networkx as nx
import pytest

from tno.quantum.problems.n_minus_1.gate_based._utils.encode_graph import (
    encode_network_edges,
)


@pytest.fixture(name="graph")
def graph_fixture() -> nx.Graph:
    graph = nx.Graph()
    graph.add_edge(0, 1, weight=1)
    graph.add_edge(0, 2, weight=1)
    graph.add_edge(1, 2, weight=-1)
    return graph


def test_active_edges(graph: nx.Graph) -> None:
    active_edges, _ = encode_network_edges(graph)
    assert active_edges == [(0, 1), (0, 2)]


def test_inactive_edges(graph: nx.Graph) -> None:
    _, inactive_edges = encode_network_edges(graph)
    assert inactive_edges == [(1, 2)]
