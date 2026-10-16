# CT-027 — Avaliação do LiteLLM como gateway de modelos

Marco: evolução opcional após M6. Tipo: técnica.
Estado e prioridade: somente no [Kanban oficial](../KANBAN-OFICIAL.md).

## Resultado esperado

Comparar o adapter validado com um proxy LiteLLM e demonstrar se a integração preserva
contratos, segurança, limites e qualidade. Adoção condicionada ao resultado registrado.

## Vínculos e dependências

- Dependência: [CT-026](CT-026-aceite-seis-fluxos.md), com sua base integrada.
- Condição de entrada: promoção explícita do backlog e decisão D-07 resolvida.
- Requisitos: `RF-13`, `RNF-03`, `RNF-04`, `RNF-06`, `RNF-09`, `RNF-14` — [spec](../../../spec.md).
- Referências: [mapa DDD e responsabilidades](../../spec-driven-development/arquitetura-ddd.md), [decisões](../../spec-driven-development/decisoes.md).

## Escopo e critérios de aceite

- [ ] Registrar versão/licença/capacidades, modo proxy, configuração mínima e decisão de adoção com trade-offs; perfil Docker opcional não é dependência da execução padrão.
- [ ] Adapter atrás das portas existentes valida geração, tool calling, streaming, embeddings, erros e usage; domínio e conversação não importam SDK LiteLLM.
- [ ] Backend preserva autorização, reservas atômicas e reconciliação; definir um dono de tentativas/fallback e comprovar o total real, custo máximo e deadline, inclusive sob resposta perdida e Redis indisponível.
- [ ] Parâmetros de roteamento/limites vêm do backend; proxy privado, credenciais fora do Git e cache compartilhado desabilitado inicialmente. Testar adulteração de limites/headers e IDs cruzados.
- [ ] Executar proxy real contra provider controlado para contratos e falhas; registrar comparação e roteiro reproduzível. Qualidade real/fallback exigem evals de provider real com custo autorizado; fake não as comprova.

## Cenários BDD de aceitação

```gherkin
Funcionalidade: Proxy de modelos atrás do AI Gateway

  Cenário: Troca de adapter
    Dado que os contratos do AI Gateway estão validados com provider controlado
    Quando o adapter é configurado para usar um proxy LiteLLM real
    Então os consumidores mantêm seu contrato público sem depender do SDK do proxy

  Cenário: Retry e custo limitados
    Dado que uma chamada possui orçamento reservado e um limite total de tentativas
    Quando o provider falha e o proxy aplica a política configurada
    Então o total de tentativas e consumo permanece dentro do limite e o uso incerto é reconciliado

  Cenário: Parâmetro de limite adulterado
    Dado que o paciente ou modelo tenta aumentar retries ou escolher uma rota não autorizada
    Quando o backend monta a chamada ao proxy
    Então os parâmetros não permitidos são rejeitados sem ampliar acesso ou consumo
```

## Validação e conclusão

Contratos, funcionais e falhas com proxy real, tentativas observadas e ledger conferido;
evals/custos registrados com o modo identificado. Ausência de prova obrigatória é PENDING.
Caso a avaliação rejeite adoção, registrar os critérios e resultados que sustentam a decisão;
não habilitar um adapter que falhou. Usar [tarefa](../../tasks/TEMPLATE.md),
[entrega](../../entregas/TEMPLATE.md) e DoD do Kanban, incluindo revisão e merge do usuário.
