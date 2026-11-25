"""Training a model on datasets it receives as arguments.

This module knows nothing about where the images come from: the caller
passes the model and the datasets in.
"""

from __future__ import annotations

from pathlib import Path

import keras
import tensorflow as tf
from matplotlib.figure import Figure


def train(
    model: keras.Model,
    train_dataset: tf.data.Dataset,
    validation_dataset: tf.data.Dataset,
    epochs: int,
) -> keras.callbacks.History:
    print(f"Training for {epochs} epoch(s)")
    # The datasets are already shuffled (or deliberately not), hence shuffle=False.
    history: keras.callbacks.History = model.fit(
        train_dataset, epochs=epochs, validation_data=validation_dataset, shuffle=False
    )
    return history


def plot_history(history: keras.callbacks.History, path: Path) -> Path:
    # Loss and accuracy, on training and validation data, saved to a file.
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
    return path
