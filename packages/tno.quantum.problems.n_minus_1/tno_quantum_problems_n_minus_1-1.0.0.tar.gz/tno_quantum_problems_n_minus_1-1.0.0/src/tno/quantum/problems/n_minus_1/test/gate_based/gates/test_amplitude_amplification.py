# EXAMPLE OF AMPLITUDE GATE SO SMALL THAT YOU CAN CHECK MATRIX
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister

from tno.quantum.problems.n_minus_1.gate_based._gates.amplitude_amplification import (
    make_amplitude_amplification_gate,
)


def test_make_amplitude_amplification_gate() -> None:
    main_register = QuantumRegister(1, "main")
    active_register = QuantumRegister(1, "active")
    inactive_register = QuantumRegister(1, "inactive")
    circuit = QuantumCircuit(main_register, active_register, inactive_register)

    gate = make_amplitude_amplification_gate(
        circuit.qubits,
        active_register,
        inactive_register,
        1,
        1,
        exact_superposition=False,
    )
    return_gate = np.array(
        [
            [-1, 0, 0, 0, 0, 0, 0, 0],
            [0, -1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 1],
        ]
    )
    np.testing.assert_allclose(gate.power(1).params[0], return_gate)
