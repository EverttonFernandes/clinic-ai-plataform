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
- [ ] Registrar antes das chamadas baseline/candidato, casos de aceitação, amostra/repetições críticas, parâmetros e limiares por dimensão conforme [protocolo](../../spec-driven-development/testes.md#protocolo-mínimo-de-avaliação-do-produto). Relatar sucessos/total, variação, falhas, cobertura e custo sem rerun até passar ou promessa estatística com amostra pequena.
- [ ] Provar separadamente relevância de embeddings/retrieval reais, geração com contexto autorizado fixo e jornada completa, incluindo múltiplos turnos, esclarecimento e ação confirmada. Efeitos/isolamento continuam verificados deterministicamente; judge calibrado não substitui banco ou autorização.

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

  Cenário: Candidato varia entre execuções
    Dado que casos e repetições foram definidos dentro de um teto autorizado antes da execução
    Quando o modelo candidato apresenta resultados diferentes nas tentativas
    Então todas as tentativas e falhas entram na comparação com a baseline e uma falha crítica impede aprovação mesmo com média alta

  Cenário: Avaliação interrompida pelo orçamento
    Dado que o teto restante não cobre as repetições planejadas
    Quando a próxima chamada seria executada
    Então ela é bloqueada e o relatório indica a cobertura incompleta sem aprovar o modelo ou renovar saldo
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
