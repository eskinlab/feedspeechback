# GPU job image for Nebius Serverless AI.
# Build on linux/amd64 (WSL or CI):
#   docker build -t <registry>/feedspeechback-job:dev .
FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

COPY --from=ghcr.io/astral-sh/uv:0.11 /uv /uvx /bin/

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

ENV UV_PYTHON_INSTALL_DIR=/opt/python
RUN uv python install 3.12

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --only-group job --python 3.12

COPY app/ app/

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["python", "-m", "app.main"]
