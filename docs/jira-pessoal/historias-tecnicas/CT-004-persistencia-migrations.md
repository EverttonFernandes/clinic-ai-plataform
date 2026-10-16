# CT-004 — Persistência multi-tenant e migrations

Marco: M2. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Criar o estado durável necessário às APIs, idempotência, eventos e jobs.

## Vínculos e dependências

- Requisitos: `RNF-01`, `RNF-02`, `RF-14`, `RNF-14` — [especificação](../../../spec.md).
- Dependências: [CT-003](../historias-tecnicas/CT-003-ci-inicial.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Modelar tenant/clínica/ator/paciente/profissional/slot e vínculos com integridade referencial de escopo.
- [ ] Planejar registros de appointment/idempotência/outbox/inbox/jobs/consumo sem tabelas para funcionalidades clínicas fora do MVP.
- [ ] Migrations reproduzíveis em banco vazio e evolução compatível, com índices de filtros de escopo.
- [ ] Fixtures sintéticas de dois tenants; nenhuma alteração silenciosa do schema ao iniciar requests.
- [ ] Identificar dono de tabelas/migrations por contexto e contrato de unidade de trabalho; modelos ORM e adapters ficam na infraestrutura. Migrations de funcionalidades futuras são planejadas, não criadas antecipadamente.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Persistência multi-tenant e migrations

  Cenário: Banco vazio
    Dado que o PostgreSQL de teste está vazio
    Quando as migrations são aplicadas
    Então o schema e constraints ficam disponíveis e a versão é registrada

  Cenário: Vínculo cruzado
    Dado que paciente e profissional pertencem a tenants diferentes
    Quando uma persistência tenta associá-los
    Então a operação é rejeitada sem registro inconsistente

  Cenário: Evolução de schema
    Dado que o banco contém a revisão anterior com dados sintéticos
    Quando a migration seguinte é aplicada
    Então os dados válidos permanecem e a revisão é reconhecida
```

## Validação e conclusão

Integração em PostgreSQL real: migrations do zero/upgrade, constraints e inexistência de registros cruzados.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
