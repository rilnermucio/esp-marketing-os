# Marketing OS

> Plugin Claude Code com **18 subagentes especializados** em marketing digital.

[![Version](https://img.shields.io/badge/version-6.0.0-blue.svg)](./CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

## O que é

Marketing OS é um plugin para o [Claude Code](https://www.anthropic.com/claude-code) que habilita 18 subagentes nativos especializados em domínios distintos do marketing digital — copy, SEO, social, vídeo, áudio, design, ads, analytics, email, brand, storytelling, funnel, growth, launch, AI tools, infoproduct builder, AB testing e research.

Cada agente tem acesso a uma knowledge base própria (`subagents/*.md`), uma biblioteca de assets (frameworks, personas, prompts, swipe files, templates, voice clones de copywriters lendários) e referências técnicas curadas (`references/`).

## Instalação

### Como plugin do Claude Code

```bash
# Clone o repositório
git clone https://github.com/rilnermucio/Marketing-OS.git "Marketing OS"
cd "Marketing OS"

# Instale as deps Python (apenas pra rodar testes/validações)
pip install -r requirements.txt

# Configure o plugin no Claude Code (via plugin.json deste repo)
# Detalhes: https://docs.anthropic.com/claude-code/plugins
```

### Workspace pessoal

Crie sua área pessoal de conteúdo (gitignored, não distribuída):

```bash
mkdir -p workspace/{drafts,outputs,brand,research,landing-pages,media}
```

## Os 18 agentes

Invoque qualquer um via `@<agente>` no Claude Code:

| Agente | Domínio |
|---|---|
| `@mos-copy` | Copywriting persuasivo (headlines, body copy, CTAs) |
| `@mos-seo` | Otimização de busca (keywords, meta, on-page, conteúdo) |
| `@mos-social` | Conteúdo para redes sociais (posts, reels, threads) |
| `@mos-video` | Roteiros e produção audiovisual (YouTube, Reels, TikTok) |
| `@mos-audio` | Podcasts, audiobooks, sound design |
| `@mos-design` | Direção visual, mockups, design specs |
| `@mos-ai-tools` | Avaliação e uso de ferramentas de IA generativa |
| `@mos-analytics` | Métricas, dashboards, KPIs, atribuição |
| `@mos-email` | Email marketing (welcome series, broadcasts, automação) |
| `@mos-ads` | Anúncios pagos (Meta, Google, LinkedIn, TikTok) |
| `@mos-research` | Pesquisa de mercado, audiência, concorrência |
| `@mos-brand` | Identidade de marca, posicionamento, voz |
| `@mos-storytelling` | Narrativa, hero's journey, frameworks de história |
| `@mos-funnel` | Funis de conversão, jornada do cliente |
| `@mos-growth` | Growth hacking, experimentação, retention |
| `@mos-launch` | Lançamentos (PLF, escassez, urgência) |
| `@mos-infoproduct` | Estrutura e curadoria de infoprodutos |
| `@mos-ab-testing` | A/B testing, multivariate, análise estatística |

## Slash commands

Comandos rápidos pra fluxos comuns (`/comando`):

- `/criar-post`, `/criar-carrossel`, `/criar-video`, `/criar-podcast`
- `/criar-anuncio`, `/criar-email`, `/criar-sequencia`, `/criar-funil`
- `/criar-artigo`, `/criar-landing-page`, `/criar-webinar`, `/criar-infoproduto`
- `/criar-clone` (clone de expert externo via web research)
- `/criar-meu-clone` (clone da SUA voz via amostras locais)
- `/analisar-concorrencia`, `/analisar-video`, `/clonar-estrategia`
- `/criar-brief-design`, `/criar-calendario`, `/gerar-imagem`, `/capturar-tela`
- `/publicar-anuncio`, `/publicar-notion`, `/campanha`, `/batch`

Ver `commands/` para a lista completa e detalhes de cada um. Para um guia de descoberta orientado a "o que voce quer fazer", veja [`docs/DISCOVERY.md`](./docs/DISCOVERY.md).

## Estrutura

```
Marketing OS/
├── plugin.json              # Manifesto do plugin
├── .claude-plugin/          # marketplace.json
├── skills/marketing-os/     # Skill entrypoint (SKILL.md)
├── subagents/               # Knowledge base (Tier 2 deep refs)
├── commands/                # Slash commands
├── workflows/               # Workflows multi-step
├── assets/                  # Frameworks, personas, prompts, swipe files,
│   ├── clones/              #   templates, voice clones (Halbert, Hopkins,
│   ├── frameworks/          #   Hormozi, Kennedy, Ogilvy, Schwartz, etc)
│   ├── personas/
│   ├── prompts/
│   ├── swipe-files/
│   └── templates/
├── references/              # Guias técnicos por domínio
├── scripts/                 # Validation, tests
│   └── tests/               # Tier 1 pytest suite
├── docs/                    # Documentação
└── workspace/               # Conteúdo pessoal (gitignored)
```

## Voice clones (assets/clones/)

35 perfis detalhados de copywriters/marketers lendários para o `@mos-clone` e `/criar-clone`:

Halbert, Hopkins, Kennedy, Ogilvy, Schwartz, Sugarman, Caples, Cialdini, Brunson, Hormozi, Leila Hormozi, GaryVee, MrBeast, Codie Sanchez, Abdaal, Abraham, Joel Jota, Conrado, Mel Robbins, Patel, Provost, Rachitsky, Suby, Welsh, Cole, Collier, Ellis, Ezra Firestone, Flavio Augusto, Gadzhi, Godin, Howell, Chen, Miller — cada um com `profile.md`, `frameworks.md`, `voice.md`, `examples.md`.

## Desenvolvimento

```bash
# Validar native agents (em .claude/agents/, gitignored)
python scripts/validate_agents.py

# Tier 1 (estático, rápido)
python -m pytest scripts/tests/ -v -m "not smoke"
```

Ver `docs/superpowers/specs/` e `docs/superpowers/plans/` para histórico de refactors arquiteturais.

## Licença

MIT — ver [LICENSE](./LICENSE).
