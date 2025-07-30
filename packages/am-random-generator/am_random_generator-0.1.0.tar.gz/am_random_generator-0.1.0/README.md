# randomgen

A simple Python package to generate random numbers, characters or both of a given length.

## Install

```bash
pip install randomgen
```

## Usage

```python
from randomgen import generate_random

print(generate_random(8))  # both by default
print(generate_random(5, 'number'))
print(generate_random(10, 'char'))
```

## Test Locally

In terminal:
```bash
pip install -e .
```

## Upload to PyPI (if you want later)

```bash
pip install twine
python setup.py sdist bdist_wheel
twine upload dist/*
```