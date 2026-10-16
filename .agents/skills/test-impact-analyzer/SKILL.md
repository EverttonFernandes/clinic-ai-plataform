---
name: test-impact-analyzer
description: "Selecionar gates e consumidores afetados por diff da Clínica IA, ampliando por risco sem omitir critérios."
metadata:
  progressive_disclosure:
    - Ler nome e descrição para decidir aplicabilidade.
    - Abrir somente a skill e as referências necessárias ao passo atual.
  conditional_details:
    - if: "mudança de regra ou contrato"
      then: "rastrear consumidores e funcionais afetados"
    - else_if: "tenant, schema, orçamento ou concorrência"
      then: "ampliar para integração/segurança/concorrência correspondentes"
    - else_if: "harness"
      then: "executar contratos do harness, não iniciar API"
    - else: "documentos"
      then: "links, coerência e critérios da demanda"
---

# Seleção de testes por impacto

Inspecionar [escopo real](../../rules/review-scope.md), imports, chamadas, migrations,
HTTP, tools e jobs consumidores. Git por diretório sozinho não demonstra ausência de impacto.
Consultar [matriz de testes](../../../docs/spec-driven-development/testes.md).

- Regra pura: unitários e funcional que a consome.
- Serviço/contrato/tool: integração e jornadas dos canais afetados.
- Tenant/schema/idempotência/budget: casos cruzados, concorrência e recuperação.
- Provider/prompt/retrieval: dataset relevante, custo, fallback e limites.
- Scripts do harness: `python3 -B -m unittest discover -s scripts/tests -v`.
- Rules/skills: validador de skills, links e evals de roteamento/completude do harness.
- Release/risco transversal: matriz integrada existente, não comandos futuros fingidos.

Registrar seleção, exclusões justificadas e ambiente. Impacto desconhecido exige investigar
ou ampliar. Não há seletor universal automático nem cobertura percentual obrigatória.
Mudança depois do gate, falha ou prova externa desatualizada exige revalidar o recorte pertinente.
