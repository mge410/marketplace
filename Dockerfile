FROM python:3.13-slim

RUN apt-get update && apt-get install -y make gcc openssl git && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install uv
WORKDIR /app

COPY pyproject.toml .
RUN uv pip install -r pyproject.toml --system
RUN uv sync

COPY src ./src
COPY .env ./.env

CMD ["python", "-m", "src.main"]
