"""Make a simple graph for testing."""

import networkx as nx


def make_test_graph() -> nx.Graph:
    """Make a test graph with 6 nodes.

    The graph has 5 active edges and 5 inactive edges.
    """
    graph = nx.Graph()
    graph.add_edge(0, 1, weight=1)
    graph.add_edge(0, 2, weight=1)
    graph.add_edge(0, 3, weight=1)
    graph.add_edge(1, 4, weight=1)
    graph.add_edge(2, 4, weight=-1)
    graph.add_edge(2, 3, weight=-1)
    graph.add_edge(3, 4, weight=-1)
    graph.add_edge(1, 2, weight=-1)
    graph.add_edge(0, 5, weight=1)
    graph.add_edge(4, 5, weight=-1)
    return graph
