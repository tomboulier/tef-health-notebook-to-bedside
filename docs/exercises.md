# Changing one thing

Research code changes all the time: you correct a mistake, you try another
hypothesis, you swap a dataset. Two questions tell you whether a change is
safe. How many places in the code does it touch? And will you find it again
in six months, alone, to explain a result or to undo it?

The architecture answers the first question. When each concern lives in one
module, a change in the data augmentation should touch the augmentation and
nothing else. Atomic commits answer the second: one commit holds one change,
with a message that says why, so `git log` finds it and `git revert` undoes it
without undoing anything else.

This page goes through three changes already made in this repository, then
proposes exercises. Clone the repository and install it first (see
[Usage](usage.md)).

## Three changes already made

### Adam's epsilon

The original notebook passed `epsilon=1e08` to the Adam optimizer instead of
`1e-08`. Epsilon sits in the denominator of every update, so with a value of
one hundred million the weights barely moved. The correction is a single
commit,
[`fix: set Adam's epsilon to 1e-08`](https://github.com/tomboulier/tef-health-notebook-to-bedside/commit/d01935b),
which changes one line. Its message explains the mistake and its effect.

### Augmented validation images

The notebook built the validation images with the same generator as the
training images, so they were randomly rotated, zoomed and flipped at every
epoch, and the validation accuracy was measured on a different set each time.
This is a data science question more than a software one, but fixing it is a
software question. The fix is again its own commit,
[`fix: stop augmenting the validation images`](https://github.com/tomboulier/tef-health-notebook-to-bedside/commit/e94241a).
At step 3, the augmentation became layers of the model, in
[`model.py`](https://github.com/tomboulier/tef-health-notebook-to-bedside/blob/main/src/hello_world_medical_imaging/model.py).
Keras applies these layers during training only, so the rule "augment the
training images and nothing else" is now enforced in one place.

### Shear in degrees

The notebook's `ImageDataGenerator` read its shear range in degrees: 0.2
means 0.2 degrees. Keras 3 has no such generator, and its `RandomShear` layer
takes a different unit. A first port of this notebook, made elsewhere, read
0.2 as a fraction rather than an angle and produced much larger shears, with
no error message. In this repository the conversion is correct, but it arrived inside
the commit
[`fix: port the notebook to Keras 3`](https://github.com/tomboulier/tef-health-notebook-to-bedside/commit/64b122c),
mixed with everything else the port changed. Nobody reading the history would
learn that the unit of the shear was a trap. This is what a non-atomic commit
costs: the knowledge is in the code, but not in the history.

Today the unit is in the name of the setting, `shear_degrees` in
[`config.toml`](https://github.com/tomboulier/tef-health-notebook-to-bedside/blob/main/config.toml),
and the conversion is in one function, `augmentation_layers` in `model.py`.

## Exercises

For each exercise, before writing any code, list the files you expect to
change. Then make the change, run the checks (`uv run pytest`,
`uv run ruff check .`, `uv run mypy src tests`) and commit it alone, with a
[Conventional Commits](https://www.conventionalcommits.org/) message. Finally,
compare your list with `git show --stat`. If the change touched a file you did
not expect, ask why.

1. **Stop flipping the radiographs.** A chest radiograph flipped left to right
   puts the heart on the wrong side, which never happens in real images (apart
   from situs inversus). Turn off the horizontal flip. Expected: one file,
   `config.toml`, and no code at all.

2. **Download the images from Software Heritage.** Pretend the original GitHub
   repository has disappeared, and use the archived copy whose address is
   given in `config.toml`. Expected: one file again. Why can you be sure that
   the images are the same ones?

3. **Move the optimizer settings to the configuration.** Adam's `beta_1`,
   `beta_2` and `epsilon` are still written in `model.py`, while the learning
   rate is in `config.toml`. An experiment parameter belongs in the
   configuration, where it is recorded with the results. Expected:
   `config.py`, `config.toml`, `model.py`, the two places that call
   `build_model` (`cli.py` and the notebook), and a test. Nothing in `data.py` or `training.py`.

4. **Find a correction in the history and undo it.** Run
   `git log --oneline --grep "^fix"`, pick the epsilon correction, and undo it
   in a scratch branch with `git revert`. Train for a few epochs and compare
   the curves with those of `main`. This is how you check, months later,
   whether a correction changed a published result.

5. **Try another pretrained network.** Replace Inception V3 by another
   network of `keras.applications`. Which modules have to change, and which
   must not? The answer to the second half is the reason for the
   architecture of step 3.
