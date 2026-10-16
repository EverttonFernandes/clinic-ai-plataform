# CT-005 — Identidade, tenant confiável e fronteira de API

Marco: M2. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Garantir identidade e autorização antes de qualquer recurso pessoal ou tool.

## Vínculos e dependências

- Requisitos: `RF-01`, `RNF-01`, `RNF-08` — [especificação](../../../spec.md).
- Dependências: [CT-004](../historias-tecnicas/CT-004-persistencia-migrations.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Definir contratos OpenAPI e matriz de paciente/operador/clínica; autenticação local segura com credencial assinada verificável e expiração.
- [ ] JWT/sessão exige assinatura, issuer/audience quando aplicáveis e vínculo consultado no backend; não confiar em headers livres.
- [ ] Claims/tenant/patient propostos pela LLM ou pelo cliente não substituem identidade validada.
- [ ] TLS na fronteira real; laboratório isolado identificado, secrets fora do Git e negativas auditáveis com minimização.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Identidade, tenant confiável e fronteira de API

  Cenário: Tenant adulterado
    Dado que um paciente autenticado pertence à clínica A
    Quando envia identificador da clínica B no pedido
    Então o serviço nega acesso antes de ler ou alterar os dados de B

  Cenário: Credencial inválida
    Dado que uma credencial está expirada ou tem assinatura adulterada
    Quando o recurso protegido é solicitado
    Então o acesso falha sem expor informação pessoal

  Cenário: Paciente não autorizado
    Dado que um ator conhece um ID válido de outro paciente do mesmo tenant
    Quando consulta o recurso
    Então a autorização de recurso nega acesso e registra evento mínimo
```

## Validação e conclusão

Funcionais HTTP de credencial e matriz de autorização; banco real; verificar corpo, persistência e auditoria.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
