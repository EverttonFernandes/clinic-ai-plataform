# CT-025 — CI completa, release e CD controlado

Marco: M6. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Promover o mesmo artefato validado com deploy e rollback controlados.

## Vínculos e dependências

- Requisitos: `RNF-13`, `RNF-12` — [especificação](../../../spec.md).
- Dependências: [CT-024](../historias-tecnicas/CT-024-prontidao-ambiente-real.md), [CT-023](../historias-tecnicas/CT-023-indices-vetoriais.md), [CT-018](../historias-tecnicas/CT-018-provider-real.md), [CT-019](../historias-tecnicas/CT-019-whatsapp-outbound.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Expandir CI desde CT-003: análise, unit/integration/functional/security/concurrency, evals offline e migrations.
- [ ] Imagem imutável sem secrets, inventário/scan de dependências com política de severidade e artifact por SHA/digest.
- [ ] CD em GitHub Actions usa ambientes/configuração verificada, credenciais restritas e ação manual/proteção disponível.
- [ ] Smoke pós-deploy, rollback compatível com migrations e nenhum deploy de PR/fork; não remover volumes.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: CI completa, release e CD controlado

  Cenário: Gate falha
    Dado que um requisito funcional ou scan bloqueante reprova
    Quando o fluxo de release é iniciado
    Então nenhum deploy é executado

  Cenário: Promoção de artefato
    Dado que uma imagem por digest passou na homologação
    Quando a promoção autorizada é iniciada
    Então o mesmo digest é usado sem rebuild divergente

  Cenário: Smoke de deploy falha
    Dado que a versão nova foi aplicada e a readiness/jornada crítica falha
    Quando o procedimento de recuperação é executado
    Então o runtime anterior compatível é restaurado e os dados permanecem íntegros
```

## Validação e conclusão

Run real de CI/CD autorizado, digest, relatórios e ensaio de rollback; sem destino/secrets, deploy continua PENDING.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
