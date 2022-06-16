# Wrath & Glory Space Hulk Generator

The _Wrath & Glory Space Hulk Generator_ contains a random map generator for [Cubicle7](https://cubicle7games.com)'s
Warhammer
40k role-playing
game _[Wrath & Glory](https://cubicle7games.com/our-games/wrath-glory)_.

## State

Active Development

## Description

The code contains the generator as well as a streamlit app for a simple website hosting the generator.

The generator uses the random tables from [_Redacted Records_](https://cubicle7games.com/product/redacted-records) to
create the events and then pipes the rolled events into [graphviz](https://graphviz.org) to create a layout graph which
is rendered into a vectorized map.

### Use Cases

An initial analysis of the use cases for the generator is given in [USE_CASES.md](docs/USE_CASES.md).

## Installation

Currently, there is no stand-alone installation. To locally use the project, e.g. for making code changes, 

1. Install the repositories via [poetry](https://python-poetry.org) from [pyproject.toml](pyproject.toml)
2. Run the app via `streamlit run streamlit_app.py` from the repository root

## Contributing

If you have any improvement suggestions or feature requests or if you found bugs, simply open
an [issue](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/issues).

Or event better create
a [pull request](https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/pulls) (PR) with the
recommended code change.
If you create a PR, Please make sure to add/update the [unittests](tests) accordingly.

## License

See [LICENSE](LICENSE)
