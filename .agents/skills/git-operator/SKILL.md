---
name: git-operator
description: "Preparar commits e releases autorizados da Clínica IA com Conventional Commits, SemVer e evidência do SHA correto."
metadata:
  progressive_disclosure:
    - Ler nome e descrição para decidir aplicabilidade.
    - Abrir somente a skill e as referências necessárias ao passo atual.
  conditional_details:
    - if: "commit autorizado"
      then: "staging seletivo e gates pertinentes"
    - else_if: "release/tag autorizada"
      then: "SemVer e correspondência entre tag, commit aprovado e artifact"
    - else_if: "push autorizado"
      then: "verificar CI do SHA publicado e reabrir falha"
    - else: "revisão local"
      then: "não executar mutações Git por ler esta skill"
---

# Git e release

Aplicar [versioning](../../rules/versioning.md) e [delivery](../../rules/delivery.md).
Histórias seguem [story-delivery](../../rules/story-delivery.md): criar branch com ID,
commitar/push e abrir PR estão autorizados para a história solicitada. Revisar com outro
modelo e obter CI verde no HEAD antes do PR; acompanhar os novos checks após abertura.
Usar [template do PR](../../../.github/pull_request_template.md) com instruções de estudo e
reprodução, critérios/evidências, decisões e limitações. Corpo longo via arquivo, sem escapes
de shell; selecionar arquivos individualmente. Preservar mudanças preexistentes.
Deixar Review para o usuário: nunca `gh pr merge`, auto-merge ou aprovação em nome dele.
Inspecionar status/diff, arquivos novos/ignorados e trabalho preexistente antes de staging.
Usar mensagem convencional que descreva problema/resultado e corpo com validação quando útil.

Selecionar SemVer pelo contrato público e efeito agregado desde a release anterior.
Propor versão/changelog quando ainda não autorizada a publicação. Não criar tag por rotina,
inventar autoria, forçar push, mover tag ou executar --no-verify.

Em branch/PR, validar CI do SHA realmente integrado. Tag de release aponta para esse commit
aprovado; artifact é identificado por digest. Uma CI de branch antiga não aprova novo SHA.
Não incluir prompts locais, logs privados ou trabalho alheio. Reportar exatamente o que foi
commitado/publicado e o que permanece local, sem executar release implícita.
