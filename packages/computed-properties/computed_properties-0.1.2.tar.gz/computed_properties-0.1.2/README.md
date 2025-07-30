# computed-properties

`computed-properties` is a small Python package that allows you to precompute properties and only recalculate them when the values of their dependencies have changed. This is useful for optimizing performance in classes where certain properties are expensive to compute and depend on other attributes.

## Installation

You can install the package using pip:

```bash
pip install computed-properties
```

## Usage

To use `computed-properties`, decorate your class properties with the provided decorator. The property will be automatically recalculated only when any of its dependencies change.

```python
from computed_properties import ComputedPropertyCache

cache = ComputedPropertyCache()
class Rectangle(metaclass=cache):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

    @cache.computed_property
    def area(self):
        print("Calculating area...")
        return self.width * self.height

rect = Rectangle(3, 4)
print(rect.area)  # Calculates and prints 12
print(rect.area)  # Uses cached value, prints 12
rect.width = 5
print(rect.area)  # Recalculates and prints 20
```

## Features

- Declarative dependency tracking for properties.
- Automatic invalidation and recalculation when dependencies change.
- Simple API using decorators.
- Lightweight and easy to integrate into existing projects.

## Additional Information

- Compatible with Python 3.7 and above.
- Well-suited for data models, scientific computing, and any scenario where computed properties depend on mutable state.
- Inspired by similar concepts in other frameworks and languages (e.g., Vue.js computed properties, Django cached_property).
- Contributions and issues are welcome via the project's GitHub repository.

For more details, examples, and API documentation, please refer to the [official documentation](https://github.com/adriaciurana/computed-properties).