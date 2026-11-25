# The notebook

`tuto-hello-world-deep-learning-medical-imaging.ipynb` started as a
transcription with Keras, written in April 2021, of the tutorial by Lakhani
et al. (Journal of Digital Imaging, 2018,
<https://doi.org/10.1007/s10278-018-0079-6>). Its code now lives in the
`hello_world_medical_imaging` package (`src/`), and the notebook is a short
demonstration that calls it: training on the radiographs, then the same
training on synthetic images.

To open it, or to run it from top to bottom without a browser:

```bash
uv sync --group notebook
uv run --group notebook --with jupyterlab jupyter lab
uv run --group notebook papermill --cwd notebooks \
    notebooks/tuto-hello-world-deep-learning-medical-imaging.ipynb \
    outputs/tuto-hello-world-deep-learning-medical-imaging.ipynb
```

Earlier versions are at the Git tags of the repository:

- `step-0-notebook`: the notebook as it was published, for TensorFlow 2.4 and
  Keras 2. With the versions pinned in `uv.lock` (TensorFlow 2.21.0,
  Keras 3.15.1), it stops at its first code cell with
  `ImportError: cannot import name 'ImageDataGenerator' from 'keras.preprocessing.image'`.
- `step-2-reproducible-environment`: the same notebook ported to Keras 3,
  with two defects of the original fixed (Adam's `epsilon` was `1e08` instead
  of `1e-08`, and the validation images were augmented like the training
  ones), its configuration in `config.toml`, and the images downloaded when
  they are missing.
