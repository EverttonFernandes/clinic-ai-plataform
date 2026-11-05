# Checkpoint — CT-001

- Escopo autorizado: somente CT-001, ambiente Docker/API mínima/DB/Redis/CI. Sem merge.
- Executor real selecionado: `gpt-6-astra` / `medium`, `/root/ct001_execucao`.
- Branch: `story/CT-001-ambiente-docker`; base/HEAD `c72a95c`.
- main local contém `37092e8` e `c72a95c` ainda não presentes em origin/main; foram preservados.
- Etapa: plano/BDD registrados antes de qualquer código. Kanban e tracking: Blocked.
- Dependências: nenhuma, CLI dependencies/ready executada com sucesso.
- Árvore inicialmente limpa. Agora apenas plano/progress, Kanban e registros do tracking mudaram.
- Nenhum comportamento/teste da aplicação foi escrito ou executado; sem commit, push ou PR.

## Impedimento comprovado

Três diagnósticos seguros, sem instalar ferramenta ou alterar Docker Desktop:

1. `docker info`: CLI WSL é stub e pede habilitar integração.
2. Sockets `/var/run/docker.sock`, `/run/docker.sock` e socket Docker Desktop inspecionados ausentes.
3. `docker.exe version`: cliente Windows 29.4.2 disponível, mas pipe
   `dockerDesktopLinuxEngine` ausente; não existe daemon acessível.

Falha de setup não é Red funcional. Não houve tentativa de correção de código nem falha
funcional. Tracking registra um evento FAILURE de ambiente, com referência a este checkpoint.
D-17 no plano limita diagnósticos e registra ausência de custo financeiro mensurável.
O coordenador informou ao usuário a necessidade de iniciar Docker Desktop e ativar WSL.

## Provas, revisão e entrega

`harness_completion.py handoff docs/tasks/CT-001/plano.md --stage local` executado:
`BLOCKED`, `completion_allowed: false`, `stage_allowed: false`.
AC1–AC6/BDD1–BDD3, Red/Green/regressão, coesão, revisão Sol, CI push/PR e aceite humano
permanecem PENDING. O gate aponta corretamente evidência funcional/revisão ausentes,
checklist incompleto e bloqueio de ambiente; nenhuma aprovação local ou externa foi alegada.
História normativa e README de estudo permanecem intactos. `git diff --check` passou.
Não há receipts de testes; o handoff não é evidência funcional.

Ownership foi adquirido, usado para registrar o bloqueio e heartbeat, e liberado
voluntariamente ao encerrar este checkpoint. A retomada deve adquirir posse novamente
por `feature_tracking.py start CT-001 --owner <execução-real>`; não há necessidade de
contornar lock/recover. Credenciais antigas permanecem somente na área administrativa Git.

## Próxima ação executável

1. Confirmar daemon com `docker info` e `docker compose version` após ação no Desktop/WSL.
2. Conferir branch/diff, reler plano e adquirir ownership antes de escrever.
3. Reconciliar scope prospectivo e versões reais; preparar setup e teste HTTP em Docker;
   obter Red pelo comportamento ausente com DB/Redis saudáveis antes do código produtivo.
4. Seguir plano para Green, recuperação/persistência, coesão, revisão Sol independente,
   commit seletivo/CI/PR. Nunca transformar falta de ambiente em PASS ou N/A.

Não iniciar CT-002. Alterações deste checkpoint permanecem locais e revisáveis.

## Retomada — Docker disponível

Usuário autorizou iniciar Docker Desktop. Daemon Linux/Windows 29.4.2 e Compose 5.1.3
confirmados. Ownership readquirido por `/root/ct001_execucao`; Kanban Doing. Preparo de
setup/teste antes do Red; todos os gates funcionais continuam PENDING até execução.

### Setup em construção

Pull público resolvido com DOCKER_CONFIG privado vazio (helper Windows falhava).
Imagens por digest e dependências Python congeladas em Docker. Compose, scaffold ASGI
sem rotas e três testes HTTP/dependências criados. Build api/smoke em execução; Red pendente.

### Red funcional observado

Build e DB/Redis saudáveis. `docker compose --env-file .env.example -p clinic-ai-ct001-red
run --rm --no-deps smoke` retornou exit1: 2 failed (HTTP404 em rotas de saúde contratadas
ainda ausentes) e 1 passed (distância pgvector real e PING Redis). Log privado:
`.git/harness/ct001-red.log`. API estava em processo separado; sem falha de import/setup.
Após esse Red, bootstrap de saúde e smoke de falhas/persistência implementados; Green pendente.

### Green e coesão

`make smoke` exit0, log `.git/harness/ct001-green.log`: 16 assertions pytest em seis
fases, runtime não root sem gcc/pytest, SQL/Redis preservados após down/up. Volumes
preservados. Coesão revista; sem refatoração adicional necessária. Unitários redundantes
não criados; decisões críticas exercitadas em integração HTTP real. Emitindo receipt funcional
sobre o scope final; revisão Sol e CI ainda pendentes.

### Receipt funcional

Gate `functional` PASS, exit0, 73.65s. Receipt local `.git/harness/CT-001/functional/latest.json`
e run `4e9542fb53e14021ad769e697b2a092a`. Fonte `fa5fd500a4142c1745bf8e9172a235c5ba252d052c9523229fad7c031999e474`; scope `3c4043a6630e3a35e7964a7413645cec913bddf404d3cd5a39c68909d3679fbb`;
contrato `b81c337e79a587fd5ae2f9683874d037b90baff917cf9130a83b26bdac315d75`. Revisão Sol iniciada em execução separada; primeira
tentativa teve erro de capacidade antes de revisar, segunda tentativa no mesmo modelo.
CI push/PR e aceite humano PENDING; nenhum PR/commit ainda.

### Revisão independente

Sol `/root/ct001_execucao/ct001_revisao` concluiu APPROVED local; effort não exposto.
Parecer integral em `revisao.md`, vinculado aos hashes do receipt funcional no plano.
Sem achados bloqueantes; CI/PR/humano permanecem PENDING. Prosseguindo gate local/commit/push.

### Gate local

`check --stage local`: LOCAL_READY, stage_allowed=true, completion_allowed=false,
sem erros. Staging seletivo/diffcheck passou. Commit/push da branch autorizados em seguida.
