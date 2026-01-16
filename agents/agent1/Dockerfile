# Minimal container for agent1 installed from a wheel
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install build tooling (flit via build) and any system deps if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir build

# Copy project files (include LICENSE for flit license-files) and build wheel
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN python -m build --wheel --outdir /tmp/wheels

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install agent1 from the built wheel
COPY --from=builder /tmp/wheels /tmp/wheels
RUN pip install --no-cache-dir /tmp/wheels/*.whl

# Default command; override with args
CMD ["agent1", "World"]
