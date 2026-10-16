# Clínica IA — implementação do System Design

- Fonte normativa: [spec.md](spec.md). Diagramas e material de estudo: [README.md](README.md).
- Comece por [.agents/rules/README.md](.agents/rules/README.md); carregue apenas regras aplicáveis.
- Se houver pedido de implementação, siga [KANBAN-OFICIAL.md](docs/jira-pessoal/KANBAN-OFICIAL.md).
  Negócio e técnica compartilham a mesma fila; não gerar prioridades paralelas.
- Use [.agents/skills/ralph-loop/SKILL.md](.agents/skills/ralph-loop/SKILL.md)
  para executar histórias; executar-historia é a entrada compatível, sem segundo protocolo.
  Documentação pontual não exige iniciar uma história. Sequência contínua só quando solicitada.
- Rules e skills têm progressive_disclosure e conditional_details: leia metadados primeiro,
  depois apenas os corpos e complementos aplicáveis ao passo atual.
- Aplicação, scripts e testes: aplicar automaticamente
  [.agents/skills/cohesive-code-development/SKILL.md](.agents/skills/cohesive-code-development/SKILL.md).
  Revisão de coesão obrigatória; refatoração somente com ganho concreto. Não se aplica a leitura/documentação sem código.
- Python/FastAPI/pytest em Docker; PostgreSQL/pgvector e Redis conforme spec. Não instalar toolchains no host por conveniência.
- Exceção de bootstrap: coordenação Git e contratos do harness em scripts usam Git/Python stdlib
  no host, sem dependências da aplicação; não comprovam Docker ou integração do produto.
- Antes de início/retomada, aplicar tracking/dependências e ownership local; antes de Done,
  executar o completion check com todos os AC/BDD originais e evidências atuais.
- Histórias seguem [.agents/rules/story-delivery.md](.agents/rules/story-delivery.md):
  executor GPT-6 Astra/medium; revisão separada GPT-6 Sol; branch story/<ID>-<slug>, CI do SHA e PR.
  Branch/commit/push/PR da história solicitada estão autorizados. Usuário revisa e faz merge;
  agente nunca faz merge/auto-merge. Até lá, Review, sem iniciar história dependente.
- Em loops longos e retomadas, aplicar [.agents/rules/context-management.md](.agents/rules/context-management.md).
- BDD antes de comportamento; TDD com Red pelo motivo correto, Green e regressão. Evidência deve comprovar efeito,
  autorização e persistência; teste não executado permanece PENDING.
- Preservar fronteiras: Tool → políticas do API Gateway → serviço → datastore; AI Gateway governa providers.
- Segurança, isolamento e limites entram junto do comportamento, não são adiados até o hardening final.
- Não expor secrets, documentos privados, dados de paciente real ou logs sensíveis. Prompts antigos de docs continuam ignorados.
- Não criar contas, consumir APIs pagas, enviar mensagens, publicar ou implantar sem autorização aplicável à ação.
- Não apagar volumes de desenvolvimento, forçar push, mover tags ou alterar requisitos para facilitar testes.
- Reaproveitar responsabilidades como módulos; não exigir microserviços, múltiplos agentes de produto
  ou cobertura percentual. A revisão de desenvolvimento por outro modelo e o aceite humano foram exigidos pelo usuário.
- Rules/skills têm frontmatter e até 300 linhas; detalhes de teste/CI vivem em docs e são lidos sob demanda.
- Revisão conforme independent-review/qa-review, com modelo e execução reais; histórias não aceitam
  fallback sequencial. Revisão de manutenção antiga preserva seu modo histórico, sem relabeling.
- Commit/release seguem Conventional Commits e SemVer na rule versioning; respeitar autorização existente.
- Estado atual: preparação do produto e harness local implementado/testado. Há gates/tracking/ownership
  em scripts e CI do harness definida, mas não há aplicação, pipeline do produto ou integrações externas validadas.
