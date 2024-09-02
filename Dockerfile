# Base stage
FROM python:3.11-slim AS base

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

# Default command
CMD ["python", "app/main.py"]

# Testing stage
FROM base AS test

CMD ["pytest", "tests"]
