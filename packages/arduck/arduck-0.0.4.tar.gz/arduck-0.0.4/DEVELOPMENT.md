
# Development Guide

Before diving into the code, you should first take the time to make sure you have an environment where you can execute the Python package.
The lowest supported Python version for my projects is _usually_ 3.12, but don't take my word for it and check the [README](README.md) file.

> [!NOTE]
> If the project version is for example 3.12+, **all** subsequent Python versions should be supported.


## Package Installation

To install the package locally, clone the repository and run `pip install`:

```bash
$ git clone https://github.com/x55xaa/arduck.git
$ cd arduck
$ pip install .
```


> [!TIP]
> Install the project in [editable mode](https://setuptools.pypa.io/en/latest/userguide/development_mode.html) with the `-e` option.
>
> ```bash
> $ pip install -e .
> ```

All required dependencies will be automatically installed.

> [!IMPORTANT]
> This project is built using [setuptools](https://setuptools.pypa.io/en/latest/userguide/) and [setuptools_scm](https://pypi.org/project/setuptools-scm/). All package information is stored in the [pyproject.toml](pyproject.toml) file.


## Code Style

It is advised to adhere to the recommendations in the [Google Python style guide](https://google.github.io/styleguide/pyguide.html), or at the very least, follow the [consistency principle](https://google.github.io/styleguide/pyguide.html#4-parting-words).
Readability and maintainability should be your top priorities when writing new code.


## Linters

This project uses [ruff](https://docs.astral.sh/ruff/linter/) as its main code linter:

```bash
$ ruff check src
```

> [!NOTE]
> The secondary linter for this project is [pylint](https://pylint.readthedocs.io/en/latest/user_guide/usage/run.html), although its output is not enforced. Pylint recommendations should be viewed more as _suggestions_, aiding the developer in writing clean code.


## Making changes to the Documentation

The project's documentation is generated using [Sphinx](https://www.sphinx-doc.org/en/master/).

To install the necessary dependencies to build the docs, run:

```bash
$ pip install .[docs]
```


## Testing your Code

This project uses [pytest](https://docs.pytest.org/en/latest/getting-started.html) to run unit tests.
New code should be tested, by adding the relevant test files to the `tests` directory.
While it is certainly advised, it is not mandatory to test all code; just be mindful of the coverage report, and try not to lower the overall test coverage of the package.

To start testing, install the required packages by running:

```bash
$ pip install .[testing]
```


## Testing in Different Environments

Testing under multiple environments is done using [tox](https://tox.wiki/en/latest):

```bash
$ tox
```

All the configuration settings for tox are stored in the [tox.ini](tox.ini) file.

> [!NOTE]
> Since tox runs automatically on `push` and `pull requests` (see [this](.github/workflows/tests.yaml) workflow), it is recommended to run it locally before committing.
