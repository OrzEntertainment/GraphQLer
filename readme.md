# GraphQLer

<p align="center">
  <img src="./docs/images/logo.png" />
</p>

[![Maintainability](https://api.codeclimate.com/v1/badges/a34db44e691904955ded/maintainability)](https://codeclimate.com/github/omar2535/GraphQLer/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a34db44e691904955ded/test_coverage)](https://codeclimate.com/github/omar2535/GraphQLer/test_coverage)
[![Tests](https://github.com/omar2535/GraphQLer/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/omar2535/GraphQLer/actions/workflows/tests.yml)
[![Lint](https://github.com/omar2535/GraphQLer/actions/workflows/lint.yml/badge.svg)](https://github.com/omar2535/GraphQLer/actions/workflows/lint.yml)

A stateful GraphQL API fuzzer with many inspirations from [Microsoft's RESTler fuzzer!](https://github.com/microsoft/restler-fuzzer)

## ⚒ Setup

Make sure to use python 3.11!

**Setting up the environment:**

```sh
# Creating the virtual environment
python3 -m venv .venv

# Activating the virtual environment
source .env/bin/activate
```

**Installing dependencies:**

```sh
(.env) pip install -r requirements.txt
```

**Setting up pre-commit hooks:**

```sh
(.env) pre-commit install
```

## ▶ Running the program

### Compile mode

```sh
(.env) python main.py --compile --url <URL> --path <SAVE_PATH>
```

### Fuzz mode

```sh
(.env) python main.py --fuzz --url <URL> --path <SAVE_PATH>
```

### Run mode

Runs both the Compile mode and Fuzz mode

```sh
(.env) python main.py --run --url <URL> --path <SAVE_PATH>
```

## 🧪 Testing

**Testing all files:**

```sh
(.env) pytest
```

**Testing a single file:**

```sh
(.env) pytest -q test_file.py
```
