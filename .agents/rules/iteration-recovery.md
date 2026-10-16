---
name: iteration-recovery
description: "Conservar incidente e trocar investigação após falhas recorrentes, sem loop infinito."
applies_when:
  - "falha de gate, correção rejeitada ou interrupção"
progressive_disclosure:
  - Ler nome, descrição e condições antes do corpo.
  - Abrir apenas o detalhe necessário ao estado da tarefa.
  - Consultar complementos somente se a condição se aplicar.
conditional_details:
  - if: "três correções verificadas falharam no mesmo incidente"
    then: "usar bug-resolution com hipótese nova e prova da causa"
  - else_if: "impasse técnico comprovado antes disso"
    then: "escalonar investigação sem gastar tentativas repetidas"
  - else_if: "há experimento distinto executável"
    then: "corrigir, verificar e devolver ao QA"
  - else: "depende de informação/acesso/custo externo"
    then: "registrar bloqueio concreto e ação mínima necessária"
---

# Recuperação de iterações

Uma tentativa é hipótese + mudança + verificação; leitura de log não conta como correção.
Contar por incidente, não pela soma de problemas da história. Guardar esperado/observado,
reprodução, revisão/ambiente, tentativas, causas refutadas e próxima ação em
`docs/tasks/<ID>/incidentes/<incidente>.md`.

A fila de correções conserva IDs; não renomear para zerar contador. Ao chegar a três
correções rejeitadas, parar edições por palpite e usar [bug-resolution](../skills/bug-resolution/SKILL.md).
Continuar exige experimento novo sustentado por evidência, não outra persona para repetir a tentativa.

Correção candidata retorna ao QA; não autoaprovar a mudança. Se revisão independente
não estiver autorizada/disponível, registrar revisão sequencial com limite explícito.
Ambiente ausente deixa gate PENDING. Persistir progress/handoff antes de interrupção;
não gravar raciocínio privado, secrets ou telemetria inventada.

Não esperar número arbitrário de loops para salvar contexto. Não transformar esgotamento
de tentativas em Done, nem reduzir critério/teste para encerrar a história.
