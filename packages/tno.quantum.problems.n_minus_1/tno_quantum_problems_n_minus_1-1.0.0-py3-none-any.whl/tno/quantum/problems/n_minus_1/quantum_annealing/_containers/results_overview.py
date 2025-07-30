"""This module contains the ``ResultsOverview`` class."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterator
from typing import TYPE_CHECKING

from tno.quantum.problems.n_minus_1.quantum_annealing._containers.decoded_result import (  # noqa: E501
    DecodedResult,
)

if TYPE_CHECKING:
    from typing import Self


class ResultsOverview:
    """ResultsOverview.

    The :py:class:`~ResultsOverview` class is a collection of
    :py:class:`~tno.quantum.problems.n_minus_1.quantum_annealing.DecodedResult`.
    """

    def __init__(self) -> None:
        """Init of the :py:class:`~ResultsOverview` class."""
        self.results: Counter[DecodedResult] = Counter()

    def add_result(self, result: DecodedResult, count: int = 1) -> Self:
        """Add a result to the overview.

        Args:
            result: Result to add to the overview.
            count: Number of times the result was seen. Default is 1.

        Returns:
            Self.
        """
        self.results[result] += count
        return self

    def __repr__(self) -> str:
        """Make a string representation of the :py:class:`~ResultsOverview`."""
        sorted_results = sorted(self.results, key=DecodedResult.get_k)
        txt = f"{'k':^3}|{'count':^7}|{'turned on':^25}|{'turned off':^25}\n"
        txt += f"{'-' * 3}+{'-' * 7}+{'-' * 25}+{'-' * 25}\n"
        for result in sorted_results:
            k = result.get_k()
            count = self.results[result]
            turned_on = str(result.turned_on)[1:-1]
            turned_off = str(result.turned_off)[1:-1]
            txt += f"{k:^3}|{count:^7}|{turned_on:^25}|{turned_off:^25}\n"
        return txt

    def __iter__(self) -> Iterator[tuple[DecodedResult, int]]:
        """Iterate over the results and counts, starting with the smallest k."""
        sorted_results = sorted(self.results, key=DecodedResult.get_k)
        return ((result, self.results[result]) for result in sorted_results)

    def __len__(self) -> int:
        """Number of unique results in the overview."""
        return len(self.results)
