FROM python:slim

WORKDIR app
COPY poetry.lock .
COPY pyproject.toml .
COPY . /app

RUN pip install poetry

RUN poetry install --no-interaction --no-ansi
