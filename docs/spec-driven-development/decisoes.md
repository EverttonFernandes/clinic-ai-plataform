# Decisões da preparação

Data: 2026-10-16. Estado: baseline de implementação, com decisões externas ainda abertas.

## Acordado com o usuário

- Python + FastAPI + pytest; aplicação e testes em Docker.
- Versionar apenas o novo planejamento de docs, preservando prompts antigos ignorados.
- Preparar especificação e Kanban antes de escrever a aplicação.
- Manter o README da raiz como guia completo do System Design e ponto de partida dos estudos,
  preservando explicações, fluxos, imagens e trade-offs. Futuramente haverá outro README
  da plataforma, combinando proposta de negócio, jornadas de uso e visão técnica; ele
  complementará o material de estudo, sem substituí-lo, resumi-lo ou deslocá-lo.
- DDD com portas e adaptadores, tomando o WorkLink como referência e adaptando os módulos para Python.
- Avaliar LiteLLM e Databricks em evoluções opcionais, com evidências práticas e custo autorizado.

## Escolhas iniciais e trade-offs

| Decisão | Problema resolvido e escolha | Alternativa / quando reconsiderar |
| --- | --- | --- |
| Monólito modular + worker | Preservar fronteiras do desenho com poucos processos. Gateways são módulos lógicos. | Extrair serviço quando carga ou isolamento operacional justificar. |
| DDD por contexto, com portas/adaptadores | Domínio puro e casos de uso protegidos de frameworks; tabela/migration tem dono. [Mapa e contratos](arquitetura-ddd.md). | Criar camadas e abstrações apenas ao implementar comportamento; não copiar classes/pacotes Java. |
| PostgreSQL + pgvector e Redis | Manter a stack do desenho. Redis coordena estado efêmero/limites; PostgreSQL registra efeitos e consumo recuperável. | Não adicionar outro banco por conveniência. |
| State temporário em Redis | Detalhar RF-07 nas histórias existentes: contexto/intenção/parâmetros/etapa por sessão, com expiração, versão e autorização. Separado de cache e consumo. | Sem promessa de histórico permanente ou recuperação integral após perda do Redis; checkpoints duráveis dependem de D-10. |
| Jobs/outbox no PostgreSQL inicialmente | Eventos e jobs duráveis sem um broker adicional; polling/leases e consumidores idempotentes. | RabbitMQ/SQS/Kafka apenas após medir atraso, disputa ou necessidades de entrega. Não prometer exactly-once externo. |
| Documentos em volume privado no laboratório | Exercitar referência por chave, quarentena, versão e autorização sem conta cloud. Não servir o diretório publicamente. | Object Storage externo com TLS, criptografia e política de acesso em CT-024; volume local não prova resiliência/KMS de produção. |
| Malware scan em Docker | Cumprir a validação de documentos; ClamAV é o candidato inicial. Scanner indisponível bloqueia publicação. | Adapter de scanner gerenciado somente com necessidade/credenciais; fake apenas nos testes unitários. |
| Arquivos TXT/Markdown UTF-8 primeiro | Limitar superfície de parser e permitir RAG completo com documentos sintéticos. | PDF e formatos adicionais exigem parser isolado, limites de extração e novos testes; não habilitar por extensão apenas. |
| Slots fixos, exclusivos e timezone explícito | Entregar reserva correta antes de intervalos/capacidade variável. | Intervalos requerem proteção contra sobreposição antes de disponibilizá-los. |
| Provider determinístico por padrão | CI/local sem chave, custo ou internet para inferência. Integração real é uma prova distinta. | Provider real em CT-018, com evals e teto de custo; não usar resultado fake como prova de groundedness real. |
| Web mínimo na própria aplicação | Demonstrar a jornada sem uma segunda stack de frontend. | SPA somente quando a experiência ou equipe justificar. |
| CI cedo; CD ao final | Verificar cada incremento sem esperar todo o produto. Release/CD dependem de ambiente definido. | Não copiar jobs mobile, Sonar, metas de cobertura ou publicação do WorkLink. |
| LiteLLM candidato | Adapter externo do AI Gateway; avaliar contrato, accounting, retry/fallback e isolamento em CT-027. | Contrato local/provider controlado continua válido; proxy não substitui automaticamente orçamento da plataforma. |
| Databricks candidato | Projeções analíticas Bronze/Silver/Gold de dados selecionados, fora da transação operacional, em CT-028. | Começar batch incremental; CDC/streaming apenas se justificados. PostgreSQL continua fonte operacional. |

O WorkLink foi referência de fila cronológica, histórias, evidências e separação DDD/hexagonal.
A organização foi adaptada à stack Python; a implementação e os contratos deste produto são próprios.

## Decisões externas pendentes

### Revisão do state temporário na fase SDD

Fontes revisadas: spec, mapa DDD, guia de estudo e histórias de conversa/canais,
Redis, budget, cache, privacidade, falhas e escala. A definição de produto está nessas
fontes; não foi identificado um PRD versionado separado. Nenhum novo domínio ou história
é necessário para este detalhamento.

| Já contemplado | Lacuna detalhada agora | Responsável existente |
| --- | --- | --- |
| Redis, sessão com TTL e intenção em RF-07. | Parâmetros faltantes/coletados, etapa, versão, volume limitado e renovação por finalidade. | CT-006/C-007; D-09. |
| Namespace tenant/clínica e autorização por paciente. | Vínculo explícito ator/sessão, duas sessões do mesmo ator, revogação e credencial distinta do state. | C-007/CT-020 e canais. |
| Separação de sessão, cache e quotas. | Ciclos de vida independentes e proibição de reconstruir confirmação a partir do cache. | CT-006/008/014. |
| Ordem/versão, estado externo e PostgreSQL oficial. | Restart versus perda de state, efeito incerto, resposta tardia e limites da retomada/checkpoint. | C-007/CT-021/022; D-10/D-11. |
| Minimização, retenção e exclusão. | Limites do payload, segredo em logs, expiração em execução e retenção das cópias. | C-007/CT-020; D-04/D-09. |

### Registro de decisões pendentes

| ID | Decisão necessária | Quando resolver | Efeito se ausente |
| --- | --- | --- | --- |
| D-01 | Provider/modelos LLM e embeddings, fallback, autorização de chamadas e teto financeiro. | Antes da validação real de CT-018. | Modo controlado disponível; integração real pendente, sem alegação de qualidade do modelo. |
| D-02 | Provider de WhatsApp, credenciais, assinatura e identidade verificável do paciente. | Contrato em C-010; sandbox real em CT-019. | Assinatura simulada/adapter de teste não comprovam entrega externa. |
| D-03 | Destino de homologação/produção, domínio/TLS, registry, secrets, KMS e Object Storage. | CT-024, antes de CD remoto. | Preparar contratos/artefato; deploy e proteção de dados reais permanecem pendentes. |
| D-04 | Política operacional de retenção/exclusão, perfis e finalidades. | Baseline sintética em CT-005/CT-020; validação do responsável antes de dados reais. | Nenhum dado de paciente real no laboratório. |
| D-05 | SLOs de p95, volume, disponibilidade, frescor, RPO/RTO e budget por ambiente. | Baseline em CT-021; aprovação para ambiente real em CT-024. | Relatar medições locais; não declarar SLO de produção atingido. |
| D-06 | Ação administrativa de alto risco que justifique HITL. | C-011, opcional. | Não adicionar tools clínicas sensíveis nem bloquear o MVP comum. |
| D-07 | LiteLLM: versão/licença, modo proxy, capacidades necessárias, dono de retries/fallback, contratos de usage e limites. | CT-027, opcional após CT-026. | Continuar com o adapter validado; não declarar proxy integrado. |
| D-08 | Databricks: caso analítico, workspace/cloud/recursos, datasets permitidos, governança, retenção, frescor e teto de custo. | CT-028, opcional após CT-026. | Manter desenho/contratos locais; execução Databricks e prova externa ficam pendentes. |
| D-09 | Política por finalidade: TTL fixo/inatividade, eventos de renovação, teto de retenção e limites de volume do state; relação entre contexto, execução e lease. TTL de cache/quota permanece independente. Mais continuidade retém mais dados e memória. | Base em CT-006; resolver parâmetros de conversa antes de C-007; cache em CT-014; retenção real com D-04. | Não presumir minutos/dias, histórico ilimitado ou renovar por qualquer acesso; evidência depende de política explícita e dados sintéticos. |
| D-10 | Necessidade de checkpoint durável de workflow, etapas/campos mínimos, política de retomada, perda tolerada de contexto e retenção de cópias. Comparar Redis temporário com persistência adicional; recuperação integral e replay automático não estão aprovados. | Decisão em C-007; validar falhas em CT-021, RPO/RTO com D-05 e ambiente real em CT-024. | Provar restart com state válido e comportamento seguro na perda; não criar tabela de histórico/checkpointer adicional por conveniência. Se necessário, registrar aprovação/impacto no planejamento antes de implementar. |
| D-11 | Coordenação por sessão: serialização ou escrita condicional, tratamento de conflito/duplicata, posse e prazo de lease se usado. Comparar simplicidade, contenção, duração de chamadas e backpressure. | C-007; base Redis em CT-006 e validação ampliada em CT-022. | Não prometer ordem total/exatamente uma execução nem eleger mecanismo por padrão; conflito não pode causar perda silenciosa ou repetição de efeito. |

Nenhuma dessas pendências impede CT-001. Resolver decisões na história responsável,
sem criar contas, enviar mensagens ou contratar serviços apenas para organizar o backlog.
