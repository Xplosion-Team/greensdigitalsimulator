FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (kept minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
  && rm -rf /var/lib/apt/lists/*

# Install python deps
COPY pyproject.toml /app/pyproject.toml
COPY src /app/src
COPY api /app/api
COPY requirments.txt /app/requirments.txt

RUN pip install --upgrade pip \
 && pip install -r /app/api/requirements.txt \
 && pip install -r /app/requirments.txt \
 && pip install -e /app

ENV PORT=8080
EXPOSE 8080

CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
