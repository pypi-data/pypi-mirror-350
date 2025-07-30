from dataclasses import dataclass


@dataclass
class StoichiometryRecord:
    e: str  # element symbol
    n: int  # count of element
