"""This module contains utility functions for the N-Minus-1 (nmo) BQM factories."""

from __future__ import annotations

from functools import partial
from typing import cast

from dimod import Binary, BinaryQuadraticModel

from tno.quantum.utils.validation import check_string


def create_discrete_variable(
    label: str, n_choices: int, encoding: str
) -> tuple[list[BinaryQuadraticModel], BinaryQuadraticModel]:
    """Create a discrete variable and penalty term.

    Args:
        label: Label of the discrete variables.
        n_choices: Number of choices the discrete variable should have.
        encoding: Choose 'domain-wall' or 'one-hot'

    Return:
        Tuple where the first argument is a list of ``BinaryQuadraticModels``
        representing the discrete choices and the second argument is a penalty term
        to enforce the behavior of the discrete variables.
    """
    bqm = BinaryQuadraticModel("BINARY")
    encoding = check_string(encoding, "encoding", lower=True).strip()
    variable = partial(_make_var, label)
    if encoding == "domain-wall":
        variables = [
            variable(1),
            *(variable(i) - variable(i - 1) for i in range(2, n_choices)),
            1 - variable(n_choices - 1),
        ]

        # Build the penalty term
        for i in range(1, n_choices - 1):
            bqm.add_linear(f"{label}[{i}]", 1)
            bqm.add_quadratic(f"{label}[{i}]", f"{label}[{i + 1}]", -1)

    elif encoding == "one-hot":
        variables = list(map(variable, range(n_choices)))

        # Build the penalty term
        bqm.offset -= 1
        for i in range(n_choices):
            bqm.add_linear(f"{label}[{i}]", -1)
            for j in range(i + 1, n_choices):
                bqm.add_quadratic(f"{label}[{i}]", f"{label}[{j}]", 2)
    else:
        error_msg = "Encoding should be 'domain-wall' or 'one-hot'"
        raise ValueError(error_msg)

    return variables, bqm  # type: ignore[return-value]


def link_variables(link_label: str, bqm: BinaryQuadraticModel) -> BinaryQuadraticModel:
    """Links the variable `link_label` to the variables of `bqm`.

    Args:
        link_label: String containing a label.
        bqm: BQM to link the variables of.

    Returns:
        New BQM where each 'variable' in `bqm` is replaced with
        'link_label*variable'
    """
    new_labels = {var: f"{link_label}*{var}" for var in bqm.variables}
    return cast(
        "BinaryQuadraticModel",
        bqm.relabel_variables(new_labels, inplace=False),  # type: ignore[no-untyped-call]
    )


def build_auxvar_bqm(bqm: BinaryQuadraticModel) -> BinaryQuadraticModel:
    """Find auxiliary variables in `bqm` and create bqm to enforce the behavior.

    Args:
        bqm: ``BinaryQuadraticModel`` with auxiliary variables in the form
            'arg1*arg2'.

    Returns:
        BQM with a penalty function to enforce the behavior of the auxiliary
        variables.
    """
    auxvar_bqm = BinaryQuadraticModel("BINARY")
    for var in bqm.variables:
        if isinstance(var, str) and "*" in var:
            aux_var = var
            var1, var2 = aux_var.split("*")
            auxvar_bqm.add_quadratic(var1, var2, 1)
            auxvar_bqm.add_quadratic(aux_var, var2, -2)
            auxvar_bqm.add_quadratic(var1, aux_var, -2)
            auxvar_bqm.add_linear(aux_var, 3)
    return auxvar_bqm


def _make_var(label: str, i: int) -> BinaryQuadraticModel:
    """Create a variable with the given label and index.

    Args:
        label: Label of the variable.
        i: Index of the variable.

    Returns:
        The created variable.
    """
    return cast("BinaryQuadraticModel", Binary(f"{label}[{i}]"))
