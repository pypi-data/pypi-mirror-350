# WADAS Runtime

## Description

WADAS Runtime is a library designed to facilitate inference using OpenVINO for the Wild Animals Detection and Alert System (WADAS) project. It provides tools and utilities to streamline the decryption and execution of AI models.

## Usage

To use the WADAS Runtime library, follow these steps:

1. Install the library locally:

   ```bash
   pip install wadas_runtime
   ```

2. Import the library in your Python project:

   ```python
   import wadas_runtime as wadas
   ```

3. Load and compile the model. The library will decrypt the model in real time

   ```python
   import wadas_runtime as wadas

   xml, bin = # Path to the model XML and encrypted binary file
   compiled_model = wadas.load_and_compile_model(xml, bin, "GPU")
   ```

## Developer Guide

It is suggested to install the package locally by using `pip install -e .[dev]`. OpenSSL is required to build the package and needs to be installed separately.

### Git hooks

All developers should install the git hooks that are tracked in the `.githooks` directory. We use the pre-commit framework for hook management. The recommended way of installing it is using pip:

```bash
pre-commit install
```

If you want to manually run all pre-commit hooks on a repository, run `pre-commit run --all-files`. To run individual hooks use `pre-commit run <hook_id>`.

Uninstalling the hooks can be done using

```bash
pre-commit uninstall
```

## Testing the library

Python test uses `pytest` library. Type

```bash
cd test && pytest
```

to run the full test suite.

### Generate Python packets

To create packets run the following commands

```bash
python -m build --sdist
cibuildwheel --platform windows --output-dir dist
```

### Publishing packets

Then check on the built `sdist` and `wheel` that are properly formatted (all files should return a green PASSED)

```bash
twine check dist/*
```

Upload the packets to `testpypi`

```bash
twine upload --repository testpypi dist/*
```

To upload them to the real index (verify first with `testpypi`)

```bash
twine upload dist/*
```
