"""Classifying a single radiograph with a trained model."""

from __future__ import annotations

from pathlib import Path

import keras
import numpy as np

# Human-readable class names, in the order of the class indices.
CLASS_NAMES = ("Chest X-ray", "Abdominal X-ray")


def label_from_score(score: float) -> str:
    """Turn the model output, the probability of the abdomen class, into a label.

    >>> label_from_score(0.1)
    'Chest X-ray'
    >>> label_from_score(0.5)
    'Abdominal X-ray'
    """
    return CLASS_NAMES[1] if score >= 0.5 else CLASS_NAMES[0]


def predict_image(model: keras.Model, image_path: Path, image_size: int) -> float:
    # The model rescales the image itself.
    image = keras.utils.load_img(image_path, target_size=(image_size, image_size))
    batch = np.expand_dims(keras.utils.img_to_array(image), axis=0)
    score: float = float(model.predict(batch, verbose=0)[0, 0])
    return score
