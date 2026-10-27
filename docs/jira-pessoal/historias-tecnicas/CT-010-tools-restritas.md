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

Funcionais passando por políticas reais e serviços existentes; verificação independente de efeitos e ausência de conexões não permitidas.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
