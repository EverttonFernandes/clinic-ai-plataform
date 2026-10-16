# Estratégia de BDD, TDD e evidências

Estado: estratégia planejada. Não existem suítes de aplicação implementadas nesta preparação.
Fonte normativa: [spec](../../spec.md). Execução: [Kanban](../jira-pessoal/KANBAN-OFICIAL.md).

## Ciclo por história

1. Ler critérios, dependências e invariantes; registrar plano e consumidores afetados.
2. Escrever cenário BDD observável antes de código produtivo. Gherkin em Markdown é requisito,
   não um teste executado; pytest vai materializar os cenários sem exigir outro framework BDD.
3. Obter Red pelo comportamento ausente/incorreto, com ambiente saudável.
4. Implementar o menor incremento para Green. Usar unitários Red/Green quando ajudarem a isolar regra pura.
5. Revisar coesão, nomes, dependências e duplicação. Refatorar só onde há ganho; reexecutar testes afetados.
6. Complementar casos críticos, verificar consumidores e registrar comandos/revisão/resultado.

Não é Red funcional: erro de import, banco não iniciado, credencial ausente ou endpoint errado
no teste. Corrigir o setup antes de usar a falha como evidência de comportamento.

## Camadas e provas distintas

| Nível | Prova esperada | Dependências e limites |
| --- | --- | --- |
| Unitário | Regra pura: estado, intenção, limites, erro, autorização sem I/O quando separável. | Doubles focados; não testar apenas chamadas internas. |
| Integração | SQL/constraints/migrations, pgvector/filtros, Redis atômico, storage/scanner e jobs. | Serviços reais em Docker; SQLite ou dicionário não comprovam PostgreSQL/Redis. |
| Funcional HTTP | Jornada pela interface pública com autorização, resposta e efeito persistido. | API em processo separado; cliente não chama funções internas. |
| Web | Login/sessão, escolha/confirmação, respostas/erros e renderização segura. | Navegador contra API real; escolher automação em C-008 sem exigir frontend complexo. |
| Segurança | IDs cruzados, credencial adulterada, prompt injection, upload e cache pessoal. | Fixtures sintéticas; nenhuma exploração de terceiros. |
| Concorrência | Disputa de slot, chave, reagendamento, sessão, budget e posse de job. | Chamadas sobrepostas com barreira e inspeção independente do estado final. |
| Falhas/recuperação | Interrupção entre commit/publicação, Redis perdido, DLQ e backup/restore. | Somente projetos/volumes descartáveis identificados como teste. |
| Carga | p95, throughput, filas, uso, limites e recuperação após sobrecarga. | Descrever hardware, dataset, janela e taxa; laboratório não é SLA de produção. |
| Evals | Qualidade, seleção/argumentos de tools, groundedness, hallucination, retrieval relevance e trajetória. | Dataset e versões; distinguir provider controlado, real, judge e humano. |
| Arquitetura | Domínio/aplicação sem dependências externas ou adapters; acesso entre contextos apenas por contratos públicos. | Verificação de imports começa em CT-002 e cresce com módulos reais; não exige ArchUnit ou stack Java. |

O [mapa DDD](arquitetura-ddd.md) orienta os testes por contexto. Unitários exercitam
transições e invariantes; integração prova os adapters e transações reais; funcionais
percorrem os contratos públicos. Um teste de importação não comprova autorização ou reserva correta.
CT-027/CT-028 acrescentam contratos específicos: tentativas/custo com proxy, replay/checkpoint,
isolamento e reconciliação analítica; evidência local não equivale a job executado no Databricks.

Usar nomes didáticos e estrutura Given/When/Then ou Arrange/Act/Assert, com expectativas
de resultado e efeitos. Evitar testes que apenas refletem a organização do código.
Práticas de organização/importação devem seguir as [orientações do pytest](https://docs.pytest.org/en/stable/explanation/goodpractices.html).

## Ambiente e dados

- Fixtures: dois tenants, clínicas e pacientes distintos, profissionais, slots e documentos semelhantes.
- Usar banco/Redis/storage e projeto Compose de teste independentes. Cada execução possui namespace.
- Cleanup restrito aos recursos da própria execução; nunca `down -v` genérico em desenvolvimento.
- Relógio controlável para TTL/deadline/expiração; testes de concorrência não dependem apenas de sleep.
- Seeds são dados sintéticos explícitos e repetíveis; não copiar documentos privados ou pacientes reais.
- Verificar efeitos por leitura independente ao banco ou interface autorizada de auditoria; não inferir persistência pelo texto da resposta.

## Casos mínimos da V2

| Comportamento | Assertion material |
| --- | --- |
| 100 intenções por um slot exclusivo | 1 sucesso, 99 conflitos de domínio, 1 reserva ativa. |
| Retry após commit e resposta perdida | Mesma chave/hash retorna resultado; sem segunda reserva/evento. |
| Payload divergente na mesma chave | Conflito sem substituir resultado anterior. |
| Reagendamento em conflito | Horário anterior preservado; nenhuma ocupação parcial. |
| Dedupe de webhook | Inbox + dedupe antes do ACK; replay não executa novamente a intenção. |
| FAQ hit autorizado | Zero novas chamadas de Agent/RAG/LLM; request contabilizado. |
| Cache/contexto cruzado | Mesmo texto/ID não expõe conteúdo pessoal ou de outro tenant. |
| Budget concorrente | Reservas totais não excedem saldo; retries/fallbacks/embeddings contabilizados. |
| Redis fora/perdido | Nenhuma nova operação cara até recuperação confiável, inclusive reservas incertas. |
| Documento malicioso/rejeitado | Sem embeddings para arquivo não validado; RAG não autoriza tool. |
| Worker atrasado/versão revogada | Job obsoleto não publica nem ressuscita conteúdo. |
| Falha após commit | Audit/invalidação/notificação recuperados sem repetir efeito de negócio. |

## Evals e uso de modelos

Dataset versionado por caso, expectativa, fonte autorizada e rubrica; registrar prompt/model/provider,
schemas, retrieval, documento/índice e configuração do runtime. Incluir ferramentas erradas,
argumentos inválidos, ausência de evidência, instruções adversariais e fallbacks.

Determinísticos validam segurança/integridade e seleção esperada; judge pode avaliar resposta
quando calibrado com revisão humana. Nota média não compensa vazamento ou efeito não autorizado.
Definir critérios de liberação antes da comparação; nunca reduzi-los depois para aprovar um modelo.

Provider controlado é o padrão local/CI e prova orquestração/contrato. Similaridade de vetores
de teste não prova relevância de um modelo real. CT-018 executa avaliação real autorizada,
com teto financeiro, dados sintéticos e fallback especificamente avaliado antes de habilitar.
Judge remoto também é chamada paga sujeita aos mesmos controles e autorização.

## Seleção por impacto

- Documento: conteúdo, links, referências, rastreabilidade e regras de ignore.
- Regra pura: unitários e consumidores da regra; funcional da jornada afetada.
- Serviço/contrato: integração e funcionais dos consumidores, tools e canais afetados.
- Schema/tenant/idempotência/budget: regressão transversal, segurança e concorrência correspondentes.
- Runtime/modelo/retrieval: dataset relevante, tools, limites, custo e falhas.
- Release e integração final: matriz completa aplicável, migrations, build/smoke e gates externos reais.

Não rodar toda a matriz em cada alteração pequena. Falha, impacto desconhecido ou mudança
transversal justifica ampliar. Cobertura auxilia inspeção; não há meta percentual artificial.

## Registro de evidência

Usar [tarefa](../tasks/TEMPLATE.md) e [entrega](../entregas/TEMPLATE.md).
PASS = executado com sucesso na revisão registrada; FAIL = execução reprovada;
PENDING = não executado/faltam insumos; N/A = não aplicável, com justificativa.
Não marcar uma história Done com gate obrigatório PENDING, nem apresentar screenshots como
substituição de prova de integridade ou integração externa.
