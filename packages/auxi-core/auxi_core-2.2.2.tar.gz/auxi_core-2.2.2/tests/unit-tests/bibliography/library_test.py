"""Provide tests."""


def test_import_package_items() -> None:
    """
    Test importing all sub-package items.
    """
    from auxi.core.bibliography import library

    entry = library.entries_dict["bowman1994"]
    assert entry is not None
    assert entry.fields_dict["author"].value == "B. Bowman"
    assert entry.fields_dict["title"].value == "Properties of arcs in DC furnaces"
