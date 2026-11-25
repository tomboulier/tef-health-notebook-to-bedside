# Container image that trains the classifier, or runs the tests, with the
# exact dependency versions of uv.lock.
#
#   docker build --tag hello-world-medical-imaging .
#   docker run --rm --volume "$PWD/data:/app/data" --volume "$PWD/outputs:/app/outputs" \
#       hello-world-medical-imaging
#   docker run --rm hello-world-medical-imaging pytest
#
# The trained model and the training curves are written to outputs/.
FROM python:3.12.16-slim

# uv installs the locked dependencies; its version is pinned like any other.
COPY --from=ghcr.io/astral-sh/uv:0.11.32 /uv /uvx /bin/

WORKDIR /app
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

# Dependencies first, so that this layer is reused when only the code changes.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# Then the package itself, its configuration and its tests.
COPY README.md config.toml ./
COPY src ./src
COPY tests ./tests
RUN uv sync --frozen

CMD ["hello-world-medical-imaging", "--config", "config.toml"]
