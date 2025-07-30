"""This module contains the ``LoadflowFactory`` class."""

from __future__ import annotations

from collections import deque
from collections.abc import Mapping
from copy import deepcopy
from typing import TYPE_CHECKING, cast, overload

import numpy as np
from dimod import BinaryQuadraticModel, SampleSet, quicksum
from numpy.typing import NDArray

from tno.quantum.problems.n_minus_1._utils import make_linear_system

if TYPE_CHECKING:
    import networkx as nx
    from networkx.classes.reportviews import EdgeView, NodeView


class LoadflowFactory:
    """:py:class:`~LoadflowFactory` class.

    This class is used for constructing Binary Quadratic Models which minimizes the
    residual of the linear equation describing the load flow constraints. If the
    minimum of the produced Binary Quadratic Models are small, then the loadflow
    constraints are met. They are false otherwise.
    """

    def __init__(self, graph: nx.Graph, K: int, L: int, M: int) -> None:
        """Init of the :py:class:`~LoadflowFactory`.

        Args:
            graph: Graph representing a power network.
            K: Number of auxiliary variables to use or encoding the real part of the
                potential.
            L: Number of auxiliary variables to use or encoding the imaginary part of
                the potential.
            M: Number of auxiliary variables to use for encoding the current.
        """
        self.graph = deepcopy(graph)
        self.K = K
        self.L = L
        self.M = M
        self._U_real = {n: self._encode_real_potential(n) for n in self._nodes}
        self._U_imag = {n: self._encode_imag_potential(n) for n in self._nodes}

    @property
    def _edges(self) -> EdgeView:
        """Edges of the graph."""
        return self.graph.edges

    @property
    def _nodes(self) -> NodeView:
        """Nodes of the graph."""
        return self.graph.nodes

    def build_bqm(self, p_extra: float = 1000) -> BinaryQuadraticModel:
        """Build the Loadflow ``BinaryQuadraticModel``.

        Args:
            p_extra: Extra power to add to each node for numerical stability.

        Returns:
            A ``BinaryQuadraticModel`` encoding the loadflow problem.
        """
        bqm_real_pot = self.build_real_potential_bqm(p_extra)
        bqm_imag_pot = self.build_imag_potential_bqm(p_extra)
        bqm_cur = self.build_current_bqm()
        return cast("BinaryQuadraticModel", bqm_real_pot + bqm_imag_pot + bqm_cur)

    def _encode_real_potential(self, n: int) -> BinaryQuadraticModel:
        """Encode the real part of the potential.

        Args:
            n: Node to encode.

        Returns:
            A fixed point representing the real part of the potential.
        """
        bqm = BinaryQuadraticModel("BINARY")
        if self._nodes[n]["type"] == "OS":
            bqm.offset = self._nodes[n]["U_min"]
            return bqm

        U_min = self._nodes[n]["U_min"]
        U_max = self._nodes[n]["U_max"]
        precision = (U_max - U_min) * 2 ** -(self.K + 1)
        bqm.offset = precision + U_min
        for k in range(1, self.K + 1):
            bqm.add_linear(f"u[r]_{n},{k}", precision * (2**k))
        return bqm

    def _encode_imag_potential(self, n: int) -> BinaryQuadraticModel:
        """Encode the imaginary part of the potential.

        Args:
            n: Node to encode.

        Returns:
            A fixed point representing the imaginary part of the potential.
        """
        bqm = BinaryQuadraticModel("BINARY")
        if self._nodes[n]["type"] == "OS":
            return bqm

        U_min = self._nodes[n]["U_min"]
        precision = U_min / 45 / (2**self.L)
        bqm.offset = -U_min / 45
        for l in range(1, self.L + 1):  # noqa E741
            bqm.add_linear(f"u[i]_{n},{l}", precision * (2**l))
        return bqm

    def _build_real_potential_penalty(
        self, n: int, p_extra: float = 1000
    ) -> BinaryQuadraticModel:
        """Build a penalty term for the real potential of node `n`."""
        load = self._nodes[n]["P_low"] + p_extra
        U_ref = self._nodes[n]["U_ref"]
        alpha = abs(load) ** 2 / (U_ref**2 * load.real)
        terms: deque[BinaryQuadraticModel] = deque()
        terms.append(alpha * self._U_real[n])
        for m in self.graph.adj[n]:
            if self._edges[n, m]["active"]:
                Z_nm = self._edges[n, m]["Z"]
                beta = (1 / Z_nm).real
                gamma = (1 / Z_nm).imag
                terms.append(
                    beta * (self._U_real[n] - self._U_real[m])
                    - gamma * (self._U_imag[n] - self._U_imag[m])
                )

        return cast("BinaryQuadraticModel", quicksum(terms) ** 2)

    def build_real_potential_bqm(self, p_extra: float = 1000) -> BinaryQuadraticModel:
        """Build a penalty term for the real potential of all nodes.

        Args:
            p_extra: Extra power to add to the nodes for numerical stability.

        Returns:
            The penalty term represented as a ``BinaryQuadraticModel``.
        """
        terms: deque[BinaryQuadraticModel] = deque()
        for n in self._nodes:
            # The potential is fixed at the OS, so we don't add it to the BQM
            if self._nodes[n]["type"] == "OS":
                continue
            terms.append(self._build_real_potential_penalty(n, p_extra))
        return cast("BinaryQuadraticModel", quicksum(terms))

    def _build_imag_potential_penalty(
        self, n: int, p_extra: float = 1000
    ) -> BinaryQuadraticModel:
        """Build a penalty term for the imaginary potential of node `n`."""
        load = self._nodes[n]["P_low"] + p_extra
        U_ref = self._nodes[n]["U_ref"]
        alpha = abs(load) ** 2 / (U_ref**2 * load.real)
        terms: deque[BinaryQuadraticModel] = deque()
        terms.append(alpha * self._U_imag[n])
        for m in self.graph.adj[n]:
            if self._edges[n, m]["active"]:
                Z_nm = self._edges[n, m]["Z"]
                beta = (1 / Z_nm).real
                gamma = (1 / Z_nm).imag
                terms.append(
                    beta * (self._U_imag[n] - self._U_imag[m])
                    + gamma * (self._U_real[n] - self._U_real[m])
                )

        return cast("BinaryQuadraticModel", quicksum(terms) ** 2)

    def build_imag_potential_bqm(self, p_extra: float = 1000) -> BinaryQuadraticModel:
        """Build a penalty term for the imaginary potential of all nodes.

        Args:
            p_extra: Extra power to add to the nodes for numerical stability.

        Returns:
            The penalty term represented as a ``BinaryQuadraticModel``.
        """
        terms: deque[BinaryQuadraticModel] = deque()
        for n in self._nodes:
            # The potential is fixed at the OS, so we don't add it to the BQM
            if self._nodes[n]["type"] == "OS":
                continue
            terms.append(self._build_imag_potential_penalty(n, p_extra))
        return cast("BinaryQuadraticModel", quicksum(terms))

    def _encode_current(self, edge: tuple[int, int]) -> BinaryQuadraticModel:
        """Encode the current for the given `edge`."""
        bqm = BinaryQuadraticModel("BINARY")
        I_max = self._edges[edge]["I_max"]
        edge_idx = self._edges[edge]["edge_idx"]
        precision = I_max * 2**-self.M
        bqm.offset = precision - I_max
        for m in range(1, self.M + 1):
            bqm.add_linear(f"i_{edge_idx},{m}", precision * 2**m)
        return bqm

    def _build_current_penalty(self, edge: tuple[int, int]) -> BinaryQuadraticModel:
        """Build a penalty term for the current of the given `edge`."""
        I = self._encode_current(edge)  # noqa: E741
        n, m = edge
        Z_nm = self._edges[edge]["Z"]
        beta = (1 / Z_nm).real
        gamma = (1 / Z_nm).imag

        bqm = (
            I
            + beta * (self._U_real[n] - self._U_real[m])
            - gamma * (self._U_imag[n] - self._U_imag[m])
        ) ** 2
        return cast("BinaryQuadraticModel", bqm)

    def build_current_bqm(self) -> BinaryQuadraticModel:
        """Build a penalty term for the current.

        The penalty term adds a penalty for violating the loadflow constraints.

        Returns:
            ``BinaryQuadraticModel`` containing the penalty.
        """
        terms: deque[BinaryQuadraticModel] = deque()
        for edge in self._edges:
            # Skip inactive edges and edges that always comply with the load flow
            if not self._edges[edge]["active"] or self.always_loadflow_compliant(edge):
                continue
            terms.append(self._build_current_penalty(edge))
        if terms:
            return cast("BinaryQuadraticModel", quicksum(terms))
        return BinaryQuadraticModel("BINARY")

    def always_loadflow_compliant(self, edge: tuple[int, int]) -> bool:
        """Check if the current on an edge is always load flow compliant.

        Args:
            edge: Edge to check.

        Returns:
            Boolean value stating wether the edge is always load flow compliant.
        """
        n, m = edge
        U_n_min = self._nodes[n]["U_min"]
        U_n_max = self._nodes[n]["U_max"]
        U_m_min = self._nodes[m]["U_min"]
        U_m_max = self._nodes[m]["U_max"]
        delta_U_max = max(U_n_max - U_m_min, U_m_max - U_n_min)
        beta = (1 / self._edges[edge]["Z"]).real
        gamma = -(1 / self._edges[edge]["Z"]).imag
        max_current = abs(beta * delta_U_max) + (U_n_min + U_m_min) * abs(gamma) / 45
        return bool(max_current <= self._edges[edge]["I_max"])

    def decode_sample(
        self, sample: Mapping[str, int] | SampleSet
    ) -> NDArray[np.complex128]:
        """Decode the given sample to get the potential at each node.

        Args:
            sample: Sample or ``SampleSet`` a retrieved from D-Wave.

        Returns:
            Array containing the solution for the given sample.
        """
        if isinstance(sample, Mapping):
            U = np.empty(len(self._nodes), dtype=complex)
            for n in self._nodes:
                real = self._U_real[n].energy(sample)
                imag = self._U_imag[n].energy(sample)
                U[n] = complex(real, imag)
            return U

        sampleset = sample
        U_sampleset = np.empty((len(self._nodes), len(sampleset)), dtype=complex)
        for i, sample_i in enumerate(sampleset):
            U_sampleset[:, i] = self.decode_sample(sample_i)
        return U_sampleset

    @overload
    def scaled_residual_norm(self, sample: Mapping[str, int]) -> np.float64: ...

    @overload
    def scaled_residual_norm(self, sample: SampleSet) -> NDArray[np.float64]: ...

    def scaled_residual_norm(
        self, sample: Mapping[str, int] | SampleSet
    ) -> np.float64 | NDArray[np.float64]:
        """Scaled residual norm the given sample(set) for the load flow equations.

        Args:
            sample: Sample or ``SampleSet`` a retrieved from D-Wave.

        Returns:
            Array containing the scaled residual norm for the given sample.
        """
        A, b = make_linear_system(self.graph)
        U = self.decode_sample(sample)[: len(b)]
        f = A @ U
        if isinstance(sample, Mapping):
            return cast("np.float64", np.linalg.norm(b - f) / np.linalg.norm(b))
        return cast(
            "NDArray[np.float64]", np.linalg.norm(b - f.T, axis=1) / np.linalg.norm(b)
        )

    @overload
    def relative_error(self, sample: Mapping[str, int]) -> np.float64: ...

    @overload
    def relative_error(self, sample: SampleSet) -> NDArray[np.float64]: ...

    def relative_error(
        self, sample: Mapping[str, int] | SampleSet
    ) -> np.float64 | NDArray[np.float64]:
        """Relative error of the voltages given by the sample.

        Args:
            sample: Sample or ``SampleSet`` a retrieved from D-Wave.

        Returns:
            Array containing the relative error for the given sample.
        """
        solution = np.linalg.solve(*make_linear_system(self.graph))
        U = self.decode_sample(sample)[: len(solution)]
        if isinstance(sample, Mapping):
            return cast(
                "np.float64", np.linalg.norm(solution - U) / np.linalg.norm(solution)
            )
        return cast(
            "NDArray[np.float64]",
            np.linalg.norm(solution - U.T, axis=1) / np.linalg.norm(solution),
        )
