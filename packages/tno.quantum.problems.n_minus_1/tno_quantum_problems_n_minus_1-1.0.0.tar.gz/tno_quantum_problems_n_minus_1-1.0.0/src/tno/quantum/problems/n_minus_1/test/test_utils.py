"""This module contains tests for the ``qtree.formulations.utils`` module."""

import networkx as nx
import pytest

from tno.quantum.problems.n_minus_1._utils import check_ordering, is_loadflow_compliant
from tno.quantum.problems.n_minus_1.quantum_annealing.datasets import load_small_dataset


@pytest.fixture(name="graph")
def graph_fixture() -> nx.Graph:
    return load_small_dataset()


def test_is_loadflow_compliant_pass(graph: nx.Graph) -> None:
    assert is_loadflow_compliant(graph)


def test_is_loadflow_compliant_fail(graph: nx.Graph) -> None:
    graph.remove_edge(2, 6)
    assert not is_loadflow_compliant(graph)


def test_check_ordering_pass(graph: nx.Graph) -> None:
    check_ordering(graph)
