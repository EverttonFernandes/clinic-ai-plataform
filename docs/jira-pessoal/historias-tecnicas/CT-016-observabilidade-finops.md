# CT-016 — Observabilidade e FinOps de ponta a ponta

Marco: M5. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Explicar cada atendimento, seu custo e suas falhas sem registrar dados sensíveis em excesso.

## Vínculos e dependências

- Requisitos: `RNF-07`, `RNF-03`, `RNF-08` — [especificação](../../../spec.md).
- Dependências: [CT-015](../historias-tecnicas/CT-015-evals-offline.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Propagar correlationId/traces de edge a agent/tools/serviços/dados/providers.
- [ ] Métricas de latência/erros/throughput/cache hit, passos/chamadas/chunks-scores/retries-fallback/evals.
- [ ] Usage por tenant/ator/feature/agent, custo estimado/confirmado e alertas/bloqueios.
- [ ] Logs minimizados; IDs em traces controlados, não labels de alta cardinalidade; sem texto clínico/prompts completos por padrão.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Observabilidade e FinOps de ponta a ponta

  Cenário: Atendimento rastreável
    Dado que uma FAQ percorre cache miss, RAG e geração
    Quando o trace é consultado
    Então mostra etapas, versões, uso e falha quando houver sem conteúdo pessoal desnecessário

  Cenário: Alerta de consumo
    Dado que um tenant aproxima-se do limite configurado
    Quando novas operações consomem o budget
    Então o alerta é emitido e o bloqueio ocorre no teto determinístico

  Cenário: Minimização
    Dado que uma requisição contém informação pessoal sintética marcada
    Quando logs e métricas são coletados
    Então a marca não aparece em payloads indiscriminados ou labels
```

## Validação e conclusão

Integração e inspeção sanitizada de traces/métricas/logs, sem exigir plataforma SaaS adicional.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
