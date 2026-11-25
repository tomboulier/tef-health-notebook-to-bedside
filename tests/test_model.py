import math

from hello_world_medical_imaging.config import Augmentation
from hello_world_medical_imaging.model import augmentation_layers, build_model
from tests.conftest import IMAGE_SIZE


def test_model_outputs_one_probability_per_image() -> None:
    model = build_model(IMAGE_SIZE, learning_rate=1e-3, pretrained=False)
    assert model.output_shape == (None, 1)
    assert model.input_shape == (None, IMAGE_SIZE, IMAGE_SIZE, 3)


def test_augmentation_keeps_image_shape() -> None:
    layers = augmentation_layers(Augmentation())
    assert layers.compute_output_shape((None, IMAGE_SIZE, IMAGE_SIZE, 3)) == (
        None,
        IMAGE_SIZE,
        IMAGE_SIZE,
        3,
    )


def test_shear_angle_is_converted_from_degrees() -> None:
    # ImageDataGenerator took the shear as an angle in degrees; RandomShear
    # takes a shift per pixel, i.e. the tangent of that angle.
    shear = augmentation_layers(Augmentation(shear_degrees=45.0)).layers[3]
    assert math.isclose(shear.x_factor[1], 1.0)
