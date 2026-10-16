---
name: clean-code-readable-names
description: "Manter nomes, responsabilidades e fronteiras legíveis em código e automação."
applies_when:
  - "conforme condição da tarefa"
progressive_disclosure:
  - Ler nome, descrição e condições antes do corpo.
  - Abrir apenas o detalhe necessário ao estado da tarefa.
  - Consultar complementos somente se a condição se aplicar.
conditional_details:
  - if: "código/scripts/testes novos"
    then: "manter responsabilidade e nomes do domínio"
  - else_if: "acoplamento ou duplicação concreta"
    then: "refatoração localizada após baseline verde"
  - else: "documentação"
    then: "não reorganizar aplicação"
---

# Clareza e responsabilidade

- Preferir funções/módulos pequenos com nomes do domínio; não criar classe por função ou interface sem consumidor.
- HTTP/canal adapta entrada; serviço valida regra; persistência concentra SQL; adapter isola dependência externa.
- Agent decide proposta, backend controla execução. Tools não consultam bancos nem aceitam capacidades genéricas.
- Extrair quando há motivo concreto: regra repetida, responsabilidade distinta, teste difícil ou dependência indevida.
- Evitar `utils`, `manager`, flags ambíguas, estado global implícito e comentários que apenas narram o código.
- Erros de domínio têm significado estável; não vazar stacktrace, SQL, secrets ou nomes internos à interface do paciente.
- Em script/CI, nomes devem explicar finalidade; comandos destrutivos não se escondem em cleanup genérico.

Revisão usa [refactor-after-functional-green.md](refactor-after-functional-green.md);
nenhuma reorganização ampla é exigida por padrão.
