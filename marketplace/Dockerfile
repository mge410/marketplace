FROM python:3.13-slim

RUN pip install uv

RUN python -m uv venv /venv
ENV PATH="/venv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml .
RUN uv pip install -r pyproject.toml
RUN uv sync

COPY ./src ./src
COPY .env ./.env

CMD ["python", "-m", "src.main"]
