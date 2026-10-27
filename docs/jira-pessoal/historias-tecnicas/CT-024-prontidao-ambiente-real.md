# CT-024 — Destino real, secrets, TLS e proteção de dados

Marco: M6. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Preparar o ambiente real com escolhas e controles verificáveis antes de CD.

## Vínculos e dependências

- Requisitos: `RNF-08`, `RNF-11`, `RNF-13` — [especificação](../../../spec.md).
- Dependências: [CT-021](../historias-tecnicas/CT-021-falhas-carga-restauracao.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Resolver D-03/D-04/D-05: destino, domínio, registry, acesso, retenção, SLOs/RPO/RTO e budget.
- [ ] Definir TLS, secrets por ambiente, least privilege, KMS/rotação, criptografia de dados/backups e Object Storage privado.
- [ ] Testar restauração, rotação e negação de acesso; volume local/fake KMS não provam proteção real.
- [ ] Provisionamento/publicação só com autorização e recursos definidos; gate externo pendente se infraestrutura faltar.
- [ ] Resolver D-15 por dependência contra as metas D-05 e custo aprovado: PostgreSQL, Redis, storage, worker/jobs e providers. Definir readiness/degradação, responsáveis e alertas; medir recuperação/failover escolhido e verificar integridade/idempotência/budget após retorno.
- [ ] Validar D-04 e condições de envio/retenção/uso dos dados pelos terceiros antes de qualquer dado real; documentar lacunas de autorização e auditoria sem tratar acesso operacional como acesso clínico.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Destino real, secrets, TLS e proteção de dados

  Cenário: Secret ausente
    Dado que a configuração de homologação não possui credencial obrigatória
    Quando o processo de preparação valida o ambiente
    Então ele falha sem expor segredo ou usar credencial de desenvolvimento

  Cenário: Objeto privado
    Dado que o storage de homologação contém documento sintético restrito
    Quando há tentativa sem vínculo autorizado
    Então a leitura é negada e a política de criptografia é verificável

  Cenário: Rotação e recuperação
    Dado que há autorização para ensaio em ambiente isolado real
    Quando a chave é rotacionada e um backup é restaurado
    Então dados permitidos continuam recuperáveis com acesso mínimo e procedimento registrado
```

## Validação e conclusão

Evidências do ambiente escolhido e ensaios sanitizados; não declarar KMS/TLS/SLO reais com simulações locais.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
