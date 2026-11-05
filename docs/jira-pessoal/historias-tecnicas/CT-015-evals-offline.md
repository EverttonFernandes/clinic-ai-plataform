# CT-015 — Dataset e pipeline de evals offline

Marco: M4. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Criar critérios de qualidade antes de conectar modelos reais ou habilitar fallback.

## Vínculos e dependências

- Requisitos: `RNF-09`, `RNF-12` — [especificação](../../../spec.md).
- Dependências: [CT-014](../historias-tecnicas/CT-014-cache-respostas.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Dataset sintético versionado com positivo, sem evidência, adversarial e isolamento.
- [ ] Cobrir A1/A2/B1 do corpus documental com perguntas e fatos/fontes esperados por clínica, políticas divergentes e revisão documental; incluir negativa de acesso a política interna e cruzamento de clínica no mesmo tenant. Expectativas referenciam documento/versão e preservam a distinção de provider controlado versus real.
- [ ] Avaliar tools/argumentos/trajectory, groundedness/hallucination/retrieval relevance, segurança, custo e latência.
- [ ] Assertions determinísticas primeiro; rubricas e calibração humana para judge quando justificado.
- [ ] Provider controlado valida harness; mudanças reais de prompt/model/provider/fallback exigem regressão real específica.
- [ ] Usar dataset mínimo cobrindo critérios obrigatórios e A1/A2/B1; justificar expansão por risco. Judge apenas para critérios que precisem dele, com calibração; execução paga tem seleção por impacto e teto explícito de chamadas/tokens/custo. CI padrão não usa inferência paga.
- [ ] Aplicar o [protocolo mínimo do produto](../../spec-driven-development/testes.md#protocolo-mínimo-de-avaliação-do-produto): casos ligados a requisitos/BDD, conjunto de aceitação separado do ajuste, múltiplos turnos/esclarecimento/confirmação, fontes esperadas e ações proibidas. Separar retrieval, geração com contexto fixo e jornada completa, com rubricas por dimensão.
- [ ] Validar avaliadores com TDD e saídas controladas corretas/incorretas; critérios críticos não são compensados por média. Relatório distingue qualidade, indisponibilidade, não executado e custo incerto. Versionar rubrica/modelo do judge quando usado e tratar instruções nos dados como não confiáveis.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Dataset e pipeline de evals offline

  Cenário: Regressão de tool
    Dado que uma versão escolhe cancelamento em vez de consultar agenda
    Quando o dataset é executado
    Então a regressão falha com caso/versão/argumentos identificáveis

  Cenário: Falha de isolamento
    Dado que uma resposta expõe fonte de outro tenant
    Quando a avaliação roda
    Então o caso crítico reprova mesmo que a média de qualidade seja alta

  Cenário: Judge divergente
    Dado que o judge atribui nota diferente da revisão humana calibrada
    Quando o resultado é analisado
    Então a divergência fica registrada e não substitui assertions de segurança/integridade

  Cenário: Avaliador detecta fonte sem suporte
    Dado que uma resposta controlada cita documento existente mas afirma uma política ausente nele
    Quando o avaliador recebe a fonte e a expectativa rotulada
    Então reprova o suporte factual mesmo com uma citação válida e distingue esse caso do positivo sustentado

  Cenário: Falha de transporte não desaparece do relatório
    Dado que um caso falha por timeout e outro não é executado por orçamento
    Quando o relatório é produzido
    Então separa indisponibilidade, cobertura e qualidade sem excluir tentativas ou declarar avaliação completa
```

## Validação e conclusão

Execução offline reproduzível com relatórios por caso e versão; sem chamadas pagas no CI padrão.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
