# CT-011 — Upload privado e validação de documentos

Marco: M4. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Receber documentos da clínica sem expor arquivos nem indexar conteúdo rejeitado.

## Vínculos e dependências

- Requisitos: `RF-09`, `RNF-01`, `RNF-05` — [especificação](../../../spec.md).
- Dependências: [C-008](../historias/C-008-chat-web.md).
- Referências: [decisões](../../spec-driven-development/decisoes.md), [testes](../../spec-driven-development/testes.md) e [ambientes/CI](../../spec-driven-development/ambientes-e-cicd.md).

## Escopo e critérios de aceite

- [ ] Contrato de objetos por chave/versão em volume privado no laboratório; bloquear path traversal e acesso público.
- [ ] Autorizar upload e download por tenant/clínica/finalidade, limitar tamanho e formatos TXT/Markdown UTF-8 iniciais.
- [ ] Malware scan real em Docker, extração segura, sanitização/classificação e limites antes de chunking.
- [ ] Scanner/parser indisponível ou arquivo rejeitado mantém quarentena; nenhum embedding é chamado.

## Cenários BDD de aceitação

Os cenários abaixo são especificação, ainda não são testes executados.

```gherkin
Funcionalidade: Upload privado e validação de documentos

  Cenário: Documento permitido
    Dado que um operador autorizado envia texto válido dentro do limite
    Quando o pipeline de segurança o valida
    Então o original privado e o resultado da validação ficam rastreáveis

  Cenário: Arquivo rejeitado
    Dado que o arquivo excede limite ou o scanner aponta ameaça em fixture segura de teste
    Quando o upload é processado
    Então ele permanece não publicável e não há chamada de embeddings

  Cenário: Chave adulterada
    Dado que um usuário tenta path traversal ou chave de outro tenant
    Quando solicita acesso ao objeto
    Então o storage adapter nega leitura sem expor arquivo local ou de outra clínica
```

## Validação e conclusão

Integração com storage privado e scanner real; doubles só em unitários; sem baixar/gerar malware real.

Registrar Red pelo motivo correto antes de implementar comportamento; depois Green,
revisão de coesão e regressão dos consumidores afetados. Complementar unitários das regras
críticas sem duplicar mecanicamente os funcionais. Não apresentar simulação como integração real.

Plano/evidências: usar [template de tarefa](../../tasks/TEMPLATE.md).
Entrega: usar [template de entrega](../../entregas/TEMPLATE.md).
A história só entra em Done com critérios satisfeitos e evidências executadas; gates não
executados ficam PENDING. Não fazer deploy, chamadas pagas ou contatos externos implicitamente.
