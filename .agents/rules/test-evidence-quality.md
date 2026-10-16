---
name: test-evidence-quality
description: "Distinguir evidência funcional real de simulação e escolher testes por impacto."
applies_when:
  - "conforme condição da tarefa"
progressive_disclosure:
  - Ler nome, descrição e condições antes do corpo.
  - Abrir apenas o detalhe necessário ao estado da tarefa.
  - Consultar complementos somente se a condição se aplicar.
conditional_details:
  - if: "selecionar testes"
    then: "rastrear consumidores e risco antes dos comandos"
  - else_if: "declarar PASS"
    then: "exigir execução, ambiente, revisão e efeito verificável"
  - else: "ambiente ou acesso ausente"
    then: "registrar PENDING; N/A somente para inaplicabilidade"
---

# Evidências e testes

- Testar comportamento, autorização e efeito persistido; status HTTP sozinho é insuficiente.
- Funcional acessa processo HTTP separado; integração de banco usa PostgreSQL/pgvector/Redis reais.
- Dobrar somente a fronteira externa necessária. Provider controlado não prova qualidade de LLM real,
  assinatura local não prova WhatsApp externo e fake de KMS não prova criptografia de produção.
- Fixtures sintéticas, namespace/banco/storage de teste próprios e cleanup limitado a esses recursos.
- Concorrência exige chamadas realmente sobrepostas e inspeção do estado final.
- Selecionar testes alterados e consumidores afetados; ampliar para suíte integrada por risco transversal.
- Cobertura pode revelar lacunas, sem meta percentual arbitrária ou testes que repetem o código.
- Não apagar assertion, mascarar erro, ignorar teste ou alterar spec para obter verde.
- Revisar também os testes: uma falha real no comportamento deve fazer a suíte falhar.
  Cobrir negativos/fronteiras relevantes, autorização, rollback/idempotência e estado final;
  não aprovar teste só porque o nome corresponde ao critério. Unitários focam regras/decisões;
  integração exercita contratos reais; funcionais provam jornadas e efeitos de ponta a ponta.
- Refatorar fixtures, duplicação ou acoplamento que escondam defeitos, preservando a força
  das assertions. Falha controlada/mutação dirigida pode demonstrar detecção quando houver dúvida;
  não impor ferramenta de mutation testing ou cobertura arbitrária a toda história.
- Registrar comando, ambiente, revisão/diff e resultado; PASS, FAIL e PENDING são distintos.

Consultar [estratégia](../../docs/spec-driven-development/testes.md) e
[template de entrega](../../docs/entregas/TEMPLATE.md). Não fabricar relatórios ou screenshots.
