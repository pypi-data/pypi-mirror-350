"""This module contains  tests for the ``LayersFactory`` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

import networkx as nx
import pytest
from dimod import BinaryQuadraticModel, SampleSet
from dwave.samplers import TreeDecompositionSolver

from tno.quantum.problems.n_minus_1.quantum_annealing._bqm_factories import (
    LayersFactory,
)

if TYPE_CHECKING:
    from tno.quantum.problems.n_minus_1.quantum_annealing import ResultsOverview


@pytest.fixture(name="small_graph")
def small_graph_fixture() -> nx.Graph:
    """Create the following graph:

       1=======3
      //\\    /
     //  \\  /
    //    \\/
    0------2
    Active edges have double bonds, inactive edges have single bonds.
    """
    graph = nx.Graph()
    graph.add_edge(0, 1, active=True)
    graph.add_edge(1, 2, active=True)
    graph.add_edge(1, 3, active=True)
    graph.add_edge(0, 2, active=False)
    graph.add_edge(2, 3, active=False)
    return graph


@pytest.fixture(name="bqm_factory")
def bqm_factory_fixture(small_graph: nx.graph) -> LayersFactory:
    return LayersFactory(small_graph)


class TestAttributes:
    def test_none_layers(self, small_graph: nx.Graph) -> None:
        bqm_factory = LayersFactory(small_graph, n_layers=None)
        assert nx.is_isomorphic(bqm_factory.graph, small_graph)
        assert bqm_factory.n_layers == 3

    @pytest.mark.parametrize("n_layers", range(1, 10))
    def test_int_layers(self, small_graph: nx.Graph, n_layers: int) -> None:
        bqm_factory = LayersFactory(small_graph, n_layers=n_layers)
        assert nx.is_isomorphic(bqm_factory.graph, small_graph)
        assert bqm_factory.n_layers == n_layers


class TestBQM:
    @pytest.fixture(name="bqm")
    def bqm_fixture(self, bqm_factory: LayersFactory) -> BinaryQuadraticModel:
        return bqm_factory.build_bqm(encoding="domain-wall")

    def test_instance(self, bqm: BinaryQuadraticModel) -> None:
        assert isinstance(bqm, BinaryQuadraticModel)

    def test_number_of_variables(self, bqm: BinaryQuadraticModel) -> None:
        assert len(bqm.variables) == 28

    @pytest.mark.parametrize("node", range(4))
    def test_node_variables(self, bqm: BinaryQuadraticModel, node: int) -> None:
        assert f"x{node}[1]" in bqm.variables
        assert f"x{node}[2]" in bqm.variables

    @pytest.mark.parametrize("edge", [(0, 1), (1, 2), (1, 3), (0, 2), (2, 3)])
    def test_edge_variables(
        self, bqm: BinaryQuadraticModel, edge: tuple[int, int]
    ) -> None:
        node_n, node_m = edge
        for i in range(1, 5):
            assert f"y{node_n},{node_m}[{i}]" in bqm.variables


class TestDecodedOutcome:
    @pytest.fixture(name="results")
    def results_fixture(self, bqm_factory: LayersFactory) -> ResultsOverview:
        bqm = bqm_factory.build_bqm(encoding="domain-wall")
        sampleset: SampleSet
        sampleset = TreeDecompositionSolver().sample(bqm, num_reads=25)  # type: ignore[no-untyped-call]
        return bqm_factory.decode_result(sampleset)

    def test_number_of_unique_results(self, results: ResultsOverview) -> None:
        assert len(results) == 8

    def test_expected_k(self, results: ResultsOverview) -> None:
        iterator = zip(results, [0, 2, 2, 2, 2, 4, 4, 4])
        for (result, _), expected_k in iterator:
            assert result.get_k() == expected_k

    def test_expected_count(self, results: ResultsOverview) -> None:
        iterator = zip(results, [4, 2, 2, 2, 2, 2, 4, 2])
        for (_, count), expected_count in iterator:
            assert count == expected_count
