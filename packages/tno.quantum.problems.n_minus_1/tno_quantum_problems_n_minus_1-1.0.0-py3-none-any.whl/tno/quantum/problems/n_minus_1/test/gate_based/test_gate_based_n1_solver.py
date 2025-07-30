"""This module contains test function for the n1gb package"""

from tno.quantum.problems.n_minus_1.gate_based._gate_based_n1_solver import (
    GateBasedNMinusOneSolver,
)
from tno.quantum.problems.n_minus_1.test.gate_based.make_test_graph import (
    make_test_graph,
)


def test_gate_based_n1_solver() -> None:
    graph = make_test_graph()
    load_flow_correctness = [[(0, 1), (1, 2), (0, 3), (1, 4), (0, 5)]]
    test_case = GateBasedNMinusOneSolver(graph, (0, 2), load_flow_correctness)

    job = test_case.run()
    counts_data = job.result().results[0].data.counts
    assert max(zip(counts_data.values(), counts_data.keys()))[1] == "0x0"
