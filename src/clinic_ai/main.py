"""Entrada ASGI da API; a composição de recursos pertence ao bootstrap."""

from clinic_ai.bootstrap import create_app

app = create_app()
