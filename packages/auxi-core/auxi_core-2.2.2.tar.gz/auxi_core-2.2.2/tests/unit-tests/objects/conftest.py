"""Provide test fixtures."""

import pytest

from auxi.core.objects import NamedObject, Object


class ConcreteObject(Object):
    """Concrete class for testing."""

    def _init(self) -> None:
        pass


@pytest.fixture()
def object() -> ConcreteObject:
    """Provide object from a concrete class."""
    result = ConcreteObject()
    result.init()

    return result


class ConcreteNamedObject(NamedObject):
    """Concrete class for testing."""

    def _init(self) -> None:
        pass


@pytest.fixture()
def named_object() -> ConcreteNamedObject:
    """Provide object from a concrete class."""
    result = ConcreteNamedObject(
        name="NameA",
        description="Description A.",
    )
    result.init()

    return result
