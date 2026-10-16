# Entrega — revisão independente e PR por história

Preparação local do harness concluída. [Plano e gates](../tasks/HARNESS-PR-20261016/plano.md),
[parecer independente](../tasks/HARNESS-PR-20261016/revisao.md) e
[checkpoint](../tasks/HARNESS-PR-20261016/progress.md).

- Política: futuras histórias com Astra/medium, revisão Sol em outra execução, branch com ID,
  testes/CI, PR didático e espera pelo usuário em Review. Merge/auto-merge pelo agente proibidos.
- Gates distinguem LOCAL_READY, READY_FOR_PR e AWAITING_USER de Done. Coletor read-only
  vincula workflows push/PR aos caminhos/eventos e HEAD/PR corretos; Done exige merge do usuário.
- Aceite histórico de dependência não expira quando código evolui; conserva fonte/contrato/
  parecer e merge verificado ancestral. Regressão é validada pela história consumidora.
- Templates, regras de testes/coesão, handoff e evals atualizados. CI mínima de aplicação
  antecipada para CT-001; CT-002 amplia testes e CT-003 consolida qualidade.
- Validação: 60 contratos locais PASS, validação documental/skills PASS e revisão real
  GPT-6 Sol APPROVED após três achados corrigidos. Receipts ficam na área administrativa Git.
- Esta manutenção não presume modelo Astra para a sessão coordenadora, não executa a aplicação
  e não comprova Docker, run remoto, provider ou CD. Não houve commit/push/PR/merge desta preparação.

Todas as histórias de produto permanecem To Do/Backlog, sem início. CI do harness definida
não substitui Application CI. Riscos residuais: metadata de modelo e uso humano de token são
cooperantes; proteções remotas não foram configuradas. Critérios desta preparação atendidos;
integrações reais serão demonstradas nas histórias correspondentes.
