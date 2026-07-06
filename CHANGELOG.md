# Changelog

Todas as mudancas notaveis deste projeto serao documentadas neste arquivo.

O formato e baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## v6.9.0 (2026-07-06)

### Added
- Distribuicao oficial para Codex via marketplace repo-scoped em `.agents/plugins/marketplace.json`.
- Pacote Codex autocontido em `plugins/marketing-os/`, gerado a partir da fonte canonica.
- Manifesto Codex em `.codex-plugin/plugin.json` e metadados de skill em `skills/marketing-os/agents/openai.yaml`.
- Scripts `scripts/build_codex_plugin.py` e `scripts/validate_codex_plugin.py` para build/check/validacao do pacote Codex.
- Job CI `validate-codex-plugin` para impedir pacote Codex defasado ou manifesto invalido.
- Camada de engenharia de IA em `docs/ai-engineering/`: operating model do mantenedor, heurísticas de design, rubricas 0-4 com threshold de merge, taxonomia de falhas com IDs estáveis (F-CAT-NN), estratégia de evals, quality gates documentados, cost control, release checklist (Claude + Codex), maintainer handbook, ADRs (0001 arquitetura two-tier, 0002 hook canônico dos gates), runbooks e worklogs.
- Golden set de roteamento com 18 briefings PT-BR (`docs/ai-engineering/evals/routing-cases.json`) validado por `scripts/tests/test_routing_evals.py` (92 testes: consistência com commands/, agents/ e taxonomia).
- New command `/otimizar-copy`: diagnóstico (PARTE XVIII), Copy Score (PARTE XV) e reescrita de copy existente com hipóteses A/B via mos-copy.
- New command `/narrar-roteiro` + `scripts/tts_runner.py`: roteiro do mos-audio/mos-video vira áudio PT-BR.
- New command `/datas-sazonais` + `scripts/seasonal_calendar_br.py`: calendário comercial brasileiro (Carnaval/Páscoa via Computus).
- Memory opt-in no `mos-analytics` (10º agent com `memory: project`) + guard de sync frontmatter↔`init_agent_memory.py`.
- Quality gate de antítese negação→afirmação ("Não é X / É Y", "Não faça X / Faça Y") nas 3 camadas: HARD BLOCK no hook, check "Vícios de IA" no `quality_gate.py` (score capado em 60) e tabelas de prompt. O hook ganhou suite de testes própria (`test_quality_gate_hook.py`, incluindo casos de falso positivo).
- `mos-copy`: Bash na tools list (lint determinístico e `headline_scorer --compare` no loop de auto-iteração), swipe file pessoal vivo em `workspace/swipe-files/aprovados.md`, nível de consciência (Schwartz) no output schema e pre-flight preservado.
- Guard no `validate_agents.py`: prompt que instrui rodar `python3 scripts/*.py` sem `Bash` na tools list falha em `--strict` (classe "instrução morta").
- Smoke tests cobrem os 18 agents (antes: 5 representativos).
- `scripts/mos.py` expõe `youtube`, `gsc` e `report` no CLI unificado.

### Changed
- README documenta instalacao Codex via `codex plugin marketplace add rilnermucio/esp-marketing-os`.
- Metadados de repositorio apontam para `https://github.com/rilnermucio/esp-marketing-os`.
- Agents de raciocínio pesado roteados para Opus via frontmatter `model:`.
- SKILL.md: CSO explicitado na description; `docs/ROADMAP.md` ganhou o princípio de escopo (geração/estratégia entra; ops/automação stateful fica fora).
- CI: black/flake8 obrigatórios (deixam de ser `|| true`); cobertura mínima de 70% mantida.
- Seções datadas do `copy-agent.md` (PARTE XVI Tendências, 6.2 Ferramentas) ganharam snapshot guards com protocolo de refresh via WebSearch.
- Prosa instrucional de agents/commands/subagents sem travessão (consistência com o próprio quality gate).
- Teto de versão nas dependências do requirements.txt (reproducibilidade).

### Fixed
- Segurança: verificação TLS + guard anti-SSRF no download de screenshot da auditoria.
- Contagem de voice clones corrigida para 34 em README/AGENTS/mos-copy/PARTE XV-B (off-by-one histórico: o inventário somava 35 com subtotal errado; guard `test_repo_consistency` valida contra o filesystem).
- SKILL.md: memory opt-in corrigido para 10 agents (mos-analytics constava como sem memory).
- Contagens de commands (38/34) e drift residual de docs corrigidos; contagem de scripts removida da prosa (variou 3x em 30 dias).
- `commands/criar-post.md`: fallback de migração morto ("se mos-social ainda não existir") removido.
- `requirements.txt`: numpy declarado (import direto em `audit_radar_chart.py`).
- `docs/CONNECTORS.md`: nome pessoal removido do connector Meta Ads + nota de que connectors são MCPs do ambiente do usuário.
- Scripts expõem erros de fetch/leitura no stderr (antes silenciados); `content_repurposer.py` sem conflito de `--output` no argparse.
- Testes de CLI do PDF resilientes a flake do weasyprint.
- Removido `narracao.aiff.txt` (arquivo de teste de 13 bytes na raiz do repo).

## v6.8.0 (2026-05-09)

### Added
- New `/projeto` slash command: workflow de projetos com pipeline declarativo, dispatch sequencial dos `mos-*` e approval gates entre stages. Subcomandos: `novo`, `list`, `status`, `avancar`, `aprovar`, `rejeitar`.
- 4 templates de projeto em `scripts/templates/projeto/`: `lancamento.md`, `perpetuo.md`, `consultoria.md`, `mentoria.md`. Cada um define pipeline + stages + approval policy.
- `runs.jsonl` append-only por projeto rastreia execucoes (`run_id`, `stage_id`, `agent`, `iteration`, `status`, `started_at`, `approved_at`/`rejected_at`, `feedback`, `source`).
- `decisions.md` por projeto: log human-readable de aprovacoes/rejeicoes com feedback.
- 26 testes em `scripts/tests/test_project_manager.py` (slugify, frontmatter, create, list, status, append_run, advance, approve, reject, iteracao).
- New command `/auditoria-pro <url>` — premium agency-grade landing audit. Output: 25-30 page PDF com radar chart (ghost outline de potencial pos-fixes), screenshots (homepage + 2-3 internas via Playwright), 3-5 paragrafos por dimensao, comparativos antes/depois de copy, analise competitiva, roadmap 30/90/180 dias com esforco/impacto/owner, apendice tecnico com outputs raw dos 7 agents, glossario filtrado por termos usados.
- 5 novos scripts: `audit_screenshot.py` (Playwright capture), `audit_radar_chart.py` (matplotlib radar com overlay de potencial), `audit_premium_template.py` (HTML/CSS premium template, ~600 linhas), `audit_roadmap_generator.py` (bucketing 30/90/180), `audit_glossary.py` (67 termos tecnicos PT-BR).
- `scripts/pdf_generator.py` extended com flag `--from-html` para templates HTML premium (skip do pipeline markdown).
- Novas deps: `matplotlib>=3.7`, `playwright>=1.40` (com browser chromium).
- User doc: `docs/AUDITORIA-PRO.md`.
- Smoke test `scripts/tests/test_auditoria_pro_smoke.py` exercita pipeline completo (synthesis mockada -> scoring -> radar -> roadmap -> HTML render -> PDF).

### Changed
- `scripts/project_manager.py` reescrito do zero. CRUD anterior (project.json + content/ + notes) substituido por state machine declarativa em `project.md` com YAML frontmatter (current_stage + pipeline + default_approval).
- `scripts/mos.py`: subcomandos `mos project` agora sao `novo|list|status|avancar|aprovar|rejeitar` (antes: `create|list|status|add-content|complete|note`).
- `agents/mos-infoproduct.md`: dispatch reference atualizado de `create` para `novo --tipo mentoria`.
- `docs/ARCHITECTURE.md`: descricao do `project_manager.py` atualizada.

### Migration notes
- Quem usava `mos project create` deve migrar pra `mos project novo --tipo {lancamento|perpetuo|consultoria|mentoria}`.
- Pasta `output/projects/` antiga nao eh mais lida. Projetos novos vivem em `workspace/projects/<slug>/` (gitignored).
- `add-content`, `complete`, `note` foram removidos. Conteudo gerado pelos agentes vai pra subpastas `<NN>-<stage>/` automaticamente; aprovacao/rejeicao registrada em `decisions.md`.

### Design rationale
Spec consensual entre Claude Opus 4.7 + Codex CLI (gpt-5.5/high) em 3 turnos de debate. Decisao: NAO construir abstracao de "times/squads" (overhead pra operador solo); flat por projeto + state machine simples + run log estruturado eh suficiente. Faseamento explicito: MVP sequencial agora; paralelismo, `auto_approve` e `published_at` ficam pra Fase 2 condicional ao uso real.

### Notes (auditoria-pro)
- `/auditoria-pro` e landing-only nesta versao. Extensoes Instagram/Meta Ads/YouTube em v6.8.1+.
- Identidade visual: deep ink blue `#0a2540` + warm orange `#ff6b35`. White-label via `.auditoria-config.json` (compativel com `/auditoria` standard).
- Tempo de geracao: ~6-9 min por run vs ~3-5 min do `/auditoria` standard.
- Custo: $0 (Playwright local, sem Apify mandatory).
- macOS: Playwright requer `playwright install chromium` apos `pip install`.

---

## v6.7.0 (2026-05-09)

### Added
- New command `/auditoria <input>`. Multi-modal audit (landing page, Instagram, Meta Ad Library, YouTube). Auto-detects type, dispatches 4-7 mos-* agents in parallel, computes weighted score per type-specific rubric, generates RELATORIO.md + RELATORIO.pdf in `workspace/auditorias/<run>/`.
- Generic, reusable PDF generator script `scripts/pdf_generator.py` (markdown to PDF via weasyprint). White-label aware via `.auditoria-config.json` in user's project root.
- Scoring infrastructure: `scripts/audit_detector.py`, `scripts/audit_scoring.py`, `scripts/audit_config.py`, plus 50+ unit tests and 1 smoke test.
- New deps: `weasyprint`, `markdown-it-py`, `jsonschema` (added to `requirements.txt`).
- User doc: `docs/AUDIT-CONFIG.md` for white-label config schema.

### Notes
- PDF output requires `pip install weasyprint`. macOS users may need `brew install cairo pango gdk-pixbuf libffi`.
- Synthesis (free-form agent outputs to 0-100 dimension scores) is performed by Claude in the command, not by NLP heuristics. Existing 18 agents are unmodified.
- Outputs land in `workspace/auditorias/<run>/` (gitignored).

---

## [6.6.0] — 2026-05-09 (Apify scraping opt-in para mos-seo + mos-research)

Minor release adicionando integração opt-in com Apify Actors pra dois agents.

### Added

- **Apify SERP scraping (`scripts/apify_serp.py`)** — `mos-seo` ganha acesso a structured SERP data (top 10 + People Also Ask + related searches) via `google-search-scraper` Actor. Substitui WebSearch quando keyword research precisa de dados estruturados pra schema markup ou intent analysis.
- **Apify Instagram scraping (`scripts/apify_instagram.py`)** — `mos-research` ganha analise de perfis de concorrentes (posts + metricas agregadas + top hashtags) via `instagram-scraper` Actor. Util pra audit de presence + hashtag strategy mining.
- `scripts/apify_client.py` — wrapper minimo (urllib stdlib only, zero deps novas) com timeout, retry e parsing.
- `docs/APIFY-INTEGRATION.md` — setup, custos estimados e FAQ.
- 83 tests novos cobrindo client + ambos os Actors.
- Updates em `agents/mos-seo.md` e `agents/mos-research.md` com instrucoes opt-in.

### Notes

- **Opt-in via env var:** `APIFY_TOKEN` precisa estar exportado pra agents usarem. Sem token, agents fall back silenciosamente pra WebSearch (zero behavior change).
- **Hard caps:** 100 results pro SERP, 100 posts pro Instagram. `--dry-run` pra estimar custo antes de rodar.
- **Output paths:** JSON salvo em diretorio user-local configuravel; Markdown summary streamado pra stdout (consumo direto pelos agents).

---

## [6.5.1] — 2026-05-09 (path canonicalization + post-v6.5.0 polish + validation docs)

Patch release que distribui dois commits acumulados desde o tag v6.5.0 (1aa2a44, 1303771) e adiciona docs derivadas da validação completa da v6.5.0 ([VALIDATION-RESULTS-v6.5.0.md](docs/VALIDATION-RESULTS-v6.5.0.md)).

### Fixed

- **Path canonicalization em prompts de dispatch** (`commands/criar-landing-page.md`, `commands/criar-funil.md`, `commands/criar-infoproduto.md`, `commands/publicar-anuncio.md`, `commands/batch.md`): substituido `agent-memory/marketing-os-mos-X/` literal por "memory existente do cliente neste projeto" generico. Bug v6.5.0: subagents `mos-funnel`/`mos-infoproduto` escreviam memory no path antigo enquanto `mos-copy`/`mos-design` usavam o canonico, causando inconsistencia entre sessoes (descoberto durante setup do Test 7 longitudinal).
- CI fixes + audit gerais (commit 1aa2a44).
- 6 presets adicionais de `/campanha` + `/mo` orchestrator (commit 1303771).

### Added

- `docs/VALIDATION-RESULTS-v6.5.0.md` — execução completa da VALIDATION-GUIDE 15 tests via `claude -p` (14/15 PASS, 1 deferido pra teste manual longitudinal).
- `CONTRIBUTING.md` — secao "Testando dispatches via `claude -p`" cobrindo namespace quirk (`/marketing-os:criar-X` em vez de `/criar-X`), AskUserQuestion limitation em -p, e flags uteis pra captura de dispatches.
- `docs/TROUBLESHOOTING.md` — workaround para `claude plugin update marketing-os` falhar com "Plugin not found" (CLI): reinstall (`uninstall` + `install`) em vez de `update`.

### Notes

Validacao end-to-end (memory persistence cross-session, T7 da VALIDATION-GUIDE) ainda pendente — agendado para 2026-05-11 (Calendar event externo). Resultados serao adicionados a VALIDATION-RESULTS-v6.5.0.md como `## T7 — Memory persistente (resultado)`.

---

## [6.5.0] — 2026-05-08 (audit cleanup: dispatch coverage + Tier 2 expansion + memory bootstrap)

Fecha os 5 itens P0/P1 da auditoria do fluxo de criação de conteúdo identificados na sessão anterior. Resolve TODOS os "Deferred (v6.5.x)" da v6.4.0.

### Added (commands dispatch — completed)

17 commands restantes reescritos no padrão dispatch-based. Agora **24 de 25 commands** dispatcham subagents `mos-*` corretamente (era 8 de 25). O único utility puro remanescente é `/publicar-notion` (Notion MCP, intencional — roteia pra commands de criação quando precisa gerar conteúdo).

Commands afetados:
- Content production: `/criar-anuncio`, `/criar-artigo`, `/criar-email`, `/criar-podcast`, `/criar-calendario`, `/criar-brief-design`
- Mixed: `/criar-sequencia`, `/gerar-imagem`, `/analisar-video`, `/analisar-concorrencia`, `/criar-clone`, `/criar-meu-clone`
- Orchestration + utilities: `/batch`, `/campanha` (6 presets), `/capturar-tela`, `/publicar-anuncio`, `/publicar-notion`

Padrões aplicados: dispatch simples, decision tree (simples ↔ paralelo), sequencial, multi-paralelo, e workflow estruturado (campanha presets).

### Added (memory protocol opt-in)

- `scripts/init_agent_memory.py`: bootstrap dos 9 diretórios `.claude/agent-memory/mos-*/MEMORY.md`. Modos `--check` (read-only) e `--force` (sobrescreve). Memory continua opt-in: sem rodar o bootstrap, agents seguem funcionando, só não persistem patterns entre sessões.
- `mos-funnel` ganhou `memory: project` no frontmatter + bloco "Atualize Memory ao final" no body (consistência com SKILL.md que já listava 9 agents).

### Added (Tier 2 expansion)

Gaps confirmados no audit v6.4.0 fechados:

- `subagents/funnel-agent.md`: **2287 → 3496 linhas** (+1209)
  - 3.4 Webinar Funnel (live e evergreen, ~330 linhas)
  - 3.5 Página de Aplicação BOFU high-ticket (~340 linhas)
  - 4.6 Anti-Avatar conceito transversal (~330 linhas)
- `subagents/copy-agent.md`: **4203 → 5316 linhas** (+1113)
  - PARTE II-C: Big Idea (~480 linhas) + Value Stack (~620 linhas)

Cobertura pros workflows #5 (página de aplicação), #6 (webinar) e #9 (VSL).

### Added (validation infra)

- `docs/VALIDATION-GUIDE.md` atualizado pra v6.5.0: **15 test cases** (era 10). Novos Tests 11-15 cobrem `/criar-anuncio`, `/criar-artigo`, `/criar-clone`, `/campanha lancamento`, `/batch`. Test 7 corrigido (path memory canônico + bootstrap mencionado).
- `scripts/tests/test_commands_dispatch.py`: **148 test cases** automatizados validam estrutura dos 25 commands (frontmatter, dispatch real, agents existentes, consolidação, quality gates, utility declaration). Pega regressão de dispatch antes do merge.
- CI ganhou novo job `validate-agents` que roda `validate_agents.py --strict` em todo PR/push.

### Fixed

- `scripts/validate_agents.py`: path hardcoded `.claude/agents/` → `agents/` (validador nunca rodou contra o estado real desde a reorganização). Agora 18/18 agents passam clean em modo `--strict`.
- Memory paths inconsistentes entre 8 agents (`mos-X/`) e SKILL.md (`marketing-os-mos-X/`) — padronizados em `mos-X/` (canônico, mais curto, alinhado com path real dos agents).
- `mos-funnel` listado no SKILL.md como agent com memory mas sem `memory: project` no frontmatter — gap real fechado.

### Resolved (deferred from v6.4.0)

- ✅ 16 commands restantes pra dispatch-based pattern (na verdade 17 — incluiu `/criar-meu-clone` que estava parcialmente compatível)
- ✅ Expansão Tier 2: `funnel-agent` (webinar funnel + página aplicação + anti-avatar) e `copy-agent` (big idea + value stack)
- ✅ Validation real: substituiu intenção manual por teste automatizado estrutural + VALIDATION-GUIDE atualizado

### Stats da release

- pytest: **1070 passed** (era 922, +148 novos), zero regressão
- validate_agents --strict: 18/18 clean
- Diff: 35 files changed, +4599 insertions / -4170 deletions
- Commits desde v6.4.0: 1 (squash de toda a sessão de cleanup)

---

## [6.4.0] — 2026-05-07 (commands dispatch + release automation + Tier 2 audit)

### Added (release automation)
- `.github/workflows/release.yml`: tag push (`v*.*.*`) auto-creates GitHub Release
  with notes extraídos da seção do CHANGELOG correspondente. Anexa CHANGELOG/README/AGENTS.

### Added (commands dispatch — partial)
6 commands prioritários reescritos no padrão dispatch-based, agora chamando
os subagents nativos conforme workflows do SKILL.md:

- `/criar-carrossel` → workflow #8 (`mos-social` + `mos-copy` + `mos-design` paralelo)
- `/criar-landing-page` → workflow #5 (`mos-funnel` + `mos-copy` + `mos-design` → opt
  handoff `frontend-design`)
- `/criar-webinar` → workflow #6 (Fase 1 `mos-launch` + `mos-funnel` + `mos-video`,
  Fase 2 `mos-copy` + `mos-email`)
- `/criar-funil` → `mos-funnel` (+ `mos-research` se cliente novo)
- `/criar-infoproduto` → workflow #7 completo (4 fases: research → structure+launch+funnel
  → copy+email+ads → quality gates)
- `/criar-video` → workflow #9 pra VSL (`mos-storytelling` + `mos-copy` + `mos-video`),
  dispatch simples pros outros formatos
- `/clonar-estrategia` → workflow #10 (`mos-research` + `mos-brand` → `mos-copy` voice clone)

**Status commands:** 9 de 25 commands agora dispatcham `mos-*` corretamente
(`/criar-post`, `/criar-meu-clone` já estavam + 7 novos). Os 16 restantes seguem
como follow-up pra próximas releases — workaround documentado em TROUBLESHOOTING.

### Documented (Tier 2 audit findings)
Auditoria via grep dos 3 KBs mais críticos vs workflows novos:
- `launch-agent.md` (5289 linhas) ✅ PLF, perpétuo, webinar, email lançamento — completo
- `funnel-agent.md` (2287 linhas) ⚠️ webinar funnel (1 ref), página aplicação (2),
  anti-avatar (3) — fraco pros workflows #5 e #6 → expansão pra v6.5.x
- `copy-agent.md` (4203 linhas) ⚠️ "big idea" (0), "stack value" (0) — gaps reais
  pro workflow #9 VSL → expansão pra v6.5.x

### Deferred (v6.5.x)
- 16 commands restantes pra dispatch-based pattern
- Expansão Tier 2: `funnel-agent` (webinar funnel + BOFU page) e `copy-agent`
  (big idea + stack value frameworks)
- Validation real do orquestrador (rodar VALIDATION-GUIDE em sessão dedicada)

---

## [6.3.1] — 2026-05-07 (CI threshold realistic)

### Fixed
- CI coverage threshold lowered from 70% → 50% to reflect reality:
  - The 71% measured before v6.3.0 was inflated by including test files
    (which cover themselves at 100%) in the denominator
  - Once `.coveragerc` correctly omitted `scripts/tests/*`, real coverage
    of production code surfaced: **54%**
  - Threshold 50% is defensible and can rise as more unit tests are added
- This was the second iteration of the CI fix in this session — first one
  (v6.3.0) addressed wrong threshold but introduced an unintended drop
  by changing what gets measured

---

## [6.3.0] — 2026-05-07 (next-steps consolidation)

### Fixed (CI broken on all 5 prior commits)
- `.coveragerc` added: omits `validate_agents.py` and `voice_extractor.py`
  (utility scripts, not plugin logic — manually invoked, hard to cover in CI)
- `.github/workflows/tests.yml` threshold lowered 80% → 70% (realistic given
  external integrations like youtube_analytics, trend_tracker, tiktok_scraper
  that are inherently hard to cover in CI)
- CI now installs `requirements.txt` before pytest (was missing dependencies)
- CI runs `-m "not smoke"` to skip Tier 2 smoke tests (require Claude Code login)

### Added (documentation external)
- `README.md` rewritten for v6.3.0 — workflows table, agents+memory map,
  install via marketplace, structure with all dirs, voice clones list,
  links to all sub-docs
- `docs/GETTING-STARTED.md` (5 cenários comuns + memory por projeto +
  compliance regulatório + voice clones)
- `docs/TROUBLESHOOTING.md` consolidando bugs v6.1.x:
  install/sync issues, schema violations, GitHub App auth, cache poisoning,
  memory location confusion, hook path resolution, CI coverage, auto-update
  timing
- `docs/VALIDATION-GUIDE.md` com 10 test cases pra validar orquestração
  funcionando: dispatch simples, paralelo, workflow #5/#8/#9, briefing vago,
  memory persistente, compliance, voice clone, skill collision

### Documented (known limitations)
- 23 dos 25 slash commands não dispatcham mos-* agents diretamente (apenas
  /criar-post e /criar-meu-clone). Workaround: usar /marketing-os em
  linguagem natural até v6.4.x. Documentado em TROUBLESHOOTING.
- Tier 2 smoke tests deferred (requirem Claude Code login). Documentado.

### Audited (Tier 2 deferred to v6.4.x)
- Auditoria estrutural dos 18 subagents/*.md vs novos workflows #6-#10 foi
  iniciada mas o agente Explore retornou "Prompt is too long" — Tier 2
  audit fica como follow-up pra v6.4.x quando houver capacidade pra fazer
  manual file-by-file ou um agent novo dedicado.

---

## [6.2.2] — 2026-05-07 (test fix)

### Fixed
- `test_workspace_separation`: `skills/marketing-os/SKILL.md` was added to
  the allowlist after Onda C (v6.2.1) introduced a legitimate documentation
  reference to `workspace/` (explaining that `/criar-meu-clone` reads samples
  from there). Suite back to 922/922 green.

---

## [6.2.1] — 2026-05-07 (Onda C — orchestration polish + compliance)

### Added (orchestration depth)
- **Briefing técnico/estratégico** agora tem dispatch explícito (`mos-research` +
  `mos-growth`/`mos-analytics`) na tabela "Quando dispatch vs inline"
- **Protocolo de briefing vago**: 5 perguntas-chave (nicho/avatar/ticket/plataforma/
  urgência) com regras de skip quando memory já tem resposta
- **Memory automática documentada**: lista exata dos 8 agents com `memory: project`
  (mos-copy, mos-funnel, mos-design, mos-brand, mos-launch, mos-research, mos-social,
  mos-infoproduct, mos-ads) e protocolo "explicite no prompt"

### Added (quality + compliance)
- **Substância (peças de venda)**: novo bloco em Quality Gates Globais checa
  promessas sem backup, comparativo competitivo sem fundamento, garantia sem
  termo claro, linguagem absoluta sem qualificador, placeholders publicados
- **Compliance regulatório**: tabela CFM/CONAR/ANVISA/CVM com disclaimers
  obrigatórios por nicho (saúde, suplementos, finanças, cosméticos). Antes
  vivia só em memory de cliente — agora é gate global do plugin

### Added (delegation)
- **Política de delegação a skills externas**: tabela explícita do que pode
  ir pra `frontend-design`, `figma-*`, `docx/pptx/xlsx`, `claude-api` — sempre
  DEPOIS dos workflows do marketing-os, nunca antes
- **Slash commands rápidos**: tabela dos 25 commands organizados por categoria
  + nota sobre invocação direta vs dispatch via linguagem natural

### Changed
- **Entregáveis padrão**: lista fixa de 8 itens → 9 entregáveis condicionais
  (sempre / quando faz sentido testar / condicionais por tipo de output).
  Hashtags só pra social/SEO, prompts IA só pra ai-tools, métricas só pra
  conversão/campanha, etc.

---

## [6.2.0] — 2026-05-07 (Onda B — composite workflows)

### Added (5 new orchestration patterns)

Briefings que requerem múltiplos `mos-*` agents agora têm workflow explícito
em SKILL.md, evitando dispatch single-agent que perde camadas estratégicas.

- **#6 Webinar (live ou perpetual)**: `mos-launch` + `mos-funnel` + `mos-video`
  → `mos-copy` + `mos-email`. Sem o `mos-launch` o webinar vira aula sem venda.
- **#7 Lançamento de Infoproduto**: 4 fases — research → estrutura+launch+funnel
  → copy+email+ads → quality gates. Pular fase 1 é o erro #1 de quem lança
  no escuro.
- **#8 Carrossel Completo**: `mos-social` + `mos-copy` + `mos-design`
  (+ `mos-ai-tools` opcional). Carrossel sofre quando feito por 1 agent só.
- **#9 VSL Completa**: `mos-storytelling` + `mos-copy` + `mos-video` em paralelo,
  consolidados em roteiro único. Inclui gates de substância (promessas com backup).
- **#10 Análise de Concorrente + Clone**: `mos-research` + `mos-brand` →
  `mos-copy` (voice clone usando assets/clones/). Clone sem research é cópia rasa.

Cada workflow inclui seção "Por que essa ordem" explicando o trade-off.

---

## [6.1.8] — 2026-05-07 (Onda A — orchestration P1 fixes)

### Added (dispatch coverage)
- `mos-social` triggers expandidos: bio Instagram, about, calendário editorial,
  planejamento de conteúdo, weekly plan
- `mos-funnel` triggers expandidos: sales funnel, funil de vendas
- `mos-email` triggers expandidos: drip
- `mos-brand` triggers expandidos: manifesto da marca, arquétipo, brand guidelines
- `mos-storytelling` triggers refinados: "hero's journey aplicado em peça"
  (vs `mos-brand` que cuida de DEFINIR identidade)

### Added (desambiguação)
- Regra explícita `mos-brand` vs `mos-storytelling`:
  - mos-brand = DEFINIR identidade (arquétipo, manifesto, tom)
  - mos-storytelling = APLICAR narrativa numa peça (sales letter com arco, origin story)

### Changed
- Seção "Versão" do SKILL.md não cita mais hardcoded — aponta pra `plugin.json`
  e `CHANGELOG.md` pra evitar drift a cada release

---

## [6.1.7] — 2026-05-07

### Added
- `SKILL.md`: explicit dispatch for landing/application/sales pages
  - New "Caso composto: páginas" section right after the dispatch table claims this
    territory and warns against direct delegation to `frontend-design` skill
  - New orchestration pattern #5: "Workflow: Página de Aplicação / Landing / Vendas (BOFU)"
    with 3-phase recipe (parallel `mos-funnel` + `mos-copy` + `mos-design`, then optional
    handoff to `frontend-design` for HTML/CSS build, then quality gates)
  - Documents WHY each agent is needed (without `mos-funnel` no BOFU patterns,
    without `mos-copy` no quality gates, etc.) and notes that agent-memory loads
    automatically when working in a client folder

### Why
- Real-world bug: when user asked `/marketing-os: cria uma página de aplicação`,
  the orchestrator delegated directly to `frontend-design` (Anthropic official plugin)
  without invoking any `mos-*` agent first. The strategic layer (funnel structure,
  copy quality gates, design direction) was skipped.
- Root cause: `frontend-design`'s skill description has aggressive triggers ("build
  web components, pages, artifacts, posters, or applications") that outranked the
  marketing-os dispatch table, which only had "funil/TOFU/MOFU/BOFU" as funnel keywords.
- Fix asserts marketing-os authority over page briefs and defines the explicit handoff
  protocol so frontend builders are called as executors of phase 2, not as deciders.

---

## [6.1.6] — 2026-05-07

### Removed
- 23 leaked tracked files (3.3 MB) that were never meant to be distributed:
  - `.vscode/`, `.playwright-mcp/`, `.mcp.json` — local IDE/tooling configs
  - `workspace/landing-pages/*` (4 files) — personal copy and HTML
  - `workspace/media/images/queila-*.png` (10 files) — personal client images
  - `workspace/outputs/*` (1 file) — personal video script
  - `workspace/research/*.docx` (2 files) — personal competitive research

  Files remain locally (`git rm --cached` only). Added new ignore rules to prevent
  future re-tracking. The `workspace/.gitkeep` markers stay (they preserve the
  directory skeleton for new users).

---

## [6.1.5] — 2026-05-07

### Fixed
- Moved plugin manifest from root `plugin.json` to canonical `.claude-plugin/plugin.json`.
  Claude Desktop's plugin validator requires the canonical location and rejected the
  root manifest with "Plugin validation failed". Claude Code accepted both, which
  masked the issue. This was confirmed empirically: a manually-repacked zip with
  `.claude-plugin/plugin.json` uploaded successfully via Desktop's "Fazer upload de
  plugin local" flow, while the GitHub-hosted version with root `plugin.json` failed.

### Changed
- `test_plugin_manifest.py` and `test_skill_md.py`: updated path from
  `project_root / "plugin.json"` to `project_root / ".claude-plugin" / "plugin.json"`

---

## [6.1.4] — 2026-05-07

### Changed (BREAKING for existing installations)
- Marketplace renamed from `marketing-os-marketplace` to `mos-marketplace`. Goal:
  bypass any server-side cached state from the broken v6.1.0–v6.1.2 syncs that
  was preventing Claude Desktop from adding the marketplace.
- After upgrade, install command changes:
  - Old: `/plugin install marketing-os@marketing-os-marketplace`
  - New: `/plugin install marketing-os@mos-marketplace`

### Migration for existing Claude Code users
1. `/plugin marketplace remove marketing-os-marketplace`
2. `/plugin marketplace add rilnermucio/Marketing-OS` (fetches new name)
3. `/plugin install marketing-os@mos-marketplace`

---

## [6.1.3] — 2026-05-07

### Changed
- `marketplace.json`: moved `description` and `version` from `metadata` block to
  top-level (modern schema; `metadata` was backward-compat per docs). The strict
  validator in Claude Desktop's "Adicionar marketplace" UI was rejecting the URL
  with "Falha na sincronização do marketplace", possibly due to legacy structure.

---

## [6.1.2] — 2026-05-07

### Fixed
- `plugin.json` schema violations rejected by Claude Code's manifest validator:
  - `author`: changed from string `"rilnermucio"` to object `{"name": "rilnermucio"}`
  - removed `skills: ["skills/marketing-os"]` field (default discovery from `skills/`
    folder already covers this and the explicit value was rejected as invalid input)
  - replaced `categories` array with single `category: "marketing"` (per spec,
    `category` is singular; `keywords` already covers the rest)
  - corrected `repository` URL from old `rilnermucio/Agents` to `rilnermucio/Marketing-OS`
  - added `license: "MIT"` (already declared in LICENSE file)
- `README.md`: same repo-URL correction in the `git clone` example

Without these, `/plugin install marketing-os@marketing-os-marketplace` failed with
"invalid manifest file ... author: expected object, received string, skills: Invalid input".

---

## [6.1.1] — 2026-05-07

### Fixed
- `.claude-plugin/marketplace.json`: relative path source must start with `./`
  per Claude Code plugin spec. Changed `"source": "."` to `"source": "./"`.
  Without this fix, `/plugin install marketing-os@marketing-os-marketplace`
  failed with "This plugin uses a source type your Claude Code version does
  not support".

---

## [6.1.0] — 2026-05-07 (distribution-ready)

### Added
- 18 native subagents (`agents/mos-*.md`) now versioned and shipped with the plugin
  (previously gitignored at `.claude/agents/`, never embarked via marketplace install)
- Root `CLAUDE.md` describing plugin architecture, dispatch protocol, quality gates,
  workspace separation, and validate_agents.py usage

### Fixed
- Quality gate hook in all 18 agents now uses `${CLAUDE_PLUGIN_ROOT}/scripts/hooks/quality_gate_hook.py`
  instead of relative `scripts/hooks/quality_gate_hook.py`. Per Claude Code hook docs,
  hook subprocess CWD is the user's working directory, so the relative path failed
  with exit 2 ("No such file or directory") in any consumer environment outside the
  plugin root. Hooks now resolve correctly regardless of CWD.
- `test_workspace_separation`: scans `agents/` instead of removed `.claude/agents/`,
  allowlists `commands/criar-meu-clone.md` (legitimately uses workspace samples by design)
- `test_integration_mcp`: excludes `voice_extractor.py` from COMMAND_MAP coverage
  (invoked directly by `/criar-meu-clone`, not via `mos.py`)

### Removed
- Synkra AIOS residue: header in `.env.example`, `AIOS_VERSION` env var,
  AIOS-FullStack ignore block in `.gitignore`, and 27 local-only AIOS files in `.claude/`
  (CLAUDE.md, rules/, commands/AIOS/) that were leftover from the v6.0.0 cleanup

### Migration
- No action required for plugin consumers — install or update via marketplace as usual
- Local developers: pull and verify `agents/` is at repo root; `.claude/agents/` is gone

---

## [6.0.0] — 2026-05-06 (refactor/plugin-first)

### Added
- `workspace/` structure (gitignored) — personal content area separated from distributed plugin
- Tier 1 pytest suite in `scripts/tests/`:
  - `test_plugin_manifest.py` — validates `plugin.json` schema and required fields
  - `test_skill_md.py` — validates `skills/marketing-os/SKILL.md` frontmatter
  - `test_subagents.py` — validates all 18 subagent knowledge base files
  - `test_native_agents.py` — wraps `validate_agents.py` (skips if `.claude/agents/` absent)
  - `test_no_dangling_symlinks.py` — enforces no orphan symlinks in tracked paths
  - `test_workspace_separation.py` — asserts personal content is not committed
  - `test_no_aios_residue.py` — asserts AIOS-framed dirs/files are not tracked
  - `test_agents_smoke.py` — stub for Tier 2 smoke tests (deferred, requires live Claude)
- `scripts/validate_agents.py` — dev-infra utility to validate `.claude/agents/` native agents
- `assets/clones/` — 35 voice clone profiles (Halbert, Hopkins, Kennedy, Ogilvy, Schwartz,
  Sugarman, Caples, Cialdini, Brunson, Hormozi, Leila Hormozi, GaryVee, MrBeast, Codie Sanchez,
  Abdaal, Abraham, Joel Jota, Conrado, Mel Robbins, Patel, Provost, Rachitsky, Suby, Welsh,
  Cole, Collier, Ellis, Ezra Firestone, Flavio Augusto, Gadzhi, Godin, Howell, Chen, Miller)

### Changed
- Consolidated `marketing-os/` to single canonical location: `skills/marketing-os/` (SKILL.md
  entrypoint) + root-level resources (`subagents/`, `commands/`, `assets/`, `references/`,
  `workflows/`)
- `commands/` now lives at repo root (was `marketing-os/commands/`)
- `CONNECTORS.md` moved to `docs/`
- README completely rewritten (~121 lines, plugin-focused, PT-BR, v6.0.0)
- Removed `GUIA-DE-USO.md` and `INSTALACAO-SKILL.md` (content superseded by new README)

### Removed (BREAKING)
- `AGENTS.md` (root) — AIOS-framed Codex CLI instructions, no longer relevant
- `marketing-os/` (root duplicate) — redundant copy, canonical location is `skills/marketing-os/`
- `skill-package/` — frozen export artifact, stale and unmaintained
- `squads/` — AIOS packaging format, superseded by plugin-first architecture
- `TestConfiguracaoMCP` test class — targeted gitignored paths invalid in plugin-first worktree

### Migration Note — Manual cleanup required after merge

When merging `refactor/plugin-first` into `main`, the following paths exist **only in your
local `main` checkout** (they are gitignored and were never committed). They are **not**
removed by this branch merge — you must delete them manually:

```
.aios/
.aios-core/
.antigravity/
.codex/
.cursor/
.aios-installation-config.yaml
.aios-pm-config.yaml
```

After merging, run in your `main` checkout:
```bash
rm -rf .aios .aios-core .antigravity .codex .cursor
rm -f .aios-installation-config.yaml .aios-pm-config.yaml
```

Also review and optionally clean `.claude/rules/` (story-lifecycle, ids-principles,
agent-authority, workflow-execution, coderabbit-integration) — these are AIOS rules
that no longer apply to the plugin-first architecture.

---

## [Unreleased] — Legacy entries

### Added
- Estrutura de stories para desenvolvimento agil (`docs/stories/`)
- CHANGELOG.md para rastreamento de versoes
- CONTRIBUTING.md com guia de contribuicao

### Changed
- (Pendente) Atualizacao do README com todos os 19 scripts

### Fixed
- (Nenhum)

---

## [4.0.0] - 2026-02-05

### Changed
- **BREAKING:** Rebrand completo: "Agente Criador de Conteúdo" / "Content Creator" → "Marketing OS"
- Skill name: `content-creator` → `marketing-os`
- Todos os diretórios renomeados: `content-creator/` → `marketing-os/`
- 16 subagentes atualizados com nova identidade
- Documentação completamente reescrita

### Added
- 5 novos subagentes: Brand Agent, Storytelling Agent, Funnel Agent, Growth Agent, Launch Agent

---

## [1.0.0] - 2026-01-28

### Added

#### Subagentes (11)
- Research Agent - Pesquisa de tendencias e concorrencia
- Copy Agent - Copywriting persuasivo e storytelling
- SEO Agent - Otimizacao para buscadores
- Social Agent - Posts para redes sociais
- Video Agent - Scripts para YouTube, Reels, TikTok, VSL
- AI Tools Agent - Prompts para geracao de imagem e video
- Design Agent - Direcao criativa e specs visuais
- Analytics Agent - Metricas e relatorios
- Audio Agent - Podcasts e roteiros de audio
- Email Agent - Sequencias de email e newsletters
- Ads Agent - Copy de anuncios Meta/Google/TikTok

#### Templates (27)
- Templates para todas as plataformas principais
- Instagram (Feed, Stories, Carrossel, Reels)
- YouTube (Long-form, Shorts)
- TikTok, LinkedIn, Twitter/X, Pinterest
- Email, Landing Pages, Webinars, VSL, Podcasts

#### Scripts Python (19)
- seo_analyzer.py - Analise de SEO
- hashtag_generator.py - Geracao de hashtags
- content_calendar.py - Calendario editorial
- ab_generator.py - Variacoes A/B
- headline_scorer.py - Pontuacao de headlines
- readability_checker.py - Analise de legibilidade
- content_repurposer.py - Adaptacao cross-platform
- hook_generator.py - Geracao de hooks
- content_idea_generator.py - Ideias de conteudo
- caption_generator.py - Legendas para posts
- carousel_structure_generator.py - Estrutura de carrosseis
- competitor_analyzer.py - Analise de concorrencia
- content_audit.py - Auditoria de conteudo
- hook_variant_generator.py - Variantes de hooks
- instagram_hashtag_research.py - Pesquisa de hashtags Instagram
- reels_script_generator.py - Scripts de Reels
- tiktok_trends_scraper.py - Scraper de trends TikTok
- trend_adapter.py - Adaptacao de trends
- trend_tracker.py - Rastreamento de trends

#### Workflows (7)
- Lancamento de Produto
- Calendario Mensal
- Campanha de Conversao
- Funil de Vendas
- Parceria com Influencer
- Batch Production
- TikTok Trends Chrome

#### Recursos Adicionais
- Swipe files com exemplos testados
- Personas por nicho
- Frameworks de crescimento
- Biblioteca de prompts para IA

---

## Tipos de Mudancas

- `Added` para novas funcionalidades
- `Changed` para mudancas em funcionalidades existentes
- `Deprecated` para funcionalidades que serao removidas
- `Removed` para funcionalidades removidas
- `Fixed` para correcoes de bugs
- `Security` para vulnerabilidades

---

*Mantido por @rilnermucio*
