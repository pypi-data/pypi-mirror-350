"""Gate Based N-1 Solver."""

from __future__ import annotations

from collections.abc import Hashable, Iterable
from typing import SupportsInt

import networkx as nx
import qiskit
import qiskit_aer
from qiskit.providers import Backend

from tno.quantum.problems.n_minus_1.gate_based._circuit_factory import CircuitFactory
from tno.quantum.utils.validation import check_instance, check_int


class GateBasedNMinusOneSolver:
    """Gate Based N-1 Solver.

    The gate based N-1 solver uses Grover to search for grid configurations that have
    the specified number of toggles and are load flow compliant.
    """

    def __init__(  # noqa: PLR0913
        self,
        graph: nx.Graph,
        failing_edge: tuple[int, int],
        load_flow_correctness: Iterable[Iterable[tuple[Hashable, Hashable]]],
        n_toggles: SupportsInt = 1,
        n_iter: SupportsInt = 1,
        quantum_backend: Backend | None = None,
        *,
        exact_superposition: bool = False,
    ) -> None:
        """Init GateBasedNMinusOneSolver.

        Args:
            graph: A `networkx` graph representation of an electric network.
            failing_edge: The edge that is currently failing i.e (1,4).
            load_flow_correctness: A list of edges that are load flow compliant
            n_toggles: Number of toggles possible.
            n_iter: Number of iterations
            quantum_backend: A 'qiskit' backend. Default is 'qasm_simulator'.
            exact_superposition: Choose if you want to use exact superposition with only
                useful states or an easier (superfluous) superposition with additional
                indices.
        """
        self.graph = check_instance(graph, "graph", nx.Graph)
        self.failing_edge = failing_edge
        self.load_flow_correctness = list(map(list, load_flow_correctness))
        self.n_toggles = check_int(n_toggles, "n_toggles", l_bound=1)
        self.n_iter = check_int(n_iter, "n_iter", l_bound=1)

        if quantum_backend is None:
            self.quantum_backend = qiskit_aer.Aer.get_backend("aer_simulator")
        else:
            self.quantum_backend = check_instance(
                quantum_backend, "quantum_backend", Backend
            )

        self.exact_superposition = exact_superposition

        self.gate_based_circuit = CircuitFactory(
            self.graph, exact_superposition=self.exact_superposition
        )

    def run(self) -> qiskit_aer.AerJob:
        """Run the algorithm."""
        circuit = self.gate_based_circuit.make_circuit(
            self.failing_edge,
            self.load_flow_correctness,
            self.n_iter,
            self.n_toggles,
        )
        transpiled_circuit = qiskit.transpile(
            circuit.reverse_bits(), backend=self.quantum_backend
        )

        return self.quantum_backend.run(transpiled_circuit, shots=10000)
