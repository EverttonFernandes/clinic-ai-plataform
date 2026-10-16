# CT-012 — Ingestão assíncrona e versões completas

Marco: M4. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Transformar documentos aprovados em jobs recuperáveis sem publicar índice parcial.

## Vínculos e dependências

- Requisitos: `RF-10`, `RNF-05`, `RNF-06` — [especificação](../../../spec.md).
- Dependências: [CT-011](../historias-tecnicas/CT-011-upload-quarentena.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Job durável por tenant/clínica/documento/versão; transições PENDING/PROCESSING/INDEXED/FAILED.
- [ ] Chunking rastreável, checkpoints, limites de custo/chunks e budget antes de embeddings.
- [ ] Upserts idempotentes, retries limitados, DLQ e reconciliação de objeto salvo/job não publicado.
- [ ] Ativação completa condicionada à versão vigente; worker obsoleto não reativa documento revogado.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Ingestão assíncrona e versões completas

  Cenário: Falha parcial
    Dado que apenas parte dos chunks da versão nova foi persistida
    Quando o worker é interrompido
    Então a consulta mantém a versão anterior e não enxerga a parcial

  Cenário: Retomada
    Dado que um job parcialmente processado volta à fila
    Quando outro worker o retoma
    Então conclui sem chunks duplicados nem cobrança duplicada de etapas já confirmadas

  Cenário: Versão obsoleta
    Dado que um job antigo termina depois de uma revisão nova ou revogação
    Quando tenta ativar sua versão
    Então a ativação é rejeitada e não ressuscita conteúdo desautorizado
```

## Validação e conclusão

Integração em PostgreSQL/storage com falhas por etapa, redelivery e corrida entre versões; embeddings controlados.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
