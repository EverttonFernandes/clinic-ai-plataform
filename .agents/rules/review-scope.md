---
name: review-scope
description: "Revisar o mesmo conteúdo incluindo arquivos novos, staged, unstaged e consumidores."
applies_when:
  - "QA, revisão ou escolha de testes"
progressive_disclosure:
  - Ler nome, descrição e condições antes do corpo.
  - Abrir apenas o detalhe necessário ao estado da tarefa.
  - Consultar complementos somente se a condição se aplicar.
conditional_details:
  - if: "revisão antes de commit"
    then: "comparar com base da demanda e inspecionar working tree e novos"
  - else_if: "revisão após push"
    then: "verificar SHA publicado e base remota reais"
  - else: "arquivo privado explicitamente no escopo"
    then: "listar caminho individual; nunca varrer secrets por rotina"
---

# Escopo compartilhado

Registrar base anterior à demanda e distinguir alterações preexistentes. Usar Git com
terminadores NUL em automação de caminhos. Inspecionar commits da demanda, staged,
unstaged e `git ls-files --others --exclude-standard`; diff remoto vazio não prova ausência de trabalho.

Arquivos de produção, contratos, testes, configuração e consumidores relevantes entram no scope.
Não incluir plano/progress/log/parecer no próprio digest de código: isso causaria invalidação circular.
Diretórios de scope capturam novos arquivos; não omitir novidade para baratear a validação.

O revisor confronta scope declarado com diff real. Arquivos ignorados só quando
explicitamente necessários à demanda; não forçar prompts, .env ou diretórios privados ao Git.
Antes de release, inspecionar artifact e runtime também; revisão de fonte não prova pacote publicado.
