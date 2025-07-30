# package `auxi.core.objects`

Provide base classes for all auxi objects.

## Classes

### `class Object(ABC, pydantic.BaseModel):`

<div style="padding-left: 20px;">

Abstract base class for all `auxi` classes.
For a child class to be concrete, the abstract `_init` method must be implemented.

#### Methods

```python
def init(self) -> None
```

<div style="padding-left: 20px;">

Initialize the object by calling the `_init` method.



</div>

```python
def write(self, path) -> None
```

<div style="padding-left: 20px;">

Write the object to a file, in either `json` or `yaml` format.

**Arguments**:
- `path(Path)`: Destination file path.

</div>

```python
def read(cls, path) -> Self
```

<div style="padding-left: 20px;">

</div>

</div>

### `class NamedObject(Object):`

<div style="padding-left: 20px;">

Abstract base class for `auxi` classes that require a name and description.

#### Fields

- `name`: `strNotEmpty`

- `description`: `str | None` = `None`

</div>
