# CT-021 — Falhas, carga, concorrência e restauração

Marco: M6. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Medir comportamento sob disputa e falhas antes de aumentar instâncias ou publicar.

## Vínculos e dependências

- Requisitos: `RNF-02`, `RNF-03`, `RNF-06`, `RNF-10` — [especificação](../../../spec.md).
- Dependências: [CT-020](../historias-tecnicas/CT-020-seguranca-privacidade.md), [CT-014](../historias-tecnicas/CT-014-cache-respostas.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Executar cenários de indisponibilidade de PostgreSQL/Redis/provider e falha entre commit/publicação.
- [ ] Repetir 100 concorrentes por slot e corridas de reagendamento/idempotência/budget.
- [ ] Medir p95/throughput/erros/filas/uso em carga sintética declarada; registrar baseline sem inventar SLA.
- [ ] Backup/restore PostgreSQL e documentos em ambiente descartável; recuperar registros/limites e medir RPO/RTO.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Falhas, carga, concorrência e restauração

  Cenário: Redis perdido
    Dado que existem chamadas/reservas de consumo ainda em aberto
    Quando Redis é reiniciado sem seus dados
    Então novas operações caras permanecem bloqueadas até reconstruir limites confiáveis

  Cenário: Restauração
    Dado que um backup sintético consistente está disponível
    Quando é restaurado em projeto Compose isolado
    Então reservas/documentos/resultados idempotentes são verificáveis e nenhum ambiente de desenvolvimento é apagado

  Cenário: Sobrecarga
    Dado que a taxa de pedidos supera capacidade medida
    Quando a carga sintética é aplicada
    Então backpressure/limites preservam integridade e o relatório informa p95, erros e consumo
```

## Validação e conclusão

Ferramenta de carga escolhida na execução, testes concorrentes e falhas reais em contêineres descartáveis; números medidos.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
