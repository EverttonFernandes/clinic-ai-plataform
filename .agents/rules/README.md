---
name: rules-index
description: "Roteamento progressivo do harness Clínica IA por tarefa, risco e estado de execução."
applies_when:
  - "qualquer tarefa"
progressive_disclosure:
  - Ler nome, descrição e condições antes do corpo.
  - Abrir apenas o detalhe necessário ao estado da tarefa.
  - Consultar complementos somente se a condição se aplicar.
conditional_details:
  - if: "iniciar ou retomar história"
    then: "workflow.md e feature-tracking.md; carregar o Ralph Loop"
  - else_if: "implementar comportamento"
    then: "tdd-bdd.md, test-evidence-quality.md e clean-code-readable-names.md"
  - else_if: "avaliar conclusão ou release"
    then: "evidence-backed-completion.md; versioning.md apenas se houver Git/release"
  - else: "consulta ou documentação pontual"
    then: "abrir somente a regra diretamente aplicável"
---

# Regras sob demanda

Ler nome/descrição e condições primeiro; abrir corpo e complementos somente quando a
condição se aplicar. Não carregar todas as personas nem todo o histórico a cada iteração.

| Situação | Abrir |
| --- | --- |
| História | [workflow](workflow.md), [tracking](feature-tracking.md), [ownership](task-ownership.md). |
| Branch, modelo, CI e PR de história | [entrega por história](story-delivery.md). |
| Loop longo/retomada | [janela de contexto e handoff](context-management.md). |
| Comportamento e testes | [BDD/TDD](tdd-bdd.md), [evidência](test-evidence-quality.md). |
| Código e clareza | [nomes/fronteiras](clean-code-readable-names.md), [revisão de coesão](refactor-after-functional-green.md). |
| Segurança/custo | [fronteiras e consumo](security-and-cost.md). |
| Revisão/conclusão | [escopo](review-scope.md), [gate de conclusão](evidence-backed-completion.md). |
| Falha recorrente | [recuperação](iteration-recovery.md). |
| Commit/tag/push | [versionamento](versioning.md), [entrega](delivery.md). |
| Mudança no harness | [evals do harness](harness-evals.md). |

Spec e Kanban são normativos. Há verificadores locais em scripts; eles não interceptam
todas as ferramentas da IDE e não substituem CI, revisão ou proteções remotas.
