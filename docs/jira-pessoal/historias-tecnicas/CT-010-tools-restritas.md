# CT-010 — Dispatcher de tools com fronteiras de domínio

Marco: M3. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Permitir capacidades limitadas sem transformar o agente em acesso genérico ao sistema.

## Vínculos e dependências

- Requisitos: `RF-08`, `RNF-01`, `RNF-05` — [especificação](../../../spec.md).
- Dependências: [CT-009](../historias-tecnicas/CT-009-ai-gateway-controlado.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Registrar schemas de conhecimento, catálogo, paciente e create/cancel/update/consulta de agenda.
- [ ] Injetar identidade/contexto/idempotencyKey pelo backend, nunca por campos de confiança da LLM.
- [ ] Executar Tool → políticas do API Gateway → serviço; somente serviço acessa datastore.
- [ ] Bloquear tool desconhecida, SQL/shell/HTTP arbitrário, argumentos excessivos e efeitos sem confirmação.
- [ ] Tratar resultados de tools/RAG e resumos como dados não confiáveis: schema ou texto retornado não concede permissão. Revalidar capacidade/recurso no serviço, com escopo delegado mínimo e resultado/saída minimizados, mesmo quando o agente propõe ação incorreta.
- [ ] Implementar fronteira comum de execução e tradução de erros no dispatcher conforme a [spec](../../../spec.md#execução-de-tools-e-tratamento-de-erros), reutilizada pelas tools. Handler HTTP e worker preservam o contrato; sem copiar `try/except`, logging ou retry genérico em cada tool.
- [ ] Distinguir validação/autorização/conflito, falha transitória, falha inesperada e resultado incerto; retornar erro seguro com correlação. Capturas específicas permanecem nos adapters quando justificadas; cancelamento/deadline interrompe novas etapas sem declarar rollback de commit.
- [ ] Preservar chave/escopo/hash da intenção pelo backend; serviço transacional garante único efeito. Em erro após commit, reconciliar ou repetir com a mesma chave e autorização atual; não gerar chave nova nem renovar budget. Não repetir automaticamente erros permanentes/inesperados; retry seguro tem um dono e limites totais.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Dispatcher de tools com fronteiras de domínio

  Cenário: Tool de agenda válida
    Dado que o paciente confirmou o horário e a tool possui schema válido
    Quando o dispatcher executa createAppointment
    Então o serviço revalida identidade e persiste pela transação de domínio

  Cenário: Capacidade arbitrária
    Dado que o modelo propõe executeSQL ou uma URL externa
    Quando o dispatcher recebe a proposta
    Então ela é rejeitada sem SQL, shell ou conexão arbitrária

  Cenário: Identidade manipulada
    Dado que a tool call contém patientId/tenantId não autorizados
    Quando a aplicação valida o pedido
    Então não adota o contexto proposto e nenhum dado alheio é acessado

  Cenário: Injeção indireta em resultado de tool
    Dado que um resultado de consulta contém instrução para publicar documento ou acessar outro paciente
    Quando o agente propõe uma chamada privilegiada a partir desse texto
    Então dispatcher e serviço negam a capacidade ou recurso não autorizado sem acesso indevido nem efeito persistente
```

## Validação e conclusão

Provas adicionais obrigatórias, ainda planejadas:

```gherkin
  Cenário: Fronteira comum para tools distintas
    Dado que duas tools distintas podem lançar falhas inesperadas com marcador sintético sensível
    Quando são executadas pelo dispatcher e uma delas pelo endpoint HTTP consumidor
    Então a mesma política gera erro interno seguro com correlação sem revelar o marcador nem retornar sucesso ou repetir chamadas

  Cenário: Exceção após commit
    Dado que a reserva, o resultado idempotente e o evento foram comitados e a entrega do resultado da tool falha
    Quando o backend retoma a intenção autorizada com a mesma chave e payload
    Então recupera o resultado persistido com uma única reserva e evento sem renovar orçamento

  Cenário: Erro de negócio ou autorização
    Dado que a tool é negada por autorização ou encontra slot ocupado
    Quando o dispatcher traduz a falha
    Então mantém o significado estável sem retry automático nem novo efeito

  Cenário: Resultado incerto sem reconciliação disponível
    Dado que houve timeout em uma escrita e o banco está indisponível para consultar o resultado
    Quando o dispatcher devolve o estado da operação
    Então informa a incerteza sem alegar rollback ou sucesso e preserva a mesma intenção e chave para reconciliação

  Cenário: Cancelamento durante execução
    Dado que o turno é cancelado ou seu deadline é atingido durante uma chamada
    Quando o controle retorna ao dispatcher
    Então não agenda nova tool ou retry e preserva a reconciliação de eventual efeito comitado
```

Funcionais passando por políticas reais e serviços existentes; verificação independente de efeitos e ausência de conexões não permitidas.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
