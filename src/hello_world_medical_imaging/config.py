"""Experiment configuration, read from a TOML file."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Augmentation:
    # Ranges and units of the ImageDataGenerator of the original notebook.
    rotation_degrees: float = 20.0
    zoom_range: float = 0.2
    shift_range: float = 0.2
    shear_degrees: float = 0.2
    horizontal_flip: bool = True


@dataclass(frozen=True)
class Config:
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
        # Missing keys keep their default; an unknown key is a TypeError.
        values = dict(values)
        for key in ("dataset_directory", "output_directory"):
            if key in values:
                values[key] = Path(values[key])
        if "augmentation" in values:
            values["augmentation"] = Augmentation(**values["augmentation"])
        return cls(**values)


def load_config(path: Path) -> Config:
    with path.open("rb") as file:
        return Config.from_dict(tomllib.load(file))
