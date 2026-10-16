---
name: story-workflow
description: "Executar a primeira história elegível com estado persistido e fechamento verificável."
applies_when:
  - "iniciar ou retomar história"
progressive_disclosure:
  - Ler nome, descrição e condições antes do corpo.
  - Abrir apenas o detalhe necessário ao estado da tarefa.
  - Consultar complementos somente se a condição se aplicar.
conditional_details:
  - if: "história ainda não iniciada"
    then: "ler Kanban/história, revisar dependências e preparar plano"
  - else_if: "retomada após interrupção"
    then: "ler plano e progress; reconciliar hashes, ownership e gates"
  - else: "demanda pontual do usuário"
    then: "usar plano próprio se necessário, sem mover histórias do produto"
---

# Execução e retomada

Ordem: [Kanban](../../docs/jira-pessoal/KANBAN-OFICIAL.md). Requisito: [spec](../../spec.md).
Seguir [tracking](feature-tracking.md) e [ownership](task-ownership.md) antes do código.

1. Inspecionar mudanças preexistentes e a primeira história elegível, incluindo consumidores;
   aplicar [modelos/branch/PR](story-delivery.md) e [handoff](context-management.md).
2. Criar `docs/tasks/<ID>/plano.md` e `progress.md` usando o [template](../../docs/tasks/TEMPLATE.md).
3. Incluir todos os critérios e cenários originais, escopo e gates aplicáveis; confirmar dependências.
4. Executar o ciclo [Ralph Loop](../skills/ralph-loop/SKILL.md): perceber → orientar → decidir → agir → registrar.
5. Implementar com BDD/TDD; revisão de coesão após validação e QA separado sobre o mesmo escopo.
6. Corrigir achados mantendo incidente/histórico; validar estágio local, CI do HEAD e estágio pre-pr.
7. Abrir PR e aguardar usuário em Review. Após revisão/merge manual, validar
   [conclusão](evidence-backed-completion.md). `finish` valida provas e libera ownership;
   só então atualizar Done no Kanban. Nenhum gate local autoriza merge pelo agente.

WIP inicial um; lock por tarefa não autoriza paralelismo. Tracking observa execução,
mas prioridade/estado de entrega publicados continuam no Kanban. Reconciliar divergências;
nunca usar JSON como fila alternativa. Demanda documental não inicia CT-001 implicitamente.
