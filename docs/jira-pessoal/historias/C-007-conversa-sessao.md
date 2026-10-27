# C-007 — Conversa com sessão e execução limitada

Marco: M3. Tipo: negócio.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Como paciente, continuar uma conversa e confirmar ações sem duplicá-las.

## Vínculos e dependências

- Requisitos: `RF-07`, `RF-08`, `RNF-01`, `RNF-03`, `RNF-04`, `RNF-08`, `RNF-10` — [especificação](../../../spec.md).
- Dependências: [CT-010](../historias-tecnicas/CT-010-tools-restritas.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Conversation conserva contexto recente/intenção em Redis com TTL e autorização por participante.
- [ ] Controlar ordem/versão por sessão entre instâncias, sem locks mantidos indefinidamente.
- [ ] Agent único usa provider controlado e dispatcher; os oito limites encerram execução.
- [ ] Confirmação de escrita vincula parâmetros à intenção; resposta usa resultado persistido, sem inventar sucesso.
- [ ] Detalhar D-09/D-10/D-11 no plano: TTLs/renovação/limites, garantia de continuidade e coordenação. Snapshot mínimo inclui contexto recente, intenção, parâmetros presentes/faltantes, etapa, referências e versão; não guarda credenciais, raciocínio interno ou histórico ilimitado.
- [ ] Autorizar leitura/escrita/retomada por tenant/clínica/ator/sessão e paciente permitido; negar IDs cruzados, revogação e mistura de duas sessões do mesmo ator. Sessão de conversa não substitui autenticação.
- [ ] Expiração/encerramento não é renovado por leitura passiva ou escrita atrasada; informar perda de contexto e recolher parâmetros necessários sem reaproveitar confirmação antiga. Alterar parâmetros invalida a confirmação anterior.
- [ ] Restart de instância retoma somente snapshot válido e etapa reconciliada; perda do Redis/state não autoriza reconstruir conversa de cache/logs, repetir tool ou zerar tetos/consumo. Reconciliar efeito persistente com a mesma intenção/chave.
- [ ] Rejeitar state inválido/incompatível/excessivo e saída tardia de execução obsoleta sem servir conteúdo sensível, sobrescrever versão nova ou recriar sessão expirada. Logs registram metadados mínimos.
- [ ] Disponibilizar contratos de criação/consulta e listagem mínima de sessões válidas do próprio ator para C-008, com autorização e expiração aplicadas pelo backend; listagem não expõe conteúdo/IDs de outro vínculo nem promete histórico permanente.

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

  Cenário: Expiração entre etapas
    Dado que a sessão contém profissional e horário coletados ainda sem reserva
    Quando sua validade termina antes da próxima confirmação
    Então a aplicação informa perda de contexto e não reserva com os parâmetros antigos

  Cenário: Isolamento de ator e sessão
    Dado que existem sessões de outros tenants e atores e duas sessões do mesmo ator
    Quando o cliente envia um identificador de sessão fora do vínculo autorizado
    Então não lê nem altera o state e nenhuma sessão herda parâmetros de outra

  Cenário: Permissão revogada antes do TTL
    Dado que uma sessão válida referencia um paciente cujo acesso foi revogado
    Quando o ator tenta continuar a conversa
    Então o backend nega acesso aos dados e não executa a ação proposta

  Cenário: Reinício da instância
    Dado que o último snapshot consistente continua válido no Redis e não há efeito pendente
    Quando a instância que atendia a sessão reinicia e outra recebe a mensagem
    Então a conversa preserva escolhas e etapa sem reiniciar os limites da execução

  Cenário: Commit sem atualização do state
    Dado que uma tool comitou uma reserva mas a instância caiu antes de salvar a resposta no state
    Quando a mesma intenção é retomada
    Então o serviço reconcilia o resultado persistido com a mesma chave sem duplicar reserva nem evento

  Cenário: Resposta de execução obsoleta
    Dado que a sessão expirou ou avançou de versão enquanto uma chamada estava em andamento
    Quando o resultado atrasado chega
    Então ele não ressuscita a sessão nem sobrescreve o state atual ou autoriza nova ação

  Cenário: Parâmetros mudam após confirmação
    Dado que uma intenção teve seus parâmetros confirmados
    Quando o usuário altera o profissional ou horário
    Então a confirmação anterior não autoriza executar a intenção modificada

  Cenário: State inválido ou excessivo
    Dado que um snapshot tem formato incompatível ou conteúdo acima do limite registrado
    Quando a aplicação tenta carregá-lo ou atualizá-lo
    Então ela trata o erro de forma segura sem executar a etapa nem expor o payload nos logs

  Cenário: Lista de conversas válidas
    Dado que existem sessões ativas e expiradas para dois atores de clínicas distintas
    Quando o ator solicita suas conversas recentes
    Então o backend lista somente as sessões válidas do vínculo autorizado sem revelar as demais
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
