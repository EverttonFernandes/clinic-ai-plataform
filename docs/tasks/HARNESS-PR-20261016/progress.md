# Checkpoint — política de PR por história

Objetivo autorizado: preparar o harness para execução Astra/medium, revisão separada Sol,
CI e PR didático, com revisão/merge do usuário. Nenhuma história de aplicação iniciada.

Branch atual: main, com preparação local ainda sem commit/push/PR. Preservadas as mudanças
da preparação anterior. Próxima branch de produto será story/CT-001-ambiente-docker quando
o usuário solicitar a execução; não foi criada implicitamente nesta manutenção.

Executor/coordenador desta manutenção: /root, modelo exato não exposto. Revisor real:
/root/revisao_harness_pr, selecionado gpt-6-sol, somente leitura. Parecer em [revisao.md](revisao.md).
Para as histórias: gpt-6-astra/medium e gpt-6-sol, sem inferir modelos por persona.

## Evidências e correções

- Red inicial: seis testes, sete falhas observadas; revisão pelo mesmo modelo/identidade
  desconhecida/fallback/effort incorreto e ausência dos gates externos eram aceitos.
- Revisão independente rejeitou coleta sem evento, formato path@ref e bloqueio por
  revalidar história aceita contra código novo. Achados preservados no plano/parecer.
- Red path@ref: três erros corretos por workflow ausente. Red continuidade: duas falhas
  reproduziram o bloqueio da evolução e confiança indevida em merge histórico sem reconsulta.
- Green final: 60 contratos stdlib passaram em Git temporário; agente revisor também
  executou 60 testes. Receipts reais dos gates contracts/documentation em .git/harness/HARNESS-PR-20261016.
- Validação documental: links, frontmatter, limite de linhas, skills e workflow local aprovados.
- Coesão: política, coleta GitHub e validação de conclusão têm responsabilidades separadas;
  distinção entre aceite histórico e regressão atual evita reabertura indevida. Sem camadas adicionais.
- APPROVED confirmado pelo revisor com os hashes source/scope/contract do plano.

Gates do produto permanecem não executados: Docker, Application CI, provider, WhatsApp e CD.
Fixtures GitHub não são evidências remotas. As 37 histórias seguem sem started_at.

Próxima ação: usuário solicitar início de CT-001. Ler a política de entrega, conferir modelo,
branch/dependências, criar plano BDD e implementar o ambiente/CI mínima dentro dessa história.
Não fazer merge pelo agente nem executar o restante do backlog sem pedido de sequência.
