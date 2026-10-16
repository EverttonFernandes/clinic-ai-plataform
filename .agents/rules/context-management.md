---
name: context-management
description: "Preservar continuidade verificável de histórias entre sessões e compactações."
applies_when:
  - "loop longo, troca de agente/modelo ou retomada"
progressive_disclosure:
  - Ler o checkpoint atual e referências do passo, não todo o histórico.
conditional_details:
  - if: "antes de encerrar ou trocar contexto"
    then: "persistir checkpoint curto e próxima ação executável"
  - else_if: "retomada"
    then: "reconciliar árvore Git, modelos, ownership e validade das provas"
  - else: "iteração normal"
    then: "atualizar progress após decisões ou resultados materiais"
---

# Continuidade do loop

Em `docs/tasks/<ID>/progress.md`, registrar objetivo e escopo autorizado, branch/base/HEAD,
URL do PR quando existir, modelos/IDs reais, etapa, critérios/gates pendentes, receipts e
parecer por referência, correções/incidentes e contadores, decisões, bloqueios e próxima ação.
Não incluir tokens do lock, secrets, PII, logs integrais nem raciocínio interno privado.

Atualizar após Red/Green, correção, revisão, commit/push, resultado de CI e espera pelo usuário.
Antes de compactar, indicar o último resultado observado e o que ainda não foi executado.
Se o contexto ficar insuficiente, persistir handoff em vez de declarar sucesso ou recomeçar.

Retomar lendo AGENTS/índice, história/plano/progress e apenas referências condicionais.
Conferir status/diff/HEAD, ownership (token apenas local), fonte/scope/contrato/parecer e
CI do SHA atual. Memória textual não renova prova expirada. Não repetir writes, commits,
PRs ou chamadas externas sem verificar se a ação anterior já ocorreu.

Aceite humano pendente permanece Review, inclusive após troca de sessão. Novo contexto
não remove dependências, correções, limites de tentativas ou a proibição de merge pelo agente.
