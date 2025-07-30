"""This module contains the ``QABasedNMinusOneSolver``."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import TYPE_CHECKING

import networkx as nx

from tno.quantum.optimization.qubo.components import QUBO, SolverConfig
from tno.quantum.problems.n_minus_1.quantum_annealing._bqm_factories import NMOFactory
from tno.quantum.utils import BaseArguments
from tno.quantum.utils.validation import check_instance, check_int, check_real

if TYPE_CHECKING:
    from collections.abc import Hashable, Mapping
    from typing import Any, Self, SupportsFloat, SupportsInt

    from tno.quantum.optimization.qubo.components import ResultInterface
    from tno.quantum.problems.n_minus_1.quantum_annealing._containers import (
        ResultsOverview,
    )


@dataclass(init=False)
class FactoryArguments(BaseArguments):
    """Arguments for the N-Minus-1 QUBO factory."""

    n_layers: int | None
    """Number of layers to use for the tree formulation."""

    K: int
    """Number of auxiliary variables to use for encoding real part of the potential."""

    L: int
    """Number of auxiliary variables to use for encoding imaginary part of the
    potential."""

    M: int
    """Number of auxiliary variables to use for encoding the current."""

    def __init__(
        self,
        n_layers: SupportsInt | None,
        K: SupportsInt,
        L: SupportsInt,
        M: SupportsInt,
    ) -> None:
        """Init of the ``NMOFactory``.

        Args:
            n_layers: Number of layers to use for the tree formulation.
            K: Number of auxiliary variables to use or encoding the real part of the
                potential.
            L: Number of auxiliary variables to use or encoding the imaginary part of
                the potential.
            M: Number of auxiliary variables to use for encoding the current.
        """
        self.n_layers = (
            n_layers if n_layers is None else check_int(n_layers, "n_layers", l_bound=1)
        )
        self.K = check_int(K, "K", l_bound=0)
        self.L = check_int(L, "L", l_bound=0)
        self.M = check_int(M, "M", l_bound=0)

    @classmethod
    def default(cls) -> Self:
        """Create a default instance of the factory arguments.

        The defaults sets the following values:

        - Number of layers: ``n_layers = None``,
        - Number of auxiliary variables real part potential: ``K = 6``,
        - Number of auxiliary variables imag part potential: ``L = 5``,
        - Number of auxiliary variables current: ``M = 5``,
        """
        return cls(n_layers=None, K=6, L=5, M=5)


@dataclass(init=False)
class QUBOArguments(BaseArguments):
    """Arguments for the N-1 QUBO."""

    penalty_depth: float
    """Absolute penalty scaling to use for the depth penalty."""

    penalty_connectivity: float
    """Absolute penalty scaling to use for the connectivity penalty."""

    penalty_loadflow: float
    """Absolute penalty scaling to use for the loadflow penalty."""

    penalty_auxvar: float
    """Absolute penalty scaling to use for the penalty governing the behaviour of the
    auxiliary variables."""

    p_extra: float
    """Extra power to add to each node for numerical stability."""

    def __init__(
        self,
        penalty_depth: SupportsFloat,
        penalty_connectivity: SupportsFloat,
        penalty_loadflow: SupportsFloat,
        penalty_auxvar: SupportsFloat,
        p_extra: SupportsFloat,
    ) -> None:
        """Arguments to configure the QUBO formulation for the N-1 problem.

        Args:
            penalty_depth: Absolute penalty scaling to use for the depth penalty.
            penalty_connectivity: Absolute penalty scaling to use for the connectivity
                penalty.
            penalty_loadflow: Absolute penalty scaling to use for the loadflow penalty.
            penalty_auxvar: Absolute penalty scaling to use for the penalty governing
                the behavior of the auxiliary variables.
            p_extra: Extra power to add to each node for numerical stability.
        """
        self.penalty_depth = check_real(penalty_depth, "penalty_depth", l_bound=0)
        self.penalty_connectivity = check_real(
            penalty_connectivity, "penalty_connectivity", l_bound=0
        )
        self.penalty_loadflow = check_real(
            penalty_loadflow, "penalty_loadflow", l_bound=0
        )
        self.penalty_auxvar = check_real(penalty_auxvar, "penalty_auxvar", l_bound=0)
        self.p_extra = check_real(p_extra, "p_extra", l_bound=0)

    @classmethod
    def default(cls) -> Self:
        """Create a default instance of the QUBO arguments.

        The defaults sets the following absolute penalty scaling values:

        - Depth penalty: ``penalty_depth = 400``,
        - Connectivity: ``penalty_connectivity = 100``,
        - Loadflow: ``penalty_loadflow = 2``,
        - Auxiliary variables: ``penalty_auxvar = 1``,
        - Numerical stability power: ``p_extra = 1``,
        """
        return cls(
            penalty_depth=400,
            penalty_connectivity=100,
            penalty_loadflow=2,
            penalty_auxvar=1,
            p_extra=1000,
        )


class QABasedNMinusOneSolver:
    """Quantum Annealing Based N-1 Solver.

    The Quantum Annealing solver performs the following steps:

        1. Transform the problem to a Binary Quadratic Model, also known as a Quadratic
           Unconstrained Optimization (QUBO).
        2. Approximate a solution to this problem with the given QUBO solver. This
           solver can be a quantum solver.
        3. Decode the bitstrings returned by the solver.
    """

    def __init__(
        self,
        graph: nx.Graph,
        failing_edge: tuple[Hashable, Hashable],
    ) -> None:
        """Init of the :py:class:`~QABasedNMinusOneSolver`.

        Args:
            graph: Network represented as a graph. Each node should have the following
                attributes: type, U_ref, P_low, P_high, U_min and U_max. Each edge
                should have the following attributes: active, edge_idx, Z and I_max.
            failing_edge: The edge that will fail in the scenario.
        """
        self.graph = check_instance(graph, "graph", nx.Graph)
        self.graph = deepcopy(graph)
        self.graph.remove_edge(*failing_edge)

    def run(
        self,
        factory_arguments: FactoryArguments | Mapping[str, Any] | None = None,
        qubo_arguments: QUBOArguments | Mapping[str, Any] | None = None,
        solver_config: SolverConfig | Mapping[str, Any] | None = None,
    ) -> ResultsOverview:
        """Run the algorithm.

        Args:
            factory_arguments: Keyword arguments for the Binary Quadratic Model factory.
                See the init of the :py:class:`~tno.quantum.problems.n_minus_1.quantum_annealing.FactoryArguments`
                for a more detailed description. If ``None`` is given (default), the
                :py:func:`~tno.quantum.problems.n_minus_1.quantum_annealing.FactoryArguments.default`
                arguments are used.
            qubo_arguments: Keyword arguments for building the QUBO. See
                :py:class:`~tno.quantum.problems.n_minus_1.quantum_annealing.QUBOArguments`
                for a more detailed description. If ``None`` is given (default), the
                :py:func:`~tno.quantum.problems.n_minus_1.quantum_annealing.QUBOArguments.default`
                arguments are used.
            solver_config: Configuration for the qubo solver to use. Must be a
                :py:class:`~tno.quantum.optimization.qubo.SolverConfig` or a mapping
                with ``"name"`` and ``"options"`` keys. If ``None`` (default) is
                provided, the :py:class:`~tno.quantum.optimization.qubo.solvers.SimulatedAnnealingSolver
                will be used, i.e. ``{"name": "simulated_annealing_solver", "options": {}}``.

        Returns:
            Result overview object containing the results.
        """  # noqa: E501
        # Parse user input
        factory_arguments = (
            FactoryArguments.default()
            if factory_arguments is None
            else FactoryArguments.from_mapping(factory_arguments)
        )
        qubo_arguments = (
            QUBOArguments.default()
            if qubo_arguments is None
            else QUBOArguments.from_mapping(qubo_arguments)
        )

        solver_config = (
            SolverConfig("simulated_annealing_solver")
            if solver_config is None
            else SolverConfig.from_mapping(solver_config)
        )

        bqm_factory = NMOFactory(self.graph, **factory_arguments)
        solver = solver_config.get_instance()

        # Run the algorithm
        bqm = bqm_factory.build_bqm(**qubo_arguments)
        labels: list[Hashable]
        qubo, labels = QUBO.from_bqm(bqm)
        result: ResultInterface = solver.solve(qubo)
        return bqm_factory.decode_result(result, labels)
