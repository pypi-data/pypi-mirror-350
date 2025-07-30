"""This module contains the gates used in the n-1 problem."""

from tno.quantum.problems.n_minus_1.gate_based._gates.amplitude_amplification import (
    make_amplitude_amplification_gate,
)
from tno.quantum.problems.n_minus_1.gate_based._gates.oracle import OracleFactory
from tno.quantum.problems.n_minus_1.gate_based._gates.utils import (
    get_bitstring_rep,
    make_superposition_gate,
)

__all__ = [
    "OracleFactory",
    "get_bitstring_rep",
    "make_amplitude_amplification_gate",
    "make_superposition_gate",
]
