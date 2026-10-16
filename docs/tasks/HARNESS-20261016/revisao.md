# Revisão de HARNESS-20261016

Modo: revisão sequencial separada pela mesma execução /root, explicitamente não independente.
Nenhum subagente, judge remoto ou calibração humana foi executado.
Veredito local: APPROVED para os oito critérios desta manutenção.

| Critério | Evidência e conclusão |
| --- | --- |
| AC1 — Leitura progressiva/condicional | 15 rules e oito skills com metadados de roteamento; YAML/links inspecionados e oito skills aprovadas pelo quick_validate. |
| AC2 — Loop/retomada | Ralph Loop único; executar-historia encaminha ao núcleo; plano/progress, corrections e incidente conservam estado e próxima ação. |
| AC3 — Conclusão por prova | Contracts exercitam comando ausente/falho, timeout, hashes/log/source alterados, AC/BDD omitidos e positivo completo. Check não aprova só por label PASS/DONE. |
| AC4 — Dependências/ownership | Importação do Kanban atual, dependência omitida/alterada, ciclo, token estrangeiro, finish sem posse e recuperação com heartbeat antigo têm testes por CLI. |
| AC5 — Versionamento | Regra e git-operator definem Conventional Commits/SemVer e tag do commit integrado; não autorizam publicação implícita. Nenhum commit/tag/push realizado. |
| AC6 — Evals/Judge | Casos H01–H10 e I01–I08, rubrica por dimensão, veto crítico, abstenção e calibração humana documentados. Judge remoto não foi alegado como executado. |
| AC7 — Contratos | 38 testes executados por CLI em Git temporário; logs/receipts registrados pelo próprio harness. |
| AC8 — Preservação | 37 registros TODO, started_at/completed_at nulos; critérios/histórias do produto preservados, prompts ignorados e docs atualizados para distinguir CI do harness do produto. |

## Escopo e hashes

- source_sha256: 44e08c60dff2cb5df6afc5c298c3d0def06bbff3b02b148b3bbedfae2854f53d
- scope_sha256: e130d18ca8b28f3aafc1861f9dbc9705c8d263fd2e033e84cec5773751c5dcf0
- contract_sha256: 231d09933cd2154fe08cbb225d579f1f424fdbcb1f893ce7394d4b0cc6d123dd
- Receipts locais: .git/harness/HARNESS-20261016/contracts/latest.json; .git/harness/HARNESS-20261016/docs/latest.json.
- Revisão cobre scripts, rules/skills, metadados, templates e referências listados no plano.
- Alterações do planejamento anteriores à demanda permanecem no working tree; não foram stageadas ou revertidas.

## Achados tratados e revisão de coesão

O parser original não reconhecia este Kanban; a adaptação lê ordem/tipo/ID/dependências sem
inferir Done. Dependências declaradas não podem ser omitidas pela revisão manual.
O gate agora compara descriptions dos AC/BDD extraídos à fonte; finish exige ownership ativo.
Os testes do catálogo foram ajustados para aceitar futuras histórias e Done legado como
UNVERIFIED, sem inventar execução histórica.

Foram mantidos três módulos com responsabilidades distintas: comprovação, tracking e ownership.
Não houve necessidade de framework, dispatcher genérico ou camadas adicionais.
Revisão posterior ao Green levou apenas a ajustes localizados no contrato dos testes,
nos filtros da CI e na coerência documental.

## Limites explícitos

Docker indisponível nesta distro; apenas bootstrap Git/Python stdlib foi executado.
CI do harness está definida e validada localmente, sem run no GitHub. Integrações da aplicação,
KMS/TLS reais, provider/WhatsApp e evals reais continuam planejados no Kanban.
Hashes locais não autenticam revisores nem impedem adulteração deliberada; revisão sequencial
não recebe a qualificação de independente. Não há achado corretivo aberto para este escopo.
