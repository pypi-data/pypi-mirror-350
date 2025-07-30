"""The ``n_minus_1`` package provides quantum computing solvers for the n-1 problem.

The N-1 problem arises in graph theory as a reconfigurational mathematical challenge.
When a cut is introduced, or an edge is removed, in a given graph of nodes and edges,
the N-1 problem seeks the most efficient method of reconfiguring the nodes using the
fewest possible edges.

Example:
    This script below uses annealing based optimization to solve the N-1 problem for the
    small dataset (:py:func:`~tno.quantum.problems.n_minus_1.quantum_annealing.datasets.load_small_dataset`)
    with some additional edits.

    Edge (1,4) is removed (this is the "broken" edge). Furthermore, the I_max attribute
    of Edge (1,5) is set to 0. In this way, there is exactly one solution: Turning edge
    (0,1) on, while all other edges are not toggled.

    .. code-block:: python

        from tno.quantum.problems.n_minus_1 import QABasedNMinusOneSolver
        from tno.quantum.problems.n_minus_1.quantum_annealing.datasets import load_small_dataset

        graph = load_small_dataset()
        graph.edges[1, 5]["I_max"] = 0
        failing_edge = (1, 4)
        solver_config = {
            "name": "simulated_annealing_solver",
            "options": {
                "num_reads": 100,
                "num_sweeps": 100000,
                "num_sweeps_per_beta": 100,
                "seed": 2024,
            },
        }

        solver = QABasedNMinusOneSolver(graph, failing_edge)
        results = solver.run(solver_config=solver_config)

        print(results)

    This prints the following result:

    .. code-block:: console

        k | count |        turned on        |       turned off
        ---+-------+-------------------------+-------------------------
        1 |   4   |         (1, 5)          |
        1 |   1   |         (0, 1)          |
        3 |   1   |     (0, 1), (1, 5)      |         (5, 6)


Example:
    This script below uses the gate grover algorithm to solve the N-1 problem for a
    custom dataset.

    .. code-block:: python

        import networkx as nx
        from qiskit.visualization import plot_distribution

        from tno.quantum.problems.n_minus_1 import GateBasedNMinusOneSolver

        # Create a graph with edges: 0-1, 0-2, 0-3, 1-4, 2-4, 2-3, 3-4, 1-2, 0-5, 4-5.
        graph = nx.Graph()
        active_edges = [(0, 1), (0, 2), (0, 3), (1, 4), (0, 5)]
        inactive_edges = [(2, 4), (2, 3), (3, 4), (1, 2), (4, 5)]
        for node_n, node_m in active_edges:
            graph.add_edge(node_n, node_m, weight=1)
        for node_n, node_m in inactive_edges:
            graph.add_edge(node_n, node_m, weight=-1)

        load_flow_correctness = [[(0, 2), (0, 1), (0, 3), (4, 5), (3, 4)]]

        # Run the algorithm
        solver = GateBasedNMinusOneSolver(
            graph, (1, 4), load_flow_correctness, n_iter=8, n_toggles=2
        )
        executed_run = solver.run()

        # Plot the results
        counts = executed_run.result().results[0].data.counts
        fig = plot_distribution(
            counts,
            title="Failed Edge (1,4) - Correct Toggles (0,5), (3,4), or (4,5)",
            bar_labels=True,
        )
        fig.savefig("grover_n-1.png")
"""  # noqa: E501

from tno.quantum.problems.n_minus_1.gate_based import GateBasedNMinusOneSolver
from tno.quantum.problems.n_minus_1.quantum_annealing import QABasedNMinusOneSolver

__all__ = ["GateBasedNMinusOneSolver", "QABasedNMinusOneSolver"]

__version__ = "1.0.0"
