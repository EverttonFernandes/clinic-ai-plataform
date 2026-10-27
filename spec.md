# Clínica IA — especificação de implementação

Estado: baseline de planejamento, sem aplicação implementada. Data: 2026-10-16.
As histórias estão em To Do; esta preparação não comprova comportamento executável.

## 1. Fontes e precedência

Esta especificação transforma o [System Design V2](draw.io/System%20Design%20-%20Clinica%20IA)
e seu [guia de estudo](README.md) em requisitos verificáveis. Preserva a arquitetura existente.
Os prompts de elaboração continuam locais e não são necessários para executar este planejamento.

- `spec.md`: comportamento e restrições normativos.
- [Kanban oficial](docs/jira-pessoal/KANBAN-OFICIAL.md): ordem e estado de execução.
- Histórias: recortes de entrega e critérios de aceite; não podem reduzir a especificação.
- [Decisões](docs/spec-driven-development/decisoes.md): escolhas de implementação e pendências.
- [Arquitetura DDD](docs/spec-driven-development/arquitetura-ddd.md): contextos, propriedade dos dados, dependências e evoluções opcionais.
- [Harness](docs/spec-driven-development/harness.md): protocolo e verificadores locais de execução/conclusão.
- Diagramas/README: explicação e referências visuais; atualizar se a implementação aprovada divergir.

Uma mudança de requisito deve explicitar motivo e impacto e atualizar histórias e rastreabilidade.
Não alterar critérios para acomodar testes falhando. Não criar uma segunda fila de execução.

## 2. Produto e limites

Plataforma multi-tenant para clínicas. Pacientes consultam informações, profissionais,
dados pessoais permitidos e agenda, e criam, cancelam ou alteram consultas via Web e WhatsApp.
O assistente interpreta intenções; serviços determinísticos protegem dados e efeitos.

Personas: paciente, operador da clínica com permissões explícitas e operador da plataforma.
Um tenant pode conter clínicas; o laboratório usará dois tenants e ao menos duas clínicas
para testar autorização. A associação ator/paciente/clínica nunca vem de uma afirmação da LLM.

O MVP não inclui diagnóstico, prescrição, cobrança, prontuário completo, aplicativo mobile,
multiagentes ou marketplace. Dados clínicos/pagamentos citados no desenho permanecem oficiais
no PostgreSQL caso uma extensão futura os implemente; não criar esses módulos agora.
HITL de alto risco é extensão opcional, sem ampliar automaticamente capacidades clínicas.

## 3. Base técnica acordada

- Python + FastAPI + pytest. Aplicação, ferramentas e testes executados em Docker Compose.
- Monólito modular com DDD e portas/adaptadores, mais worker; sem deployment obrigatório por caixa.
- Repositório único para frontend/backend/testes/migrations; módulos de negócio são pacotes
  internos, com uma release da plataforma. API e worker usam o mesmo código/artefato e versão;
  assets do chat integram a aplicação publicada. Não há serviços independentes por contexto.
- Módulos por contexto de negócio, com domínio puro, aplicação, entradas e infraestrutura criados por necessidade; composição no bootstrap.
- PostgreSQL + pgvector; Redis; documentos privados persistentes; jobs duráveis e eventos.
- Gateway de API como fronteira lógica; AI Gateway/Model Router como módulos internos.
- Frontend conversacional inspirado na experiência do ChatGPT, integrado à aplicação,
  conforme C-008; framework, transporte e renderização serão definidos em D-12.
- Provider LLM/embedding controlado em testes; integração real separada, com custo limitado.
- CI/CD do produto planejado para GitHub Actions. A CI dos contratos do harness já está definida,
  separada da futura aplicação; execução remota ainda não foi realizada nesta preparação.

Versões suportadas e dependências travadas serão registradas em CT-001. Não usar tags
flutuantes em releases. Não instalar a aplicação nem consumir APIs durante o planejamento.

LiteLLM é candidato futuro para implementar a integração de modelos atrás de uma porta
do AI Gateway. Databricks é candidato à consolidação analítica assíncrona de dados
selecionados. CT-027/CT-028 são opcionais, após CT-026 e decisões D-07/D-08; não ampliam
o aceite do MVP nem substituem PostgreSQL/pgvector/Redis. Detalhes no mapa DDD.

## 4. Fronteiras obrigatórias

1. Canal → API Gateway/BFF → Conversation → cache autorizado → Agent, se necessário.
2. Agent → Tool → API Gateway → serviço determinístico → datastore.
3. Agent → AI Gateway → Model Router → provider; credenciais não chegam à LLM.
4. Upload → quarentena/segurança → chunks → embeddings → publicação completa no pgvector.
5. PostgreSQL é source of truth; Redis não decide a validade final de uma reserva.
6. Tools não recebem SQL, shell ou URL arbitrária e não acessam bancos diretamente.

Módulos podem chamar-se no mesmo processo, mas sem contornar autenticação, autorização,
schema, quota e auditoria. HTTP/BFF adapta entrada; serviços contêm regras de negócio.
Domínio/aplicação não dependem de adapters. Outros módulos usam contratos públicos,
identificadores e DTOs mínimos; o compartilhamento do banco não libera SQL cruzado.

## 5. Requisitos funcionais

| ID | Requisito e resultado verificável |
| --- | --- |
| RF-01 | Autenticar atores e resolver tenantId/clinicId/paciente a partir de credenciais/mapeamento confiáveis. Negar acesso cruzado e campos de identidade propostos pelo modelo. |
| RF-02 | Consultar especialidades/profissionais e horários autorizados no PostgreSQL; disponibilidade exibida não equivale a reserva. |
| RF-03 | Criar consulta após intenção confirmada, idempotencyKey e revalidação transacional. Confirmar sucesso somente após commit. |
| RF-04 | Cancelar consulta autorizada idempotentemente, liberando capacidade e emitindo evento durável. |
| RF-05 | Reagendar atomicamente: reservar novo/liberar antigo na mesma transação; conflito mantém a reserva original. |
| RF-06 | getPatientData retorna somente campos permitidos do paciente autorizado e da finalidade. |
| RF-07 | Conversation conserva contexto recente, intenção, parâmetros coletados e etapa do workflow em state temporário autorizado, com TTL por finalidade, versão e recuperação segura conforme a seção 7. Web permite percorrer o fluxo real. |
| RF-08 | Agent usa tools de negócio com schemas: searchClinicKnowledge, findProfessionals, getAvailableSlots, getPatientData, create/cancel/updateAppointment. Backend controla execução. |
| RF-09 | Upload autorizado, validação de formato/tamanho, malware scan, extração segura, sanitização/classificação e quarentena antes de embeddings. Rejeitados não são indexados. |
| RF-10 | Ingestão assíncrona idempotente e versionada; RAG gera embedding da pergunta e busca autorizada no pgvector com Top-K limitado e fontes. Sem chunking da pergunta. |
| RF-11 | Cache de respostas antes do Agent: hit autorizado evita Agent/RAG/LLM. Separar respostas pessoais e compartilhadas não pessoais e invalidar/versionar quando necessário. |
| RF-12 | WhatsApp valida origem/assinatura, resolve identidade, deduplica e persiste inbox/evento atomicamente antes do ACK. Processamento/outbound recuperáveis e assíncronos. |
| RF-13 | AI Gateway controla rotas, credenciais, timeout, retry limitado, backoff/jitter, circuit breaker, accounting e fallback previamente avaliado. |
| RF-14 | Eventos de operações relevantes alimentam auditoria e notificações recuperáveis após commit, sem exigir conversas completas. |
| RF-15 | Extensão opcional: HITL para ação de alto risco definida, vinculada a tenant/ator/payload/prazo, com revalidação na execução. Não bloqueia o MVP administrativo. |

A experiência Web de RF-07 é detalhada em
[C-008](docs/jira-pessoal/historias/C-008-chat-web.md): navegação recolhível por sessões
recentes válidas, Nova conversa, mensagens centrais, compositor multilinha, estados reais
de execução, confirmação explícita e uso responsivo/acessível. Semelhança com ChatGPT
orienta a interação, com identidade visual da plataforma. Não aprova histórico permanente,
anexos de paciente, voz, seletor de modelos ou replay/regeneração de ações implicitamente.
Controles de identidade, TTL, consumo e idempotência permanecem no backend. Fontes do RAG
entram quando C-009 estiver integrada, mantendo a demonstração M3 honesta sobre seus módulos.

## 6. Invariantes e requisitos não funcionais

| ID | Obrigação verificável |
| --- | --- |
| RNF-01 | Isolamento em SQL, pgvector, Redis, sessão, cache, jobs, documentos, auditoria e FinOps; testes negativos com IDs válidos de outro tenant/paciente. |
| RNF-02 | Só uma reserva ativa por slot exclusivo. Chave idempotente inclui tenant + clínica + ator + operação + chave; payload divergente conflita; chave, efeito, resultado e evento persistem atomicamente. |
| RNF-03 | Toda chamada cara passa por rate limit, quota, concurrency e reserva atômica de budget entre instâncias, antes do provider. Redis indisponível bloqueia consumo até recuperação confiável. |
| RNF-04 | Runtime impõe maxSteps, maxLLMCalls, maxToolCalls, maxInputTokens, maxOutputTokens, maxCost, timeout e maxRetries. Retries/fallbacks/embeddings contam; LLM não pode ampliar limites. |
| RNF-05 | Documentos e resultados externos são dados não confiáveis, nunca instruções/autorização. Segurança continua determinística mesmo sob prompt injection. |
| RNF-06 | Timeout/deadline total e retries coordenados; retry de write exige idempotência. Jobs têm backoff/jitter, tentativas limitadas, DLQ e reprocessamento controlado. |
| RNF-07 | Logs, métricas/traces de latência, erros, throughput, cache hit ratio, provider/model, prompt version, tokens/custo, chamadas, passos, chunks/scores, retries/fallbacks e evals. Sem texto sensível indiscriminado ou labels de alta cardinalidade. |
| RNF-08 | Auditoria mínima: actor, tenant, paciente/recurso, ação, resultado, timestamp, correlationId. Minimização, finalidade, retenção/exclusão, menor privilégio; criptografia recuperável, TLS, gestão/rotação de chaves e KMS antes de dados reais. Hash não é criptografia reversível. |
| RNF-09 | Evals versionadas cobrem tools/argumentos, groundedness, hallucination, retrieval relevance, trajetória, segurança, custo, latência e fallback. Combinar determinísticos, judge calibrado e revisão humana quando necessários. |
| RNF-10 | Estado externo e escala horizontal por réplicas da API completa atrás de balanceamento, com os módulos Webhook/Conversation/Agent/Scheduling/Knowledge juntos; worker do mesmo artefato pode escalar por jobs. Limites globais, sessões ordenadas e pools limitados. Extração de serviços exige decisão/replanejamento aprovados. |
| RNF-11 | Ambiente isolado e reproduzível: Docker, migrations, fixtures sintéticas, namespaces/bancos de teste independentes, cleanup restrito ao ambiente de teste e sem apagar volumes de desenvolvimento. |
| RNF-12 | BDD antes da implementação; TDD Red → Green → revisão de coesão/refatoração pertinente → regressão. Testes por impacto e evidências executadas; sem percentual arbitrário de cobertura. |
| RNF-13 | CI em PR com testes e análise; release imutável; CD controlado com secrets por ambiente, smoke e rollback. Não publicar nem assumir infraestrutura configurada por existir um documento. |
| RNF-14 | DDD modular conforme mapa de contextos; domínio puro, aplicação orientada por portas e composição externa. Tabelas/migrations com dono, contratos públicos entre módulos e verificação de dependências conforme módulos surgirem. Preservar transações críticas e simplicidade. |

## 7. Dados e contratos mínimos

- Tenant, clínica, ator e vínculo autorizado com paciente; catálogo de profissionais e slots.
- Appointment: tenant/clínica/paciente/profissional/slot, estado e versão de concorrência.
- Idempotency record: escopo, chave, hash do payload, estado e resultado recuperável.
- Evento/outbox, inbox de canal e job: identificador estável, escopo, estado, tentativas e lease.
- Documento/versão/chunk: tenantId, clinicId, patientId quando aplicável, visibility,
  documentType, permissions, status, documentId, version, createdAt, chunkId e referência original.
- Usage ledger: reserva, tentativas, estimativa, uso confirmado/incerto e reconciliação.

Não existe promessa de exactly-once para sistemas externos. Deduplicar efeitos locais;
quando o destino não permitir confirmar um envio ambíguo, registrar incerteza e reconciliar.

### Redis

Namespace obrigatório de tenant + clínica antes destas chaves conceituais:

| Chave | Conteúdo | Política |
| --- | --- | --- |
| session:{actorId}:{sessionId} | Contexto recente, intenção, parâmetros coletados e etapa do workflow. | TTL por finalidade; vínculo de ator/sessão validado. |
| answer-cache:{patientId}:{questionHash} | Resposta do mesmo paciente. | Autorização em cada hit; TTL próprio. |
| shared-answer-cache:{clinicId}:{questionHash} | Resposta sem conteúdo pessoal. | Contexto/permissões/versão compatíveis. |
| usage:{patientId} | Requests, LLM/RAG/tools, tokens input/output e custo. | Quota por janela independente da sessão. |

Cache inclui contexto, permissões e versões; não reaproveitar confirmação de escrita como FAQ.
Cache de agenda, se habilitado, tem TTL curto e invalidação recuperável em create/cancel/update.

### State temporário de agentes e conversas — detalhamento de RF-07

Redis já foi escolhido para estado temporário compartilhado. Seu uso aqui complementa
RF-07 e RNF-01/03/04/08/10; não cria histórico permanente, memória de longo prazo,
novo workflow de negócio ou requisito de retomada integral após perda do armazenamento.

**Responsabilidades e conteúdo.** `conversations` possui o state por sessão: janela
limitada de mensagens/contexto recente, intenção atual, parâmetros validados e ainda
faltantes, etapa de execução, versão do registro e referências mínimas de execução/tool.
O contexto inclui o vínculo confiável de tenant/clínica/ator/sessão e, quando necessário,
paciente autorizado; ator e paciente não são identidades intercambiáveis. Registrar
instantes de criação/atividade/expiração e versão do formato para validar a leitura.
Confirmação fica vinculada à intenção e aos parâmetros atuais: alterá-los exige nova
confirmação; o texto de uma mensagem ou resumo não representa autorização.

| Classe | Dono / armazenamento | Expiração e fonte de verdade |
| --- | --- | --- |
| State de conversação e execução | `conversations`, Redis. Snapshot temporário da etapa e referências, separado do cache. | TTL de conversa/execução conforme política; perda não apaga efeitos oficiais. |
| Cache de respostas | `conversations`, Redis; entradas pessoais e compartilhadas elegíveis separadas. | TTL próprio e invalidação por contexto/permissões/versão. Não restaura intenção nem confirmação. |
| Consumo, quotas e reservas | `consumption`: Redis coordena contadores; PostgreSQL mantém ledger recuperável. | Janela de quota e reconciliação próprias; expirar state/cache não limpa saldo, uso ou custo incerto. |
| Operações de negócio e entrega | Contexto de domínio/delivery, PostgreSQL. | Reservas, idempotência, inbox/outbox e resultados seguem retenção transacional; nunca dependem do TTL da conversa. |

Métricas agregadas de observabilidade são derivadas e não autorizam consumo: atraso ou
perda de telemetria não pode renovar quota nem substituir contadores/ledger de controle.

**TTL e retenção.** TTLs são configuráveis pelo backend por finalidade: contexto da
conversa, snapshot de execução, lease de concorrência e cada classe de cache/controle.
Não presumir que tenham a mesma duração. D-09 definirá valores, limites de tamanho/número
de mensagens, expiração fixa ou por inatividade, eventos que renovam TTL e limite máximo
de retenção. Se houver renovação por inatividade, ela respeita esse teto. Leituras passivas,
polling, mensagens rejeitadas e tarefas de manutenção não mantêm dados indefinidamente.
Cliente/LLM não escolhem TTL ou removem a expiração. Escrita/atualização e política de
expiração devem ser consistentes atomicamente, inclusive na substituição de um registro.
Expiração é verificada antes de usar/atualizar state; não depender de notificação de chave
expirada para impedir execução. A política deve distinguir remoção do dado ativo de
retenção em snapshots/backups/logs, conforme D-04; TTL não prova exclusão dessas cópias.
Se o prazo da execução terminar antes do contexto da conversa, a etapa/confirmação não
permanece executável só porque mensagens recentes ainda estão disponíveis.

**Identidade e segurança.** Todas as operações derivam tenant/clínica/ator de autenticação
validada e verificam o vínculo com a sessão e a permissão atual para o recurso/paciente.
Sessão de conversa é diferente da sessão/credencial de autenticação. Conhecer `sessionId`
ou um prefixo Redis não concede acesso, nem permite enumerar outras sessões. Cache e
state não funcionam como prova de acesso anterior: revogação de permissão impede leitura,
retomada e nova ação, mesmo antes do TTL. Sessões de usuários distintos ou duas sessões
do mesmo usuário não herdam parâmetros/intenções entre si; compartilhamento entre canais
ou retomada entre identidades não é autorizado implicitamente pelo uso do mesmo número.

Persistir só dados necessários à próxima etapa, preferindo referências autorizadas a
cópias de cadastro, documentos e resultados completos de tools. Campos textuais são
dados não confiáveis, com formato/tamanho limitados; state incompatível ou inválido não
é executado nem desserializado como objeto arbitrário. Não guardar secrets/tokens de
autenticação/provider nem raciocínio interno do modelo. Logs/traces registram metadados
mínimos de expiração/conflito/recuperação, sem dumps de state. Acesso ao Redis é do backend,
com menor privilégio e transporte protegido conforme o ambiente, mantendo os gates de CT-024.

**Concorrência e ciclo de vida.** Atualizações têm versão esperada e uma ordem verificável
por sessão entre instâncias. D-11 escolherá serialização ou atualização condicional com
tratamento explícito de conflito; nenhuma escrita pode perder alterações silenciosamente.
Mensagem duplicada não avança duas vezes a mesma intenção. Lease, se adotado, tem posse
e prazo limitados, sem lock indefinido durante LLM/tool; o detentor antigo não pode liberar
posse alheia, sobrescrever versão nova ou ressuscitar sessão encerrada/expirada. Resultado
tardio revalida validade/versão/posse e autorização antes de avançar state ou propor novo
efeito. Expiração/cancelamento não desfaz um commit de negócio já ocorrido.

**Reinicialização e checkpoints.** Reiniciar uma instância com Redis saudável permite
continuar uma sessão válida por outra instância, usando o último snapshot consistente.
Retomada valida formato, prazo, autorização, versão e resultado da etapa interrompida.
Uma etapa em andamento não equivale a concluída; resposta perdida de tool com escrita é
reconciliada pelo serviço/idempotência no PostgreSQL, com a mesma intenção/chave. Consumo
conhecido/incerto e os tetos da execução não são zerados para repetir uma chamada.
Sem evidência suficiente para continuar, interromper a execução e informar o limite,
sem replay cego. Checkpoint temporário é esse snapshot mínimo; não exige engine ou SDK.

Perda/eviction de uma sessão ou expiração exige informar ausência de contexto e recolher
somente parâmetros necessários, com nova confirmação para uma nova intenção. State ausente
não vira uma sessão vazia reutilizando confirmação antiga; cache/log/inbox não são cópias
automáticas para reconstruir toda a conversa. Sessão perdida/expirada não autoriza repetir
efeito: resultados já comitados continuam consultáveis pelo contrato autorizado existente.
Se a referência da intenção também foi perdida e o resultado é desconhecido, não criar
automaticamente outra chave para tentar de novo; primeiro orientar a consulta autorizada
do resultado/agenda existente. Uma nova reserva exige uma nova intenção explícita.
Redis indisponível impede progressão que dependa de state e bloqueia operações caras até
recuperar controles confiáveis; não fazer fallback para memória permissiva da instância.

D-10 definirá se algum workflow precisa de checkpoint durável adicional no PostgreSQL,
quais campos/etapas, retenção e perda de contexto aceitável. Isso não está aprovado como
persistência obrigatória da conversa. RDB/AOF e restauração não garantem sozinhos ausência
de perda nem validade do snapshot: ao restaurar, revalidar expiração, revogação e referências
transacionais; state antigo não renova confirmações ou orçamento. Nenhum checkpoint pode
ser a única fonte de resultados de reserva, idempotência ou registros de consumo.

Critérios e cenários verificáveis ficam nas histórias existentes C-007, CT-006/008/014,
CT-020/021/022 e nos canais C-008/C-010; a [estratégia de testes](docs/spec-driven-development/testes.md#state-temporário-rf-07)
liga esses casos às provas esperadas. Sem valores/política definidos, D-09/10/11 não são PASS.
Referências técnicas de suporte: [expiração Redis](https://redis.io/docs/latest/commands/expire/),
[concorrência/transações Redis](https://redis.io/docs/latest/develop/using-commands/transactions/)
e [persistência e seus trade-offs](https://redis.io/docs/latest/management/persistence/).

### Contratos de API

CT-005 e cada história funcional definem contratos HTTP/OpenAPI antes da implementação:
entrada, saída, autorização por recurso, Idempotency-Key quando houver efeito e erros estáveis.
Sem credenciais no payload de tools. Prever AUTH_REQUIRED, ACCESS_DENIED, VALIDATION_ERROR,
IDEMPOTENCY_CONFLICT, SLOT_ALREADY_TAKEN, LIMIT_EXCEEDED e DEPENDENCY_UNAVAILABLE.
O mapeamento HTTP será fixado nos contratos; não confundir resposta indisponível com sucesso.

## 8. Concorrência e recuperação

Slots fixos e exclusivos são o primeiro recorte. Usar integridade no PostgreSQL e operação
atômica; SELECT FOR UPDATE somente quando existe linha a bloquear. Intervalos variáveis
exigem proteção contra sobreposição antes de habilitá-los. Tempo em UTC e timezone IANA da clínica.

Persistir alteração + resultado idempotente + evento durável juntos. Publicação posterior
é reconciliável. Falha após commit não permite criar nova intenção para encobrir resposta perdida.
Jobs usam posse/lease e atualização condicionada para impedir publicação por worker obsoleto.
Versão parcial nunca entra na busca; ativação não pode ressuscitar revisão revogada ou substituída.

Reservar orçamento máximo aplicável e reconciliar consumo real. Timeout não prova custo zero;
não liberar reserva incerta só porque o lease expirou. Após perda de Redis, restaurar limites
e reservas do estado durável antes de reabrir chamadas caras. Não substituir controle global
por contador local. Nenhuma chave de provider é necessária para o modo determinístico.

## 9. Marcos e demonstrações

| Marco | Resultado | Estado atual |
| --- | --- | --- |
| M1 — fundação | Compose, harness e CI mínima reproduzíveis. | Planejado |
| M2 — domínio | Paciente, catálogo e agenda seguros sem LLM, com testes concorrentes. | Planejado |
| M3 — conversa | Runtime limitado, tools e Web com provider controlado. | Planejado |
| M4 — conhecimento | Documentos reais sintéticos no pgvector, cache e evals offline. | Planejado |
| M5 — canais e qualidade | Providers configuráveis, WhatsApp de teste e segurança operacional. | Planejado |
| M6 — operação | Falhas, escala, backup/restore, release e ensaio de CD. | Planejado |

Modo controlado prova integração da aplicação com provider determinístico, não qualidade
de um LLM real. CT-018 exige provider/credenciais/autorização de custo para evidência real;
sem isso, sua validação externa fica pendente e a história não é Done.
Um marco local pode ser demonstrado antes da integração externa, sem alegar produção pronta.

## 10. Critério global de aceite

Os seis fluxos da aba 09 devem ter testes por HTTP/processos reais e evidência persistida:

1. FAQ miss: Redis → Agent → Tool/Gateway/Knowledge → embedding/pgvector → LLM → Redis.
2. FAQ hit autorizado: nenhuma nova chamada a Agent/RAG/LLM; request ainda contabilizado.
3. Agenda: tool → gateway → Scheduling → PostgreSQL; disponibilidade não confirma reserva.
4. Reserva: intenção + idempotência + concorrência + transação + audit/eventos recuperáveis.
5. Provider indisponível: gateway aplica fallback avaliado dentro do budget/deadline ou degradação.
6. Abuso: gateway/runtime bloqueiam antes da operação cara, inclusive com múltiplas instâncias.

Também provar: isolamento de tenant/paciente, 100 tentativas em um slot → 1 sucesso/99 conflitos,
retry após commit sem duplicação, reagendamento atômico, Redis fora, ingestão parcial invisível,
documento malicioso sem capacidade extra e restauração de backup em ambiente descartável.
Os 100 concorrentes são um teste de integridade, não uma meta de capacidade em produção.

Latência p95, throughput sustentável, disponibilidade, RPO/RTO, frescor e orçamento de produção
dependem de medição e do ambiente escolhido. CT-020/CT-021/CT-024 registram baselines e metas
antes da homologação; número não definido não pode ser declarado atendido.

## 11. Próximo passo

Cada história solicitada usa branch com ID, execução GPT-6 Astra/medium, revisão independente
GPT-6 Sol, CI no SHA e PR didático. O usuário revisa e faz merge; o agente não faz merge nem
ativa auto-merge. A história permanece Review até aceite/merge e prova final. Fluxo e limites:
[entrega por história](.agents/rules/story-delivery.md). CI mínima começa em CT-001, testes
entram em CT-002 e a consolidação em CT-003; CD continua progressivo, com destino autorizado.

Executar a primeira história elegível do [Kanban](docs/jira-pessoal/KANBAN-OFICIAL.md),
começando por CT-001, quando o usuário solicitar implementação. Esta preparação não inicia código da aplicação,
contêineres, workflows remotos, contas, deploy ou chamadas pagas.
