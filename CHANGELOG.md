# Changelog

Todas as mudancas notaveis deste projeto serao documentadas neste arquivo.

O formato e baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

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
