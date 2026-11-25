# Container image that runs the notebook from top to bottom, without a
# browser, with the exact dependency versions of uv.lock.
#
#   docker build --tag hello-world-medical-imaging .
#   docker run --rm --volume "$PWD/data:/app/data" --volume "$PWD/outputs:/app/outputs" \
#       hello-world-medical-imaging
#
# The executed notebook, with its outputs, is written to outputs/.
FROM python:3.12.16-slim

# uv installs the locked dependencies; its version is pinned like any other.
COPY --from=ghcr.io/astral-sh/uv:0.11.32 /uv /uvx /bin/

WORKDIR /app
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

# Dependencies first, so that this layer is reused when only the notebook changes.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY config.toml ./
COPY notebooks ./notebooks
RUN mkdir outputs

# papermill runs the notebook in its own folder, as Jupyter does.
CMD ["papermill", "--cwd", "notebooks", \
     "notebooks/tuto-hello-world-deep-learning-medical-imaging.ipynb", \
     "outputs/tuto-hello-world-deep-learning-medical-imaging.ipynb"]
