# `ticktocker`

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
</p>


`ticktocker` is a Python package that helps you measure the time taken by code execution. It provides a simple and intuitive way to track performance and optimize your code.

## Todos

- CI/CD
  - Unit tests
  - Git branching
- Add templates for PR and issues.

## Features

### Context Manager

`ticktocker` supports to measure the time taken by a block of code using a context manager.

```python
from ticktocker import clock

with clock() as sw:
    ...
print(sw.elapsed)
```

### Decorator

`ticktocker` also supports to measure the time taken by a function using a decorator.

```python
from ticktocker import clock

@clock
def my_function():
    ...
my_function() # Elapsed time: ...
```
