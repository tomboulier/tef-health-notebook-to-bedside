# Contributing

Thank you for looking at this project. It is a teaching example: the goal is
code that stays small, readable and verifiable. Coding agents read
[`AGENTS.md`](AGENTS.md), which says the same things in their terms.

## Setting up

```bash
uv sync
```

This creates `.venv` with Python 3.12 and the exact dependency versions of
`uv.lock`, including the tools that check the code (pytest, Ruff, mypy).

## Architecture in one paragraph

`cli.py` reads `config.toml`, downloads the images (`data.py`), builds the
model (`model.py`) and hands both to `train()` (`training.py`). Training never
reads files or configuration itself: the data source is passed in, so the
tests replace the radiographs with synthetic images without touching the
model ([ADR 0001](docs/adr/0001-inject-the-data-source-into-training.md)).

## Two guard-rails

- **KISS** (keep it simple): prefer a plain function to a class, and a class
  to a framework.
- **YAGNI** (you aren't gonna need it): do not add abstractions, options or
  layers for needs this repository does not have yet.

## Before you commit

```bash
uv run ruff check . && uv run ruff format --check .
uv run mypy
uv run pytest
```

When you fix a bug or add behaviour, write the failing test first
([Testing](docs/testing.md)). Give every public function a docstring in the
Google style, with an example when it helps (pytest runs it), and report
progress with `logging`, not `print`. Record a decision that shapes the code
as a new [architecture decision record](docs/adr/index.md).

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/) in English:
`feat: ...`, `fix: ...`, `docs: ...`, `test: ...`, `refactor: ...`,
`build: ...`, `ci: ...`, `chore: ...`. One commit, one change.

## What never goes into Git

Images, model weights, training outputs and notebook outputs. The dataset is
downloaded at run time from its original repository. If you need to version
data, use a tool made for that, for example DVC or Git LFS.
