FROM python:3.13-slim

RUN pip install uv

WORKDIR /app

COPY pyproject.toml .
RUN uv pip install -r pyproject.toml --system
RUN uv sync

COPY ./src ./src
COPY .env ./.env

CMD ["python", "-m", "src.main"]
