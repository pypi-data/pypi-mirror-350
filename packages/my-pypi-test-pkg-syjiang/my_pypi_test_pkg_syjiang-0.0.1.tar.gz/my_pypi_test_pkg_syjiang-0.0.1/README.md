# My PyPI Test Package (Example)

This is a simple package created for testing the PyPI packaging and publishing process.

Remember to replace `example` in the package name and `pyproject.toml` with your unique identifier.

## Installation

Once published to TestPyPI (or PyPI):

```bash
# From TestPyPI
pip install -i https://test.pypi.org/simple/ my-pypi-test-pkg-example

# From PyPI (if you publish there)
# pip install my-pypi-test-pkg-example
```

## Usage

```python
from my_pypi_test_pkg_example import greet

print(greet("Your Name"))
``` 