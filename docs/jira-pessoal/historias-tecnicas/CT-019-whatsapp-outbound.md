# CT-019 — Worker de canal e outbound recuperável

Marco: M5. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Processar eventos WhatsApp e enviar respostas recuperáveis sem duplicar efeitos locais.

## Vínculos e dependências

- Requisitos: `RF-12`, `RF-14`, `RNF-06` — [especificação](../../../spec.md).
- Dependências: [C-010](../historias/C-010-whatsapp-inbox.md), [CT-007](../historias-tecnicas/CT-007-outbox-auditoria-notificacoes.md), [C-007](../historias/C-007-conversa-sessao.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Consumir inbox por conversa com ordem/posse/lease e runtime compartilhado ao Web.
- [ ] Outbox de resposta com identificador estável, retries, DLQ e estado de entrega.
- [ ] Contrato de idempotência/query do destino; envio ambíguo fica reconciliável, sem promessa de exactly-once.
- [ ] Validar adapter em sandbox real após D-02; ausência de acesso mantém gate externo pendente.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Worker de canal e outbound recuperável

  Cenário: Reinício do worker
    Dado que um evento recebido ainda não foi processado
    Quando o worker reinicia
    Então retoma o atendimento sem perder o evento ou duplicar reserva

  Cenário: Resposta perdida no destino
    Dado que o provider pode ter aceitado o envio mas a confirmação se perdeu
    Quando o worker trata o timeout
    Então consulta/reconcilia conforme capacidade do destino e registra a incerteza sem retry cego

  Cenário: Jornada no sandbox
    Dado que o sandbox e identidade de teste estão autorizados
    Quando o paciente consulta e confirma pelo WhatsApp
    Então a mensagem externa e a reserva persistida são correlacionáveis
```

## Validação e conclusão

Integração local com destino controlado e teste separado de sandbox real; relatório distingue os dois.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
