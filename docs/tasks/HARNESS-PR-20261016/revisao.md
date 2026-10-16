# Revisão independente — política de PR

Revisor: `/root/revisao_harness_pr`, selecionado explicitamente como `gpt-6-sol`,
em execução distinta e somente leitura. Effort não exposto pela ferramenta.
Executor/coordenador desta manutenção: `/root`; modelo exato da sessão não exposto.
A seleção Astra/medium aplica-se às futuras histórias; não foi presumida nesta manutenção.

## Parecer final recebido

**APPROVED** para a preparação local do harness. A correção aceita `path@ref` do GitHub,
mantém a exigência de runs `push` e `pull_request`, e preserva o aceite histórico de
CT-001 quando CT-002 evolui seu código ou os receipts locais desaparecem. A prova histórica
ainda exige PR integrado pelo usuário e commit de merge ancestral da base atual.

O revisor executou **60 testes locais, todos verdes**, incluindo base sem ancestralidade
e merge por outro ator. Nenhuma CI remota, PR real ou história CT-001 foi executado;
este parecer não os substitui. O parecer cobre o código, regras, skills e planejamento
do escopo de preparação; hashes source/scope/contract ficam em evaluation do plano.

## Achados devolvidos e corrigidos

- REJECTED: coleta por nome/SHA permitia workflow_dispatch. Separados os gates push e PR,
  com caminho/identidade do workflow e associação PR/HEAD; novos contratos negativos.
- REJECTED: igualdade literal de path não suportava o formato REST path@ref. Parser e
  fixtures ajustados; testes positivos/negativos e merge sintético vinculado ao HEAD.
- REJECTED: dependências aceitas eram rechecadas contra código atual e receipts de 24h.
  Agora usam aceite histórico, fonte/contrato/parecer, merge GitHub e ancestralidade;
  regressões atuais pertencem à história consumidora. Dois testes Red reproduziram o defeito.

Não houve aprovação pelo próprio executor nem alteração de código pelo revisor.
Não houve calibração humana de LLM-as-a-Judge; a rubrica continua preparada para essa etapa.

## Vinculação confirmada pelo revisor

O revisor recalculou e confirmou source, scope e contract via harness_completion,
mantendo APPROVED para este snapshot (sem repetir a suíte, pois não mudou o scope):

- source: `0e9d4179a221d79311c11b7cc267da55b01db07e9022f0af6d2f6550d914b266`
- scope: `b6671bdbd81d1cf08c8d5a64614a7572918076d9670e62a5b62993665767dad7`
- contract: `86d51db4905574e89b1d979a62b37fb3114089d521ecb354e2557991296f88b8`
