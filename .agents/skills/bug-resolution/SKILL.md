---
name: bug-resolution
description: "Investigar causa raiz de falha recorrente da Clínica IA após três correções rejeitadas no mesmo incidente ou impasse comprovado."
metadata:
  progressive_disclosure:
    - Ler nome e descrição para decidir aplicabilidade.
    - Abrir somente a skill e as referências necessárias ao passo atual.
  conditional_details:
    - if: "três tentativas falharam no mesmo incidente"
      then: "confirmar reprodução e hipótese nova antes da edição"
    - else_if: "impasse comprovado"
      then: "investigar causa antes do limite de tentativas"
    - else: "falha inicial com causa clara"
      then: "manter fluxo normal do executor/QA"
---

# Diagnóstico de falha recorrente

Entrada: incidente persistido, critério original, esperado/observado, reprodução, revisão,
ambiente, logs sanitizados e tentativas anteriores. Dado desconhecido permanece UNKNOWN.
Consultar [recuperação](../../rules/iteration-recovery.md).

Reproduzir a menor falha e separar sintoma de causa. Formular hipótese falsificável e um
experimento de cada vez. Não repetir hipótese refutada sem nova evidência. Rastrear fronteiras,
dados, concorrência e consumidores, sem enfraquecer assertion ou usar retry/sleep para esconder erro.

Antes da correção, fixar regressão conforme BDD/TDD. Corrigir causa com diff limitado,
revisar coesão e validar consumidores. Devolver ao QA causa comprovada, mudança, comandos,
resultados, incertezas e riscos; não aprovar a própria correção.

O coordenador mantém ownership; esta skill não inicia outro escritor ou zera contador.
Nova rodada precisa de experimento distinto executável. Ausência de caminho técnico
requer handoff concreto; não loop infinito ou falso Done.
