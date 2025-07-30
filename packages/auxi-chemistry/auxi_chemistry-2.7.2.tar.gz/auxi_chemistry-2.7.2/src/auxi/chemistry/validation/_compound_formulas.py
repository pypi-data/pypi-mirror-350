from typing import Annotated

from pydantic import AfterValidator, ValidationInfo

from ..stoichiometry import is_compound


# region re-usable checks


def check_compound_formula(
    v: str,
    field_name: str | None,
) -> str:
    fn = "" if field_name is None else f"{field_name} "

    result = v.strip()

    if not is_compound(result):
        raise ValueError(f"{fn} must be a valid compound formula.")

    return result


def check_compound_formula_list(
    v: list[str],
    field_name: str | None,
) -> list[str]:
    return [check_compound_formula(vv, field_name) for vv in v]


def check_compound_formula_list_n(
    v: list[str],
    field_name: str | None,
    n: int,
) -> list[str]:
    fn = "" if field_name is None else f"{field_name} "

    if len(v) != n:
        raise ValueError(f"{fn} must contain exactly {n} valid compound formulas.")

    result = check_compound_formula_list(v, fn)

    return result


# endregion re-usable checks


def str_is_compound_formula(
    v: str,
    info: ValidationInfo,
) -> str:
    return check_compound_formula(v, info.field_name)


strCompoundFormula = Annotated[
    str,
    AfterValidator(str_is_compound_formula),
]


def list_is_compound_formulas(
    v: list[str],
    info: ValidationInfo,
) -> list[str]:
    return check_compound_formula_list(v, info.field_name)


listCompoundFormulas = Annotated[
    list[str],
    AfterValidator(list_is_compound_formulas),
]


def list_is_compound_formulas_binary(
    v: list[str],
    info: ValidationInfo,
) -> list[str]:
    return check_compound_formula_list_n(v, info.field_name, 2)


listCompoundFormulasBinary = Annotated[
    list[str],
    AfterValidator(list_is_compound_formulas_binary),
]
