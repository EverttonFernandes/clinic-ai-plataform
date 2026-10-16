# Plano e evidências — ID da história

Usar em `docs/tasks/<ID>/plano.md` quando a implementação começar. Este template não é uma execução.
Criar também progress.md com objetivo, última ação/prova, pendências, decisões e próxima ação.
Protocolo e comandos: [harness](../spec-driven-development/harness.md).

- História/requisitos/dependências:
- Revisão de partida e alterações preexistentes:
- Branch story/<ID>-<slug>, base/HEAD e modelo/ID real do executor (Astra/medium):
- Objetivo e limite de escopo:
- Decisões pendentes e consumidores afetados:
- Cenários BDD e efeito observável:
- Testes selecionados por impacto, ambiente e componentes reais/doubles:
- Passos mínimos de implementação:
- Custos, autorização externa e preservação de dados aplicáveis:

## Evidências executadas

| Etapa | Comando/ação | Ambiente e revisão/diff | Resultado e evidência |
| --- | --- | --- | --- |
| Red | A preencher na execução | A preencher | PENDING |
| Green | A preencher na execução | A preencher | PENDING |
| Revisão de coesão | A preencher na execução | A preencher | PENDING |
| Regressão afetada | A preencher na execução | A preencher | PENDING |

Em Red, registrar por que a falha corresponde ao comportamento; falha de setup não conta.
Documentar N/A quando a etapa não se aplica, com motivo. Não inserir secrets/logs privados.
Gates externos não executados continuam PENDING, com impedimento e próximo passo.

## Frontmatter verificável do plano real

O plano começa com JSON entre delimitadores YAML. Preencher caminhos/hash/comandos reais;
o exemplo abaixo é incompleto de propósito, não uma prova válida. Todos os AC e BDD extraídos
da história com `harness_completion.py criteria` entram em requirements com descrição original.
Não incluir plano/progress/parecer/log no scope do próprio código.

```text
---
{
  "task_key": "<ID>",
  "objective": "<resultado da história>",
  "phase": "PLANNING",
  "loop_iteration": 0,
  "requirement_source": {"path": "<história oficial>", "sha256": "<hash atual>"},
  "scope": ["<arquivos/diretórios reais e consumidores afetados>"],
  "requirements": {
    "AC1": {"description": "<critério original>", "status": "PENDING", "evidence": ["functional"]},
    "BDD1": {"description": "<cenário original completo normalizado>", "status": "PENDING", "evidence": ["functional"]}
  },
  "exit_bar": {"functional": "PENDING", "final_review": "PENDING", "ci": "PENDING", "pr_ci": "PENDING", "human_review": "PENDING"},
  "verification": {
    "functional": {"command": ["<executável real>", "<argumento>"]},
    "ci": {"command": ["python3", "scripts/pr_evidence.py", "docs/tasks/<ID>/plano.md", "ci"]},
    "pr_ci": {"command": ["python3", "scripts/pr_evidence.py", "docs/tasks/<ID>/plano.md", "pr"]},
    "human_review": {"command": ["python3", "scripts/pr_evidence.py", "docs/tasks/<ID>/plano.md", "merged"]}
  },
  "evaluation": {"status": "PENDING"},
  "correction_queue": [],
  "handoff": {"next_action": "<próxima ação>", "decisions": [], "blockers": []},
  "completion_promise": "PENDING"
}
---
# Plano técnico
- [ ] Implementar e verificar cada critério original
```

Acrescentar gates de integração/segurança/custo/concorrência/CI/release conforme impacto e aceite.
N/A exige justificativa e não pode ocultar comando de verificação declarado. Critério aplicável
precisa de prova PASS, não N/A. O gate extrai AC/BDD para detectar omissão/reescrita do original.

## Parecer e fila de correções

Evaluation referencia status, mode, worker_id/reviewer_id reais, path/sha256 do parecer e
source_sha256/scope_sha256/contract_sha256 retornados por verify. Listar gates de revisão avaliados.
Histórias exigem independent: worker_model gpt-6-astra, worker_reasoning_effort medium,
reviewer_model gpt-6-sol, IDs de execuções diferentes. Não usar fallback.
Revisor confere fonte/scope/contrato e testes reais conforme a skill independent-review.
Os estágios local, pre-pr e post-pr adiam somente gates externos definidos, sem permitir Done.
Aceite humano pendente fica no frontmatter/progress; checkbox aberto no corpo indica trabalho local pendente.

No progress, incluir branch/base/HEAD, modelos/IDs, etapa, PR/CI, critérios e gates pendentes,
receipts/parecer, incidentes/contadores e próxima ação. Excluir tokens do lock e logs privados.
Ao retomar, conferir fatos/hashes; não confiar apenas na narrativa do checkpoint.

Correction queue conserva ID, critério, severidade, estado OPEN/CLOSED e referência à prova da correção.
Incidente recorrente registra esperado/observado, reprodução, ambiente/revisão, hipóteses/tentativas,
resultados e próximo experimento em `incidentes/<ID>.md`. Não zerar contador trocando nome/persona.
Falha de teste volta ao executor; ausência de ambiente fica PENDING, sem aprovação por narrativa.
