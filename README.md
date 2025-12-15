# Wrath & Glory Space Hulk Generator

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/lordfckhelmchen/wrath-and-glory-space-hulk-generator/main)
![release (latest SemVer)](https://img.shields.io/github/v/release/LordFckHelmchen/wrath-and-glory-space-hulk-generator?sort=semver)
[![Code checks](https://img.shields.io/github/actions/workflow/status/LordFckHelmchen/wrath-and-glory-space-hulk-generator/code_checks.yml?label=checks)](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/actions/workflows/code_checks.yml)
[![Coverage Status](https://coveralls.io/repos/github/LordFckHelmchen/wrath-and-glory-space-hulk-generator/badge.svg?branch=djm/add_pytest)](https://coveralls.io/github/LordFckHelmchen/wrath-and-glory-space-hulk-generator?branch=djm/add_pytest)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![prek](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/j178/prek/master/docs/assets/badge-v0.json)](https://github.com/j178/prek)

The _Wrath & Glory Space Hulk Generator_ contains a random map generator for [Cubicle7](https://cubicle7games.com)'s
Warhammer 40k role-playing game _[Wrath & Glory](https://cubicle7games.com/our-games/wrath-glory)_.

## State

Maintained

## Description

This repository contains the generator as well as the app that is hosted at the
[Streamlit app](https://share.streamlit.io/lordfckhelmchen/wrath-and-glory-space-hulk-generator/main).

A description of the app is given in [APP_ABOUT.md](docs/APP_ABOUT.md).

### Use Cases

An initial analysis of the use cases for the generator is given in [USE_CASES.md](docs/USE_CASES.md).

## Installation

Currently, there is no stand-alone installation. To locally use the project, e.g. for making code changes,

1. Install the external dependencies from [packages.txt](packages.txt) (e.g. the graphviz backend)
2. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
3. Run the app via `uv run streamlit run streamlit_app.py` from the repository root

## Contributing

If you have any improvement suggestions or feature requests or if you found bugs, simply open an
[issue](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/issues).

Or event better create a [pull request](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/pulls)
(PR) with the recommended code change. If you create a PR, Please make sure to add/update the [unittests](tests)
accordingly.

### Unittests

Run the unittests via pytest + coverage with:

```bash
uv run pytest --cov
```

### Linting & Formatting

[Prek](https://prek.j178.dev) is used for linting and formatting the code via pre-commit hooks. To run the checks
manually, use:

```bash
prek run --all-files
```

## License

See [LICENSE](LICENSE)
