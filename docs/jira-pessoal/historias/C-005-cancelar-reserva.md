# C-005 — Cancelamento autorizado e idempotente

Marco: M2. Tipo: negócio.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Como paciente, cancelar minha consulta sem repetir efeitos.

## Vínculos e dependências

- Requisitos: `RF-04`, `RNF-02`, `RF-14` — [especificação](../../../spec.md).
- Dependências: [C-004](../historias/C-004-criar-reserva.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Cancelar somente reserva autorizada e em estado permitido pelo domínio.
- [ ] Registrar cancelamento/resultado/evento atomicamente com idempotencyKey.
- [ ] Repetição da mesma intenção não produz novos efeitos; payload divergente conflita.
- [ ] Liberar capacidade para nova reserva; não expor recurso de outro paciente.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Cancelamento autorizado e idempotente

  Cenário: Cancelamento válido
    Dado que a paciente possui uma reserva ativa
    Quando confirma cancelamento com chave nova
    Então a reserva muda de estado e o slot volta à disponibilidade

  Cenário: Cancelamento repetido
    Dado que o cancelamento já foi comitado
    Quando a mesma chave e payload são reenviados
    Então o resultado é recuperado sem novo evento de cancelamento

  Cenário: Reserva alheia
    Dado que o ator conhece uma consulta de outra pessoa
    Quando tenta cancelá-la
    Então a operação é negada e a reserva original permanece ativa
```

## Validação e conclusão

Funcionais HTTP, integridade de estado/eventos e reuso do slot no PostgreSQL.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
