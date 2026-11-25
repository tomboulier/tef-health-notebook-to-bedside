# Instructions for coding agents

This file is read by coding agents (see <https://agents.md>). It describes the
project, its architecture and its rules.

## What this project is

A chest-versus-abdomen radiograph classifier, moved from a Jupyter notebook
into a small Python package to teach software engineering practices. It is a
teaching example, not a medical device. Never claim otherwise in code or docs.

## Architecture (keep it)

`src/hello_world_medical_imaging/`:

- `config.py`: experiment settings from a TOML file (paths, hyperparameters, seed).
- `data.py`: data sources. Each returns `(train, validation)` datasets of RGB
  images in `[0, 255]` with binary labels. `load_image_datasets` reads the
  radiographs; `synthetic_datasets` generates noise images.
- `model.py`: builds and compiles the Keras model. Rescaling and augmentation
  are layers of the model.
- `training.py`: `train(model, train_dataset, validation_dataset, epochs)`. It
  receives the model and the data as arguments and knows nothing about files,
  downloads or configuration.
- `predict.py`: classifies one image with a trained model.
- `cli.py`: the only module that imports all the others and wires them
  together (the composition root).

The data source is injected into training. Keep that boundary: `training.py`
and `model.py` never read files or the configuration.

`notebooks/` holds a short demonstration that calls the package. Do not put
logic in it.

## Two guard-rails

- **KISS** (keep it simple): prefer a plain function to a class, and a class
  to a framework.
- **YAGNI** (you aren't gonna need it): do not add abstractions, options or
  layers for needs that do not exist in this repository yet.

## Commands

```bash
uv sync                                    # install the locked environment (Python 3.12)
uv run hello-world-medical-imaging         # train with config.toml
```

## Conventions

- Conventional Commits in English (`feat:`, `fix:`, `docs:`, `test:`,
  `refactor:`, `build:`, `ci:`, `chore:`).
- No data, model weights or notebook outputs in Git (`.gitignore`).
- Pin every new dependency to an exact version in `pyproject.toml` and run
  `uv lock`.
