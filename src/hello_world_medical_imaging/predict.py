"""Classifying a single radiograph with a trained model."""

from __future__ import annotations

from pathlib import Path

import keras
import numpy as np

# Human-readable class names, in the order of the class indices.
CLASS_NAMES = ("Chest X-ray", "Abdominal X-ray")


def label_from_score(score: float) -> str:
    """Turn the model output, the probability of the abdomen class, into a label.

    Args:
        score: Probability of the abdomen class, between 0 and 1.

    Returns:
        The class name; 0.5 and above is an abdominal radiograph.

    >>> label_from_score(0.1)
    'Chest X-ray'
    >>> label_from_score(0.5)
    'Abdominal X-ray'
    """
    return CLASS_NAMES[1] if score >= 0.5 else CLASS_NAMES[0]


def predict_image(model: keras.Model, image_path: Path, image_size: int) -> float:
    """Return the probability that an image is an abdominal radiograph.

    Args:
        model: A trained model, as built by :func:`~hello_world_medical_imaging.model.build_model`.
        image_path: The image file.
        image_size: Side of the model's input images; the image is resized to it.

    Returns:
        The probability of the abdomen class. Rescaling is done by the model.
    """
    image = keras.utils.load_img(image_path, target_size=(image_size, image_size))
    batch = np.expand_dims(keras.utils.img_to_array(image), axis=0)
    score: float = float(model.predict(batch, verbose=0)[0, 0])
    return score
