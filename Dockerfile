FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app
COPY requirements.txt .
RUN uv venv && uv pip install -r requirements.txt

FROM python:3.12-slim

WORKDIR /app
COPY --from=builder /app/.venv .venv
COPY sync.py .
COPY zendesk/ zendesk/

CMD [".venv/bin/python", "sync.py"]
