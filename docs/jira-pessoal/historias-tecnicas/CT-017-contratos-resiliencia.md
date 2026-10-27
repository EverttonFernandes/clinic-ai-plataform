# CT-017 — Contratos de dependências e resiliência

Marco: M5. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Consolidar contratos de provider/embeddings/notificações e degradação antes da rede externa.

## Vínculos e dependências

- Requisitos: `RF-13`, `RNF-06`, `RNF-09` — [especificação](../../../spec.md).
- Dependências: [CT-016](../historias-tecnicas/CT-016-observabilidade-finops.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Definir contrato verificável de capacidades, schemas, usage e erros transitórios/permanentes.
- [ ] Coordenar retry/deadline e circuit breaker entre SDK/gateway/runtime; fallback somente se avaliado.
- [ ] Separar falha de retrieval de falha de agenda; bulkhead apenas quando a disputa medida exigir.
- [ ] Revalidar dataset e confirmar que troca de modelo não repete efeitos já persistidos.
- [ ] Exercitar a matriz de degradação do [detalhamento de segurança](../../spec-driven-development/seguranca-producao.md): falha de provider sem alternativa, Redis e PostgreSQL não produz sucesso inventado, fallback cruzado de dados ou contadores permissivos.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Contratos de dependências e resiliência

  Cenário: Contrato divergente
    Dado que o provider retorna tool arguments ou usage inválidos
    Quando o adapter valida a resposta
    Então rejeita ou degrada conforme contrato sem executar efeito inválido

  Cenário: Retrieval indisponível
    Dado que o índice falha mas Scheduling/PostgreSQL estão saudáveis
    Quando o paciente consulta um slot pelo caminho disponível
    Então a função determinística continua sem inventar resposta documental

  Cenário: Fallback após ação
    Dado que uma reserva já foi comitada antes de falha de geração
    Quando a resposta final usa alternativa segura
    Então nenhuma segunda reserva é criada e o resultado persistido é preservado

  Cenário: Provider sem alternativa segura
    Dado que o provider está indisponível e não há fallback avaliado
    Quando uma resposta exige geração
    Então a aplicação informa a limitação dentro do deadline sem inventar resposta ou repetir writes

  Cenário: PostgreSQL indisponível
    Dado que o PostgreSQL não está acessível e o cache mostra um horário previamente disponível
    Quando a reserva é solicitada
    Então ela não é confirmada pelo cache e a operação informa indisponibilidade
```

## Validação e conclusão

Testes de contrato e falhas com adapters controlados, serviços reais e dataset de regressão.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
