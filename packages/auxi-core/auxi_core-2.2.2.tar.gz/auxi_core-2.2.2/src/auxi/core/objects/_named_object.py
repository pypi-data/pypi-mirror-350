from ._object import Object
from ..validation import strNotEmpty


class NamedObject(Object):
    """
    Abstract base class for `auxi` classes that require a name and description.

    Args:
        name (str): the object's name
        description (str): the object's description
    """

    name: strNotEmpty
    description: str | None = None
