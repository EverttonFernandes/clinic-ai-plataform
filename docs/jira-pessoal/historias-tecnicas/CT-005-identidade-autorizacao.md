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
- [ ] Resolver D-13 com matriz de capacidades/recursos/campos e contexto tenant/clínica/ator/paciente; avaliar os seis perfis candidatos no [detalhamento de segurança](../../spec-driven-development/seguranca-producao.md), sem aprovar papéis ou novos portais automaticamente. Negar por padrão e restringir delegação de grants.
- [ ] Validar vínculo/finalidade e permissão atual em APIs, tools e consumidores; revogação tem efeito antes do TTL de credencial/state/cache. Administrador operacional não recebe acesso global a dados pessoais/médicos por herança do papel.
- [ ] Provar matriz com acessos legítimos mínimos e negativas por papel, recurso e escopo, incluindo ausência de capacidade médica/prontuário fora do MVP; não criar endpoint clínico apenas para testar sua negação.

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

  Cenário: Administrador operacional sem acesso pessoal
    Dado que um administrador da plataforma possui somente capacidades operacionais
    Quando solicita dados pessoais ou documento restrito de uma clínica
    Então o serviço nega acesso sem tratar o papel global como autorização clínica

  Cenário: Médico sem vínculo ou capacidade
    Dado que um ator identificado como médico não tem capacidade e vínculo válidos para a agenda de outro profissional ou paciente
    Quando solicita esse recurso por um contrato existente
    Então o acesso é negado mesmo com identidade autenticada e IDs válidos

  Cenário: Revogação de capacidade
    Dado que uma capacidade de consulta foi revogada e ainda existe cache ou credencial válida
    Quando a mesma operação é solicitada via API ou tool
    Então a permissão atual prevalece sem retorno de conteúdo anterior
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
