"""Composição dos recursos técnicos da API; sem regras de negócio."""

from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import psycopg
from redis import Redis
from redis.backoff import NoBackoff
from redis.exceptions import RedisError
from redis.retry import Retry


def dependencies_ready(cache: Redis) -> bool:
    """Consulta dependências reais, com limites de conexão e execução."""
    try:
        with psycopg.connect(
            connect_timeout=2, options="-c statement_timeout=2000", autocommit=True
        ) as connection:
            vector_installed = connection.execute(
                "SELECT 1 FROM pg_extension WHERE extname = 'vector'"
            ).fetchone()
        return vector_installed is not None and cache.ping()
    except (psycopg.Error, RedisError):
        return False


def create_app() -> FastAPI:
    cache = Redis(
        host=os.environ["REDIS_HOST"],
        socket_connect_timeout=2,
        socket_timeout=2,
        retry=Retry(NoBackoff(), 0),
    )

    @asynccontextmanager
    async def lifespan(app):
        yield
        cache.close()

    app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)

    @app.get("/health/live")
    def liveness():
        return {"status": "alive"}

    @app.get("/health/ready")
    def readiness():
        if dependencies_ready(cache):
            return {"status": "ready"}
        return JSONResponse(status_code=503, content={"status": "unavailable"})

    return app
