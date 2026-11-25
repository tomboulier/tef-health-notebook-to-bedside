# Testing

The tests live in `tests/` and run with `uv run pytest`. There are three
kinds:

- **unit tests** of the functions of the package: reading and validating the
  configuration, unpacking the dataset archive (from a local `file://`
  archive, without network), reading a folder of generated images, the
  shapes of the model and the units of its augmentation layers;
- **one integration test** (`tests/test_training.py`) that builds the real
  architecture with random weights at 75 x 75 pixels, trains it for one epoch
  on synthetic images, predicts one image and saves the curves. It runs in
  about half a minute on a laptop processor, with no download;
- **doctests**: the examples written in the docstrings, which pytest runs
  through `--doctest-modules`, so that they stay true.

Ruff (style and formatting) and mypy (types, strict mode) are configured in
`pyproject.toml`:

```bash
uv run pytest
uv run ruff check . && uv run ruff format --check .
uv run mypy
```

## A test written before its code

Test-driven development means writing a failing test that describes the
behaviour wanted, then the smallest code that makes it pass, then tidying up.
The history of this repository shows one such cycle, in two consecutive
commits of step 4.

The behaviour wanted: if the archive downloaded from the configured address
does not contain the expected folder (a wrong address, a new layout
upstream), `download_dataset` should say so at once. Until then it returned a
path that did not exist, and the error only appeared later, when the images
were read, far from its cause.

The commit *test: require download_dataset to reject an archive without the
dataset folder* adds the test alone, with a tiny archive built in a temporary
folder so that no network is needed:

```python
def test_download_dataset_rejects_an_archive_without_the_dataset_folder(tmp_path: Path) -> None:
    archive = tmp_path / "wrong.zip"
    with zipfile.ZipFile(archive, "w") as zipped:
        zipped.writestr("something_else/readme.txt", "no images here")

    with pytest.raises(FileNotFoundError):
        download_dataset(archive.as_uri(), tmp_path / "Open_I_abd_vs_CXRs")
```

At that commit, `uv run pytest` fails with `Failed: DID NOT RAISE
FileNotFoundError`: the test states the contract before the code exists. The
next commit, *feat: reject a dataset archive that does not contain the
dataset folder*, adds the two lines that make it pass:

```python
    if not destination.exists():
        raise FileNotFoundError(f"Archive from {url} did not contain {destination.name}")
```

To see it for yourself:

```bash
git log --oneline step-3-architecture..step-4-tests
git checkout <hash of the test: commit> && uv run pytest     # one failure
git checkout <hash of the feat: commit> && uv run pytest     # all pass
git checkout main
```

## What a green test suite does and does not tell you

A passing suite says that the behaviours someone thought of writing down
still hold. It says nothing about the behaviours nobody wrote down. A coverage
percentage counts the lines executed by some test, not the lines whose
behaviour was checked: it is a way to find untested code, not a measure of
robustness. The integration test here trains on noise: it shows that the
pipeline runs, not that the model is any good.
