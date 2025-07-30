FROM python:3.10-slim AS base

# Install system dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y build-essential git libportaudio2 pandoc && \
    rm -rf /var/lib/apt/lists/*

# Create app user with UID 1000
RUN useradd -m -u 1000 -s /bin/bash appuser

WORKDIR /app

# Create virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Playwright browser settings
ENV PLAYWRIGHT_BROWSERS_PATH=/home/appuser/pw-browsers
ENV PLAYWRIGHT_SKIP_BROWSER_GC=1

# Create directories with proper permissions
RUN mkdir -p /home/appuser/.codecraft /home/appuser/.cache /home/appuser/pw-browsers && \
    chown -R appuser:appuser /home/appuser /app /venv && \
    chmod -R 777 /home/appuser/.codecraft /home/appuser/.cache /home/appuser/pw-browsers

# So git doesn't complain about unusual permissions
RUN git config --system --add safe.directory /app

# This puts the container's ~/.codecraft into the host's project directory (usually host's cwd).
# That way caches, version checks, etc get stored in the host filesystem not
# simply discarded every time the container exits.
ENV HOME=/app

#########################
FROM base AS codecraft-full

ENV CODECRAFT_DOCKER_IMAGE=elevenlimitededition/codecraft-full

# Copy the package files
COPY . /app

# Fix git directory permissions
RUN if [ -d "/app/.git" ]; then chown -R appuser:appuser /app/.git; fi

# Install dependencies as root
RUN /venv/bin/python -m pip install --upgrade --no-cache-dir pip && \
    /venv/bin/python -m pip install --no-cache-dir -e /app[help,browser,playwright] boto3 \
       --extra-index-url https://download.pytorch.org/whl/cpu

# Install playwright browsers
RUN /venv/bin/python -m playwright install --with-deps chromium

# Fix site-packages permissions - use chmod directly on the directory for efficiency
RUN chmod -R a+rX /venv/lib/python3.10/site-packages

# Switch to appuser
USER appuser

# Use --no-git as a fallback in case git operations fail
ENTRYPOINT ["/venv/bin/codecraft"]

#########################
FROM base AS codecraft

ENV CODECRAFT_DOCKER_IMAGE=elevenlimitededition/codecraft

# Copy the package files
COPY . /app

# Fix git directory permissions
RUN if [ -d "/app/.git" ]; then chown -R appuser:appuser /app/.git; fi

# Install dependencies as root
RUN /venv/bin/python -m pip install --upgrade --no-cache-dir pip && \
    /venv/bin/python -m pip install --no-cache-dir -e /app[playwright] boto3 google-cloud-aiplatform \
       --extra-index-url https://download.pytorch.org/whl/cpu

# Install playwright browsers
RUN /venv/bin/python -m playwright install --with-deps chromium

# Fix site-packages permissions - use chmod directly on the directory for efficiency
RUN chmod -R a+rX /venv/lib/python3.10/site-packages

# Switch to appuser
USER appuser

# Use --no-git as a fallback in case git operations fail
ENTRYPOINT ["/venv/bin/codecraft"]
