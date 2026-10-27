# CT-021 — Falhas, carga, concorrência e restauração

Marco: M6. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Medir comportamento sob disputa e falhas antes de aumentar instâncias ou publicar.

## Vínculos e dependências

- Requisitos: `RNF-02`, `RNF-03`, `RNF-06`, `RNF-10`, `RF-07` — [especificação](../../../spec.md).
- Dependências: [CT-020](../historias-tecnicas/CT-020-seguranca-privacidade.md), [CT-014](../historias-tecnicas/CT-014-cache-respostas.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Executar cenários de indisponibilidade de PostgreSQL/Redis/provider e falha entre commit/publicação.
- [ ] Repetir 100 concorrentes por slot e corridas de reagendamento/idempotência/budget.
- [ ] Medir p95/throughput/erros/filas/uso em carga sintética declarada; registrar baseline sem inventar SLA.
- [ ] Backup/restore PostgreSQL e documentos em ambiente descartável; recuperar registros/limites e medir RPO/RTO.
- [ ] Distinguir restart da API, perda/eviction de state e indisponibilidade/perda do Redis: continuidade somente com snapshot válido; perda informa limite, mantém efeitos/consumo e não libera replay. Se houver restauração de state, validar expiração, revogação e resultado transacional.
- [ ] Identificar pontos únicos de falha e evidências faltantes sob D-05/D-15: réplicas de API e backup não provam HA das dependências. Medir retorno ao serviço e reconciliação; ensaio de failover só é obrigatório no ambiente/estratégia que o adotar.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Falhas, carga, concorrência e restauração

  Cenário: Redis perdido
    Dado que existem chamadas/reservas de consumo ainda em aberto
    Quando Redis é reiniciado sem seus dados
    Então novas operações caras permanecem bloqueadas até reconstruir limites confiáveis

  Cenário: Restauração
    Dado que um backup sintético consistente está disponível
    Quando é restaurado em projeto Compose isolado
    Então reservas/documentos/resultados idempotentes são verificáveis e nenhum ambiente de desenvolvimento é apagado

  Cenário: Sobrecarga
    Dado que a taxa de pedidos supera capacidade medida
    Quando a carga sintética é aplicada
    Então backpressure/limites preservam integridade e o relatório informa p95, erros e consumo

  Cenário: Perda de state após reserva
    Dado que uma reserva e seu resultado idempotente estão comitados mas a resposta não chegou ao paciente
    Quando o state é perdido e o usuário repete a tentativa pela mesma intenção identificável
    Então o resultado é reconciliado no PostgreSQL sem nova reserva e sem reconstruir confirmação a partir do cache

  Cenário: Snapshot antigo reaparece
    Dado que um snapshot anterior à expiração ou revogação é reapresentado à aplicação
    Quando o backend verifica sua validade antes da retomada
    Então ele não reativa a sessão nem concede autorização ou saldo anterior

  Cenário: Recuperação do banco após resposta incerta
    Dado que uma reserva pode ter sido comitada antes da indisponibilidade do PostgreSQL
    Quando o banco retorna e a mesma intenção é consultada ou repetida com a chave original
    Então o serviço reconcilia o resultado sem segunda reserva ou evento e registra a recuperação observada
```

## Validação e conclusão

Ferramenta de carga escolhida na execução, testes concorrentes e falhas reais em contêineres descartáveis; números medidos.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
