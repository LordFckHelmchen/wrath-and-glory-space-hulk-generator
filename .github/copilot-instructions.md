# Copilot Instructions: Wrath & Glory Space Hulk Generator

## Project Overview

**Python Streamlit web application** that generates random Space Hulk maps for Warhammer 40k RPG "Wrath & Glory". Uses
random tables from Redacted Records rulebook and renders maps using Graphviz (vector) or DeBroglie (bitmap tiles).

**Frameworks**: Streamlit, Graphviz, Pydantic

## Build & Development Workflow

### Prerequisites (Install First)

1. **graphviz**: `sudo apt-get install graphviz` (listed in packages.txt)
2. **uv**: Install from https://docs.astral.sh/uv/ (version 0.9.x+)

### Setup Commands (in order)

**IMPORTANT**: Always run these commands from the repository root directory.

1. **Sync dependencies**: `uv sync` (~3-5s, creates `.venv/`, run before other uv commands)
2. **Run tests** (REQUIRED): `uv run pytest --cov` (~7s, 30 tests, ≥74% coverage required, all must pass)
3. **Run linting** (REQUIRED): `prek run --all-files` (~10-15s, runs ruff/mdformat/yaml/toml/json checks)
4. **Run app**: `uv run streamlit run streamlit_app.py` (port 8501, use `--server.headless=true` for testing)

### Command Order for Changes

1. Make changes
2. `uv run pytest --cov` (REQUIRED)
3. `prek run --all-files` (REQUIRED)
4. Commit

**NEVER skip steps 2-3** - CI will fail.

## CI/CD Pipeline

**unittest.yml**, **linting.yml** (PRs and main): Unittests (pytest + Coveralls) and Linting (prek) run in parallel.
Both must pass.

**release.yml** (main only): Python Semantic Release versioning, updates uv.lock. Requires conventional commits. Uses
`uvx python-semantic-release version` to update the version, tag the release commit, generate CHANGELOG.md, and create
GitHub releases.

## Project Structure

```
streamlit_app.py              # Main app entry point
src/generator/                # Space hulk generation (random tables, dice)
  space_hulk_generator.py     # Main generator class
  space_hulk.py               # Space hulk data model (Pydantic)
src/layouter/                 # Layout engines
  graphviz_layouter/          # Vector map renderer
  de_broglie_layouter/        # Bitmap tile-based renderer
src/app/layout_file_creator.py # PDF/image export
tests/                        # 30 tests
pyproject.toml                # Config: deps, tools, Python 3.13, coverage 74%
.pre-commit-config.yaml       # Pre-commit hooks
.streamlit/config.toml        # Port 8501, dark theme
packages.txt                  # System deps (graphviz)
```

## Architecture

**Data Flow**: `SpaceHulkGenerator` → random tables → `SpaceHulk` (Pydantic) → `ICreateLayouts` → `ILayout` → PDF/PNG

**Key Classes**: `SpaceHulkGenerator`, `SpaceHulk`, `GraphvizLayouter`, `DeBroglieLayouter`

**Tests**: 30 pytest tests, 74% min coverage. `test_app.py` starts server + curls (~5s). `src/app/` modules uncovered
(acceptable).

## Code Style

**Ruff**: 120 char lines, Python 3.13, single-line imports, NumPy docstrings. TODOs allowed, no TYPE_CHECKING blocks.
Run via `prek run ruff-format`.

## Common Issues & Workarounds

1. **Graphviz not found**: `sudo apt-get install graphviz`
2. **Python version mismatch**: Requires 3.13.0+
3. **DeBroglie subprocess**: Uses `check=False` (de_broglie_layouter.py:46, Issue #28)

`.venv/` auto-created by `uv sync`. Use `uv` only. `uv.lock` synced by pre-commit hook.

## Making Changes

**Tests**: Always add/update for `src/generator/` or `src/layouter/` changes. Mirror structure: `src/foo/bar.py` →
`tests/test_bar.py`. Maintain ≥74% coverage.

**Docs**: Update `docs/APP_*.md` for user-facing changes, README for setup changes. CHANGELOG auto-generated.

**Commits**: REQUIRED format: `<type>: <subject>`. Types: `build`, `chore`, `ci`, `docs`, `feat`, `fix`, `refactor`,
`revert`, `test`. Example: `feat: add room type`

**Pre-commit hooks**: Conventional commits, ruff, yaml/toml/json, uv-lock, uv-sync, mdformat. Manual:
`prek run --all-files`.

## Trust These Instructions

**This file contains verified, tested information.** Only search the codebase if:

- Information here is incomplete or unclear
- You need to understand implementation details not covered
- These instructions are found to be incorrect (please report!)

**Do not waste time re-discovering:**

- How to run tests (documented above)
- How to run linting (documented above)
- Project structure (documented above)
- CI requirements (documented above)

Focus your exploration on the specific task at hand, using these instructions as your foundation.
