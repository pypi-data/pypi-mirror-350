# `auxi.core.objects`

This package provides the main base classes that are used to create classes in the `auxi` framework.
Other packages like `auxi-chemistry` and `auxi-mpp` can use these classes to inherit useful features for their concrete classes.

```mermaid
{{#include auxi.core.objects.mermaid}}
```


## Inheritance


### Abstract Base Classes

`Object` is firstly derived from `abc.ABC` to explicitly make it and its children abstract base classes by default.
To make a child class concrete, the `_init` method must be overridden.


### Pydantic `BaseModel`

`Object` is also derived from [Pydantic](https://docs.pydantic.dev/latest/)'s `BaseModel` class.
This provides all its children with Pydantic base model capabilities, which includes validation, serialisation, and deserialisation.


## Serde

`Object` serialisation and deserialisation (serde) is achieved with the `write` and `read` methods.
Supported data formats include [json](https://www.json.org/json-en.html) and [yaml](https://yaml.org/).

* `write` is an object method that persists the current object to the specified path.
* `read` is a class method that reads from the specified path, and returns an instance of the child class on which the method was called.
