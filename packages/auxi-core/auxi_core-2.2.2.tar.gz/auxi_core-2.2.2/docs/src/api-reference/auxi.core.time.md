# package `auxi.core.time`

Provide time tools.

## Classes

### `class TimePeriod(IntEnum):`

<div style="padding-left: 20px;">

A period of time.

</div>

### `class Clock(NamedObject):`

<div style="padding-left: 20px;">

A clock that provides functions to manage a ticking clock based on a time period as well as retrieve the current tick's date since the start date.

#### Fields

- `start_datetime`: `dt.datetime` = `dt.datetime.min`

- `timestep_period`: `TimePeriod` = `TimePeriod.MONTH`

- `timestep_period_count`: `intPositive` = `1`

- `timestep_index`: `intPositiveOrZero` = `0`

#### Methods

```python
def model_post_init(self, __context) -> None
```

<div style="padding-left: 20px;">

</div>

```python
def tick(self) -> None
```

<div style="padding-left: 20px;">

Increment the clock's timestep index.



</div>

```python
def reset(self) -> None
```

<div style="padding-left: 20px;">

Reset the clock's timestep index to '0'.



</div>

```python
def datetime(self) -> dt.datetime
```

<div style="padding-left: 20px;">

The clock's current date and time.



</div>

```python
def delta(self) -> relativedelta
```

<div style="padding-left: 20px;">

Timestep duration.



</div>

```python
def get_datetime(self, index) -> dt.datetime
```

<div style="padding-left: 20px;">

Get the clock's current datetime, or the specified number of timesteps into the future.

**Arguments**:
- `index(int)`

**Returns**:
- Datetime.


</div>

```python
def serialize_timestep_period(self, timestep_period) -> str | None
```

<div style="padding-left: 20px;">

Serialize the field.

**Arguments**:
- `timestep_period(TimePeriod)`

</div>

</div>
