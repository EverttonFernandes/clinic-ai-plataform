---
{
  "task_key": "CT-001",
  "objective": "Subir API mínima e PostgreSQL/pgvector e Redis em Docker reproduzível, com saúde, recuperação, persistência e CI reais.",
  "phase": "AUDIT",
  "loop_iteration": 3,
  "requirement_source": {
    "path": "docs/jira-pessoal/historias-tecnicas/CT-001-ambiente-docker.md",
    "sha256": "fa5fd500a4142c1745bf8e9172a235c5ba252d052c9523229fad7c031999e474"
  },
  "scope": [
    "src/clinic_ai",
    "tests/functional",
    "Dockerfile",
    "compose.yaml",
    "Makefile",
    ".env.example",
    ".dockerignore",
    "requirements.txt",
    "requirements-test.txt",
    "scripts/smoke-environment.sh",
    ".github/workflows/application.yml",
    "docs/spec-driven-development/ambientes-e-cicd.md",
    "docker/postgres/001-vector.sql"
  ],
  "requirements": {
    "AC1": {
      "description": "Definir versões suportadas/travadas e comandos de build/up/down, com .env.example sem segredos.",
      "status": "PASS",
      "evidence": [
        "functional"
      ]
    },
    "AC2": {
      "description": "Compose inicia PostgreSQL/pgvector e Redis com healthchecks; API expõe liveness/readiness distintos.",
      "status": "PASS",
      "evidence": [
        "functional"
      ]
    },
    "AC3": {
      "description": "Parar ambiente preserva volumes; runtime sem root quando viável e sem ferramentas de build desnecessárias.",
      "status": "PASS",
      "evidence": [
        "functional"
      ]
    },
    "AC4": {
      "description": "Documentar portas, projeto Compose, perfis e recuperação de falha de dependência.",
      "status": "PASS",
      "evidence": [
        "functional"
      ]
    },
    "AC5": {
      "description": "Workflow Application CI em push da branch e PR executa build/smoke reais do ambiente; registrar sucesso do HEAD antes do PR e conferir os checks após abertura.",
      "status": "PASS",
      "evidence": [
        "functional",
        "evaluation"
      ]
    },
    "AC6": {
      "description": "Bootstrap FastAPI segue o [mapa DDD](../../spec-driven-development/arquitetura-ddd.md), sem regra de negócio no transporte nem geração antecipada de módulos/camadas vazios.",
      "status": "PASS",
      "evidence": [
        "functional"
      ]
    },
    "BDD1": {
      "description": "Cenário: Subida limpa Dado que um checkout sem banco inicializado e configuração sintética Quando o ambiente é construído e iniciado Então as dependências ficam saudáveis e a API fica pronta sem ajuste manual no host",
      "status": "PASS",
      "evidence": [
        "functional"
      ]
    },
    "BDD2": {
      "description": "Cenário: Dependência indisponível Dado que a API está ativa e o PostgreSQL é interrompido Quando a readiness é consultada Então ela indica indisponibilidade e não anuncia capacidade de executar reservas",
      "status": "PASS",
      "evidence": [
        "functional"
      ]
    },
    "BDD3": {
      "description": "Cenário: Persistência local Dado que dados sintéticos existem no volume de desenvolvimento Quando o ambiente é parado e reiniciado Então os dados continuam disponíveis sem recriar ou apagar o volume",
      "status": "PASS",
      "evidence": [
        "functional"
      ]
    }
  },
  "exit_bar": {
    "functional": "PASS",
    "final_review": "PASS",
    "ci": "PENDING",
    "pr_ci": "PENDING",
    "human_review": "PENDING"
  },
  "verification": {
    "functional": {
      "command": [
        "make",
        "smoke"
      ]
    },
    "ci": {
      "command": [
        "python3",
        "scripts/pr_evidence.py",
        "docs/tasks/CT-001/plano.md",
        "ci"
      ]
    },
    "pr_ci": {
      "command": [
        "python3",
        "scripts/pr_evidence.py",
        "docs/tasks/CT-001/plano.md",
        "pr"
      ]
    },
    "human_review": {
      "command": [
        "python3",
        "scripts/pr_evidence.py",
        "docs/tasks/CT-001/plano.md",
        "merged"
      ]
    }
  },
  "evaluation": {
    "status": "PASS",
    "mode": "independent",
    "worker_id": "/root/ct001_execucao",
    "worker_model": "gpt-6-astra",
    "worker_reasoning_effort": "medium",
    "reviewer_id": "/root/ct001_execucao/ct001_revisao",
    "reviewer_model": "gpt-6-sol",
    "reviewer_reasoning_effort": "not_exposed",
    "path": "docs/tasks/CT-001/revisao.md",
    "sha256": "76b0e19722d9463b2c73cdb694ff92594e8a9698f7e3f5cd6b69f26d7bab1841",
    "gates": [
      "final_review"
    ],
    "scope_sha256": "3c4043a6630e3a35e7964a7413645cec913bddf404d3cd5a39c68909d3679fbb",
    "source_sha256": "fa5fd500a4142c1745bf8e9172a235c5ba252d052c9523229fad7c031999e474",
    "contract_sha256": "b81c337e79a587fd5ae2f9683874d037b90baff917cf9130a83b26bdac315d75"
  },
  "correction_queue": [],
  "handoff": {
    "next_action": "Gate local, commit seletivo e push branch; coletar CI push do HEAD antes do PR.",
    "decisions": [
      "Escopo exclusivo CT-001; nenhuma dependência de história.",
      "Preservar dois commits documentais preexistentes na main local, sem push de main.",
      "D-17: até três diagnósticos locais seguros de ambiente; sem loop nem instalação host para contornar Docker."
    ],
    "blockers": []
  },
  "completion_promise": "PENDING"
}
---
# Plano e execução — CT-001

História/requisitos originais íntegros no frontmatter (AC1–AC6, BDD1–BDD3; RNF-11/12/13/14).
Dependências: nenhuma, validadas por tracking. Branch `story/CT-001-ambiente-docker`,
base `c72a95c`; árvore inicialmente limpa. Commits documentais preexistentes `37092e8`
e `c72a95c` preservados, sem push de main. Executor real `gpt-6-astra`/`medium`,
`/root/ct001_execucao`; Ralph Loop, cohesive-code-development e git-operator aplicados.

## Plano anterior ao código e BDD

Plano criado antes do scaffold: API mínima com bootstrap técnico, PostgreSQL/pgvector,
Redis e smoke Docker. Sem domínio, worker, scanner, frontend, camadas vazias ou ampliação
do harness. README de estudo e história normativa preservados. Consumidores: operação
Compose/Makefile, smoke HTTP e Application CI. Arquitetura segue mapa DDD incremental.

Cenários definidos antes da implementação:

1. Checkout/projeto sem dados: build/up, dependências saudáveis e saúde HTTP real.
2. PostgreSQL parado: live200, ready503; recuperar e observar ready200. Repetir com Redis.
3. Gravar marcadores sintéticos em PG/Redis, down sem remover volumes, up e leitura
   independente dos mesmos marcadores. Testar operação vetorial real, além de conexão.
4. Runtime não root, sem compilador/pytest; portas DB/Redis não publicadas.
5. CI push/PR usa build/smoke real. Runs remotos e aceite humano têm gates próprios.

Contrato: GET /health/live → 200 {status: alive}; GET /health/ready →
200 {status: ready} ou 503 {status: unavailable}. Corpo sem dados internos.
Readiness comprova infraestrutura deste incremento, não reservas ou controles futuros.

## Implementação e seleção de testes

Bootstrap compõe Redis e sondas técnicas; main é entrada ASGI. Não há regra de negócio.
Conexões/consultas têm timeouts; Redis sem retry automático nesta sonda. Compose fixa
imagens por digest; requirements fixam dependências transitivas resolvidas em Docker.
Runtime UID10001 e filesystem somente leitura. Extensão vector inicializada no banco;
migrations de domínio ficam em CT-004. Dados exclusivamente sintéticos.

`make smoke` seleciona todo o incremento: pytest por HTTP contra processo separado,
pgvector/Redis reais, paradas/recuperações, inspeção runtime e persistência PostgreSQL/Redis.
Projeto único de teste e porta loopback aleatória; cleanup encerra somente esse projeto,
sempre preservando volumes. Sem fake, chamadas pagas, contas, deploy ou dados reais.
Unitário duplicando status/sonda não acrescentaria prova: as decisões relevantes (saúde,
falha das duas dependências, recuperação) são exercitadas pela fronteira real.

## Red, Green e coesão

| Etapa | Comando/ambiente | Resultado |
| --- | --- | --- |
| Setup inicial | Docker WSL, sockets e docker.exe | Bloqueio real de daemon, não Red; resolvido após usuário autorizar iniciar Desktop |
| Setup retomado | Engine29.4.2/Compose5.1.3, Linux amd64 | PASS; imagens públicas via DOCKER_CONFIG temporário sem credenciais por falha do helper Windows |
| Red | Compose projeto clinic-ai-ct001-red; pytest no smoke, ASGI vazio em processo separado | 2 failed HTTP404 nas rotas contratadas ausentes; 1 passed pgvector/Redis reais. `.git/harness/ct001-red.log` |
| Green | DOCKER_CONFIG privado + make smoke | exit0: subida3, falhaPG2, recuperação3, falhaRedis2, recuperação3 e restart3 testes; marcadores PG/Redis preservados; runtime não root sem gcc/pytest. `.git/harness/ct001-green.log` |
| Coesão após Green | Revisão de bootstrap/main, Compose, script e assertions | Funções pequenas; infraestrutura no bootstrap, sem domínio artificial. Script separa fases observáveis e preserva exitcode/volumes. Sem refatoração adicional necessária |
| Regressão/gate | harness_completion.py verify ... functional | Receipt próprio obrigatório; estado consultável no frontmatter/progress |

O scaffold inicial só criava FastAPI vazio; falhas HTTP404 foram ausência do contrato,
não URL errada ou processo indisponível. Teste real de dependências passou no mesmo Red.
O guia operacional em ambientes-e-cicd documenta versões, portas, perfis, configurações,
recuperação e limitações. Smoke foi integrado à Application CI assim que nasceu.

## D-17 e continuidade

Uma história; diagnóstico inicial limitado a três verificações seguras, com handoff no
bloqueio. Usuário autorizou iniciar Docker e continuar, permitindo novo incremento.
Uma revisão Sol independente inicial; novas rodadas apenas para correções concretas.
Três correções rejeitadas de mesmo incidente exigem diagnóstico. Custo de desenvolvimento
assistido não é observável; nenhum valor financeiro inferido. Produto sem inferência paga.

Gates externos permanecem obrigatórios e separados: ci(push), pr_ci(pull_request),
human_review(merge pelo usuário). O parecer/local avalia implementação de AC5 e seu smoke;
PASS local de requisito não substitui os runs externos, nem autoriza conclusão.
Após local: commit seletivo, push branch, CI HEAD, pre-pr, PR, CI PR, post-pr e Review.
Não fazer merge, release, deploy nem iniciar CT-002. Status final depende de provas reais.
