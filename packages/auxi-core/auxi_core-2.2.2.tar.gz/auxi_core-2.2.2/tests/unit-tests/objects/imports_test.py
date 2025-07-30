"""Provide tests."""


def test_import_package() -> None:
    """
    Test importing the sub-package.
    """
    from auxi.core import objects

    assert objects is not None


def test_import_package_items() -> None:
    """
    Test importing all sub-package items.
    """
    from auxi.core.objects import Object, NamedObject

    assert Object is not None
    assert NamedObject is not None
