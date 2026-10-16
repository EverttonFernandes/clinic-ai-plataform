---
name: task-ownership
description: "Evitar escritores concorrentes na mesma tarefa em Git local compartilhado."
applies_when:
  - "assumir execução ou encontrar tarefa adquirida"
progressive_disclosure:
  - Ler nome, descrição e condições antes do corpo.
  - Abrir apenas o detalhe necessário ao estado da tarefa.
  - Consultar complementos somente se a condição se aplicar.
conditional_details:
  - if: "start de história"
    then: "guardar token local e renovar heartbeat por iteração significativa"
  - else_if: "tarefa pertence a outra execução"
    then: "não iniciar escritor concorrente ou usar registry alternativo"
  - else_if: "proprietário comprovadamente interrompido"
    then: "recuperar explicitamente com token, heartbeat observado e confirmação de inatividade"
  - else: "leitura de estado"
    then: "usar status sem alterar ownership"
---

# Ownership local

`feature_tracking.py start` adquire ownership. Tokens ficam na área administrativa Git,
não em documentação versionada. Heartbeat/release via `scripts/orchestration_lock.py`.

Um processo guarda o token; leitor/revisor não se torna proprietário. Não assumir tarefa
por idade do lock, timeout ou ausência de PID. Recuperação exige comprovar inatividade,
motivo, token e heartbeat observado; se heartbeat mudou, o comando recusa recuperação.
Ver [comandos e limites](../../docs/spec-driven-development/harness.md).

O mutex usa flock em Linux/WSL/POSIX e filesystem local. A posse é compartilhada entre
worktrees do mesmo repositório, não entre clones/máquinas. Não autentica usuário do SO
nem impede edição livre. Não ativar subagentes/paralelismo por causa desta regra.

Falha de gravação preserva estado para inspeção. Não remover automaticamente writer-lock
abandonado ou arquivos corrompidos. Liberação não marca Done nem dispensa revalidação.
