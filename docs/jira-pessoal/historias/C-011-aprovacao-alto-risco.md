# C-011 — Aprovação humana para ação de alto risco definida

Marco: Opcional. Tipo: negócio; opcional, fora do MVP obrigatório.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Como operador autorizado, aprovar uma ação de alto impacto que realmente justifique HITL.

## Vínculos e dependências

- Requisitos: `RF-15`, `RNF-08` — [especificação](../../../spec.md).
- Dependências: [CT-026](../historias-tecnicas/CT-026-aceite-seis-fluxos.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Resolver D-06 antes de implementar: escolher ação dentro do escopo autorizado e sua finalidade.
- [ ] Vincular aprovação a tenant/clínica, ator/aprovador, payload/hash, prazo e uso único.
- [ ] Executar após revalidar permissões e condições; alteração do payload invalida a aprovação.
- [ ] Não exigir HITL em agendamento comum nem adicionar prescrição/ação clínica por esta história.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Aprovação humana para ação de alto risco definida

  Cenário: Aprovação válida
    Dado que a ação de alto risco foi definida e a aprovação está válida
    Quando a execução revalida contexto e payload
    Então produz um único efeito autorizado e auditável

  Cenário: Payload alterado
    Dado que a ação foi aprovada com parâmetros anteriores
    Quando a execução recebe parâmetros diferentes
    Então a aprovação não é reutilizada e nenhum efeito é executado

  Cenário: Agendamento comum
    Dado que o paciente confirma uma reserva administrativa comum
    Quando o fluxo de agenda é executado
    Então segue as regras existentes sem aprovação interna obrigatória
```

## Validação e conclusão

Funcionais de aprovação expirada/reuso/payload e regressão do agendamento comum; fora da linha obrigatória do MVP.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
