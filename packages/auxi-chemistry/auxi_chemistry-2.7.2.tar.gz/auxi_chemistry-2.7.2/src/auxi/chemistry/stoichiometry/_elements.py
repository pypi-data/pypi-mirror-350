from auxi.core.objects import Object


class Element(Object):
    """
    An element in the periodic table.

    :param period: Period to which the element belongs.
    :param group: Group to which the element belongs.
    :param atomic_number: Number of protons in the element's nucleus.
    :param symbol: Element's symbol.
    :param molar_mass: [kg/kmol] Element's standard atomic mass.
    """

    # TODO: Add tests.
    # TODO: Implement validate method.

    period: int
    group: int
    atomic_number: int
    symbol: str
    molar_mass: float

    def __repr__(self):
        return f"Element({self.symbol})"

    def _init(self):
        return


periodic_table: dict[str, Element] = {
    # period 1
    "H": Element(period=1, group=1, atomic_number=1, symbol="H", molar_mass=1.00794),
    "D": Element(period=1, group=1, atomic_number=1, symbol="D", molar_mass=2.0141017778),
    "He": Element(period=1, group=18, atomic_number=2, symbol="He", molar_mass=4.002602),
    # period 2
    "Li": Element(period=2, group=1, atomic_number=3, symbol="Li", molar_mass=6.941),
    "Be": Element(period=2, group=2, atomic_number=4, symbol="Be", molar_mass=9.012182),
    "B": Element(period=2, group=13, atomic_number=5, symbol="B", molar_mass=10.811),
    "C": Element(period=2, group=14, atomic_number=6, symbol="C", molar_mass=12.0107),
    "N": Element(period=2, group=15, atomic_number=7, symbol="N", molar_mass=14.00674),
    "O": Element(period=2, group=16, atomic_number=8, symbol="O", molar_mass=15.9994),
    "F": Element(period=2, group=17, atomic_number=9, symbol="F", molar_mass=18.9984032),
    "Ne": Element(period=2, group=18, atomic_number=10, symbol="Ne", molar_mass=20.1797),
    # period 3
    "Na": Element(period=3, group=1, atomic_number=11, symbol="Na", molar_mass=22.98977),
    "Mg": Element(period=3, group=2, atomic_number=12, symbol="Mg", molar_mass=24.305),
    "Al": Element(period=3, group=13, atomic_number=13, symbol="Al", molar_mass=26.981538),
    "Si": Element(period=3, group=14, atomic_number=14, symbol="Si", molar_mass=28.0855),
    "P": Element(period=3, group=15, atomic_number=15, symbol="P", molar_mass=30.973762),
    "S": Element(period=3, group=16, atomic_number=16, symbol="S", molar_mass=32.066),
    "Cl": Element(period=3, group=17, atomic_number=17, symbol="Cl", molar_mass=35.4527),
    "Ar": Element(period=3, group=18, atomic_number=18, symbol="Ar", molar_mass=39.948),
    # period 4
    "K": Element(period=4, group=1, atomic_number=19, symbol="K", molar_mass=39.0983),
    "Ca": Element(period=4, group=2, atomic_number=20, symbol="Ca", molar_mass=40.078),
    "Sc": Element(period=4, group=3, atomic_number=21, symbol="Sc", molar_mass=44.95591),
    "Ti": Element(period=4, group=4, atomic_number=22, symbol="Ti", molar_mass=47.867),
    "V": Element(period=4, group=5, atomic_number=23, symbol="V", molar_mass=50.9415),
    "Cr": Element(period=4, group=6, atomic_number=24, symbol="Cr", molar_mass=51.9961),
    "Mn": Element(period=4, group=7, atomic_number=25, symbol="Mn", molar_mass=54.938049),
    "Fe": Element(period=4, group=8, atomic_number=26, symbol="Fe", molar_mass=55.845),
    "Co": Element(period=4, group=9, atomic_number=27, symbol="Co", molar_mass=58.9332),
    "Ni": Element(period=4, group=10, atomic_number=28, symbol="Ni", molar_mass=58.6934),
    "Cu": Element(period=4, group=11, atomic_number=29, symbol="Cu", molar_mass=63.546),
    "Zn": Element(period=4, group=12, atomic_number=30, symbol="Zn", molar_mass=65.39),
    "Ga": Element(period=4, group=13, atomic_number=31, symbol="Ga", molar_mass=69.723),
    "Ge": Element(period=4, group=14, atomic_number=32, symbol="Ge", molar_mass=72.61),
    "As": Element(period=4, group=15, atomic_number=33, symbol="As", molar_mass=74.9216),
    "Se": Element(period=4, group=16, atomic_number=34, symbol="Se", molar_mass=78.96),
    "Br": Element(period=4, group=17, atomic_number=35, symbol="Br", molar_mass=79.904),
    "Kr": Element(period=4, group=18, atomic_number=36, symbol="Kr", molar_mass=83.8),
    # period 5
    "Rb": Element(period=5, group=1, atomic_number=37, symbol="Rb", molar_mass=85.4678),
    "Sr": Element(period=5, group=2, atomic_number=38, symbol="Sr", molar_mass=87.62),
    "Y": Element(period=5, group=3, atomic_number=39, symbol="Y", molar_mass=88.90585),
    "Zr": Element(period=5, group=4, atomic_number=40, symbol="Zr", molar_mass=91.224),
    "Nb": Element(period=5, group=5, atomic_number=41, symbol="Nb", molar_mass=92.90638),
    "Mo": Element(period=5, group=6, atomic_number=42, symbol="Mo", molar_mass=95.94),
    "Tc": Element(period=5, group=7, atomic_number=43, symbol="Tc", molar_mass=98.0),
    "Ru": Element(period=5, group=8, atomic_number=44, symbol="Ru", molar_mass=101.07),
    "Rh": Element(period=5, group=9, atomic_number=45, symbol="Rh", molar_mass=102.9055),
    "Pd": Element(period=5, group=10, atomic_number=46, symbol="Pd", molar_mass=106.42),
    "Ag": Element(period=5, group=11, atomic_number=47, symbol="Ag", molar_mass=107.8682),
    "Cd": Element(period=5, group=12, atomic_number=48, symbol="Cd", molar_mass=112.411),
    "In": Element(period=5, group=13, atomic_number=49, symbol="In", molar_mass=114.818),
    "Sn": Element(period=5, group=14, atomic_number=50, symbol="Sn", molar_mass=118.71),
    "Sb": Element(period=5, group=15, atomic_number=51, symbol="Sb", molar_mass=121.76),
    "Te": Element(period=5, group=16, atomic_number=52, symbol="Te", molar_mass=127.6),
    "I": Element(period=5, group=17, atomic_number=53, symbol="I", molar_mass=126.90447),
    "Xe": Element(period=5, group=18, atomic_number=54, symbol="Xe", molar_mass=131.29),
    # period 6
    "Cs": Element(period=6, group=1, atomic_number=55, symbol="Cs", molar_mass=132.90545),
    "Ba": Element(period=6, group=2, atomic_number=56, symbol="Ba", molar_mass=137.327),
    "La": Element(period=6, group=0, atomic_number=57, symbol="La", molar_mass=138.9055),
    "Ce": Element(period=6, group=0, atomic_number=58, symbol="Ce", molar_mass=140.116),
    "Pr": Element(period=6, group=0, atomic_number=59, symbol="Pr", molar_mass=140.90765),
    "Nd": Element(period=6, group=0, atomic_number=60, symbol="Nd", molar_mass=144.24),
    "Pm": Element(period=6, group=0, atomic_number=61, symbol="Pm", molar_mass=145.0),
    "Sm": Element(period=6, group=0, atomic_number=62, symbol="Sm", molar_mass=150.36),
    "Eu": Element(period=6, group=0, atomic_number=63, symbol="Eu", molar_mass=151.964),
    "Gd": Element(period=6, group=0, atomic_number=64, symbol="Gd", molar_mass=157.25),
    "Tb": Element(period=6, group=0, atomic_number=65, symbol="Tb", molar_mass=158.92534),
    "Dy": Element(period=6, group=0, atomic_number=66, symbol="Dy", molar_mass=162.5),
    "Ho": Element(period=6, group=0, atomic_number=67, symbol="Ho", molar_mass=164.93032),
    "Er": Element(period=6, group=0, atomic_number=68, symbol="Er", molar_mass=167.26),
    "Tm": Element(period=6, group=0, atomic_number=69, symbol="Tm", molar_mass=168.93421),
    "Yb": Element(period=6, group=0, atomic_number=70, symbol="Yb", molar_mass=173.04),
    "Lu": Element(period=6, group=0, atomic_number=71, symbol="Lu", molar_mass=174.967),
    "Hf": Element(period=6, group=4, atomic_number=72, symbol="Hf", molar_mass=178.49),
    "Ta": Element(period=6, group=5, atomic_number=73, symbol="Ta", molar_mass=180.9479),
    "W": Element(period=6, group=6, atomic_number=74, symbol="W", molar_mass=183.84),
    "Re": Element(period=6, group=7, atomic_number=75, symbol="Re", molar_mass=186.207),
    "Os": Element(period=6, group=8, atomic_number=76, symbol="Os", molar_mass=190.23),
    "Ir": Element(period=6, group=9, atomic_number=77, symbol="Ir", molar_mass=192.217),
    "Pt": Element(period=6, group=10, atomic_number=78, symbol="Pt", molar_mass=195.078),
    "Au": Element(period=6, group=11, atomic_number=79, symbol="Au", molar_mass=196.96655),
    "Hg": Element(period=6, group=12, atomic_number=80, symbol="Hg", molar_mass=200.59),
    "Tl": Element(period=6, group=13, atomic_number=81, symbol="Tl", molar_mass=204.3833),
    "Pb": Element(period=6, group=14, atomic_number=82, symbol="Pb", molar_mass=207.2),
    "Bi": Element(period=6, group=15, atomic_number=83, symbol="Bi", molar_mass=208.98038),
    "Po": Element(period=6, group=16, atomic_number=84, symbol="Po", molar_mass=210.0),
    "At": Element(period=6, group=17, atomic_number=85, symbol="At", molar_mass=210.0),
    "Rn": Element(period=6, group=18, atomic_number=86, symbol="Rn", molar_mass=222.0),
    # period 7
    "Fr": Element(period=7, group=1, atomic_number=87, symbol="Fr", molar_mass=223.0),
    "Ra": Element(period=7, group=2, atomic_number=88, symbol="Ra", molar_mass=226.0),
    "Ac": Element(period=7, group=0, atomic_number=89, symbol="Ac", molar_mass=227.0),
    "Th": Element(period=7, group=0, atomic_number=90, symbol="Th", molar_mass=232.0381),
    "Pa": Element(period=7, group=0, atomic_number=91, symbol="Pa", molar_mass=231.03588),
    "U": Element(period=7, group=0, atomic_number=92, symbol="U", molar_mass=238.0289),
    "Np": Element(period=7, group=0, atomic_number=93, symbol="Np", molar_mass=237.0),
    "Pu": Element(period=7, group=0, atomic_number=94, symbol="Pu", molar_mass=244.0),
    "Am": Element(period=7, group=0, atomic_number=95, symbol="Am", molar_mass=243.0),
    "Cm": Element(period=7, group=0, atomic_number=96, symbol="Cm", molar_mass=247.0),
    "Bk": Element(period=7, group=0, atomic_number=97, symbol="Bk", molar_mass=247.0),
    "Cf": Element(period=7, group=0, atomic_number=98, symbol="Cf", molar_mass=251.0),
    "Es": Element(period=7, group=0, atomic_number=99, symbol="Es", molar_mass=252.0),
    "Fm": Element(period=7, group=0, atomic_number=100, symbol="Fm", molar_mass=257.0),
    "Md": Element(period=7, group=0, atomic_number=101, symbol="Md", molar_mass=258.0),
    "No": Element(period=7, group=0, atomic_number=102, symbol="No", molar_mass=259.0),
    "Lr": Element(period=7, group=0, atomic_number=103, symbol="Lr", molar_mass=262.0),
    "Rf": Element(period=7, group=4, atomic_number=104, symbol="Rf", molar_mass=261.0),
    "Db": Element(period=7, group=5, atomic_number=105, symbol="Db", molar_mass=262.0),
    "Sg": Element(period=7, group=6, atomic_number=106, symbol="Sg", molar_mass=266.0),
    "Bh": Element(period=7, group=7, atomic_number=107, symbol="Bh", molar_mass=264.0),
    "Hs": Element(period=7, group=8, atomic_number=108, symbol="Hs", molar_mass=269.0),
    "Mt": Element(period=7, group=9, atomic_number=109, symbol="Mt", molar_mass=268.0),
    "Ds": Element(period=7, group=10, atomic_number=110, symbol="Ds", molar_mass=269.0),
    "Rg": Element(period=7, group=11, atomic_number=111, symbol="Rg", molar_mass=272.0),
    # Cn missing
    # Uut missing
    # Fl missing
    # Uup missing
    # Lv missing
    # Uus missing
    # Uuo missing
    # actinides
}
