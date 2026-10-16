# CT-008 — Budget cumulativo e ledger de consumo

Marco: M3. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Garantir orçamento determinístico antes de habilitar providers ou loops de agente.

## Vínculos e dependências

- Requisitos: `RNF-03`, `RNF-04`, `RF-07` — [especificação](../../../spec.md).
- Dependências: [CT-007](../historias-tecnicas/CT-007-outbox-auditoria-notificacoes.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Implementar os oito limites do runtime e reserva atômica de custo/quota/concurrency antes de chamadas caras.
- [ ] Incluir embeddings, retries/fallbacks e ferramentas caras no total; ledger financeiro recuperável no PostgreSQL.
- [ ] Expirar sessão não renova quota; timeout com cobrança incerta não libera budget indevidamente.
- [ ] Perda de Redis bloqueia e exige recuperação confiável dos controles antes da reabertura; testes com múltiplas instâncias.
- [ ] Retomada/reinício da execução não zera tetos nem consumo; expirar/remover state ou cache não remove ledger, reserva incerta ou quota vigente, conforme RF-07.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Budget cumulativo e ledger de consumo

  Cenário: Último saldo disputado
    Dado que duas instâncias disputam um orçamento que só cobre uma chamada
    Quando reservam consumo simultaneamente
    Então somente uma obtém autorização antes de alcançar o provider

  Cenário: Retry e fallback
    Dado que uma tarefa já consumiu parte de maxCost/maxLLMCalls
    Quando o caminho solicita nova tentativa e alternativa
    Então todas consomem o orçamento original e o excedente é bloqueado

  Cenário: Custo desconhecido
    Dado que uma chamada possivelmente cobrada termina em timeout e o lease expira
    Quando outra chamada é solicitada
    Então o saldo incerto permanece reservado até reconciliação, sem crédito artificial

  Cenário: State perdido com consumo em aberto
    Dado que uma execução possui uso confirmado e uma chamada de custo incerto
    Quando sua sessão expira e a aplicação reinicia
    Então a próxima execução respeita a quota vigente e a reserva incerta sem receber saldo adicional
```

## Validação e conclusão

Integração Redis/PostgreSQL, provider espião sem rede externa e corridas de reservas; exercitar os oito tetos.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
