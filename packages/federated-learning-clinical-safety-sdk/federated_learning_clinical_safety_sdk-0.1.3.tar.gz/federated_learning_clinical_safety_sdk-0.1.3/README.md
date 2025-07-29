# 🔧 Federated Learning Clinical Safety Server SDK

This is the documentation for the Federated Learning Clinical Safety Dashboard SDK! This project provides a package for interacting with the [Federated Learning Clinical Safety Dashboard Server](https://github.com/AlexDobsonPleming/federated-learning-clinical-safety-server) in a type-safe and easy manner.


[![CI](https://github.com/AlexDobsonPleming/federated-learning-clinical-safety-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/AlexDobsonPleming/federated-learning-clinical-safety-sdk/actions/workflows/ci.yml)

[![SDK ↔ Server Integration](https://github.com/AlexDobsonPleming/federated-learning-clinical-safety-sdk/actions/workflows/integration.yml/badge.svg)](https://github.com/AlexDobsonPleming/federated-learning-clinical-safety-sdk/actions/workflows/integration.yml)

[![📦 Publish to PyPI](https://github.com/AlexDobsonPleming/federated-learning-clinical-safety-sdk/actions/workflows/publish.yml/badge.svg)](https://github.com/AlexDobsonPleming/federated-learning-clinical-safety-sdk/actions/workflows/publish.yml)

## Using the SDK

The package is [available from PyPi](https://pypi.org/project/federated-learning-clinical-safety-sdk/).

### Installation

```bash
pip install federated-learning-clinical-safety-sdk
```

### Getting started

Read our [code examples](https://github.com/AlexDobsonPleming/federated-learning-clinical-safety-sdk/wiki/Code-examples) to get an idea of how to use this package.

## Development
### Prerequisites

Before you begin, ensure you have the following installed:

* Python 3.10+
* Poetry

#### Installing poetry

Windows NT
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

Then add to path:

```
%USERPROFILE%\AppData\Roaming\pypoetry\venv\Scripts
```

Linux/MacOS/Unix-like systems:
```bash
pipx install poetry
```

### Publishing new versions

This repo is set up with Continuous Deployment to automatically deploy new packages to PyPi.

To deploy a new version, do the following.

1. Bump the package version

```bash
poetry version patch
```

2. Create a matching git tag

```bash
git tag v<version number (i.e. 0.1.1)>
```

3. Push the tag to GitHub

```bash
git push origin v<version number from step 2 (i.e. 0.1.1)>
```

### Integration testing

To test the SDK works with the server integration testing with docker has been added.

This will also run as part of the GitHub CI platform.

```bash
export API_BASE_URL="http://localhost:8000/api"

export SDK_TEST_TOKEN=<token from your live instance>

poetry install

poetry run pytest src/tests/test_integration.py -q

```