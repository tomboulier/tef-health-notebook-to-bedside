# From notebook to bedside

This repository is the worked example of a capsule of the TEF-Health training
course, *Best Practices in Software Engineering for Robust and Maintainable
Medical AI*. It starts from a Jupyter notebook that trains a deep learning
model on radiographs, and takes it, one step at a time, towards code that is
reproducible, tested, documented and checked automatically.

The notebook in [`notebooks/`](notebooks/) is a transcription with Keras of
the tutorial *Hello World Deep Learning in Medical Imaging* (Lakhani et al.,
Journal of Digital Imaging, 2018,
[doi:10.1007/s10278-018-0079-6](https://doi.org/10.1007/s10278-018-0079-6);
original code and images at
[paras42/Hello_World_Deep_Learning](https://github.com/paras42/Hello_World_Deep_Learning)).
It fine-tunes Inception V3, pre-trained on ImageNet, to tell chest radiographs
from abdominal ones.

Each step of the capsule is a series of commits that ends with a Git tag:
`step-1-version-control`, `step-2-reproducible-environment`,
`step-3-architecture`, `step-4-tests`, `step-5-documentation` and
`step-6-automation`. Check out a tag to see the repository as it was at the
end of that step.

> This is a teaching example. It is not a medical device and must not be used
> to make any decision about a patient.

## Running the notebook

The environment is described in files, so that it can be rebuilt anywhere:
[`.python-version`](.python-version) (Python 3.12),
[`pyproject.toml`](pyproject.toml) (direct dependencies, pinned to exact
versions) and [`uv.lock`](uv.lock) (every transitive dependency, pinned too).
With [uv](https://docs.astral.sh/uv/):

```bash
uv sync                                    # create .venv with the locked versions
uv run --with jupyterlab jupyter lab       # open the notebook in a browser
```

Paths, hyperparameters and the random seed are in
[`config.toml`](config.toml), not in the code. The notebook downloads the
images into `data/` on its first run. To run it from top to bottom without a
browser, with [papermill](https://papermill.readthedocs.io/), and keep the
executed copy with its outputs:

```bash
mkdir -p outputs
uv run papermill --cwd notebooks \
    notebooks/tuto-hello-world-deep-learning-medical-imaging.ipynb \
    outputs/tuto-hello-world-deep-learning-medical-imaging.ipynb
```

Add `-p config_file my-experiment.toml` to use another configuration (a
path relative to `notebooks/`, or an absolute one).

The [`Dockerfile`](Dockerfile) packages the same environment in a container
image that runs the notebook in the same way, on any machine with Docker:

```bash
docker build --tag hello-world-medical-imaging .
docker run --rm \
    --volume "$PWD/data:/app/data" --volume "$PWD/outputs:/app/outputs" \
    hello-world-medical-imaging
```

[Podman](https://podman.io/) accepts the same commands. On a computing cluster,
where Docker is usually not available,
[Apptainer](https://apptainer.org/) runs the same image.

## Version control

Everything needed to understand and rerun the work is in Git; nothing that
can be regenerated or that is too large is.

- **Commits** follow [Conventional Commits](https://www.conventionalcommits.org/)
  (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `build:`, `ci:`,
  `chore:`), so that `git log --oneline` reads as the history of the work.
- **Notebook outputs** are cleared before a notebook is committed (*Edit >
  Clear All Outputs* in Jupyter, or a tool such as
  [nbstripout](https://github.com/kynan/nbstripout)): outputs make diffs
  unreadable and can leak data.
- **Data, model weights and outputs** are listed in [`.gitignore`](.gitignore).
  When large files do need to be versioned, use a tool made for them, such as
  [DVC](https://dvc.org) (data and models stored next to the code, in a remote
  of your choice) or [Git LFS](https://git-lfs.com) (large files stored outside
  the Git history).

## Data

The 75 radiographs used by the tutorial are not stored in this repository.
They come from the original tutorial repository, which describes them as
de-identified images from [Open-i](https://openi.nlm.nih.gov/) and states no
licence for them. The notebook's outputs were cleared for the same reason: they
contained two of these images.

## Licence

- The code is licensed under the MIT licence ([`LICENSE`](LICENSE)).
- The documentation (the README files and the text cells of the notebook) is
  licensed under the Creative Commons Attribution-ShareAlike 4.0
  International licence, CC BY-SA 4.0 ([`LICENSE-docs`](LICENSE-docs),
  <https://creativecommons.org/licenses/by-sa/4.0/>).
- The radiographs are not part of this repository and are covered by neither
  licence.

The notebook transcribes the code of the tutorial by Lakhani et al.; see the
article and the original repository for the terms of that material.
