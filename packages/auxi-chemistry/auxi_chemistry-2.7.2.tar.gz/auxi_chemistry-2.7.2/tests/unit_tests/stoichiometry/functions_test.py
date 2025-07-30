"""Provide tests."""

from typing import Any

import pytest


def test_invalid_characters():
    """Test exception upon invalid input."""
    from auxi.chemistry.stoichiometry import molar_mass as mm

    formulae = [
        "(FeO)*(Fe2O3)",
        "CaO1,5",
    ]

    for formula in formulae:
        with pytest.raises(Exception):
            mm(formula)


def test_molar_mass(compounds: dict[str, dict[str, Any]], tolerance: float):
    """Test function."""
    from auxi.chemistry.stoichiometry import molar_mass as mm

    for compound, data in compounds.items():
        molar_mass = data["molar_mass"]
        assert mm(compound) == pytest.approx(molar_mass, tolerance)  # type: ignore


def test_amount(compounds: dict[str, dict[str, Any]], tolerance: float):
    """Test function."""
    from auxi.chemistry.stoichiometry import (
        amount as n,
        molar_mass as mm,
    )

    for compound in compounds.keys():
        m = 1000.0
        assert n(compound, m) == pytest.approx(m / mm(compound), tolerance)  # type: ignore


def test_amounts():
    """Test function."""
    from auxi.chemistry.stoichiometry import (
        amounts,
        molar_mass as mm,
    )

    compounds = ["SiO2", "CaO", "MgO", "FeO"]
    m = 1000.0
    ms = {compound: m for compound in compounds}
    ns = {compound: ms[compound] / mm(compound) for compound in compounds}

    assert amounts(ms) == ns


def test_amount_fractions():
    """Test function."""
    from auxi.chemistry.stoichiometry import (
        amount_fractions,
        molar_mass as mm,
    )

    compounds = ["SiO2", "CaO", "MgO", "FeO"]
    m = 1000.0
    ms = {compound: m for compound in compounds}
    ns = {compound: ms[compound] / mm(compound) for compound in compounds}
    n_tot = sum(ns.values())
    xs = {compound: ns[compound] / n_tot for compound in compounds}

    assert amount_fractions(ms) == xs


def test_mass(compounds: dict[str, dict[str, Any]], tolerance: float):
    """
    Test whether the mass of a compound is calculated correctly.
    """
    from auxi.chemistry.stoichiometry import (
        mass as m,
        molar_mass as mm,
    )

    for compound in compounds.keys():
        n = 1000.0
        assert m(compound, n) == pytest.approx(n * mm(compound), tolerance)  # type: ignore


def test_masses():
    """Test function."""
    from auxi.chemistry.stoichiometry import (
        masses,
        molar_mass as mm,
    )

    compounds = ["SiO2", "CaO", "MgO", "FeO"]
    n = 1000.0
    ns = {compound: n for compound in compounds}
    ms = {compound: ns[compound] * mm(compound) for compound in compounds}

    assert masses(ns) == ms


def test_mass_fractions():
    """Test function."""
    from auxi.chemistry.stoichiometry import (
        mass_fractions,
        molar_mass as mm,
    )

    compounds = ["SiO2", "CaO", "MgO", "FeO"]
    n = 1000.0
    ns = {compound: n for compound in compounds}
    ms = {compound: ns[compound] * mm(compound) for compound in compounds}
    m_tot = sum(ms.values())
    ys = {compound: ms[compound] / m_tot for compound in compounds}

    assert mass_fractions(ns) == ys


def test_convert_compound(tolerance: float):
    """
    Test whether compound conversions are calculated correctly.
    """
    from auxi.chemistry.stoichiometry import (
        convert_compound as cc,
        molar_mass as mm,
    )

    m = 1000.0

    m_converted = m / mm("Fe2O3") * 2 * mm("FeO")
    assert cc(m, "Fe2O3", "FeO", "Fe") == pytest.approx(m_converted, tolerance)  # type: ignore

    m_converted = m / mm("FeO(OH)") * 0.5 * mm("H2O")
    assert cc(m, "FeO(OH)", "H2O", "H") == pytest.approx(m_converted, tolerance)  # type: ignore

    assert cc(m, "FeO(OH)", "H2O", "S") == 0.0


def test_element_mass_fraction(tolerance: float):
    """Test function."""
    from auxi.chemistry.stoichiometry import (
        element_mass_fraction as ye,
        molar_mass as mm,
        stoichiometry_coefficient as sc,
    )

    compounds = ["FeO", "Fe2O3", "SiO2", "Ca(OH)2"]
    elements = ["Fe", "O", "Si", "Ca", "H"]

    for c in compounds:
        for e in elements:
            ye_check = sc(c, e) * mm(e) / mm(c)
            assert ye(c, e) == pytest.approx(ye_check, tolerance)  # type: ignore


def test_element_mass_fractions(tolerance: float):
    """Test function."""
    from auxi.chemistry.stoichiometry import (
        element_mass_fractions as yes,
        molar_mass as mm,
        stoichiometry_coefficient as sc,
    )

    compounds = ["FeO", "Fe2O3", "SiO2", "Ca(OH)2"]
    elements = ["Fe", "O", "Si", "Ca", "H"]

    for c in compounds:
        yes_check = [sc(c, e) * mm(e) / mm(c) for e in elements]
        assert yes(c, elements) == pytest.approx(yes_check, tolerance)  # type: ignore


def test_elements():
    """Test function."""
    from auxi.chemistry.stoichiometry import (
        elements as es,
    )

    compounds = ["Ar", "Fe2O3", "SiO2", "Al2O3", "SO3", "CaO", "Fe", "Mn2O3"]
    es_calc = es(compounds)
    es_check = {"Al", "Ar", "Ca", "Fe", "Mn", "O", "S", "Si"}
    assert es_calc == es_check

    compounds = ["CO2"]
    assert es(compounds) == {"C", "O"}


def test_stoichiometry_coefficient():
    """Test function."""
    from auxi.chemistry.stoichiometry import (
        ChemicalFormulaParseResult as ParseResult,
        parser,
        stoichiometry_coefficient as sc,
    )

    compounds = ["FeO", "Fe2O3", "SiO2", "Ca(OH)2"]
    elements = ["Fe", "O", "Si", "Ca", "H"]

    for c in compounds:
        pr: ParseResult = parser(c)
        for e in elements:
            assert sc(c, e) == pr.stoichiometry[e]


def test_stoichiometry_coefficients():
    """Test function."""
    from auxi.chemistry.stoichiometry import (
        ChemicalFormulaParseResult as ParseResult,
        parser,
        stoichiometry_coefficients as scs,
    )

    compounds = ["FeO", "Fe2O3", "SiO2", "Ca(OH)2"]
    elements = ["Fe", "O", "Si", "Ca", "H"]

    for c in compounds:
        pr: ParseResult = parser(c)
        scs_check = [pr.stoichiometry[e] for e in elements]
        assert scs(c, elements) == scs_check


def test_is_compound():
    """Test function."""
    from auxi.chemistry.stoichiometry import (
        is_compound,
    )

    compounds = ["FeO", "Fe2O3", "SiO2", "Ca(OH)2"]

    for c in compounds:
        assert is_compound(c)

    compounds = ["Az", "CcO2", "H2O*", "-NaCl"]

    for c in compounds:
        assert not is_compound(c)
