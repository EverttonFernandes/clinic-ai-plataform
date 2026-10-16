# CT-028 — Avaliação de consolidação analítica no Databricks

Marco: evolução opcional após M6. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Demonstrar uma projeção analítica reconciliável da plataforma em Databricks, com dados
sintéticos, governança, qualidade e custo medidos, sem dependência do atendimento.

## Vínculos e dependências

- Dependência: [CT-026](CT-026-aceite-seis-fluxos.md), com sua base integrada; independe de LiteLLM.
- Condição de entrada: promoção explícita do backlog, D-08 resolvida, workspace e custo autorizado.
- Requisitos: `RNF-01`, `RNF-07`, `RNF-08`, `RNF-14` — [spec](../../../spec.md).
- Referências: [mapa DDD e fluxo analítico](../../spec-driven-development/arquitetura-ddd.md), [decisões](../../spec-driven-development/decisoes.md).

## Escopo e critérios de aceite

- [ ] Definir perguntas de ocupação/cancelamento e custo/qualidade por tenant/janela, dataset sintético, esquema versionado, política de acesso/retenção/exclusão e teto de custo; verificar recursos disponíveis de governança no workspace escolhido.
- [ ] Exportar dados selecionados por batch incremental recuperável, com IDs, versão, tenant/clínica e checkpoints após persistência confirmada; eventos/outbox não recebem consumidores que bloqueiem transações de agenda.
- [ ] Implementar Bronze/Silver/Gold com dedupe, tipos, validação, dados inválidos identificados, correções tardias e remoções; leitura por tenant impede exposição cruzada em todas as camadas.
- [ ] Reconciliar indicadores com a origem; replay e restart não perdem nem duplicam resultados, nem ressuscitam dados excluídos. Registrar frescor, volume e custo do experimento.
- [ ] Executar job real no Databricks e consulta de indicadores com evidências sanitizadas e roteiro; exportação/fixture somente local não satisfaz o gate externo. Queda do lakehouse não impede reserva nem atendimento.

## Cenários BDD de aceitação

```gherkin
Funcionalidade: Projeção analítica governada

  Cenário: Indicadores reconciliados
    Dado que dois tenants têm reservas e consumo sintéticos com resultados conhecidos
    Quando o job real processa Bronze, Silver e Gold
    Então os indicadores coincidem com a origem e o consumidor de um tenant não lê o outro

  Cenário: Replay após interrupção
    Dado que a exportação é interrompida após persistir um lote e antes de avançar o checkpoint
    Quando o lote é reenviado e o pipeline reexecutado
    Então os indicadores permanecem corretos sem perda nem duplicação

  Cenário: Exclusão seguida de reprocessamento
    Dado que um registro foi removido pela política de retenção ou exclusão
    Quando uma janela antiga é reprocessada
    Então a remoção continua respeitada em todas as camadas e projeções

  Cenário: Lakehouse indisponível
    Dado que a plataforma operacional está saudável e o destino analítico está indisponível
    Quando uma reserva é confirmada
    Então o commit permanece correto e a exportação aguarda recuperação sem bloquear atendimento
```

## Validação e conclusão

Prova externa do job, consultas/reconciliação, replay, isolamento, exclusão e indisponibilidade,
com dados sintéticos e custo registrado. Sem workspace/autorização, o gate permanece PENDING.
Usar [tarefa](../../tasks/TEMPLATE.md), [entrega](../../entregas/TEMPLATE.md) e DoD do Kanban.
Provisionamento, consumo pago e dados reais exigem autorização aplicável ao escopo concreto.
