# Marketing OS — Guia de Descoberta

> Encontre em 5 segundos o agent, comando ou workflow certo para sua tarefa.

## Decisão rápida: o que voce quer fazer?

### 1. Produzir uma peça única

| Quero criar... | Slash command | Subagent |
|----------------|---------------|----------|
| Post Instagram | `/criar-post` | `@mos-social` |
| Carrossel Instagram | `/criar-carrossel` | `@mos-social` |
| Roteiro Reels/TikTok/Shorts | `/criar-video` | `@mos-video` |
| Vídeo YouTube longo | `/criar-video` | `@mos-video` |
| VSL (Video Sales Letter) | `/criar-video` | `@mos-video` + `@mos-copy` |
| Roteiro de podcast | `/criar-podcast` | `@mos-audio` |
| Headlines, CTAs, microcopy | (direto) | `@mos-copy` |
| Artigo SEO / blog post | `/criar-artigo` | `@mos-seo` |
| Sequência de email | `/criar-email` ou `/criar-sequencia` | `@mos-email` |
| Anúncio Meta/Google/TikTok | `/criar-anuncio` | `@mos-ads` |
| Landing page | `/criar-landing-page` | `@mos-copy` + `@mos-design` |
| Webinar | `/criar-webinar` | `@mos-launch` + `@mos-copy` |
| Imagem com IA (prompt) | `/gerar-imagem` | `@mos-ai-tools` |
| Brief de design | `/criar-brief-design` | `@mos-design` |

### 2. Produzir uma campanha completa (multi-artefato)

Use **workflows** (em `workflows/`) quando precisa de vários artefatos coordenados.

| Objetivo | Workflow |
|----------|----------|
| Lançamento de produto (PLF) | `lancamento-produto.md` |
| Campanha de conversão (paid + orgânico) | `campanha-conversao.md` |
| Calendário editorial mensal | `calendario-mensal.md` |
| Pipeline de conteúdo end-to-end | `content-pipeline.md` |
| Funil de vendas completo | `funil-vendas.md` |
| Parceria com influenciador | `parceria-influencer.md` |
| Produção em escala (batch) | `batch-production-workflow.md` |
| Hijack de tendência TikTok | `tiktok-trends-chrome.md` |
| Campanha end-to-end (briefing → publicação) | `end-to-end-campaign-workflow.md` |

Slash command equivalente: `/campanha` (briefing alto nível → workflow recomendado) ou `/batch` (produção em massa).

### 3. Análise e diagnóstico

| Quero... | Use |
|----------|-----|
| Auditar concorrente | `/analisar-concorrencia` ou `@mos-research` |
| Pesquisar tendências de nicho | `@mos-research` |
| Analisar vídeo (concorrente ou meu) | `/analisar-video` |
| Métricas / relatório de performance | `@mos-analytics` |
| Clonar estratégia de outro perfil | `/clonar-estrategia` |
| Capturar screenshot pra brief | `/capturar-tela` |

### 4. Estratégia / setup (geralmente 1x)

| Quero... | Use |
|----------|-----|
| Definir identidade de marca | `@mos-brand` |
| Definir tom de voz / posicionamento | `@mos-brand` |
| Estruturar narrativa de marca | `@mos-storytelling` |
| Criar curso ou infoproduto | `/criar-infoproduto` ou `@mos-infoproduct` |
| Mapear funil completo (TOFU/MOFU/BOFU) | `/criar-funil` ou `@mos-funnel` |
| Plano de growth / experimentação | `@mos-growth` |
| Plano de teste A/B | `@mos-ab-testing` |
| Clone de copywriter (voz Halbert, Ogilvy, etc.) | `/criar-clone` |

### 5. Publicação

| Quero publicar em... | Use |
|---------------------|-----|
| Meta Ads (anúncio direto) | `/publicar-anuncio` |
| Notion (post/artigo) | `/publicar-notion` |

## Quando usar comando vs subagent vs workflow

| Cenário | Use |
|---------|-----|
| Tarefa simples e direta ("escreve 5 headlines") | **Subagent direto** (`@mos-copy`) |
| Fluxo padrão repetitivo ("crio post toda quarta") | **Slash command** (`/criar-post`) |
| Operação multi-artefato com dependências | **Workflow** (em `workflows/`) |
| Briefing amplo ("preciso de campanha completa") | **Slash command `/campanha`** (delega pro workflow certo) |

## Dispatch paralelo (avançado)

Quando precisar de múltiplas peças independentes, peça produção em paralelo:

```
"Tenho um curso novo de IA. Preciso de:
- pesquisa de mercado (mos-research)
- tom de marca (mos-brand)
- 5 headlines iniciais (mos-copy)
em paralelo."
```

O orquestrador (skill `marketing-os`) dispara os 3 agents simultaneamente, cada um em contexto isolado.

## Os 18 subagents (referência)

| Agent | Especialidade |
|-------|--------------|
| `mos-copy` | Copywriting persuasivo (headlines, CTAs, microcopy) |
| `mos-seo` | SEO técnico e de conteúdo |
| `mos-social` | Posts e estratégia em redes sociais |
| `mos-video` | Roteiros de vídeo (YouTube, Reels, TikTok, VSL) |
| `mos-audio` | Podcasts e produção de áudio |
| `mos-design` | Direção visual e brief de design |
| `mos-ai-tools` | Prompts para Midjourney, Runway, ElevenLabs, etc. |
| `mos-analytics` | Métricas, GA4, dashboards |
| `mos-email` | Email marketing e automação |
| `mos-ads` | Campanhas pagas (Meta, Google, TikTok, LinkedIn) |
| `mos-research` | Pesquisa de mercado, concorrência, audiência |
| `mos-brand` | Identidade de marca, arquétipos, posicionamento |
| `mos-storytelling` | Narrativas e arcos de história |
| `mos-funnel` | Funis de vendas e jornada do cliente |
| `mos-growth` | Growth hacking e aquisição |
| `mos-launch` | Lançamentos (PLF, semente, relâmpago) |
| `mos-infoproduct` | Cursos, ebooks, memberships, mentorias |
| `mos-ab-testing` | Testes A/B e otimização estatística |

## Próximos passos

- **Primeira vez aqui?** Comece com `/criar-post` ou `/criar-artigo` para sentir o sistema.
- **Quer entender a arquitetura?** Leia `skills/marketing-os/SKILL.md` (orquestrador) e `docs/architecture/subagents-migration.md`.
- **Quer estender o sistema?** Veja `docs/archive/SUBAGENTS-EXPANSION-PLAN.md`.

## Quality gates (sempre aplicados)

Toda saída de conteúdo passa por gates automáticos via `scripts/hooks/quality_gate_hook.py`:

**HARD BLOCK (exit 2, refazer obrigatorio):**
- Em-dash `—`
- Palavra "brutal"

**WARN (exit 0 + stderr, agent decide):**
- Clichês PT-BR: "em um mundo onde", "sem mais delongas", "vamos mergulhar", "imagine se", "e se eu te dissesse", "preparados? vamos lá"
- Fillers: "vale ressaltar", "é importante destacar", "em última análise", "na verdade", "basicamente", "simplesmente"
- Superlativos vagos: "extraordinário", "revolucionário", "incrível", "o melhor do mundo"

**COMPLIANCE WARN (exit 0 + stderr):**
- Conteúdo financeiro sem disclaimer CVM
- Conteúdo de saúde sem disclaimer ANVISA
- Depoimento sem disclaimer CONAR
- Link afiliado sem disclosure

Violações HARD bloqueiam a escrita. WARNs aparecem no terminal mas não bloqueiam — agent decide se reescreve. Acentuação PT-BR e fact-check de citações são validados no agent (não no hook). Detalhes em `skills/marketing-os/SKILL.md` (Quality Gates Globais).

## Voice clones (35 + custom)

35 voice clones pré-construídos em `assets/clones/` (Halbert, Ogilvy, Hormozi, Schwartz, ...). Cada clone tem 4 arquivos profundos: `profile.md`, `voice.md`, `frameworks.md`, `examples.md`.

**Para gerar copy "estilo X"**: o `mos-copy` agent é instruído a Read `assets/clones/{nome}/voice.md` ANTES de gerar (não usa só resumo inline).

**Para criar SEU próprio clone**: use `/criar-meu-clone {slug}` com 10-20 amostras reais da sua escrita. O comando extrai vocabulário, cadência, estrutura narrativa e anti-padrões da sua voz e gera os 4 arquivos.
