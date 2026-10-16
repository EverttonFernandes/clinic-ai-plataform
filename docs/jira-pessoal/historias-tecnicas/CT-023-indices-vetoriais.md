# CT-023 — Avaliação de índices vetoriais e metadados

Marco: M6. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Escolher índices por qualidade e latência medidas com filtros reais.

## Vínculos e dependências

- Requisitos: `RF-10`, `RNF-09`, `RNF-10` — [especificação](../../../spec.md).
- Dependências: [CT-022](../historias-tecnicas/CT-022-escala-horizontal.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Comparar baseline exato com HNSW e/ou IVFFlat em dataset representativo sintético.
- [ ] Medir recall/relevância/latência com filtros tenant/clínica/visibility/paciente e índices tradicionais.
- [ ] Documentar custo de memória/build/update e estratégia de reindexação/modelo compatível.
- [ ] Adotar somente opção justificada; nenhuma otimização pode relaxar autorização ou versões completas.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Avaliação de índices vetoriais e metadados

  Cenário: Filtros seletivos
    Dado que o corpus contém vários tenants e poucos documentos elegíveis
    Quando a busca é comparada com diferentes índices
    Então nenhum resultado fora de escopo é retornado e qualidade/latência são relatadas

  Cenário: Índice sem ganho
    Dado que o ANN não melhora o baseline no volume medido
    Quando a decisão técnica é registrada
    Então mantém a solução mais simples com evidência da comparação

  Cenário: Troca de embedding
    Dado que a configuração muda espaço/modelo vetorial
    Quando o índice novo é preparado
    Então não mistura vetores incompatíveis nem publica revisão incompleta
```

## Validação e conclusão

Benchmark repetível em pgvector real, planos/medidas e dataset/versionamento; sem critério fictício de performance.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
