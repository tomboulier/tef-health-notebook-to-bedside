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
    """Download and unpack the dataset archive, unless ``destination`` exists.

    The archive must contain a top-level folder named like ``destination``,
    with ``TRAIN``, ``VAL`` and ``TEST`` sub-folders.

    Args:
        url: Where to fetch the zip archive from (``https://`` or ``file://``).
        destination: Folder that will hold the unpacked images.

    Returns:
        ``destination``, for convenience.

    Raises:
        FileNotFoundError: If the archive does not contain the expected folder.
    """
    if destination.exists():
        return destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {url}")
    with tempfile.NamedTemporaryFile(suffix=".zip") as archive:
        urllib.request.urlretrieve(url, archive.name)
        with zipfile.ZipFile(archive.name) as zipped:
            zipped.extractall(destination.parent)
    if not destination.exists():
        raise FileNotFoundError(f"Archive from {url} did not contain {destination.name}")
    return destination


def load_image_datasets(
    directory: Path, image_size: int, batch_size: int, seed: int
) -> DatasetPair:
    """Read the ``TRAIN`` and ``VAL`` image folders as datasets.

    Each folder holds one sub-folder per class; class indices follow the
    alphabetical order of the sub-folder names, which makes the chest
    radiographs (``openI_CXR``) class 0 and the abdominal ones class 1.
    The training images are shuffled, the validation images are not.

    Args:
        directory: Root of the dataset, the folder that contains ``TRAIN`` and ``VAL``.
        image_size: Images are resized to ``image_size`` x ``image_size`` pixels.
        batch_size: Number of images per batch.
        seed: Seed of the shuffling.

    Returns:
        The training and validation datasets.
    """

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
    to run the training pipeline in seconds, which is what the tests do.

    Args:
        image_size: Side of the square images, in pixels.
        batch_size: Number of images per batch.
        seed: Seed of the random images and labels.
        train_samples: Number of training images.
        validation_samples: Number of validation images.

    Returns:
        The training and validation datasets.

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
