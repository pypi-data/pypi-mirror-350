"""Provide tests."""


def test_import_package() -> None:
    """
    Test importing the sub-package.
    """
    from auxi.core import bibliography

    assert bibliography is not None


def test_import_package_items() -> None:
    """
    Test importing all sub-package items.
    """
    from auxi.core.bibliography import library

    assert library is not None
