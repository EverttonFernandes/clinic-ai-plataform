# C-009 — FAQ com RAG e fontes

Marco: M4. Tipo: negócio.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Como paciente, obter respostas documentais com fontes e limite explícito de evidência.

## Vínculos e dependências

- Requisitos: `RF-08`, `RF-10`, `RNF-05`, `RNF-09` — [especificação](../../../spec.md).
- Dependências: [CT-013](../historias-tecnicas/CT-013-retrieval-pgvector.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Integrar Agent → searchClinicKnowledge → gateway → Knowledge → pgvector → fontes → geração.
- [ ] Usar dados sintéticos de políticas/endereço/funcionamento, sem diagnóstico.
- [ ] Sem evidência, reconhecer limite; conteúdo recuperado não altera capacidades ou prompt de confiança.
- [ ] Apresentar fontes e registrar versões; provider controlado prova fluxo, não qualidade de um LLM real.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: FAQ com RAG e fontes

  Cenário: Política documentada
    Dado que a política da clínica consta na versão ativa
    Quando o paciente faz a pergunta pelo Web
    Então o fluxo recupera a fonte autorizada e a resposta aponta para ela

  Cenário: Sem evidência
    Dado que a base não contém a resposta solicitada
    Quando a busca não encontra suporte suficiente
    Então o assistente informa o limite sem inventar política

  Cenário: Instrução no documento
    Dado que um trecho inclui pedido de acessar outro paciente ou executar shell
    Quando ele é recuperado como dado
    Então nenhuma capacidade extra é concedida e a tool indevida é bloqueada
```

## Validação e conclusão

Funcional Web/HTTP com pgvector real, traces e provider controlado; qualidade real reavaliada em CT-018.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
