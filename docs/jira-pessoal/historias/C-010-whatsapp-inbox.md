# C-010 — Entrada WhatsApp confiável e inbox durável

Marco: M5. Tipo: negócio.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Como paciente, iniciar atendimento por um canal com origem e identidade verificadas.

## Vínculos e dependências

- Requisitos: `RF-12`, `RF-01`, `RF-07`, `RNF-01`, `RNF-06` — [especificação](../../../spec.md).
- Dependências: [CT-017](../historias-tecnicas/CT-017-contratos-resiliencia.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Definir adapter do provider sem acoplar domínio à API específica; resolver D-02 para a validação externa.
- [ ] Validar assinatura/origem, mapear tenant/usuário e evitar confiar no número informado livremente no payload.
- [ ] Persistir evento + dedupe/inbox atomicamente antes do ACK rápido; encaminhar processamento pesado ao worker.
- [ ] Duplicatas e eventos fora de ordem não alteram contexto alheio nem criam novas intenções de escrita.
- [ ] Correlacionar ator/sessão somente após validação do canal; mensagem tardia ou replay da inbox não ressuscita state expirado nem restaura confirmação antiga, conforme RF-07.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Entrada WhatsApp confiável e inbox durável

  Cenário: Webhook válido
    Dado que um evento tem assinatura válida e mapeamento confiável
    Quando o webhook recebe o evento
    Então persiste inbox/dedupe e responde ACK antes do processamento pesado

  Cenário: Evento duplicado
    Dado que o mesmo evento do provider já está persistido
    Quando o provider o reenvia
    Então o recebimento não agenda outro atendimento ou reserva

  Cenário: Persistência falha
    Dado que não é possível salvar inbox/dedupe duráveis
    Quando o webhook recebe um evento válido
    Então não confirma recebimento como persistido e não executa efeito de negócio

  Cenário: Mensagem atrasada após expiração da conversa
    Dado que uma mensagem de confirmação chega depois de expirar o state que continha a intenção
    Quando o worker processa o evento autenticado da inbox
    Então ele informa ausência de contexto sem recriar a confirmação ou duplicar ação já persistida
```

## Validação e conclusão

Funcionais HTTP com assinatura de teste e PostgreSQL real; isso não comprova webhook externo até teste do sandbox.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
