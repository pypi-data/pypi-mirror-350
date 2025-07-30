"""This module contains the ``LayersFactory`` class."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from copy import deepcopy
from math import floor
from typing import TYPE_CHECKING, Any, cast, overload

import numpy as np
from dimod import BinaryQuadraticModel, SampleSet, quicksum
from numpy.typing import NDArray

from tno.quantum.problems.n_minus_1.quantum_annealing._bqm_factories.utils import (
    create_discrete_variable,
)
from tno.quantum.problems.n_minus_1.quantum_annealing._containers import (
    DecodedResult,
    ResultsOverview,
)

if TYPE_CHECKING:
    import networkx as nx
    from networkx.classes.reportviews import EdgeView, NodeView

LOGGER = logging.getLogger(__name__)


class LayersFactory:
    """The :py:class:`~LayersFactory` class.

    This class is used for constructing Binary Quadratic Models of which the low energy
    states represents a tree graph. This is done by using the layered properties of
    rooted trees.
    """

    def __init__(self, graph: nx.Graph, n_layers: int | None = None) -> None:
        """Init of the :py:class:`~LayersFactory` class.

        Args:
            graph: Networkx graph to build the BQMs for.
            n_layers: Number of layers to use in the formulation.
        """
        self.graph = deepcopy(graph)
        if n_layers is None:
            self.n_layers = floor(len(graph) / 2) + 1
        else:
            self.n_layers = n_layers

    @property
    def _edges(self) -> EdgeView:
        """Edges of the graph."""
        return self.graph.edges

    @property
    def _nodes(self) -> NodeView:
        """Nodes of the graph."""
        return self.graph.nodes

    def build_bqm(  # noqa: PLR0913
        self,
        encoding: str = "domain-wall",
        *,
        penalty_depth_nodes: float = 20,
        penalty_depth_edges: float = 20,
        penalty_one_root: float = 10,
        penalty_connectivity: float = 10,
        penalty_indicators: float = 10,
    ) -> BinaryQuadraticModel:
        """Build the BQM using the specified parameters.

        Args:
            encoding: Choose 'domain-wall' (default) or 'one-hot'.
            penalty_depth_nodes: Absolute penalty scaling to use for the depth penalty
                of the nodes.
            penalty_depth_edges: Absolute penalty scaling to use for the depth penalty
                of the edges.
            penalty_one_root: Absolute penalty scaling to use for the one root penalty.
            penalty_connectivity: Absolute penalty scaling to use for the connectivity
                penalty.
            penalty_indicators: Absolute penalty scaling to use for the indicator
                penalty.

        Returns:
            A ``BinaryQuadraticModel`` of which low energy values encode tree subgraphs
            of the original graph. The lower the number of switches needed to get to
            the output graph, the lower the energy of that encoded graph is.
        """
        # Create Variables:
        x, penalty_discrete_nodes = self._create_x(encoding)
        y, penalty_discrete_edges = self._create_y(encoding)

        # There can only be one root node
        bqm_one_root = (quicksum(x[:, 0]) - 1) ** 2
        bqm_indicators = self._make_indicators_bqm(x, y)
        # Every non root node has exactly one edge connecting it with the layer above
        bqm_connectivity = self._make_connectivity_bqm(x, y)

        # Set the objective
        bqm_objective = self._make_objective(y)

        return cast(
            "BinaryQuadraticModel",
            (
                bqm_objective
                + penalty_depth_nodes * penalty_discrete_nodes
                + penalty_depth_edges * penalty_discrete_edges
                + penalty_one_root * bqm_one_root
                + penalty_connectivity * bqm_connectivity
                + penalty_indicators * bqm_indicators
            ),
        )

    def _create_x(self, encoding: str) -> tuple[NDArray[Any], BinaryQuadraticModel]:
        """Create the node variables."""
        variables = []
        penalties = []
        for n in self._nodes:
            var, penalty = create_discrete_variable(f"x{n}", self.n_layers, encoding)
            variables.append(var)
            penalties.append(penalty)

        return np.array(variables), cast("BinaryQuadraticModel", quicksum(penalties))

    def _create_y(
        self, encoding: str
    ) -> tuple[dict[tuple[int, int], NDArray[Any]], BinaryQuadraticModel]:
        """Create the edge variables."""
        penalties = []
        n_choices = 2 * self.n_layers - 1
        variables = {}
        for n, m in self._edges:
            var, penalty = create_discrete_variable(f"y{n},{m}", n_choices, encoding)
            variables[n, m] = np.array(var)
            penalties.append(penalty)
        return variables, cast("BinaryQuadraticModel", quicksum(penalties))

    def _make_objective(
        self, y: dict[tuple[int, int], NDArray[Any]]
    ) -> BinaryQuadraticModel:
        """Construct the objective function."""
        bqm_objective = BinaryQuadraticModel("BINARY")
        for n, m in self._edges:
            if self._edges[n, m]["active"]:
                bqm_objective += y[n, m][-1]
            else:
                bqm_objective.offset += 1
                bqm_objective -= y[n, m][-1]
        return bqm_objective

    def _make_indicators_bqm(
        self,
        x: NDArray[Any],
        y: dict[tuple[int, int], NDArray[Any]],
    ) -> BinaryQuadraticModel:
        """Construct the indicator penalty term."""
        bqm_indicators = BinaryQuadraticModel("BINARY")
        for n, m in self._edges:
            # For edge at depth i connects a vertex from layer i with layer i+1
            for i in range(self.n_layers - 1):
                bqm_indicators += y[n, m][i] * (2 - x[n, i + 1] - x[m, i])
                bqm_indicators += y[n, m][i + self.n_layers - 1] * (
                    2 - x[n, i] - x[m, i + 1]
                )
        return bqm_indicators

    def _make_connectivity_bqm(
        self,
        x: NDArray[Any],
        y: dict[tuple[int, int], NDArray[Any]],
    ) -> BinaryQuadraticModel:
        """Construct the connectivity penalty term."""
        # Every non root node has exactly one edge connecting it with the layer above
        bqm_connectivity = BinaryQuadraticModel("BINARY")
        for n in self._nodes:
            for i in range(1, self.n_layers):
                terms = [x[n, i]]
                for m in self.graph.adj[n]:
                    if (n, m) in y:
                        terms.append(-y[n, m][i - 1])
                    else:
                        terms.append(-y[m, n][i + self.n_layers - 2])
                bqm_connectivity += cast("BinaryQuadraticModel", quicksum(terms) ** 2)
        return bqm_connectivity

    @overload
    def decode_result(self, result: Mapping[str, int]) -> DecodedResult: ...

    @overload
    def decode_result(self, result: SampleSet) -> ResultsOverview: ...

    def decode_result(
        self, result: Mapping[str, int] | SampleSet
    ) -> DecodedResult | ResultsOverview:
        """Decode the results.

        Args:
            result: Single sample or ``SampleSet`` as retrieved from D-Wave.

        Returns:
            Decoded result or overview of the results.
        """
        if isinstance(result, SampleSet):
            return self._decode_sampleset(result)

        if isinstance(result, Mapping):
            self.check_feasible(result)
            return self._decode_sample(result)

        error_msg = "'result' must be an instance of Mapping or SampleSet"
        raise TypeError(error_msg)

    def _decode_sample(self, sample: Mapping[str, int]) -> DecodedResult:
        """Decode a single sample."""
        graph = deepcopy(self.graph)
        encoding = "one-hot" if "x0[0]" in sample else "domain-wall"

        y, _ = self._create_y(encoding)

        for n, m in self._edges:
            new_inactive = y[n, m][-1].energy(sample)
            old_active = self._edges[n, m]["active"]
            graph.edges[n, m]["switched"] = new_inactive == old_active

        return DecodedResult(graph)

    def _decode_sampleset(self, sampleset: SampleSet) -> ResultsOverview:
        """Decode a whole ``SampleSet``."""
        results_overview = ResultsOverview()
        sampleset = sampleset.aggregate()  # type: ignore[no-untyped-call]
        for sample, count in sampleset.data(fields=["sample", "num_occurrences"]):  # type: ignore[no-untyped-call]
            sample_dict = dict(sample)
            if self.is_feasible(sample_dict):
                decoded_result = self._decode_sample(sample_dict)
                results_overview.add_result(decoded_result, count)

        return results_overview

    def check_feasible(self, sample: Mapping[str, int]) -> None:
        """Check if a `sample` is feasible.

        Args:
            sample: Sample to check.

        Raises:
            ValueError: If the sample is not feasible.
        """
        encoding = "one-hot" if "x0[0]" in sample else "domain-wall"
        x, bqm_x = self._create_x(encoding)
        y, bqm_y = self._create_y(encoding)
        # There can only be one root node
        bqm_one_root = (quicksum(x[:, 0]) - 1) ** 2
        bqm_indicators = self._make_indicators_bqm(x, y)
        # Every non root node has exactly one edge connecting it with the layer above
        bqm_connectivity = self._make_connectivity_bqm(x, y)

        error_msg = None
        if bqm_x.energy(sample):
            error_msg = f"{encoding} broke in the nodes"
        elif bqm_y.energy(sample):
            error_msg = f"{encoding} broke in the edges"
        elif bqm_one_root.energy(sample):
            error_msg = "There is not exactly one root"
        elif bqm_indicators.energy(sample):
            error_msg = "Indicators do not behave correctly"
        elif bqm_connectivity.energy(sample):
            error_msg = "Graph is not connected"

        if error_msg:
            raise ValueError(error_msg)

    def is_feasible(self, sample: Mapping[str, int]) -> bool:
        """Deduce the feasibility of the `sample`.

        Args:
            sample: Sample to check.

        Returns:
            Boolean value stating wether the `sample` is feasible or not.
        """
        try:
            self.check_feasible(sample)
        except ValueError:
            return False
        return True
