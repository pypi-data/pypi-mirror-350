"""This module contains tests for the ``LoadflowFactory``."""

from __future__ import annotations

from math import isclose

import networkx as nx
import pytest
from dimod import BinaryQuadraticModel

from tno.quantum.optimization.qubo.components import QUBO
from tno.quantum.optimization.qubo.solvers import TreeDecompositionSolver
from tno.quantum.problems.n_minus_1.quantum_annealing._bqm_factories import (
    LoadflowFactory,
)


@pytest.fixture(name="small_graph")
def small_graph_fixture() -> nx.Graph:
    graph = nx.Graph()
    graph.add_node(0, type="MSR", U_min=9800, U_max=11000)
    return graph


@pytest.fixture(name="bqm_factory")
def bqm_factory_fixture(small_graph: nx.Graph) -> LoadflowFactory:
    return LoadflowFactory(small_graph, 0, 0, 0)


@pytest.mark.parametrize("K", range(2, 8))
def test_encode_real_potential(bqm_factory: LoadflowFactory, K: int) -> None:
    bqm_factory.K = K
    pot_real_bqm = bqm_factory._encode_real_potential(0)
    sample_all_0 = dict.fromkeys(pot_real_bqm.variables, 0)
    sample_all_1 = dict.fromkeys(pot_real_bqm.variables, 1)
    precision = 1200 * 2 ** -(K + 1)
    assert isclose(pot_real_bqm.energy(sample_all_0), 9800 + precision)
    assert isclose(pot_real_bqm.energy(sample_all_1), 11000 - precision)


@pytest.mark.parametrize("L", range(2, 8))
def test_imag_real_potential(bqm_factory: LoadflowFactory, L: int) -> None:
    bqm_factory.L = L
    pot_imag_bqm = bqm_factory._encode_imag_potential(0)
    sample_all_0 = dict.fromkeys(pot_imag_bqm.variables, 0)
    sample_all_1 = dict.fromkeys(pot_imag_bqm.variables, 1)
    precision = 9800 / 45 * 2**-L
    assert isclose(pot_imag_bqm.energy(sample_all_0), -9800 / 45)
    assert isclose(pot_imag_bqm.energy(sample_all_1), 9800 / 45 - 2 * precision)


def test_sampleset_result() -> None:
    graph = nx.Graph()
    graph.add_node(0, type="MSR", U_min=0, U_max=1, P_low=1, U_ref=1)
    graph.add_node(1, type="OS", U_min=1, U_max=1, P_low=1, U_ref=1)
    graph.add_edge(0, 1, active=True, Z=1, I_max=1, edge_idx=0)

    bqm_factory = LoadflowFactory(graph, 2, 2, 2)
    bqm = bqm_factory.build_bqm(p_extra=0)
    assert isinstance(bqm, BinaryQuadraticModel)

    qubo = QUBO(bqm)
    solver = TreeDecompositionSolver()
    result = solver.solve(qubo)
    assert result.best_value == 1 / 16
