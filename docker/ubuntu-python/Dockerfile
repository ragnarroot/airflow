# -------- Build stage: compile any wheels that need build deps --------
FROM ubuntu:22.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Base tools and build deps (kept ONLY in this stage)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl gnupg \
    python3 python3-pip python3-venv \
    build-essential pkg-config \
    unixodbc-dev \
 && rm -rf /var/lib/apt/lists/*

# Python deps: build wheels in an isolated directory (no cache)
# Pin versions in practice (e.g., pandas==2.2.2, etc.) or use a requirements.txt with hashes.
RUN python3 -m pip install --upgrade --no-cache-dir pip wheel && \
    mkdir -p /wheelhouse && \
    python3 -m pip wheel --no-cache-dir \
      pandas numpy requests aiohttp nest_asyncio msal pyodbc sqlalchemy \
      -w /wheelhouse

# -------- Runtime stage: minimal surface, signed repo keys, non-root --------
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Core runtime libs only (no compilers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl gnupg \
    python3 python3-pip \
    unixodbc \
 && rm -rf /var/lib/apt/lists/*

# Microsoft repo (signed-by; no deprecated apt-key)
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc \
      | gpg --dearmor -o /etc/apt/keyrings/microsoft.gpg && \
    echo "deb [arch=amd64,arm64 signed-by=/etc/apt/keyrings/microsoft.gpg] https://packages.microsoft.com/ubuntu/22.04/prod jammy main" \
      > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
      msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

# Install prebuilt wheels from builder (drops the need for build-essential here)
COPY --from=builder /wheelhouse /wheelhouse
RUN python3 -m pip install --no-cache-dir /wheelhouse/* && rm -rf /wheelhouse

# App user & workspace
RUN useradd -m -u 10001 app
WORKDIR /app
RUN mkdir -p /app/scripts && chown -R app:app /app
USER app

# If you truly need scripts to be executable, set perms on specific files after COPY in your own image.
# COPY your scripts in the image that extends this base:
# COPY --chown=app:app ./python_scripts/ /app/scripts/
# RUN chmod +x /app/scripts/*.py

# Keep the same entrypoint behavior
ENTRYPOINT ["python3"]
# Or prefer CMD so users can override easily:
# CMD ["-c", "print('hello')"]
