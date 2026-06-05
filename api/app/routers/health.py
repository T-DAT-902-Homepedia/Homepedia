"""Endpoint de santé."""

import asyncpg
from fastapi import APIRouter, Depends

from ..db import get_connection

router = APIRouter(tags=["health"])


@router.get("/healthz")
async def healthz(conn: asyncpg.Connection = Depends(get_connection)) -> dict:
    """Vérifie l'API et la connexion PostGIS."""
    await conn.execute("SELECT 1;")
    return {"status": "ok"}
