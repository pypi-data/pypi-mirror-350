"""This module provides functions to load and save graphs in various formats."""

from tno.quantum.problems.n_minus_1.io._graphs_io import (
    load_gml,
    write_gml,
)

__all__ = ["load_gml", "write_gml"]
