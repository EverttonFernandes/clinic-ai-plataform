---
{
  "task_key": "HARNESS-PR-20261016",
  "objective": "Preparar execução de histórias com outro modelo revisor, CI e PR para revisão manual do usuário",
  "phase": "DONE",
  "loop_iteration": 4,
  "requirement_source": {
    "path": "docs/tasks/HARNESS-PR-20261016/solicitacao.md",
    "sha256": "0e9d4179a221d79311c11b7cc267da55b01db07e9022f0af6d2f6550d914b266"
  },
  "scope": [
    ".agents",
    ".github",
    "scripts",
    "AGENTS.md",
    "spec.md",
    "README.md",
    ".gitignore",
    "docs/README.md",
    "docs/spec-driven-development",
    "docs/jira-pessoal",
    "docs/tasks/TEMPLATE.md",
    "docs/entregas/TEMPLATE.md",
    "docs/tracking"
  ],
  "requirements": {
    "AC1": {
      "description": "Registrar modelos/papéis, sem tratar troca de persona como modelo independente.",
      "status": "PASS",
      "evidence": [
        "contracts",
        "documentation",
        "evaluation"
      ]
    },
    "AC2": {
      "description": "Bloquear aprovação da história com mesmo executor/modelo, identidade desconhecida ou fallback sequencial.",
      "status": "PASS",
      "evidence": [
        "contracts",
        "documentation",
        "evaluation"
      ]
    },
    "AC3": {
      "description": "Exigir branch com ID da história, testes e CI do SHA correto antes do PR pronto para revisão.",
      "status": "PASS",
      "evidence": [
        "contracts",
        "documentation",
        "evaluation"
      ]
    },
    "AC4": {
      "description": "Manter a história em Review enquanto aguarda revisão humana; Done requer aceite e merge verificados.",
      "status": "PASS",
      "evidence": [
        "contracts",
        "documentation",
        "evaluation"
      ]
    },
    "AC5": {
      "description": "Revisar rigor dos testes funcionais/integrados/unitários e critérios, sem enfraquecer assertions.",
      "status": "PASS",
      "evidence": [
        "contracts",
        "documentation",
        "evaluation"
      ]
    },
    "AC6": {
      "description": "Preparar PR didático com problema, decisões, trade-offs, validações e roteiro de estudo/reprodução.",
      "status": "PASS",
      "evidence": [
        "contracts",
        "documentation",
        "evaluation"
      ]
    },
    "AC7": {
      "description": "Persistir handoff e evidências por revisão, invalidando aprovação depois de mudanças relevantes.",
      "status": "PASS",
      "evidence": [
        "contracts",
        "documentation",
        "evaluation"
      ]
    },
    "AC8": {
      "description": "Validar o protocolo e atualizar skills/rules/planejamento sem iniciar CT-001 ou alegar CI remota executada.",
      "status": "PASS",
      "evidence": [
        "contracts",
        "documentation",
        "evaluation"
      ]
    }
  },
  "exit_bar": {
    "contracts": "PASS",
    "documentation": "PASS",
    "final_review": "PASS"
  },
  "verification": {
    "contracts": {
      "command": [
        "python3",
        "-B",
        "-m",
        "unittest",
        "discover",
        "-s",
        "scripts/tests",
        "-v"
      ]
    },
    "documentation": {
      "command": [
        "python3",
        "-c",
        "from pathlib import Path\nimport json, subprocess, sys\nimport yaml\nfrom markdown_it import MarkdownIt\nfrom urllib.parse import unquote, urlsplit\nfiles=[Path('AGENTS.md'),Path('README.md'),Path('spec.md')]\nfiles+=list(Path('.agents').rglob('*.md'))\nfiles+=list(Path('.github').rglob('*.md'))\nfiles+=[p for p in Path('docs').rglob('*.md') if subprocess.run(['git','check-ignore','-q',str(p)]).returncode==1]\nparser=MarkdownIt()\ncount=0\ndef walk(tokens):\n    for token in tokens:\n        yield token\n        yield from walk(token.children or [])\nfor path in files:\n    for token in walk(parser.parse(path.read_text())):\n        target=token.attrGet('href') if token.type=='link_open' else token.attrGet('src') if token.type=='image' else None\n        if not target: continue\n        url=urlsplit(target)\n        if url.scheme or url.netloc or not url.path: continue\n        assert (path.parent / unquote(url.path)).exists(), (str(path),target)\n        count+=1\nrules=list(Path('.agents/rules').glob('*.md'))\nskills=list(Path('.agents/skills').glob('*/SKILL.md'))\nfor path in rules+skills:\n    content=path.read_text()\n    assert len(content.splitlines())<=300, path\n    front=yaml.safe_load(content.split('---',2)[1])\n    metadata=front.get('metadata',front)\n    assert 'progressive_disclosure' in metadata and 'conditional_details' in metadata, path\nfor path in skills:\n    result=subprocess.run([sys.executable,'/home/everton/.codex/skills/.system/skill-creator/scripts/quick_validate.py',str(path.parent)],capture_output=True,text=True)\n    assert result.returncode==0, (str(path),result.stdout,result.stderr)\nworkflow=yaml.load(Path('.github/workflows/harness.yml').read_text(),Loader=yaml.BaseLoader)\nassert set(workflow['on'])=={'push','pull_request','workflow_dispatch'}\nassert workflow['on']['push'] in ('',None) and workflow['on']['pull_request'] in ('',None)\nassert workflow['permissions']=={'contents':'read'}\nassert workflow['jobs']['contracts']['steps'][-1]['run']=='python3 -B -m unittest discover -s scripts/tests -v'\nrecords=[json.loads(p.read_text()) for p in Path('docs/tracking').glob('*.json') if p.name!='index.json']\nassert len(records)==37 and all(r['status']=='TODO' and r['started_at'] is None for r in records)\nassert subprocess.check_output(['git','branch','--show-current'],text=True).strip()=='main'\nprint(f'PASS: {len(files)} Markdown files, {count} local links, {len(rules)} rules, {len(skills)} skills, CI configuration; 37 stories not started')\n"
      ]
    }
  },
  "evaluation": {
    "status": "PASS",
    "mode": "independent",
    "worker_id": "/root",
    "worker_model": "not-exposed-in-maintenance-session",
    "reviewer_id": "/root/revisao_harness_pr",
    "reviewer_model": "gpt-6-sol",
    "path": "docs/tasks/HARNESS-PR-20261016/revisao.md",
    "sha256": "84545ab9eaf5afeec4bb3b9af6b55e762c78d5c336fec6f50e92e501f7ab3290",
    "scope_sha256": "b6671bdbd81d1cf08c8d5a64614a7572918076d9670e62a5b62993665767dad7",
    "source_sha256": "0e9d4179a221d79311c11b7cc267da55b01db07e9022f0af6d2f6550d914b266",
    "contract_sha256": "86d51db4905574e89b1d979a62b37fb3114089d521ecb354e2557991296f88b8",
    "gates": [
      "final_review"
    ]
  },
  "correction_queue": [
    {
      "id": "CI-EVENT",
      "status": "CLOSED",
      "severity": "HIGH",
      "evidence": "contracts: evento/path e gates ci/pr_ci"
    },
    {
      "id": "REST-PATH-REF",
      "status": "CLOSED",
      "severity": "HIGH",
      "evidence": "contracts: formato path@ref e merge sintético"
    },
    {
      "id": "HISTORICAL-ACCEPTANCE",
      "status": "CLOSED",
      "severity": "HIGH",
      "evidence": "contracts: evolução, receipts ausentes, merge e ancestralidade"
    }
  ],
  "handoff": {
    "next_action": "Aguardar solicitação de execução de CT-001; nenhuma história de aplicação iniciada",
    "blockers": [],
    "decisions": [
      "Astra/medium executa histórias; Sol revisa, sem fallback nas histórias",
      "PR e CI por história; usuário revisa e faz merge; nenhuma história de produto iniciada",
      "Receipts GitHub em fixtures não representam execução remota"
    ]
  },
  "completion_promise": "DONE"
}
---
# Plano da política de PR

Escopo: evolução do harness de preparação; histórias do produto não iniciadas.

## Cenários antes do código

- Revisão com mesmo modelo, mesma sessão ou identidade desconhecida é rejeitada.
- Revisão real conforme os modelos configurados, com hashes atuais, permite o gate local.
- Story sem CI/revisão humana no contrato não pode ser Done.
- CI sem run, de outro SHA, pendente, cancelada ou com falha não autoriza PR pronto.
- Novo commit exige nova CI; mudança de source/scope/contrato invalida também revisão e provas locais.
- PR aberto mantém Review; somente merge pelo usuário configurado confirma o aceite final.

## Mudanças planejadas

Configuração versionada de modelos; gates de revisão e entrega; coleta GitHub read-only;
skills de revisão/PR, template didático, regras de contexto e ajustes incrementais de CI no backlog.

## Validação

Red/Green com contratos locais e fixtures de respostas GitHub, sem apresentar fixtures como CI real.
Revisão em outro agente GPT-6 Sol conforme autorização do usuário, somente leitura e sem merge.
Nenhuma publicação ou implantação da aplicação nesta preparação.

## Achados durante a revisão independente

1. Sol rejeitou coleta por nome/SHA sem evento/identidade. Corrigido com path/ID do
   workflow, gates push e pull_request associados ao PR/HEAD, e estágio post-pr.
2. Sol identificou formato REST path@ref. Red reproduziu três erros de ausência de workflow;
   parser e fixtures passaram a tratar path/ref e merge sintético sem perder vínculo ao HEAD.
3. Sol identificou dependência Done revalidada contra código atual/receipts de 24h. Dois
   testes Red reproduziram bloqueio da evolução e confiança em merge histórico sem consulta.
   Aceite histórico foi separado da regressão atual; fonte/contrato/parecer, merge GitHub
   e ancestralidade continuam obrigatórios para liberar dependências.
