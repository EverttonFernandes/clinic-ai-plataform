---
name: executar-historia
description: "Selecionar a próxima história elegível da Clínica IA e encaminhar ao Ralph Loop; excluir documentação pontual."
metadata:
  progressive_disclosure:
    - Ler nome e descrição para decidir aplicabilidade.
    - Abrir somente a skill e as referências necessárias ao passo atual.
  conditional_details:
    - if: "pedido de implementar história"
      then: "ler Kanban e usar ralph-loop"
    - else_if: "retomada"
      then: "ler plano/progress e estado de ownership antes de continuar"
    - else: "pedido de documentação ou consulta"
      then: "tratar diretamente sem iniciar aplicação"
---

# Entrada de execução de histórias

Esta skill mantém compatibilidade com as referências iniciais do projeto.
O protocolo único está em [ralph-loop](../ralph-loop/SKILL.md); não duplicar outro ciclo aqui.

Selecionar a primeira história elegível do [Kanban](../../../docs/jira-pessoal/KANBAN-OFICIAL.md),
confirmar dependências e preservar alterações preexistentes. Uma história ainda não iniciada
não recebe PASS, timestamps de execução ou aprovação por existir no planejamento.
