---
name: architecture-ddd
description: "Preservar contextos, domínio puro e portas/adapters no monólito modular Python."
applies_when:
  - "planejar ou implementar módulo, contrato, persistência ou integração da plataforma"
progressive_disclosure:
  - Ler o mapa de contextos antes de introduzir dependências.
  - Consultar transações ou integrações futuras somente quando afetadas.
conditional_details:
  - if: "módulo ou caso de uso"
    then: "identificar contexto dono e dependências no guia de arquitetura"
  - else_if: "provider ou analytics"
    then: "preservar portas e consultar a evolução correspondente no guia"
  - else: "alteração sem impacto arquitetural"
    then: "manter mudança localizada"
---

# Fronteiras DDD

- Seguir [arquitetura DDD](../../docs/spec-driven-development/arquitetura-ddd.md).
- Organizar por contexto, com domínio/aplicação/entradas/infraestrutura conforme comportamento real.
- Domínio puro: sem FastAPI, ORM, Redis, SDK, ambiente ou internals de outro contexto.
- Aplicação usa domínio e portas; bootstrap liga adapters e controla recursos.
- Módulos conversam por contratos públicos e DTOs mínimos; sem SQL ou imports internos cruzados.
- Contexto confiável e autorização também se aplicam a chamadas internas, tools e workers.
- Unidade de trabalho do agendamento mantém efeito, resultado idempotente e outbox no commit.
- Banco compartilhado aceita constraints por IDs/tenant; tabelas e migrations têm dono.
- Não gerar pastas vazias, frameworks de domínio, barramento, repository genérico ou microserviços por padrão.
- Guardrails de importação nascem em CT-002 e crescem com os módulos; testes funcionais continuam obrigatórios.
- LiteLLM é adapter/proxy candidato; backend preserva autorização, budget e limite de tentativas.
- Databricks é evolução analítica assíncrona; atendimento não depende do lakehouse.
- Provas externas, dados reais e custos obedecem às condições das histórias e autorizações aplicáveis.
