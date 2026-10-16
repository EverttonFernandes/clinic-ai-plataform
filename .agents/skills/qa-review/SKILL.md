---
name: qa-review
description: "Revisar critérios, diff e evidências da história Clínica IA sem implementar a própria aprovação."
metadata:
  progressive_disclosure:
    - Ler nome e descrição para decidir aplicabilidade.
    - Abrir somente a skill e as referências necessárias ao passo atual.
  conditional_details:
    - if: "gates de execução disponíveis"
      then: "confrontar critérios originais e fontes de evidência"
    - else_if: "falta execução ou ambiente"
      then: "rejeitar conclusão e manter PENDING/FAIL"
    - else: "história sem revisor de outro modelo"
      then: "revisão PENDING; não substituir por persona ou fallback"
---

# QA e revisão final

Ler [escopo](../../rules/review-scope.md), [evidências](../../rules/test-evidence-quality.md)
e [conclusão](../../rules/evidence-backed-completion.md).

Entrada: história original, plano, diff incluindo arquivos novos, comandos/logs e hashes.
Não usar o resumo otimista do executor como prova. Conferir todos os AC e BDD extraídos.
Não exigir unitário redundante para cada critério quando integração/funcional é a prova correta.

Reprovar: critério omitido, mock no lugar de integração exigida, assertion enfraquecida,
teste ignorado, sucesso sem efeito persistido, scope reduzido, PII/secret ou gate externo não executado.
Validar fonte de verdade, isolamento, custo, concorrência e fronteiras conforme risco.
UI Web exige jornada e estados reais quando afetada, sem copiar gates mobile.

Saída: APPROVED ou REJECTED, critério → evidência, achados por severidade, riscos,
ações corretivas e decisão de continuidade. Não corrigir código no mesmo passo de aprovação;
devolver achados ao executor e revisar a nova revisão depois.

Para histórias, usar [independent-review](../independent-review/SKILL.md). Registrar
modo/modelos/identidades reais e hash do parecer. Independência exige outra execução e
outro modelo configurado; manutenção histórica com fallback conserva essa limitação.
O parecer pré-PR avalia o estágio local; CI e aceite humano são gates posteriores obrigatórios,
não falhas a disfarçar nem motivo para impedir a própria criação do PR.
