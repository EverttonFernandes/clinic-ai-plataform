# Decisões da preparação

Data: 2026-10-16. Estado: baseline de implementação, com decisões externas ainda abertas.

## Acordado com o usuário

- Python + FastAPI + pytest; aplicação e testes em Docker.
- Versionar apenas o novo planejamento de docs, preservando prompts antigos ignorados.
- Preparar especificação e Kanban antes de escrever a aplicação.

## Escolhas iniciais e trade-offs

| Decisão | Problema resolvido e escolha | Alternativa / quando reconsiderar |
| --- | --- | --- |
| Monólito modular + worker | Preservar fronteiras do desenho com poucos processos. Gateways são módulos lógicos. | Extrair serviço quando carga ou isolamento operacional justificar. |
| PostgreSQL + pgvector e Redis | Manter a stack do desenho. Redis coordena estado efêmero/limites; PostgreSQL registra efeitos e consumo recuperável. | Não adicionar outro banco por conveniência. |
| Jobs/outbox no PostgreSQL inicialmente | Eventos e jobs duráveis sem um broker adicional; polling/leases e consumidores idempotentes. | RabbitMQ/SQS/Kafka apenas após medir atraso, disputa ou necessidades de entrega. Não prometer exactly-once externo. |
| Documentos em volume privado no laboratório | Exercitar referência por chave, quarentena, versão e autorização sem conta cloud. Não servir o diretório publicamente. | Object Storage externo com TLS, criptografia e política de acesso em CT-024; volume local não prova resiliência/KMS de produção. |
| Malware scan em Docker | Cumprir a validação de documentos; ClamAV é o candidato inicial. Scanner indisponível bloqueia publicação. | Adapter de scanner gerenciado somente com necessidade/credenciais; fake apenas nos testes unitários. |
| Arquivos TXT/Markdown UTF-8 primeiro | Limitar superfície de parser e permitir RAG completo com documentos sintéticos. | PDF e formatos adicionais exigem parser isolado, limites de extração e novos testes; não habilitar por extensão apenas. |
| Slots fixos, exclusivos e timezone explícito | Entregar reserva correta antes de intervalos/capacidade variável. | Intervalos requerem proteção contra sobreposição antes de disponibilizá-los. |
| Provider determinístico por padrão | CI/local sem chave, custo ou internet para inferência. Integração real é uma prova distinta. | Provider real em CT-018, com evals e teto de custo; não usar resultado fake como prova de groundedness real. |
| Web mínimo na própria aplicação | Demonstrar a jornada sem uma segunda stack de frontend. | SPA somente quando a experiência ou equipe justificar. |
| CI cedo; CD ao final | Verificar cada incremento sem esperar todo o produto. Release/CD dependem de ambiente definido. | Não copiar jobs mobile, Sonar, metas de cobertura ou publicação do WorkLink. |

O WorkLink foi referência de organização: fila cronológica, histórias separadas e evidências.
Não foi copiado como implementação nem como política de aprovação/versionamento.

## Decisões externas pendentes

| ID | Decisão necessária | Quando resolver | Efeito se ausente |
| --- | --- | --- | --- |
| D-01 | Provider/modelos LLM e embeddings, fallback, autorização de chamadas e teto financeiro. | Antes da validação real de CT-018. | Modo controlado disponível; integração real pendente, sem alegação de qualidade do modelo. |
| D-02 | Provider de WhatsApp, credenciais, assinatura e identidade verificável do paciente. | Contrato em C-010; sandbox real em CT-019. | Assinatura simulada/adapter de teste não comprovam entrega externa. |
| D-03 | Destino de homologação/produção, domínio/TLS, registry, secrets, KMS e Object Storage. | CT-024, antes de CD remoto. | Preparar contratos/artefato; deploy e proteção de dados reais permanecem pendentes. |
| D-04 | Política operacional de retenção/exclusão, perfis e finalidades. | Baseline sintética em CT-005/CT-020; validação do responsável antes de dados reais. | Nenhum dado de paciente real no laboratório. |
| D-05 | SLOs de p95, volume, disponibilidade, frescor, RPO/RTO e budget por ambiente. | Baseline em CT-021; aprovação para ambiente real em CT-024. | Relatar medições locais; não declarar SLO de produção atingido. |
| D-06 | Ação administrativa de alto risco que justifique HITL. | C-011, opcional. | Não adicionar tools clínicas sensíveis nem bloquear o MVP comum. |

Nenhuma dessas pendências impede CT-001. Resolver decisões na história responsável,
sem criar contas, enviar mensagens ou contratar serviços apenas para organizar o backlog.
