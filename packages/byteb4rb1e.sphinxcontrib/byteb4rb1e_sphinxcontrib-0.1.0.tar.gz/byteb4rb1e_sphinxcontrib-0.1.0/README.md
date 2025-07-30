

## Installation

You must either provide a `pipenv` command system-wide, or bootstrap the build
environment manually.

### Bootstrap Development Environment

### via Pipenv

```sh
$> python3 -m pipenv install -d
```

### via pip

```sh
$> python3 -m pip install -r requirements-dev.txt
```

### via venv

```sh
$> python3 -m venv .venv
```

```sh
$> .venv/bin/python3 -m pip install -r requirements-dev.txt
```

```sh
$> python3 -m pipenv run sh ./configure
```
