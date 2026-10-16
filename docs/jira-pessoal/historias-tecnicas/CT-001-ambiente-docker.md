# CT-001 — Ambiente Docker reproduzível

Marco: M1. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Subir API mínima e dependências em ambiente isolado antes de construir regras.

## Vínculos e dependências

- Requisitos: `RNF-11`, `RNF-12`, `RNF-13` — [especificação](../../../spec.md).
- Dependências: nenhuma; primeira história da implementação.
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Definir versões suportadas/travadas e comandos de build/up/down, com .env.example sem segredos.
- [ ] Compose inicia PostgreSQL/pgvector e Redis com healthchecks; API expõe liveness/readiness distintos.
- [ ] Parar ambiente preserva volumes; runtime sem root quando viável e sem ferramentas de build desnecessárias.
- [ ] Documentar portas, projeto Compose, perfis e recuperação de falha de dependência.
- [ ] Workflow Application CI em push da branch e PR executa build/smoke reais do ambiente; registrar sucesso do HEAD antes do PR e conferir os checks após abertura.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Ambiente Docker reproduzível

  Cenário: Subida limpa
    Dado que um checkout sem banco inicializado e configuração sintética
    Quando o ambiente é construído e iniciado
    Então as dependências ficam saudáveis e a API fica pronta sem ajuste manual no host

  Cenário: Dependência indisponível
    Dado que a API está ativa e o PostgreSQL é interrompido
    Quando a readiness é consultada
    Então ela indica indisponibilidade e não anuncia capacidade de executar reservas

  Cenário: Persistência local
    Dado que dados sintéticos existem no volume de desenvolvimento
    Quando o ambiente é parado e reiniciado
    Então os dados continuam disponíveis sem recriar ou apagar o volume
```

## Validação e conclusão

Smoke via HTTP, inspeção de configuração Compose e teste de reinício preservando dados; Docker real.
CI mínima entra nesta história, antes da consolidação em CT-003; teste disponível integra
o workflow assim que nasce. Branch/revisão por outro modelo/PR e aceite humano seguem o
[DoD oficial](../KANBAN-OFICIAL.md#definition-of-done).

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
