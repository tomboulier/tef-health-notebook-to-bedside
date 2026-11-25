# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Entries below the marker are generated from the
[Conventional Commits](https://www.conventionalcommits.org/) history by
python-semantic-release (see `docs/automation.md`).

<!-- version list -->

## v1.0.0 (2026-11-25)

First citable version, the one presented in the TEF-Health capsule.

- The original notebook taken to maintainable code in six steps, one Git tag
  per step, from `step-0-notebook` to `step-6-automation`.
- The command `hello-world-medical-imaging`, configured by `config.toml`,
  with a synthetic data source for the tests.
- The download of the images checks their SHA-256 checksum; the archive is
  also preserved by Software Heritage.
- Companion page on GitHub Pages, with exercises on isolating one change.
- `CITATION.cff` for citing the repository.
