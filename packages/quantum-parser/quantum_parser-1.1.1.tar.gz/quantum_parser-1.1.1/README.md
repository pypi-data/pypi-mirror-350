# Quantum Parser

<!-- SPHINX-START -->

This project provides modules for parsing quantum circuits.

## Overview

- **qcis_parser**: A parser for QCIS format, offering similar functionalities for a different quantum circuit representation.

- **qasm2_parser**: A parser for OpenQASM 2.0 code, converting it into tokenized instructions and extracting circuit information.

## Installation

Clone the repository and install the required dependencies using nix flake:

```bash
nix develop .
```

## Usage

See APIs.

## Features

### QSIC Parser

- Parses QSIC format circuits.
- Provides a similar tokenization and analysis interface.

### QASM2 Parser

- Parses OpenQASM 2.0 code.
- Extracts quantum operations into a token list.
- Currently does not support classical operations or measurements.

## Notes

- Ensure that the input strings conform to the expected format for each parser.
- The parsers are currently in development and may not support all features or operations.
