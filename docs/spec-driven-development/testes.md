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
| Web | Layout conversacional, sessões, compositor, escolha/confirmação, respostas/erros, reconexão, responsividade, teclado/foco e renderização segura. | Navegador contra API real; escolher stack/automação em D-12/C-008, sem exigir framework específico. |
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

## Determinístico e probabilístico: responsabilidades de teste

| Camada / responsáveis | BDD/TDD e prova futura |
| --- | --- |
| Domínio/API — CT-005/006/008, C-001–C-006 | Cenários positivos, negativos e fronteiras viram funcionais HTTP antes do comportamento, com Red válido, Green e regressão. Regras puras têm unitários úteis; adapters usam PostgreSQL/Redis reais. Conferir resposta, autorização, ausência/presença de efeito e registros por leitura independente. |
| Dispatcher/runtime — CT-010, C-007 | Provider controlado propõe tool inválida, identidade adulterada, chamada duplicada, loop, erro e timeout. Os controles determinísticos devem bloquear efeito indevido mesmo se a proposta da LLM for maliciosa. |
| Ingestão/retrieval — CT-011–CT-013 | Integração real prova filtros, versões e publicação. Embeddings controlados provam o contrato; relevância semântica com embeddings reais é prova separada em CT-018. |
| Resposta/decisão da LLM — C-009, CT-015/018 | Casos BDD definem tarefa, fatos/fontes permitidos, comportamento esperado e proibições. Evals medem seleção/argumentos de tools, evidência, resposta e sucesso da jornada; não comparar redação exata nem exigir uma única trajetória quando alternativas são válidas. |

BDD expressa o comportamento em ambas as camadas. TDD conduz código determinístico e
avaliadores com testes repetíveis; evolução de prompt/modelo usa baseline → avaliação →
comparação por caso. Uma resposta real ocasionalmente verde não comprova regressão resolvida.
Nem todo critério precisa de teste separado nos três níveis: escolher a menor combinação
que prove o comportamento e seus consumidores, sem duplicação mecânica.

## Ambiente e dados

- Fixtures: dois tenants e ao menos três clínicas (A1/A2 no tenant A e B1 no B), pacientes
  distintos, especialidades, médicos, vínculos e slots sintéticos. Corpus com ao menos nove
  documentos conforme a [spec](../../spec.md#corpus-documental-sintético-para-ingestão-e-rag).
- Perguntas equivalentes com políticas divergentes e fontes esperadas por clínica detectam
  contaminação. Incluir política interna restrita, operador permitido, paciente negado,
  ausência de evidência e substituição de versão; comparar IDs/fontes/fatos além do texto.
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

CT-010/CT-017 exercitam a [fronteira comum de erros](../../spec.md#execução-de-tools-e-tratamento-de-erros):
duas tools distintas sob a mesma política, saída sanitizada no dispatcher/HTTP, falhas
permanentes sem retry, cancelamento/deadline e tentativa transitória sem multiplicação.
Injetar falha depois do commit e conferir reserva/evento/resultado por leitura independente;
retomada conserva chave/hash e autorização. Banco indisponível para reconciliação mantém
resultado incerto. Testar chave divergente e chamadas simultâneas conforme RNF-02;
nenhuma dessas provas é satisfeita apenas por mock do handler ou pelo texto da LLM.

## State temporário (RF-07)

Detalhamento normativo na [spec](../../spec.md#state-temporário-de-agentes-e-conversas--detalhamento-de-rf-07).
Casos abaixo são provas futuras, com parâmetros sintéticos declarados no plano. Valores
de TTL/volume e garantias pendentes vêm de D-09/D-10/D-11, não de defaults inventados no teste.

| Caso / histórias responsáveis | Resultado verificável |
| --- | --- |
| Prazo e atualização — CT-006/C-007 | Antes/no limite/depois do prazo: acesso conforme política; atualização mantém expiração, leitura passiva não prolonga retenção e LLM/cliente não altera TTL. |
| Classes separadas — CT-006/008/014 | Expirar state preserva quota/ledger/cache ainda válido; expirar cache preserva state. Hit não restaura confirmação perdida nem executa reserva. |
| Escopo — C-007/CT-020 | Dois tenants, duas clínicas do mesmo tenant, dois atores e duas sessões do mesmo ator: IDs válidos cruzados não leem nem alteram conteúdo; parâmetros não migram entre sessões. |
| Permissão atual — C-007/CT-020 | Credencial inválida ou vínculo revogado impede retomada antes do TTL; identificador não revela conteúdo nem enumera sessões. |
| Restart — C-007/CT-022 | Encerrar a API e continuar em outra instância com Redis saudável preserva snapshot válido, parâmetros e etapa, com limites originais. |
| Concorrência — C-007/CT-022 | Barreira entre duas atualizações e mensagem duplicada: versão/conflito explícitos; resultado obsoleto não perde escolhas, recria sessão nem repete efeito. |
| Expiração durante chamada — C-007/CT-022 | Provider controlado responde após expiração/perda de posse: state não é ressuscitado e não há nova tool autorizada pelo resultado tardio. |
| Falha após commit — C-007/CT-021 | Interromper entre commit da tool e atualização do state: mesma intenção/chave reconcilia resultado com uma reserva/evento; ausência da referência não autoriza retry com chave nova. |
| Ausência/perda de Redis — CT-008/021 | State ausente solicita contexto mínimo; Redis indisponível não vira memória local permissiva; perda de controles mantém chamadas caras bloqueadas até recuperação confiável. |
| Snapshot antigo — CT-021 | Registro com prazo vencido, permissão revogada ou formato incompatível é recusado; não renova saldo nem confirmações. |
| Minimização e retenção — C-007/CT-020 | Dados acima do limite são tratados sem execução; markers sintéticos sensíveis/segredos não aparecem em state proibido ou logs; remoção e cópias seguem política declarada. |
| Canais — C-008/C-010 | Interface distingue autenticação de contexto expirado; replay/mensagem atrasada não reconstitui intenção do cache ou da inbox. |

Usar relógio controlável para regras temporais e verificar TTL real no adapter Redis em
integração. Falhas/restarts ocorrem apenas em ambiente de teste isolado. Inspecionar
PostgreSQL e contagem de chamadas independentemente do texto retornado pela conversa.
Não exigir checkpoints duráveis como condição de teste antes da decisão D-10; a prova
deve corresponder à garantia explicitamente escolhida, incluindo perda segura de contexto.

## Evals e uso de modelos

Começar com o menor dataset que cubra os cenários obrigatórios e A1/A2/B1, registrando
quantidade e motivo de cada caso. Controle determinístico não exige judge. Comparações
com modelo/judge real usam seleção por impacto, limite de chamadas/tokens/custo e parada
definidos antes da execução; CI habitual não chama inferência paga. Reutilizar embeddings
de documentos inalterados com identidade de conteúdo/modelo/versão e escopo autorizados,
sem reutilizar índice incompatível. Não repetir avaliações caras para mudança só documental.

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

### Protocolo mínimo de avaliação do produto

Este protocolo avalia o assistente da clínica; [evals do harness](evals-harness.md)
avaliam o agente de desenvolvimento e não substituem essas provas.

1. **Casos antes do ajuste:** registrar ID, requisito/BDD, tenant/ator, mensagens e
   contexto inicial, fontes/versões, fatos obrigatórios, ação esperada e efeitos proibidos.
   Incluir conversa de múltiplos turnos, correção de parâmetros, pedido ambíguo que exige
   esclarecimento, ausência de evidência e tentativas de injeção. Manter pequeno conjunto
   de aceitação separado dos exemplos usados para ajustar o prompt; registrar sua exposição
   ou alteração, sem selecionar só casos favoráveis depois de observar resultados.
2. **Isolar causas:** avaliar retrieval por fontes/documentos relevantes esperados no
   Top-K (cobertura/recall@K e proporção relevante/precision@K quando rotulado), separando
   esses scores do isolamento obrigatório. Avaliar geração também com contexto autorizado
   fixo, e depois a jornada RAG completa. Citação existente não comprova suporte: verificar
   se os fatos da resposta são sustentados pelas fontes, com rubrica/humano quando necessário.
3. **Decisão e efeito:** avaliar tool e argumentos semanticamente, ausência de tool quando
   cabível, confirmação/esclarecimento antes da escrita e resultado persistido. Medir
   sucesso por tarefa, afirmações sem suporte, reconhecimento de limite, latência e custo.
   Segurança/integridade são assertions próprias; média de qualidade nunca as compensa.
4. **Comparação real limitada:** registrar baseline/candidato, configurações de geração,
   revisões de prompt/tools/retriever/índice, casos e repetições planejadas por risco e teto
   financeiro. Mesmos casos e condições comparáveis; declarar cache hit/miss e comparar
   índice compatível ao trocar embeddings. Seed/temperatura registrados não prometem
   determinismo. Repetir uma amostra crítica dentro do orçamento e relatar dispersão,
   sucessos/total e falhas por caso; amostra pequena não sustenta garantia estatística.
5. **Sem verde por seleção:** guardar todas as tentativas planejadas e falhas; não repetir
   até passar. Timeout/erro de transporte é indisponibilidade, não nota zero de groundedness
   nem exclusão silenciosa: separar execução, qualidade e cobertura. Informar casos não
   executados e custo incerto. Parada por orçamento mantém a avaliação incompleta/PENDING.
6. **Critérios prévios:** CT-015 define rubricas e critérios por dimensão; CT-018 registra
   limiares numéricos e amostra antes de chamar o provider. Bloqueio determinístico ou falha
   crítica observada reprova o candidato, mesmo com nota média alta. Não alterar limiar após
   o resultado para obter aprovação. Não habilitar modelo/fallback obrigatório sem sua prova.

LLM-as-a-Judge recebe pergunta, resposta e evidências mínimas autorizadas com rubrica
versionada. Conteúdo avaliado é dado não confiável, inclusive instruções para dar nota alta.
Registrar modelo/configuração do judge, discordâncias com amostra humana e avaliações
inconclusivas; julgar a própria resposta não é validação independente. Se faltar evidência,
abster-se. O judge não substitui checagem de schema, isolamento, autorização ou persistência.

Os avaliadores também têm TDD: respostas controladas corretas/incorretas, fonte inexistente,
fato sem suporte, argumento errado e vazamento devem produzir os verdicts esperados.
Não introduzir framework de evals ou serviço SaaS obrigatório; pytest e relatórios pequenos
versionados bastam inicialmente. Relatórios reais gerados devem ser sanitizados e referenciados
por execução; não registrar prompts completos/dados privados por conveniência.

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
