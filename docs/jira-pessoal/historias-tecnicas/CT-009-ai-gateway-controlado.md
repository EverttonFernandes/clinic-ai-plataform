# CT-009 — AI Gateway e provider determinístico

Marco: M3. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Exercitar model routing e resiliência sem consumir APIs reais.

## Vínculos e dependências

- Requisitos: `RF-13`, `RNF-04`, `RNF-06`, `RNF-14` — [especificação](../../../spec.md).
- Dependências: [CT-008](../historias-tecnicas/CT-008-budget-runtime.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Definir adapter de provider e rotas simple-extraction/general-chat/summarization/complex-reasoning/document-analysis.
- [ ] Centralizar credentials/config, timeout, backoff/jitter, circuit breaker, retry e accounting.
- [ ] Provider controlado devolve respostas/tool calls, uso, erros e demora por roteiro versionado.
- [ ] Fallback controlado consome o mesmo deadline/budget; execução real só em CT-018 após evals.
- [ ] Portas próprias de geração/embedding isolam agentes/aplicação dos SDKs; registrar dono de retry/fallback e permitir adapter futuro LiteLLM sem mudar domínio nem autorização. Implementar o proxy pertence à CT-027 opcional.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: AI Gateway e provider determinístico

  Cenário: Rota permitida
    Dado que o agente solicita uma rota lógica configurada
    Quando a chamada chega ao gateway
    Então o adapter correto recebe contexto mínimo e contabiliza o uso

  Cenário: Provider indisponível
    Dado que o provider controlado falha e existe alternativa avaliada para o teste
    Quando o gateway executa fallback
    Então a alternativa usa o saldo/deadline restante sem repetir writes

  Cenário: Amplificação de retries
    Dado que o SDK e o runtime têm possibilidade de repetir
    Quando a dependência falha
    Então a política central limita o número total efetivo de tentativas
```

## Validação e conclusão

Contratos com provider controlado em processo/container próprio quando funcional; relógio controlado e contagem real das tentativas.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
