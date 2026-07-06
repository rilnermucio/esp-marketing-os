# 2026-07-06: Backlog completo via delegação (Cursor Composer 2.5 Fast)

**Executor**: Cursor Composer 2.5 Fast (`cursor-agent -p`, 3 ondas em background) sob especificação e revisão de Claude Fable 5
**Objetivo**: implementar todo o backlog implementável de uma vez, delegando o volume ao Composer e mantendo especificação, revisão e integração com o modelo de fronteira (COST-CONTROL §2 na prática).
**Fora de escopo declarado**: itens H do backlog (decisões com gatilho: fusões de agents, gerador de gates); F2/F3 dos evals (dispatch executado, instrumentação de uso: gatilhos registrados); Fase 5 humana das releases.

## Método

1 branch (`feat/backlog-delegado`), 3 briefs cirúrgicos auto-contidos (o Composer não tem o contexto da sessão; tem o que o repo carrega: AGENTS.md → ai-engineering), execução headless em background, revisão minha entre ondas com 2 camadas: guards independentes (nunca confiar no relatório do executor) + prova funcional real. Regras inegociáveis em todo brief: sem push, sem tocar versões, sem AI-tells, "RELATÓRIO DE BLOQUEIO" em vez de improviso.

## Resultado por onda

| Onda | Escopo | Commit | Veredito da revisão |
|---|---|---|---|
| 1 | Housekeeping: índices nas KBs growth/storytelling, docs/archive com links corrigidos em 5 docs, cross-links workflows↔SKILL, runbook copy-agent-refresh movido, black cobrindo scripts/hooks/ no CI | `0e9a03d` | Aprovada sem correção. Índices fiéis aos headers reais; corrigiu links além do enumerado (CONTRIBUTING, DISCOVERY) dentro da instrução |
| 2 | Fase 4: memory_writer.py (append-only, idempotente, categorias, 400 chars, 20/dia), metrics_collector.py (normalizador stdlib), /aprender, 31 testes, mos.py, RT-023 | `3c3da4a` | Aprovada sem correção. Prova funcional: dedupe, categoria e agent inválidos exatos; matemática do collector conferida na mão (média, deltas, candidatos >30%); decisão de design MCP-no-runtime respeitada à risca |
| 3 | Fase 3: mos-community e mos-partnerships (20º/21º), KBs com índice (333/360 linhas), 2 commands, desempates, contagens 21/46/17, manifests (só descriptions), RT-024/025 | `f0828e6` | Aprovada sem correção. Regra nunca-enviar na identidade + description + gates dos dois; guard EXPECTED_AGENT_COUNT atualizado conscientemente pra 21; deferiu o rebuild do pacote Codex documentando (correto: era da integração) |

**Correções necessárias pelo revisor: zero.** Micro-desvios aceitos e documentados: entrada do memory_writer sem hífen de bullet (cosmético); índices de KB parafraseiam os headers em vez de ecoar byte a byte (mesma convenção do copy-agent).

## Integração (pelo revisor)

- Pacote Codex rebuildado e validado com 21 especialistas (item deferido da onda 3)
- F1 dos evals: protocolo LLM-graded manual + âncoras positiva/negativa em `evals/quality-anchors.md` (EVALS-STRATEGY §4 agora tem material executável)
- Camada viva dos 3 roteamentos novos: **3/3 exatos** (RT-023 aprender, RT-024 responder-comentarios, RT-025 prospectar-creators). Acumulado do dia: 12/12 em rota

## Evidências

- Suite: 2046 → **2107 passed** (+61 testes ao longo das ondas); strict **21/21 clean**; black no escopo do CI limpo; validate_codex passed
- Funcionais: memory_writer 4/4 cenários; metrics_collector com matemática conferida (média 53,33; candidatos exatos A/F); 3 sessões headless de roteamento
- Relatórios do Composer: honestos nas 3 ondas, com desvios auto-documentados (nenhum descoberto pelo revisor que ele não tivesse declarado)

## Rubrica aplicada (ao trabalho delegado + integração)

- R1 Implementação: 4 (guards verdes independentes, prova funcional, zero correções)
- R2 Documentação: 4 (contagens perfeitas nos 3 docs + manifests; ROADMAP e CHANGELOG atualizados por onda)
- R3 Roteamento: 4 (3 casos novos no golden set + 3/3 na camada viva)
- R5 Compatibilidade: 3 (validates verdes; install real fica pra release)
- Veredito de merge: **aprovado**

## Resposta à pergunta que originou a rodada ("fica perfeito igual?")

Com dados: o executor entregou 3/3 ondas sem precisar de correção, MAS a equivalência veio do sistema em volta dele: briefs com as decisões de design já tomadas (a de MCP-no-runtime teria sido o erro provável), 2107 guards que reprovam desvio estrutural, e revisão funcional independente. O mesmo executor sem essa malha teria outra taxa de acerto. Conclusão registrada: delegação funciona no padrão da casa QUANDO especificação e revisão ficam com quem carrega o contexto; o custo de fronteira migra de "fazer" pra "especificar e auditar".

## Custo aproximado

- 3 execuções Composer 2.5 Fast (plano Cursor do usuário) + fração de sessão de fronteira (briefs, 2 rodadas de revisão por onda, integração) + 3 sessões headless (~20s cada). Não medido em tokens.

## Próximos passos

1. Release v6.13.0 (Unreleased das 3 ondas pronto no CHANGELOG)
2. Fase 5 humana (1 install cobre tudo)
3. Backlog restante é só o de gatilho: itens H (fusões com dado de uso), F2/F3 (dispatch executado, instrumentação), recorrentes G
