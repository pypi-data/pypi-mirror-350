# OpenShift Operator Installation Tool

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenShift Compatible](https://img.shields.io/badge/OpenShift-4.x-lightgrey.svg)

A Python CLI tool for installing and managing OpenShift operators with parallel installation support.

## 📋 Table of Contents
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [How It Works](#-how-it-works)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## ✨ Features
- Install single or multiple OpenShift operators
- Parallel installation for faster deployments
- Configurable timeouts and retries
- Detailed logging to `test.log`
- Supports:
  - Serverless Operator
  - Service Mesh Operator  
  - Authorino Operator

## 📂 Project Structure
```
O
.
├── cli/                    # Command-line interface components
│   ├── args.py            # Command line argument parsing
│   ├── commands.py        # CLI command implementations
│   └── __init__.py
├── logger/                # Logging functionality
│   ├── logger.py          # Logging configuration
│   └── __init__.py
├── utils/                 # Core utilities
│   ├── operator/
│   │   ├── operator.py    # Core operator logic
│   │   ├── cleanup.py     # Cleanup utilities
│   │   └── __init__.py
│   ├── utils.py           # Utility functions
│   ├── constants.py       # Constants and configurations
│   └── __init__.py
├── scripts/               # Utility scripts
│   └── cleanup/          # Cleanup and maintenance scripts
│       ├── cleanup_all.sh
│       └── remove_image_from_worker_node.sh
├── rhoai_upgrade_matrix/  # RHOAI upgrade testing utilities
│   ├── cli.py            # Upgrade matrix CLI
│   └── __init__.py
├── main.py                # CLI entry point
├── run_upgrade_matrix.sh  # Upgrade matrix execution script
├── upgrade_matrix_usage.md # Upgrade matrix documentation
├── README.md              # This document
├── pyproject.toml         # Project dependencies
└── test.log              # Generated log file
```

## 📋 Components

### Core Components
- **CLI**: Command-line interface implementation for operator management
- **Logger**: Logging configuration and utilities
- **Utils**: Core utilities and operator management logic

### RHOAI Components
- **RHOAI Upgrade Matrix**: Utilities for testing RHOAI upgrades
- **Upgrade Matrix Scripts**: Execution and documentation for upgrade testing

### Maintenance Scripts
- **Cleanup Scripts**: Utilities for cleaning up operator installations and related resources
- **Worker Node Scripts**: Utilities for managing worker node configurations

## 📋 Additional Components

### RHOAI Upgrade Matrix
The `rhoai_upgrade_matrix/` directory contains utilities for testing RHOAI upgrades. See `upgrade_matrix_usage.md` for detailed documentation.

### Cleanup Utilities
The `utils/operator/cleanup.py` and `cleanup_all.sh` provide utilities for cleaning up operator installations and related resources.

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/mwaykole/O.git
cd O
```
2. Install dependencies:
```
pip install -e .    
```
3. Verify installation:
```
python main.py --help
💻 Usage
```

```
# Install single operator
python main.py --serverless

# Install multiple operators
python main.py --serverless --servicemesh

# Install kserve raw config
python main.py --rhoai --rhoai-channel=<channel> --rhoai-image=<image> --raw=True

# Install kserve Serverles config

python main.py --rhoai --rhoai-channel=<channel> --rhoai-image=<image> --raw=False --all

# Install all operators 
python main.py --all

# create dsc and dsci with rhoai operator installarion
python main.py --rhoai --rhoai-channel=<channel> --rhoai-image=<image> --raw=False --deploy-rhoai-resources

# Verbose output
python main.py --all --verbose
```
# Advanced Options

```
# Custom oc binary path
python main.py --serverless --oc-binary /path/to/oc

# Custom timeout (seconds)
python main.py --all --timeout 900

# View logs
tail -f test.log

```

