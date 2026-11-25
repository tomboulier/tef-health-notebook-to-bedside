"""The classifier: Inception V3 pre-trained on ImageNet, with a new binary head.

The rescaling to [0, 1] and the data augmentation are layers of the model, so
that it receives raw images in [0, 255]. Keras applies the augmentation
during training only, never to validation images or predictions.
"""

from __future__ import annotations

import math

import keras

from hello_world_medical_imaging.config import Augmentation


def augmentation_layers(augmentation: Augmentation) -> keras.Sequential:
    """Random transformations of the training images, as ImageDataGenerator did them.

    Angles are converted from degrees to the units of the Keras layers, and
    borders are filled with the nearest pixel.

    Args:
        augmentation: Ranges of the transformations.

    Returns:
        The layers, to be applied in sequence; Keras only applies them in training.

    >>> len(augmentation_layers(Augmentation(horizontal_flip=False)).layers)
    4
    """
    fill_mode = "nearest"
    layers: list[keras.Layer] = [
        keras.layers.RandomRotation(augmentation.rotation_degrees / 360, fill_mode=fill_mode),
        keras.layers.RandomZoom(augmentation.zoom_range, fill_mode=fill_mode),
        keras.layers.RandomTranslation(
            augmentation.shift_range, augmentation.shift_range, fill_mode=fill_mode
        ),
        # A shear angle, as a horizontal shift per pixel of height.
        keras.layers.RandomShear(
            x_factor=math.tan(math.radians(augmentation.shear_degrees)), fill_mode=fill_mode
        ),
    ]
    if augmentation.horizontal_flip:
        layers.append(keras.layers.RandomFlip("horizontal"))
    return keras.Sequential(layers, name="augmentation")


def build_model(
    image_size: int,
    learning_rate: float,
    augmentation: Augmentation | None = None,
    pretrained: bool = True,
) -> keras.Model:
    """Build and compile the transfer-learning classifier.

    Inception V3 without its top layers, followed by global average pooling,
    a fully connected layer of 256 units, dropout and a sigmoid output.

    Args:
        image_size: Side of the square input images, at least 75 pixels.
        learning_rate: Learning rate of the Adam optimizer (kept low for transfer learning).
        augmentation: Random transformations of the training images, if any.
        pretrained: Load the ImageNet weights (downloaded once by Keras). ``False``
            gives random weights, which is what the tests use to stay offline.

    Returns:
        A compiled model that takes images in ``[0, 255]`` and outputs the
        probability of the abdomen class.
    """
    base_model = keras.applications.InceptionV3(
        weights="imagenet" if pretrained else None,
        include_top=False,
        input_shape=(image_size, image_size, 3),
    )

    inputs = keras.Input(shape=(image_size, image_size, 3), name="image")
    x = keras.layers.Rescaling(1.0 / 255)(inputs)
    if augmentation is not None:
        x = augmentation_layers(augmentation)(x)
    x = base_model(x)
    x = keras.layers.GlobalAveragePooling2D()(x)
    x = keras.layers.Dense(256, activation="relu")(x)
    x = keras.layers.Dropout(0.5)(x)
    outputs = keras.layers.Dense(1, activation="sigmoid", name="abdomen_probability")(x)

    model = keras.Model(inputs=inputs, outputs=outputs, name="hello_world_medical_imaging")
    model.compile(
        optimizer=keras.optimizers.Adam(
            learning_rate=learning_rate, beta_1=0.9, beta_2=0.999, epsilon=1e-08
        ),
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )
    return model
