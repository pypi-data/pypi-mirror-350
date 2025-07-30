"""Provide tests."""


def test___repr__():
    """
    Test method.
    """
    from auxi.chemistry.stoichiometry import periodic_table

    for symbol, element in periodic_table.items():
        assert repr(element) == f"Element({symbol})"
