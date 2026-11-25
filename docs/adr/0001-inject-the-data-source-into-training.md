# 0001. Inject the data source into training

Date: 2026-11-25

## Status

Accepted

## Context

In the notebook, the training cell used whatever the cells above it had left
in memory: the image generators built from folders on disk, themselves built
from paths written in the code. Training could not run without the 75
radiographs and the ImageNet weights, and there was no way to train on
anything else without editing those cells.

Moving the code into a package raised the question of where the training
function gets its data from. Training needs two things: a compiled model and
batches of `(images, labels)`. It does not need to know where either comes
from.

## Decision

`train()` in `training.py` takes the model and the two datasets as arguments.
The caller decides where they come from:

- `cli.py` downloads the archive and reads the `TRAIN` and `VAL` folders with
  `load_image_datasets()`;
- the tests, and the last cells of the demonstration notebook, call
  `synthetic_datasets()`, which generates noise images with the same shape
  and labels.

Both sources honour one contract, stated in `data.py`: batches of RGB images
with values in `[0, 255]` and binary labels. The model rescales to `[0, 1]`
and applies augmentation itself, so a source only has to read images.

There is no `DataSource` base class or interface: two functions with the same
return type are enough for the needs of this repository (YAGNI). `cli.py` is
the only module that imports every other one; it is where the pieces are
assembled (the *composition root*).

## Consequences

- The integration test trains the real architecture for one epoch in about
  half a minute, offline, with random weights, because nothing in
  `training.py` touches the network or the disk.
- Replacing the data source (another folder layout, a DICOM reader, a
  database) means adding one function to `data.py` and calling it from
  `cli.py`; the model and the training code do not change.
- Anyone reading `train()` sees its whole input in its signature.
- The cost: `cli.py` passes a few more arguments around, and a new data
  source has to respect the contract by discipline, since nothing enforces it
  when the code is imported. The test
  `test_synthetic_datasets_have_the_same_contract_as_real_ones` checks it for
  the two existing sources.
