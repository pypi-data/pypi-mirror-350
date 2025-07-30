"""Provide tests."""

import pytest
from .conftest import ConcreteNamedObject


def test_constructor(named_object: ConcreteNamedObject) -> None:
    """Test class constructor."""
    assert named_object.name == "NameA"
    assert named_object.description == "Description A."


def test__str__(named_object: ConcreteNamedObject) -> None:
    """Test the method."""
    str_o = str(named_object)
    assert '"name": "NameA",' in str_o
    assert '"description": "Description A."' in str_o


def test_name_validation() -> None:
    """Test field validation."""
    with pytest.raises(ValueError, match="string length must be greater than 0"):
        ConcreteNamedObject(name="")


def test_write(named_object: ConcreteNamedObject) -> None:
    """Test the method."""
    import json
    import tempfile
    from pathlib import Path
    from typing import Any
    import yaml

    loaders: dict[str, Any] = {".json": json.loads, ".yaml": yaml.safe_load}

    for suffix, loader in loaders.items():
        f = Path(tempfile.NamedTemporaryFile().name).with_suffix(suffix)
        named_object.write(f)

        str_o: str = f.read_text()
        dict_o: dict[str, Any] = loader(str_o)
        new_o: ConcreteNamedObject = ConcreteNamedObject(**dict_o)

        assert isinstance(new_o, ConcreteNamedObject)
        assert str(named_object) == str(new_o)
        assert named_object.name == new_o.name
        assert named_object.description == new_o.description


def test_read(named_object: ConcreteNamedObject) -> None:
    "Test the method." ""
    import tempfile
    from pathlib import Path

    suffixes: list[str] = [".json", ".yaml"]

    for suffix in suffixes:
        f = Path(tempfile.NamedTemporaryFile().name).with_suffix(suffix)
        named_object.write(f)

        new_o: ConcreteNamedObject = ConcreteNamedObject.read(f)

        assert isinstance(new_o, ConcreteNamedObject)
        assert str(named_object) == str(new_o)
        assert named_object.name == new_o.name
        assert named_object.description == new_o.description
