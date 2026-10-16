# Planejamento da implementação

Esta pasta versiona apenas o novo planejamento. Os prompts antigos continuam locais e ignorados.

1. [Especificação normativa](../spec.md): escopo, requisitos e invariantes.
2. [Kanban oficial](jira-pessoal/KANBAN-OFICIAL.md): fila única de execução cronológica.
3. [Decisões e pendências](spec-driven-development/decisoes.md): stack, simplificações e limites.
4. [Matriz de rastreabilidade](spec-driven-development/rastreabilidade.md): requisito → história → prova.
5. [Estratégia de testes](spec-driven-development/testes.md): BDD/TDD, testes funcionais, evals e falhas.
6. [Ambientes e CI/CD](spec-driven-development/ambientes-e-cicd.md): contratos de automação a implementar.
7. [Template de tarefa](tasks/TEMPLATE.md) e [template de entrega](entregas/TEMPLATE.md).
8. [Harness de execução](spec-driven-development/harness.md), [evals e LLM-as-a-Judge](spec-driven-development/evals-harness.md) e [tracking](tracking/README.md).

Histórias de negócio ficam em `jira-pessoal/historias/`; técnicas em `historias-tecnicas/`.
Todas são selecionadas pelo mesmo Kanban. Não há código de aplicação ou pipeline do produto nesta etapa;
a CI definida e os contratos executados pertencem somente ao harness de desenvolvimento.
Histórias seguem [branch, outro modelo revisor, CI e PR](../.agents/rules/story-delivery.md).
O usuário revisa e faz merge; o agente mantém Review até esse aceite, com handoff entre sessões.
