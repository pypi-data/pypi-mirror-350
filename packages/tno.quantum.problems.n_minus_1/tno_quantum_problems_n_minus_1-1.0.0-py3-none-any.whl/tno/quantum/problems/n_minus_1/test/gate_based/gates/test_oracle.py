"""This module contains tests for the ``OracleFactory``."""

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import ZGate

from tno.quantum.problems.n_minus_1.gate_based._gates.oracle import OracleFactory


def test_oracle_factory() -> None:
    main_register = QuantumRegister(3, "main")
    circuit = QuantumCircuit(main_register)
    oracle = OracleFactory(3, 1, 2, 1, [(1, 2)], [((0, 1), (1, 2))], [((0, 2),)])
    gate = oracle.make_load_flow_gate(circuit.qubits, [[(1, 2)]])
    expected_gate = np.kron(np.rint(ZGate("").to_matrix()), np.identity(4))

    np.testing.assert_array_equal(gate.power(1).params[0], expected_gate)
