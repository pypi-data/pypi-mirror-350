from pathlib import Path

import networkx as nx
import pytest

from tno.quantum.problems.n_minus_1.io._graphs_io import (
    load_gml,
    write_gml,
)


@pytest.fixture(scope="session", name="temp_path")
def temp_path_fixture(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return tmp_path_factory.mktemp("temp_data")


def test_graphs_io(temp_path: Path) -> None:
    """Test if loading writing to and loading from does not alter the graph."""
    graph1 = nx.Graph()
    graph1.add_edge(0, 1, weight=1)
    graph1.add_edge(0, 2, weight=1)
    graph1.add_edge(0, 3, weight=1)
    graph1.add_edge(1, 4, weight=1)
    graph1.add_edge(2, 4, weight=-1)
    graph1.add_edge(2, 3, weight=-1)

    write_gml(graph1, temp_path / "test.gml", compressed=True)
    graph2 = load_gml(temp_path / "test.gml.gz")

    # Check if all the nodes are the same
    assert graph1.nodes == graph2.nodes
    for node in graph1.nodes:
        assert graph1.nodes[node] == graph2.nodes[node]

    # Check if all the edges are the same
    assert graph1.edges == graph2.edges
    for edge in graph1.edges:
        assert graph1.edges[edge] == graph2.edges[edge]
