# CT-014 — Cache autorizado antes do Agent

Marco: M4. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Evitar novas chamadas de IA em respostas reutilizáveis sem misturar pacientes/contextos.

## Vínculos e dependências

- Requisitos: `RF-11`, `RF-07`, `RNF-01`, `RNF-03` — [especificação](../../../spec.md).
- Dependências: [C-009](../historias/C-009-faq-com-fontes.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Implementar answer-cache e shared-answer-cache separados, namespaced e com TTLs próprios.
- [ ] Incluir contexto/permissões/versão na identidade da entrada e autorizar cada hit.
- [ ] Shared cache contém somente conteúdo não pessoal; confirmação de write não é resposta reutilizável.
- [ ] Invalidar/versionar após atualização documental ou de permissão; cache de agenda opcional respeita commit.
- [ ] Hit não preenche state perdido nem recupera intenção/confirmação expirada; expiração/invalidação do cache não apaga state válido ou controles de consumo.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Cache autorizado antes do Agent

  Cenário: FAQ repetida
    Dado que uma resposta não pessoal elegível já está no cache válido
    Quando o usuário repete pergunta com contexto compatível
    Então responde sem Agent/RAG/LLM e incrementa somente os contadores aplicáveis ao request

  Cenário: Contexto diferente
    Dado que o mesmo texto ocorre para outro paciente ou permissões revogadas
    Quando o cache é consultado
    Então não retorna conteúdo pessoal ou obsoleto indevidamente

  Cenário: Documento atualizado
    Dado que a versão documental ativa foi substituída
    Quando a pergunta anterior é refeita
    Então a resposta antiga não é reutilizada como se fosse vigente

  Cenário: Cache remanescente após expiração de state
    Dado que a sessão expirou mas existe uma resposta elegível no cache
    Quando chega uma mensagem de confirmação que depende da intenção perdida
    Então o cache não restaura parâmetros nem confirmação e nenhuma reserva é criada
```

## Validação e conclusão

Funcionais HTTP com contagem independente de chamadas ao provider/retrieval e verificação dos namespaces Redis.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
