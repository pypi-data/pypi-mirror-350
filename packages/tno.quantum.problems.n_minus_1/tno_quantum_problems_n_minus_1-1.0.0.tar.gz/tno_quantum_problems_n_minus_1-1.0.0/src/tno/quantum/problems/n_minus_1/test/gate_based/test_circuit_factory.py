"""This module contains tests for ``CircuitFactory``."""

import pytest
import qiskit
from qiskit_aer import Aer

from tno.quantum.problems.n_minus_1.gate_based._circuit_factory import CircuitFactory
from tno.quantum.problems.n_minus_1.test.gate_based.make_test_graph import (
    make_test_graph,
)


@pytest.fixture(name="circuit_factory")
def circuit_factory_fixture() -> CircuitFactory:
    graph = make_test_graph()
    return CircuitFactory(graph, exact_superposition=False)


@pytest.fixture(name="test_circuit")
def build_circuit(circuit_factory: CircuitFactory) -> qiskit.QuantumCircuit:
    load_flow_correctness = [[(0, 1), (1, 2), (0, 3), (1, 4), (0, 5)]]
    return circuit_factory.make_circuit(
        (0, 2),
        load_flow_correctness,  # type: ignore[arg-type]
        1,
    )


def test_circuit_depth(test_circuit: qiskit.QuantumCircuit) -> None:
    assert test_circuit.depth() == 19


def test_num_qubits(test_circuit: qiskit.QuantumCircuit) -> None:
    assert test_circuit.num_qubits == 11


def test_num_clbits(test_circuit: qiskit.QuantumCircuit) -> None:
    assert test_circuit.num_clbits == 3


def test_circuit_factory(test_circuit: qiskit.QuantumCircuit) -> None:
    backend = Aer.get_backend("aer_simulator")
    transpiled_circuit = qiskit.transpile(
        test_circuit.reverse_bits(),
        backend=backend,
    )
    executed_run = backend.run(transpiled_circuit, shots=10000)
    counts_data = executed_run.result().results[0].data.counts
    assert max(zip(counts_data.values(), counts_data.keys()))[1] == "0x0"
