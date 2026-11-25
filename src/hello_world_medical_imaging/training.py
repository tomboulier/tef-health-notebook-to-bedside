"""Training a model on datasets it receives as arguments.

This module knows nothing about where the images come from: the caller
passes the model and the datasets in.
"""

from __future__ import annotations

import logging
from pathlib import Path

import keras
import tensorflow as tf
from matplotlib.figure import Figure

logger = logging.getLogger(__name__)


def train(
    model: keras.Model,
    train_dataset: tf.data.Dataset,
    validation_dataset: tf.data.Dataset,
    epochs: int,
) -> keras.callbacks.History:
    """Fit ``model`` for ``epochs`` passes over ``train_dataset``.

    Args:
        model: A compiled Keras model.
        train_dataset: Batches of ``(images, labels)`` used to update the weights.
        validation_dataset: Batches of ``(images, labels)`` only used to report metrics.
        epochs: Number of passes over the training data.

    Returns:
        The training history: one value per epoch for the loss, the accuracy,
        the validation loss and the validation accuracy.
    """
    logger.info("Training for %d epoch(s)", epochs)
    # The datasets are already shuffled (or deliberately not), hence shuffle=False.
    history: keras.callbacks.History = model.fit(
        train_dataset, epochs=epochs, validation_data=validation_dataset, shuffle=False
    )
    final = {name: round(values[-1], 4) for name, values in history.history.items()}
    logger.info("Training finished: %s", final)
    return history


def plot_history(history: keras.callbacks.History, path: Path) -> Path:
    """Save the training curves (loss and accuracy, training and validation) to a file.

    Args:
        history: The history returned by :func:`train`.
        path: The image file to write, for example ``outputs/training_curves.png``.

    Returns:
        ``path``, for convenience.
    """
    figure = Figure()
    axes = figure.subplots()
    for key, color in (
        ("accuracy", "orange"),
        ("val_accuracy", "blue"),
        ("loss", "red"),
        ("val_loss", "green"),
    ):
        axes.plot(history.history[key], color, label=key.replace("_", " "))
    axes.set_xlabel("epoch")
    axes.legend()
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path)
    logger.info("Training curves saved to %s", path)
    return path
