# C-008 — Chat Web mínimo integrado

Marco: M3. Tipo: negócio.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Como paciente, percorrer cadastro autorizado, catálogo e agenda pelo navegador.

## Vínculos e dependências

- Requisitos: `RF-07`, `RF-01`, `RNF-08` — [especificação](../../../spec.md).
- Dependências: [C-007](../historias/C-007-conversa-sessao.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Servir cliente Web mínimo pela aplicação, sem adicionar framework frontend obrigatório.
- [ ] Autenticação e sessão integradas às APIs reais; credenciais não são exemplos hardcoded.
- [ ] Exibir sucesso, vazio, falha, limite e confirmação pendente sem inserir HTML do modelo.
- [ ] Se houver SSE, cancelar/fechar conexão não remove limites nem repete efeitos; sem SSE obrigatório para o primeiro incremento.
- [ ] Distinguir estado expirado/perdido de falha de autenticação; orientar recolha mínima de parâmetros e nova confirmação sem anunciar que um commit anterior foi cancelado.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Chat Web mínimo integrado

  Cenário: Jornada visível
    Dado que a paciente está autenticada no Web e há profissional/slot sintéticos
    Quando consulta e confirma uma reserva pelo chat
    Então a tela mostra o resultado real e a reserva existe no PostgreSQL

  Cenário: Conteúdo não confiável
    Dado que uma resposta contém markup com script
    Quando o cliente apresenta a mensagem
    Então o conteúdo é tratado como texto e não executa código

  Cenário: Resposta pendente
    Dado que a reserva foi comitada mas a resposta de rede se perdeu
    Quando o usuário tenta novamente na interface
    Então a mesma intenção é reconciliada sem duplicar a consulta

  Cenário: Contexto expirado na interface
    Dado que a sessão de conversa expirou e a autenticação continua válida
    Quando o usuário tenta continuar uma intenção ainda não executada
    Então a interface informa a perda de contexto e solicita os parâmetros necessários sem confirmar reserva inexistente
```

## Validação e conclusão

Funcional HTTP mais evidência de navegador da jornada; teste de renderização segura; provider controlado identificado.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
