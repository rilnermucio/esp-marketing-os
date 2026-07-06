# Rubricas de qualidade

> Canônico. Atualizado em 2026-07-06. Toda rodada declara no worklog as notas das rubricas aplicáveis. Rubrica não aplicável à rodada é marcada "N/A", não omitida.

## Escala (comum a todas)

| Nota | Significado |
|---|---|
| 4 | Exemplar: vira referência pra próxima rodada |
| 3 | Sólido: atende o padrão do repo sem ressalvas |
| 2 | Aceitável com dívida: funciona, mas deixa follow-up registrado |
| 1 | Frágil: precisa retrabalho antes de merge |
| 0 | Ausente ou quebrado |

**Threshold de merge**: todas as rubricas aplicáveis com nota ≥ 3, exceto no máximo UMA dimensão com nota 2 acompanhada de follow-up registrado no worklog. Qualquer 0 ou 1 bloqueia. **Threshold de release**: tudo ≥ 3, sem exceção.

## R1: Qualidade de implementação

| Critério | Nota 4 (âncora) | Nota 2 (âncora) |
|---|---|---|
| Correção verificada | Comportamento novo demonstrado por teste ou execução real registrada no worklog | "Deve funcionar"; verificação parcial |
| Escopo | Diff contém só o tema declarado; descobertas viraram backlog | 1-2 arquivos fora do tema, justificados |
| Testes | Teste novo nasce junto; casos de falso positivo cobertos (ex: `test_quality_gate_hook.py` cobre antítese E não-antítese) | Teste cobre só o caminho feliz |
| Guard-rail | Regra que quebrou vira validador executável | Regra vira parágrafo de doc |
| Estilo do repo | Código indistinguível do existente (idioma, densidade de comentário, padrões pytest parametrizado) | Funciona mas destoa (comentários narrando o óbvio, estrutura alheia ao repo) |

## R2: Documentação

| Critério | Nota 4 | Nota 2 |
|---|---|---|
| Sincronia | Contagens/tabelas/docs atualizados no mesmo diff (README, AGENTS, SKILL quando afetados) | Atualizou os principais, deixou secundário pra depois com registro |
| Drift-proofing | Preferiu frase sem número; número necessário tem guard ou é gerado | Números soltos novos, mas poucos e anotados |
| Snapshot guards | Todo conteúdo datável novo tem carimbo "atualizado em" ou preâmbulo de snapshot | Conteúdo datável sem carimbo em seção secundária |
| Navegabilidade | Links relativos funcionais; doc > 1.500 linhas tem índice | Links ok, índice ausente onde devia |
| Worklog | Completo, com evidências reais e campos todos preenchidos | Preenchido, mas evidências fracas ("rodei os testes" sem números) |

## R3: Roteamento de agentes

| Critério | Nota 4 | Nota 2 |
|---|---|---|
| Cobertura do golden set | `test_routing_evals.py` verde e matriz revisada após a mudança | Verde, matriz não revisada |
| Descriptions | Frontmatter com triggers concretos em PT-BR (palavras que o usuário digita) | Description correta mas genérica |
| Desempate | Ambiguidade entre agents vizinhos tem regra escrita na SKILL | Ambiguidade conhecida registrada como gap, sem regra |
| Exposição | Agent alcançável por ≥1 command OU roteamento natural documentado na SKILL | Agent alcançável só por quem conhece o nome |
| Anti-inline | Produção sempre via dispatch (mapa da SKILL respeitado) | N/A: violação aqui é nota 0, não 2 |

## R4: Output de marketing

Para peças de copy, aplicar também o Copy Score System (PARTE XV de `subagents/copy-agent.md`). Esta rubrica cobre o processo:

| Critério | Nota 4 | Nota 2 |
|---|---|---|
| Gates | Passa as 3 camadas (prompt, hook, CLI `quality_gate.py`) sem violação | Passa com warnings justificados |
| Fact-check | Todo claim classificado (CONFIRMADO/PROVÁVEL/NÃO USAR) com fonte | Claims verificados, classificação implícita |
| Plataforma | Limites e formato da plataforma respeitados + mobile preview quando aplicável | Limites ok, preview ausente |
| PT-BR | Acentuação perfeita, adaptação BR (não tradução literal) | Acentuação ok, adaptação superficial |
| Variação | 5-10 geradas internamente, top 2-3 entregues com hipótese A/B e métrica | Variações entregues sem hipótese |
| Social | Post/reels/carrossel inclui sugestão de enquete (gate global) | N/A: ausência é nota 1 |

## R5: Compatibilidade Claude Code / Codex

| Critério | Nota 4 | Nota 2 |
|---|---|---|
| Manifests | `claude plugin validate .` + `python scripts/validate_codex_plugin.py` verdes | Um validado, outro pendente com motivo |
| Gotchas | Tabela de gotchas do AGENTS.md respeitada (author object, category singular, source `./`, sem field skills) | Conformidade não re-verificada em mudança que não toca manifests |
| Paths portáveis | Hooks usam `${CLAUDE_PLUGIN_ROOT}/...`; nada assume CWD = raiz do plugin | Path relativo em contexto que só roda em dev local, anotado |
| Pacote Codex | `build_codex_plugin.py` gera pacote e nada pessoal vaza (workspace/, memory) | Build ok, verificação de vazamento manual |
| Versões | Base semver sincronizada nos 3 pontos (plugin.json, marketplace.json x2) + sufixo `+codex.YYYYMMDD` atualizado quando o pacote muda | Sincronizado, sufixo esquecido |

## R6: Release

| Critério | Nota 4 | Nota 2 |
|---|---|---|
| Checklist | [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md) executado item a item, com evidência por item | N/A: release aceita só nota ≥3 |
| Tag | Tag aponta pra commit alcançável a partir do main (verificado com `git merge-base`) | N/A |
| CHANGELOG | Cobre todo o range desde a última tag, agrupado Added/Changed/Fixed | N/A |
| Install real | `/plugin install` testado em projeto limpo (Claude) + install Codex testado | Um dos dois testado, outro registrado como pendente |
| Rollback | Passos de reversão anotados antes do push da tag | N/A |
