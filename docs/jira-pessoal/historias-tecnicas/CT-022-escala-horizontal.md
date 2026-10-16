# CT-022 — Duas instâncias e balanceamento no laboratório

Marco: M6. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Demonstrar que estado externo e limites continuam corretos entre instâncias.

## Vínculos e dependências

- Requisitos: `RNF-10`, `RNF-03`, `RF-07` — [especificação](../../../spec.md).
- Dependências: [CT-021](../historias-tecnicas/CT-021-falhas-carga-restauracao.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Adicionar perfil Compose de balanceamento com ao menos duas instâncias e worker concorrente.
- [ ] Reusar Redis/PostgreSQL/storage compartilhados, pools limitados e budget global.
- [ ] Provar ordem de sessão e posse de job; falha de uma instância não perde evento durável.
- [ ] Comparar baseline e gargalos; não prometer autoscaling/Kubernetes nem disponibilidade de produção.
- [ ] Validar a decisão D-11 com sessões concorrentes: conflito explícito, duplicatas e resultado atrasado após perda de posse/expiração não sobrescrevem state nem duplicam efeitos; mesma sessão continua em outra instância somente se ainda válida.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Duas instâncias e balanceamento no laboratório

  Cenário: Sessão em duas instâncias
    Dado que mensagens da mesma conversa chegam a backends diferentes
    Quando a intenção é atualizada
    Então a sequência/versão preserva escolhas e não duplica ação

  Cenário: Quota global
    Dado que duas instâncias recebem tráfego do mesmo tenant
    Quando a quota compartilhada se esgota
    Então nenhuma instância recebe orçamento adicional local

  Cenário: Worker obsoleto
    Dado que um worker perde lease e outro assume o job
    Quando o primeiro tenta publicar atrasado
    Então a atualização condicionada impede sobrescrever estado mais recente

  Cenário: Execução de conversa perde posse
    Dado que uma execução antiga perdeu sua autorização de atualização e outra instância avançou a sessão
    Quando a execução antiga termina a chamada ao provider
    Então não sobrescreve escolhas novas nem libera posse alheia ou inicia outra tool com a confirmação antiga
```

## Validação e conclusão

Funcionais e carga no perfil multi-instância real; identificar backend nos traces e verificar estado final compartilhado.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
