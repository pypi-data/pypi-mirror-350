"""This module contains tests for the ``NMOFactory`` class."""

from __future__ import annotations

from tno.quantum.optimization.qubo.components import QUBO
from tno.quantum.optimization.qubo.solvers import SimulatedAnnealingSolver
from tno.quantum.problems.n_minus_1.quantum_annealing._bqm_factories import NMOFactory
from tno.quantum.problems.n_minus_1.quantum_annealing.datasets import load_small_dataset


def test_n_minus_1_bqm() -> None:
    graph = load_small_dataset()
    bqm_factory = NMOFactory(graph, None, 6, 5, 5)
    bqm = bqm_factory.build_bqm()
    assert len(bqm.variables) == 292

    qubo = QUBO(bqm)
    solver = SimulatedAnnealingSolver()
    solver.solve(qubo)
