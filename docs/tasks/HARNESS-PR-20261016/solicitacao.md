# Política de revisão e PR por história

Instrução do usuário para as próximas histórias: GPT-6 Astra, effort medium, executa;
GPT-6 Sol revisa em sessão separada antes da abertura do PR. O usuário revisa e faz merge.

- [ ] Registrar modelos/papéis, sem tratar troca de persona como modelo independente.
- [ ] Bloquear aprovação da história com mesmo executor/modelo, identidade desconhecida ou fallback sequencial.
- [ ] Exigir branch com ID da história, testes e CI do SHA correto antes do PR pronto para revisão.
- [ ] Manter a história em Review enquanto aguarda revisão humana; Done requer aceite e merge verificados.
- [ ] Revisar rigor dos testes funcionais/integrados/unitários e critérios, sem enfraquecer assertions.
- [ ] Preparar PR didático com problema, decisões, trade-offs, validações e roteiro de estudo/reprodução.
- [ ] Persistir handoff e evidências por revisão, invalidando aprovação depois de mudanças relevantes.
- [ ] Validar o protocolo e atualizar skills/rules/planejamento sem iniciar CT-001 ou alegar CI remota executada.
