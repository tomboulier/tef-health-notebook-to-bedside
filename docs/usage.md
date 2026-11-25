# Usage

How to install, configure and run the training, on a workstation or on a
cluster.

## Install

Requirements: Python 3.12 and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/tomboulier/tef-health-notebook-to-bedside.git
cd tef-health-notebook-to-bedside
uv sync
```

`uv sync` creates a virtual environment in `.venv` with the exact versions
recorded in `uv.lock`. Direct dependencies are pinned in `pyproject.toml`;
`uv.lock` pins every transitive dependency too, so two people running
`uv sync` get the same environment. `.python-version` tells uv which Python
to use, and uv downloads it if needed.

Without uv: `python -m venv .venv && . .venv/bin/activate && pip install -e .`
(the direct dependencies are pinned, the transitive ones are not).

## Configure

`config.toml` holds everything that used to be a global variable in the
notebook: where the images are downloaded from and to, where the results go,
image size, batch size, number of epochs, learning rate, data augmentation
ranges and the random seed. Copy it, edit the copy, and pass it with
`--config`:

```bash
uv run hello-world-medical-imaging --config my-experiment.toml
```

A setting absent from the file keeps its default (see
`src/hello_world_medical_imaging/config.py`); an unknown setting, such as a
misspelt name, stops the program with an error. Paths are relative to the
folder the command is run from.

The seed is applied to Python, NumPy and TensorFlow. On a CPU, two runs with
the same seed and the same environment give the same numbers, in the
container as on the host. On a GPU, some operations stay non-deterministic
unless TensorFlow is told otherwise.

## Run

```bash
uv run hello-world-medical-imaging
```

On the first run the 75 radiographs are downloaded from the original tutorial
repository into `data/` (ignored by Git), and Keras downloads the ImageNet
weights of Inception V3 into its cache. The results are the trained model
(`outputs/model.keras`), the training curves (`outputs/training_curves.png`)
and, in the log, the score and predicted class of the two test images.

The demonstration notebook calls the same functions:

```bash
uv sync --group notebook
uv run --group notebook --with jupyterlab jupyter lab
```

## Run the same image with Docker on a workstation

The `Dockerfile` builds an image with Python 3.12 and the locked
dependencies. Build it once:

```bash
docker build --tag hello-world-medical-imaging .
```

Train, keeping the data and the outputs on the host:

```bash
docker run --rm \
  --volume "$PWD/data:/app/data" \
  --volume "$PWD/outputs:/app/outputs" \
  hello-world-medical-imaging
```

Run the tests inside the image:

```bash
docker run --rm hello-world-medical-imaging pytest
```

[Podman](https://podman.io/), which needs no daemon, accepts the same commands
with `podman` in place of `docker`.

## Run the same image with Apptainer on a cluster

Computing clusters usually do not allow Docker but provide
[Apptainer](https://apptainer.org/), which runs Docker images without a
daemon or administrator rights. The GRICAD computing centre in Grenoble, for
example, documents this use (<https://gricad-doc.univ-grenoble-alpes.fr/>).

Apptainer pulls the image from a registry. If the image has been pushed, for
example to the GitHub Container Registry as
`ghcr.io/tomboulier/tef-health-notebook-to-bedside`, then on the cluster:

```bash
apptainer exec docker://ghcr.io/tomboulier/tef-health-notebook-to-bedside:latest \
  hello-world-medical-imaging --config config.toml
```

`apptainer exec` mounts the current folder, so `config.toml`, `data/` and
`outputs/` are read and written where the command is launched. Add `--nv` to
use the node's GPUs. This repository does not push the image to a registry.

Without a registry, build the image on a machine that has Docker, convert it
to a single file and copy that file to the cluster:

```bash
apptainer build hello-world-medical-imaging.sif docker-daemon://hello-world-medical-imaging:latest
apptainer exec hello-world-medical-imaging.sif hello-world-medical-imaging --config config.toml
```
