# Homepedia DVF API

API HTTP **read-only** exposant les données immobilières DVF pour la dataviz
cartographique (choroplèthe prix/m²). FastAPI + asyncpg, lecture seule sur PostGIS.

## Principe

Tout le calcul lourd est précalculé en amont (pipeline Kedro → PostGIS) :
- agrégats prix/m² par commune/département (`agg_commune`, `agg_departement`) ;
- contours administratifs pré-simplifiés à 3 niveaux de détail (`commune_geometry`,
  `departement_geometry`, colonnes `geom_low`/`geom_mid`/`geom_high`).

L'API se contente de **joindre** stats et géométrie et de renvoyer une
`FeatureCollection` GeoJSON **sérialisée par PostgreSQL** (`json_build_object` +
`ST_AsGeoJSON`) — aucun travail de sérialisation lourd côté Python. Réponses gzip +
`Cache-Control` long (la donnée ne change qu'au run du pipeline).

## Endpoints

```
GET /healthz
GET /api/v1/choropleth/communes?type_local=Appartement&lod=mid&code_departement=75
GET /api/v1/choropleth/departements?type_local=Appartement&lod=low
```

- `type_local` : `Appartement` (défaut) | `Maison`
- `lod` : `low` (dézoom national) | `mid` | `high` (zoom local) — sélectionne la
  colonne géométrie pré-simplifiée.
- `code_departement` (communes, optionnel) : restreint au département (payload réduit).

## Lancer en local

```bash
# Prérequis : PostGIS peuplé (compose.data.yml + pipelines gold/geo)
uv venv .venv && uv pip install -r requirements.txt
API_DATABASE_URL=postgresql://homepedia:changeme-postgres@localhost:5432/homepedia \
  .venv/bin/uvicorn app.main:app --reload
# Doc interactive : http://localhost:8000/docs
```

## En conteneur

Service `api` de `compose.data.yml` (build local, port 8000, branché au service
`postgis`). Config via variables `API_*` (voir `app/config.py`).
