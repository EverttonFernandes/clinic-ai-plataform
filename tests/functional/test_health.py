"""Contratos HTTP contra a API em processo separado e dependências reais."""

import json
import os
from urllib.error import HTTPError
from urllib.request import urlopen

import psycopg
import redis


def get_health(path):
    try:
        response = urlopen(os.environ["API_URL"] + path, timeout=6)
    except HTTPError as error:
        response = error
    with response:
        return response.status, json.load(response)


def test_liveness_independent_of_dependencies():
    assert get_health("/health/live") == (200, {"status": "alive"})


def test_readiness_matches_dependency_availability():
    if os.getenv("EXPECT_UNAVAILABLE") == "1":
        assert get_health("/health/ready") == (503, {"status": "unavailable"})
    else:
        assert get_health("/health/ready") == (200, {"status": "ready"})


def test_real_dependencies_support_vector_and_redis():
    with psycopg.connect(connect_timeout=3) as connection:
        distance = connection.execute("SELECT '[1,2,3]'::vector <-> '[1,2,4]'::vector").fetchone()[0]
    assert distance == 1.0
    with redis.Redis(host=os.environ["REDIS_HOST"], socket_timeout=3) as cache:
        assert cache.ping() is True
