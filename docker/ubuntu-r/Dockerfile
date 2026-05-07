# ---------------------- Build stage: compile R packages ----------------------
FROM ubuntu:22.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Etc/UTC \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    R_LIBS_SITE=/usr/local/lib/R/site-library

# 1) Install & preconfigure tzdata FIRST to avoid interactive prompts
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata && \
    ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    echo "Etc/UTC" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata && \
    rm -rf /var/lib/apt/lists/*

# 2) Now it’s safe to install everything else (no prompts)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl gnupg \
    r-base \
    build-essential pkg-config \
    unixodbc-dev \
    libssl-dev libcurl4-openssl-dev libxml2-dev \
    libfontconfig1-dev libfreetype6-dev libharfbuzz-dev \
    libfribidi-dev libglib2.0-dev \
    libpng-dev libjpeg-dev libtiff-dev \
 && rm -rf /var/lib/apt/lists/*

# Ensure the target library path exists and is used for installs
RUN mkdir -p "${R_LIBS_SITE}"

# Install packages (compiled here)
RUN R -q -e "options(repos='https://packagemanager.posit.co/cran/__linux__/jammy/latest');" \
         -e ".libPaths(Sys.getenv('R_LIBS_SITE'));" \
         -e "install.packages(c('DBI','odbc','tidyverse','logger'))"


# ---------------------- Runtime stage: slim image ----------------------
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Etc/UTC \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    R_LIBS_SITE=/usr/local/lib/R/site-library

# 1) Install & preconfigure tzdata FIRST here too
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata && \
    ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    echo "Etc/UTC" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata && \
    rm -rf /var/lib/apt/lists/*

# 2) Now install runtime bits (no compilers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl gnupg \
    r-base \
    unixodbc \
    libcurl4 libssl3 libxml2 \
    libfontconfig1 libfreetype6 libharfbuzz0b libfribidi0 \
    libglib2.0-0 libpng16-16 libjpeg-turbo8 libtiff5 \
 && rm -rf /var/lib/apt/lists/*

# Microsoft SQL Server ODBC Driver 18 (signed-by; no apt-key)
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc \
      | gpg --dearmor -o /etc/apt/keyrings/microsoft.gpg && \
    echo "deb [arch=amd64,arm64 signed-by=/etc/apt/keyrings/microsoft.gpg] https://packages.microsoft.com/ubuntu/22.04/prod jammy main" \
      > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 && \
    rm -rf /var/lib/apt/lists/*

# Bring in compiled R packages from builder
COPY --from=builder /usr/local/lib/R/site-library /usr/local/lib/R/site-library

# Non-root user & workspace
RUN useradd -m -u 10001 app
WORKDIR /app
RUN mkdir -p /app/scripts && chown -R app:app /app
USER app

ENTRYPOINT ["Rscript"]
# CMD ["./scripts/your_entry.R"]  # optional default command
