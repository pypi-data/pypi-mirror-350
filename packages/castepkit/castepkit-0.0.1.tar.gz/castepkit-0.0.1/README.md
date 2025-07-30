# GAUSSPY
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://docs.python.org/3.10/)


[`GAUSSPY`](https://github.com/yingxingcheng/castepkit) is a Python package that process outputs of CASTEP program.

## License

![GPLv3 License](https://img.shields.io/badge/license-GPLv3-blue.svg)


`castepkit` is distributed under GPL License version 3 (GPLv3).


## Installation

To install `castepkit` with version `0.0.x`:

```bash
pip install castepkit
```

To install latest `castepkit`:

```bash
git clone http://github.com/yingxingcheng/castepkit
cd castepkit
pip install .
```

To run test, one needs to add tests dependencies for `tests`:

```bash
pip install .[tests]
```

For developers, one could need all dependencies:
```bash
pip install -e .[dev,tests]
```
