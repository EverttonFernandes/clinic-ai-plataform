#!/usr/bin/env bash
# Ensaio CT-001 isolado: nenhum recurso/volume de desenvolvimento é removido.
set -euo pipefail
cd "$(dirname "$0")/.."

smoke_project="clinic-ai-test-$(date +%s)-$$"
export API_PORT=0 POSTGRES_DB=clinic_smoke POSTGRES_USER=clinic_smoke
export POSTGRES_PASSWORD=synthetic-smoke-only
compose=(docker compose --env-file .env.example --project-name "$smoke_project")

cleanup() {
    result=$?
    trap - EXIT
    "${compose[@]}" down --timeout 10 || result=1
    printf 'Projeto %s encerrado; volumes preservados para inspeção.\n' "$smoke_project"
    exit "$result"
}
trap cleanup EXIT

printf 'Subida limpa: %s\n' "$smoke_project"
"${compose[@]}" build api smoke
"${compose[@]}" up --detach --wait --wait-timeout 120 api
"${compose[@]}" run --rm --no-deps smoke

printf 'Runtime sem root e sem compilador/pytest\n'
"${compose[@]}" exec -T api sh -ec 'test "$(id -u)" = 10001; ! command -v gcc; ! python -m pip show pytest >/dev/null 2>&1'

for dependency in postgres redis; do
    printf 'Indisponibilidade e recuperação: %s\n' "$dependency"
    "${compose[@]}" stop "$dependency"
    "${compose[@]}" run --rm --no-deps -e EXPECT_UNAVAILABLE=1 smoke -k 'liveness or readiness'
    "${compose[@]}" up --detach --wait --wait-timeout 120 api
    "${compose[@]}" run --rm --no-deps smoke
done

printf 'Persistência PostgreSQL e Redis após down/up sem excluir volumes\n'
"${compose[@]}" exec -T postgres psql -U clinic_smoke -d clinic_smoke -v ON_ERROR_STOP=1 -c \
    "CREATE TABLE smoke_marker (value text PRIMARY KEY); INSERT INTO smoke_marker VALUES ('synthetic-ct001');"
"${compose[@]}" exec -T redis redis-cli SET smoke:ct001 synthetic-ct001
"${compose[@]}" down --timeout 10
"${compose[@]}" up --detach --wait --wait-timeout 120 api
sql_marker=$("${compose[@]}" exec -T postgres psql -U clinic_smoke -d clinic_smoke -At -v ON_ERROR_STOP=1 -c 'SELECT value FROM smoke_marker')
redis_marker=$("${compose[@]}" exec -T redis redis-cli --raw GET smoke:ct001)
test "$sql_marker" = synthetic-ct001
test "$redis_marker" = synthetic-ct001
"${compose[@]}" run --rm --no-deps smoke
printf 'PASS: HTTP, pgvector, Redis, falhas, recuperação, runtime e persistência reais.\n'
