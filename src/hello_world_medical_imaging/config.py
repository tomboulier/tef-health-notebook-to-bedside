"""Experiment configuration, read from a TOML file.

Everything that used to be a global variable in the notebook (paths,
hyperparameters, data augmentation ranges, random seed) lives here, so that
the code does not change from one experiment to the next.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Augmentation:
    """Ranges of the random transformations applied to the training images.

    The values and units are those of the ``ImageDataGenerator`` of the
    original notebook.

    Attributes:
        rotation_degrees: Maximum rotation, in degrees, either way.
        zoom_range: Maximum zoom in or out, as a fraction of the image size.
        shift_range: Maximum shift, as a fraction of the height and of the width.
        shear_degrees: Maximum shear angle, in degrees, either way.
        horizontal_flip: Whether images are flipped left to right at random.
    """

    rotation_degrees: float = 20.0
    zoom_range: float = 0.2
    shift_range: float = 0.2
    shear_degrees: float = 0.2
    horizontal_flip: bool = True


@dataclass(frozen=True)
class Config:
    """All the settings of one experiment.

    Attributes:
        dataset_url: Address of the zip archive of the images.
        dataset_directory: Folder where the archive is unpacked.
        output_directory: Folder where the trained model and the curves are written.
        image_size: Images are resized to ``image_size`` x ``image_size`` pixels.
        batch_size: Number of images per batch.
        epochs: Number of passes over the training images.
        learning_rate: Learning rate of the Adam optimizer.
        seed: Seed of every random number generator.
        augmentation: Random transformations of the training images.

    >>> config = Config.from_dict({"image_size": 75, "epochs": 1})
    >>> config.image_size, config.epochs, config.seed
    (75, 1, 42)
    """

    dataset_url: str = (
        "https://raw.githubusercontent.com/paras42/Hello_World_Deep_Learning/"
        "9921a12c905c00a88898121d5dc538e3b524e520/Open_I_abd_vs_CXRs.zip"
    )
    dataset_directory: Path = Path("data/Open_I_abd_vs_CXRs")
    output_directory: Path = Path("outputs")
    image_size: int = 299
    batch_size: int = 5
    epochs: int = 20
    learning_rate: float = 1e-4
    seed: int = 42
    augmentation: Augmentation = Augmentation()

    @classmethod
    def from_dict(cls, values: dict[str, Any]) -> Config:
        """Build a configuration from a dictionary, such as parsed TOML.

        Missing keys keep their default; an unknown key is an error, so that a
        typo in the file is noticed at once.

        Args:
            values: Settings by name, with ``augmentation`` as a nested dictionary.

        Returns:
            The configuration, with paths converted to :class:`~pathlib.Path`.

        Raises:
            TypeError: If a key is not a known setting.

        >>> Config.from_dict({"epoch": 3})
        Traceback (most recent call last):
            ...
        TypeError: Config.__init__() got an unexpected keyword argument 'epoch'
        """
        values = dict(values)
        for key in ("dataset_directory", "output_directory"):
            if key in values:
                values[key] = Path(values[key])
        if "augmentation" in values:
            values["augmentation"] = Augmentation(**values["augmentation"])
        return cls(**values)


def load_config(path: Path) -> Config:
    """Read a TOML file and return the corresponding configuration.

    Args:
        path: The TOML file, for example ``config.toml``.

    Returns:
        The configuration; settings absent from the file keep their default.
    """
    with path.open("rb") as file:
        return Config.from_dict(tomllib.load(file))
