"""Provide tests."""

from .conftest import ConcreteObject


def test_constructor(object: ConcreteObject) -> None:
    """Test constructor."""
    assert object is not None


def test___str__(object: ConcreteObject) -> None:
    """Test the method."""
    assert str(object) == object.model_dump_json(indent=4)


def test___hash__(object: ConcreteObject) -> None:
    """Test the method."""
    assert hash(object) == hash(str(object))


def test_write(object: ConcreteObject) -> None:
    """Test the method."""
    import json
    import tempfile
    from pathlib import Path
    from typing import Any
    import yaml

    loaders: dict[str, Any] = {".json": json.loads, ".yaml": yaml.safe_load}

    for suffix, loader in loaders.items():
        f = Path(tempfile.NamedTemporaryFile().name).with_suffix(suffix)
        object.write(f)
        str_o: str = f.read_text()
        dict_o: dict[str, Any] = loader(str_o)
        new_o: ConcreteObject = ConcreteObject(**dict_o)
        assert isinstance(new_o, ConcreteObject)
        assert str(object) == str(new_o)


def test_read(object: ConcreteObject) -> None:
    "Test the method." ""
    import tempfile
    from pathlib import Path

    suffixes: list[str] = [".json", ".yaml"]

    for suffix in suffixes:
        f = Path(tempfile.NamedTemporaryFile().name).with_suffix(suffix)
        object.write(f)
        new_o: ConcreteObject = ConcreteObject.read(f)
        assert isinstance(new_o, ConcreteObject)
        assert str(object) == str(new_o)
