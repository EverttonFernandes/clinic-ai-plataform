---
name: refactor-after-functional-green
description: "Revisar coesão após validação e refatorar apenas onde exista ganho concreto."
applies_when:
  - "conforme condição da tarefa"
progressive_disclosure:
  - Ler nome, descrição e condições antes do corpo.
  - Abrir apenas o detalhe necessário ao estado da tarefa.
  - Consultar complementos somente se a condição se aplicar.
conditional_details:
  - if: "validação ficou verde"
    then: "revisar clareza e coesão e registrar resultado"
  - else_if: "há problema concreto"
    then: "refatorar localmente e repetir regressão"
  - else: "implementação já está clara"
    then: "registrar nenhuma refatoração necessária"
---

# Revisão após Green

Perguntar: a regra está no serviço certo? Nomes explicam intenção? Existe dependência
externa vazando no domínio? A mudança introduziu duplicação ou um módulo com motivos distintos para mudar?
Revisar também legibilidade/isolamento dos testes, força das assertions, dados e cleanup.
Uma suíte verde que não detecta a violação do critério exige correção, não aprovação cosmética.

Registrar resultado da revisão. Se estiver claro, declarar que não há refatoração necessária.
Se houver problema concreto, aplicar mudança localizada preservando comportamento e reexecutar
os testes afetados. Não misturar correção de requisito com limpeza estrutural silenciosa.

Não introduzir camadas, heranças ou padrões apenas por preferência estética. Uma reorganização
ampla só cabe com necessidade comprovada ou autorização de escopo. A revisão é obrigatória;
a refatoração depende do achado.
