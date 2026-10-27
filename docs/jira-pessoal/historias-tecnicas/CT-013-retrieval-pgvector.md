# CT-013 — Retrieval autorizado no PostgreSQL e pgvector

Marco: M4. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Buscar trechos autorizados com embedding compatível e Top-K limitado.

## Vínculos e dependências

- Requisitos: `RF-10`, `RNF-01`, `RNF-03` — [especificação](../../../spec.md).
- Dependências: [CT-012](../historias-tecnicas/CT-012-ingestao-versionada.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Persistir embedding/chunk/metadados e versionar modelo/dimensão/espaço vetorial.
- [ ] Aplicar tenantId/clinicId/visibility/documentType/permissões/versão ativa e patientId quando aplicável na consulta.
- [ ] Gerar embedding da pergunta após autorização/budget; não fazer chunking da pergunta.
- [ ] Top-K possui teto de backend e fontes estáveis; índices de metadados primeiro, ANN avaliado em CT-023.
- [ ] Validar corpus A1/A2/B1 com tópicos semelhantes e políticas divergentes: isolamento entre clínicas do mesmo tenant e entre tenants; paciente não recupera política interna restrita, mesmo que seja o trecho mais semelhante.
- [ ] Aplicar D-16 ao número de consultas/retries, tempo e concorrência, além do Top-K; validar autorização da fonte original ao abri-la e revogação de permissão/visibilidade antes de devolver contexto ou fonte.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Retrieval autorizado no PostgreSQL e pgvector

  Cenário: Busca da clínica
    Dado que há chunks semelhantes em dois tenants
    Quando o paciente consulta conhecimento autorizado
    Então recebe apenas trechos ativos de seu escopo e suas fontes

  Cenário: Conteúdo pessoal
    Dado que há documento pessoal do paciente B dentro da mesma clínica
    Quando o paciente A faz uma pergunta semelhante
    Então o trecho pessoal de B não entra em resultado ou contexto

  Cenário: Top-K abusivo
    Dado que a LLM pede quantidade acima do teto
    Quando o serviço recebe a busca
    Então aplica o limite de backend e contabiliza embedding sem consulta ilimitada

  Cenário: Clínicas do mesmo tenant
    Dado que A1 e A2 pertencem ao mesmo tenant mas possuem políticas de atendimento diferentes
    Quando um paciente autorizado apenas em A1 consulta a política
    Então o resultado contém somente fontes ativas de A1 sem trechos de A2 ou B1

  Cenário: Política interna restrita
    Dado que a clínica possui uma política interna reservada a operadores
    Quando um paciente e um operador autorizado fazem uma consulta pertinente separadamente
    Então somente a consulta do operador pode receber o trecho interno e o paciente não o recebe no contexto
```

## Validação e conclusão

Integração com extensão pgvector real e vetores controlados; inspeção dos IDs retornados, filtros e chamadas.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
