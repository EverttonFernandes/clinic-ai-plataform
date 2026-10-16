# Ambiente isolado e CI/CD planejados

Este documento define contratos para futuras histórias. **Não há Dockerfile, Compose,
Makefile, testes da aplicação ou workflows do produto criados por esta preparação.** O harness de desenvolvimento
tem [utilitários e contratos locais](harness.md), separados da futura aplicação. Comandos abaixo são a interface
proposta para CT-001/CT-002 e CT-025 implementarem, não instruções já executáveis.

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

| Comando futuro | Contrato a implementar | História |
| --- | --- | --- |
| `make up` | Construir/iniciar ambiente de desenvolvimento, esperar dependências saudáveis. | CT-001 |
| `make down` | Parar sem remover volumes. | CT-001 |
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
| `make smoke` | Readiness e jornada mínima do artefato real. | CT-001, expandido por marco |

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
