# Homepedia

The Homepedia app provides users with comprehensive information and analysis on
the housing market in France.

Le projet est éclaté en plusieurs repos dédiés :

| Repo | Rôle |
|------|------|
| [`api`](https://github.com/T-DAT-902-Homepedia/api) | API choroplèthe read-only (FastAPI + asyncpg) |
| [`webapp`](https://github.com/T-DAT-902-Homepedia/webapp) | Front (React + deck.gl) |
| [`pipelines`](https://github.com/T-DAT-902-Homepedia/pipelines) | Pipelines de données (Kedro / Spark) |
| [`schemas`](https://github.com/T-DAT-902-Homepedia/schemas) | Schéma PostGIS — source de vérité |
| [`docs`](https://github.com/T-DAT-902-Homepedia/docs) | Documentation (mdBook) et directives |
