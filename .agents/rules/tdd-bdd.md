---
name: tdd-bdd
description: "Definir comportamento e obter Red e Green antes de concluir código produtivo."
applies_when:
  - "conforme condição da tarefa"
progressive_disclosure:
  - Ler nome, descrição e condições antes do corpo.
  - Abrir apenas o detalhe necessário ao estado da tarefa.
  - Consultar complementos somente se a condição se aplicar.
conditional_details:
  - if: "comportamento novo ou corrigido"
    then: "cenário funcional Red antes do código; Green e revisão de coesão"
  - else_if: "refatoração coberta"
    then: "baseline verde e regressão"
  - else: "documentação sem comportamento"
    then: "validar conteúdo e links, sem teste fictício"
---

# Comportamento antes do código

- Cenário de aceite em Dado/Quando/Então antecede a implementação.
- Converter o cenário crítico em teste funcional/integrado executável e obter Red por
  comportamento ausente/incorreto. Import quebrado, banco fora ou credencial ausente não provam Red funcional.
- Implementar a menor mudança que produz Green. Unitários também podem conduzir regras internas
  pelo ciclo Red/Green; complementar os casos críticos depois, sem espelhar a implementação.
- Revisar coesão e clareza após validação; refatorar somente o necessário e reexecutar regressões.
- Casos de autorização, concorrência e custo acompanham cada incremento relevante.
- Gherkin nas histórias ainda é documentação, não evidência de teste executado.

Em refatoração coberta, obter baseline verde antes de alterar estrutura. Em tarefa somente
documental, TDD/BDD executável não se aplica: validar links, conteúdo e coerência.
Detalhes em [testes](../../docs/spec-driven-development/testes.md).
