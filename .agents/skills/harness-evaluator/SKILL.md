---
name: harness-evaluator
description: "Avaliar comportamento do harness Clínica IA com casos determinísticos e rubrica de LLM-as-a-Judge; não confundir com evals do produto."
metadata:
  progressive_disclosure:
    - Ler nome e descrição para decidir aplicabilidade.
    - Abrir somente a skill e as referências necessárias ao passo atual.
  conditional_details:
    - if: "scripts de gate/tracking mudam"
      then: "rodar contratos positivos e negativos em Git temporário"
    - else_if: "instruções/skills mudam"
      then: "avaliar roteamento, completude e handoff pela rubrica"
    - else_if: "judge remoto solicitado"
      then: "verificar autorização, budget, dados sintéticos e calibração"
    - else: "qualidade do assistente clínico"
      then: "usar pipeline de evals do produto"
---

# Avaliar o harness

Ler [evals e rubrica](../../../docs/spec-driven-development/evals-harness.md) e a
[regra de evals](../../rules/harness-evals.md). Avaliar a demanda bruta, fontes originais,
mudanças reais e provas; evitar apresentar ao avaliador a conclusão esperada do executor.

Executar contratos que tentam obter Done indevido, omitir dependência/critério, reutilizar
prova desatualizada, ignorar ownership ou confundir fake com integração real.
Depois revisar suficiência das regras e o caminho demanda → skill → gate → evidência → próxima ação.

LLM-as-a-Judge pode auxiliar o parecer sem substituir assertions nem autorização.
Separar resultado executado de cenário apenas percorrido conceitualmente. Se o próprio
executor fizer revisão sequencial, registrar fallback e limite; não inventar sessão independente
ou calibração humana. Retornar findings acionáveis e apontar todo gate ainda pendente.
Esse fallback não satisfaz histórias C/CT, que exigem independent-review e os modelos
configurados. Exercitar também branch errada, CI de outro SHA e tentativa de Done antes do usuário.
