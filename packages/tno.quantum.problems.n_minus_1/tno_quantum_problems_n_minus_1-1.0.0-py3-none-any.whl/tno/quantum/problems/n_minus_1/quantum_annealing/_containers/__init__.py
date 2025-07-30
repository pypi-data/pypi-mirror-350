"""Data containers used in the quantum annealing implementation.

More specifically, this package contains :py:class:`~DecodedResult` and
:py:class:`~ResultsOverview`.
The :py:class:`~DecodedResult` stores results decoded from a sample of a sampleset.
:py:class:`~ResultsOverview` is a collection of :py:class:`~DecodedResult`.
"""

# ruff: noqa: E501

from tno.quantum.problems.n_minus_1.quantum_annealing._containers.decoded_result import (
    DecodedResult,
)
from tno.quantum.problems.n_minus_1.quantum_annealing._containers.results_overview import (
    ResultsOverview,
)

__all__ = ["DecodedResult", "ResultsOverview"]
