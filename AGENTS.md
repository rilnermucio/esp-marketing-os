# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, Codex CLI, Cursor, Gemini CLI, etc.) when working with code in this repository.

> **Canonical source.** Edit this file directly. `CLAUDE.md` is a thin shim that imports this file via `@AGENTS.md` — Claude Code reads it on launch, Codex and other tooling-agnostic agents read this file directly. Don't duplicate content; everything goes here.

## O que é este repositório

Marketing OS é um **plugin do Claude Code** (`plugin.json` v6.0.0) que distribui 18 subagents nativos especializados em marketing digital, mais 25 slash commands, knowledge bases, voice clones e scripts Python. O conteúdo é majoritariamente PT-BR e otimizado para o mercado brasileiro.

Arquivos manifesto: `plugin.json` (raiz) e `.claude-plugin/marketplace.json` (listagem de marketplace). O entrypoint da skill é `skills/marketing-os/SKILL.md`.

## Comandos

```bash
# Test suite Tier 1 (estática, rápida — valida manifesto, SKILL.md, subagents, simlinks, separação workspace)
python -m pytest scripts/tests/ -v -m "not smoke"

# Rodar um único teste
python -m pytest scripts/tests/test_plugin_manifest.py -v
python -m pytest scripts/tests/test_subagents.py::test_subagent_files_exist -v

# Validar native agents em agents/ (YAML frontmatter, knowledge base refs)
python scripts/validate_agents.py
python scripts/validate_agents.py --strict   # falha em warnings também

# CLI unificado das ferramentas (29 scripts)
python scripts/mos.py seo analyze artigo.md "keyword"
python scripts/mos.py headlines score "Sua headline"
```

Não há `npm run lint` / `npm run build` — o repositório é Python + Markdown puro.

## Arquitetura (two-tier)

A arquitetura crítica de entender antes de mexer em qualquer agent:

- **Tier 1** — `agents/mos-*.md` (18 arquivos, ~250 linhas cada). System prompts enxutos com YAML frontmatter (`name`, `description`, `tools`, `model`, `color`, `hooks`). Carregados automaticamente pelo Claude Code quando a sessão abre. Contêm dispatch protocol, output schema e quality gates.
- **Tier 2** — `subagents/*-agent.md` (18 arquivos, ~3500 linhas cada). Knowledge base profunda: frameworks, cases, tabelas, exemplos. Lida sob demanda via `Read` pelos agents tier-1 quando precisam de profundidade.

Isso mantém contextos leves, carrega profundidade só quando precisa, e permite evoluir knowledge sem mexer no dispatch.

A skill em `skills/marketing-os/SKILL.md` é um **orquestrador** — ela mapeia briefings de usuário para `Agent(subagent_type: "mos-*")` calls. Os symlinks dentro de `skills/marketing-os/` (`assets`, `references`, `scripts`, `subagents`, `workflows`) apontam para os diretórios da raiz.

## Protocolo de dispatch (regra fundamental)

Para qualquer pedido de produção de marketing (copy, SEO, post, anúncio, vídeo, etc.), **NÃO execute inline**. Despache o subagent via `Agent(subagent_type: "mos-*", prompt: ...)`.

| Situação | Ação |
|----------|------|
| Pedido de produção (copy, post, artigo, anúncio) | Dispatch |
| Pergunta conceitual ("o que é AIDA?") | Inline |
| Briefing amplo ("campanha completa") | Dispatch paralelo (single message, múltiplas Agent calls) |
| Dependência real entre etapas | Dispatch sequencial (research → seo → copy) |
| Pergunta sobre o próprio sistema | Inline |

Mapeamento completo briefing → agent em `skills/marketing-os/SKILL.md` (seção "Mapa de Dispatch").

## Quality Gates Globais (aplicar SEMPRE antes de entregar)

Mesmo que o subagent rode seus próprios gates, valide antes da entrega final:

| Item | Ação |
|------|------|
| `—` (travessão longo) | substituir por `.` `,` `:` ou quebrar frase |
| Palavra "brutal" | trocar por: intenso, forte, pesado, impactante, poderoso |
| PALAVRAS EM CAPS | reescrever em minúscula |
| Aspas em roteiros/falas | escrever direto |
| Mais de 2 emojis | reduzir para 0-1 |
| Texto sem acentos PT-BR | sempre acentuar corretamente |

Citação de pessoas/estatísticas/cases requer fact-check via WebSearch antes de publicar (CONFIRMADO / PROVÁVEL / NÃO USAR).

Conteúdos de redes sociais (Reels, posts, carrosséis, stories) **devem** incluir sugestão de enquete.

## Separação workspace pessoal vs. plugin distribuível

- `workspace/` — gitignored. Conteúdo pessoal (drafts, outputs, brand, research, landing-pages, media). Nunca commitar.
- `assets/`, `references/`, `subagents/`, `commands/`, `workflows/`, `skills/` — versionados, distribuídos com o plugin.
- O teste `scripts/tests/test_workspace_separation.py` falha se conteúdo pessoal vazar para paths versionados.

## Ferramentas Python relevantes

29 scripts em `scripts/` (CLI unificado em `scripts/mos.py`). Os agents Tier 1 com acesso a `Bash` invocam-nos para tarefas determinísticas: `seo_analyzer.py`, `hashtag_generator.py`, `hook_generator.py`, `reels_script_generator.py`, `carousel_structure_generator.py`, `caption_generator.py`, `trend_tracker.py`, `quality_gate.py`, `headline_scorer.py`, `competitor_analyzer.py`, etc.

Hook de quality gate: `scripts/hooks/quality_gate_hook.py` é invocado via `PreToolUse` matcher `Write|Edit|MultiEdit` em vários agents Tier 1 (ver frontmatter `hooks` em `agents/mos-*.md`).

## Voice clones (`assets/clones/`)

35 perfis detalhados (Halbert, Hopkins, Kennedy, Ogilvy, Schwartz, Sugarman, Hormozi, GaryVee, MrBeast, Brunson, Cialdini, Codie Sanchez, Abdaal, Conrado, Joel Jota, etc.). Cada clone tem `profile.md`, `frameworks.md`, `voice.md`, `examples.md`. Usados por `/criar-clone` e referenciados pelo `mos-copy` quando o briefing pede estilo de um copywriter específico.

`/criar-meu-clone` é o caso especial: usa amostras locais do usuário em `workspace/` (não copywriters externos).

## Plugin distribution gotchas (aprendidos no debug de v6.1.0–v6.1.6)

Antes de mexer em `.claude-plugin/plugin.json` ou `.claude-plugin/marketplace.json`, leia. Cada item abaixo quebrou install via marketplace numa versão específica e exigiu um patch.

| Item | Regra | Quem reclama |
|---|---|---|
| Localização do `plugin.json` | **MUST** ser `.claude-plugin/plugin.json`. Raiz funciona no Claude Code (parser frouxo) mas falha no Claude Desktop com "Plugin validation failed" | Desktop |
| `marketplace.json` source relativo | **MUST** começar com `./`. Bare `"."` é rejeitado como "source type your Claude Code version does not support" | Code + Desktop |
| Field `author` em `plugin.json` | Object `{"name": "..."}`, não string. Schema validator rejeita string com "expected object, received string" | Desktop |
| Field `category` em `plugin.json` | Singular `"category": "marketing"`, não plural `"categories": [...]`. Plural é input inválido | Desktop |
| Field `skills` em `plugin.json` | **Não declarar** se usa folder default `skills/`. O explicit `["skills/marketing-os"]` é rejeitado como "Invalid input"; default discovery cobre | Desktop |
| `marketplace.json` metadata block | Use top-level `description` e `version` (NÃO `metadata.{description,version}`). Metadata block é só backward-compat e Desktop pode rejeitar | Desktop |
| Hook command em agent frontmatter | **MUST** usar `${CLAUDE_PLUGIN_ROOT}/scripts/hooks/...`. Caminho relativo `scripts/hooks/...` falha em qualquer CWD ≠ raiz do plugin (CWD do hook é do user, não do plugin install dir) | Code + Desktop em runtime |
| Marketplace name bug | Anthropic cacheia state por nome de marketplace server-side. Se seu marketplace teve syncs broken, rename pra bypass cache (ex: `marketing-os-marketplace` → `mos-marketplace`) | Desktop |
| Reserved names | `claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`, `anthropic-marketplace`, `anthropic-plugins`, `agent-skills` — não usar | Validator |
| kebab-case strict | Plugin/marketplace `name` deve ser kebab-case. Outras formas funcionam no Code mas Claude.ai sync rejeita | Sync layer |

**Workflow recomendado pra mudar manifest:**

1. Edita `.claude-plugin/plugin.json` ou `.claude-plugin/marketplace.json`
2. `claude plugin validate .` (passa? bom)
3. Bump versão (campo `version` em ambos os manifests)
4. Update `CHANGELOG.md`
5. Commit + tag `vX.Y.Z` + push
6. **Teste real de install:** rode `/plugin install marketing-os@mos-marketplace` num projeto novo. `claude plugin validate` é necessário mas não suficiente.

**Quando o install falha sem mensagem clara:**

`log show --predicate 'process == "Claude" OR process == "Claude Helper"' --info --debug --last 10m | grep -iE "marketplace|github|git|fetch|fail|error|sync|plugin"` no Terminal pra extrair o erro real do Console.app.

## Convenções de mudança em agents

Ao editar um Tier 1 agent (`agents/mos-*.md`):
1. Não inche o system prompt — knowledge profunda vai no Tier 2 (`subagents/*-agent.md`).
2. Mantenha YAML frontmatter válido (`validate_agents.py` valida).
3. Se referenciar uma knowledge base, garanta que `subagents/<correspondente>.md` existe.
4. Filename **deve** bater com o campo `name` do frontmatter.

Ao editar Tier 2 (`subagents/*-agent.md`): edição livre de profundidade. O Tier 1 lê sob demanda.
