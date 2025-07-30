# https://www.augmentedmind.de/2020/10/25/marshmallow-vs-pydantic-python/
# https://stackoverflow.com/questions/68746351/using-pydantic-to-deserialize-sublasses-of-a-model
# https://github.com/pydantic/pydantic/discussions/3091

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Self

import pydantic


class Object(ABC, pydantic.BaseModel):
    """
    Abstract base class for all `auxi` classes.

    For a child class to be concrete, the abstract `_init` method must be implemented.
    """

    def __str__(self) -> str:
        return self.model_dump_json(indent=4)

    def __hash__(self) -> int:
        return hash(str(self))

    @abstractmethod
    def _init(self) -> None: ...

    def init(self) -> None:
        """Initialize the object by calling the `_init` method."""
        self._init()

    def write(self, path: Path) -> None:
        """
        Write the object to a file, in either `json` or `yaml` format.

        Args:
            path (Path): Destination file path.

        Raises:
            ValueError: Raised if the file format is not supported.
        """
        match path.suffix:
            case ".json":
                with open(path, "w") as f:
                    f.write(self.model_dump_json(indent=4))

            case ".yaml":
                import yaml

                with open(path, "w") as f:
                    o = self.model_dump()
                    yaml.dump(o, f, allow_unicode=True)

            case _:
                raise ValueError(f"Unsupported file format: {path.suffix}")

    @classmethod
    def read(cls, path: Path) -> Self:
        """
        Read the file from the specified path, in either `json` or `yaml` format, and create an object.

        Args:
            path (Path): Destination file path.

        Raises:
            FileExistsError
            ValueError: Raised if the file format is not supported.
        """
        with open(path) as f:
            s = f.read()

        match path.suffix:
            case ".json":
                import json

                result = cls(**json.loads(s))

            case ".yaml":
                import yaml

                result = cls(**yaml.safe_load(s))

            case _:
                raise ValueError(f"Unsupported file format: {path.suffix}")

        result._init()
        return result
