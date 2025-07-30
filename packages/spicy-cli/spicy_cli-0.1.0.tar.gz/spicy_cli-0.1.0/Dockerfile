# Use an official Python runtime as the base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install dependencies
COPY pyproject.toml README.md ./
COPY src ./src/

# Install the package
RUN pip install --no-cache-dir .

# Set the entrypoint
ENTRYPOINT ["spicy"]
CMD ["--help"]
