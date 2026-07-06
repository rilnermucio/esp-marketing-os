# Marketing OS

> Plugin Claude Code e Codex com **18 especialistas** em marketing digital + 38 slash commands Claude + 34 voice clones de copywriters lendários.

[![Version](https://img.shields.io/badge/version-6.9.0-blue.svg)](./CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

## O que é

Marketing OS é um plugin para o [Claude Code](https://www.anthropic.com/claude-code) e para o Codex que orquestra 18 especialistas nativos em domínios distintos do marketing digital. O plugin reivindica território explícito sobre briefings de marketing. Quando você pede "cria página de aplicação" ou "monta um webinar", ele roteia os especialistas corretos em paralelo, com camada estratégica antes de qualquer execução técnica.

**34 dos 38 slash commands** dispatcham subagents `mos-*`. Os 4 que não dispatcham são intencionais: `/publicar-notion` (utility do Notion MCP), `/campanha` (índice dos 6 sub-commands de preset), `/projeto` (orquestrador de workflow com dispatch dinâmico) e `/datas-sazonais` (utilitário de dados do calendário sazonal BR). Use `/mo` pra briefing aberto se não souber qual command escolher. **Conteúdo PT-BR otimizado para o mercado brasileiro.**

## Instalação

### Claude Code via marketplace

No Claude Code (CLI ou Desktop):

```
/plugin marketplace add rilnermucio/esp-marketing-os
/plugin install marketing-os@mos-marketplace
```

Auto-update fica ligado por padrão. Cada `git push` no repo vira atualização automática no startup da próxima sessão.

### Codex via marketplace GitHub

Para instalar no Codex a partir deste repositório:

```bash
codex plugin marketplace add rilnermucio/esp-marketing-os --ref main
codex plugin add marketing-os@marketing-os-marketplace
```

Para uma versão fixa, troque `main` pela tag da release:

```bash
codex plugin marketplace add rilnermucio/esp-marketing-os --ref v6.8.0
codex plugin add marketing-os@marketing-os-marketplace
```

No Codex app, depois de adicionar o marketplace, abra Plugins, selecione **Marketing OS** como fonte e instale o plugin `Marketing OS`.

### Via clone local (desenvolvimento)

```bash
git clone https://github.com/rilnermucio/esp-marketing-os.git "Marketing OS"
cd "Marketing OS"

# Deps Python pra rodar testes e validações
pip install -r requirements.txt

# Validar native agents
python scripts/validate_agents.py

# Tier 1 test suite
python -m pytest scripts/tests/ -v -m "not smoke"

# Carrega no Claude Code via --plugin-dir
claude --plugin-dir .
```

### Workspace pessoal (gitignored)

Crie sua área de trabalho local, não distribuída pelo plugin:

```bash
mkdir -p workspace/{drafts,outputs,brand,research,landing-pages,media}
```

## Os 18 subagentes nativos

Invocados pelo orquestrador (skill `/marketing-os`) ou diretamente via `@<agente>`:

| Agente | Domínio | Memory |
|---|---|---|
| `@mos-copy` | Copywriting persuasivo (headlines, CTAs, sales letters) | sim |
| `@mos-seo` | Otimização de busca (keywords, on-page, E-E-A-T, AI-SEO) | sim |
| `@mos-social` | Posts e estratégia em redes sociais (cross-platform) | sim |
| `@mos-video` | Roteiros (YouTube, Reels, TikTok, VSL, Shorts) | não |
| `@mos-audio` | Podcasts, audiobooks, spots, sound design | não |
| `@mos-design` | Direção visual, paletas, tipografia, design specs | sim |
| `@mos-ai-tools` | Prompts pra Midjourney, Flux, Runway, Sora, etc. | não |
| `@mos-analytics` | Métricas, KPIs, dashboards, GA4 | sim |
| `@mos-email` | Email marketing (welcome, nurture, vendas, automação) | sim |
| `@mos-ads` | Anúncios pagos (Meta, Google, TikTok, LinkedIn) | sim |
| `@mos-research` | Trend spotting, audience research, validação | sim |
| `@mos-brand` | Identidade de marca, arquétipos, manifesto | sim |
| `@mos-storytelling` | Narrativa aplicada (hero's journey, StoryBrand) | não |
| `@mos-funnel` | Funis de conversão, jornada (TOFU/MOFU/BOFU) | sim |
| `@mos-growth` | Growth hacking, AARRR, retention | não |
| `@mos-launch` | Lançamentos (PLF, semente, relâmpago, perpétuo) | sim |
| `@mos-infoproduct` | Cursos, memberships, mentorias, ebooks | sim |
| `@mos-ab-testing` | A/B/MVT, ICE prioritization, significância estatística | não |

**Memory opt-in (12 agents).** `mos-ads`, `mos-analytics`, `mos-brand`, `mos-copy`, `mos-design`, `mos-email`, `mos-funnel`, `mos-infoproduct`, `mos-launch`, `mos-research`, `mos-seo` e `mos-social` podem persistir aprendizados entre sessões em `.claude/agent-memory/mos-*/MEMORY.md`. Para ativar, rode o bootstrap uma vez na raiz do projeto:

```bash
python3 scripts/init_agent_memory.py
```

Sem o bootstrap os agents seguem funcionando normalmente, só não persistem patterns. Modos `--check` (read-only) e `--force` (sobrescreve) disponíveis.

## Workflows orquestrados

10 padrões de orquestração documentados em [`skills/marketing-os/SKILL.md`](./skills/marketing-os/SKILL.md):

| # | Workflow | Agents disparados |
|---|---|---|
| 1 | Dispatch simples | 1 agent |
| 2 | Dispatch paralelo | múltiplos agents independentes |
| 3 | Dispatch sequencial | agents com dependência (ex: research → seo → copy) |
| 4 | Content pipeline | research+brand → seo/copy/social + design |
| 5 | **Página de aplicação / landing / vendas (BOFU)** | mos-funnel + mos-copy + mos-design, opcionalmente handoff a `frontend-design` |
| 6 | **Webinar (live ou perpetual)** | launch + funnel + video → copy + email |
| 7 | **Lançamento de infoproduto** | research → infoproduct + launch + funnel → copy + email + ads |
| 8 | **Carrossel completo** | social + copy + design (+ ai-tools) |
| 9 | **VSL completa** | storytelling + copy + video |
| 10 | **Análise de concorrente + clone** | research + brand → copy (voice clone) |

Ver SKILL.md pra detalhes de cada workflow e "por que essa ordem importa". Tier 2 cobre profundidade: `subagents/funnel-agent.md` documenta webinar funnel, página de aplicação BOFU e anti-avatar (workflows #5, #6, #9); `subagents/copy-agent.md` cobre big idea e value stack.

## Slash commands rápidos

38 commands em `commands/` cobrindo workflows comuns. **34 deles dispatcham subagents `mos-*`** seguindo os workflows da tabela acima (os 4 sem dispatch são utilities intencionais: `/publicar-notion`, `/campanha` índice, `/projeto` e `/datas-sazonais`). Quando você invoca direto (`/criar-carrossel`), segue lógica do command file. Quando pede em linguagem natural ("cria carrossel sobre X"), o orquestrador da skill dispatcha conforme tabela.

| Categoria | Commands |
|---|---|
| Meta-orquestrador | `/mo` (briefing aberto, roteia pro command apropriado) |
| Conteúdo social | `/criar-post`, `/criar-carrossel`, `/criar-calendario` |
| Copy | `/otimizar-copy` (diagnóstico + score + reescrita de copy existente) |
| Vídeo/áudio | `/criar-video`, `/criar-podcast`, `/narrar-roteiro` |
| Páginas/funis | `/criar-landing-page`, `/criar-funil`, `/criar-webinar` |
| Email | `/criar-email`, `/criar-sequencia` |
| Ads | `/criar-anuncio`, `/publicar-anuncio` |
| Infoproduto | `/criar-infoproduto` |
| Voice clones | `/criar-clone` (expert externo), `/criar-meu-clone` (suas amostras) |
| Análise | `/analisar-concorrencia`, `/analisar-video`, `/clonar-estrategia`, `/auditoria`, `/auditoria-pro` |
| Visual | `/criar-brief-design`, `/gerar-imagem`, `/capturar-tela` |
| Operação | `/batch`, `/criar-artigo`, `/publicar-notion`, `/projeto`, `/datas-sazonais` |
| Campanhas (presets) | `/campanha` (índice), `/campanha-lancamento`, `/campanha-prospeccao`, `/campanha-retencao`, `/campanha-autoridade`, `/campanha-growth`, `/campanha-black-friday` |

## Estrutura

```
Marketing OS/
├── .claude-plugin/         # plugin.json + marketplace.json
├── .codex-plugin/          # plugin.json para desenvolvimento local no Codex
├── .agents/plugins/        # marketplace Codex repo-scoped
├── plugins/marketing-os/   # pacote Codex distribuível, gerado por script
├── agents/                 # 18 native subagents (mos-*.md)
├── skills/marketing-os/    # Skill entrypoint (SKILL.md = orquestrador)
├── subagents/              # Tier 2 knowledge bases (~3500 linhas cada)
├── commands/               # 38 slash commands (34 com dispatch + /publicar-notion + /campanha índice + /projeto + /datas-sazonais)
├── workflows/              # 10 workflows end-to-end documentados
├── assets/                 # Frameworks, personas, prompts, swipe files,
│   ├── clones/             #   templates, 34 voice clones (+ design-dna)
│   ├── frameworks/
│   ├── personas/
│   ├── prompts/
│   ├── swipe-files/
│   └── templates/
├── references/             # Guias técnicos por domínio
├── scripts/                # ferramentas Python, validações e Tier 1 tests
│   ├── hooks/              # Quality gate hook (PreToolUse)
│   └── tests/              # Suite pytest
├── docs/                   # Documentação técnica
│   ├── GETTING-STARTED.md  # Começo rápido
│   ├── TROUBLESHOOTING.md  # Bugs comuns
│   └── ARCHITECTURE.md     # Arquitetura two-tier
└── workspace/              # Área pessoal (gitignored)
```

## Voice clones (34 perfis em `assets/clones/`)

Copywriters/marketers lendários referenciados pelo `mos-copy` quando o briefing pede estilo específico:

Halbert, Hopkins, Kennedy, Ogilvy, Schwartz, Sugarman, Caples, Cialdini, Brunson, Hormozi, Leila Hormozi, GaryVee, MrBeast, Codie Sanchez, Abdaal, Abraham, Joel Jota, Conrado, Mel Robbins, Patel, Provost, Rachitsky, Suby, Welsh, Cole, Collier, Ellis, Ezra Firestone, Flavio Augusto, Gadzhi, Godin, Howell, Chen, Miller.

Cada um com `profile.md`, `frameworks.md`, `voice.md`, `examples.md`.

## Desenvolvimento

Ver [`AGENTS.md`](./AGENTS.md) pra guia completo de desenvolvimento (arquitetura, dispatch protocol, plugin distribution gotchas, quality gates). `CLAUDE.md` é shim que importa AGENTS.md, Claude Code lê automaticamente.

```bash
# Tier 1 test suite (estática, rápida, sem Claude Code login)
python -m pytest scripts/tests/ -v -m "not smoke"

# Validar native agents (frontmatter, knowledge base refs)
python scripts/validate_agents.py
python scripts/validate_agents.py --strict   # falha em warnings também

# Validar plugin manifest
claude plugin validate .

# Gerar e validar pacote Codex oficial
python scripts/build_codex_plugin.py
python scripts/build_codex_plugin.py --check
python scripts/validate_codex_plugin.py plugins/marketing-os

# Bootstrap memory (opt-in, 10 agents)
python3 scripts/init_agent_memory.py

# CLI unificado das ferramentas
python scripts/mos.py --help
```

CI rodando em `.github/workflows/tests.yml`: suite Tier 1, cobertura ≥50%, validação do pacote Codex e job `validate-agents` em modo `--strict` em todo PR/push (pega regressão de frontmatter, knowledge refs quebrados, name collisions). Estado atual: **18/18 agents clean** no validator.

## Documentação adicional

- **[docs/GETTING-STARTED.md](./docs/GETTING-STARTED.md)**: primeiros passos com 5 exemplos de briefings
- **[docs/TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md)**: problemas comuns de install/configuração e como resolver
- **[docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)**: arquitetura two-tier (system prompts enxutos + knowledge bases profundas)
- **[CHANGELOG.md](./CHANGELOG.md)**: histórico completo de releases
- **[AGENTS.md](./AGENTS.md)**: guia canônico pra contributors e agentes de IA

## Licença

MIT, ver [LICENSE](./LICENSE).
