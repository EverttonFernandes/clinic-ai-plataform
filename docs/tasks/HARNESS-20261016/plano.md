---
{
  "task_key": "HARNESS-20261016",
  "objective": "Adaptar o harness do WorkLink com regras condicionais, Ralph Loop e conclusão verificável, sem iniciar o produto",
  "phase": "DONE",
  "loop_iteration": 2,
  "requirement_source": {
    "path": "docs/tasks/HARNESS-20261016/solicitacao.md",
    "sha256": "44e08c60dff2cb5df6afc5c298c3d0def06bbff3b02b148b3bbedfae2854f53d"
  },
  "scope": [
    "scripts",
    ".agents",
    ".github/workflows/harness.yml",
    "AGENTS.md",
    ".gitignore",
    "README.md",
    "spec.md",
    "docs/README.md",
    "docs/jira-pessoal/KANBAN-OFICIAL.md",
    "docs/tasks/TEMPLATE.md",
    "docs/entregas/TEMPLATE.md",
    "docs/tracking/README.md",
    "docs/spec-driven-development/harness.md",
    "docs/spec-driven-development/evals-harness.md",
    "docs/spec-driven-development/ambientes-e-cicd.md"
  ],
  "requirements": {
    "AC1": {
      "description": "Adaptar conditional details e progressive disclosure nas rules e skills locais, sem carregar todos os especialistas por rotina.",
      "status": "PASS",
      "evidence": [
        "contracts",
        "docs",
        "evaluation"
      ]
    },
    "AC2": {
      "description": "Integrar Ralph Loop com plano persistido, fila de correções, handoff, retomada e escalonamento de falhas repetidas.",
      "status": "PASS",
      "evidence": [
        "contracts",
        "docs",
        "evaluation"
      ]
    },
    "AC3": {
      "description": "Impedir conclusão sem execução real, cobertura dos critérios originais, escopo atual e revisão identificada.",
      "status": "PASS",
      "evidence": [
        "contracts",
        "docs",
        "evaluation"
      ]
    },
    "AC4": {
      "description": "Validar dependências e ownership local antes de executar histórias, preservando a prioridade do Kanban.",
      "status": "PASS",
      "evidence": [
        "contracts",
        "docs",
        "evaluation"
      ]
    },
    "AC5": {
      "description": "Adaptar Conventional Commits e SemVer, distinguindo conclusão local de release/publicação autorizada.",
      "status": "PASS",
      "evidence": [
        "contracts",
        "docs",
        "evaluation"
      ]
    },
    "AC6": {
      "description": "Definir evals do harness e protocolo LLM-as-a-Judge calibrado, sem aprovação fictícia ou chamada paga automática.",
      "status": "PASS",
      "evidence": [
        "contracts",
        "docs",
        "evaluation"
      ]
    },
    "AC7": {
      "description": "Testar a adaptação por CLI em repositórios Git temporários, incluindo casos negativos e evidências desatualizadas.",
      "status": "PASS",
      "evidence": [
        "contracts",
        "docs",
        "evaluation"
      ]
    },
    "AC8": {
      "description": "Preservar arquitetura, histórias de produto, prompts ignorados e alterações preexistentes; atualizar referências e limites reais.",
      "status": "PASS",
      "evidence": [
        "contracts",
        "docs",
        "evaluation"
      ]
    }
  },
  "exit_bar": {
    "contracts": "PASS",
    "docs": "PASS",
    "final_review": "PASS"
  },
  "verification": {
    "contracts": {
      "command": [
        "/usr/bin/python3",
        "-B",
        "-m",
        "unittest",
        "discover",
        "-s",
        "scripts/tests",
        "-v"
      ]
    },
    "docs": {
      "command": [
        "/usr/bin/python3",
        "-B",
        "-c",
        "from pathlib import Path\nfrom urllib.parse import unquote, urlsplit\nimport json, re\nfiles = [Path('AGENTS.md'), Path('README.md'), Path('spec.md'), Path('docs/README.md'),\n         Path('docs/tasks/TEMPLATE.md'), Path('docs/entregas/TEMPLATE.md'), Path('docs/tracking/README.md'),\n         *Path('.agents').rglob('*.md'), *Path('docs/jira-pessoal').rglob('*.md'),\n         *Path('docs/spec-driven-development').rglob('*.md')]\ncount = 0\nfor file in files:\n    content = file.read_text()\n    if '.agents' in file.parts:\n        assert content.startswith('---\\n') and len(content.splitlines()) <= 300, file\n        header = content.split('---\\n', 2)[1]\n        assert 'conditional_details:' in header and 'progressive_disclosure:' in header, file\n    links = re.findall(r'\\[[^\\]]*\\]\\(([^)]+)\\)', content)\n    links += re.findall(r'^\\[[^\\]]+\\]:\\s+(\\S+)', content, re.M)\n    for uri in links:\n        uri = uri.strip('<>')\n        url = urlsplit(uri)\n        if url.scheme or uri.startswith('#'): continue\n        assert (file.parent / unquote(url.path)).exists(), (file, uri)\n        count += 1\nrecords = [json.loads(file.read_text()) for file in Path('docs/tracking').glob('*.json') if file.name != 'index.json']\nassert len(records) == 37\nassert all(record['status'] == 'TODO' and record['started_at'] is None and record['completed_at'] is None for record in records)\nassert not Path('compose.yml').exists()\nprint(f'{len(files)} Markdown documents, {count} existing local references; 37 unstarted product stories.')\n"
      ]
    }
  },
  "evaluation": {
    "status": "PASS",
    "mode": "separate-review-fallback",
    "worker_id": "/root",
    "reviewer_id": "/root",
    "reason": "Revisão sequencial separada na mesma execução; nenhuma sessão independente foi executada.",
    "path": "docs/tasks/HARNESS-20261016/revisao.md",
    "sha256": "31ed928739d1c20de14576234dd6ab3b3567d8aa5620d40ac1814acb4c835aa3",
    "scope_sha256": "e130d18ca8b28f3aafc1861f9dbc9705c8d263fd2e033e84cec5773751c5dcf0",
    "contract_sha256": "231d09933cd2154fe08cbb225d579f1f424fdbcb1f893ce7394d4b0cc6d123dd",
    "source_sha256": "44e08c60dff2cb5df6afc5c298c3d0def06bbff3b02b148b3bbedfae2854f53d",
    "gates": [
      "final_review"
    ]
  },
  "correction_queue": [],
  "handoff": {
    "next_action": "Manutenção local concluída; CT-001 permanece a próxima história de produto, sem início.",
    "decisions": [
      "Scripts de coordenação Git/Python stdlib no host; aplicação permanece Docker",
      "Histórias de produto não iniciadas",
      "Nenhum commit/push/deploy ou chamada paga"
    ],
    "blockers": []
  },
  "completion_promise": "DONE"
}
---
# Plano — adaptação do harness

Escopo: harness de desenvolvimento, sem aplicação de clínicas ou integração externa.
Base: scripts e práticas lidas no WorkLink, adaptadas aos contratos deste repositório.

## Comportamento esperado antes das mudanças

1. Dado o Kanban atual, importar 37 histórias com IDs/dependências e nenhuma conclusão inferida.
2. Dado um requisito omitido ou dependência removida do plano, recusar a conclusão/início.
3. Dado PASS apenas escrito ou log/escopo alterado, recusar DONE.
4. Dado comando real, revisão válida e critérios completos, permitir conclusão local.
5. Dado execução concorrente ou token incorreto, preservar ownership; recuperação não é automática por idade.
6. Dado falha recorrente, conservar incidente/tentativas e mudar investigação antes de repetir correção.
7. Dado pedido de release, aplicar Conventional Commits/SemVer sem autorizar push/deploy implicitamente.

## Implementação e prova

- Portar o núcleo pequeno de verificação/tracking/ownership e os contratos existentes.
- Escrever casos de adaptação; obter Red funcional contra o núcleo ainda não adaptado.
- Corrigir parser do Kanban, validação de critérios e dependências; executar os contratos e evals locais.
- Atualizar regras condicionais, skills, templates e política de release; revisão de coerência e links.
- Registrar revisão separada e limites: metadata local não é assinatura nem prova de identidade de agente.

## Ambiente

Docker Desktop não está integrado nesta distro WSL: `docker version` falha antes de acessar daemon.
Os utilitários de coordenação usam apenas Git e biblioteca padrão Python, como no WorkLink,
sem instalar dependências nem executar a aplicação. A exceção de bootstrap do harness será explícita
em AGENTS; a toolchain da aplicação continua em Docker. Não simular validação Docker.

## Resultados

Preencher com comandos/resultados executados no relatório desta manutenção. Não registrar
gates da aplicação como PASS nem alterar estados das 37 histórias por esta demanda.
