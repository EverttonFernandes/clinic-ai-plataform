# CT-026 — Aceite integrado e roteiro de demonstração

Marco: M6. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Demonstrar os seis fluxos da aba 09 e registrar o nível real de prontidão.

## Vínculos e dependências

- Requisitos: `RF-02`, `RF-03`, `RF-10`, `RF-11`, `RF-12`, `RF-13`, `RNF-01`, `RNF-09` — [especificação](../../../spec.md).
- Dependências: [CT-025](../historias-tecnicas/CT-025-release-cicd.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Executar os seis fluxos por HTTP/Web/WhatsApp disponível com serviços e dados reais sintéticos.
- [ ] Verificar persistência, chamadas evitadas no hit, isolamento, budget e eventos, não apenas resposta visual.
- [ ] Relatar separadamente laboratório controlado, integração externa e homologação; pendências impedem declarar produção pronta.
- [ ] Atualizar guia/diagrama se decisões aprovadas mudarem o contrato e produzir roteiro reproduzível.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Aceite integrado e roteiro de demonstração

  Cenário: Seis fluxos
    Dado que a release e o dataset sintético foram registrados
    Quando o roteiro percorre miss/hit/agenda/reserva/fallback/abuso
    Então cada fluxo tem resultado verificável e vínculo com requisito/história/evidência

  Cenário: Prontidão incompleta
    Dado que um gate de provider ou deploy externo permanece pendente
    Quando o relatório final é preparado
    Então a limitação fica explícita e o ambiente não é anunciado como produção validada

  Cenário: Checkout independente
    Dado que outra execução parte de checkout e configuração documentados
    Quando reproduz o roteiro no ambiente autorizado
    Então obtém resultados equivalentes sem arquivos privados ou prompts antigos
```

## Validação e conclusão

Suite integrada, run autorizado de CI, roteiro Web e evidências externas correspondentes; fechar somente gates efetivos.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
