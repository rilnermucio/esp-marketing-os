# 2026-09-28: Auditoria de runtime, distribuição e produto

**Executor**: Claude Opus 5.5 via Claude Code (app desktop)
**Objetivo**: pedido aberto de "auditar o plugin e ver o que podemos implementar ou melhorar". Rodada somente leitura que re-verifica a auditoria de 2026-08-21 (nunca executada nem commitada) e estende a cobertura para o comportamento do plugin **instalado** (hooks, memória, caminhos, distribuição), frescor de fatos de plataforma, roteamento e oportunidades de produto.
**Fora de escopo declarado**: implementação de qualquer fix (rodadas próprias, após aprovação), commit/push/tag/release, `git rm` ou reescrita de histórico dos arquivos pessoais versionados (decisão do mantenedor), alteração da conta claude.ai, smoke tests completos, RT-031/RT-028 no ChatGPT Work.

## Metodologia

1. SCOUT: memórias, OPERATING-MODEL, worklog de 2026-08-21 e "Próximos passos" dos worklogs de 2026-08-08 e 2026-08-09.
2. Linha de base: suíte estática e validadores.
3. Re-verificação manual dos 8 achados de 2026-08-21 e checagens determinísticas próprias (TOC contra headings PARTE, inventário de clones em todos os `.md` versionados, acentuação, fatos de plataforma, segredos e binários versionados).
4. Doc oficial do Claude Code (hooks, sub-agents, skills) lida diretamente.
5. **Sonda empírica**: plugin descartável de 1 a 3 agents (Haiku), carregado via `--plugin-dir` no Claude Code 2.1.283 com a sessão **fora** da pasta do plugin, registrando o payload real de cada hook. Converte afirmação de doc em fato observado (princípio 4). Cinco execuções curtas.
6. Quatro subagentes em paralelo: `claude-code-guide` (plataforma), Explore (scripts e hooks), Explore (commands, roteamento e evals), general-purpose (oportunidades de produto). Todo achado deles passou por conferência antes de entrar aqui; o que não foi re-executado está marcado como "reportado pelo subagente".

## Estado geral medido

| Verificação | Resultado |
|---|---|
| `pytest scripts/tests/ -m "not smoke" -q` | 2262 passed, 2 skipped, 22 deselected (10,5s) |
| `validate_agents.py --strict` | 21/21 clean, 0 warnings |
| `validate_codex_plugin.py .` | aprovado |
| Release | `main` sincronizado com `origin/main`; `v6.16.0` ancestral do main; 1 commit de docs depois da tag |
| Auditoria 2026-08-21 | 0 de 8 itens executados; itens absorvidos abaixo (#15, #17, #18, #25) |

A suíte verde não descreve o produto instalado: os achados #2 e #3 passam por ela porque nenhum teste roda o plugin fora do próprio repo.

## Achados P0: risco real para usuários ou terceiros

| # | Achado | Evidência | Taxonomia |
|---|---|---|---|
| 1 | **Documentos de cliente versionados em repo público e distribuídos em toda instalação**: 3 arquivos `.docx` em `workspace/research/` (uma análise competitiva com nome de pessoa física no título e duas tabelas de preços de concorrentes) | `git ls-files workspace/` lista os 3; entraram em `d8421f5` (2026-05-06, reestruturação v6.0.0) e seguem rastreados porque a regra `workspace/**` (`.gitignore:16`) não remove arquivo já versionado; `gh repo view` = PUBLIC; presentes no cache de instalação `~/.claude/plugins/cache/mos-marketplace/marketing-os/6.16.0/workspace/research/`. O guard `test_workspace_separation.py:10-59` verifica se código cita `workspace/`, não o invariante "só `.gitkeep` rastreado". Varredura de segredos em arquivos versionados: 0 ocorrências; nenhum outro binário pessoal fora desses 3 | F-CODEX-03 (mesma classe, lado Claude, sem guard) |
| 2 | **KBs Tier 2, scripts, clones e references inalcançáveis numa instalação real.** Agents, commands e SKILL.md apontam para `subagents/`, `scripts/`, `assets/`, `references/` por caminho relativo, que só resolve quando a sessão roda dentro do repo do plugin | Sonda com a sessão fora da pasta do plugin: agent com caminho relativo respondeu NOT-FOUND após 10 tentativas de Read/Glob; o mesmo agent com `${CLAUDE_PLUGIN_ROOT}/kb/...` no corpo leu a KB na primeira tentativa (a plataforma substitui a variável em corpo de agent de plugin). 291 referências relativas em 36 arquivos (21 agents, 14 commands, SKILL.md): 134 para `scripts/`, 76 para `assets/`, 60 para `subagents/`, 18 para `references/`, 3 para `workflows/`. Só `commands/auditoria.md` e `commands/auditoria-pro.md` usam `${CLAUDE_PLUGIN_ROOT}` (desde 2026-05-09). `scripts/tests/test_agents_smoke.py:156` roda com `cwd=project_root`, por isso nenhum teste exercita o cenário do usuário | F-REL-03; proposta F-DIST-01 |
| 3 | **Nenhuma camada determinística de quality gate roda numa instalação via plugin.** (a) Os 21 agents declaram o gate de escrita em `hooks:` no frontmatter, que a plataforma ignora para agents de plugin. (b) O `SubagentStop` de `hooks/hooks.json` dispara, mas `scripts/hooks/quality_gate_hook.py:315` descarta todo `agent_type` que não começa com `mos-`, e o runtime envia `marketing-os:mos-copy` | Doc oficial (sub-agents): "plugin subagents don't support the `hooks`, `mcpServers`, or `permissionMode` frontmatter fields. These fields are ignored". Doc oficial (hooks): nome de agent de plugin é `plugin-name:agent-name`; matcher com `.`/`*` é regex sem âncora. Sonda: hook de frontmatter não disparou apesar do Write executado; `PreToolUse` e `SubagentStop` de nível de plugin dispararam com `agent_type: "hookprobe:probe-writer"`. O subagente de scripts achou no binário 2.1.283 a mensagem "sets hooks, which is ignored for plugin agents" e a montagem `[plugin, nome].join(":")`. Testes `test_quality_gate_hook.py:141,154,167,193` usam só `"mos-copy"` sem prefixo. Worklog 2026-08-03:86 já registrava que o gate "ainda precisa de execução em uma instalação Claude" | F-COPY-04 segue aberto na prática; premissa da ADR-0002 ("camada 2 garantida no Claude Code") inválida; propostas F-HOOK-01 e F-HOOK-02 |
| 4 | **O app desktop carrega uma cópia sincronizada congelada na v6.1.5** (18 agents, 25 commands) em vez da 6.16.0 | `~/.claude/plugins/synced/<conta>/marketing-os/.claude-plugin/plugin.json` = 6.1.5; `.marketplaces.json` da conta registra "Marketing-OS" (fonte `rilnermucio/Marketing-OS`, `updated_at` 2026-05-07, nome fora de kebab-case), o mesmo dia do rename para `mos-marketplace` (`7d5b704`, v6.1.4). A lista de agents da sessão desktop mostra 18 `marketing-os:mos-*`, sem offer, community e partnerships. `installed_plugins.json` tem a 6.16.0 instalada e habilitada, mas ela não é a carregada no desktop | F-REL-03 |

## Achados P1: funcionais ou de qualidade do output

| # | Achado | Evidência |
|---|---|---|
| 5 | **Scripts gravam estado dentro da pasta do plugin** (mesma classe do #2) | `scripts/project_manager.py:32-33` (`<plugin>/workspace/projects`, estado do `/projeto`), `scripts/weekly_report.py:22-23` (`<plugin>/output/reports`), `scripts/tiktok_trends_scraper.py:39` (`<plugin>/outputs/tiktok-trends`). Em instalação real, cai no cache versionado: some no update e mistura clientes |
| 6 | **`/criar-meu-clone` grava dado pessoal em pasta do plugin** | `commands/criar-meu-clone.md:36-37,61,88`: cria `assets/clones/{slug}/` e edita `assets/clones/clone-manifest.yaml`. No repo de dev, polui a árvore versionada pública e muda a contagem de 34 que `test_repo_consistency.py` trava; em instalação, pelo #2, o caminho relativo cai no projeto do usuário e a pré-condição do manifest falha (inferido, não testado). A doc oficial oferece `${CLAUDE_PLUGIN_DATA}`, que sobrevive a updates |
| 7 | **Memória nativa e memória do plugin em diretórios diferentes** | Sonda: com `memory: project`, o agent de plugin recebeu e criou `.claude/agent-memory/hookprobe-probe-writer/MEMORY.md` (padrão `<plugin>-<agent>`). Para o Marketing OS isso é `marketing-os-mos-<agent>/`; bootstrap, `memory_writer.py`, `/aprender` e os 21 agents usam `mos-<agent>/` (42 arquivos citam esse path, ex: `scripts/init_agent_memory.py:5,47`, `agents/mos-copy.md:104`). Doc oficial: a plataforma injeta as primeiras 200 linhas ou 25 KB do `MEMORY.md` do diretório nativo. Resultado: dois repositórios de aprendizado, e o loop do `/aprender` alimenta o que a plataforma não injeta |
| 8 | **Instruções mortas por assinatura de CLI** | Executado nesta rodada: `agents/mos-seo.md:277` (`apify serp "<kw>"`) sai com "required: --query/-q"; `agents/mos-partnerships.md:46` (`apify_instagram.py "@handle"`) sai com "required: --handle/-u"; `agents/mos-analytics.md:227` (`metrics_collector.py --summary`) sai com "required: --metrica" (a flag não existe). Reportado pelo subagente: `subagents/research-agent.md:3469` chama `mos.py research`, categoria inexistente. `validate_agents.py` checa existência do script e Bash na tools list, não a assinatura (F-BLOAT-02) |
| 9 | **Bug de produção mascarado por teste** | `scripts/reels_script_generator.py`: 48 de 400 chamadas de `gerar_roteiro` (12%) levantam `KeyError` por placeholders que não casam com o `.format`. `scripts/tests/test_reels_script_generator_funcs.py:19-32` documenta o bug e tenta até 30 vezes antes de dar skip. Chamado por `mos-social` e `mos-video`. Reportado pelo subagente: mesmo padrão em `caption_generator.py` (2 de 42 templates; não medido) |
| 10 | **Fatos de plataforma desatualizados, sem data de verificação nem rotina de refresh** | Checados via WebSearch nesta rodada. Reels "15-90s"/"até 90s" (`agents/mos-video.md:94`, `references/design-specs.md:34`, `references/social-media.md:21`): limite de 3 min desde 18/01/2025. Shorts "< 60s"/"15-60s" (`agents/mos-video.md:93`, `subagents/video-agent.md:805`): 3 min desde 15/10/2024. "Advantage+ Shopping (ASC)" (`subagents/ads-agent.md:2686,2705,3581,5972`): renomeado Advantage+ Sales em fev/2025. Tier 1 do SEO ainda fala "SGE" (`agents/mos-seo.md:3,51,77`), enquanto a KB já usa "AI Overviews (antigo SGE)" (`subagents/seo-agent.md:2464-2469`); "fatores de ranking 2024-2025" (`agents/mos-seo.md:43`). Nenhum `verificado em` nas references de specs; nenhuma rotina de refresh em `docs/ai-engineering/` |
| 11 | **Erro factual no gate de compliance global** | `skills/marketing-os/SKILL.md:380` põe "dental / nutrição" sob **CFM/CRM**; odontologia é CFO/CRO e nutrição é CFN/CRN. OAB, CFP e CFO não aparecem no gate global |
| 12 | **Golden set contradiz o sistema e nenhum teste percebe** | `routing-cases.json`: RT-001 espera `["mos-social","mos-copy"]` em paralelo, mas `commands/criar-post.md` só despacha `mos-research` e `mos-social`; RT-018 manda bio para `mos-copy`, enquanto `SKILL.md:77,150` manda para `mos-social`. Nenhum teste cruza `expected_agents` com o corpo do command, e a camada viva pontua só o command (`ROUTING-EVALS.md:79`) |
| 13 | **`/mo` mantém mapa de roteamento próprio e defasado**, apesar de declarar o SKILL.md como fonte única | `commands/mo.md:237` diz "25 commands específicos" (são 48); 21 dos 48 commands não aparecem no arquivo (15 sem nenhuma menção e os 6 presets só na forma `/campanha <preset>`); diverge do SKILL.md em gatilhos como reels, lançamento, posicionamento, growth e leads |
| 14 | **Description da skill não cobre os prompts de vitrine do ChatGPT Work** | `skills/marketing-os/SKILL.md:3` não cita avatar, persona, USP, oferta, lançamento, funil, pesquisa, comentários, parcerias nem métricas; os 3 `defaultPrompt` (`.codex-plugin/plugin.json:38-42`, `agents/openai.yaml`) são avatar, USP e oferta. No ChatGPT Work e no Codex a description é a principal superfície de roteamento; relevante para RT-031/RT-028 pendentes |
| 15 | **Drift documental de 2026-08-21 intacto e maior do que o registrado** | Itens 1, 2, 3 e 5 de agosto re-confirmados: mapa de PARTES do `mos-seo.md:48-50,293`; TOC do `copy-agent.md` sem II-C e XV-B; TOC do `infoproduct-builder-agent.md` sem XIV a XX; benchmarks contraditórios em `funnel-agent.md:1112` contra `:2746-2749`. Checagem determinística das 15 KBs com headings PARTE: só essas 2 têm TOC incompleto, e `seo-agent.md` não tem TOC nenhum (o histórico confirma que nunca teve). "35 clones" vivo em **5** arquivos: `docs/GETTING-STARTED.md:143`, `docs/DISCOVERY.md:150`, `commands/campanha.md:45`, `commands/criar-meu-clone.md:140`, `assets/clones/design/design-dna-system.md:3`. `docs/GETTING-STARTED.md` sem commit desde 2026-05-07: diz "18 subagents" (`:14`) e não cita nenhum dos 12 commands mais novos (`/mo`, `/criar-oferta`, `/criar-usp`, `/criar-avatar`, `/aprender`, `/auditoria`, `/auditoria-pro`, `/projeto`, `/responder-comentarios`, `/prospectar-creators`, `/narrar-roteiro`, `/produzir-reels`). `docs/DISCOVERY.md:98` "18 subagents"; `docs/ARCHITECTURE.md:639` "17 agents" e `:259` "24 commands" |

## Achados P2: robustez de processo

| # | Achado | Evidência |
|---|---|---|
| 16 | **Brechas e ruído no próprio gate** (pré-requisito da correção do #3) | Exclusões de caminho sem âncora (`quality_gate_hook.py:52-73`: `r"docs/"`, `r"scripts/"`): uma pasta `docs/` no projeto do usuário desliga o gate. Avisos de clichê e compliance saem em stderr com código 0 (`:356-364`), canal que não chega ao modelo. O ramo PreToolUse (`:320-326`) não filtra por agent: movido para `hooks.json` como está, bloquearia escrita da sessão inteira do usuário. Padrões `\bCVM\b`, `\bANVISA\b`, `\bCONAR\b` (`:182,205,222`) buscados em texto minúsculo (`:289-292`) nunca casam. Reportado pelo subagente com execução própria: `.txt` sempre pulado (o roteiro do `/narrar-roteiro` é `.txt`), travessão curto `–` e "brutais" passam, travessão como célula vazia de tabela bloqueia. Regras regexáveis da tabela global (CAPS, mais de 2 emojis) não estão no hook |
| 17 | Guards de inventário com escopo menor que o alcance da falha | Guard de clones varre só agents e subagents (item 7 de agosto); os 5 "35 clones" estão fora desse escopo. Contagens de agents não são checadas em GETTING-STARTED, DISCOVERY e ARCHITECTURE. `test_no_emdash_in_distributed_prose` (`test_repo_consistency.py:228`) cobre só agents e commands; o SKILL.md tem 21 linhas de prosa com travessão |
| 18 | Smoke tests sem trava | `pytest scripts/tests/` coleta 2286 casos, 22 deles smoke com Claude real, rede ou browser; `scripts/tests/conftest.py` não tem gate. `pytest.ini` ainda declara markers das fases v6.0 (`aios_removed`, `workspace_extracted`, `consolidated`) |
| 19 | Descriptions de commands fracas para descoberta automática | Cerca de metade em inglês (25 a 28 de 48, conforme o critério); só 4 ou 5 de 48 dizem quando usar; a maioria gasta espaço com mecânica interna (nomes de agents, "workflow #N", "PARTE XV") que envelhece. O campo `when_to_use` (doc oficial) não é usado. Grupos sem fronteira escrita: 6 commands disputam "lançamento"; `criar-email` e `criar-sequencia`; `auditoria` e `auditoria-pro`; `gerar-imagem` (entrega só prompt) e `renderizar-imagem` |
| 20 | Descriptions das skills do plugin somem da listagem em ambientes com muitos plugins | Doc oficial (skills): orçamento de 1% da janela de contexto; ao estourar, cai primeiro a description das skills menos usadas. Na sessão desktop desta auditoria, com dezenas de plugins, as skills do Marketing OS apareceram só com o nome |
| 21 | Cobertura do golden set e dos evals | 25 dos 48 commands sem caso; `mos-growth` e `mos-infoproduct` sem caso; a camada viva rodou 13 dos 31 casos. Eval de output executado só no mos-copy; 6 perfis (email, ads, offer, funnel, seo, video) sem briefs nem baseline. O caso de post (CO-002) mede o mos-copy, mas quem produz post é o mos-social |
| 22 | SKILL.md acima do recomendado e com duplicação | 509 linhas (doc oficial: menos de 500). Workflows #5 a #10 (121 linhas) parafraseiam os corpos de 6 commands; gates e tabela dispatch×inline repetem o AGENTS.md |
| 23 | Contratos duplicados entre command e agent | `commands/criar-avatar.md:44-177` define dossiê de 12 seções paralelo ao contrato canônico `assets/personas/persona-template.md` citado em `agents/mos-research.md:30,196`; `criar-usp.md` e `criar-oferta.md` repetem esquemas dos agents brand e offer (F-BLOAT-03) |
| 24 | CI testa uma única versão de Python | `.github/workflows/tests.yml:16` = `["3.12"]`; os hooks rodam com o `python3` do PATH (3.9.6 no macOS limpo). O subagente compilou os 58 arquivos no 3.9.6 sem erro, então hoje funciona, mas nada impede regressão; não há `requires-python` |
| 25 | Validador universal herda marketplace ancestral | Pendência registrada em 2026-08-09; mantida |

## Baixa severidade

- Travessão nas descriptions públicas de `.claude-plugin/plugin.json` e `marketplace.json` (vitrine do plugin), contra a regra global de copy.
- `commands/criar-meu-clone.md` concentra texto sem acento (15 ocorrências das palavras de controle; outros 6 arquivos com 5 a 7).
- `docs/stories/` e `docs/skill-v1-archive.md` (fev/2026) são backlog e arquivo de um processo anterior; candidatos a `docs/archive/`.
- O pacote Claude instalado carrega `plugins/marketing-os/` (6,3 MB de 15 MB) e `docs/` inteiros, porque a fonte do marketplace é a raiz.
- `commands/mo.md:185` usa a flag `--ticket=`, que não existe; `SKILL.md:425` fala em "29 ferramentas" (há 55 scripts).
- Reportados pelo subagente de scripts (linhas citadas, não re-executados): `scripts/hooks/install.py` órfão e com o caminho relativo que o AGENTS.md proíbe; `test_native_agents.py:16-26` procura `.claude/agents` e sempre dá skip (são os 2 skipped da suíte); `instagram_api.py` e `notion_api.py` citados só em docs; 5 exceções vencidas em `test_integration_mcp.py:274-280`; `cryptography` importado sem declaração (import protegido); erros engolidos em `trend_tracker.py`, `competitor_analyzer.py` e `tiktok_trends_scraper.py`; `notion_api.py` sem timeout de rede.

## Oportunidades (implementar)

Estruturais, habilitadas pela plataforma (verificadas por doc e sonda):

| # | Oportunidade | Base | Esforço |
|---|---|---|---|
| O1 | **Commands como skills com `context: fork` + `agent: marketing-os:mos-*`**: a plataforma garante o dispatch (F-ROUTE-01 por construção), substitui `${CLAUDE_PLUGIN_ROOT}`, aceita `when_to_use` e arquivos de apoio para os esquemas de saída que hoje incham os corpos. Commands multi-agent continuam como orquestradores | Sonda: skill de plugin com `context: fork`, `agent: hookprobe:probe-writer` e `background: false` rodou dentro do agent do plugin, substituiu `$ARGUMENTS` e devolveu o resultado no turno. Doc: o fork não vê o histórico da conversa | M (piloto com 2 ou 3 commands de agent único; ADR para o pacote universal) |
| O2 | **Smoke de instalação real**: a sonda desta rodada vira teste (`--plugin-dir`, cwd em `tmp_path`) cobrindo leitura de KB, `agent_type` qualificado, bloqueio e correção pelo gate. Os payloads capturados viram fixtures | Os achados #2 e #3 passaram pela suíte porque nenhum teste roda fora do repo | S |
| O3 | **Registro de specs de plataforma com `verificado_em`** e guard de validade, mais rotina periódica de refresh | Achado #10 | S |
| O4 | **Guard de contrato de CLI**: extrair as invocações `scripts/X.py` citadas em agents e commands e validar as flags contra o argparse | Achado #8 | S |

De produto (Grupo A; levantadas por subagente e conferidas nos pontos citados):

| # | Oportunidade | Estado hoje | Esforço |
|---|---|---|---|
| P-a | **Perfil de marca/projeto único** (`/configurar-marca`) lido por todos os agents: nicho, avatar, oferta, tom, proibições, categoria regulada. Absorve o clone pessoal (#6), o handoff do avatar e as 5 perguntas que o SKILL.md refaz a cada sessão | `workspace/brand/` não é lido por nenhum agent, command ou pelo SKILL.md; memória é por agent; padrão reaproveitável em `.auditoria-config.json` (`docs/AUDIT-CONFIG.md`) | M |
| P-b | **Compliance BR** (`/checar-compliance` + `references/compliance-br.md` + regras no hook com teste): conselhos corretos, OAB, CFP, CFO, CRN, promessas de ganho | Conhecimento espalhado em `ads-agent.md` e `copy-agent.md`; gate global com erro (#11) | M |
| P-c | **Reaproveitamento 1→N** a partir de live, aula, podcast ou vídeo | `scripts/content_repurposer.py` é heurística sem uso por agent ou command; `/batch` varia por tema, não deriva de uma fonte | M |
| P-d | **GEO/AEO** (AI Overviews, AI Mode, ChatGPT Search, bots de IA, métrica de citação) | PARTE XII do seo-agent tem cerca de 124 linhas genéricas; Tier 1 ainda fala "SGE" | M |
| P-e | **Voz do cliente**: reviews, comentários e Reclame Aqui viram dores, objeções e frases literais | Só técnica em `research-agent.md`; nenhum command recebe export | M |
| P-f | **Plataformas BR**: Kwai e Shopee (0 menções em agents, KBs, commands e references), WhatsApp Status e Canais, fichas de marketplace | `mos-social` não cita Threads, WhatsApp nem Kwai na description | M |
| P-g | **Evals de output** para mos-social, mos-email e mos-ads | Perfis de email e ads já existem sem briefs nem baseline | M |
| P-h | Ganhos rápidos: UTM + `piece_id` gerados com a peça (fecha a atribuição do `/aprender`); modo avaliações no `/responder-comentarios`; `/coletar-prova` (depoimentos e cases); `/revisar-peca` estendendo o `/otimizar-copy` a roteiro, carrossel e sequência | Nenhum script gera UTM; `agents/mos-ads.md:212` deixa "[com UTMs]" como placeholder | S cada |

Deixado de fora por ora: espanhol LATAM (dilui o posicionamento BR e exige regulação por país; só com ADR).

## Decisões desta rodada (e alternativas rejeitadas)

- Sonda empírica paga em vez de confiar só na doc: a doc e os testes concordavam entre si e estavam errados sobre o runtime nos achados #2 e #3. Custo: 5 execuções curtas com Haiku.
- Sem `git rm` nos `.docx` e sem mexer na conta claude.ai: exigem autorização explícita (OPERATING-MODEL, "Pare e pergunte").
- O worklog não repete o nome da pessoa que aparece no título de um dos `.docx`, para não reexpor o dado ao ser commitado num repo público.
- Achados de subagente só entraram após conferência. Neutralizado: "46 de 48 commands não usam `$ARGUMENTS`" funciona como documentado, porque a plataforma anexa `ARGUMENTS: <input>` quando não há placeholder. Descartada como achado a heurística de h2 fora do TOC nas 6 KBs sem PARTE (métrica ruim do mesmo tipo refutado em jul/2026).
- A resposta do `claude-code-guide` foi usada só onde a doc lida diretamente confirmou: ele atribuiu à doc oficial um texto que vem da tabela de gotchas do próprio AGENTS.md e afirmou que o plugin de marketplace vence o sincronizado, o que a sessão desktop desmente.

## Sequência recomendada de rodadas

1. **Privacidade** (#1): `git rm --cached` dos 3 `.docx`, guard "só `.gitkeep` rastreado em `workspace/`", decisão sobre reescrita de histórico.
2. **"O plugin funciona instalado"** (#2, #3, #5, #6, com #16 como pré-requisito): recursos do plugin via `${CLAUDE_PLUGIN_ROOT}` nos 36 arquivos, com guard contra caminho relativo; estado do usuário no projeto (ou `${CLAUDE_PLUGIN_DATA}` quando for entre projetos); gate de escrita movido para `hooks/hooks.json` com filtro por agent, `agent_type` normalizado e exclusões ancoradas; avisos num canal que chega ao modelo; smoke de instalação real (O2); ADR nova revisando a premissa da ADR-0002; ajuste do build do pacote universal.
3. **Ambiente do mantenedor** (#4): remover ou atualizar o marketplace "Marketing-OS" na conta claude.ai e confirmar 21 agents no app desktop.
4. **Memória** (#7): ADR de path canônico e migração dos diretórios `mos-*` existentes.
5. **Scripts e conteúdo** (#8 a #11, #15): guard de contrato de CLI (O4), bug do gerador de Reels sem o retry no teste, fatos de plataforma com fonte e data (O3), conselhos de compliance, drift de agosto e GETTING-STARTED reescrito.
6. **Roteamento** (#12 a #14, #19 a #23): golden set corrigido e teste cruzado com o corpo do command; `/mo` delegando ao SKILL.md; description da skill com os domínios de vitrine; descriptions em PT-BR com `when_to_use`; SKILL.md abaixo de 500 linhas.
7. **Processo** (#17, #18, #24, #25).
8. **Produto**: P-a primeiro (destrava consistência em tudo), depois O1 em piloto, P-b e P-c.

## Evidências

- Linha de base: `pytest scripts/tests/ -q -m "not smoke"` = 2262 passed, 2 skipped, 22 deselected; `validate_agents.py --strict` = 21/21 clean; `validate_codex_plugin.py .` = aprovado; `pytest --co` = 2286 coletados, 22 smoke.
- Sonda 1 (`claude -p --plugin-dir`, Haiku, sessão em diretório vazio): `out.txt` criado pelo agent de plugin; log com `PLUGIN_PreToolUse_FIRED` e `PLUGIN_SubagentStop_FIRED`, ambos com `agent_type: "hookprobe:probe-writer"`; nenhuma linha `FRONTMATTER_PreToolUse_FIRED`.
- Sonda 2 (`memory: project`): diretório criado `.claude/agent-memory/hookprobe-probe-writer/MEMORY.md`.
- Sonda 3 (skill com `context: fork`, `agent: hookprobe:probe-writer`, `background: false`): resposta `FORK-DONE`, `forked.txt` = "fork ok teste-de-argumento", hooks com `agent_type` do agent do plugin.
- Sondas 4 e 5 (leitura de KB fora do repo): caminho relativo = NOT-FOUND após 10 tentativas; `${CLAUDE_PLUGIN_ROOT}` = primeira linha da KB lida.
- Doc oficial lida diretamente: code.claude.com/docs/en/hooks (matcher sem âncora, nome `plugin-name:agent-name`, bloqueio por código 2), /sub-agents (campos ignorados em agent de plugin, diretório de memória, aviso de 15.000 tokens), /skills (commands fundidos em skills, `context: fork`, `agent`, orçamento de listagem de 1%, limite de 1.536 caracteres, recomendação de menos de 500 linhas, `${CLAUDE_PLUGIN_ROOT}` e `${CLAUDE_PLUGIN_DATA}`).
- Fatos de plataforma via WebSearch: Instagram Reels até 3 min (18/01/2025); YouTube Shorts até 3 min (15/10/2024); Meta Advantage+ Shopping renomeado Advantage+ Sales (fev/2025).
- Execuções diretas: 3 CLIs documentados saíram com erro de argumento obrigatório; `gerar_roteiro` com 48 `KeyError` em 400 sementes.
- Contagens: `find assets/clones -maxdepth 1 -type d ! -name design` = 34; 291 referências relativas em 36 arquivos (script de contagem que ignora o frontmatter e as ocorrências já prefixadas por `${CLAUDE_PLUGIN_ROOT}`).

## Testes

- Rodados: suíte padrão, os dois validadores, coleta com e sem marker smoke, 5 execuções da sonda, 3 CLIs documentados, reprodução do `KeyError`.
- Não rodados e motivo: smoke tests completos (custo real e, pelo #2, rodam no cwd do repo, então não medem o cenário instalado); RT-031/RT-028 (ação manual no ChatGPT Work); instalação via marketplace em projeto limpo (a sonda usou `--plugin-dir`, que aplica o mesmo namespacing e as mesmas restrições de agent de plugin segundo a doc; a diferença de origem não foi testada); `caption_generator.py` (reportado pelo subagente, não medido).

## Falhas da taxonomia tocadas

- F-COPY-04: segue aberto na prática (#3).
- F-REL-03: causa raiz comum de #2, #3 e #4; nenhuma release foi validada instalada fora do repo.
- F-CODEX-03: ocorre no lado Claude sem guard (#1).
- F-BLOAT-02 (#8), F-BLOAT-03 (#23), F-DOC-01 (#15, #17), F-DOC-02 (docs de fev/2026), F-DOC-03 (#10), F-ROUTE-02 e F-ROUTE-04 (#12, #13, #19), F-EVAL-02 (#17).
- Propostas de IDs novos, para registrar na rodada de correção: **F-DIST-01** recurso do plugin por caminho relativo ou estado gravado na pasta do plugin (#2, #5, #6); **F-HOOK-01** hook declarado em superfície que a plataforma ignora (#3a); **F-HOOK-02** identidade de agent assumida sem namespace do plugin (#3b); **F-MEM-01** memória fora do diretório nativo (#7); **F-EVAL-05** teste contorna bug de produção com retry ou skip (#9).

## Rubrica aplicada

- R1 Implementação: N/A (sem mudança de comportamento).
- R2 Documentação: 3. Achados com path:linha, evidência executada e taxonomia; índice atualizado no mesmo diff.
- R3 Roteamento: N/A para a rodada. Estado auditado do sistema: 2 (golden set com 2 contradições, mapa do `/mo` divergente, description da skill sem os domínios de vitrine).
- R4 Output de marketing: N/A. Estado auditado: sem gate determinístico no produto instalado (#3).
- R5 Compatibilidade: N/A para a rodada. Estado auditado: 1 no Claude Code instalado (#2, #3, #4); ChatGPT Work e Codex pendentes de RT-031/RT-028.
- R6 Release: N/A.
- Veredito: relatório pronto para guiar as rodadas; nada a mergear além deste registro.

## Custo aproximado

- Subagentes: cerca de 1,23 milhão de tokens somados (claude-code-guide 189 mil, scripts 364 mil, commands 372 mil, produto 306 mil).
- Sonda: 5 execuções curtas com Haiku (custo marginal).
- Sessão principal: não medida.

## Riscos e follow-ups

- Até a rodada 2, toda instalação real roda sem Tier 2 e sem gate; qualquer avaliação feita no repo superestima o produto instalado.
- Corrigir caminhos sem o smoke de instalação real repete o erro de origem (validar no cwd do repo).
- Mover o gate para `hooks.json` sem filtro por agent bloquearia escritas do usuário fora do Marketing OS (#16).
- Reescrita de histórico para os `.docx` não alcança clones e forks já feitos; avaliar a sensibilidade do conteúdo antes de decidir.
- A migração de memória precisa preservar o que já existe em `.claude/agent-memory/mos-*`.
- O worklog de 2026-08-21 segue sem commit; seus itens foram absorvidos aqui (#15, #17, #18, #25).

## Próximos passos

1. Mantenedor: decidir sobre os `.docx` (rodada 1) e sobre o marketplace da conta claude.ai (rodada 3).
2. Rodada 2 ("o plugin funciona instalado"), começando pelo smoke de instalação real, para que a correção tenha régua (princípio 1).
3. ADRs: revisão da ADR-0002 (gates) e path canônico de memória.
4. Rodadas 4 a 7 conforme a sequência acima.
5. Mantenedor: RT-031 e RT-028 no ChatGPT Work, de preferência depois do #14.
6. Produto: brainstorming de design do P-a antes de codar (disciplina do ROADMAP).
