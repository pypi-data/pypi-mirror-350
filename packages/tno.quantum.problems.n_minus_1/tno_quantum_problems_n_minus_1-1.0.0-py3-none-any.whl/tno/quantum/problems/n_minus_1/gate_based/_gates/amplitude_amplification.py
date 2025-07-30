"""This module contains the amplitude amplification circuit segment."""

from __future__ import annotations

from itertools import chain

import numpy as np
from qiskit.circuit import Gate, QuantumCircuit, QuantumRegister, Qubit

from tno.quantum.problems.n_minus_1.gate_based._gates.utils import (
    make_superposition_gate,
)


def make_amplitude_amplification_gate(  # noqa: PLR0913
    qubits: list[Qubit],
    active_toggle: QuantumRegister,
    inactive_toggle: QuantumRegister,
    n_active_edges_combinations: int,
    n_inactive_edges_combinations: int,
    *,
    exact_superposition: bool,
) -> Gate:
    """Creates the amplitude amplification circuit segment.

    Args:
        qubits: list of qubits.
        active_toggle: the quantum regsiter possessing the active toggles.
        inactive_toggle: the quantum regsiter possessing the inactive toggles.
        n_active_edges_combinations: number of active edge combinations.
        n_inactive_edges_combinations: number of inactive edge combinations.
        exact_superposition: whether or not exact superposition is shown.

    Returns:
        Gate object with circuit of the amplitude amplification.
    """
    circuit = QuantumCircuit(qubits)
    if active_toggle is None:
        target_qubits = inactive_toggle
    else:
        target_qubits = list(chain(active_toggle, inactive_toggle))

    if active_toggle is not None:
        superposition_gate_active = make_superposition_gate(
            len(active_toggle),
            n_active_edges_combinations,
            exact_superposition=exact_superposition,
        )
        circuit.append(superposition_gate_active.inverse(), active_toggle)

    superposition_gate_inactive = make_superposition_gate(
        len(inactive_toggle),
        n_inactive_edges_combinations,
        exact_superposition=exact_superposition,
    )
    circuit.append(superposition_gate_inactive.inverse(), inactive_toggle)

    circuit.x(target_qubits)
    if len(target_qubits) == 1:
        circuit.z(target_qubits[0])
    else:
        circuit.mcp(np.pi, target_qubits[:-1], target_qubits[-1])
    circuit.x(target_qubits)

    circuit.append(superposition_gate_inactive, inactive_toggle)
    if active_toggle is not None:
        circuit.append(superposition_gate_active, active_toggle)

    return circuit.to_gate()
