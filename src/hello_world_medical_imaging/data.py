"""Where the images come from.

A data source returns a pair of (training, validation) datasets whose
elements are batches of RGB images with pixel values in [0, 255] and binary
labels (0 for chest, 1 for abdomen). Two sources honour that contract: the
radiographs of the tutorial, and synthetic images. The training code works
with either.
"""

from __future__ import annotations

import tempfile
import urllib.request
import zipfile
from pathlib import Path

import keras
import numpy as np
import tensorflow as tf

# Sub-directories of the dataset, as shipped in the tutorial's zip archive.
TRAIN_SUBDIRECTORY = "TRAIN"
VALIDATION_SUBDIRECTORY = "VAL"
TEST_SUBDIRECTORY = "TEST"

DatasetPair = tuple[tf.data.Dataset, tf.data.Dataset]


def download_dataset(url: str, destination: Path) -> Path:
    # Download and unpack the archive, unless the images are already there.
    if destination.exists():
        return destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {url}")
    with tempfile.NamedTemporaryFile(suffix=".zip") as archive:
        urllib.request.urlretrieve(url, archive.name)
        with zipfile.ZipFile(archive.name) as zipped:
            zipped.extractall(destination.parent)
    return destination


def load_image_datasets(
    directory: Path, image_size: int, batch_size: int, seed: int
) -> DatasetPair:
    # One sub-directory per class; class indices follow the alphabetical order.
    def read(subdirectory: str, shuffle: bool) -> tf.data.Dataset:
        dataset: tf.data.Dataset = keras.utils.image_dataset_from_directory(
            directory / subdirectory,
            label_mode="binary",
            image_size=(image_size, image_size),
            interpolation="nearest",  # as ImageDataGenerator did
            batch_size=batch_size,
            shuffle=shuffle,
            seed=seed,
        )
        return dataset

    return read(TRAIN_SUBDIRECTORY, shuffle=True), read(VALIDATION_SUBDIRECTORY, shuffle=False)


def synthetic_datasets(
    image_size: int, batch_size: int, seed: int, train_samples: int = 8, validation_samples: int = 4
) -> DatasetPair:
    """Random images with random labels, with the same contract as the radiographs.

    No download, no patient data, and nothing for the model to learn: enough
    to run the training pipeline.

    >>> train, validation = synthetic_datasets(image_size=32, batch_size=4, seed=0)
    >>> images, labels = next(iter(train))
    >>> tuple(images.shape), tuple(labels.shape)
    ((4, 32, 32, 3), (4, 1))
    """
    generator = np.random.default_rng(seed)

    def make(samples: int) -> tf.data.Dataset:
        images = generator.integers(0, 256, size=(samples, image_size, image_size, 3))
        labels = generator.integers(0, 2, size=(samples, 1))
        return tf.data.Dataset.from_tensor_slices(
            (images.astype(np.float32), labels.astype(np.float32))
        ).batch(batch_size)

    return make(train_samples), make(validation_samples)
