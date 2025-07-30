"""Module for the CircuitFactory class.

This class is used to create a quantum circuit for the N-1 problem.
"""

from __future__ import annotations

import logging
from collections.abc import Hashable
from itertools import combinations
from math import ceil, log2
from typing import TYPE_CHECKING

from qiskit.circuit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.circuit.library.standard_gates import XGate

from tno.quantum.problems.n_minus_1.gate_based._gates import (
    OracleFactory,
    get_bitstring_rep,
    make_amplitude_amplification_gate,
    make_superposition_gate,
)
from tno.quantum.problems.n_minus_1.gate_based._utils.encode_graph import (
    encode_graph,
    encode_network_edges,
    set_active_edges,
)

if TYPE_CHECKING:
    import networkx as nx

LOGGER = logging.getLogger(__name__)


class CircuitFactory:
    """CircuitFactory class for the n-1 problem."""

    def __init__(self, graph: nx.Graph, *, exact_superposition: bool = False) -> None:
        """Init CircuitFactory.

        Args:
            graph: A `networkx` graph representation of an electric network.
            The weights of the edges should be 1 if active, and -1 if inactive.
            exact_superposition: A Boolean that indicates if we prepare superpositions
                over 0...n-1 or over 0...2**(ceil(log_2(n)))-1. Default is false.
        """
        self.exact_superposition = exact_superposition

        # graph + properties
        self.graph = graph
        self.n_nodes = self.graph.number_of_nodes()
        self.log_n_nodes = ceil(log2(self.n_nodes))

    # below are all helper functions
    def _toggle_edge(
        self, vertex: int | Hashable, neighbor: int | Hashable, circuit: QuantumCircuit
    ) -> None:
        control_state = get_bitstring_rep(neighbor, self.log_n_nodes)
        control_state += get_bitstring_rep(vertex, self.log_n_nodes)
        sub_routine = XGate().control(len(control_state), ctrl_state=control_state)
        circuit.append(sub_routine, list(range(2 * self.log_n_nodes + 1)))
        circuit.barrier()

    def make_counter_register(self, n_toggles: int) -> QuantumRegister:
        """Prepare a register that holds the number of edges in the tree.

        Then later, subtract one from this value for every edge that is active, and
        apply a phase if all edges are active.
        """
        return QuantumRegister(2 * n_toggles - 1, "counter_reg")

    def make_circuit(
        self,
        failing_edge: tuple[Hashable, Hashable],
        load_flow_correctness: list[list[tuple[Hashable, Hashable]]],
        n_iter: int,
        n_toggles: int = 1,
    ) -> QuantumCircuit:
        """Create the registers and initializing N-1 circuit.

        Args:
            failing_edge: The edge that is currently failing i.e (1,4).
            load_flow_correctness: A list of edges that are load flow compliant
            n_toggles: Number of toggles possible.
            n_iter: Number of iterations

        Returns:
            The algorithm represented as a quantum circuit.

        """
        # Data sanitisation steps
        if not isinstance(failing_edge, tuple):
            error_msg = "Wrong type of failing edge given."
            raise TypeError(error_msg)
        if n_toggles < 1:
            error_msg = "No toggles are searched for, computation finished"
            raise ValueError(error_msg)

        # Encode networkx graph into circuit
        node_register = QuantumRegister(self.log_n_nodes, "v")
        edge_register = QuantumRegister(self.log_n_nodes, "e")
        circuit = QuantumCircuit(node_register, edge_register)
        encode_graph(circuit, self.graph, exact_superposition=self.exact_superposition)
        active_edges, inactive_edges = encode_network_edges(self.graph)

        if failing_edge not in active_edges:
            error_msg = "Failing edge is inactive."
            raise ValueError(error_msg)

        set_active_edges(circuit, self.graph)

        # Remove the failing edge as active and turn it off
        active_edges.remove(failing_edge)
        self._toggle_edge(failing_edge[0], failing_edge[1], circuit)
        self._toggle_edge(failing_edge[1], failing_edge[0], circuit)

        # Create the toggle and counter registers
        (
            active_toggle,
            n_active_qubits,
            active_edges_combinations,
        ) = self.make_active_toggle_register(n_toggles, active_edges)
        (
            inactive_toggle,
            n_inactive_qubits,
            inactive_edges_combinations,
        ) = self.make_inactive_toggle_register(n_toggles, inactive_edges)
        counter_register = self.make_counter_register(n_toggles)

        # Add the toggle and counter registers to the circuit and initialize them
        if active_toggle is not None:
            self.initialize_toggle_register(
                circuit, active_toggle, len(active_edges_combinations)
            )
        self.initialize_toggle_register(
            circuit, inactive_toggle, len(inactive_edges_combinations)
        )
        circuit.add_register(counter_register)

        oracle_factory = OracleFactory(
            self.n_nodes,
            n_toggles,
            n_active_qubits,
            n_inactive_qubits,
            active_edges,
            active_edges_combinations,
            inactive_edges_combinations,
        )
        toggles_gate = oracle_factory.make_toggles_gate(circuit.qubits)
        lf_gate = oracle_factory.make_load_flow_gate(
            circuit.qubits, load_flow_correctness
        )
        aa_gate = make_amplitude_amplification_gate(
            circuit.qubits,
            active_toggle,
            inactive_toggle,
            len(active_edges_combinations),
            len(inactive_edges_combinations),
            exact_superposition=self.exact_superposition,
        )
        for _ in range(n_iter):
            # Oracle
            circuit.append(toggles_gate, circuit.qubits)
            circuit.append(lf_gate, circuit.qubits)
            circuit.append(toggles_gate, circuit.qubits)

            # Amplitude amplification
            circuit.append(aa_gate, circuit.qubits)

        self.add_measurements(circuit, active_toggle, inactive_toggle)
        self._logg_message(
            inactive_edges_combinations,
            active_edges_combinations,
            n_inactive_qubits,
            n_active_qubits,
        )

        return circuit

    def add_measurements(
        self,
        circuit: QuantumCircuit,
        active_toggle: None | QuantumRegister,
        inactive_toggle: QuantumRegister,
    ) -> None:
        """Add measurement circuit segment.

        Args:
            circuit: the current quantum circuit to append the measurement segment to.
            active_toggle: the quantum regsiter possessing the active toggles.
            inactive_toggle: the quantum regsiter possessing the inactive toggles.
        """
        if active_toggle is not None:
            active_cregister = ClassicalRegister(
                size=len(active_toggle), name="active_meas"
            )
        inactive_cregister = ClassicalRegister(
            size=len(inactive_toggle), name="inactive_meas"
        )
        circuit.barrier()

        if active_toggle is not None:
            circuit.add_register(active_cregister)
            for qubit, cbit in zip(active_toggle, active_cregister):
                circuit.measure(qubit, cbit)

        circuit.add_register(inactive_cregister)
        for qubit, cbit in zip(inactive_toggle, inactive_cregister):
            circuit.measure(qubit, cbit)

    def _logg_message(
        self,
        inactive_edges_combinations: (
            list[tuple[tuple[Hashable, Hashable]]]
            | list[tuple[tuple[Hashable, Hashable], ...]]
        ),
        active_edges_combinations: (
            list[tuple[tuple[Hashable, Hashable]]]
            | list[tuple[tuple[Hashable, Hashable], ...]]
        ),
        n_inactive_qubits: int,
        n_active_qubits: int,
    ) -> None:
        if n_active_qubits > 0:
            LOGGER.info(
                "The counts of the first %s qubits correspond to the following active "
                "edges being toggled:",
                n_active_qubits,
            )
            LOGGER.info(active_edges_combinations)

        LOGGER.info(
            "The counts of the first %s qubits correspond to the following inactive "
            "edges being toggled:",
            n_inactive_qubits,
        )
        LOGGER.info(inactive_edges_combinations)

    def make_active_toggle_register(
        self, n_toggles: int, active_edges: list[tuple[Hashable, Hashable]]
    ) -> tuple[
        None | QuantumRegister, int, list[tuple[tuple[Hashable, Hashable], ...]]
    ]:
        """Generates register for the active toggle.

        Args:
            n_toggles: number of toggles.
            active_edges: list of active edges.

        Returns:
            Quantum register with the number of active qubits, the number of active
            qubits and the active edge combinations.
        """
        active_edges_combinations: list[tuple[tuple[Hashable, Hashable], ...]] = []
        n_toggles -= 1
        if n_toggles == 0:
            return None, 0, active_edges_combinations

        active_edges_combinations = list(combinations(active_edges, n_toggles))
        n_active_qubits = ceil(log2(len(active_edges_combinations)))
        if n_active_qubits == 0:
            n_active_qubits = 1

        return (
            QuantumRegister(n_active_qubits, "active_reg"),
            n_active_qubits,
            active_edges_combinations,
        )

    def make_inactive_toggle_register(
        self, n_toggles: int, inactive_edges: list[tuple[Hashable, Hashable]]
    ) -> tuple[QuantumRegister, int, list[tuple[tuple[Hashable, Hashable], ...]]]:
        """Generates register for the inactive toggle.

        Args:
            n_toggles: number of toggles.
            inactive_edges: list of inactive edges.

        Returns:
            Quantum register with the number of inactive qubits, the number of inactive
            qubits and the inactive edge combinations.
        """
        inactive_edges_combinations = list(combinations(inactive_edges, n_toggles))
        n_inactive_qubits = ceil(log2(len(inactive_edges_combinations)))
        if n_inactive_qubits == 0:
            n_inactive_qubits = 1

        return (
            QuantumRegister(n_inactive_qubits, "inactive_reg"),
            n_inactive_qubits,
            inactive_edges_combinations,
        )

    def initialize_toggle_register(
        self, circuit: QuantumCircuit, toggle_register: QuantumRegister, n_states: int
    ) -> None:
        """Add the `toggle_register` to the `circuit` and initialize it.

        Every qubit is initialized in perfect superposition. The circuit is manipulated
        inplace.

        Args:
            circuit: Circuit to add the register to.
            toggle_register: Register to add and bring in superposition.
            n_states: Number of states.
        """
        circuit.add_register(toggle_register)
        circuit.barrier()  # This barrier greatly influence the compilation time

        # Initialize the toggle register
        superposition_gate = make_superposition_gate(
            len(toggle_register), n_states, exact_superposition=self.exact_superposition
        )

        circuit.append(superposition_gate, toggle_register)
