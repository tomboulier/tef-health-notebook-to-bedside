# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Entries below the marker are generated from the
[Conventional Commits](https://www.conventionalcommits.org/) history by
python-semantic-release (see `docs/automation.md`).

<!-- version list -->

## v1.0.1 (2026-11-25)

### Bug Fixes

- **release**: Keep uv.lock in step with the package version
  ([`da427aa`](https://github.com/tomboulier/tef-health-notebook-to-bedside/commit/da427aa92654c4f17de97dd6a998bed2021b0ce4))

### Documentation

- Ask for one change per commit at step 1
  ([`9e298db`](https://github.com/tomboulier/tef-health-notebook-to-bedside/commit/9e298dba64fa9c405788560488621066dd0b2cad))

- Say which version the video presents and how to cite it
  ([`8b1eaa4`](https://github.com/tomboulier/tef-health-notebook-to-bedside/commit/8b1eaa4791daf6080ac3e9bff8c9a9d8ef68423e))

### Testing

- Read the expected version from the package metadata
  ([`c500908`](https://github.com/tomboulier/tef-health-notebook-to-bedside/commit/c500908ffc6bde96b2618c811b2d1f5a87fdc870))


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
