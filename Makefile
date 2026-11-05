ENV_FILE ?= .env.example
COMPOSE = docker compose --env-file $(ENV_FILE)

.PHONY: build up down smoke
build:
	$(COMPOSE) build api

up:
	$(COMPOSE) up --build --detach --wait --wait-timeout 120 api

down:
	$(COMPOSE) down

smoke:
	bash scripts/smoke-environment.sh
