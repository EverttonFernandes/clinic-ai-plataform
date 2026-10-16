---
name: ralph-loop
description: "Conduzir uma história ou sequência explicitamente solicitada do Kanban Clínica IA até critérios e evidências completos; não iniciar produto em tarefas só documentais."
metadata:
  progressive_disclosure:
    - Ler nome e descrição para decidir aplicabilidade.
    - Abrir somente a skill e as referências necessárias ao passo atual.
  conditional_details:
    - if: "história ativa"
      then: "perceber/orientar/decidir/agir/registrar com gates e correções"
    - else_if: "falha recorrente ou impasse"
      then: "bug-resolution sem zerar histórico"
    - else_if: "gates locais satisfeitos"
      then: "outro modelo revisa; CI e PR; aguardar usuário em Review"
    - else: "escopo pontual"
      then: "menor skill aplicável, sem iniciar a fila inteira"
---

# Ralph Loop — Clínica IA

Objetivo: fechar o escopo autorizado com prova, sem encerrar na implementação parcial.
Uma história solicitada não autoriza executar todo o backlog. Sequência contínua só quando pedida.

## Entrada mínima

Ler [índice de regras](../../rules/README.md), [Kanban](../../../docs/jira-pessoal/KANBAN-OFICIAL.md),
história atual, plano/progress existentes. Não carregar todas as histórias ou especialistas.
[Workflow](../../rules/workflow.md) e [tracking](../../rules/feature-tracking.md) governam início/retomada.
Modelos, branch e PR: [story-delivery](../../rules/story-delivery.md). A seleção de modelo deve
ser explícita/observável; não basta escrever Astra no plano. [Contexto](../../rules/context-management.md)
define checkpoints curtos e retomada após compactação.

## Ciclo

1. **Perceber:** estado real, mudanças anteriores, dependências, ownership, critérios e provas atuais.
2. **Orientar:** lacunas entre fonte, contrato do plano, diff e gates; ler rules condicionais relevantes.
3. **Decidir:** próxima ação verificável com escopo pequeno; fila de correções tem prioridade sobre nova história.
4. **Agir:** BDD/TDD e implementação mínima; testes por impacto; revisão de coesão após validação.
5. **Registrar:** hipótese/ação/resultado, correções, blockers e próxima ação em plano/progress. Heartbeat quando significativo.

Antes do código, usar [formato de plano](../../../docs/tasks/TEMPLATE.md).
Executar gates por CLI, nunca preencher PASS por relato. Se falhar, preservar incidente e
usar [recuperação](../../rules/iteration-recovery.md); três correções rejeitadas no mesmo
incidente exigem diagnóstico, não outra rodada de palpites.

## Roteamento por necessidade

- Testes/consumidores: [test-impact-analyzer](../test-impact-analyzer/SKILL.md).
- Correção recorrente: [bug-resolution](../bug-resolution/SKILL.md).
- Revisão da entrega: [independent-review](../independent-review/SKILL.md) com qa-review.
- Mudança neste harness: [harness-evaluator](../harness-evaluator/SKILL.md).
- Commit/release: [git-operator](../git-operator/SKILL.md), somente no escopo autorizado.
- Código/scripts/testes: [cohesive-code-development](../cohesive-code-development/SKILL.md).

Skills são modos de trabalho, não agentes já executados. O usuário autorizou executor
Astra/medium e revisão Sol em execuções distintas; não usar fallback nas histórias.

## Saída e continuidade

Concluir com critérios e cenários completos, comandos reais verdes, correções/bloqueios
resolvidos e revisão válida; estágios local/pre-pr aprovados permitem abrir PR, não Done.
Aguardar revisão/merge do usuário em Review, sem iniciar outra história. Após merge,
coletar human_review e `harness_completion.py check` aprovado. Depois, finish e Kanban.
Se release/CI externa faz parte do aceite, seus gates continuam obrigatórios.

Falha técnica corrigível mantém o loop. Impedimento externo registra PENDING/BLOCKED e
ação mínima; não converte para N/A. Handoff permite retomar sem perder tentativa ou recomeçar do zero.
O verificador não executa este loop automaticamente nem impede toda edição manual.
