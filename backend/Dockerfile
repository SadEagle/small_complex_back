FROM python:3.14-slim

# Install uv
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Verify uv installation
RUN which uv && uv --version

WORKDIR /backend
ENV PYTHONPATH=./

COPY ./uv.lock ./pyproject.toml ./
RUN uv sync --frozen

COPY ./app/ ./app/

# COPY ./alembic.ini ./
# COPY ./alembic/ ./alembic/

CMD ["uv", "run", "fastapi", "run", "--workers", "4", "./app/main.py", "--host", "0.0.0.0"]

EXPOSE 8000
