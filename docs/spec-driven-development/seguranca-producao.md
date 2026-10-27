# Segurança, autorização e resiliência — revisão SDD

Estado: requisitos de especificação, sem implementação ou prova de conformidade/produção.
Complementa [spec](../../spec.md), [mapa DDD](arquitetura-ddd.md) e
[decisões](decisoes.md); critérios executáveis continuam nas histórias do Kanban único.
Preserva monólito modular, API/worker do mesmo artefato, PostgreSQL/pgvector e Redis.
Não cria portais profissionais, prontuário, novo serviço de políticas ou infraestrutura.

## Cobertura encontrada e lacunas

“Contemplado” nesta tabela significa descrito, não implementado ou testado.
Fontes analisadas: spec, arquitetura, decisões, estratégia de testes e histórias
CT-005/006/008–014/016/017/020–024 e C-001/007–011. Não há PRD versionado separado.

| Tema | Cobertura anterior | Lacuna / refinamento proporcional |
| --- | --- | --- |
| Autenticação e autorização | Parcial: credencial verificável, paciente/operador e vínculos de recurso. | Matriz de capacidades por papel/contexto ainda não definida; detalhar candidatos e negação padrão em CT-005/D-13. |
| Isolamento | Contemplado: tenant/clínica/paciente em serviços, SQL, retrieval, state e cache. | Aplicar a mesma política em delegação, mudança de perfil, tarefas atrasadas e retorno de fontes; manter testes positivos e negativos. |
| Ingestão | Parcial: quarentena, scanner, parser, classificação, versões e corpus sintético. | Distinguir permissão de envio, revisão, publicação, alteração/remoção e mudança de visibilidade; D-14. |
| Segurança agêntica | Contemplado: tools restritas, schemas, autorização fora da LLM e confirmação/idempotência. | Tornar explícita a mesma desconfiança de resultados de tools e conteúdo derivado; não prometer que scanner/filtro elimina prompt injection. |
| Abuso financeiro | Contemplado em execução; parcial em agregado: oito limites, ledger, quotas e Redis atômico. | Vincular teto de tenant à soma dos atores; limitar ingestão/retrieval/fila e definir alertas/backpressure em D-16. |
| Alta disponibilidade | Parcial: réplicas da API, healthchecks, retries e backup/restore. | PostgreSQL/Redis compartilhados continuam pontos de falha; estratégia por dependência, failover e metas/custo em D-03/D-05/D-15. |
| Privacidade | Parcial: minimização, criptografia, retenção, auditoria e dados sintéticos. | Validar finalidade/base aplicável, responsabilidades e condições de envio a terceiros em D-04; não tratar consentimento ou criptografia como autorização universal. |

## RF-01/RNF-01: capacidades e contexto

Negar por padrão. Uma decisão de acesso combina identidade autenticada, capacidade
explícita para ação/recurso e contexto validado: tenant, clínica, ator (`userId`/`actorId`),
paciente quando aplicável, vínculo vigente, finalidade e classificação/estado do recurso.
RBAC agrupa capacidades; regras de atributos/vínculos complementam o papel (ABAC).
Não exigir engine externa: as decisões ficam nos serviços determinísticos do monólito.

Perfis abaixo são candidatos à composição da matriz em D-13. Nome de cargo não concede
permissões; não se aprovam seis papéis separados nem todas as funcionalidades associadas.

| Perfil candidato | Responsabilidade a avaliar | Fronteira obrigatória |
| --- | --- | --- |
| Administrador da plataforma | Operação de ambiente, disponibilidade e metadados operacionais. | Não possui leitura irrestrita de pacientes/documentos médicos nem pode se conceder esse acesso pelo papel global. |
| Gestor da clínica | Operação da clínica e eventual gestão delegada de usuários, conteúdo e permissões. | Só no escopo delegado; não concede capacidade que não está autorizado a delegar. Função administrativa não implica acesso clínico. |
| Secretária/atendente | Cadastro administrativo e agenda conforme atribuição. | Não publica documentos nem acessa dados médicos pelo cargo; somente capacidades atribuídas. |
| Gestor de conhecimento | Envio/manutenção/revisão/publicação de documentos conforme atribuição. | Acesso ao conhecimento institucional não concede agenda, dados pessoais ou poder de promover a própria permissão. |
| Médico | Candidato a agenda própria e dados permitidos por vínculo assistencial válido. | Papel e vínculo, sozinhos, não aprovam finalidade/campos; prontuário/portal médico permanecem fora do MVP. |
| Paciente | Próprios dados administrativos, agenda e conhecimento autorizado. | Não acessa outro paciente, outra clínica ou política interna restrita, mesmo com IDs válidos ou prompt persuasivo. |

CT-005 escolhe apenas capacidades necessárias aos fluxos existentes e registra operações,
recursos, condições, campos retornáveis e negativas. Os demais candidatos podem ficar sem
grants. Atribuição/revogação segue caminho administrativo autorizado e auditável, sem
gerenciamento de usuários novo por inferência. Auditoria identifica a política/resultado,
com acesso restrito e sem duplicar o conteúdo sensível consultado.

API, dispatcher/tool e caso de uso usam a mesma política; listas, downloads/fontes, cache,
sessões e consumidores assíncronos também a aplicam. Tools não herdam privilégios amplos
da credencial técnica do backend. Usuário com vários vínculos seleciona escopo dentre
os autorizados, sem acesso implícito às demais clínicas do tenant. Identidade do paciente
é resolvida pelo vínculo, não por nome/número/ID fornecido pela LLM.

Revalidar permissões atuais antes de divulgar dados ou efetivar uma operação. Evento/job
carrega referências confiáveis ao solicitante/escopo, sem carregar um grant eterno.
Revogação/mudança de visibilidade invalida o acesso mesmo com cache/state ainda válidos.
Erro de autorização não revela existência, texto ou IDs internos do recurso alheio;
contrato HTTP estável será definido na história responsável, sem exigir um código único agora.

## RF-09/RF-10: publicação e retrieval seguros

Permissões são avaliadas por ação: ler original/fonte, enviar, revisar, publicar, atualizar,
remover/revogar e alterar classificação/permissões. Enviar não implica publicar. D-14
define quando revisão humana é necessária e se autor e revisor podem coincidir; não
exige quatro olhos para todo documento nem depende do HITL opcional C-011.

Separar estado de segurança/processamento (quarentena, validação, indexação) da autorização
de publicação. Só ativar versão completa, aprovada conforme política vigente e com grant
de publicação ainda válido no escopo. Job/scanner não pode ampliar visibilidade. Alterações
em ACL/versão e remoção invalidam acesso no retrieval, fontes e caches antes de servir conteúdo
revogado; versão parcial/pendente não aparece em consulta de paciente.

Rastrear actor/tenant/clínica/documento/versão, ação, decisão, resultado e tempo de envio,
revisão/publicação/remoção, sem payload documental nos eventos. Originais/versionamento
permanecem privados. Metadados vêm de contexto validado e alterações exigem autorização.

TXT/Markdown UTF-8 continuam os formatos iniciais. PDF, imagem, arquivo compactado e
outros formatos são rejeitados até ampliação explícita, parser isolado, limites e testes.
Na futura extensão PDF, texto extraído, OCR/metadados e instruções ocultas serão igualmente
não confiáveis; não habilitar formato para cumprir um exemplo de teste. Limitar bytes,
extração, chunks, tempo de parser/scanner e backlog antes de processamento caro.

Classificar conhecimento institucional de leitura permitida, interno restrito e pessoal
por finalidade/escopo. “Compartilhável” não autoriza cruzar tenants/clínicas. Conhecimento
institucional não recebe dados pessoais por conveniência; conteúdo médico real não é
admitido no laboratório. Filtros de tenant/clínica/permissões/visibilidade/paciente/versão
se aplicam na consulta vetorial, antes de trechos chegarem a contexto, logs ou resposta;
pós-filtro isolado não é barreira suficiente. O original/fonte exige autorização própria.

## RNF-05/RF-08: agente comprometido continua limitado

Documentos, trechos RAG, resultados de tools, mensagens e resumos são dados não confiáveis.
Mesmo conteúdo validado contra malware ou revisado por operador não redefine instruções,
identidades, capabilities ou limites. Instruções e dados têm origem separada, mas essa
separação textual não substitui autorização e validação junto ao efeito.

Dispatcher e serviços rejeitam tools/campos não permitidos e recursos fora do vínculo;
validam parâmetros, intenção confirmada e idempotência. Uma instrução para publicar,
exportar dados, executar SQL/shell, acessar URL arbitrária ou ignorar budget não cria
capacidade. Conteúdo da resposta passa pelas proteções do destino, inclusive UI, sem
interpretar HTML/URLs executáveis. Não expor secrets em prompts ou resultados de tools.
Sem identidade/grant/confirmacão válida, nem uma resposta plausível da LLM autoriza ação.

## RNF-03/04/06: abuso financeiro e esgotamento de recursos

Limites já aprovados continuam cumulativos: maxSteps, maxLLMCalls, maxToolCalls,
maxInputTokens, maxOutputTokens, maxCost, timeout e maxRetries. Aplicar rate/quota e
concorrência por ator e tenant e, conforme finalidade, clínica/origem/canal; prevalece
o limite mais restritivo aplicável. Novos usuários/sessões não renovam o saldo do tenant.

Reservar consumo entre instâncias antes de LLM/embeddings/tools caras; reconciliar usage
e custo incerto no ledger. Orçamento de tenant inclui todos os atores/jobs; contadores
individuais não podem permitir exceder o agregado. Sem controles confiáveis, bloquear
operações caras. Cache hit autorizado evita IA e continua sujeito ao rate limit de requests.

Top-K limita resultados, não quantidade de consultas: contabilizar e limitar buscas,
retries e operações de embedding no orçamento/quotas aplicáveis. Ingestão limita uploads,
bytes, chunks e jobs por tenant; admissão/fila não pode crescer sem limite enquanto se
espera pelo budget. Backpressure rejeita/adia explicitamente, com escopo e prazo definidos,
sem retry automático infinito nem custos escondidos em rejeições. Limites/limiares e
política de fila são D-16; não aprovar números por suposição.

CT-016 registra consumo confirmado/estimado/incerto, rejeições e tentativas/fallbacks;
define alertas para anomalias e responsável por resposta. Telemetria atrasada não substitui
enforcement. Proteção financeira atua inclusive em requests autenticados válidos; não
equivale a proteção volumétrica DDoS. Limites de payload/conexões e proteção de borda no
destino real entram em D-03/D-15 conforme risco, sem adicionar WAF/broker/CDN por padrão.

## RNF-06/07/10/13: disponibilidade e degradação

Escala replica a API completa do monólito e workers do mesmo artefato. Load balancing,
liveness e readiness orientam tráfego; duas APIs não tornam PostgreSQL/Redis disponíveis.
Backup/restore atende recuperação; não comprova failover nem disponibilidade contínua.

D-05 define jornadas críticas, metas de disponibilidade/p95, RPO/RTO e continuidade.
D-15 compara recuperação manual, redundância/failover ou serviço gerenciado por dependência
com custo e perda tolerada. Sem metas/ambiente aprovados, CT-021 relata somente medições
locais; CT-024 deixa requisitos externos pendentes. Não acrescentar cluster, multi-região,
réplica de banco ou Sentinel automaticamente.

| Dependência indisponível | Comportamento necessário |
| --- | --- |
| LLM/provider | Fallback avaliado dentro do mesmo teto/deadline ou limite explícito. APIs determinísticas existentes podem continuar se identidade, banco e controles necessários estiverem saudáveis. Chat não inventa resultado. |
| Retrieval/embedding | Não inventar política/fontes; operações determinísticas independentes podem continuar. Não rotear para conteúdo de outro escopo como fallback. |
| Redis | Bloquear progressão que depende de state e consumo caro; sem contadores locais permissivos. Após recuperação/failover, revalidar quotas, reservas incertas e snapshots antes de liberar consumo. |
| PostgreSQL | Não confirmar writes nem usar cache como agenda oficial; sem ACK de inbox quando não há persistência durável. Recuperar/reconciliar intents, outbox e ledger antes de reprocessar. |
| Fila/worker | Outbox/jobs duráveis permanecem recuperáveis no PostgreSQL, com leases, retry limitado e DLQ. Admissão respeita backlog; falha não libera publicação parcial nem apaga evento. |

Failover, quando adotado, deve ser ensaiado com resultado ambíguo: preservar integridade,
idempotência e budget mesmo se a leitura restaurada estiver atrasada. Operações que exigem
consistência não usam estado desatualizado para confirmar reserva ou recriar saldo. Alarmes
cobrem erro/latência, dependências, backlog/idade, rejeições e custo, com procedimento e
responsável de recuperação. A prova de falha inclui retorno ao serviço, não só a interrupção.

## RNF-08: governança e limites de privacidade

D-04 registra finalidade e classificação dos dados, responsáveis, base legal aplicável,
condições de autorização/consentimento quando pertinentes, retenção/exclusão e atendimento
de incidentes/direitos. A validação cabe ao responsável competente antes de dados reais;
não presumir consentimento universal ou que um papel clínico resolve a base do tratamento.

Minimizar campos na origem e antes de enviar contexto/embedding a terceiros. Verificar
destinos, retenção/uso pelo provider e condições de transferência conforme o ambiente
aprovado. Dados institucionais e pessoais têm permissões distintas em SQL, storage, índice,
state, cache, prompts e evidências. Auditabilidade não exige guardar toda a conversa.
Criptografia/TLS/KMS/rotação e mínimo privilégio são controles do ambiente; criptografar
conteúdo não autoriza sua leitura e laboratório não comprova conformidade legal.

Negativas e leituras/alterações sensíveis geram eventos mínimos com acesso restrito,
proteção contra alteração indevida e política de retenção. D-04 define tratamento de falha
de auditoria para operações sensíveis e impacto na disponibilidade; não descartar eventos
obrigatórios silenciosamente. Exclusão alcança derivados/caches e política de cópias,
preservando apenas registros com retenção aplicável, sem ressuscitar conteúdo por replay.

Referências de apoio, sem substituição da política do produto:
[autorização OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html),
[prompt injection OWASP](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html),
[disponibilidade PostgreSQL](https://www.postgresql.org/docs/current/high-availability.html)
e [orientações gerais da ANPD](https://www.gov.br/anpd/pt-br/acesso-a-informacao/perguntas-frequentes).
