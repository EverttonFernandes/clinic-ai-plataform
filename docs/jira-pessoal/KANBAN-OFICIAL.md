# Kanban oficial — Clínica IA

Fila única de implementação baseada na [especificação](../../spec.md).
Atualizado em 2026-10-16. **Planejamento e harness preparados; nenhuma história de aplicação iniciada.**

## Como selecionar a próxima história

- Começar por **CT-001**. WIP inicial: uma história em Doing.
- Escolher a primeira linha To Do cujas dependências estejam Done. A ordem é cronológica por dependência, não um prazo de calendário.
- Não iniciar tarefas dependentes antes dos pré-requisitos. Se houver bloqueio externo, registrar motivo e retomar a primeira tarefa independente elegível, sem reordenar silenciosamente a fila.
- Estados: To Do → Doing → Review → Done; Blocked registra dependência externa ou impedimento concreto. Não confundir Backlog opcional com bloqueio.
- Review aguarda revisão e merge do usuário. O agente não faz merge/auto-merge nem avança
  para outra história durante essa espera. PR aberto não equivale a Done.
- Estado oficial fica somente nesta tabela. Planos/entregas registram provas, não uma segunda prioridade.
- D-01/D-02/D-03, nas [decisões](../spec-driven-development/decisoes.md), exigem insumos externos na história correspondente. Sua ausência não autoriza inventar evidência ou chamar fake de integração externa.

## Linha principal

| Ordem | Marco | História | Tipo | Dependências | Estado |
| --- | --- | --- | --- | --- | --- |
| 01 | M1 | [CT-001 — Ambiente Docker reproduzível](historias-tecnicas/CT-001-ambiente-docker.md) | Técnica | — | To Do |
| 02 | M1 | [CT-002 — Harness de testes isolados e evidências](historias-tecnicas/CT-002-harness-testes.md) | Técnica | CT-001 | To Do |
| 03 | M1 | [CT-003 — CI inicial no GitHub Actions](historias-tecnicas/CT-003-ci-inicial.md) | Técnica | CT-002 | To Do |
| 04 | M2 | [CT-004 — Persistência multi-tenant e migrations](historias-tecnicas/CT-004-persistencia-migrations.md) | Técnica | CT-003 | To Do |
| 05 | M2 | [CT-005 — Identidade, tenant confiável e fronteira de API](historias-tecnicas/CT-005-identidade-autorizacao.md) | Técnica | CT-004 | To Do |
| 06 | M2 | [CT-006 — Redis e limites compartilhados de entrada](historias-tecnicas/CT-006-redis-limites-entrada.md) | Técnica | CT-005 | To Do |
| 07 | M2 | [C-001 — Consulta autorizada de dados do paciente](historias/C-001-dados-paciente.md) | Negócio | CT-006 | To Do |
| 08 | M2 | [C-002 — Catálogo de especialidades e profissionais](historias/C-002-catalogo-profissionais.md) | Negócio | C-001 | To Do |
| 09 | M2 | [C-003 — Consulta de horários disponíveis](historias/C-003-disponibilidade-agenda.md) | Negócio | C-002 | To Do |
| 10 | M2 | [C-004 — Reserva idempotente com proteção de concorrência](historias/C-004-criar-reserva.md) | Negócio | C-003 | To Do |
| 11 | M2 | [C-005 — Cancelamento autorizado e idempotente](historias/C-005-cancelar-reserva.md) | Negócio | C-004 | To Do |
| 12 | M2 | [C-006 — Reagendamento atômico](historias/C-006-reagendar-reserva.md) | Negócio | C-005 | To Do |
| 13 | M2 | [CT-007 — Entrega recuperável de eventos e notificações](historias-tecnicas/CT-007-outbox-auditoria-notificacoes.md) | Técnica | C-006 | To Do |
| 14 | M3 | [CT-008 — Budget cumulativo e ledger de consumo](historias-tecnicas/CT-008-budget-runtime.md) | Técnica | CT-007 | To Do |
| 15 | M3 | [CT-009 — AI Gateway e provider determinístico](historias-tecnicas/CT-009-ai-gateway-controlado.md) | Técnica | CT-008 | To Do |
| 16 | M3 | [CT-010 — Dispatcher de tools com fronteiras de domínio](historias-tecnicas/CT-010-tools-restritas.md) | Técnica | CT-009 | To Do |
| 17 | M3 | [C-007 — Conversa com sessão e execução limitada](historias/C-007-conversa-sessao.md) | Negócio | CT-010 | To Do |
| 18 | M3 | [C-008 — Chat Web conversacional inspirado no ChatGPT](historias/C-008-chat-web.md) | Negócio | C-007 | To Do |
| 19 | M4 | [CT-011 — Upload privado e validação de documentos](historias-tecnicas/CT-011-upload-quarentena.md) | Técnica | C-008 | To Do |
| 20 | M4 | [CT-012 — Ingestão assíncrona e versões completas](historias-tecnicas/CT-012-ingestao-versionada.md) | Técnica | CT-011 | To Do |
| 21 | M4 | [CT-013 — Retrieval autorizado no PostgreSQL e pgvector](historias-tecnicas/CT-013-retrieval-pgvector.md) | Técnica | CT-012 | To Do |
| 22 | M4 | [C-009 — FAQ com RAG e fontes](historias/C-009-faq-com-fontes.md) | Negócio | CT-013 | To Do |
| 23 | M4 | [CT-014 — Cache autorizado antes do Agent](historias-tecnicas/CT-014-cache-respostas.md) | Técnica | C-009 | To Do |
| 24 | M4 | [CT-015 — Dataset e pipeline de evals offline](historias-tecnicas/CT-015-evals-offline.md) | Técnica | CT-014 | To Do |
| 25 | M5 | [CT-016 — Observabilidade e FinOps de ponta a ponta](historias-tecnicas/CT-016-observabilidade-finops.md) | Técnica | CT-015 | To Do |
| 26 | M5 | [CT-017 — Contratos de dependências e resiliência](historias-tecnicas/CT-017-contratos-resiliencia.md) | Técnica | CT-016 | To Do |
| 27 | M5 | [CT-018 — Integração controlada com provider real](historias-tecnicas/CT-018-provider-real.md) | Técnica | CT-017 | To Do |
| 28 | M5 | [C-010 — Entrada WhatsApp confiável e inbox durável](historias/C-010-whatsapp-inbox.md) | Negócio | CT-017 | To Do |
| 29 | M5 | [CT-019 — Worker de canal e outbound recuperável](historias-tecnicas/CT-019-whatsapp-outbound.md) | Técnica | C-010, CT-007, C-007 | To Do |
| 30 | M5 | [CT-020 — Verificação adversarial e políticas de privacidade](historias-tecnicas/CT-020-seguranca-privacidade.md) | Técnica | CT-017, C-010 | To Do |
| 31 | M6 | [CT-021 — Falhas, carga, concorrência e restauração](historias-tecnicas/CT-021-falhas-carga-restauracao.md) | Técnica | CT-020, CT-014 | To Do |
| 32 | M6 | [CT-022 — Duas instâncias e balanceamento no laboratório](historias-tecnicas/CT-022-escala-horizontal.md) | Técnica | CT-021 | To Do |
| 33 | M6 | [CT-023 — Avaliação de índices vetoriais e metadados](historias-tecnicas/CT-023-indices-vetoriais.md) | Técnica | CT-022 | To Do |
| 34 | M6 | [CT-024 — Destino real, secrets, TLS e proteção de dados](historias-tecnicas/CT-024-prontidao-ambiente-real.md) | Técnica | CT-021 | To Do |
| 35 | M6 | [CT-025 — CI completa, release e CD controlado](historias-tecnicas/CT-025-release-cicd.md) | Técnica | CT-024, CT-023, CT-018, CT-019 | To Do |
| 36 | M6 | [CT-026 — Aceite integrado e roteiro de demonstração](historias-tecnicas/CT-026-aceite-seis-fluxos.md) | Técnica | CT-025 | To Do |

## Backlog opcional

| Ordem | História | Condição de entrada | Dependência | Estado |
| --- | --- | --- | --- | --- |
| 37 | [C-011 — Aprovação humana para ação de alto risco definida](historias/C-011-aprovacao-alto-risco.md) | D-06 e autorização do escopo de alto risco. | CT-026 | Backlog |
| 38 | [CT-027 — Avaliação do LiteLLM como gateway de modelos](historias-tecnicas/CT-027-avaliacao-litellm.md) | D-07, escolha explícita da evolução e escopo de custo definido. | CT-026 | Backlog |
| 39 | [CT-028 — Avaliação de consolidação analítica no Databricks](historias-tecnicas/CT-028-avaliacao-databricks.md) | D-08, escolha explícita da evolução, workspace e custo autorizado. | CT-026 | Backlog |

DDD é uma decisão transversal aplicada desde CT-001/CT-002, conforme o
[mapa de contextos](../spec-driven-development/arquitetura-ddd.md). LiteLLM e Databricks
são candidatos futuros; entram na execução somente por promoção explícita deste backlog,
sem alterar as dependências ou o aceite do MVP.

## Marcos de demonstração

| Marco | Primeira demonstração útil | Fechamento da etapa |
| --- | --- | --- |
| M1 | API e testes em Docker, CI pequena. | CT-003 |
| M2 | Paciente consulta catálogo/agenda e cria/cancela/reagenda por API sem LLM. | CT-007 |
| M3 | Chat Web responsivo com experiência inspirada no ChatGPT usa sessões válidas, tools e provider controlado com limites. | C-008 |
| M4 | FAQ usa documento sintético real, pgvector e cache; dataset de evals executável. | CT-015 |
| M5 | Observabilidade, contratos, integração externa e revisão adversarial. | CT-020; CT-018/CT-019 exigem suas provas externas para fechar o marco. |
| M6 | Carga, falhas, restauração, escala e promoção controlada; seis fluxos demonstrados. | CT-026 |

Um laboratório em M3/M4 é utilizável para estudo sem afirmar qualidade de LLM real ou prontidão de produção.
As histórias de provider, WhatsApp externo, proteção real e CD permanecem pendentes se faltarem recursos/autorização.

## Definition of Ready

História com escopo, critérios BDD, requisitos e dependências identificados; ambiente e evidência
esperados claros; decisões que bloqueiam execução resolvidas ou registradas como impedimento.
O primeiro passo de cada história detalha plano/testes, sem aumentar escopo por conveniência.

## Definition of Done

- Critérios e invariantes aplicáveis satisfeitos; comportamento validado por evidência executada.
- Cenário funcional escrito antes do código; Red correto e Green registrados quando há comportamento novo.
- Integrações críticas usam componentes reais; simulações identificadas e gate externo não realizado fica PENDING.
- Revisão de coesão, nomes e fronteiras após validação; refatorar somente se houver ganho concreto.
- Testes dos consumidores afetados, documentação e contratos atualizados; sem dados pessoais ou secrets em evidências.
- [Entrega](../entregas/TEMPLATE.md) com comandos/resultados/limitações e referência à revisão validada.
- Executor GPT-6 Astra/medium e revisão GPT-6 Sol em outra execução; nenhum fallback pelo executor.
- Branch `story/<ID>-<slug>`, commits convencionais, CI do HEAD verde antes do PR e checks do PR verdes.
- PR com decisões, critérios/evidências e roteiro de estudo/reprodução; revisão/merge feitos pelo usuário.
- Completion check final aprovado e finish com ownership válido após prova de merge; até lá Review.
- CI mínima da aplicação começa em CT-001; CT-002 amplia testes, CT-003 consolida. Não exigir
  tag/deploy em toda história; CD/release têm critérios próprios e autorização correspondente.

## Replanejamento

Registrar motivo, impacto em requisitos e dependências e nova ordem nesta tabela. Não apagar testes,
reduzir exigências de segurança ou acrescentar microserviços apenas para concluir uma história.
O Kanban permanece a fila oficial. Tracking, ownership e completion gate locais estão implementados
no [harness](../spec-driven-development/harness.md); não há seletor universal de testes nem execução automática do backlog.
