# Tracking de histórias

Fonte de prioridade: [Kanban](../jira-pessoal/KANBAN-OFICIAL.md). Protocolo/comandos:
[harness](../spec-driven-development/harness.md). Não manter outra fila neste diretório.

`feature_tracking.py import-kanban` cria registros sem inferir execução anterior.
JSONs guardam eventos e referências; `index.json` é regenerável, não editável manualmente.
Nenhum registro TODO significa dependências revisadas ou critério validado.

Revisar dependências antes de start; falta/ciclo/prova inválida bloqueiam a ação.
Finish exige token do proprietário e completion check atual, e não cria commit/tag/deploy.
Atualizar o Kanban depois da confirmação; divergência após interrupção exige reconciliação.

Timestamps/históricos não conhecidos não são inventados. Não guardar token, secret, dump
ou log sensível nos eventos. Logs e locks ficam na área administrativa Git, fora deste diretório.
Escrita é atômica por arquivo; registry usa writer-lock e não oferece transação multi-arquivo.
