---
name: delivery
description: "Relatar estado real de validação e limitar efeitos de Git, CI e deploy ao escopo autorizado."
applies_when:
  - "conforme condição da tarefa"
progressive_disclosure:
  - Ler nome, descrição e condições antes do corpo.
  - Abrir apenas o detalhe necessário ao estado da tarefa.
  - Consultar complementos somente se a condição se aplicar.
conditional_details:
  - if: "conclusão local"
    then: "evidence-backed-completion.md e entrega sem alegação de publicação"
  - else_if: "Git ou release"
    then: "versioning.md e CI do SHA real quando disparada"
  - else: "somente planejamento"
    then: "não publicar para demonstrar documento"
---

# Entrega e CI/CD

- Mudança documental não exige publicar para ser revisável. Não fazer commit/push/deploy implicitamente.
- História solicitada tem autorização persistente para branch/commit/push/PR, conforme
  [story-delivery](story-delivery.md); review e merge são do usuário. Não executar merge automático.
- Antes de versionar, inspecionar diff, arquivos ignorados e evidências; prompts antigos continuam privados.
- CI planeja e executa gates existentes; teste sem execução ou pipeline inexistente não pode ser PASS.
- Imagem de release por digest/SHA, sem secrets; promover o mesmo artefato e validar smoke/rollback.
- Não publicar artefatos nem conceder secrets a PRs não confiáveis; ambiente de deploy precisa estar configurado.
- Falta de destino/credencial deixa o gate externo PENDING, não justifica removê-lo.
- Nunca apagar volume de desenvolvimento para limpar testes ou recuperar deployment.

Detalhes de etapas em [ambientes e CI/CD](../../docs/spec-driven-development/ambientes-e-cicd.md).
