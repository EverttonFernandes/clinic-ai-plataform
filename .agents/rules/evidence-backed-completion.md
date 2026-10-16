---
name: evidence-backed-completion
description: "Recusar fechamento por relato, critério omitido, prova desatualizada ou revisão não identificada."
applies_when:
  - "planejar validação, revisar ou declarar conclusão"
progressive_disclosure:
  - Ler nome, descrição e condições antes do corpo.
  - Abrir apenas o detalhe necessário ao estado da tarefa.
  - Consultar complementos somente se a condição se aplicar.
conditional_details:
  - if: "gate sem execução, falha ou ambiente indisponível"
    then: "manter PENDING/FAIL; não converter em N/A"
  - else_if: "implementação pronta"
    then: "executar verificações, revisão identificada e completion check"
  - else: "documento ou consulta sem implementação"
    then: "validar a evidência pertinente sem inventar gates da aplicação"
---

# Conclusão baseada em evidências

O [template](../../docs/tasks/TEMPLATE.md) define frontmatter JSON, válido como YAML.
Fonte oficial imutável por hash, critérios AC e cenários BDD completos, escopo, comandos,
gates e fila de correções formam o contrato do plano.

1. `harness_completion.py criteria <história>` extrai checkboxes e cenários originais.
2. `verify <plano> <gate>` executa argv sem shell implícito e registra resultado/log/hash.
3. Revisar critérios, diff real, testes, resultados e limitações no mesmo snapshot.
4. Histórias: `check --stage local` → CI push → `check --stage pre-pr` → abrir PR →
   pr_ci pull_request → `check --stage post-pr` → Review.
   Após revisão/merge do usuário, coletar human_review, `check <plano>` e `finish`.
5. Atualizar entrega e Kanban sem alegar release/produção se o escopo é local.

O gate recusa AC/BDD omitido ou alterado, evidência ausente/expirada, comando falho,
timeout, log adulterado, snapshot alterado, correção aberta, bloqueio e checkbox pendente.
N/A é inaplicabilidade real com motivo; nunca substitui teste declarado ou gate de revisão.

Histórias exigem [revisão por outro modelo](../skills/independent-review/SKILL.md), sem
fallback. O contrato inclui a política de modelos/effort. Registrar identidades reais;
trocar de persona não cria outro agente. Manutenções sem essa exigência podem declarar
fallback com motivo, sem alegar independência. Não converter CI/aceite humano em N/A.
Os estágios local/pre-pr/post-pr nunca retornam completion_allowed: true.

Hashes detectam conteúdo desatualizado/acidente, não adulteração deliberada de quem
controla o disco. O verificador não prova que um comando é semanticamente suficiente;
QA e evals tentam refutar essa suficiência. [Limites](../../docs/spec-driven-development/harness.md).
