# package `auxi.core.reporting`

Provide reporting tools.

## Classes

### `class ReportFormat(IntEnum):`

<div style="padding-left: 20px;">

Report output format.

</div>

### `class Report(Object):`

<div style="padding-left: 20px;">

Abstract base class for all auxi reports.

#### Fields

- `data_source`: `Any`

- `output_path`: `Path | None` = `None`

#### Methods

```python
def serialize_output_path(self, output_path) -> str | None
```

<div style="padding-left: 20px;">

Serialize the field.

**Arguments**:
- `output_path(Path | None)`

</div>

```python
def render(self, format) -> str | None
```

<div style="padding-left: 20px;">

Render the report in the specified format.

**Arguments**:
- `format(ReportFormat)`: The format. The default format is to print the report to the console.

**Returns**:
- If the format was set to 'string' then a string representation of the report is returned.


</div>

</div>
