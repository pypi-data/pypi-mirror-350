"""Provide tests."""

from typing import Any

import pytest

from auxi.chemistry.stoichiometry import ChemicalFormulaParser


def test_element_molar_masses(
    parser: ChemicalFormulaParser,
):
    """
    Test whether the parser correctly replicates element molar masses.
    """
    from auxi.chemistry.stoichiometry import (
        periodic_table,
    )

    for symbol, element in periodic_table.items():
        assert parser(symbol).molar_mass == element.molar_mass


def test_parse_simple_valid(
    parser: ChemicalFormulaParser,
    compounds: dict[str, dict[str, Any]],
    tolerance: float,
):
    """
    Test parsing of valid chemical formulae.
    """
    from auxi.chemistry.stoichiometry import ChemicalFormulaParseResult as Result

    for compound, data in compounds.items():
        mm: float = data["molar_mass"]
        stoich: dict[str, int] = data["stoichiometry"]
        ph: str = data["phase"]

        result: Result = parser(compound)
        assert result.molar_mass == pytest.approx(mm, tolerance)  # type: ignore
        assert result.stoichiometry == stoich
        assert result.phase is None
        assert result.charge == 0

        result: Result = parser(f"{compound}[{ph}]")
        assert result.molar_mass == pytest.approx(mm, tolerance)  # type: ignore
        assert result.stoichiometry == stoich
        assert result.phase == ph
        assert result.charge == 0


def test_parse_simple_invalid(
    parser: ChemicalFormulaParser,
):
    """
    Test parsing of valid chemical formulae.
    """
    formulae = [
        "(FeO)*(Fe2O3)",
        "CaO1,5",
    ]

    for formula in formulae:
        with pytest.raises(Exception):
            parser(formula)


def test_parse_charged_valid(
    parser: ChemicalFormulaParser,
    charged_compounds: dict[str, dict[str, Any]],
    tolerance: float,
):
    """
    Test parsing of valid chemical formulae with charges.
    """
    from auxi.chemistry.stoichiometry import ChemicalFormulaParseResult as Result

    for compound, data in charged_compounds.items():
        mm: float = data["molar_mass"]
        stoich: dict[str, int] = data["stoichiometry"]
        charge = data["charge"]
        ch: str = f"{data['charge']:+}"
        if abs(data["charge"]) == 1:
            ch = ch[:1]
        else:
            ch = ch[1:] + ch[:1]
        ph: str = data["phase"]

        result: Result = parser(f"{compound}[{ph}]")
        assert result.molar_mass == pytest.approx(mm, tolerance)  # type: ignore
        assert result.stoichiometry == stoich
        assert result.phase == ph
        assert result.charge == 0

        result: Result = parser(f"{compound}[{ch}][{ph}]")
        assert result.molar_mass == pytest.approx(mm, tolerance)  # type: ignore
        assert result.stoichiometry == stoich
        assert result.phase == ph
        assert result.charge == charge

        result: Result = parser(f"{compound}[{ch}]")
        assert result.molar_mass == pytest.approx(mm, tolerance)  # type: ignore
        assert result.stoichiometry == stoich
        assert result.phase is None
        assert result.charge == charge
