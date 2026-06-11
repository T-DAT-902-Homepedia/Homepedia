FROM python:3.13-slim

# Installer uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Installer les dépendances en premier pour tirer parti du cache Docker
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# Le code source est monté via bind mount en dev
EXPOSE 8000

CMD ["uv", "run", "fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]
