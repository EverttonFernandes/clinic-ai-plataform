# CT-018 — Integração controlada com provider real

Marco: M5. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Validar o fluxo com LLM/embeddings reais, separando qualidade real de roteiro de teste.

## Vínculos e dependências

- Requisitos: `RF-13`, `RNF-03`, `RNF-09` — [especificação](../../../spec.md).
- Dependências: [CT-017](../historias-tecnicas/CT-017-contratos-resiliencia.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Resolver D-01: provider/modelo/embedding, credenciais fora do Git, preço de referência e teto autorizado.
- [ ] Adapter respeita limites de tokens/custo/deadline, registra usage e reconcilia chamadas incertas.
- [ ] Rodar dataset relevante com provider real e comparação de qualidade/latência/custo; fallback só habilitado se avaliado.
- [ ] CI padrão continua sem custo; sem autorização/credenciais, prova externa é PENDING e a história não é Done.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Integração controlada com provider real

  Cenário: Execução real limitada
    Dado que há autorização de custo, credenciais e modelos registrados
    Quando o conjunto mínimo é executado
    Então produz respostas e embeddings reais com usage, versões e custo dentro do teto

  Cenário: Saldo insuficiente
    Dado que o saldo não cobre a próxima chamada real
    Quando uma tarefa a solicita
    Então o backend bloqueia antes de enviar ao provider

  Cenário: Fallback não avaliado
    Dado que um modelo alternativo está configurado mas não aprovado por evals
    Quando o primário falha
    Então a alternativa não é habilitada silenciosamente e a resposta degrada explicitamente
```

## Validação e conclusão

Contrato + evals reais sanitizadas, versões e custo; ausência de credenciais não pode virar PASS por uso de fake.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
