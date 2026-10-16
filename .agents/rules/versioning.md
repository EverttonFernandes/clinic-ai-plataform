---
name: versioning
description: "Aplicar Conventional Commits e SemVer sem confundir código concluído com release publicada."
applies_when:
  - "preparar commit, tag, PR, push ou release"
progressive_disclosure:
  - Ler nome, descrição e condições antes do corpo.
  - Abrir apenas o detalhe necessário ao estado da tarefa.
  - Consultar complementos somente se a condição se aplicar.
conditional_details:
  - if: "commit está autorizado"
    then: "staging seletivo e Conventional Commit que descreva o resultado"
  - else_if: "release/tag foi pedida"
    then: "calcular SemVer pelo contrato público e validar digest/commit de integração"
  - else_if: "push autorizado dispara CI"
    then: "verificar run do SHA publicado; falha retorna à correção"
  - else: "entrega local sem pedido de versionamento"
    then: "registrar status local; não criar commit/tag/push implicitamente"
---

# Commits e versões

Formato: `tipo(escopo): descrição`, com corpo quando esclarecer motivo/validação.
Escopo e marcador `!` são opcionais; o marcador antes de `:` indica ruptura de contrato.
Usar feat, fix, docs, test, refactor, ci, build, perf ou chore conforme mudança real.
`!`/BREAKING CHANGE explicita incompatibilidade; não inventar coautoria ou email.

SemVer: definir API pública e contrato de versão. Em API estável, correção compatível é PATCH,
funcionalidade compatível MINOR e ruptura MAJOR. Desenvolvimento 0.y.z tem contrato inicial
instável, mas rupturas continuam explícitas. Não criar versão/tag agora apenas por existir planejamento.

Histórias só chegam a Done após critérios/provas/entrega, revisão de outro modelo, CI e
revisão/merge do usuário. Manutenção local fora de história não implica publicação.
Release exige adicionalmente versão, changelog,
commit/digest e validação de publicação quando contratada. Se história exigir release,
esse gate não pode ser omitido do plano. Não exigir uma tag por ajuste documental.

Antes de commit: diff completo, staging seletivo, `git diff --cached --check`, gates por impacto
e inspection de secrets/ignorados. Nunca `git add .` indiscriminado, --no-verify, force push ou mover tag.

Fluxo obrigatório por história: [branch/PR e aceite humano](story-delivery.md), CI do SHA real.
Tag de release aponta para
commit de integração aprovado, não para SHA antigo anterior ao merge. Verificar tag com
`git rev-parse <tag>^{}`; registrar versão e digest, sem refazer artefato na promoção.
Depois de push autorizado, acompanhar CI; falha não pode ser anunciada como release validada.
Sem workflow existente, declarar ausência, sem inventar CI verde.

Referências: [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
e [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html).
