"""Provide test fixtures."""

from typing import Any

import pytest

from auxi.chemistry.stoichiometry import ChemicalFormulaParser


@pytest.fixture()
def tolerance() -> float:
    """Provide floating point comparison tolerance."""
    return 1.0e-12


@pytest.fixture()
def compounds() -> dict[str, dict[str, Any]]:
    """Provide valid compounds."""
    return {
        "H2O": {
            "molar_mass": 18.01528,
            "stoichiometry": {"H": 2, "O": 1},
            "phase": "s",
        },
        "H2SO4": {
            "molar_mass": 98.07948,
            "stoichiometry": {"H": 2, "S": 1, "O": 4},
            "phase": "l",
        },
        "FeO(OH)": {
            "molar_mass": 88.85174,
            "stoichiometry": {"Fe": 1, "O": 2, "H": 1},
            "phase": "s1",
        },
        "Mg5(CO3)4(OH)2.4H2O": {
            "molar_mass": 467.6364,
            "stoichiometry": {"Mg": 5, "C": 4, "O": 18, "H": 10},
            "phase": "s",
        },
        "CaO.H2O": {
            "molar_mass": 74.09268,
            "stoichiometry": {"Ca": 1, "O": 2, "H": 2},
            "phase": "s",
        },
    }


@pytest.fixture()
def charged_compounds() -> dict[str, dict[str, Any]]:
    """Provide valid charged compounds."""
    return {
        "H": {
            "molar_mass": 1.00794,
            "stoichiometry": {"H": 1},
            "charge": 1,
            "phase": "aq",
        },
        "OH": {
            "molar_mass": 17.00734,
            "stoichiometry": {"O": 1, "H": 1},
            "charge": -1,
            "phase": "aq",
        },
        "NH4": {
            "molar_mass": 18.0385,
            "stoichiometry": {"N": 1, "H": 4},
            "charge": 1,
            "phase": "aq",
        },
        "SO4": {
            "molar_mass": 96.0636,
            "stoichiometry": {"S": 1, "O": 4},
            "charge": -2,
            "phase": "aq",
        },
        "Fe": {
            "molar_mass": 55.845,
            "stoichiometry": {"Fe": 1},
            "charge": 3,
            "phase": "aq",
        },
    }


@pytest.fixture()
def parser() -> ChemicalFormulaParser:
    """Provide a chemical formula parser instance."""
    return ChemicalFormulaParser()
