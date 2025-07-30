from ._chemical_formula_parser import parser


def amount(compound: str, mass: float) -> float:
    """
    Calculate chemical compound amount.

    :param compound: Compound formula, e.g. CaO, H2O, Fe2O3[S1].
    :param mass: [kg]
    :returns: Amount. [kmol]
    """
    return mass / molar_mass(compound)


def amounts(masses: dict[str, float]) -> dict[str, float]:
    """
    Calculate chemical compound amounts.

    :param compound masses: [kg] E.g. {'SiO2': 3.0, 'FeO': 1.5, 'MgO[s]: 2.5}
    :returns: [kmol]
    """
    return {compound: amount(compound, masses[compound]) for compound in masses.keys()}


def amount_fractions(masses: dict[str, float]) -> dict[str, float]:
    """
    Calculate chemical compound amount fractions.

    :param compound masses: [kg] E.g. {'SiO2': 3.0, 'FeO': 1.5, 'MgO[s]: 2.5}
    :returns: [kmol/kmol]
    """
    n = amounts(masses)
    n_total = sum(n.values())
    return {compound: n[compound] / n_total for compound in n.keys()}


def mass(compound: str, amount: float) -> float:
    """
    Calculate chemical compound mass.

    :param compound: Compound formula, e.g. CaO, H2O, Fe2O3[S1].
    :param amount: [kmol]
    :returns: Mass. [kg]
    """
    return amount * molar_mass(compound)


def masses(amounts: dict[str, float]) -> dict[str, float]:
    """
    Calculate chemical compound masses.

    :param amounts: [kmol] E.g. {'SiO2': 3.0, 'FeO': 1.5, 'MgO[s]: 2.5}
    :returns: [kg]
    """
    return {compound: mass(compound, amounts[compound]) for compound in amounts.keys()}


def mass_fractions(amounts: dict[str, float]) -> dict[str, float]:
    """
    Calculate chemical compound mass fractions.

    :param amounts: [kmol] E.g. {'SiO2': 3.0, 'FeO': 1.5, 'MgO[s]: 2.5}
    :returns: [kg/kg]
    """
    m = masses(amounts)
    m_total = sum(m.values())

    return {compound: m[compound] / m_total for compound in m.keys()}


def convert_compound(mass: float, source: str, target: str, element: str) -> float:
    """
    Convert a source compound mass to the target compound based on the the specified element.

    :param mass: Mass of from_compound. [kg]
    :param source: Source compound formula, e.g. CaO, H2O, Fe2O3[S1].
    :param target: Target compound formula, e.g. 'Fe[S1]'.
    :param element: Basis element symbol, e.g. 'Fe' or 'O'.
    :returns: Target mass. [kg]
    """
    target_y = element_mass_fraction(target, element)
    if target_y == 0.0:
        return 0.0
    else:
        source_y = element_mass_fraction(source, element)
        return mass * source_y / target_y


def element_mass_fraction(compound: str, element: str) -> float:
    """
    Calculate element mass fraction in a compound.

    :param compound: Compound formula, e.g. CaO, H2O, Fe2O3[S1].
    :param element: Element, e.g. 'Cr'.
    :returns: Element mass fraction.
    """
    sc = stoichiometry_coefficient(compound, element)

    if sc == 0.0:
        return 0.0

    formula_mm = molar_mass(compound)
    element_mm = molar_mass(element)

    return sc * element_mm / formula_mm


def element_mass_fractions(compound: str, elements: list[str]) -> list[float]:
    """
    Calculate element mass fractions in a chemical compound.

    :param compound: Compound formula, e.g. CaO, H2O, Fe2O3[S1].
    :param elements: List of elements, e.g. ['Si', 'O', 'Fe'].
    :returns: Mass fractions.
    """
    return [element_mass_fraction(compound, element) for element in elements]


def elements(compounds: list[str]) -> set[str]:
    """
    Determine the elements present in the specified chemical compounds.

    The list of elements is sorted alphabetically.

    :param compounds: Compound formulae, e.g. ['Fe2O3[S1]', 'Al2O3[S1]', 'SiO2'].
    :returns: Elements.
    """
    elements: list[str] = []
    for compound in compounds:
        elements += parser.parse(compound).elements

    return set(sorted(elements))


def molar_mass(compound: str) -> float:
    """
    Calculate the molar mass of a chemical compound.

    :param compound: Compound formula, e.g. CaO, H2O, Fe2O3[S1].
    :returns: [kg/kmol] Molar mass.
    """
    return parser.parse(compound).molar_mass


def stoichiometry_coefficient(compound: str, element: str) -> float:
    """
    Calculate an element stoichiometry coefficient in a chemical compound.

    :param compound: Compound formula, e.g. CaO, H2O, Fe2O3[S1].
    :param element:  Element, e.g. 'Si'.
    :returns: Stoichiometry coefficient.
    """
    return parser.parse(compound).stoichiometry[element]


def stoichiometry_coefficients(compound: str, elements: list[str]) -> list[float]:
    """
    Calculate element stoichiometry coefficients in a chemical compound.

    :param compound: Compound formula, e.g. CaO, H2O, Fe2O3[S1].
    :param elements: List of elements, e.g. ['Si', 'O', 'C'].
    :returns: List of stoichiometry coefficients.
    """
    stoichiometry = parser.parse(compound).stoichiometry
    return [stoichiometry[element] for element in elements]


def charge(compound: str) -> int:
    """
    Determine the charge of a chemical compound.
    """
    return parser.parse(compound).charge


def is_compound(compound: str) -> bool:
    """Determine whether the specified formula is a valid chemical compound."""
    try:
        parser.parse(compound)
        return True
    except Exception:
        return False


def is_cation(compound: str) -> bool:
    """Determine whether the specified formula is a valid cation."""
    try:
        return parser.parse(compound).charge > 0
    except Exception:
        return False


def is_anion(compound: str) -> bool:
    """Determine whether the specified formula is a valid anion."""
    try:
        return parser.parse(compound).charge < 0
    except Exception:
        return False
