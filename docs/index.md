# From notebook to bedside: a roadmap

This page accompanies the video *Best Practices in Software Engineering for
Robust and Maintainable Medical AI*, a capsule of the TEF-Health training
course. The video is a map, not a tutorial: each of the six steps below
points to existing lessons and readings rather than teaching them. The
repository [tomboulier/tef-health-notebook-to-bedside](https://github.com/tomboulier/tef-health-notebook-to-bedside) shows every
step carried out on one small example, the *Hello World Deep Learning in
Medical Imaging* tutorial of Lakhani et al.
([doi:10.1007/s10278-018-0079-6](https://doi.org/10.1007/s10278-018-0079-6),
original code and images at
[paras42/Hello_World_Deep_Learning](https://github.com/paras42/Hello_World_Deep_Learning)),
a Jupyter notebook that classifies radiographs as chest or abdomen.

The original tutorial is very good work, and worth reading before this page.
The article explains each step for clinicians, and the repository ships the
notebook together with its 75 images, so anyone can run it without asking
for data. That a published notebook comes with its data is already a large
part of reproducibility.

The roadmap is not about certifying a medical device. It is about what has to
be true of the code before anyone relies on it. Tools are named below as
examples, never as recommendations.

## Two ways to get code that runs

Code that runs comes, more and more often, from one of two places. A
**notebook**: cells written and rerun in an order only the author remembers,
global variables, paths and hyperparameters typed in the code, libraries in
whatever version was installed that day. Or a **prototype written by a coding
agent** ("vibe coding"): hundreds of lines produced in an afternoon, which run,
but which nobody has read in full, with no tests and dependencies taken at
their latest version.

The symptoms are the same: the code works on one machine, today; nobody can
say exactly why; and it breaks as soon as something changes, the data, a
library or the person running it. The remedy is the same too. Code that runs
is not yet code you can rely on; the six steps below, basic software
engineering, make it reproducible, maintainable and ready to be used by
others.

## How to read the repository

Each step is a series of commits whose messages follow
[Conventional Commits](https://www.conventionalcommits.org/), ending with a
Git tag. Under each step, *Browse the code at this step* shows the repository
as it was at the end of the step, and *See what this step changed* shows the
difference with the previous step, commit by commit. The starting point, the
notebook as it was published, is the tag
[`step-0-notebook`](https://github.com/tomboulier/tef-health-notebook-to-bedside/tree/step-0-notebook).

## 1. Version control

[Browse the code at this step](https://github.com/tomboulier/tef-health-notebook-to-bedside/tree/step-1-version-control) ·
[See what this step changed](https://github.com/tomboulier/tef-health-notebook-to-bedside/compare/step-0-notebook...step-1-version-control)

**Done here.** The original notebook is the first commit, with its outputs
cleared (they contained radiographs). A
[`.gitignore`](https://github.com/tomboulier/tef-health-notebook-to-bedside/blob/step-1-version-control/.gitignore) keeps data,
model weights, training outputs, caches and virtual environments out of Git,
and the README says how to version large files when needed. Every commit
since is a Conventional Commit, so that `git log --oneline` reads as the
roadmap itself.

**What to retain.** A history is a lab notebook that cannot be lost or
rewritten by accident; it is only useful if each entry says what changed and
why. Large files (images, weights) do not belong in Git: tools such as
[DVC](https://dvc.org) or [Git LFS](https://git-lfs.com) version them next to
the code without bloating it.

**Lessons and readings.**
[Version Control with Git](https://swcarpentry.github.io/git-novice/), Software Carpentry ·
[Pro Git](https://git-scm.com/book/en/v2).

## 2. Reproducible environment

[Browse the code at this step](https://github.com/tomboulier/tef-health-notebook-to-bedside/tree/step-2-reproducible-environment) ·
[See what this step changed](https://github.com/tomboulier/tef-health-notebook-to-bedside/compare/step-1-version-control...step-2-reproducible-environment)

**Done here.** Python 3.12 and the direct dependencies are pinned to exact
versions in [`pyproject.toml`](https://github.com/tomboulier/tef-health-notebook-to-bedside/blob/step-2-reproducible-environment/pyproject.toml),
and every transitive dependency in `uv.lock`. Paths, hyperparameters and the
random seed left the code for
[`config.toml`](https://github.com/tomboulier/tef-health-notebook-to-bedside/blob/step-2-reproducible-environment/config.toml).
The notebook was ported to Keras 3, and a
[`Dockerfile`](https://github.com/tomboulier/tef-health-notebook-to-bedside/blob/step-2-reproducible-environment/Dockerfile)
executes it from top to bottom with papermill, without a browser. Run twice
on a laptop processor, or once on the laptop and once in the container, it
gives the same numbers.

The data are identified too. The images are not copied into the repository:
they are downloaded from the original tutorial repository, at a fixed commit,
and the download stops if the archive does not have the SHA-256 checksum
written in `config.toml`. A GitHub account can close, so `config.toml` also
gives the address of the same archive in
[Software Heritage](https://www.softwareheritage.org/), the universal archive
of source code. This is the A of the
[FAIR principles](https://www.go-fair.org/fair-principles/) (findable,
accessible, interoperable, reusable): data that others cannot reach cannot
be used to check a result. For larger data that change over time, tools such
as [DVC](https://dvc.org) record which version of the data each experiment
used.

### Why this step matters: the 2018 notebook no longer runs

The tutorial notebook (published in 2018; the version here is a 2021
transcription) never said which versions of its libraries it needed. Run
unchanged with the versions of today, TensorFlow 2.21.0 and the Keras 3.15.1
that comes with it, it stops at its first code cell:

```
ImportError: cannot import name 'ImageDataGenerator' from 'keras.preprocessing.image'
```

Once that import is fixed, it stops again when the model is compiled:
`ValueError: Argument(s) not recognized: {'lr': 0.0001}`. Nothing in the
notebook changed; the world around it did. This is *software rot*: code whose
dependencies are not pinned breaks when one of them changes, here at the
major version change from Keras 2 to Keras 3, which removed
`ImageDataGenerator` and renamed `lr` to `learning_rate`. The
[port to Keras 3](https://github.com/tomboulier/tef-health-notebook-to-bedside/commit/64b122caa21896bb89d64b523456850131335a3c) is
one commit; reading the old code closely to port it also brought out two
defects of the original, each fixed in its own commit: Adam's
[`epsilon` was `1e08` instead of `1e-08`](https://github.com/tomboulier/tef-health-notebook-to-bedside/commit/d01935b7ab9fd81ca3db541434138e1e3a2122d4),
and the [validation images were augmented](https://github.com/tomboulier/tef-health-notebook-to-bedside/commit/e94241a7a7f456ad6fa224eb1e83cbd9d9252a9f)
like the training ones.

There are two ways to fight software rot, and they are often combined.

- **Freeze**, to reproduce a published result: a lock file that pins every
  dependency (`uv.lock` here), and a container image archived with the
  result (pushed to a registry and cited by its digest, or saved as a file),
  which holds the whole system down to the operating system.
- **Maintain**, to keep the code alive: upgrade in small steps, each one
  checked by the tests and the continuous integration (steps 4 and 6). Tools
  such as [Dependabot](https://docs.github.com/en/code-security/dependabot)
  or [Renovate](https://docs.renovatebot.com/) open a pull request for each
  new version of a dependency, and a scheduled run of the continuous
  integration (weekly in this repository, see step 6) detects breakage early,
  before someone needs the code.

**What to retain.** "It works on my machine" is a statement about the
machine. Writing down the exact versions, taking the magic numbers out of the
code and packaging the whole thing in an image are three steps towards
someone else, or you in a year, getting the same result.

**Lessons and readings.**
[Good enough practices in scientific computing](https://doi.org/10.1371/journal.pcbi.1005510), Wilson et al. 2017 ·
[The Turing Way](https://book.the-turing-way.org/) ·
[Python packaging](https://carpentries-incubator.github.io/python_packaging), Carpentries Incubator ·
[Docker documentation](https://docs.docker.com/get-started/).

## 3. Architecture

[Browse the code at this step](https://github.com/tomboulier/tef-health-notebook-to-bedside/tree/step-3-architecture) ·
[See what this step changed](https://github.com/tomboulier/tef-health-notebook-to-bedside/compare/step-2-reproducible-environment...step-3-architecture)

**Done here.** The notebook's code became a package,
[`src/hello_world_medical_imaging/`](https://github.com/tomboulier/tef-health-notebook-to-bedside/tree/step-3-architecture/src/hello_world_medical_imaging),
with one module per concern: `config`, `data`, `model`, `training`,
`predict` and `cli`, the command line that assembles them. The training
function receives the model and the datasets as arguments instead of building
them itself (dependency injection), so a second data source, synthetic noise
images, replaces the radiographs without any change to the model
([ADR 0001](adr/0001-inject-the-data-source-into-training.md), written at
step 5). The notebook became a short demonstration that calls the package,
the container runs the package's command, and
[`AGENTS.md`](https://github.com/tomboulier/tef-health-notebook-to-bedside/blob/step-3-architecture/AGENTS.md) states the
architecture and two guard-rails: keep it simple (KISS), and do not build what
is not needed yet (YAGNI).

**What to retain.** The point of architecture is to decide what depends on
what. When the part that trains does not know where the data comes from, you
can test it in seconds and replace the data source later. Any further layer
has to earn its place.

**Lessons and readings.**
[Clean Architecture](https://www.oreilly.com/library/view/clean-architecture-a/9780134494272/), Robert C. Martin ·
[Hexagonal architecture](https://alistair.cockburn.us/hexagonal-architecture/), Alistair Cockburn ·
[SOLID](https://en.wikipedia.org/wiki/SOLID) ·
[Design patterns](https://en.wikipedia.org/wiki/Design_Patterns) ·
[Better Architecture, Better Software, Better Research](https://doi.org/10.1109/MCSE.2025.3573887), Druskat et al. 2025 ·
[Intermediate Research Software Development](https://carpentries-incubator.github.io/python-intermediate-development/), Carpentries Incubator ·
[Programming with Python](https://swcarpentry.github.io/python-novice-inflammation/), Software Carpentry ·
[Research Software Engineering with Python](https://alan-turing-institute.github.io/rse-course/html/index.html), Alan Turing Institute.

## 4. Tests

[Browse the code at this step](https://github.com/tomboulier/tef-health-notebook-to-bedside/tree/step-4-tests) ·
[See what this step changed](https://github.com/tomboulier/tef-health-notebook-to-bedside/compare/step-3-architecture...step-4-tests)

**Done here.** [`tests/`](https://github.com/tomboulier/tef-health-notebook-to-bedside/tree/step-4-tests/tests) holds pytest unit
tests of the package, one integration test that trains the real architecture
for one epoch on synthetic images, offline, and the doctests of the
docstrings. One test was
[written before its code](https://github.com/tomboulier/tef-health-notebook-to-bedside/commit/a781ec1e7eb153d0d2dfb5d4115031712889148b)
and fails at that commit; the
[next commit](https://github.com/tomboulier/tef-health-notebook-to-bedside/commit/bff3320ffae0ba49d3223ca4201edf5d41e5fe14) makes it
pass ([Testing](testing.md) tells the story). Ruff (lint and formatting) and
mypy (types) are configured in `pyproject.toml`, and the container runs the
tests too.

**What to retain.** A test is a written-down expectation that a machine checks
on every change. Writing it first forces you to say what the code should do
before you say how. A coverage percentage is a way to find untested code, not
a measure of robustness.

**Lessons and readings.**
[Python Testing and Continuous Integration](https://carpentries-incubator.github.io/python-testing), Carpentries Incubator ·
[Test-Driven Development: By Example](https://www.oreilly.com/library/view/test-driven-development/0321146530/), Kent Beck ·
[pytest](https://docs.pytest.org/) ·
[Ruff](https://docs.astral.sh/ruff/) ·
[mypy](https://mypy.readthedocs.io/).

## 5. Documentation

[Browse the code at this step](https://github.com/tomboulier/tef-health-notebook-to-bedside/tree/step-5-documentation) ·
[See what this step changed](https://github.com/tomboulier/tef-health-notebook-to-bedside/compare/step-4-tests...step-5-documentation)

**Done here.** The [README](https://github.com/tomboulier/tef-health-notebook-to-bedside/blob/step-5-documentation/README.md) says
how to install, run and check the code, and which licence applies to what.
Every public function has a docstring in the Google style, several with
examples that pytest runs. Messages go through the `logging` module instead
of `print`. The first [architecture decision record](adr/index.md), in the
format proposed by Michael Nygard, records the injection of the data source.
[`CONTRIBUTING.md`](https://github.com/tomboulier/tef-health-notebook-to-bedside/blob/step-5-documentation/CONTRIBUTING.md),
[Usage](usage.md) and [Testing](testing.md) complete the set.

**What to retain.** Documentation is several things for several readers: a
how-to for the user, a reference for the developer, an explanation for the
reviewer. Docstrings with examples stay true because they are tested;
decision records stay useful because they are never rewritten.

**Lessons and readings.**
[Diátaxis](https://diataxis.fr/) ·
[PEP 257](https://peps.python.org/pep-0257/) ·
[doctest](https://docs.python.org/3/library/doctest.html) ·
[Logging HOWTO](https://docs.python.org/3/howto/logging.html) ·
[Better Research Software](https://carpentries-incubator.github.io/better-research-software/), Carpentries Incubator ·
[Architecture decision records](https://adr.github.io/).

## 6. Automation

[Browse the code at this step](https://github.com/tomboulier/tef-health-notebook-to-bedside/tree/step-6-automation) ·
[See what this step changed](https://github.com/tomboulier/tef-health-notebook-to-bedside/compare/step-5-documentation...step-6-automation)

**Done here.** A GitHub Actions
[workflow](https://github.com/tomboulier/tef-health-notebook-to-bedside/blob/step-6-automation/.github/workflows/ci.yml) runs Ruff,
mypy, pytest and the doctests on every push and pull request, builds the
container image and runs the tests inside it. It also runs every Monday, so
that a change in the world around the code (a withdrawn package, a moved
download) is found within a week. A second workflow builds this site with
MkDocs and publishes it on GitHub Pages. The version number, 0.1.0 to start
with, and `CHANGELOG.md` are derived from the Conventional Commits by
python-semantic-release, and the command line prints the version with
`--version`. Nothing is published to PyPI; [Automation and
releases](automation.md) describes how it would be done.

**What to retain.** Whatever is checked by hand is checked sometimes. A
workflow that runs the checks on every change turns "we should test this"
into "this was tested", and leaves a record of it.

**Lessons and readings.**
[GitHub Actions](https://docs.github.com/en/actions) ·
[Publishing a Python package](https://carpentries-incubator.github.io/python-packaging-publishing/), Carpentries Incubator ·
[GitHub Pages](https://pages.github.com/) ·
[python-semantic-release](https://python-semantic-release.readthedocs.io/) ·
[Semantic Versioning](https://semver.org/) ·
[Keep a Changelog](https://keepachangelog.com/).

## Practise: changing one thing

The page [Changing one thing](exercises.md) goes through three corrections
made in this repository, each isolated in one place of the code and, in two
cases out of three, in one commit. It then proposes five exercises: turn off
the horizontal flip, switch to the archived data, move the optimizer settings
to the configuration, undo a correction with `git revert`, and change the
pretrained network.

## Working with coding agents

Much of the code in this repository was written with a coding agent, under the
instructions of `AGENTS.md` and the checks of the continuous integration. The
references below describe the practice from several angles; none of them is a
recommendation.

- Bridgeford et al., *Twelve quick tips for AI-assisted coding in science*,
  PLOS Computational Biology, 2026, <https://doi.org/10.1371/journal.pcbi.1014428>.
- O'Brien and Eisty, *Scientific Software in the Age of Vibe Coding*,
  Computing in Science & Engineering, 2026, <https://doi.org/10.1109/MCSE.2026.3661610>.
- Elle O'Brien, *Who is scientific code for? Maintaining human-readable landmarks in agent-written code*, 2026, <https://arxiv.org/abs/2607.25975>.
- Birgitta Böckeler, *Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl*, 2025,
  <https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html>;
  Thoughtworks, *Spec-driven development: Unpacking one of 2025's key new AI-assisted engineering practices*, 2025,
  <https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices>.
- Examples of tools for specification-driven work:
  [spec-kit](https://github.com/github/spec-kit),
  [BMAD](https://github.com/bmad-code-org/BMAD-METHOD),
  [Kiro](https://kiro.dev/docs/specs/),
  [Tessl](https://tessl.io/).
- Instruction files for agents, as open conventions shared by most tools:
  [AGENTS.md](https://agents.md) and [Agent Skills](https://agentskills.io/).
- Policies and guides:
  [The Carpentries' GenAI policy](https://docs.carpentries.org/policies/genai-policy.html);
  [Responsible use of AI in research software](https://www.software.ac.uk/guide/responsible-use-ai-research-software), Institute for Research Software;
  [Developing Research Software with Generative AI](https://carpentries-incubator.github.io/software-development-with-genai/), Carpentries Incubator.
- Measured effects: Becker et al. (METR), *Measuring the Impact of Early-2025 AI on
  Experienced Open-Source Developer Productivity*, 2025, <https://arxiv.org/abs/2507.09089>,
  and METR's follow-up of February 2026, <https://metr.org/blog/2026-02-24-uplift-update/>.

## Background reading

- Hannay et al., *How do scientists develop and use scientific software?*, 2009, <https://doi.org/10.1109/SECSE.2009.5069155>.
- Merali, *Computational science: ...Error*, Nature, 2010, <https://doi.org/10.1038/467775a>.
- Sandve et al., *Ten simple rules for reproducible computational research*, PLOS Computational Biology, 2013, <https://doi.org/10.1371/journal.pcbi.1003285>.
- Wilson et al., *Best practices for scientific computing*, PLOS Biology, 2014, <https://doi.org/10.1371/journal.pbio.1001745>.
- McDermott et al., *Reproducibility in machine learning for health research: Still a ways to go*, Science Translational Medicine, 2021, <https://doi.org/10.1126/scitranslmed.abb1655>.
- Heil et al., *Reproducibility standards for machine learning in the life sciences*, Nature Methods, 2021, <https://doi.org/10.1038/s41592-021-01256-7>.
- Varoquaux and Cheplygina, *Machine learning for medical imaging: methodological failures and recommendations for the future*, npj Digital Medicine, 2022, <https://doi.org/10.1038/s41746-022-00592-y>.

## About

Repository: <https://github.com/tomboulier/tef-health-notebook-to-bedside> ·
this page: <https://tomboulier.github.io/tef-health-notebook-to-bedside/>.

This page and the repository are a capsule of the TEF-Health training course,
produced at Université Grenoble Alpes. TEF-Health, the Testing and
Experimentation Facility for Health AI and Robotics, is funded by the
European Union under grant agreement No 101100700.

The code is licensed under the MIT licence and the documentation, this page
included, under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
