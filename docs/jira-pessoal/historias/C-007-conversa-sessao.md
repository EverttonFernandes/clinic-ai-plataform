# C-007 — Conversa com sessão e execução limitada

Marco: M3. Tipo: negócio.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Como paciente, continuar uma conversa e confirmar ações sem duplicá-las.

## Vínculos e dependências

- Requisitos: `RF-07`, `RF-08`, `RNF-04`, `RNF-10` — [especificação](../../../spec.md).
- Dependências: [CT-010](../historias-tecnicas/CT-010-tools-restritas.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Conversation conserva contexto recente/intenção em Redis com TTL e autorização por participante.
- [ ] Controlar ordem/versão por sessão entre instâncias, sem locks mantidos indefinidamente.
- [ ] Agent único usa provider controlado e dispatcher; os oito limites encerram execução.
- [ ] Confirmação de escrita vincula parâmetros à intenção; resposta usa resultado persistido, sem inventar sucesso.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Conversa com sessão e execução limitada

  Cenário: Continuidade
    Dado que o paciente já selecionou um profissional em sessão autorizada
    Quando informa o horário e confirma
    Então a intenção usa a escolha atual e a reserva só é anunciada após o serviço confirmar

  Cenário: Mensagens simultâneas
    Dado que duas instâncias recebem mensagens da mesma sessão
    Quando atualizam a intenção
    Então a ordem/versão evita perda silenciosa e não mistura confirmações

  Cenário: Loop de tools
    Dado que o provider controlado solicita etapas sucessivas sem concluir
    Quando o limite determinístico é alcançado
    Então a tarefa encerra sem nova chamada cara ou sucesso inventado
```

## Validação e conclusão

Funcionais HTTP de conversa com Redis/PostgreSQL reais e provider controlado; concorrência e limites observáveis.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
