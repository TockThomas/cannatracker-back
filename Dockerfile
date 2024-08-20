FROM python:3.11-slim AS builder

COPY . /app

WORKDIR /app

RUN pip3 install poetry --no-cache-dir --upgrade
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-root --only=main --no-ansi -vvv --no-cache --no-interaction

FROM python:3.11-slim AS base

COPY --from=builder /app /app

WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app:$PATH"

RUN pip install --no-cache-dir --upgrade "fastapi[standard]"

EXPOSE 80
CMD ["fastapi", "run", "src/main.py", "--port", "80"]