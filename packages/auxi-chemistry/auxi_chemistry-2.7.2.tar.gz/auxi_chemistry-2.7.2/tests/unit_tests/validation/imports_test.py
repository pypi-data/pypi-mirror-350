"""Provide tests."""


def test_import_package() -> None:
    """Test importing the sub-package."""
    from auxi.chemistry import validation

    assert validation is not None


def test_import_package_items() -> None:
    """Test importing all sub-package items."""
    from auxi.chemistry.validation import (
        listCompoundFormulas,
        strCompoundFormula,
    )

    assert strCompoundFormula is not None
    assert listCompoundFormulas is not None
