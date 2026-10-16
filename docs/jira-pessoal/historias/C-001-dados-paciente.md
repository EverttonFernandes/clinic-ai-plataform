# C-001 — Consulta autorizada de dados do paciente

Marco: M2. Tipo: negócio.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Como paciente, consultar meus dados administrativos permitidos.

## Vínculos e dependências

- Requisitos: `RF-06`, `RF-01`, `RNF-08` — [especificação](../../../spec.md).
- Dependências: [CT-006](../historias-tecnicas/CT-006-redis-limites-entrada.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Definir GET/contrato equivalente para os campos administrativos mínimos; não criar prontuário completo.
- [ ] Revalidar paciente, vínculo com clínica e finalidade em cada acesso.
- [ ] Negativas e acessos relevantes geram evento mínimo; não logar payload pessoal.
- [ ] Operador só acessa dados explicitamente permitidos por perfil.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Consulta autorizada de dados do paciente

  Cenário: Consulta própria
    Dado que uma paciente autenticada tem cadastro na clínica
    Quando consulta seus dados administrativos
    Então recebe apenas campos permitidos do próprio cadastro

  Cenário: Outro paciente
    Dado que o ator conhece o ID de outra pessoa
    Quando solicita o cadastro dela
    Então recebe negativa sem dados pessoais no corpo ou log

  Cenário: Operador limitado
    Dado que um operador pode consultar cadastro mas não dados clínicos
    Quando consulta o recurso
    Então somente os campos autorizados são devolvidos
```

## Validação e conclusão

Funcionais HTTP e inspeção de campos/logs/eventos; PostgreSQL real.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
