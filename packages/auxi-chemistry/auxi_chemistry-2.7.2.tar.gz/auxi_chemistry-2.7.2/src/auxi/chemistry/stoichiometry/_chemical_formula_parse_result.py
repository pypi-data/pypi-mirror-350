from collections import defaultdict
from dataclasses import dataclass


@dataclass
class ChemicalFormulaParseResult:
    elements: list[str]
    stoichiometry: defaultdict[str, int]
    charge: int
    phase: str | None
    molar_mass: float
