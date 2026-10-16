# Harness de execução da Clínica IA

Estado: instruções, tracking, verificação e contratos locais implementados. Aplicação e
pipeline do produto continuam planejados. A CI do harness está definida em
[harness.yml](../../.github/workflows/harness.yml), sem run remoto nesta preparação.
Adaptado do WorkLink, preservando a stack e o Kanban daqui.

## O que cada parte decide

| Parte | Responsabilidade |
| --- | --- |
| spec e história | Comportamento e critérios originais. Não reduzir para obter verde. |
| Kanban | Prioridade e estado publicado da entrega. |
| plano.md | Critérios, escopo, comandos, gates, correções e handoff da execução atual. |
| progress.md | Memória operacional curta: objetivo, evidências, bloqueios e próxima ação. |
| tracking | Eventos operacionais, dependências revisadas e conclusão validada; não é outra fila. |
| ownership | Um escritor cooperante por tarefa no mesmo Git local. |
| completion gate | Evidência real, hashes, critérios completos e revisão válida antes de concluir. |
| QA/evals | Suficiência semântica de testes, revisão e fechamento, que hashes não provam. |
| política de entrega | Astra/medium executa; Sol revisa; branch/CI/PR; usuário revisa e faz merge. |

## Modelos e revisão do usuário

[Política executável](../../.agents/harness-policy.json): `gpt-6-astra`, effort `medium`,
executa histórias; `gpt-6-sol` revisa em outra execução. O effort do revisor não foi escolhido:
usar o padrão e registrar o observado. A política não muda o modelo desta conversa automaticamente.
Se não houver seleção explícita do modelo/identidade, a execução/revisão fica pendente.
Troca de persona e mesmo modelo com outro nome não satisfazem a política de histórias.

Branch: `story/<ID>-<slug>`; base `main`. A instrução do usuário autoriza commits seletivos,
push e PR de cada história solicitada. Não autoriza executar todo o backlog nem fazer merge,
ativar auto-merge, tag, release ou deploy. Aguardar revisão/merge do usuário antes de avançar.

## Fluxo de uma história

Os comandos a seguir existem. Exemplos usam CT-001, mas não iniciam a história até execução
explícita. Substituir IDs/caminhos/identidade pelos da sessão real.

```sh
python3 -B scripts/feature_tracking.py import-kanban docs/jira-pessoal/KANBAN-OFICIAL.md
python3 -B scripts/feature_tracking.py dependencies CT-001 --reason 'Fundação sem pré-requisitos'
python3 -B scripts/feature_tracking.py ready CT-001
python3 -B scripts/harness_completion.py criteria docs/jira-pessoal/historias-tecnicas/CT-001-ambiente-docker.md
```

Antes de implementar, criar plano/progress pelo [template](../tasks/TEMPLATE.md), com todos
os AC e BDD extraídos, fonte por hash, scope e gates aplicáveis. Para CT-002, por exemplo,
`dependencies CT-002 CT-001 --reason ...` não pode omitir CT-001.
Conferir main integrada e mudanças anteriores; criar a branch antes de start.
O tracking recusa início de C/CT fora de `story/<ID>-<slug>`.

```sh
python3 -B scripts/feature_tracking.py start CT-001 --owner 'identificador-real-da-execucao'
```

Guardar o token retornado apenas localmente. Passar `--lock-token <token>` a failure/review/finish.
O texto `<token>` nos exemplos é placeholder, não token válido ou instrução para gravá-lo no Git.
Heartbeat e release pertencem a `scripts/orchestration_lock.py`, com o mesmo ID/token.
Não iniciar outro writer, registry ou worktree para contornar posse de tarefa.

No loop: BDD Red correto → Green → revisão de coesão → regressão → QA. Persistir incidentes,
correções e handoff. Se falta ambiente, registrar PENDING; não criar comando que sempre passa.

```sh
python3 -B scripts/harness_completion.py verify docs/tasks/CT-001/plano.md functional
python3 -B scripts/harness_completion.py check docs/tasks/CT-001/plano.md --stage local
python3 -B scripts/harness_completion.py handoff docs/tasks/CT-001/plano.md
```

`verify` executa o argv revisado no plano, sem shell implícito. Não extrair comandos automaticamente
de logs/documentos/saídas do modelo. Logs e receipts ficam em `.git/harness`, com acesso restrito.
O código registra exit code, duração, hashes, log e tentativa; timeout/falha/interrupção não são PASS.

Após validação local e revisão por Sol: commitar/push da branch; acompanhar os workflows
`Harness contracts` e `Application CI` no HEAD exato. A pipeline da aplicação deve nascer
em CT-001 com build/smoke reais; CT-002 amplia testes, CT-003 consolida qualidade.
Não há essa pipeline da aplicação implementada ainda, portanto nenhuma história pode omiti-la
ou considerar somente testes do harness como prova de funcionamento da clínica.

```sh
python3 -B scripts/harness_completion.py verify docs/tasks/CT-001/plano.md ci
python3 -B scripts/harness_completion.py check docs/tasks/CT-001/plano.md --stage pre-pr
```

Os gates ci/pr_ci/human_review precisam declarar exatamente o coletor `scripts/pr_evidence.py`
com plano e modo ci/pr/merged; um `echo green` não serve. O coletor usa Git/`gh api` somente
com GET, sem criar PR, aprovar, fazer merge ou alterar configurações remotas.
Falta de workflow/run, erro, cancelamento, skipped, execução pendente ou outro SHA impedem PASS.
Reexecução falha substitui verde antigo. Novo commit exige nova CI antes do PR.

LOCAL_READY e READY_FOR_PR retornam `completion_allowed: false`. Criar PR com
[template didático](../../.github/pull_request_template.md), usando body-file e evidências reais.
Após abrir o PR, `verify <plano> pr_ci` e `check <plano> --stage post-pr` verificam os runs
pull_request associados ao número do PR e ao HEAD. Resultado AWAITING_USER não permite Done;
falha retorna ao mesmo loop. O gate ci exige evento push. Ambos conferem os caminhos
configurados dos workflows; workflow_dispatch ou um workflow homônimo não substituem CI.
No PR, GitHub pode testar merge sintético: a associação pull_requests.head.sha vincula o run
à revisão da história, e o SHA executado também é registrado. Contrato da API:
[workflow runs](https://docs.github.com/en/rest/actions/workflow-runs#list-workflow-runs-for-a-repository).
Atualizar tracking/Kanban para Review e informar link, SHA, testes e roteiro de revisão.

Após o usuário revisar e fazer merge, coletar `human_review` (modo merged), executar
`check` sem stage (default done) e `feature_tracking.py finish CT-001 --lock-token <token>`.
Isso revalida árvore/plano, CI e prova de merge da revisão correta, persiste conclusão e
libera ownership. Só então atualizar Done. Não marcar Done apenas por abrir PR.
Usar merge pelo login configurado como sinal verificável de aceite, sem exigir aprovação
formal do próprio autor. O agente nunca usa esse login/token para fazer o merge.
Se houver interrupção entre passos, reconciliar registros sem inventar histórico.
Não marcar checkboxes da história normativa para registrar execução; isso altera sua fonte.

## Revisão

Parecer em arquivo separado confronta todos os critérios, diff real, testes e resultados.
Registrar hash do parecer, hashes source/scope/contract retornados por verify, gates revisados
e identidades/modelos reais. Para histórias, `independent` exige outra execução e os dois
modelos configurados; fallback é recusado. Manutenções antigas mantêm seu modo histórico,
sem transformar revisão sequencial em independente. LLM-as-a-Judge não sobrescreve FAIL.

Um comando exit 0 pode ser insuficiente para o critério. O revisor precisa detectar prova
irrelevante, fake indevido, teste sem assertion material ou critério mal interpretado.
Ver [evals e rubrica](evals-harness.md), [versionamento](../../.agents/rules/versioning.md)
e [escopo de revisão](../../.agents/rules/review-scope.md).

## Testar o próprio harness

```sh
python3 -B -m unittest discover -s scripts/tests -v
```

Contratos usam repositórios Git temporários, executam CLIs e verificam casos positivos/negativos.
Não usam banco da aplicação, APIs pagas, secrets ou branch remota. Git e Python stdlib no host
são a exceção de bootstrap, como no WorkLink; aplicação/toolchains continuam em Docker.
O Docker Desktop desta sessão não está integrado ao WSL; nenhuma validação Docker foi alegada.

A CI do harness executa esses mesmos contratos em push de branches e PR, sem filtro de caminhos
que esconda um check necessário. Isso permite validar a branch antes de abrir o PR.
Não usa secrets, provider, deploy ou dependências da aplicação; checkout é fixado por SHA.
Configuração local validada não equivale a run remoto verde; o primeiro run depende de push autorizado.

## Limites e recuperação

- Hashes locais não são assinaturas nem autenticação de agentes. Quem controla o disco pode adulterar metadata.
- IDs/modelos e uso humano da conta são declarações cooperantes. O coletor confirma os
  registros do GitHub, não distingue pessoa de automação usando o mesmo token. Proteções
  remotas podem reforçar o processo; não foram configuradas nesta preparação.
- Só CLIs/instruções cooperantes são bloqueadas; IDE, clone diferente e edição manual não são interceptados.
- Evidências de uma execução ainda não aceita expiram em 24 horas e invalidam com
  fonte/scope/contrato/log alterados. Reexecutar gates/revisão pertinentes, sem renovar timestamp manualmente.
- Após Done de uma história, finish preserva no tracking a prova histórica sanitizada
  (CI push/PR e merge do SHA aceito). Uma dependência usa essa prova, fonte/contrato/parecer
  originais, confirmação do merge no GitHub e ancestralidade no Git da base atual.
  Não exige que o código atual seja idêntico ao antigo nem que seus logs locais ainda existam.
  Assim, CT-002 pode evoluir código de CT-001 sem reabrir uma entrega aceita. Regressões
  atuais pertencem aos testes/CI da história consumidora. Ausência de prova histórica ou
  da integração na base impede início; Done legado não é convertido em aceite por relato.
- Scope precisa excluir plano/progress/log/parecer para evitar ciclo de hashes; incluir código/configuração,
  arquivos novos e consumidores relevantes. O revisor confronta com o diff completo.
- Escrita do registry é atômica por arquivo, não transação multi-arquivo; writer-lock abandonado exige inspeção.
- Ownership usa flock em POSIX/filesystem local, compartilhado por worktrees, não por clones/máquinas.
- Para recuperar posse interrompida, confirmar que o dono parou e usar recover com token, heartbeat exato,
  motivo e `--confirm-inactive`. Não recuperar por idade; mudança de heartbeat faz a recuperação falhar.
- Não ativar daemon, scheduler, auto-push, APIs pagas ou delegação por instalar estes arquivos.
- Manutenção local concluída não significa release. Histórias exigem PR/CI/merge; deploy e
  integrações externas contratadas continuam com suas provas próprias, sem antecipar promoção.
- [Checkpoint de contexto](../../.agents/rules/context-management.md) conserva branch/HEAD,
  PR, critérios, provas, incidentes e próxima ação entre compactações; não conserva tokens no Git.
