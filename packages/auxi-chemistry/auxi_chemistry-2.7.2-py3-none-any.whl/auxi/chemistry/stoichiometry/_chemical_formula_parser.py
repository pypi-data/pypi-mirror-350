from collections import defaultdict
from pathlib import Path
from typing import TYPE_CHECKING, Any

from parsimonious import Grammar, NodeVisitor
from parsimonious.nodes import RegexNode

from ._chemical_formula_parse_result import ChemicalFormulaParseResult
from ._elements import periodic_table
from ._stoichiometry_record import StoichiometryRecord


class ChemicalFormulaParser(NodeVisitor[ChemicalFormulaParseResult] if TYPE_CHECKING else NodeVisitor):
    """A parser for chemical formulae."""

    def __init__(self) -> None:
        self.grammar_file = Path(__file__).with_suffix(".ebnf")
        self.grammar_text = self.grammar_file.read_text()

        self.grammar = Grammar(self.grammar_text)

    def __call__(self, text: str, pos: int = 0) -> ChemicalFormulaParseResult:
        return self.parse(text, pos)

    def parse(self, text: str, pos: int = 0) -> ChemicalFormulaParseResult:
        return super().parse(text, pos)

    def visit_formula(
        self,
        node: RegexNode,
        child_results: list[Any],
    ) -> ChemicalFormulaParseResult:
        stoich_dict: defaultdict[str, int] = child_results[0]
        charge: int
        phase: str | None

        if isinstance(child_results[1], defaultdict):
            dd: defaultdict[str, int] = child_results[1]
            for se, sn in dd.items():
                stoich_dict[se] += sn

        match child_results[2:]:
            case ["", ""]:
                charge = 0
                phase = None

            case ["", str(phase)]:
                charge = 0

            case [int(charge), ""]:
                phase = None

            case [int(charge), str(phase)]:
                pass

            case _:
                raise ValueError("Unexpected parse result.")

        element_list: list[str] = list(stoich_dict.keys())

        result = ChemicalFormulaParseResult(
            elements=element_list,
            stoichiometry=stoich_dict,
            charge=charge,
            phase=phase,
            molar_mass=ChemicalFormulaParser._calculate_molar_mass(stoich_dict),
        )

        return result

    def visit_compound(
        self,
        node: RegexNode,
        child_results: list[Any],
    ) -> defaultdict[str, int]:
        result: defaultdict[str, int] = defaultdict(int)

        for r in child_results:
            if isinstance(r, StoichiometryRecord):
                result[r.e] += r.n
            elif isinstance(r, defaultdict):
                rdd: defaultdict[str, int] = r
                for se, sn in rdd.items():
                    result[se] += sn
            else:
                raise ValueError("Unexpected parse result.")

        return result

    def visit_compound_n(
        self,
        node: RegexNode,
        child_results: list[Any],
    ) -> defaultdict[str, int]:
        stoich_dict: defaultdict[str, int]
        n: int

        match child_results:
            case ["(", stoich_dict, ")", ""]:
                n = 1

            case ["(", stoich_dict, ")", int(n)]:
                pass

            case _:
                raise ValueError("Unexpected parse result.")

        result: defaultdict[str, int] = defaultdict(int)
        for se, sn in stoich_dict.items():
            result[se] += sn * n

        return result

    def visit_dot_n_compound(
        self,
        node: RegexNode,
        child_results: list[Any],
    ) -> defaultdict[str, int]:
        stoich_dict: defaultdict[str, int]
        n: int

        match child_results:
            case [".", "", stoich_dict]:
                n = 1

            case [".", int(n), stoich_dict]:
                pass

            case _:
                raise ValueError("Unexpected parse result.")

        result: defaultdict[str, int] = defaultdict(int)
        for se, sn in stoich_dict.items():
            result[se] += sn * n

        return result

    def visit_charge(
        self,
        node: RegexNode,
        child_results: list[Any],
    ) -> int:
        match child_results[1:3]:
            case ["", "+"]:
                return 1

            case ["", "-"]:
                return -1

            case [int(n), "+"]:
                return n

            case [int(n), "-"]:
                return -n

            case _:
                raise ValueError("Unexpected parse result.")

    def visit_charge_number(
        self,
        node: RegexNode,
        child_results: list[Any],
    ) -> int:
        result = int(node.text)

        return result

    def visit_charge_sign(
        self,
        node: RegexNode,
        child_results: list[Any],
    ) -> str:
        result = node.text

        return result

    def visit_phase(
        self,
        node: RegexNode,
        child_results: list[Any],
    ) -> str:
        result = child_results[1]

        return result

    def visit_phase_label(
        self,
        node: RegexNode,
        child_results: list[Any],
    ) -> str:
        result = node.text

        return result

    def visit_element_n(
        self,
        node: RegexNode,
        child_results: list[Any],
    ) -> StoichiometryRecord:
        (element, number) = child_results
        result = StoichiometryRecord(
            e=element.e,
            n=element.n * number,
        )

        return result

    def visit_element(
        self,
        node: RegexNode,
        child_results: list[Any],
    ) -> StoichiometryRecord:
        result = StoichiometryRecord(
            e=node.text,
            n=1,
        )

        return result

    def visit_n(
        self,
        node: RegexNode,
        child_results: list[Any],
    ) -> int:
        result = int(node.text)

        return result

    def generic_visit(  # type: ignore
        self,
        node: RegexNode,
        child_results: list[Any],
    ) -> str | list[Any]:
        crs = self._clear_crs(child_results)
        if len(crs) == 0:
            result = node.text.strip()
        elif len(crs) == 1:
            result = crs[0]
        else:
            result = crs

        return result

    def _clear_crs(self, child_results: list[Any]) -> list[Any]:
        return [r for r in child_results if r != ""]

    @staticmethod
    def _calculate_molar_mass(stoichiometry: dict[str, int]) -> float:
        for element in stoichiometry.keys():
            if element not in periodic_table:
                raise ValueError(f"Invalid element symbol '{element}'.")

        return sum([periodic_table[element].molar_mass * count for element, count in stoichiometry.items()])


parser = ChemicalFormulaParser()
