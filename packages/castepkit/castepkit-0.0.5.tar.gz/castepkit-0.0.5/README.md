# CASTEPKIT

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![GPLv3 License](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)

[`castepkit`](https://github.com/yingxingcheng/castepkit) is a Python package that provides a unified CLI and programmatic interface for post-processing and analyzing output files from the [CASTEP](https://www.castep.org/) first-principles simulation software. It provides wrappers for multiple CASTEP auxiliary programs such as `NewSHG_ZY-XTIPC.x`, `weighted_den.x`, and supports seamless integration of additional tools like `atom_cutting_impi_XTIPC`, `calculate_ome_impi_XTIPC`, and more.

---

## Features

* Unified CLI for running various CASTEP-related post-processing executables
* Configurable executable paths and MPI launch settings via a user config file
* Modular architecture: easily extendable for additional tools
* Compatible with Python 3.10+

---

## Installation

### Stable version (from PyPI):

```bash
pip install castepkit
```

### Development version (from GitHub):

```bash
git clone https://github.com/yingxingcheng/castepkit
cd castepkit
pip install .
```

### Editable mode for developers:

```bash
pip install -e .[dev,tests]
```

### To run tests:

```bash
pip install .[tests]
pytest
```

---

##  User Configuration

You can configure executable names, MPI settings, and default parameters using a TOML config file:

**Config path**:
Linux/macOS: `~/.config/castepkit/config.toml`
Windows: `%APPDATA%\castepkit\config.toml`

### Example `config.toml`:

```toml
[executables]
shg = "/opt/bin/NewSHG_ZY-XTIPC.x"
weighted_den = "/opt/bin/weighted_den.x"

[mpirun]
enabled = true
nproc = 8
```

---

## Example Usage

```bash
# Run SHG alone
castepkit-shg GaAs_Optics --scissors 0.8 --direction 111

# Run weighted_den.x for a single file
castepkit-dens run GaAs_Optics --input_file_suffix shg_weight_veocc

# Run for both veocc and veunocc weights
castepkit-dens ve GaAs_Optics

# Run full SHG pipeline + weighted density
castepkit-dens shg GaAs_Optics --scissors 0.8 --direction 111
```

---

## License

`castepkit` is distributed under the terms of the [GNU General Public License v3](https://www.gnu.org/licenses/gpl-3.0.html).
