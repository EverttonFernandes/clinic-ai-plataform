# C-004 — Reserva idempotente com proteção de concorrência

Marco: M2. Tipo: negócio.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Como paciente, reservar um horário e receber confirmação fiel ao commit.

## Vínculos e dependências

- Requisitos: `RF-03`, `RNF-02`, `RF-14` — [especificação](../../../spec.md).
- Dependências: [C-003](../historias/C-003-disponibilidade-agenda.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Exigir intenção/parâmetros confirmados e chave com escopo tenant/clínica/ator/operação.
- [ ] Revalidar slot no PostgreSQL e impor integridade para uma reserva ativa.
- [ ] Persistir chave/hash, reserva, resultado e evento na mesma transação.
- [ ] Resultado divergente com mesma chave conflita; resposta perdida é recuperável com a chave original.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Reserva idempotente com proteção de concorrência

  Cenário: Criação confirmada
    Dado que o paciente confirmou um slot livre e uma chave nova
    Quando a criação é executada
    Então uma reserva e seu evento são persistidos e só então o sucesso é devolvido

  Cenário: Resposta perdida
    Dado que a reserva foi comitada e a resposta não chegou
    Quando o cliente repete mesma chave e payload
    Então recebe o resultado anterior sem uma segunda reserva ou evento de criação

  Cenário: Disputa de slot
    Dado que 100 intenções autorizadas usam chaves diferentes para o mesmo slot livre
    Quando as chamadas HTTP disputam simultaneamente
    Então uma cria reserva e 99 recebem SLOT_ALREADY_TAKEN sem duplicação
```

## Validação e conclusão

Funcionais e concorrência com PostgreSQL real; barreira de início, contagem independente de reservas/idempotência/eventos.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
