"""Module containing utility functions."""

from __future__ import annotations

from collections.abc import Hashable
from math import ceil, log2

import numpy as np
from qiskit.circuit import Gate, QuantumCircuit
from qiskit.circuit.library.generalized_gates import MCMT
from qiskit.circuit.library.standard_gates import RYGate


def make_superposition_gate(
    num_qubits: int, num_states: int, *, exact_superposition: bool
) -> Gate:
    """Create a superposition gate for a given number of qubits and states.

    The superposition gate creates a uniform superposition of the given number of
    states over the qubits. The gate is constructed using a combination of Hadamard
    gates and controlled rotations.

    Args:
        num_qubits: Number of qubits to use for the superposition.
        num_states: Number of states to create a superposition of.
        exact_superposition: Whether to create an exact superposition or not.

    Returns:
        A Qiskit Gate object representing the superposition circuit.
    """
    superposition_circuit = QuantumCircuit(num_qubits, name="superposition")

    # In case of few number of states, some qubits are deterministically in the
    # zero-state.
    start_qubit = num_qubits - ceil(log2(num_states))

    rem_states = num_states - 2 ** (num_qubits - start_qubit - 1)
    if num_states == 2 ** (num_qubits - start_qubit) or not exact_superposition:
        for i_qubit in range(start_qubit, num_qubits):
            superposition_circuit.h(i_qubit)
        return superposition_circuit.to_gate()

    theta = -2 * np.arcsin(np.sqrt(rem_states / num_states))
    superposition_circuit.ry(theta, start_qubit)

    i_qubit = start_qubit + 1

    ## For the |0> part, a uniform superposition is needed for the rest
    if i_qubit < num_qubits:
        # num_qubits - i_qubit: the number of repetitions of H-gate
        ch_gate = MCMT(
            RYGate(np.pi / 2), (i_qubit - start_qubit), num_qubits - i_qubit
        )  # Note, Ry(pi/2)|0> = H|0>
        superposition_circuit.x(i_qubit - 1)
        superposition_circuit.append(ch_gate, list(range(start_qubit, num_qubits)))
        superposition_circuit.x(i_qubit - 1)

    ## For the |1> part, a weighted superposition is needed
    if rem_states > 1:
        controlled_sub_gate = make_superposition_gate(
            num_qubits - i_qubit, rem_states, exact_superposition=False
        )  # Decompose is necessary, else Qiskit throws error
        superposition_circuit.append(
            controlled_sub_gate.control(i_qubit),
            list(range(start_qubit, num_qubits)),
        )
    return superposition_circuit.to_gate()


def get_bitstring_rep(integer: int | Hashable, num_bits: int) -> str:
    """Convert integer to bit string.

    Args:
        integer: Integer value to encode.
        num_bits: Number of bits to use.

    Returns:
        A string containing the binary representation of the `integer` using `num_bits`.
    """
    return "{0:0{x}b}".format(integer, x=num_bits)[::-1]
