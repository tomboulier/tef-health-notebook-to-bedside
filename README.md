[![CI](https://github.com/tomboulier/tef-health-notebook-to-bedside/actions/workflows/ci.yml/badge.svg)](https://github.com/tomboulier/tef-health-notebook-to-bedside/actions/workflows/ci.yml)
[![Documentation](https://github.com/tomboulier/tef-health-notebook-to-bedside/actions/workflows/docs.yml/badge.svg)](https://tomboulier.github.io/tef-health-notebook-to-bedside/)

# From notebook to bedside

This repository is the worked example of a capsule of the TEF-Health training
course, *Best Practices in Software Engineering for Robust and Maintainable
Medical AI*. It starts from a Jupyter notebook that trains a deep learning
model on radiographs, and takes it, one step at a time, towards code that is
reproducible, tested, documented and checked automatically.

The starting point is a transcription with Keras of the tutorial *Hello World
Deep Learning in Medical Imaging* (Lakhani et al., Journal of Digital
Imaging, 2018,
[doi:10.1007/s10278-018-0079-6](https://doi.org/10.1007/s10278-018-0079-6);
original code and images at
[paras42/Hello_World_Deep_Learning](https://github.com/paras42/Hello_World_Deep_Learning)).
It fine-tunes Inception V3, pre-trained on ImageNet, to tell chest
radiographs from abdominal ones.

The companion page of the capsule, with the six steps, their readings and
links to the code at each step, is published at
<https://tomboulier.github.io/tef-health-notebook-to-bedside/>.

> This is a teaching example. It is not a medical device and must not be used
> to make any decision about a patient.

## The steps

Each step of the capsule is a series of
[Conventional Commits](https://www.conventionalcommits.org/) that ends with a
Git tag. Check out a tag to see the repository as it was at the end of that
step, and compare two tags to see what the step changed
(`git diff step-2-reproducible-environment step-3-architecture`).

| Tag | What the step adds |
|---|---|
| `step-0-notebook` | The original notebook, as published |
| `step-1-version-control` | `.gitignore` for data, weights, outputs and environments |
| `step-2-reproducible-environment` | Pinned dependencies, `config.toml`, a container; the notebook ported to Keras 3 |
| `step-3-architecture` | The `hello_world_medical_imaging` package, with the data source injected into training |
| `step-4-tests` | Unit tests, an offline integration test, doctests, Ruff and mypy |
| `step-5-documentation` | Docstrings, logging, a decision record, usage and testing guides |
| `step-6-automation` | Continuous integration, the documentation site, versions and changelog from the commits |

## Install

Requirements: Python 3.12 and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/tomboulier/tef-health-notebook-to-bedside.git
cd tef-health-notebook-to-bedside
uv sync
```

`uv sync` creates `.venv` with the exact dependency versions recorded in
`uv.lock`.

## Usage

Train with the settings of [`config.toml`](config.toml) (the images are
downloaded on the first run):

```bash
uv run hello-world-medical-imaging
uv run hello-world-medical-imaging --config my-experiment.toml
```

The trained model and the training curves are written to `outputs/`; the log
reports the prediction for each of the two test images. The same runs in a
container:

```bash
docker build --tag hello-world-medical-imaging .
docker run --rm --volume "$PWD/data:/app/data" --volume "$PWD/outputs:/app/outputs" \
    hello-world-medical-imaging
```

[docs/usage.md](docs/usage.md) gives the details, including Podman and
Apptainer on a computing cluster. The demonstration notebook is described in
[notebooks/README.md](notebooks/README.md).

## Checking the code

```bash
uv run pytest                  # unit tests, integration test and doctests
uv run ruff check .            # lint
uv run ruff format --check .   # formatting
uv run mypy                    # types
uv run --group docs mkdocs build --strict   # documentation site
```

The same checks run on GitHub Actions on every push and pull request, and
every week; versions and [`CHANGELOG.md`](CHANGELOG.md) are derived from the
commit messages ([docs/automation.md](docs/automation.md)).

The tests need neither the network nor the radiographs; see
[docs/testing.md](docs/testing.md).

## Layout

```
src/hello_world_medical_imaging/   the package: config, data, model, training, predict, cli
tests/                             pytest suite
notebooks/                         a short demonstration of the package
docs/                              companion page (MkDocs site), usage, testing, automation, decision records
.github/workflows/                 continuous integration, documentation site, releases
config.toml                        experiment settings
Dockerfile                         image that runs the training or the tests
AGENTS.md, CONTRIBUTING.md         architecture and rules, for coding agents and for people
```

## Version control

Everything needed to understand and rerun the work is in Git; nothing that
can be regenerated, or that is too large, is. Notebook outputs are cleared
before a commit (*Edit > Clear All Outputs* in Jupyter, or a tool such as
[nbstripout](https://github.com/kynan/nbstripout)). Data, model weights and
outputs are listed in [`.gitignore`](.gitignore). When large files do need to
be versioned, use a tool made for them, such as [DVC](https://dvc.org) or
[Git LFS](https://git-lfs.com).

## Data

The 75 radiographs used by the tutorial are not stored in this repository.
They are downloaded at run time from the original tutorial repository, which
describes them as de-identified images from
[Open-i](https://openi.nlm.nih.gov/) and states no licence for them. Notebook
outputs are cleared before a commit for the same reason.

The download is checked against the SHA-256 checksum given in `config.toml`,
so that a result can always be traced to the exact data it was obtained
with. The same archive is preserved by
[Software Heritage](https://www.softwareheritage.org/); `config.toml` gives
its address, to use if the original repository ever disappears.

## Citing

Version 1.0.1 is the one presented in the TEF-Health video. To cite the
repository, use the *Cite this repository* button on GitHub, which reads
[`CITATION.cff`](CITATION.cff).

## Licence

- The code is licensed under the MIT licence ([`LICENSE`](LICENSE)).
- The documentation (the README files, the `docs/` folder and the text cells
  of the notebook) is licensed under the Creative Commons
  Attribution-ShareAlike 4.0 International licence, CC BY-SA 4.0
  ([`LICENSE-docs`](LICENSE-docs),
  <https://creativecommons.org/licenses/by-sa/4.0/>).
- The radiographs are not part of this repository and are covered by neither
  licence.

The original notebook transcribes the code of the tutorial by Lakhani et al.;
see the article and the original repository for the terms of that material.
That tutorial is very good work: read the article, and run the original
notebook, which comes with its images and runs on its own.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md), and [AGENTS.md](AGENTS.md) for coding
agents.
