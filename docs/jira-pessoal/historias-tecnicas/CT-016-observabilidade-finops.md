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
- [ ] Correlação básica nasce com os fluxos anteriores; esta história consolida a inspeção. Registrar D-18 avaliando OpenTelemetry/Langfuse por custo, recursos, acesso, retenção e mascaramento na origem. Não exigir SaaS, cluster ou stack de observabilidade adicional para o laboratório.
- [ ] Correlacionar jobs e tentativas assíncronas; exportação falha sem impedir a jornada autorizada nem suspender budget/auditoria duráveis. Buffers/retries de telemetria têm limites; indisponibilidade fica identificável localmente.
- [ ] Métricas de latência/erros/throughput/cache hit, passos/chamadas/chunks-scores/retries-fallback/evals.
- [ ] Usage por tenant/ator/feature/agent, custo estimado/confirmado e alertas/bloqueios.
- [ ] Logs minimizados; IDs em traces controlados, não labels de alta cardinalidade; sem texto clínico/prompts completos por padrão.
- [ ] Definir limiares e responsáveis de D-16 para chamadas repetitivas, rejeições, retries, crescimento/idade da fila e consumo anômalo por tenant; alerta não substitui bloqueio determinístico e não expõe conteúdo privado.

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

  Cenário: Observabilidade externa indisponível
    Dado que o exportador de telemetria está indisponível e os controles oficiais estão saudáveis
    Quando uma jornada autorizada e um job são executados
    Então a jornada mantém orçamento e auditoria oficiais, a falha de exportação é identificável localmente e não há retry ou buffer ilimitado

  Cenário: Minimização
    Dado que uma requisição contém informação pessoal sintética marcada
    Quando logs e métricas são coletados
    Então a marca não aparece em payloads indiscriminados ou labels

  Cenário: Script repetitivo
    Dado que um script autenticado tenta consumir chamadas além da janela e dos tetos definidos
    Quando os limites são atingidos
    Então novas operações caras são bloqueadas antes do provider e os indicadores/alertas identificam o abuso sem conteúdo pessoal
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
