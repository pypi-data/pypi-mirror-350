import pytest
from qiskit.circuit import Gate

from tno.quantum.problems.n_minus_1.gate_based._gates.utils import (
    get_bitstring_rep,
    make_superposition_gate,
)


@pytest.mark.parametrize(
    ("integer", "num_bits", "expected"), [(1, 1, "1"), (1, 2, "10"), (3, 3, "110")]
)
def test_get_bitstring_rep(integer: int, num_bits: int, expected: str) -> None:
    assert get_bitstring_rep(integer, num_bits) == expected


def test_make_superposition_gate() -> None:
    assert isinstance(make_superposition_gate(2, 1, exact_superposition=False), Gate)
