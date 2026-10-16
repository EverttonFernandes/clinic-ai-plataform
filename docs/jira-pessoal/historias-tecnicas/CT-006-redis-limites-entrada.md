# CT-006 — Redis e limites compartilhados de entrada

Marco: M2. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Impedir abuso de requests e preparar estado temporário compartilhado.

## Vínculos e dependências

- Requisitos: `RNF-01`, `RNF-03`, `RF-07` — [especificação](../../../spec.md).
- Dependências: [CT-005](../historias-tecnicas/CT-005-identidade-autorizacao.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Separar namespaces tenant/clínica de sessão/uso e janelas de rate/quota/concurrency.
- [ ] Atualizações atômicas entre instâncias; TTL da sessão não renova quota.
- [ ] Identificar ator autenticado e origem/canal anônimo; negar tráfego protegido quando o controle falha.
- [ ] Registrar requests e rejeições sem liberar chamadas caras; orçamento monetário vem em CT-008.
- [ ] Documentar classes separadas de state, cache e consumo e política D-09 por finalidade; state terá escopo tenant/clínica/ator/sessão, sem impor uma instância Redis por classe.
- [ ] Gravações/atualizações temporárias mantêm expiração consistentemente; validar que o caminho de substituição não produz chave sem TTL e que valores de cliente/LLM não ampliam retenção.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Redis e limites compartilhados de entrada

  Cenário: Quota entre instâncias
    Dado que duas instâncias compartilham a mesma quota restante de um request
    Quando recebem pedidos concorrentes do mesmo ator
    Então somente um é admitido e o contador não ultrapassa a quota

  Cenário: Nova sessão
    Dado que o ator esgotou a quota da janela atual
    Quando abre outra sessão
    Então o limite continua esgotado até a janela correspondente

  Cenário: Redis fora
    Dado que o backend não consegue verificar os limites compartilhados
    Quando recebe um pedido protegido
    Então nega a operação sem usar limite local permissivo

  Cenário: Atualização preserva política de expiração
    Dado que um registro temporário possui prazo definido pela finalidade
    Quando o adapter substitui seu conteúdo
    Então a expiração segue a política definida e o registro não se torna permanente

  Cenário: Finalidades independentes
    Dado que state, cache e quota têm prazos distintos na política de teste
    Quando um deles expira ou é atualizado
    Então a validade dos outros não é alterada implicitamente
```

## Validação e conclusão

Integração com Redis real e requests concorrentes; verificar contador, TTL, respostas e inexistência de execução protegida.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
