"""Module contains the ``NMOFactory``, which makes BQM models for the N-1 problem."""

from __future__ import annotations

from collections import deque
from collections.abc import Hashable, Mapping
from typing import TYPE_CHECKING, Any, cast, overload

from dimod import BinaryQuadraticModel, quicksum
from numpy.typing import NDArray

from tno.quantum.optimization.qubo.components import ResultInterface
from tno.quantum.problems.n_minus_1.quantum_annealing._bqm_factories.layers_factory import (  # noqa: E501
    LayersFactory,
)
from tno.quantum.problems.n_minus_1.quantum_annealing._bqm_factories.loadflow_factory import (  # noqa: E501
    LoadflowFactory,
)
from tno.quantum.problems.n_minus_1.quantum_annealing._bqm_factories.utils import (
    build_auxvar_bqm,
    link_variables,
)
from tno.quantum.problems.n_minus_1.quantum_annealing._containers import (
    DecodedResult,
    ResultsOverview,
)
from tno.quantum.utils import BitVector

if TYPE_CHECKING:
    import networkx as nx
    from networkx.classes.reportviews import EdgeView, NodeView

    from tno.quantum.utils import BitVectorLike


class NMOFactory:
    """:py:class:`~NMOFactory` class.

    This class is used for constructing Binary Quadratic Models which of which the low
    energy states represent tree graph which minimize the residual of the linear
    equations used to describe the load flow constraint. To construct such Binary
    Quadratic Model, this Factory uses combines tools from the
    :py:class:`~LayersFactory` and the :py:class:`~LoadflowFactory`.

    More specifically, the variables governing the tree structure are linked to the
    variables describing the loadflow constraints using
    :py:func:`~n_minus_1.quantum_annealing.bqm_factories.utils.link_variables`.
    """

    def __init__(
        self, graph: nx.Graph, n_layers: int | None, K: int, L: int, M: int
    ) -> None:
        """Init of the ``NMOFactory``.

        Args:
            graph: Graph representing a power network.
            n_layers: Number of layers to use for the tree formulation.
            K: Number of auxiliary variables to use or encoding the real part of the
                potential.
            L: Number of auxiliary variables to use or encoding the imaginary part of
                the potential.
            M: Number of auxiliary variables to use for encoding the current.
        """
        self._layers_factory = LayersFactory(graph, n_layers)
        self._loadflow_factory = LoadflowFactory(graph, K, L, M)
        self._U_real = {
            n: self._loadflow_factory._encode_real_potential(n)  # noqa: SLF001
            for n in self._nodes
        }
        self._U_imag = {
            n: self._loadflow_factory._encode_imag_potential(n)  # noqa: SLF001
            for n in self._nodes
        }

    @property
    def graph(self) -> nx.Graph:
        """Graph representing a power network."""
        return self._layers_factory.graph

    @property
    def _nodes(self) -> NodeView:
        """Nodes of the graph."""
        return self._layers_factory.graph.nodes

    @property
    def _edges(self) -> EdgeView:
        """Edges of the graph."""
        return self._layers_factory.graph.edges

    def build_bqm(
        self,
        penalty_depth: float = 400,
        penalty_connectivity: float = 100,
        penalty_loadflow: float = 2,
        penalty_auxvar: float = 1,
        p_extra: float = 1000,
    ) -> BinaryQuadraticModel:
        """Build the N-1 ``BinaryQuadraticModel``.

        Args:
            p_extra: Extra power to add to each node for numerical stability.
            penalty_depth: Absolute penalty scaling to use for the depth penalty.
            penalty_connectivity: Absolute penalty scaling to use for the connectivity
                penalty.
            penalty_loadflow: Absolute penalty scaling to use for the loadflow penalty.
            penalty_auxvar: Absolute penalty scaling to use for the penalty governing
                the behavior of the auxiliary variables.

        Returns:
            A ``BinaryQuadraticModel`` encoding the N-1 problem.
        """
        # Create Variables:
        y, _ = self._layers_factory._create_y("domain-wall")  # noqa: SLF001

        bqm_objective_and_tree = self._layers_factory.build_bqm(
            penalty_depth_nodes=penalty_depth,
            penalty_depth_edges=penalty_depth,
            penalty_one_root=penalty_connectivity,
            penalty_connectivity=penalty_connectivity,
            penalty_indicators=penalty_connectivity,
        )

        bqm_load_flow = self._build_loadflow_bqm(y, p_extra)

        # Build auxvar BQM
        bqm_auxvar = build_auxvar_bqm(bqm_load_flow)

        bqm_all = (
            bqm_objective_and_tree
            + penalty_loadflow * bqm_load_flow
            + penalty_auxvar * bqm_auxvar
        )
        return cast("BinaryQuadraticModel", bqm_all)

    def _build_loadflow_bqm(
        self, y: dict[tuple[int, int], NDArray[Any]], p_extra: float = 1000
    ) -> BinaryQuadraticModel:
        """Build a loadflow BQM."""
        bqm_real_potential = self._build_real_potential_bqm(y, p_extra)
        bqm_imag_potential = self._build_imag_potential_bqm(y, p_extra)
        bqm_current = self._build_current_bqm(y)
        bqm_loadflow = bqm_real_potential + bqm_imag_potential + bqm_current
        return cast("BinaryQuadraticModel", bqm_loadflow)

    def _build_real_potential_penalty(
        self, n: int, y: dict[tuple[int, int], NDArray[Any]], p_extra: float = 1000
    ) -> BinaryQuadraticModel:
        """Build the real potential penalty."""
        load = self._nodes[n]["P_low"] + p_extra
        U_ref = self._nodes[n]["U_ref"]
        alpha = abs(load) ** 2 / (U_ref**2 * load.real)
        terms: deque[BinaryQuadraticModel] = deque()
        terms.append(alpha * self._U_real[n])

        for m in self.graph.adj[n]:
            edge = (n, m) if (n, m) in y else (m, n)
            Z_nm = self._edges[edge]["Z"]
            beta = (1 / Z_nm).real
            gamma = (1 / Z_nm).imag
            y_nm = y[edge][-1].variables[0]

            terms.append(beta * link_variables(y_nm, self._U_real[n]))
            terms.append(-beta * link_variables(y_nm, self._U_real[m]))
            terms.append(-gamma * link_variables(y_nm, self._U_imag[n]))
            terms.append(gamma * link_variables(y_nm, self._U_imag[m]))

        return cast("BinaryQuadraticModel", quicksum(terms) ** 2)

    def _build_real_potential_bqm(
        self, y: dict[tuple[int, int], NDArray[Any]], p_extra: float = 1000
    ) -> BinaryQuadraticModel:
        """Build the real potential bqm."""
        terms: deque[BinaryQuadraticModel] = deque()
        for n in self._nodes:
            # The potential is fixed at the OS, so we don't add it to the BQM
            if self._nodes[n]["type"] == "OS":
                continue
            terms.append(self._build_real_potential_penalty(n, y, p_extra))
        return cast("BinaryQuadraticModel", quicksum(terms))

    def _build_imag_potential_bqm(
        self, y: dict[tuple[int, int], NDArray[Any]], p_extra: float = 1000
    ) -> BinaryQuadraticModel:
        """Build the imaginary potential bqm."""
        terms: deque[BinaryQuadraticModel] = deque()
        for n in self._nodes:
            # The potential is fixed at the OS, so we don't add it to the BQM
            if self._nodes[n]["type"] == "OS":
                continue
            terms.append(self._build_imag_potential_penalty(n, y, p_extra))
        return cast("BinaryQuadraticModel", quicksum(terms))

    def _build_imag_potential_penalty(
        self, n: int, y: dict[tuple[int, int], NDArray[Any]], p_extra: float = 1000
    ) -> BinaryQuadraticModel:
        """Build the imaginary potential penalty."""
        load = self._nodes[n]["P_low"] + p_extra
        U_ref = self._nodes[n]["U_ref"]
        alpha = abs(load) ** 2 / (U_ref**2 * load.real)
        terms: deque[BinaryQuadraticModel] = deque()
        terms.append(alpha * self._U_imag[n])

        for m in self.graph.adj[n]:
            edge = (n, m) if (n, m) in y else (m, n)
            Z_nm = self._edges[edge]["Z"]
            beta = (1 / Z_nm).real
            gamma = (1 / Z_nm).imag
            y_nm = y[edge][-1].variables[0]

            terms.append(beta * link_variables(y_nm, self._U_imag[n]))
            terms.append(-beta * link_variables(y_nm, self._U_imag[m]))
            terms.append(gamma * link_variables(y_nm, self._U_real[n]))
            terms.append(-gamma * link_variables(y_nm, self._U_real[m]))

        return cast("BinaryQuadraticModel", quicksum(terms) ** 2)

    def _build_current_penalty(
        self, edge: tuple[int, int], y: dict[tuple[int, int], NDArray[Any]]
    ) -> BinaryQuadraticModel:
        """Build the current penalty term."""
        I = self._loadflow_factory._encode_current(edge)  # noqa: SLF001, E741
        n, m = edge if edge in y else (edge[1], edge[0])
        Z_nm = self._edges[edge]["Z"]
        beta = (1 / Z_nm).real
        gamma = (1 / Z_nm).imag
        y_nm = y[n, m][-1].variables[0]

        bqm = (
            quicksum(
                [
                    I,
                    beta * link_variables(y_nm, self._U_real[n]),
                    -beta * link_variables(y_nm, self._U_real[m]),
                    -gamma * link_variables(y_nm, self._U_imag[n]),
                    gamma * link_variables(y_nm, self._U_imag[m]),
                ]
            )
            ** 2
        )
        return cast("BinaryQuadraticModel", bqm)

    def _build_current_bqm(
        self, y: dict[tuple[int, int], NDArray[Any]]
    ) -> BinaryQuadraticModel:
        """Build the current BQM for all edges."""
        terms: deque[BinaryQuadraticModel] = deque()
        for edge in self._edges:
            # Skip inactive edges and edges that always comply with the load flow
            if self._loadflow_factory.always_loadflow_compliant(edge):
                continue
            terms.append(self._build_current_penalty(edge, y))
        return cast("BinaryQuadraticModel", quicksum(terms))

    @overload
    def decode_result(
        self, result: BitVectorLike, labels: list[Hashable]
    ) -> DecodedResult: ...

    @overload
    def decode_result(
        self, result: ResultInterface, labels: list[Hashable]
    ) -> ResultsOverview: ...

    def decode_result(
        self, result: BitVectorLike | ResultInterface, labels: list[Hashable]
    ) -> DecodedResult | ResultsOverview:
        """Decode the results.

        Args:
            result: Result as returned by a tno Solver.
            labels: Labels of the variables in the QUBO problem.

        Returns:
            Decoded results.
        """
        if isinstance(result, ResultInterface):
            return self._decode_result_interface(result, labels)

        try:
            bit_vector = BitVector(result)
        except TypeError as e:
            error_msg = (
                "'result' must be an instance of ResultInterface or a BitVectorLike "
            )
            raise TypeError(error_msg) from e

        sample = dict(zip(map(str, labels), map(int, bit_vector)))
        self._layers_factory.check_feasible(sample)
        return self._decode_sample(sample)

    def _decode_sample(self, sample: Mapping[str, int]) -> DecodedResult:
        """Decode a single sample."""
        return self._layers_factory._decode_sample(sample)  # noqa: SLF001

    def _decode_result_interface(
        self, result: ResultInterface, labels: list[Hashable]
    ) -> ResultsOverview:
        """Decode a whole `sampleset`."""
        results_overview = ResultsOverview()
        for bitvector, _, count in result.freq:
            sample = dict(zip(map(str, labels), map(int, bitvector)))
            if self._layers_factory.is_feasible(sample):
                decoded_result = self._decode_sample(sample)
                results_overview.add_result(decoded_result, count)

        return results_overview
