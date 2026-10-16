# C-002 — Catálogo de especialidades e profissionais

Marco: M2. Tipo: negócio.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Como paciente, encontrar profissionais da clínica por critérios verificáveis.

## Vínculos e dependências

- Requisitos: `RF-02`, `RNF-01` — [especificação](../../../spec.md).
- Dependências: [C-001](../historias/C-001-dados-paciente.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Consultar especialidade e profissionais ativos com paginação e limites de filtros.
- [ ] Aplicar tenant/clínica e vínculo autorizado no serviço.
- [ ] Responder vazio de forma explícita quando não houver correspondência.
- [ ] Recomendação é administrativa; não produzir diagnóstico ou inventar especialidade/profissional.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Catálogo de especialidades e profissionais

  Cenário: Busca por especialidade
    Dado que a clínica possui dermatologistas ativos e um cadastro inativo
    Quando o paciente filtra dermatologia
    Então recebe somente profissionais ativos elegíveis da clínica

  Cenário: Catálogo de outra clínica
    Dado que há profissionais semanticamente semelhantes em outro tenant
    Quando a consulta é executada
    Então nenhum profissional externo ao escopo aparece

  Cenário: Sem resultado
    Dado que nenhum profissional atende aos filtros autorizados
    Quando o catálogo é consultado
    Então retorna lista vazia sem profissional inventado
```

## Validação e conclusão

Funcionais HTTP de filtro/paginação/isolamento com catálogo real sintético.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
