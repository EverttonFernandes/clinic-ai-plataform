# C-008 — Chat Web conversacional inspirado no ChatGPT

Marco: M3. Tipo: negócio.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Como paciente, conversar com o assistente em uma interface Web familiar, inspirada na
experiência de chat do ChatGPT, para consultar informações, escolher profissionais e
horários e confirmar ações com clareza sobre o que está acontecendo.

Esta história evolui o chat mínimo já previsto, preservando seu ID, dependência e posição
no Kanban. A referência orienta a experiência de conversa; identidade visual e conteúdo
pertencem à plataforma. A interface acompanha os módulos disponíveis em cada marco:
agenda em M3; FAQ/fontes após C-009. Não apresentar funcionalidades ainda não integradas.

## Vínculos e dependências

- Requisitos: `RF-07`, `RF-01`, `RNF-08` — [especificação](../../../spec.md).
- Dependências: [C-007](../historias/C-007-conversa-sessao.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Disponibilizar frontend conversacional integrado à aplicação, com hierarquia visual e interações definidas no escopo abaixo; registrar D-12 antes da implementação, sem tornar um framework frontend específico obrigatório.
- [ ] Autenticação e sessão integradas às APIs reais; credenciais não são exemplos hardcoded.
- [ ] Exibir sucesso, vazio, falha, limite e confirmação pendente sem inserir HTML do modelo.
- [ ] Se houver SSE, cancelar/fechar conexão não remove limites nem repete efeitos; sem SSE obrigatório para o primeiro incremento.
- [ ] Distinguir estado expirado/perdido de falha de autenticação; orientar recolha mínima de parâmetros e nova confirmação sem anunciar que um commit anterior foi cancelado.
- [ ] Layout responsivo com navegação lateral recolhível, ação Nova conversa, lista de conversas recentes ainda válidas, área central de mensagens e compositor acessível na parte inferior. Em tela estreita, a navegação não encobre permanentemente a conversa ou o campo de entrada.
- [ ] Estado inicial apresenta a finalidade do assistente e sugestões de perguntas compatíveis com os serviços disponíveis; usuário e assistente têm mensagens visualmente distinguíveis, com texto legível e conteúdo longo sem quebrar o layout.
- [ ] Compositor aceita múltiplas linhas; enviar por botão ou Enter, usar Shift+Enter para quebra de linha e respeitar composição de texto/IME. Impedir envio vazio e envio duplicado enquanto o mesmo turno aguarda resultado; preservar o rascunho quando houver falha antes da aceitação.
- [ ] Exibir estados reais de enviando/processando/respondendo/concluído, indisponibilidade, limite atingido e confirmação pendente. Streaming, se adotado em D-12, mostra texto incremental e permite interromper a exibição/geração conforme contrato, sem anunciar rollback de efeitos ou liberar quotas.
- [ ] Nova conversa cria sessão isolada e limpa escolhas/confirmações da interface; alternar entre conversas consulta somente sessões do ator autorizado ainda válidas. Expiradas não são tratadas como histórico permanente e uma sessão não herda a intenção de outra.
- [ ] Mensagens mantêm ordem e identidade estável: refresh/reconexão reconcilia o último state válido sem duplicar mensagens ou ações. Resultado recebido para conversa que deixou de estar selecionada não é inserido na conversa atual.
- [ ] Atualizações acompanham o fim da conversa apenas se o usuário já estiver nele; ao ler mensagens anteriores, oferecer indicação de novas mensagens sem forçar rolagem. Foco de teclado não é perdido a cada atualização.
- [ ] Resumo de confirmação expõe profissional, data, horário/fuso e ação propostos; somente resultado persistido do backend permite mostrar reserva/cancelamento/reagendamento concluído. Alterar parâmetros exige nova confirmação e erro de rede não vira sucesso.
- [ ] Navegação, compositor e ações funcionam por teclado, têm nomes acessíveis, foco visível e estados de carregamento/erro anunciáveis por tecnologia assistiva, sem depender apenas de cor; avisos não tornam o texto incremental uma sequência excessiva de anúncios.
- [ ] UI renderiza conteúdo do modelo como texto seguro. Markdown é decisão D-12 e, se habilitado, usa sanitização/allowlist sem HTML bruto ou URLs executáveis; erro não expõe payload interno. Logout/troca de identidade limpa mensagens e referências locais; não persistir conversa ou credenciais em localStorage por conveniência.

## Limites e integração incremental

- A aplicação continua com API/worker e responsabilidades DDD existentes. O frontend
  apresenta contratos públicos; não acessa Redis, banco ou provider diretamente.
  Seu código fica neste repositório, organizado em componentes e funcionalidades; seus
  assets integram a release da plataforma, servidos pela aplicação. D-12 pode escolher
  ferramentas de build, preservando esse contrato sem criar serviço de negócio separado.
- A lista lateral usa apenas sessões válidas autorizadas de C-007. Histórico permanente,
  pesquisa em conversas antigas e sincronização entre canais dependem de decisão futura.
  Ao recarregar, a UI apresenta a janela de contexto ainda retida pelo backend e informa
  quando ela é limitada; não promete uma transcrição integral fora da política D-09.
- M3 usa provider controlado explicitamente identificado no ambiente de estudo. Mensagens,
  estados de execução e cards de agenda vêm do fluxo real, sem delays/etapas inventados.
- Após C-009, a mesma UI apresenta fontes retornadas pelo backend junto da resposta, com
  referência autorizada; não antecipar retrieval falso para concluir C-008.
- Upload de documentos da clínica pertence à CT-011. Anexos do paciente no compositor,
  voz, imagens, seletor de modelos, edição/regeneração de turnos e compartilhamento público
  de conversas não entram implicitamente por semelhança com o ChatGPT.
- Estilo visual, stack, transporte e biblioteca de renderização serão registrados em D-12;
  layout navegável e fluxos de erro/confirmação devem ser definidos antes do código.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Chat Web conversacional inspirado no ChatGPT

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

  Cenário: Início e envio de mensagem
    Dado que o paciente abriu uma sessão Web autenticada sem conversa selecionada
    Quando inicia uma conversa e envia uma pergunta pelo compositor
    Então a mensagem aparece uma vez na área central e os estados de processamento e resposta são observáveis

  Cenário: Texto multilinha e envio vazio
    Dado que o foco está no compositor
    Quando o usuário usa Shift+Enter ou tenta enviar apenas espaços
    Então pode escrever várias linhas e o conteúdo vazio não gera request ao backend

  Cenário: Conversas separadas
    Dado que uma conversa contém profissional e horário ainda não confirmados
    Quando o usuário inicia outra conversa e depois alterna entre ambas
    Então cada sessão mantém apenas suas escolhas válidas e nenhuma confirmação é transferida

  Cenário: Resposta chega após trocar a conversa
    Dado que uma conversa aguarda resposta e o usuário selecionou outra sessão
    Quando o resultado da primeira conversa chega
    Então ele fica associado à sessão de origem sem aparecer no histórico da sessão selecionada

  Cenário: Falha de envio antes da aceitação
    Dado que um rascunho válido foi digitado e a rede falha antes da aceitação pelo backend
    Quando o envio falha
    Então a interface informa o erro e permite tentar novamente preservando o texto sem duplicar o turno

  Cenário: Reconexão com resultado desconhecido
    Dado que o request foi aceito e a conexão caiu antes de informar seu resultado
    Quando o usuário reconecta ou atualiza a página
    Então a interface reconcilia a mesma intenção antes de oferecer nova execução e não duplica mensagens ou reservas

  Cenário: Navegação acessível em tela estreita
    Dado que o chat está aberto em uma viewport móvel e o usuário navega por teclado
    Quando abre a navegação lateral, seleciona uma conversa e retorna ao compositor
    Então os controles têm nomes e foco identificáveis e a conversa pode ser usada sem sobreposição permanente

  Cenário: Leitura de mensagens anteriores
    Dado que o usuário está lendo mensagens anteriores e chega uma atualização
    Quando a interface apresenta a atualização
    Então preserva a posição e o foco e oferece acesso às novas mensagens sem rolar à força

  Cenário: Identidade encerrada
    Dado que mensagens pessoais estão visíveis em uma sessão autenticada
    Quando ocorre logout ou troca de identidade
    Então a interface limpa mensagens e referências locais e o backend nega acesso à sessão anterior

  Cenário: Limite ou indisponibilidade
    Dado que o backend recusou o turno por quota ou dependência indisponível
    Quando a interface recebe a resposta
    Então informa a condição e mantém as escolhas válidas sem simular resposta do assistente ou contornar o limite
```

## Validação e conclusão

Funcional HTTP mais testes de navegador contra aplicação real: jornada, estados de erro,
isolamento de sessões, reconexão, responsividade, teclado/foco e renderização segura.
Provider controlado identificado; verificar efeitos no PostgreSQL e contagem de turnos
independentemente do texto da UI. Evidência visual acompanha os testes e não substitui integração.
Streaming/Markdown, se adotados, têm seus contratos e cenários negativos cobertos; ausência
de um desses recursos é decisão explícita D-12, não uma alegação de equivalência completa ao ChatGPT.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
