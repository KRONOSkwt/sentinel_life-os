# apps/backend/Dockerfile
FROM python:3.12-slim AS base

WORKDIR /app

# Install dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

# Copy source
COPY src/ ./src/

# Create data directory
RUN mkdir -p /app/data

EXPOSE 8000

# Production target
FROM base AS production
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Dev target (with hot reload)
FROM base AS development
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]