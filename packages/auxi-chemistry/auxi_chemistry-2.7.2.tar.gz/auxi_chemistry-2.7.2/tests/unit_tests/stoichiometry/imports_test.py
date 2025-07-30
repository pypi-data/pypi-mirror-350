"""Provide tests."""


def test_import_package() -> None:
    """
    Test importing the sub-package.
    """
    from auxi.chemistry import stoichiometry

    assert stoichiometry is not None


def test_import_package_items() -> None:
    """
    Test importing all sub-package items.
    """
    from auxi.chemistry.stoichiometry import (
        ChemicalFormulaParser,
        ChemicalFormulaParseResult,
        Element,
        amount,
        amount_fractions,
        amounts,
        convert_compound,
        element_mass_fraction,
        element_mass_fractions,
        elements,
        is_compound,
        mass,
        mass_fractions,
        masses,
        molar_mass,
        parser,
        periodic_table,
        stoichiometry_coefficient,
        stoichiometry_coefficients,
    )

    assert Element is not None
    assert periodic_table is not None
    assert ChemicalFormulaParseResult is not None
    assert ChemicalFormulaParser is not None
    assert parser is not None
    assert molar_mass is not None
    assert amount is not None
    assert amounts is not None
    assert amount_fractions is not None
    assert mass is not None
    assert masses is not None
    assert mass_fractions is not None
    assert convert_compound is not None
    assert element_mass_fraction is not None
    assert element_mass_fractions is not None
    assert elements is not None
    assert stoichiometry_coefficient is not None
    assert stoichiometry_coefficients is not None
    assert is_compound is not None
