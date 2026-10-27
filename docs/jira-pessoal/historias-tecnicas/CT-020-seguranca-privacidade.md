# CT-020 — Verificação adversarial e políticas de privacidade

Marco: M5. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Revisar as fronteiras já implementadas e exercitar retenção/exclusão com dados sintéticos.

## Vínculos e dependências

- Requisitos: `RNF-01`, `RNF-05`, `RNF-08`, `RF-07` — [especificação](../../../spec.md).
- Dependências: [CT-017](../historias-tecnicas/CT-017-contratos-resiliencia.md), [C-010](../historias/C-010-whatsapp-inbox.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Consolidar threat model de prompt injection, identidade/canal, IDOR, objetos e Denial of Wallet.
- [ ] Definir retenção por classe/finalidade e autorização de acesso; exclusão alcança originais, índice/cache e política de backups.
- [ ] Auditoria minimizada com acesso restrito; hashes não substituem criptografia; KMS/rotação reais ficam como gate de CT-024.
- [ ] Testar negativa antes do acesso em todos os caminhos; segurança não começa nesta história, ela verifica os controles anteriores.
- [ ] Incluir state e snapshots/checkpoints eventualmente aprovados na retenção/exclusão e política de cópias; verificar minimização, revogação antes do TTL e ausência de payloads/credenciais em logs/traces. TTL no Redis não comprova exclusão de backups.
- [ ] Consolidar cenários positivos/negativos de D-13/D-14 em API/tool/retrieval/fontes: administrador operacional, atendente sem publicação, paciente próprio/alheio e candidato médico sem capacidade/vínculo. Prontuário continua indisponível sem criar endpoint ou papel produtivo só para testar a negativa.
- [ ] Registrar D-04 para dados reais, finalidade/base aplicável, responsáveis, condições de uso/retencão de terceiros e falha de auditoria; laboratório usa dados sintéticos e não afirma conformidade LGPD pelo diagrama ou pelo teste.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Verificação adversarial e políticas de privacidade

  Cenário: Instrução maliciosa
    Dado que um documento recuperado pede exfiltração e gasto elevado
    Quando o agente recebe o trecho
    Então tools e budgets impedem ação indevida independentemente do texto gerado

  Cenário: Exclusão autorizada
    Dado que uma versão documental/pessoal sintética é elegível para exclusão
    Quando a rotina autorizada executa a política
    Então origem, índice e caches deixam de servir o conteúdo sem apagar auditoria obrigatória indevidamente

  Cenário: Acesso à auditoria
    Dado que um paciente tenta ler eventos internos de outro recurso
    Quando o endpoint protegido é chamado
    Então o acesso é negado sem expor conversa, chaves ou eventos pessoais

  Cenário: Exclusão de state e cópias
    Dado que um state sintético contém dado elegível para exclusão pela política definida
    Quando a rotina autorizada aplica a política e o ciclo de cópias é verificado
    Então o conteúdo deixa de ser servido e cópias seguem a retenção aprovada sem apagar registros transacionais obrigatórios

  Cenário: Logs de erro de state
    Dado que um snapshot inválido contém texto pessoal e um valor de teste marcado como segredo
    Quando o backend registra o erro de leitura
    Então o log contém somente metadados mínimos e não expõe os valores do snapshot

  Cenário: Papel não cria capacidade clínica
    Dado que um ator possui rótulo de médico ou administrador mas o MVP não oferece capacidade de prontuário
    Quando tenta obter acesso clínico por prompt ou parâmetro de tool
    Então o sistema não concede capacidade nem devolve dados médicos e mantém apenas os contratos administrativos existentes
```

## Validação e conclusão

Security tests HTTP/SQL/storage/cache e verificação do ciclo de dados; políticas reais exigem responsável definido.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
