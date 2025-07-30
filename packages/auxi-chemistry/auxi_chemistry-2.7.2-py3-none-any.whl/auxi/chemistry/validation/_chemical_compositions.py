from typing import Annotated

from pydantic import AfterValidator, ValidationInfo

from auxi.core.validation import check_fraction_list

from ._compound_formulas import check_compound_formula_list


# region re-usable checks


def check_chemical_composition(
    v: dict[str, float],
    field_name: str | None,
) -> dict[str, float]:
    fn = "" if field_name is None else f"{field_name} "

    check_compound_formula_list(list(v.keys()), fn)
    check_fraction_list(list(v.values()), fn)

    return v


def check_chemical_composition_n(
    v: dict[str, float],
    field_name: str | None,
    n: int,
) -> dict[str, float]:
    fn = "" if field_name is None else f"{field_name} "

    if len(v) != n:
        raise ValueError(f"{fn} must contain exactly {n} valid compound formulas.")

    check_compound_formula_list(list(v.keys()), fn)
    check_fraction_list(list(v.values()), fn)

    return v


# endregion re-usable checks


def dict_is_chemical_composition(
    v: dict[str, float],
    info: ValidationInfo,
) -> dict[str, float]:
    return check_chemical_composition(v, info.field_name)


dictChemicalComposition = Annotated[
    dict[str, float],
    AfterValidator(dict_is_chemical_composition),
]


def dict_is_chemical_composition_binary(
    v: dict[str, float],
    info: ValidationInfo,
) -> dict[str, float]:
    return check_chemical_composition_n(v, info.field_name, 2)


dictChemicalCompositionBinary = Annotated[
    dict[str, float],
    AfterValidator(dict_is_chemical_composition),
]
