# 2026-08-21: Auditoria completa do sistema

**Executor**: Claude (ox-alpha) via opencode
**Objetivo**: pedido aberto de "auditar todo o sistema e ver o que precisamos melhorar, implementar, corrigir". Rodada de auditoria somente leitura sobre todos os subsistemas (agents Tier 1/2, commands, skill orquestradora, manifests, scripts, hooks, testes, docs), com entrega de relatório priorizado. Esta auditoria atende ao gatilho do OPERATING-MODEL: toca 3+ subsistemas e usa "melhorar" sem alvo específico.
**Fora de escopo declarado**: implementação dos fixes apontados (fica para rodada própria), commit/push/tag/release, alteração de KBs além do registro dos achados, execução dos smoke tests pagos e das validações vivas externas (ChatGPT Work, login OAuth).

## Metodologia

1. Suíte estática completa + validadores como linha de base (`pytest -m "not smoke"`, `validate_agents.py --strict`, `validate_codex_plugin.py`).
2. Exploração paralela por subagente nos dois maiores subsistemas (agents/KBs, commands/docs).
3. Fact-check manual de cada achado grave antes de registrar (princípio 4 do OPERATING-MODEL). Todos os itens P1 abaixo foram confirmados olhando o arquivo citado; nada entrou no relatório por claim não verificado.
4. Cruzamento com backlog vivo (seção "Próximos passos" dos dois worklogs mais recentes) pra separar achado novo de pendência conhecida.

## Arquivos lidos (relevantes pra decisão)

- `AGENTS.md`, `docs/ai-engineering/OPERATING-MODEL.md`, `IMPLEMENTATION-LOG.md`, `FAILURE-TAXONOMY.md`: contratos de processo, formato deste registro e IDs de taxonomia.
- `agents/mos-*.md` (21) e `subagents/*-agent.md` (21): mapeamento 1:1, frontmatter, referências a scripts/KBs/memory, esqueleto interno, TOCs.
- `commands/*.md` (48): frontmatter, dispatch, contagens, gates globais citados.
- `skills/marketing-os/SKILL.md`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`, `CHANGELOG.md`, `README.md`, `docs/GETTING-STARTED.md`, `docs/ROADMAP.md`: sincronia de versões e contagens.
- `scripts/hooks/quality_gate_hook.py`, `hooks/hooks.json`: alinhamento regra documentada vs implementada.
- `pytest.ini`, `pyproject.toml`, `requirements.txt`, `.github/workflows/tests.yml`: config de qualidade e CI.
- `scripts/tests/test_repo_consistency.py` e `test_agents_smoke.py`: escopo real dos guards de inventário e do custo dos smoke tests.
- Worklogs de 2026-08-08 e 2026-08-09: pendências herdadas (RT-031/RT-028, validador universal, login OAuth).

## Arquivos alterados/criados

- Este worklog: artefato da auditoria.
- `docs/ai-engineering/IMPLEMENTATION-LOG.md`: entrada no índice de rodadas.

Nenhum outro arquivo foi modificado nesta rodada.

## Estado geral medido

| Verificação | Resultado |
|---|---|
| Suíte padrão (`not smoke`) | 2262 passed, 2 skipped (esperados), ~10s |
| `validate_agents.py --strict` | 21/21 clean, zero warnings |
| `validate_codex_plugin.py .` | PASS |
| Versões nos 3 manifests + CHANGELOG | Sincronizadas em 6.16.0 |
| Contagens README (21 agents / 48 commands / 44 dispatch / 34 clones) | Bate com filesystem |
| Refs agents → scripts, KBs, memory, assets | Zero quebradas |
| TODO/FIXME/HACK em scripts/*.py | Zero |

## Achados P1: corrigir (drift documental, esforço baixo)

| # | Achado | Evidência | Impacto |
|---|---|---|---|
| 1 | Mapa de PARTES do mos-seo desatualizado vs KB real | `agents/mos-seo.md:48-50` e `:293` dizem content strategy = PARTES VI-VII, link building = VIII, E-E-A-T = IX-X. Real em `subagents/seo-agent.md`: E-E-A-T = VI (L1147), link building = VII (L1309), content SEO = VIII (L1571) | Agent segue o mapa e lê a PARTE errada sob demanda |
| 2 | TOC do copy-agent omite a maior seção do arquivo | `subagents/copy-agent.md:15-38` lista 22 itens sem a PARTE II-C (L1255, Big Idea + Value Stack, ~1100 linhas, ~19% do arquivo) nem a PARTE XV-B (L5091). O próprio agent cita II-C em `agents/mos-offer.md:64` | Navegação da KB engana; leitura guiada pula as seções mais operacionais |
| 3 | TOC do infoproduct-builder para na XIII | `subagents/infoproduct-builder-agent.md:67-91` termina na PARTE XIII + Apêndices A-I. O arquivo tem PARTES XIV-XX (L4562-5474) e Apêndices J-L (L4281-4472). `agents/mos-infoproduct.md:24` cita essas seções novas | Índice interno desconhece 7 partes inteiras adicionadas depois |
| 4 | "35 perfis" residual no GETTING-STARTED | `docs/GETTING-STARTED.md:143` diz 35 perfis; filesystem tem 34 clones conformes (+ design). O fix da v6.16.0 cobriu README, agents e subagents; este arquivo ficou pra trás | Recorrência exata do F-DOC-01 que a v6.16.0 disse ter fechado |
| 5 | Benchmarks contraditórios no funnel-agent | `subagents/funnel-agent.md`: show-up rate 30-50% (L1112) vs 20-35% (L2746); webinar→venda tabela por ticket 3-7% / 12-20% (L1086-1107) vs 5-15% flat (L2747); refund <8% (L1257) vs 5-10% (L2749) | Sem nota harmonizadora, o agent pode citar faixas quase disjuntas no mesmo output |

Causa provável comum: KBs ganharam seções novas nas ondas de nivelamento/jul-ago sem atualizar os TOCs internos, e o mapa de partes do mos-seo guardou uma ordenação anterior do seo-agent.

## Achados P2: robustez de processo

| # | Achado | Evidência | Sugestão |
|---|---|---|---|
| 6 | Footgun de custo/tempo no pytest | `pytest scripts/tests/` cru coleta 22 smoke tests; `test_agents_smoke.py` invoca o CLI claude real por agent (TIMEOUT_SECONDS=180, L15/L157) e `test_audit_screenshot.py::test_real_capture_example_com` faz captura de browser real (L73-76) | Gate no conftest: pular marker smoke a menos que `MOS_SMOKE=1`; AGENTS.md já documenta `-m "not smoke"` mas nada impede o acidente |
| 7 | Guard de inventário de clones com escopo estreito | `test_repo_consistency.py` varre só `AGENTS + SUBAGENTS` (função `test_clone_inventory_claims_match_filesystem`) e seus regex não casam "perfis". Por isso o item 4 escapou | Estender varredura a todos os `.md` versionados (README, docs/, SKILL.md, commands) e ampliar padrões ("perfis", "especialistas") |
| 8 | Validador universal herda marketplace ancestral | Follow-up já registrado no release v6.16.0 (worklog 2026-08-09, L134/L143) | Manter como pendência registrada; não duplicar decisão aqui |

## Pendências externas herdadas (não são achado novo)

- RT-031 e RT-028 exigem conversa manual nova no ChatGPT Work; pendente desde v6.15/v6.16 (worklogs 2026-08-08 e 2026-08-09).
- Prova viva de `/marketing-os:criar-post` + briefing natural no Claude Code depende de renovação de login OAuth.

## Baixa severidade / cosmético (registrar, sem pressa)

- Naming excepcional `mos-infoproduct` → `infoproduct-builder-agent.md` (referências internas corretas; risco apenas se alguém gerar path pela convenção `<nome>-agent.md`).
- Âncoras de TOC não casam com slugs dos headings (ex: `#parte-i` vs heading `PARTE I: A CIÊNCIA...`). Inócuo para consumo por LLM; relevante só se renderizado como HTML.
- Fences markdown aninhados nos Output Schemas (`agents/mos-copy.md:176` com fence interno em `:205-207`; idem `mos-funnel.md:102`). Padrão consistente entre agents, parece aceito.
- Seção "Anti-padrões" presente em copy/seo mas ausente nos outros 14 agents (assimetria de esqueleto, sem contradição).

## Oportunidades (backlog, sem prazo)

- Eval de output existe só para `mos-copy` (baseline ago/2026, 5 golden briefs). `EVALS-STRATEGY` prevê estender para funnel/ads/email quando houver volume; auditar antes da próxima refactor ampla desses agents.
- Contradições de benchmark no funnel-agent (item 5) sugerem revisão mais ampla de claims numéricos entre KBs quando essa rodada acontecer.

## Decisões (e alternativas rejeitadas)

- Auditoria como rodada própria, sem consertar no mesmo diff: OPERATING-MODEL manda auditar primeiro quando o pedido usa "melhorar" sem alvo, e proíbe consertar fora de escopo no mesmo diff.
- Fact-check manual de todo achado grave: princípio 4 (precedente jun/2026 com 6 claims falsos de subauditores). Os 5 itens P1 foram confirmados lendo os arquivos citados.
- Achados P1 como "corrigir" e não "quebra funcional": nenhum teste falha hoje porque os guards não navegam conteúdo interno de TOC/mapas; o dano é na qualidade do dispatch sob demanda, não no install.
- Não reabrir decisão do validador universal (item 8): já tem dono e receita no worklog da v6.16.0.

## Evidências

- `python -m pytest scripts/tests/ -q -m "not smoke"`: 2262 passed, 2 skipped, 22 deselected em 9,78s.
- Skips identificados: `test_native_agents.py:19` e `:26`, ambos por `.claude/agents/` ausente neste checkout (comportamento esperado).
- `python scripts/validate_agents.py --strict`: Total 21, Clean 21, OK 21, Warnings 0, Falhas 0.
- `python scripts/validate_codex_plugin.py .`: aprovado.
- Filesystem: `find assets/clones -maxdepth 1 -type d ! -name design | wc -l` = 34; `ls commands/ | wc -l` = 48.
- Item 1: headings reais conferidos em `subagents/seo-agent.md` L1147/1309/1571/1766/2105 contra texto de `agents/mos-seo.md:48-50`.
- Item 2 e 3: TOCs lidos integralmente e comparados com `rg "^# PARTE|^## PARTE XV-B"`.
- Item 4: frase "35 perfis disponíveis" localizada em `docs/GETTING-STARTED.md:143`; README correto ("34 voice clones", L3/L212).
- Item 5: blocos comparados com `sed -n '1110,1113p;2744,2750p'`.
- Item 6: coleta `pytest -m "smoke" --co` mostra 22 casos; TIMEOUT_SECONDS=180 em `test_agents_smoke.py:15`; captura real em `test_audit_screenshot.py:73-76`.
- Item 7: função de inventário varre `AGENTS + SUBAGENTS` apenas (`test_repo_consistency.py`, bloco `_CLONE_INVENTORY_PATTERNS`).
- Travessão e "brutal" em commands/: ocorrências são meta-texto das próprias regras ("Sem `—`, sem brutal"), não violações de copy. Antítese em `copy-agent.md` (L768 etc.) é material didático citando copy clássica; ok.

## Testes

- Rodados: `python -m pytest scripts/tests/ -q -m "not smoke"`: 2262 passed, 2 skipped.
- Rodados: `python scripts/validate_agents.py --strict`: 21/21 clean.
- Rodados: `python scripts/validate_codex_plugin.py .`: aprovado.
- Rodados: `python -m pytest scripts/tests/ -q -m "smoke" --co`: 22 casos coletados (não executados).
- Não rodados e motivo: smoke tests completos (custo real de runtime Claude + rede + browser; fora do escopo de auditoria); RT-031/RT-028 no ChatGPT Work (dependem de ação manual externa); CI remota (sem push nesta rodada).

## Falhas da taxonomia tocadas

- F-DOC-01: recorrência confirmada (item 4). A prevenção existente (guard de inventário) tem escopo menor do que o alcance da falha; item 7 propõe fechar esse buraco.
- F-EVAL-02 (padrão, não incidente): guards por coleção de arquivos evitam escape; o guard de inventário ainda não segue esse padrão pra docs/.
- Sem novos IDs propostos; os itens 1-3 e 5 são variantes de F-DOC (drift interno de KB) já cobertos conceitualmente pela família.

## Rubrica aplicada

- R1 Implementação: N/A (rodada de auditoria; nenhuma mudança de comportamento).
- R2 Documentação: 4. Achados com path:linha, evidência verificada e proposta por item; índice atualizado no mesmo diff.
- R3 Roteamento: 4. Golden set e `test_routing_evals.py` verdes dentro da suíte padrão; sem mudança em descriptions/SKILL.md.
- R4 Output de marketing: N/A. Nenhuma peça produzida.
- R5 Compatibilidade: 4. Três superfícies validadas pelos validators locais; pendências vivas herdadas permanecem registradas como tais.
- R6 Release: N/A. Sem ação de release.
- Veredito: relatório pronto pra guiar a próxima rodada de fixes.

## Custo aproximado

- Não medido. Sessão interativa sem telemetria consolidada de tokens.

## Riscos e follow-ups

- Os itens P1 tendem a piorar silenciosamente: cada onda futura de expansão de KB sem atualização de TOC repete o padrão. Um guard leve (TOC cita toda `^# PARTE` do arquivo) eliminaria a classe.
- O footgun do pytest (item 6) custa tempo real de quem esquece o marker: 22 testes × até 180s cada.
- Pendências vivas (RT-031, RT-028, prova OAuth) continuam fora do controle de repo e devem ser resolvidas manualmente pelo mantenedor.

## Próximos passos

1. Rodada "fix de drift documental": itens 1-5 (~10 arquivos, todos temáticos, sem mudança de comportamento).
2. Mesma rodada ou imediatamente após: guard de escopo amplo de inventário (item 7) e gate MOS_SMOKE no conftest (item 6).
3. Guard leve de TOC vs PARTES reais nas KBs densas (prevenção da classe dos itens 2-3).
4. Mantenedor: executar RT-031 e RT-028 no app desktop e registrar em ROUTING-EVALS.md.
5. Avaliar extensão do eval de output para funnel/ads/email conforme EVALS-STRATEGY quando houver volume de uso real.
