---
name: story-delivery
description: "Branch, revisão por outro modelo, CI e PR de cada história; conclusão somente após revisão e merge do usuário."
applies_when:
  - "executar, revisar ou entregar história C/CT"
progressive_disclosure:
  - Abrir esta regra no início e na entrega, não em consulta documental isolada.
conditional_details:
  - if: "início da história"
    then: "conferir modelo, dependências e criar branch com ID"
  - else_if: "implementação validada"
    then: "revisão independente, push, CI e PR"
  - else: "aguardando usuário"
    then: "Review até revisão e merge; preservar handoff"
---

# Entrega por história

A instrução do usuário autoriza branch, commits seletivos, push e abertura de PR para
cada história solicitada. Não autoriza merge pelo agente, auto-merge, release, deploy
ou execução de todo o backlog. Preparação documental não inicia CT-001.

1. Ler [política](../harness-policy.json). Executar com `gpt-6-astra`/`medium`. Se a sessão
   não expõe essa identidade, encaminhar a execução ao modelo explicitamente selecionado
   numa ferramenta que o suporte; não registrar o modelo por suposição. Coordenador não
   edita simultaneamente ao executor. Revisão: `gpt-6-sol`, outra execução.
2. Dependências Done e main atualizada; preservar alterações anteriores. Criar
   `story/<ID>-<slug>` (ex.: `story/CT-001-ambiente-docker`) a partir da base integrada.
   Não renomear branch existente nem carregar trabalho de outra história silenciosamente.
3. BDD/TDD, testes por impacto, refatoração do código **e dos testes** quando necessária.
   [Revisão independente](../skills/independent-review/SKILL.md) após validação; corrigir
   achados até novo parecer válido. Qualquer alteração relevante invalida a prova anterior.
4. `check <plano> --stage local`; commits Conventional com staging seletivo. Push da branch.
   Rodar o coletor pelo gate `ci`; precisa dos workflows configurados no HEAD exato.
   CI mínima da aplicação começa em CT-001 (`.github/workflows/application.yml`, nome
   `Application CI`); não aceitar apenas contratos do harness. Exigir evento push.
5. `check <plano> --stage pre-pr`. Abrir PR para main com o [template](../../.github/pull_request_template.md)
   e corpo por arquivo (`gh pr create --body-file ...`). Incluir evidências e explicação útil
   ao estudo. Coletar gate pr_ci (modo pr) e executar `check --stage post-pr`: exigir
   evento pull_request e associação ao PR/HEAD atuais; falha retorna ao loop.
6. Atualizar Review e informar URL, SHA, CI e roteiro de revisão. Parar o avanço do backlog
   enquanto o usuário revisa. Não aprovar em nome do usuário, não acionar `gh pr merge`
   nem habilitar auto-merge. Pedido de alteração retorna ao loop da mesma história.
7. Após o usuário revisar e fazer merge, coletar `human_review`, executar check final e
   `finish`; reconciliar Done no Kanban. Merge pelo login configurado é o sinal verificável
   de aceite. Isso não exige uma aprovação formal do próprio autor na interface do GitHub.

CI verde é evidência do SHA, não garantia de ausência de defeitos. O coletor usa apenas GETs
da API do GitHub; falta de autenticação/run/merge fica PENDING. Identidade de modelo e uso
humano da conta são cooperantes: metadata local e token compartilhado não autenticam pessoas.
Proteções remotas e controle de credenciais são complementares, não configurados por esta regra.
