"""Test the QA N-Minus1 solver for the following graph:

Graph:
OS
3=======0
//     /
//     /
//     /
2------1
Active edges have double bonds, inactive edges have single bonds.
"""

import networkx as nx

from tno.quantum.problems.n_minus_1 import QABasedNMinusOneSolver


def test_qa_based_n_minus_one_solver() -> None:
    factory_kwargs = {"n_layers": None, "K": 2, "L": 1, "M": 2}
    qubo_kwargs = {
        "penalty_depth": 15,
        "penalty_connectivity": 6,
        "penalty_loadflow": 10,
        "penalty_auxvar": 30,
        "p_extra": 0,
    }

    graph = nx.Graph()

    graph.add_node(0, type="MSR", U_ref=1, P_low=1, P_high=1, U_min=1, U_max=9)
    graph.add_node(1, type="MSR", U_ref=1, P_low=1, P_high=1, U_min=1, U_max=9)
    graph.add_node(2, type="MSR", U_ref=1, P_low=1, P_high=1, U_min=4, U_max=12)
    graph.add_node(3, type="OS", U_ref=1, P_low=1, P_high=1, U_min=10, U_max=10)

    graph.add_edge(3, 0, active=True, edge_idx=0, Z=complex(1), I_max=20)
    graph.add_edge(3, 2, active=True, edge_idx=1, Z=complex(1), I_max=16)
    graph.add_edge(0, 1, active=False, edge_idx=2, Z=complex(1), I_max=8)
    graph.add_edge(1, 2, active=False, edge_idx=3, Z=complex(1), I_max=0)
    graph.add_edge(3, 1, active=True, edge_idx=4, Z=complex(1), I_max=8)  # Failing Edge

    qubo_solver = {"name": "simulated_annealing_solver", "options": {}}
    solver = QABasedNMinusOneSolver(graph, (1, 3))
    solver.run(factory_kwargs, qubo_kwargs, qubo_solver)
