# CT-003 — CI inicial no GitHub Actions

Marco: M1. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Consolidar a CI mínima iniciada em CT-001 e ampliada com os testes de CT-002.

## Vínculos e dependências

- Requisitos: `RNF-12`, `RNF-13` — [especificação](../../../spec.md).
- Dependências: [CT-002](../historias-tecnicas/CT-002-harness-testes.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Consolidar Application CI de push de branches e PR com build, análise e smoke/testes disponíveis, preservando os gates já executados em CT-001/CT-002.
- [ ] Usar Docker, permissões mínimas, timeouts, concorrência e artifacts sanitizados.
- [ ] PRs de forks não recebem secrets de produção nem fazem chamadas pagas ou deploy.
- [ ] Uma assertion quebrada impede sucesso; não usar placeholders verdes para suítes inexistentes.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: CI inicial no GitHub Actions

  Cenário: Regressão no PR
    Dado que um PR introduz uma assertion funcional que falha
    Quando a CI executa os gates afetados
    Então o resultado é falha com relatório e sem publicação

  Cenário: Checkout limpo
    Dado que um runner não possui dependências locais do desenvolvedor
    Quando a CI constrói o ambiente
    Então o smoke e os testes disponíveis executam em Docker

  Cenário: PR sem segredos
    Dado que um PR externo executa validação
    Quando o workflow é inspecionado e rodado
    Então não acessa credenciais de provider, registry de escrita ou ambiente de deploy
```

## Validação e conclusão

Validação local equivalente e evidência de run do GitHub Actions quando autorizado; sem run remoto, gate remoto PENDING.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
