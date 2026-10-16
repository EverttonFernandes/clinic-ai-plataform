# C-006 — Reagendamento atômico

Marco: M2. Tipo: negócio.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Como paciente, alterar o horário sem perder minha consulta em caso de conflito.

## Vínculos e dependências

- Requisitos: `RF-05`, `RNF-02`, `RF-14` — [especificação](../../../spec.md).
- Dependências: [C-005](../historias/C-005-cancelar-reserva.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Validar autorização e versão/estado atual da reserva antes de alterar.
- [ ] Reservar novo slot e liberar antigo na mesma transação, protegendo corridas com cancelamento.
- [ ] Aplicar idempotência de alteração com hash do payload e evento durável.
- [ ] Conflito ou falha intermediária faz rollback completo, preservando o horário anterior.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Reagendamento atômico

  Cenário: Troca de horário
    Dado que a reserva atual e o novo slot são elegíveis
    Quando o paciente confirma reagendamento
    Então a nova ocupação e a liberação antiga são comitadas juntas

  Cenário: Novo horário ocupado
    Dado que outro paciente já ocupa o destino
    Quando o reagendamento é solicitado
    Então retorna conflito e a reserva anterior continua intacta

  Cenário: Falha intermediária
    Dado que a transação começou a alterar os slots
    Quando uma falha é injetada antes do commit
    Então nenhuma alteração parcial ou evento de sucesso permanece
```

## Validação e conclusão

Integração transacional e funcionais concorrentes de cancelamento/reagendamento; verificar ambos os slots.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
