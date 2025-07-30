"""This module contains the ``DecodedResult`` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

import networkx as nx

from tno.quantum.problems.n_minus_1._utils import is_loadflow_compliant
from tno.quantum.utils.validation import check_ax

if TYPE_CHECKING:
    from matplotlib.axes import Axes


class DecodedResult:
    """The :py:class:`~DecodedResult` class.

    :py:class:`~DecodedResult` stores results decoded from a sample of a sampleset.
    """

    def __init__(self, graph: nx.Graph) -> None:
        """Init of the :py:class:`~DecodedResult` class.

        Args:
            graph: Graph of a power network. If the :py:class:`~DecodedResult` is used
                store decoded results containing loadflow constraints, then `graph`
                should have nodes and edges as described in
                :py:class:`~tno.quantum.problems.n_minus_1.QABasedNMinusOneSolver`.
        """
        self._graph = graph
        self.turned_on = []
        self.turned_off = []
        for edge, switched in nx.get_edge_attributes(graph, "switched").items():
            if switched and graph.edges[edge]["active"]:
                self.turned_off.append(edge)
            elif switched and not graph.edges[edge]["active"]:
                self.turned_on.append(edge)

    def __repr__(self) -> str:
        """String representation of the result.

        Returns:
            String representation of the class, using the class name, number of nodes,
            turned on edges and turned off edges.

        Example:
                ``"DecodedResult[n_nodes=4, turned_on=[(3,4)], turned_off=[(2,3)]]"``.
        """
        return (
            f"{self.__class__.__name__}"
            f"[n_nodes={len(self._graph)}, "
            f"turned_on={self.turned_on}, "
            f"turned_off={self.turned_off}]"
        )

    def get_k(self) -> int:
        """Get `k`, which is the number of switches.

        Returns:
            Integer value representing the number of switched used in this solution.
            In this case, the failing edge is not interpreted as a switch.
        """
        return len(self.turned_on) + len(self.turned_off)

    def draw(self, ax: Axes | None = None, *, check_loadflow: bool = False) -> None:
        """Create image of the result.

        Args:
            check_loadflow: Wether to check if the graph is loadflow complient. Default
                is ``False``.
            ax: Axes to plot on. If ``None`` create a new figure with a new ax.
        """
        ax = check_ax(ax, "ax")

        # Visualize graph and save image
        edge_color = []
        for edge in self._graph.edges:
            edge_attributes = self._graph.edges[edge]
            if edge_attributes["active"] and not edge_attributes["switched"]:
                edge_color.append("black")
            elif edge_attributes["active"] and edge_attributes["switched"]:
                edge_color.append("red")
            elif not edge_attributes["active"] and not edge_attributes["switched"]:
                edge_color.append("grey")
            else:
                edge_color.append("green")

        pos = nx.kamada_kawai_layout(self._graph)
        if check_loadflow:
            if is_loadflow_compliant(self._graph):
                ax.set_title(f"k={self.get_k()}  |  loadflow compliant")
            else:
                ax.set_title(f"k={self.get_k()}  |  not loadflow compliant")
        else:
            ax.set_title(f"k={self.get_k()}")
        nx.draw_networkx(self._graph, pos=pos, edge_color=edge_color, width=2, ax=ax)

    def __eq__(self, other: object) -> bool:
        r"""Simple equals function.

        Two :py:class:`~DecodedResult`\s are equal if if the underlying graph after
        performing the switches are equal.
        """
        if not isinstance(other, DecodedResult):
            return False
        return bool(nx.utils.graphs_equal(self._graph, other._graph))

    def __hash__(self) -> int:
        """Simple hash function.

        Creates a hash of the graph using the Return Weisfeiler Lehman (WL) graph hash
        together with simple hashes of the turned on/off edges.
        """
        graph_hash = nx.weisfeiler_lehman_graph_hash(self._graph)
        turned_on_hash = hash(tuple(self.turned_on))
        turned_off_hash = hash(tuple(self.turned_off))
        return hash((graph_hash, turned_on_hash, turned_off_hash))
