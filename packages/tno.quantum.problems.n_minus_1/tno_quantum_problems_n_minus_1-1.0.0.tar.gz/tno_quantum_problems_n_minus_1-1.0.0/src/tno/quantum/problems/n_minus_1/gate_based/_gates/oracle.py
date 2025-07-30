"""Oracle factory for the n-1 problem.

This module contains the `OracleFactory` class, which is responsible for creating
the oracle for the n-1 problem.
"""

from __future__ import annotations

from collections.abc import Hashable, Iterable
from math import ceil, log2
from typing import TYPE_CHECKING

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library.standard_gates.x import MCXGate

from tno.quantum.problems.n_minus_1.gate_based._gates.utils import get_bitstring_rep

if TYPE_CHECKING:
    from qiskit.circuit import Gate, Qubit


class OracleFactory:
    """Factory class to create the oracle for the n-1 problem."""

    def __init__(  # noqa: PLR0913
        self,
        n_nodes: int,
        n_toggles: int,
        n_active_qubits: int,
        n_inactive_qubits: int,
        active_edges: list[tuple[Hashable, Hashable]],
        active_edges_comb: list[tuple[tuple[Hashable, Hashable], ...]],
        inactive_edges_comb: list[tuple[tuple[Hashable, Hashable], ...]],
    ) -> None:
        """Initialize the OracleFactory.

        Args:
            n_nodes: Number of nodes in the graph.
            n_toggles: Number of toggles allowed.
            n_active_qubits: Number of active qubits.
            n_inactive_qubits: Number of inactive qubits.
            active_edges: List of active edges in the graph.
            active_edges_comb: List of combinations of active edges.
            inactive_edges_comb: List of combinations of inactive edges.
        """
        self.n_nodes = n_nodes
        self.log_n_nodes = ceil(log2(self.n_nodes))
        self.n_toggles = n_toggles
        self.n_active_qubits = n_active_qubits
        self.n_inactive_qubits = n_inactive_qubits
        self.active_edges = active_edges
        self.active_edges_comb = active_edges_comb
        self.inactive_edges_comb = inactive_edges_comb

    def make_load_flow_gate(
        self,
        qubits: list[Qubit],
        load_flow_correctness: list[list[tuple[Hashable, Hashable]]],
    ) -> Gate:
        """Method to create gate utilized in load flow.

        Args:
            qubits: list of qubits necessary to create the gate.
            load_flow_correctness: list of correct load flow combinations.

        Returns:
            Load flow gate.
        """
        lf_circuit = QuantumCircuit(qubits, name="LF")

        for satisfying_tree in load_flow_correctness:
            if not self._is_correct_satisfying_tree(satisfying_tree):
                # No satisfying spanning tree with n_toggles switches off
                continue

            # Set the counter register
            self._set_counter_register(lf_circuit, satisfying_tree)

            # Apply phase
            if self.n_toggles == 1:
                lf_circuit.z(-1)
            else:
                lf_circuit.mcp(np.pi, list(range(-2 * self.n_toggles + 1, -1)), [-1])

            # Uncompute the counter register
            self._uncompute_counter_register(lf_circuit, satisfying_tree)

        return lf_circuit.to_gate()

    def _set_counter_register(
        self,
        lf_circuit: QuantumCircuit,
        satisfying_tree: list[tuple[Hashable, Hashable]],
    ) -> None:
        start_idx = 2 * self.log_n_nodes + 1
        for idx_active, temp_active_edges in enumerate(self.active_edges_comb):
            if not self._are_all_active_edges_turned_off(
                satisfying_tree, temp_active_edges
            ):
                continue
            for num, _ in enumerate(temp_active_edges):
                bit_rep_num = get_bitstring_rep(idx_active, self.n_active_qubits)
                sub_routine = MCXGate(self.n_active_qubits, ctrl_state=bit_rep_num)

                qargs = [*range(start_idx, start_idx + self.n_active_qubits), -num - 1]
                lf_circuit.append(sub_routine, qargs)

        start_idx = 2 * self.log_n_nodes + 1 + self.n_active_qubits
        for num_inactive, temp_inactive_edges in enumerate(self.inactive_edges_comb):
            if any(i_edge not in satisfying_tree for i_edge in temp_inactive_edges):
                # Continue if not all inactive edges are turned on in the tree
                continue
            for num, _ in enumerate(temp_inactive_edges):
                bit_rep_num = get_bitstring_rep(num_inactive, self.n_inactive_qubits)
                sub_routine = MCXGate(self.n_inactive_qubits, ctrl_state=bit_rep_num)
                qargs = [
                    *range(start_idx, start_idx + self.n_inactive_qubits),
                    -num - self.n_toggles,
                ]
                lf_circuit.append(sub_routine, qargs)

    def _uncompute_counter_register(
        self,
        lf_circuit: QuantumCircuit,
        satisfying_tree: list[tuple[Hashable, Hashable]],
    ) -> None:
        start_idx = 2 * self.log_n_nodes + 1 + self.n_active_qubits
        for num_inactive, temp_inactive_edges in enumerate(self.inactive_edges_comb):
            if any(i_edge not in satisfying_tree for i_edge in temp_inactive_edges):
                # If not all inactive edges are turned on in the satisfying tree
                # we should continue
                continue
            for num, _ in enumerate(temp_inactive_edges):
                bit_rep_num = get_bitstring_rep(num_inactive, self.n_inactive_qubits)
                sub_routine = MCXGate(self.n_inactive_qubits, ctrl_state=bit_rep_num)
                qargs = [
                    *range(start_idx, start_idx + self.n_inactive_qubits),
                    -num - self.n_toggles,
                ]
                lf_circuit.append(sub_routine, qargs)

        start_idx = 2 * self.log_n_nodes + 1
        for num_active, temp_active_edges in enumerate(self.active_edges_comb):
            if any(i_edge in satisfying_tree for i_edge in temp_active_edges):
                # Continue if not all active edges are turned off in the tree
                continue
            for num, _ in enumerate(temp_active_edges):
                bit_rep_num = get_bitstring_rep(num_active, self.n_active_qubits)
                sub_routine = MCXGate(self.n_active_qubits, ctrl_state=bit_rep_num)
                qargs = [*range(start_idx, start_idx + self.n_active_qubits), -num - 1]
                lf_circuit.append(sub_routine, qargs)

    def _is_correct_satisfying_tree(
        self, satisfying_tree: Iterable[tuple[Hashable, Hashable]]
    ) -> bool:
        count = sum(
            (edge in self.active_edges) or (edge[::-1] in self.active_edges)
            for edge in satisfying_tree
        )
        return count == self.n_nodes - self.n_toggles - 1

    @staticmethod
    def _are_all_active_edges_turned_off(
        satisfying_tree: list[tuple[Hashable, Hashable]],
        temp_active_edges: Iterable[tuple[Hashable, Hashable]],
    ) -> bool:
        return all(i_edge not in satisfying_tree for i_edge in temp_active_edges)

    def make_toggles_gate(self, qubits: list[Qubit]) -> Gate:
        """Toggles the edges for the oracle step."""
        toggles_circuit = QuantumCircuit(qubits)
        log_qubits = 2 * self.log_n_nodes
        if self.n_toggles > 1:
            control_target_qubits = list(range(log_qubits + 1 + self.n_active_qubits))
            control_target_qubits.append(control_target_qubits.pop(log_qubits))

            for i_toggle, active_toggles in enumerate(self.active_edges_comb):
                for vertex, neighbor in active_toggles:
                    bit_rep_neighbor = get_bitstring_rep(neighbor, self.log_n_nodes)
                    bit_rep_vertex = get_bitstring_rep(vertex, self.log_n_nodes)
                    bit_rep_toggle = get_bitstring_rep(i_toggle, self.n_active_qubits)

                    # neighbor - vertex
                    control_state = bit_rep_toggle + bit_rep_neighbor + bit_rep_vertex
                    sub_routine = MCXGate(len(control_state), ctrl_state=control_state)
                    toggles_circuit.append(sub_routine, control_target_qubits)

                    # vertex - neighbor
                    control_state = bit_rep_toggle + bit_rep_vertex + bit_rep_neighbor
                    sub_routine = MCXGate(len(control_state), ctrl_state=control_state)
                    toggles_circuit.append(sub_routine, control_target_qubits)

        control_target_qubits = list(
            range(log_qubits + 1 + self.n_active_qubits + self.n_inactive_qubits)
        )
        del control_target_qubits[log_qubits : log_qubits + 1 + self.n_active_qubits]
        control_target_qubits += [log_qubits]
        for i_toggle, inactive_toggles in enumerate(self.inactive_edges_comb):
            for vertex, neighbor in inactive_toggles:
                bit_rep_neighbor = get_bitstring_rep(neighbor, self.log_n_nodes)
                bit_rep_vertex = get_bitstring_rep(vertex, self.log_n_nodes)
                bit_rep_toggle = get_bitstring_rep(i_toggle, self.n_inactive_qubits)

                # neighbor - vertex
                control_state = bit_rep_toggle + bit_rep_neighbor + bit_rep_vertex
                sub_routine = MCXGate(len(control_state), ctrl_state=control_state)
                toggles_circuit.append(sub_routine, control_target_qubits)

                # vertex - neighbor
                control_state = bit_rep_toggle + bit_rep_vertex + bit_rep_neighbor
                sub_routine = MCXGate(len(control_state), ctrl_state=control_state)
                toggles_circuit.append(sub_routine, control_target_qubits)

        return toggles_circuit.to_gate()
