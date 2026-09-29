# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, Codex CLI, Cursor, Gemini CLI, etc.) when working with code in this repository.

> **Canonical source.** Edit this file directly. `CLAUDE.md` is a thin shim that imports this file via `@AGENTS.md` — Claude Code reads it on launch, Codex and other tooling-agnostic agents read this file directly. Don't duplicate content; everything goes here.

## O que é este repositório

Marketing OS é um **plugin do ChatGPT Work, Claude Code e Codex**. A distribuição Claude usa `.claude-plugin/`; o pacote universal para ChatGPT Work e Codex usa `.codex-plugin/`. O sistema distribui 21 especialistas em marketing digital, mais 51 slash commands no Claude Code, knowledge bases, voice clones e scripts Python. O conteúdo é majoritariamente PT-BR e otimizado para o mercado brasileiro.

Arquivos manifesto: `.claude-plugin/plugin.json` e `.claude-plugin/marketplace.json` (listagem de marketplace). O entrypoint da skill é `skills/marketing-os/SKILL.md`.

## Comandos

```bash
# Test suite Tier 1 (estática, rápida — valida manifesto, SKILL.md, subagents, simlinks, separação workspace)
python -m pytest scripts/tests/ -v -m "not smoke"

# Smoke de instalação real (Claude Code instalado, sessão fora do repo, agents em Haiku; ~2 min)
# Obrigatório ao mexer em hooks, caminhos, nomes de agent, memória ou manifests (ADR-0005)
MOS_SMOKE=1 python -m pytest scripts/tests/test_install_smoke.py -m smoke -v

# Rodar um único teste
python -m pytest scripts/tests/test_plugin_manifest.py -v
python -m pytest scripts/tests/test_subagents.py::test_subagent_files_exist -v

# Validar native agents em agents/ (YAML frontmatter, knowledge base refs)
python scripts/validate_agents.py
python scripts/validate_agents.py --strict   # falha em warnings também

# Bootstrap memory opt-in (cria .claude/agent-memory/marketing-os-mos-*/MEMORY.md no projeto atual)
python3 scripts/init_agent_memory.py            # todos os agents com memory: project
python3 scripts/init_agent_memory.py mos-copy   # apenas um agent

# CLI unificado das ferramentas (mos.py expõe um subconjunto dos scripts)
python scripts/mos.py seo analyze artigo.md "keyword"
python scripts/mos.py headlines score "Sua headline"
```

Não há `npm run lint` / `npm run build` — o repositório é Python + Markdown puro.

## Camada de engenharia de IA (`docs/ai-engineering/`)

Processo canônico de manutenção do plugin, para humanos e agentes de IA. Antes de qualquer rodada não-trivial, leia `docs/ai-engineering/OPERATING-MODEL.md` (como trabalhar, quando auditar, quando pedir aprovação). Regras que valem sempre:

1. **Medir antes de refatorar**: refactor amplo só com rubrica/eval existente (`docs/ai-engineering/RUBRICS.md`, `EVALS-STRATEGY.md`).
2. **Toda rodada gera worklog** em `docs/ai-engineering/worklogs/` (template em `IMPLEMENTATION-LOG.md`).
3. **Decisão estrutural vira ADR** em `docs/ai-engineering/adr/`; bug/eval referencia IDs de `FAILURE-TAXONOMY.md`.
4. **Roteamento tem gabarito**: mexeu em SKILL.md, descriptions ou commands, rode `python -m pytest scripts/tests/test_routing_evals.py` e revise `ROUTING-EVALS.md`.

## Arquitetura (two-tier)

A arquitetura crítica de entender antes de mexer em qualquer agent:

- **Tier 1** — `agents/mos-*.md` (21 arquivos, ~250 linhas cada). System prompts enxutos com YAML frontmatter (`name`, `description`, `tools`, `model`, `color`, `memory`). Hooks não entram no frontmatter: a plataforma ignora esse campo em agent de plugin (ADR-0005). Carregados automaticamente pelo Claude Code quando a sessão abre. Contêm dispatch protocol, output schema e quality gates.
- **Tier 2** — `subagents/*-agent.md` (21 arquivos, profundidade variável de ~400 a ~6,5 mil linhas). Knowledge base profunda: frameworks, cases, tabelas, exemplos. Lida sob demanda via `Read` pelos agents tier-1 quando precisam de profundidade. Os mais densos hoje: `copy-agent.md` (~5,3 mil linhas, inclui PARTE II-C Big Idea + Value Stack) e `funnel-agent.md` (~3,5 mil linhas, inclui Webinar Funnel 3.4, Página de Aplicação BOFU 3.5 e Anti-Avatar 4.6).

Isso mantém contextos leves, carrega profundidade só quando precisa, e permite evoluir knowledge sem mexer no dispatch.

Todos os 21 agents declaram `memory: project` no frontmatter (completado no nivelamento de jul/2026). Ver "Memory opt-in (per-projeto)" abaixo.

A skill em `skills/marketing-os/SKILL.md` é um **orquestrador**. Ela usa `Agent(subagent_type: "marketing-os:mos-*")` no Claude Code e mapeia o mesmo dispatch para leitura Tier 1/Tier 2 no ChatGPT Work e no Codex. Os symlinks dentro de `skills/marketing-os/` (`assets`, `references`, `scripts`, `subagents`, `workflows`) apontam para os diretórios da raiz.

## Protocolo de dispatch (regra fundamental)

Para qualquer pedido de produção de marketing (copy, SEO, post, anúncio, vídeo, etc.), **NÃO execute inline**. Despache o subagent via `Agent(subagent_type: "marketing-os:mos-*", prompt: ...)`. Instalado, o agent de plugin só responde pelo nome qualificado; o nome curto falha com "Agent type not found".

| Situação | Ação |
|----------|------|
| Pedido de produção (copy, post, artigo, anúncio) | Dispatch |
| Pergunta conceitual ("o que é AIDA?") | Inline |
| Briefing amplo ("campanha completa") | Dispatch paralelo (single message, múltiplas Agent calls) |
| Dependência real entre etapas | Dispatch sequencial (research → seo → copy) |
| Pergunta sobre o próprio sistema | Inline |

Mapeamento completo briefing → agent em `skills/marketing-os/SKILL.md` (seção "Mapa de Dispatch").

Command que despacha um único agent, com todo o input vindo do pedido e dos arquivos do projeto e sem aprovação no meio, pode usar `context: fork` com `agent: marketing-os:mos-<agent>` e `background: false` no frontmatter. Aí a própria plataforma roda o corpo do command dentro do agent, sem depender do orquestrador. O agent em fork não vê a conversa, então pedido incompleto devolve perguntas. Piloto: `/gerar-imagem`. Critérios e contratos na ADR-0007.

Hoje 47 dos 51 slash commands em `commands/` dispatcham subagents. Os 2 commands premium na v6.8.0+ são `/auditoria` (multi-modal básico, ver `docs/AUDIT-CONFIG.md`) e `/auditoria-pro` (landing agency-grade com radar/screenshots/roadmap, ver `docs/AUDITORIA-PRO.md`). Os 4 sem dispatch são intencionais: `/publicar-notion` (utility do Notion MCP), `/campanha` (índice dos 6 sub-commands `/campanha-{preset}`), `/projeto` (workflow orchestrator com dispatch dinâmico por etapa) e `/datas-sazonais` (utilitário de dados do calendário sazonal BR, ver `scripts/seasonal_calendar_br.py`). Existe ainda `/mo` (meta-orquestrador) que recebe briefing aberto e roteia automaticamente. O teste `scripts/tests/test_commands_dispatch.py` trava regressão de cobertura: se você adicionar um command novo de produção, ele precisa dispatchar ou o teste falha.

## Quality Gates Globais (aplicar SEMPRE antes de entregar)

Mesmo que o subagent rode seus próprios gates, valide antes da entrega final:

| Item | Ação |
|------|------|
| `—` (travessão longo) | substituir por `.` `,` `:` ou quebrar frase |
| Palavra "brutal" | trocar por: intenso, forte, pesado, impactante, poderoso |
| Antítese negação→afirmação ("Não é X / É Y", "Não faça X / Faça Y") | reescrever afirmando direto, sem o paralelo |
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

Os scripts Python em `scripts/` (CLI unificado em `scripts/mos.py`) são invocados pelos agents Tier 1 com acesso a `Bash` para tarefas determinísticas: `seo_analyzer.py`, `hashtag_generator.py`, `hook_generator.py`, `reels_script_generator.py`, `carousel_structure_generator.py`, `caption_generator.py`, `trend_tracker.py`, `quality_gate.py`, `headline_scorer.py`, `competitor_analyzer.py`, etc.

Hook de quality gate: `scripts/hooks/quality_gate_hook.py` é registrado no nível do plugin, em `hooks/hooks.json`: `PreToolUse` (`Write|Edit|MultiEdit`) e `SubagentStop`. Ele só age em eventos de agents do Marketing OS (`marketing-os:mos-*`, ou `mos-*` em instalação local); escrita da sessão principal do usuário passa direto. O núcleo puro `evaluate_event` atende as duas superfícies e limita a correção final a uma tentativa para evitar loop. Bloqueio sai em stderr com exit 2; avisos saem em JSON `additionalContext`, o único canal de exit 0 que o modelo vê. `MOS_HOOK_LOG=<arquivo>` registra cada evento para diagnóstico.

Caminhos em runtime (ADR-0005): instalado, o plugin roda com a sessão no projeto do usuário. Agents, commands e SKILL.md referenciam recursos do plugin como `${CLAUDE_PLUGIN_ROOT}/subagents/...` (comandos de terminal com o caminho entre aspas), e scripts gravam estado do usuário em `workspace/` do diretório da sessão (`scripts/workspace_paths.py`). O guard `scripts/tests/test_plugin_runtime_paths.py` trava a regressão, e o build do pacote universal desfaz essas adaptações para ChatGPT Work e Codex.

**Apify (opt-in)**: 6 scripts opcionais (`apify_client.py` + 5 scrapers: `apify_serp.py`, `apify_instagram.py`, `apify_meta_ads.py`, `apify_tiktok.py`, `apify_youtube.py`) habilitam scraping estruturado de SERP do Google, Instagram, Meta Ad Library, TikTok e YouTube. Usados pelos agents `mos-seo`, `mos-research`, `mos-ads` e `mos-video` quando a variável `APIFY_TOKEN` está disponível. Sem token, comportamento idêntico ao anterior (fallback automático para `WebSearch`). Setup, custo estimado, mapeamento Actor↔agent e FAQ em `docs/APIFY-INTEGRATION.md`.

## Voice clones (`assets/clones/`)

34 perfis de copywriters (Halbert, Hopkins, Kennedy, Ogilvy, Schwartz, Sugarman, Hormozi, GaryVee, MrBeast, Brunson, Cialdini, Codie Sanchez, Abdaal, Conrado, Joel Jota, etc.). Cada clone tem `profile.md`, `frameworks.md`, `voice.md`, `examples.md`. Usados por `/criar-clone` e referenciados pelo `mos-copy` quando o briefing pede estilo de um copywriter específico. O diretório `assets/clones/design/` é a exceção: guarda o `design-dna-system.md` (DNA visual usado pelo `mos-design`), não um perfil de voz.

`/criar-meu-clone` é o caso especial: usa amostras locais do usuário em `workspace/` (não copywriters externos).

## Memory opt-in (per-projeto)

Agents com `memory: project` no frontmatter persistem aprendizado por projeto em `.claude/agent-memory/marketing-os-mos-*/MEMORY.md`. Esse é o diretório nativo que o Claude Code usa para agent de plugin (`<plugin>-<agent>`): a plataforma injeta o início do `MEMORY.md` no contexto do agent. Até 2026-09 o plugin usava `mos-*/`, que a plataforma não lê em agent de plugin; `init_agent_memory.py` e `memory_writer.py` migram esse legado sem perda (ADR-0006). O bootstrap continua explícito e idempotente: `python3 scripts/init_agent_memory.py` cria os arquivos e migra o legado.

Regras pra mexer:

1. Pra adicionar memory a um agent novo: declarar `memory: project` no frontmatter, incluir o agent em `AGENTS_WITH_MEMORY` (`scripts/init_agent_memory.py`) e referenciar `.claude/agent-memory/marketing-os-<nome-do-agent>/MEMORY.md` no system prompt. Aprendizado se grava só via `memory_writer.py` (schema e limites anti-poluição).
2. Não escrever no diretório de memory dentro do plugin install dir. É sempre relativo ao CWD do projeto do usuário.
3. `init_agent_memory.py` é idempotente: roda quantas vezes quiser, não sobrescreve conteúdo existente.

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
| Hook em frontmatter de agent de plugin | **Ignorado pela plataforma** (junto com `mcpServers` e `permissionMode`). Registre hooks em `hooks/hooks.json` com `"${CLAUDE_PLUGIN_ROOT}/..."` entre aspas | Code + Desktop em runtime |
| Nome de agent de plugin | Chega qualificado: `marketing-os:mos-copy` no dispatch (`subagent_type`) e no `agent_type` dos hooks. Nome curto falha com "Agent type not found" | Code + Desktop em runtime |
| Caminho relativo a recurso do plugin | Só resolve com a sessão dentro do repo. Instalado, use `${CLAUDE_PLUGIN_ROOT}/...` (substituído em agents, commands e skills) | Code + Desktop em runtime |
| Marketplace de conta claude.ai | Marketplace adicionado na conta sincroniza para `~/.claude/plugins/synced/` e pode congelar; o app desktop carrega essa cópia. Diagnóstico: `python3 scripts/mos.py install doctor` | Desktop |
| Memória nativa de agent de plugin | Diretório `.claude/agent-memory/<plugin>-<agent>/` (ex: `marketing-os-mos-copy`), não o nome curto | Code + Desktop em runtime |
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

CI tem job `validate-agents` que roda `python scripts/validate_agents.py --strict` em todo PR/push e bloqueia merge em frontmatter inválido, name collision ou knowledge ref quebrado. Pega regressão antes de chegar em release.

### Distribuição universal ChatGPT Work e Codex

O pacote em `.codex-plugin/plugin.json` é `skills-only`, conforme ADR-0004. Regras:

1. `description` e `interface.longDescription` citam ChatGPT Work e Codex.
2. `interface.shortDescription` tem no máximo 30 caracteres.
3. `interface.category` e a categoria do marketplace usam um valor oficial do diretório universal. Para este plugin: `Business & Operations`.
4. `interface.defaultPrompt` contém de 1 a 3 prompts, cada um em uma linha e com no máximo 128 caracteres.
5. O manifesto não declara `apps` nem `mcpServers` enquanto a arquitetura continuar skills-only.
6. Mudanças em `skills/`, scripts ou metadados exigem rebuild, `--check`, validador do pacote e uma conversa nova no ChatGPT Work e no Codex.
7. Antes de copiar o pacote para um marketplace pessoal, execute `test ! -L <destino>` e compare o `realpath` do destino com `pwd -P`. O destino precisa ser uma pasta física fora do repositório. Não use `rsync --delete` enquanto esse preflight não estiver comprovado (F-CODEX-04).

O guard canônico dessas regras está em `scripts/validate_codex_plugin.py` e `scripts/tests/test_chatgpt_distribution.py`. O nome histórico do script foi preservado para não quebrar CI e documentação externa.

**Quando o install falha sem mensagem clara:**

`log show --predicate 'process == "Claude" OR process == "Claude Helper"' --info --debug --last 10m | grep -iE "marketplace|github|git|fetch|fail|error|sync|plugin"` no Terminal pra extrair o erro real do Console.app.

## Convenções de mudança em agents

Ao editar um Tier 1 agent (`agents/mos-*.md`):
1. Não inche o system prompt — knowledge profunda vai no Tier 2 (`subagents/*-agent.md`).
2. Mantenha YAML frontmatter válido (`validate_agents.py` valida).
3. Se referenciar uma knowledge base, garanta que `subagents/<correspondente>.md` existe.
4. Filename **deve** bater com o campo `name` do frontmatter.

Ao editar Tier 2 (`subagents/*-agent.md`): edição livre de profundidade. O Tier 1 lê sob demanda.
