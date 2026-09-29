# Marketing OS

> Plugin para ChatGPT Work, Claude Code e Codex com **21 especialistas** em marketing digital, 53 slash commands no Claude Code e 34 voice clones de copywriters.

[![Version](https://img.shields.io/badge/version-6.16.0-blue.svg)](./CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

## O que é

Marketing OS é um plugin para ChatGPT Work, [Claude Code](https://www.anthropic.com/claude-code) e Codex que orquestra 21 especialistas em domínios distintos do marketing digital. O plugin reivindica território explícito sobre briefings de marketing. Quando você pede "cria página de aplicação" ou "monta um webinar", ele roteia os especialistas corretos, preserva dependências entre etapas e executa a camada estratégica antes do build técnico.

**49 dos 53 slash commands** dispatcham subagents `mos-*`. Os 4 que não dispatcham são intencionais: `/publicar-notion` (utility do Notion MCP), `/campanha` (índice dos 6 sub-commands de preset), `/projeto` (orquestrador de workflow com dispatch dinâmico) e `/datas-sazonais` (utilitário de dados do calendário sazonal BR). Use `/mo` pra briefing aberto se não souber qual command escolher. **Conteúdo PT-BR otimizado para o mercado brasileiro.**

## Instalação

### ChatGPT Work

O pacote universal em `.codex-plugin/plugin.json` pode ser instalado no ChatGPT Work como plugin `skills-only`. Para testar a versão deste repositório no ChatGPT Desktop:

1. Abra este repositório no ChatGPT Desktop.
2. Selecione **ChatGPT** e ative **Work**.
3. Abra **Plugins** e escolha a fonte **Marketing OS**.
4. Instale o plugin e inicie uma conversa Work nova.
5. Digite `@Marketing OS` ou descreva o resultado diretamente.

Exemplos:

```text
@Marketing OS crie o avatar completo do meu cliente ideal.
```

```text
@Marketing OS crie uma USP usando o avatar e as evidências disponíveis.
```

```text
@Marketing OS estruture minha oferta com preço, bônus e garantia.
```

O marketplace repo-scoped usado pelo ChatGPT Desktop está em `.agents/plugins/marketplace.json`. A instalação local fica disponível no Desktop. O uso no ChatGPT Work pela web depende de publicação ou compartilhamento no diretório de plugins.

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
codex plugin marketplace add rilnermucio/esp-marketing-os --ref v6.16.0
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

## Os 21 subagentes nativos

Invocados pelo orquestrador (skill `/marketing-os`) ou diretamente via `@<agente>`:

| Agente | Domínio | Memory |
|---|---|---|
| `@mos-copy` | Copywriting persuasivo (headlines, CTAs, sales letters) | sim |
| `@mos-seo` | Otimização de busca (keywords, on-page, E-E-A-T, AI-SEO) | sim |
| `@mos-social` | Posts e estratégia em redes sociais (cross-platform) | sim |
| `@mos-video` | Roteiros (YouTube, Reels, TikTok, VSL, Shorts) | sim |
| `@mos-audio` | Podcasts, audiobooks, spots, sound design | sim |
| `@mos-design` | Direção visual, paletas, tipografia, design specs | sim |
| `@mos-ai-tools` | Prompts pra Midjourney, Flux, Runway, Sora, etc. | sim |
| `@mos-analytics` | Métricas, KPIs, dashboards, GA4 | sim |
| `@mos-email` | Email marketing (welcome, nurture, vendas, automação) | sim |
| `@mos-ads` | Anúncios pagos (Meta, Google, TikTok, LinkedIn) | sim |
| `@mos-research` | Trend spotting, audience research, validação | sim |
| `@mos-brand` | Identidade de marca, arquétipos, manifesto | sim |
| `@mos-storytelling` | Narrativa aplicada (hero's journey, StoryBrand) | sim |
| `@mos-funnel` | Funis de conversão, jornada (TOFU/MOFU/BOFU) | sim |
| `@mos-growth` | Growth hacking, AARRR, retention | sim |
| `@mos-launch` | Lançamentos (PLF, semente, relâmpago, perpétuo) | sim |
| `@mos-infoproduct` | Cursos, memberships, mentorias, ebooks | sim |
| `@mos-offer` | Arquitetura de ofertas (value stack, preço, garantia, bônus) | sim |
| `@mos-community` | Gestão de comentários/DMs (triagem, rascunhos, moderação) | sim |
| `@mos-partnerships` | Parcerias com creators (sourcing, fit, outreach) | sim |
| `@mos-ab-testing` | A/B/MVT, ICE prioritization, significância estatística | sim |

**Memory opt-in (21 agents).** Todos os agents podem persistir aprendizados entre sessões em `.claude/agent-memory/marketing-os-mos-*/MEMORY.md`. Para ativar, rode o bootstrap uma vez na raiz do projeto:

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

Ver SKILL.md pra detalhes de cada workflow e "por que essa ordem importa". Tier 2 cobre profundidade: `subagents/funnel-agent.md` documenta webinar funnel, página de aplicação BOFU e anti-avatar (workflows #5, #6, #9); `subagents/copy-agent.md` cobre big idea e value stack; `subagents/brand-agent.md` define o contrato de USP baseada em evidências.

## Slash commands rápidos

53 commands em `commands/` cobrindo workflows comuns. **49 deles dispatcham subagents `mos-*`** seguindo os workflows da tabela acima (os 4 sem dispatch são utilities intencionais: `/publicar-notion`, `/campanha` índice, `/projeto` e `/datas-sazonais`). Quando você invoca direto (`/criar-carrossel`), segue lógica do command file. Quando pede em linguagem natural ("cria carrossel sobre X"), o orquestrador da skill dispatcha conforme tabela.

| Categoria | Commands |
|---|---|
| Meta-orquestrador | `/mo` (briefing aberto, roteia pro command apropriado) |
| Conteúdo social | `/criar-post`, `/criar-carrossel`, `/criar-calendario`, `/reaproveitar` (uma fonte pilar vira várias peças) |
| Copy | `/otimizar-copy` (diagnóstico + score + reescrita de copy existente) |
| Compliance | `/checar-compliance` (conselhos, ANVISA, CVM, CONAR, CDC e LGPD, com a norma de cada ponto e a peça corrigida) |
| Prova social | `/coletar-prova` (pedido, entrevista, modelo de case e termo de autorização) |
| Vídeo/áudio | `/criar-video`, `/criar-podcast`, `/narrar-roteiro`, `/produzir-reels` (vídeo legendado renderizado) |
| Páginas/funis | `/criar-landing-page`, `/criar-funil`, `/criar-webinar` |
| Email | `/criar-email`, `/criar-sequencia` |
| Ads | `/criar-anuncio`, `/publicar-anuncio` |
| Infoproduto | `/criar-infoproduto` |
| Oferta | `/criar-oferta` (USP preservada, evidências, value stack, preço, garantia, score e validação) |
| Pesquisa de público | `/criar-avatar` (evidências, avatar principal, segmentos, anti-avatar, JTBD e handoff), `/minerar-voc` (dores, desejos e objeções literais de reviews) |
| Marca e posicionamento | `/configurar-marca` (perfil da marca lido por todos os especialistas), `/criar-usp` (USP principal, evidências, diferenciação, score, validação e handoff) |
| Comunidade | `/responder-comentarios` (triagem + rascunhos de comentários/DMs) |
| Parcerias | `/prospectar-creators` (shortlist + outreach de creators) |
| Voice clones | `/criar-clone` (expert externo), `/criar-meu-clone` (suas amostras) |
| Análise | `/analisar-concorrencia`, `/analisar-video`, `/clonar-estrategia`, `/auditoria`, `/auditoria-pro` |
| Testes A/B | `/criar-teste-ab` (hipótese, amostra, duração, critério de parada) |
| Visual | `/criar-brief-design`, `/gerar-imagem`, `/renderizar-imagem` (prompt vira PNG), `/gerar-thumbnail` (16:9 com overlay tipográfico), `/capturar-tela` |
| Operação | `/batch`, `/criar-artigo`, `/publicar-notion`, `/projeto`, `/datas-sazonais`, `/aprender` (métricas → memory) |
| Campanhas (presets) | `/campanha` (índice), `/campanha-lancamento`, `/campanha-prospeccao`, `/campanha-retencao`, `/campanha-autoridade`, `/campanha-growth`, `/campanha-black-friday` |

## Estrutura

```
Marketing OS/
├── .claude-plugin/         # plugin.json + marketplace.json
├── .codex-plugin/          # manifesto universal para ChatGPT Work e Codex
├── .agents/plugins/        # marketplace repo-scoped para ChatGPT Desktop e Codex
├── plugins/marketing-os/   # pacote universal distribuível, gerado por script
├── agents/                 # 21 native subagents (mos-*.md)
├── skills/marketing-os/    # Skill entrypoint (SKILL.md = orquestrador)
├── subagents/              # Tier 2 knowledge bases (~3500 linhas cada)
├── commands/               # 53 slash commands (49 com dispatch + /publicar-notion + /campanha índice + /projeto + /datas-sazonais)
├── workflows/              # 9 workflows end-to-end documentados
├── assets/                 # Frameworks, personas, prompts, swipe files,
│   ├── clones/             #   templates, 34 voice clones (+ design-dna)
│   ├── frameworks/
│   ├── personas/
│   ├── prompts/
│   ├── swipe-files/
│   └── templates/
├── references/             # Guias técnicos por domínio
├── scripts/                # ferramentas Python, validações e Tier 1 tests
│   ├── evals/              # perfis de avaliação por domínio
│   ├── hooks/              # núcleo do gate PreToolUse/SubagentStop
│   └── tests/              # Suite pytest
├── hooks/                  # registro global de hooks do plugin Claude
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

# Gerar e validar pacote universal ChatGPT Work e Codex
python scripts/build_codex_plugin.py
python scripts/build_codex_plugin.py --check
python scripts/validate_codex_plugin.py plugins/marketing-os

# Bootstrap memory (opt-in, 21 agents)
python3 scripts/init_agent_memory.py

# Listar perfis do avaliador de outputs
python3 scripts/copy_output_eval.py profiles

# CLI unificado das ferramentas
python scripts/mos.py --help
```

CI rodando em `.github/workflows/tests.yml`: suite Tier 1, cobertura ≥70%, validação do pacote universal para ChatGPT Work e Codex e job `validate-agents` em modo `--strict` em todo PR/push (pega regressão de frontmatter, knowledge refs quebrados e name collisions). O workflow de release repete esses gates antes de publicar. Estado atual: **21/21 agents clean** no validator.

## Documentação adicional

- **[docs/GETTING-STARTED.md](./docs/GETTING-STARTED.md)**: primeiros passos com 5 exemplos de briefings
- **[docs/TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md)**: problemas comuns de install/configuração e como resolver
- **[docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)**: arquitetura two-tier (system prompts enxutos + knowledge bases profundas)
- **[CHANGELOG.md](./CHANGELOG.md)**: histórico completo de releases
- **[AGENTS.md](./AGENTS.md)**: guia canônico pra contributors e agentes de IA

## Licença

MIT, ver [LICENSE](./LICENSE).
