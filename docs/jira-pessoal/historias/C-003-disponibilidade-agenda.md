# C-003 — Consulta de horários disponíveis

Marco: M2. Tipo: negócio.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Como paciente, consultar horários reais sem criar uma reserva.

## Vínculos e dependências

- Requisitos: `RF-02`, `RNF-02` — [especificação](../../../spec.md).
- Dependências: [C-002](../historias/C-002-catalogo-profissionais.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Definir slots fixos exclusivos e timezone IANA da clínica com persistência UTC.
- [ ] Consulta limitada por profissional/período e escopo; sem cache inicialmente.
- [ ] Horário passado, profissional inválido ou recurso de outro tenant não é oferecido.
- [ ] Resposta informa disponibilidade momentânea, sem efeito persistente de reserva.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Consulta de horários disponíveis

  Cenário: Horários livres
    Dado que há slots livres e um já reservado
    Quando a agenda do profissional é consultada
    Então somente horários elegíveis aparecem e nenhuma reserva é criada

  Cenário: Timezone da clínica
    Dado que um slot está persistido em UTC e a clínica tem timezone definido
    Quando a disponibilidade é apresentada
    Então o horário corresponde ao fuso da clínica sem ambiguidade

  Cenário: Período inválido
    Dado que o pedido informa intervalo invertido ou acima do limite
    Quando a API é chamada
    Então rejeita a consulta sem busca ilimitada
```

## Validação e conclusão

Funcionais por HTTP e consulta independente ao PostgreSQL; casos de fuso e ausência de efeitos.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
