---
name: cohesive-code-development
description: "Organizar responsabilidades e revisar coesão em código, scripts e testes; excluir leitura e documentação sem código."
metadata:
  progressive_disclosure:
    - Ler nome e descrição para decidir aplicabilidade.
    - Abrir somente a skill e as referências necessárias ao passo atual.
  conditional_details:
    - if: "há código/scripts/testes"
      then: "ler regras de nomes, TDD e evidência antes de implementar"
    - else_if: "validação verde"
      then: "revisar coesão e refatorar somente achado concreto"
    - else: "somente leitura/documentação"
      then: "não acionar esta skill"
---

# Desenvolvimento coeso

Antes de implementar, localizar o responsável pelo comportamento e seus consumidores.
Consultar [nomes e fronteiras](../../rules/clean-code-readable-names.md) e as regras de
[BDD/TDD](../../rules/tdd-bdd.md) e [evidências](../../rules/test-evidence-quality.md).

Manter a mudança no menor conjunto de módulos que possui essa responsabilidade.
Separar dependência externa somente quando isso permitir controlar a fronteira real;
não criar uma abstração para cada função.

Após validar, fazer a [revisão de coesão](../../rules/refactor-after-functional-green.md)
e registrar achados. Refatorar apenas um problema concreto, com regressão depois.
Não transformar uma história em reorganização ampla do projeto.
