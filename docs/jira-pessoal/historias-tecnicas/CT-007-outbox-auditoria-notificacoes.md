# CT-007 — Entrega recuperável de eventos e notificações

Marco: M2. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Processar eventos após commit sem perder auditoria ou duplicar efeitos locais.

## Vínculos e dependências

- Requisitos: `RF-14`, `RNF-06`, `RNF-08` — [especificação](../../../spec.md).
- Dependências: [C-006](../historias/C-006-reagendar-reserva.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Worker consome outbox durável PostgreSQL com posse/lease e idempotência por evento/destino.
- [ ] Auditoria inclui actor/tenant/paciente-recurso/ação/resultado/timestamp/correlationId.
- [ ] Falha entre commit e publicação é reconciliada; retries com backoff/jitter e DLQ.
- [ ] Notificações locais usam destino controlado; entrega externa real tem contrato de reconciliação de resultado incerto.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Entrega recuperável de eventos e notificações

  Cenário: Falha após commit
    Dado que uma reserva e seu evento estão comitados e o worker caiu
    Quando o worker reinicia
    Então o evento pendente é entregue e a reserva não é criada novamente

  Cenário: Entrega duplicada
    Dado que o mesmo evento é recebido por dois consumidores
    Quando a projeção auditável é atualizada
    Então o identificador estável produz um único efeito local

  Cenário: Destino persistente em falha
    Dado que um destino falha até o limite de tentativas
    Quando o worker processa os retries
    Então o job chega à DLQ e pode ser reprocessado sem alterar a reserva
```

## Validação e conclusão

Integração em PostgreSQL real com restart, redelivery e contagem independente de auditoria/jobs.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
