# Ambiente isolado e CI/CD planejados

CT-001 implementa Dockerfile, Compose, API mínima, smoke real e workflow Application CI.
Os comandos build/up/down/smoke abaixo estão disponíveis; os demais continuam planejados.
O [harness de desenvolvimento](harness.md) é separado da aplicação. Evidências e pendências
remotas estão no [plano CT-001](../tasks/CT-001/plano.md); existir workflow não significa CI verde.

## Operação disponível — CT-001

Requisitos do host: Docker Engine/Compose funcionando e Make/Bash para os atalhos;
Python, pip, pytest e dependências da aplicação rodam apenas nos containers.
Validado em Docker Desktop/WSL com Engine 29.4.2 e Compose 5.1.3, Linux amd64.
Não há garantia de outras arquiteturas sem executar o smoke correspondente.

| Componente | Versão resolvida e travamento |
| --- | --- |
| Python | 3.13.18, base slim-bookworm por digest no Dockerfile |
| PostgreSQL / pgvector | 17.11 / 0.8.7, imagem oficial pgvector por digest no Compose |
| Redis servidor | 7.4.12, imagem oficial por digest no Compose |
| FastAPI / Uvicorn | 0.162.0 / 0.54.0 |
| psycopg / redis cliente | 3.3.8 / 7.4.1 |
| pytest | 9.2.0, somente target test |

`requirements.txt` e `requirements-test.txt` fixam também dependências transitivas,
resolvidas via pip em containers da mesma base. Atualização exige nova resolução explícita,
revisão e smoke; as tags legíveis das imagens estão acompanhadas de digest imutável.
Referências dos mantenedores: [FastAPI no PyPI](https://pypi.org/project/fastapi/),
[pgvector Docker](https://github.com/pgvector/pgvector#docker).

```sh
# Configuração sintética incluída; nenhum .env privado é necessário.
make build
make up
curl --fail http://127.0.0.1:8000/health/live
curl --fail http://127.0.0.1:8000/health/ready
make down

# Opcional: personalizar arquivo local ignorado, nunca versionar secrets.
cp .env.example .env
make up ENV_FILE=.env
make down ENV_FILE=.env

# Build, HTTP, pgvector/Redis reais, falhas, recuperação e persistência.
make smoke
```

Projeto habitual `clinic-ai-dev`; `COMPOSE_PROJECT_NAME` e `API_PORT` podem ser alterados
na configuração. API escuta internamente em 8000, publicada somente em `127.0.0.1:8000`.
PostgreSQL 5432 e Redis 6379 são internos à rede do projeto, sem portas publicadas.
O perfil padrão sobe API/DB/Redis; `test` contém somente o cliente pytest. Worker, scanner,
balanceador e serviços de observabilidade ainda não entram neste incremento.

`/health/live` responde 200/`alive` quando o processo atende. `/health/ready` consulta
PostgreSQL (incluindo extensão vector) e Redis, respondendo 200/`ready` ou 503/`unavailable`.
Não retorna mensagens internas/credenciais e não promete reserva/consumo de IA implementados.
Timeouts limitam conexão e consultas; não há retries de Redis escondidos nesta sonda.
API usa UID/GID 10001, filesystem somente leitura, sem capabilities e sem pytest/compilador.
PostgreSQL e Redis usam seus entrypoints oficiais para preparar volumes e reduzir privilégios;
não é necessário forçar UID incompatível com inicialização de volume novo.

Credenciais do exemplo são públicas e exclusivamente sintéticas; a API usa a role de
bootstrap do laboratório. Privilégios de domínio/migrations serão tratados em CT-004/005.
O volume PostgreSQL inicializa apenas a extensão vector. Não usar este ambiente com dados
reais nem expor as portas publicamente. Mudar POSTGRES_* não reconfigura volume já inicializado.

### Falha e recuperação sem apagar dados

```sh
docker compose --env-file .env.example stop postgres
curl -i http://127.0.0.1:8000/health/ready # 503
curl --fail http://127.0.0.1:8000/health/live # 200
docker compose --env-file .env.example up -d --wait --wait-timeout 120 api
curl --fail http://127.0.0.1:8000/health/ready # 200 após recuperação
```

Repetir com `redis` exercita a outra dependência. Não remover volumes para recuperar saúde.
`make down` remove containers/rede e preserva volumes nomeados PostgreSQL/Redis; `make up`
reutiliza os dados. Redis usa AOF; persistência após parada normal não promete ausência de
perda em crash, HA ou recuperação confiável de quotas futuras. Falhas de inicialização:
conferir `docker compose --env-file .env.example ps` e logs somente do serviço afetado,
sem publicar dados sensíveis. Docker Desktop/WSL precisa estar iniciado/integrado.

Smoke cria projeto único `clinic-ai-test-<timestamp>-<pid>`, credenciais sintéticas próprias,
porta de API aleatória em loopback e volumes separados do desenvolvimento. Ele escreve e
confere marcadores PostgreSQL/Redis após down/up, além de verificar leitura vetorial real.
O trap encerra apenas seu projeto; volumes são preservados até inspeção/remoção manual
explícita pelo operador. Nenhum comando automatizado usa `down -v`. Em CI, o runner é efêmero.
O script imprime o nome do projeto para identificar esses volumes sem adivinhar nomes.

Se o helper de credenciais Docker Desktop falhar no WSL, investigar integração/daemon;
um diretório temporário `DOCKER_CONFIG` vazio permite imagens públicas sem alterar o
arquivo de credenciais do usuário. Não copiar tokens para scripts, docs ou logs.

## Unidade de entrega do monólito modular

Frontend e backend pertencem a este repositório e à mesma release. Assets do chat são
incluídos no artefato servido pela aplicação. API e worker compartilham imagem/código e
versão, iniciados por entradas distintas. Jobs separados de build/teste na CI podem
validar partes do repositório, sem publicar um serviço por módulo de negócio.

CT-022 escala réplicas completas da API e processos do worker. PostgreSQL, Redis, scanner
e proxy de modelos opcional têm ciclos técnicos próprios; não são contextos de negócio
extraídos. Estrutura e fronteiras: [mapa DDD](arquitetura-ddd.md#unidade-de-repositório-aplicação-e-release).

## Perfis de ambiente

| Perfil | Finalidade | Recursos |
| --- | --- | --- |
| Desenvolvimento | Jornada local com dados sintéticos. | API/worker, PostgreSQL+pgvector, Redis e volume documental privado. |
| Teste | Validação reproduzível sem afetar desenvolvimento. | Projeto Compose, banco, Redis e storage independentes; provider controlado. |
| Documentos | Testar validação de arquivos. | Scanner em Docker e limites de parser; indisponibilidade impede indexação. |
| Escala local | Duas instâncias e worker concorrente. | Balanceamento + estado compartilhado; introduzido em CT-022. |
| Homologação | Integrações externas e ensaio de release. | Infra, identidade, TLS, storage, KMS e secrets definidos em CT-024. |

Não subir todos os componentes opcionais no primeiro commit. Começar por API/DB/Redis;
adicionar worker, scanner e balanceamento na história consumidora. Readiness verifica condições
de atendimento; liveness verifica processo. Ordem de criação não significa disponibilidade:
usar healthchecks e condição de saúde para dependências, conforme [Docker Compose](https://docs.docker.com/compose/how-tos/startup-order/).

Scanner inicial candidato: ClamAV em container, para realizar a [verificação de arquivos](https://docs.clamav.net/manual/Usage/Scanning.html)
requerida pelo desenho. Database de assinaturas e disponibilidade precisam ser verificadas;
scanner fake é útil em unitários, mas não satisfaz o gate de integração.

## Interface local proposta

O perfil habitual usa apenas os componentes exigidos pela jornada atual. Scanner,
balanceador, ferramentas de observabilidade e experimentos externos ficam sob demanda;
encerrar o experimento sem remover volumes de desenvolvimento. Não manter homologação
cloud permanente. Registrar recursos e duração dos ensaios conforme a
[política de proporcionalidade](decisoes.md#proporcionalidade-e-orçamento-do-projeto-pessoal).
O consumo de CI também deve ser limitado: cancelar runs obsoletos, reaproveitar cache
de build e evitar matrizes redundantes; preservar os checks obrigatórios do SHA atual.

| Comando futuro | Contrato a implementar | História |
| --- | --- | --- |
| `make up` | Disponível: construir/iniciar desenvolvimento, esperar saúde. | CT-001 |
| `make down` | Disponível: parar sem remover volumes. | CT-001 |
| `make migrate` | Aplicar migrations explicitamente e reportar versão. | CT-004 |
| `make seed-demo` | Criar dados sintéticos de forma repetível sem sobrescrever dados reais. | CT-004 |
| `make test-unit` | Executar unitários em Docker, falhando se houver erro. | CT-002 |
| `make test-integration` | Componentes reais em ambiente de teste isolado. | CT-002 |
| `make test-functional` | Cliente HTTP contra API em processo separado. | CT-002 |
| `make test-security` | Rodar casos de fronteira/isolamento implementados. | Incremental; CT-020 consolida |
| `make test-concurrency` | Rodar disputas reais e verificar estado final. | C-004 e CT-021 |
| `make eval-offline` | Dataset sem APIs pagas por padrão. | CT-015 |
| `make quality` | Análise estática/format e verificações disponíveis. | CT-003 |
| `make test` | Matriz local completa aplicável; uso em integração final/risco transversal. | Incremental |
| `make test-load` | Carga sintética declarada em ambiente descartável. | CT-021 |
| `make smoke` | Disponível: HTTP, falhas, recuperação e persistência reais. | CT-001, expandido por marco |

Alvos não disponíveis ainda devem ser apresentados como planejados, nunca como comando
bem-sucedido. Não criar `make clean` que apague volumes por padrão. A automação de teste só
pode remover recursos exclusivos e identificados da própria execução.

## CI incremental — GitHub Actions

### CT-001: CI mínima desde a primeira história

- Criar `.github/workflows/application.yml`, nome `Application CI`, de push de branches e PR com build Docker e smoke reais
  do incremento CT-001 (API/DB/Redis e recuperação), sem suítes vazias ou sucesso artificial.
- `Harness contracts` é separado; sozinho não comprova a aplicação.
- Push da branch → CI do HEAD verde → abrir PR. Checks disparados pelo PR também devem passar.
- CT-002 incorpora testes isolados à pipeline existente na mesma história.

### CT-003: consolidar a pipeline

- PR e push de branches/main: checkout, build Docker, análise e testes/smoke já implementados.
- Jobs com timeout, permissões mínimas, concorrência e relatórios sanitizados como artifacts.
- Não inserir gates vazios ou sucesso artificial para suítes ainda inexistentes.
- Rodar sem secrets de inferência ou deploy; nenhuma chamada paga ou mensagem externa.

### Durante as histórias

Cada teste entra na CI na história que cria o comportamento. Segurança, integração e concorrência
não aguardam CT-025. Manter desenvolvimento e runner alinhados em versões e comandos Docker.
Testes funcionais inicializam a API e usam HTTP; não substituir tudo por cliente in-process.
Cada história usa branch com ID, revisão Sol distinta do executor Astra/medium e CI do SHA
antes do PR. O usuário revisa e faz merge; até lá, Review. A automação não faz merge.
CD é incremental: não se exige deploy nas primeiras histórias nem se alega CD validado
sem destino real. CT-025 cobre publicação/promoção autorizadas e suas evidências.

### CT-025: release e promoção

1. Build/format/análise, unitários, integração/migrations, funcionais, segurança e concorrência.
2. Dataset determinístico offline; avaliação real de mudança de modelo/provider quando autorizada.
3. Imagem de runtime sem secrets, inventário de dependências, scan com política explícita e smoke.
4. Identificar artefato por SHA/digest; publicar no registry apenas em contexto autorizado.
5. Promover o mesmo digest à homologação; smoke e jornada crítica pós-deploy.
6. Promoção controlada ao ambiente real após critérios operacionais; rollback ensaiado.

Sem infraestrutura ou secrets, o job de deploy não é sucesso de publicação. O gate fica
PENDING com motivo. Não usar `pull_request_target` para executar código não confiável com secrets.
Migrations exigem compatibilidade com runtime anterior; rollback de aplicação não é apagar dados
ou assumir reversão automática de schema.

Os [ambientes do GitHub Actions](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)
permitem associar secrets e regras de proteção a jobs. Verificar disponibilidade no plano e
visibilidade do repositório antes de depender de reviewers/proteções específicas. Esta preparação
não configura ambientes remotos; se o recurso não existir, definir promoção manual verificável.

## Segredos, rede e persistência

- `.env.example` só documenta chaves e valores sintéticos seguros; `.env` real fica ignorado.
- Credenciais de provider/WhatsApp, registry, KMS e storage ficam fora de código/logs/artifacts.
- Rede local restrita; banco/Redis não publicados desnecessariamente. TLS termina na fronteira real.
- Roles de banco por função com mínimo privilégio, storage privado e política de criptografia/rotação.
- Jobs/outbox no PostgreSQL são a escolha inicial; medir antes de acrescentar broker.
- Backup inclui dados e documentos/metadados coerentes; restore testa permissões, versões e idempotência.
- Readiness de Redis não basta para liberar consumo após perda de estado: recuperar quotas/reservas antes.

## Critérios de publicação

Destino, budget, responsáveis, acesso, TLS/KMS, retenção, backups, alertas, SLOs e runbook
precisam estar definidos. Nunca usar dados reais para testar uma preparação ainda incompleta.
CI verde não comprova, sozinha, disponibilidade de produção ou qualidade do modelo real.
