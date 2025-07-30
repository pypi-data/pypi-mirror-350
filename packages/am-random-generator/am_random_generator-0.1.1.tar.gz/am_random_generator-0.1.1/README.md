# am-random-generator

A simple Python package to generate random numbers, characters or both of a given length.

## Installation

```bash
pip install am-random-generator
```

## Usage

```python
from randomgen import generate_random

# Generate both numbers and characters (default)
print(generate_random(8))  # e.g., "a2b9c4d8"

# Generate numbers only
print(generate_random(5, 'number'))  # e.g., "12345"

# Generate characters only
print(generate_random(10, 'char'))  # e.g., "abcdefghij"
```

## Development

To install the package locally for development:

```bash
git clone https://github.com/ashish4824/RandomValue.git
cd RandomValue
pip install -e .
```

## License

MIT License