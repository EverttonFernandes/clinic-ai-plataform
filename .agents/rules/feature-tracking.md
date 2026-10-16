---
name: feature-tracking
description: "Validar dependências e registrar execução sem substituir a prioridade do Kanban."
applies_when:
  - "história, dependências ou estado operacional"
progressive_disclosure:
  - Ler nome, descrição e condições antes do corpo.
  - Abrir apenas o detalhe necessário ao estado da tarefa.
  - Consultar complementos somente se a condição se aplicar.
conditional_details:
  - if: "primeiro uso do registry"
    then: "importar Kanban sem inferir conclusão"
  - else_if: "iniciar ou retomar"
    then: "revisar dependências; ready/start validam novamente fontes e provas"
  - else: "falha, revisão ou conclusão"
    then: "registrar evento; finish exige prova atual"
---

# Tracking operacional

Consultar [manual](../../docs/spec-driven-development/harness.md) para a sequência completa.

- Importar com `python3 -B scripts/feature_tracking.py import-kanban docs/jira-pessoal/KANBAN-OFICIAL.md`.
- Revisar `dependencies <ID> [pré-requisitos] --reason <motivo>` antes de start; o gate
  recusa omitir dependências declaradas no Kanban. A lista pode ampliar o recorte com justificativa.
- `ready <ID>` valida a árvore. `start <ID> --owner <execução-real>` repete os checks e adquire token local.
- Histórias exigem branch com seu ID. Review aguarda usuário; `finish` exige CI e merge
  da revisão correta pelo login configurado, além dos testes e do parecer por outro modelo.
- `failure`, `review` e `finish` exigem ownership ativo e `--lock-token`.
- Finalizar só depois do completion check; label DONE não substitui prova. Dependências
  aceitas usam prova histórica de CI/merge, fonte/contrato/parecer originais e ancestralidade,
  sem exigir código antigo idêntico à evolução atual ou renovar sua validade a cada 24h.
  Regressões atuais ficam nos testes/CI da história consumidora.
- Kanban é consultado no início: priorizar a primeira elegível e não executar Backlog opcional sem promoção explícita.

JSON registra eventos, não critérios duplicados ou prioridade paralela. Índice é regenerável;
não editar status/contadores manualmente. Importação é aditiva, preservando histórico.
Não inventar timestamps antigos, PASS ou falhas anteriores à importação.

Tracking pode registrar BLOCKED após falha técnica; o loop consulta a causa e corrige.
Isso não significa automaticamente necessidade de ação humana ou bloqueio externo no Kanban.
