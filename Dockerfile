FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app/src:/app"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt /app/requirements.txt
COPY api/requirements.txt /app/api/requirements.txt

# Install all dependencies
RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt \
    && pip install -r /app/api/requirements.txt

# Copy the rest of the application
COPY . /app

# Install the package in editable mode so src/ is discoverable
RUN pip install -e .

# App Runner uses PORT 8080 by default in many configs, consistent with your app
EXPOSE 8080

# Start the API using uvicorn
CMD ["python3", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
