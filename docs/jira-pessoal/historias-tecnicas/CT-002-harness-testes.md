# CT-002 — Harness de testes isolados e evidências

Marco: M1. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Executar testes reproduzíveis por HTTP e por camada sem contaminar o ambiente de desenvolvimento.

## Vínculos e dependências

- Requisitos: `RNF-11`, `RNF-12`, `RNF-14` — [especificação](../../../spec.md).
- Dependências: [CT-001](../historias-tecnicas/CT-001-ambiente-docker.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Separar pytest unit/integration/functional/security/concurrency/evals por marcadores e finalidade.
- [ ] Usar projeto Compose e banco/Redis/storage de teste próprios, fixtures de dois tenants e relógio controlável.
- [ ] Cliente funcional acessa API em processo/container separado; integração usa PostgreSQL/Redis reais.
- [ ] Comandos retornam falha em erro ou zero testes esperados; cleanup atua só em recursos identificados como teste.
- [ ] Incorporar as suítes implementadas ao Application CI existente, com falha real bloqueando sucesso e execução no HEAD da história.
- [ ] Verificar imports das camadas/módulos existentes conforme o [mapa DDD](../../spec-driven-development/arquitetura-ddd.md); comprovar falha com violação controlada, sem exigir domínios fictícios no produto.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Harness de testes isolados e evidências

  Cenário: Isolamento de dados
    Dado que o ambiente de desenvolvimento contém um registro sentinela
    Quando uma suíte cria e limpa dados no ambiente de teste
    Então a sentinela e os volumes de desenvolvimento permanecem intactos

  Cenário: Teste funcional real
    Dado que a API está ativa em outro processo
    Quando um cliente HTTP consulta a readiness
    Então a resposta vem da API e a falha do processo é observável pelo teste

  Cenário: Falha verificável
    Dado que uma expectativa funcional é deliberadamente violada
    Quando a suíte correspondente é executada
    Então o comando termina com código de erro e relatório que identifica a assertion

  Cenário: Fronteira arquitetural violada
    Dado que o verificador recebe uma fixture com domínio importando infraestrutura
    Quando a regra de dependências é verificada
    Então a violação é identificada e o comando falha
```

## Validação e conclusão

Teste do harness com falha controlada e recuperação, HTTP externo e inspeção dos namespaces de teste.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
