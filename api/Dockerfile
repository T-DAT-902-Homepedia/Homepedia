FROM python:3.13-slim

WORKDIR /app

# Dépendances d'abord (cache de build).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

# En conteneur, la base est accessible via le service `postgis` du compose.
# Surcharger API_DATABASE_URL si besoin.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
