---
name: marketing-os
description: "Marketing OS: sistema operacional completo de marketing digital com 18 subagentes nativos Claude Code. Use para posts Instagram/LinkedIn/TikTok/Twitter, artigos SEO, email marketing, landing pages, anúncios Meta/Google Ads, calendários editoriais, vídeos YouTube/Reels/VSL, podcasts, geração de imagens e vídeos com IA, infoprodutos, testes A/B. NICHOS: Marketing Digital, IA, Dev Pessoal/Profissional, Tech, Empreendedorismo, Finanças, Saúde, Educação, Produtividade. TRIGGERS: conteúdo, post, blog, SEO, newsletter, copy, landing page, campanha, anúncio, carrossel, stories, reels, vídeo, podcast, design, imagem IA, infoproduto, teste A/B."
argument-hint: "[tipo-conteúdo] [nicho] [plataforma]"
---

# Marketing OS: Sistema Operacional de Marketing Digital

Este skill é um **orquestrador** que dispara 18 subagents nativos do Claude Code, cada um com contexto isolado, tool access controlado e knowledge base profunda.

## Modo de Operação: Dispatch Nativo

**REGRA FUNDAMENTAL**: Para qualquer pedido de produção de marketing (copy, SEO, research, social, ads, etc.), **NÃO execute inline**. **Dispare o subagent especializado** via `Agent(subagent_type: "mos-*")`.

Motivo: cada subagent tem contexto próprio (evita poluição do main), tools filtrados (segurança), knowledge base deep (qualidade), e output schema padronizado (handoff entre agents).

### Quando dispatch vs execução inline

| Situação | Ação |
|----------|------|
| Pedido claro de produção de peça (copy, post, artigo, anúncio, etc.) | Dispatch |
| Pergunta conceitual sobre marketing (ex: "o que é AIDA?") | Responda inline (não precisa de agent) |
| Briefing amplo ("cria campanha completa") | Dispatch em paralelo de múltiplos agents |
| Pedido de informação sobre o próprio sistema | Inline |

## Mapa de Dispatch (18 Agents)

| Briefing típico do usuário | Agent | Arquivo |
|----|----|----|
| "escreve headline / CTA / sales letter / microcopy" | `mos-copy` | `agents/mos-copy.md` |
| "cria artigo SEO / keyword research / on-page" | `mos-seo` | `agents/mos-seo.md` |
| "pesquisa tendências / concorrentes / audience / validar produto" | `mos-research` | `agents/mos-research.md` |
| "post Instagram / LinkedIn / TikTok / Twitter / cross-platform" | `mos-social` | `agents/mos-social.md` |
| "roteiro YouTube / Reels / VSL / Shorts" | `mos-video` | `agents/mos-video.md` |
| "podcast / roteiro de áudio / spot / audiobook" | `mos-audio` | `agents/mos-audio.md` |
| "prompt para IA gerar imagem / vídeo" | `mos-ai-tools` | `agents/mos-ai-tools.md` |
| "direção criativa / paleta / tipografia / design spec" | `mos-design` | `agents/mos-design.md` |
| "métricas / relatório / análise de performance / dashboard" | `mos-analytics` | `agents/mos-analytics.md` |
| "sequência de email / newsletter / automação / subject line" | `mos-email` | `agents/mos-email.md` |
| "campanha Meta Ads / Google Ads / TikTok Ads (completa)" | `mos-ads` | `agents/mos-ads.md` |
| "identidade de marca / posicionamento / tom de voz" | `mos-brand` | `agents/mos-brand.md` |
| "storytelling / narrativa / arco de história" | `mos-storytelling` | `agents/mos-storytelling.md` |
| "funil / jornada do cliente / TOFU MOFU BOFU" | `mos-funnel` | `agents/mos-funnel.md` |
| "growth hacking / aquisição / crescimento" | `mos-growth` | `agents/mos-growth.md` |
| "lançamento de produto / campanha de lançamento / PLF" | `mos-launch` | `agents/mos-launch.md` |
| "infoproduto / curso / ebook / membership / mentoria" | `mos-infoproduct` | `agents/mos-infoproduct.md` |
| "teste A/B / variação / otimização de conversão" | `mos-ab-testing` | `agents/mos-ab-testing.md` |

## Padrões de Orquestração

### 1. Dispatch Simples (1 agent, caso mais comum)

```
Pedido: "escreve 5 headlines para curso de Python iniciante"
Ação: Agent(subagent_type: "mos-copy", prompt: "5 headlines... contexto: curso Python iniciante, público: devs juniores")
```

### 2. Dispatch Paralelo (múltiplos agents independentes)

Quando o briefing envolve áreas que **não dependem uma da outra**, dispare em **paralelo** (um único message com múltiplas Agent calls):

```
Pedido: "tenho um curso novo de IA para empreendedores, preciso de pesquisa + tom de marca + headlines iniciais"

Ação (single message, 3 tool calls simultâneas):
- Agent(subagent_type: "mos-research", prompt: "pesquisar nicho IA para empreendedores BR, concorrência, dores, trends")
- Agent(subagent_type: "mos-brand", prompt: "definir tom de voz para curso IA para empreendedores BR")
- Agent(subagent_type: "mos-copy", prompt: "5 headlines para curso IA para empreendedores BR")
```

### 3. Dispatch Sequencial (quando há dependência real)

Só sequencie quando output de um é **input necessário** do próximo:

```
Workflow "artigo SEO completo":
1. Agent(subagent_type: "mos-research", prompt: "research sobre [tema]")
2. → (usa research) Agent(subagent_type: "mos-seo", prompt: "artigo sobre [tema], usando research: [colar research brief]")
3. → (opcional) Agent(subagent_type: "mos-copy", prompt: "otimizar headline + CTA do artigo")
```

### 4. Workflow Completo (content-pipeline)

Para "criar conteúdo completo sobre X":

```
Fase 1 (paralelo): mos-research + mos-brand (se marca nova)
Fase 2 (paralelo onde possível):
  - mos-seo (se blog)  OU  mos-copy (se peça isolada)  OU  mos-social (se post)
  - mos-design (direção visual)
Fase 3: Quality gates + revisão humana
```

## Quality Gates Globais (aplicam SEMPRE)

Mesmo os subagents já aplicarem seus próprios gates, valide sempre antes de entregar ao usuário:

### Palavras e Símbolos Proibidos

| Item | Ação |
|------|------|
| `—` (travessão longo) | substituir por `.` `,` `:` ou quebrar frase |
| "brutal" | usar: intenso, forte, pesado, impactante, poderoso |
| PALAVRAS EM CAPS | reescrever em minúscula |
| Aspas em roteiros/falas | escrever direto |
| Mais de 2 emojis | reduzir para 0-1 |
| Texto sem acentos | SEMPRE usar acentuação PT-BR correta |

### Verificação de Fatos Obrigatória

Ao citar pessoas famosas, estatísticas, eventos históricos, resultados de empresas:

1. Buscar fonte primária (entrevistas, biografias, documentários, fonte oficial)
2. Verificar credibilidade (múltiplas fontes, sem desmentidos)
3. Classificar: CONFIRMADO (múltiplas fontes) | PROVÁVEL (1 fonte) | NÃO CONFIRMADO (não usar) | DESMENTIDO (nunca usar)
4. Usar WebSearch antes de publicar

### Enquetes para Engajamento

OBRIGATÓRIO para conteúdos de redes sociais (Reels, posts, carrosséis, stories). Sempre incluir sugestão de enquete relacionada.

| Tipo | Quando usar |
|------|-------------|
| Escolha binária | Opinião simples |
| Qual você faz | Identificação |
| Escala 1-10 | Medir nível |
| Desafio | Gerar compromisso |
| Curiosidade | Gerar dados |

## Nichos Suportados

| Nicho | Tom Sugerido |
|-------|--------------|
| Marketing Digital | Autoridade, data-driven |
| Inteligência Artificial | Educativo, acessível |
| Desenvolvimento Pessoal | Inspiracional, empático |
| Desenvolvimento Profissional | Profissional, prático |
| Tecnologia/Programação | Técnico, didático |
| Empreendedorismo | Motivador, estratégico |
| Finanças Pessoais | Educativo, confiável |
| Saúde e Bem-Estar | Acolhedor, motivador |
| Educação | Didático, encorajador |
| Produtividade | Prático, direto |

Detalhes em `references/niches.md`.

## Recursos Auxiliares (invocados sob demanda pelos agents)

### Templates (`assets/templates/`)
- `youtube-script.md`, `reels-tiktok-script.md`, `vsl-script.md`, `podcast-episode.md`, `instagram-feed-post.md`, `post-instagram-carrossel.md`, `instagram-stories.md`, `sales-page.md`, `webinar-script.md`, `lead-magnet.md` e mais 16 especializados.

### Swipe Files (`assets/swipe-files/`)
- `headlines-virais.md`, `hooks-reels.md`, `ctas-conversao.md`, `copy-carrossel.md`, `bios-instagram.md`, `transicoes-reels.md`, `paletas-cores.md`, `emails-conversao.md`, `trends-adaptaveis.md`.

### Scripts Python (`scripts/`)
29 ferramentas + CLI unificado `mos.py`. Os agents com acesso a `Bash` podem invocar:
- `seo_analyzer.py`, `hashtag_generator.py`, `hook_generator.py`, `reels_script_generator.py`, `carousel_structure_generator.py`, `caption_generator.py`, `trend_tracker.py`, `project_manager.py`, `quality_gate.py`, etc.

### Workflows (`workflows/`)
9 workflows end-to-end documentados: `lancamento-produto.md`, `calendario-mensal.md`, `funil-vendas.md`, `batch-production-workflow.md`, `parceria-influencer.md`, `content-pipeline.md`, `campanha-conversao.md`, `tiktok-trends-chrome.md`, `end-to-end-campaign-workflow.md`.

### Referências (`references/`)
- `social-media.md`, `blog-seo.md`, `email-marketing.md`, `landing-pages.md`, `ads-copy.md`, `design-specs.md`, `strategy.md`, `ux-writing-microcopy.md`, `niches.md`.

## Protocolo de Entrega ao Usuário

Após o agent (ou agents em paralelo) retornar(em):

1. **Consolide** os outputs (se múltiplos agents): junte as peças em uma entrega única.
2. **Rode Quality Gates Globais** acima (mesmo que os agents já tenham rodado).
3. **Formate** em markdown clean, sem travessões, com acentos corretos.
4. **Inclua enquete** (se conteúdo social).
5. **Adicione próximos passos** acionáveis (ex: "testar variação B em 7 dias", "publicar em horário X").

## Entregáveis Padrão

1. Conteúdo principal formatado
2. 2-3 variações A/B
3. Recomendações de otimização
4. Métricas sugeridas
5. Próximos passos acionáveis
6. Hashtags/Keywords relevantes
7. Prompts de IA (quando aplicável)
8. Enquete para engajamento (para conteúdos de redes sociais)

## Arquitetura (two-tier)

- **Tier 1** (`agents/mos-*.md`): system prompts enxutos (~250 linhas) com dispatch protocol, output schema, quality gates. Carregados pelo Claude Code automaticamente quando sessão abre.
- **Tier 2** (`subagents/*-agent.md`): knowledge base profunda (~3500 linhas cada) com frameworks, cases, tabelas, exemplos. Lida sob demanda via Read pelos agents tier-1.

Isso mantém contextos dos agents leves, carrega profundidade só quando precisa, e permite evoluir knowledge sem mexer no dispatch.

## Versão

Marketing OS v6.0.0 (native subagents). Migração documentada em `docs/architecture/subagents-migration.md`.
