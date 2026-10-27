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
- [ ] Criar corpus versionado de ao menos três clínicas fictícias e nove documentos conforme a [spec](../../../spec.md#corpus-documental-sintético-para-ingestão-e-rag): equipe/especialidades, políticas de atendimento e políticas internas por clínica, com manifesto e IDs coerentes com os seeds de CT-004.
- [ ] Validar escopo/metadados no upload e distinguir documentos informativos autorizados a pacientes dos internos restritos a operadores; nomes de arquivos ou texto não concedem permissão. Marcar conteúdo como sintético e separar fixtures adversariais do corpus normal.
- [ ] Definir D-14 e capacidades de leitura/envio/revisão/publicação/alteração/remoção/classificação; envio não concede publicação. Registrar ator, documento/versão, escopo, decisão e resultado sem payload sensível na auditoria.
- [ ] Limitar bytes, extração, tempo e admissão de jobs conforme D-16; rejeitar PDF/formatos fora da allowlist atual. Malware scan não declara conteúdo confiável contra prompt injection.

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

  Cenário: Corpus de três clínicas
    Dado que os seeds contêm A1 e A2 no tenant A e B1 no tenant B
    Quando os operadores enviam os três tipos de documento de cada clínica pelo fluxo autorizado
    Então os nove originais e seus metadados ficam vinculados ao escopo correto e às permissões previstas

  Cenário: Atendente sem permissão de publicação
    Dado que uma atendente possui capacidade de agenda mas não de publicação documental
    Quando tenta publicar ou ampliar a visibilidade de um documento
    Então a ação é negada e auditada sem ativar conteúdo nem alterar permissões

  Cenário: Formato PDF fora do escopo
    Dado que o laboratório permite somente TXT e Markdown UTF-8
    Quando um usuário autorizado envia PDF ou arquivo com formato real incompatível
    Então o pipeline rejeita o formato sem indexar ou chamar embeddings
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
