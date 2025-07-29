# Installation

## Basic Installation

Install the package using pip:

```bash
pip install biocontext
```

## Development Setup

We use `uv` for dependency management and versioning. The script `bump.sh` is
used to bump the version and create a git tag, which then can be used to create
a release on GitHub that triggers publication to PyPI. It can be used with
semantic versioning by passing the bump type as an argument, e.g. `./bump.sh
patch`.

Adherence to best practices is ensured by a pre-commit hook that runs `ruff`,
`mypy`, and `deptry`. To check the code base at any time, run `make check` from
the terminal.

Docs are built using `mkdocs` (the [Material
theme](https://squidfunk.github.io/mkdocs-material/)); you can preview the docs
by running `uv run mkdocs serve`.
