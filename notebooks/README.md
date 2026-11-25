# The notebook

`tuto-hello-world-deep-learning-medical-imaging.ipynb` is a transcription with
Keras, written in April 2021, of the tutorial by Lakhani et al. (Journal of
Digital Imaging, 2018, <https://doi.org/10.1007/s10278-018-0079-6>). Its
outputs are cleared: they contained two radiographs from the dataset, which
is not stored in this repository.

The notebook was written for TensorFlow 2.4 and Keras 2, in an environment
that was never written down. Run as it was with the versions pinned in
`pyproject.toml` and `uv.lock` (TensorFlow 2.21.0, Keras 3.15.1), it stops at
its first code cell:

```
ImportError: cannot import name 'ImageDataGenerator' from 'keras.preprocessing.image'
```

It now runs with these versions, after three changes:

- a port to Keras 3, which no longer has `ImageDataGenerator`: the images are
  read with `image_dataset_from_directory`, and the same random
  transformations are done by preprocessing layers;
- two fixes of the original: Adam's `epsilon` was `1e08` instead of `1e-08`,
  and the validation images were augmented like the training ones;
- the configuration (paths, hyperparameters, random seed) is read from
  `config.toml`, and the images are downloaded when they are missing.

The notebook as it was published is at the Git tag `step-0-notebook`.
