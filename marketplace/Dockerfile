FROM python:3.11-slim

RUN pip install uv

RUN python -m uv venv /venv
ENV PATH="/venv/bin:$PATH"

WORKDIR /app
COPY pyproject.toml .

RUN uv pip install -r pyproject.toml

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]