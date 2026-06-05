-- Active l'extension PostGIS sur la base homepedia (couche Gold du pipeline DVF).
-- Exécuté automatiquement par l'image postgis au premier démarrage du volume.
CREATE EXTENSION IF NOT EXISTS postgis;
