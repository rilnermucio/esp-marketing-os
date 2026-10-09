---
name: content-creator
description: "Agente de criação de conteúdo para múltiplos nichos e plataformas. Use para: posts de redes sociais (Instagram, LinkedIn, Twitter/X, TikTok), artigos SEO, email marketing, landing pages, anúncios (Meta/Google Ads), calendários editoriais, vídeos (YouTube, Reels, VSL), podcasts, geração de imagens e vídeos com IA. NICHOS: Marketing Digital, IA, Desenvolvimento Pessoal/Profissional, Tech, Empreendedorismo, Finanças, Saúde, Educação, Produtividade. TRIGGERS: conteúdo, marketing, post, blog, SEO, newsletter, copy, landing page, campanha, anúncio, Instagram, LinkedIn, TikTok, IA, desenvolvimento pessoal, carreira, vídeo, YouTube, Reels, podcast, VSL."
---

# Content Creator - Agente de Criação de Conteúdo

Agente especializado em criação de conteúdo estratégico cobrindo múltiplos nichos, plataformas e formatos com foco em engajamento, conversão e SEO.

## Arquitetura do Agente

```
CONTENT CREATOR (Agente Principal)
│
├── 🔍 RESEARCH AGENT (Subagente de Pesquisa)
│   ├── Pesquisa de tendências
│   ├── Análise de concorrência
│   ├── Keyword research
│   ├── Mapeamento de audiência
│   └── Coleta de dados/estatísticas
│
├── ✍️ COPY AGENT (Subagente de Copywriting)
│   ├── Headlines e hooks
│   ├── CTAs otimizados
│   ├── Copy de vendas
│   ├── Variações A/B
│   └── Copy de anúncios
│
├── 🔎 SEO AGENT (Subagente de SEO)
│   ├── Otimização on-page
│   ├── Estruturação de conteúdo
│   ├── Meta tags
│   ├── Featured snippets
│   └── E-E-A-T
│
├── 📱 SOCIAL AGENT (Subagente de Redes Sociais)
│   ├── Posts por plataforma
│   ├── Adaptação cross-platform
│   ├── Hashtags e timing
│   ├── Calendário social
│   └── Métricas de engajamento
│
├── 🎬 VIDEO AGENT (Subagente de Vídeo) ⭐ NOVO
│   ├── Scripts YouTube (long-form)
│   ├── Scripts Reels/TikTok/Shorts
│   ├── VSL (Video Sales Letter)
│   ├── Hooks e retenção
│   └── Estruturas de storytelling
│
├── 🤖 AI TOOLS AGENT (Subagente de Ferramentas IA)
│   ├── Prompts para imagem (Nanobanana Pro, GPT 1.5, Midjourney, DALL-E)
│   ├── Prompts para vídeo (Veo 3.1, Sora 2, Kling 2.6, Kling O1, Seedance)
│   ├── Workflows multi-ferramenta
│   └── Otimização de prompts
│
├── 🎨 DESIGN AGENT (Subagente de Design Visual) 🆕
│   ├── Direção criativa e moodboards
│   ├── Specs técnicos por plataforma
│   ├── Templates e layouts visuais
│   ├── Paletas de cores e tipografia
│   ├── Prompts otimizados para imagem IA
│   ├── Briefing visual completo
│   └── 🆕 Posts prontos (Nano Banana Pro) - imagem + texto
│
├── 📊 ANALYTICS AGENT (Subagente de Análise)
│   ├── Métricas por plataforma
│   ├── Relatórios semanais/mensais
│   ├── Análise de performance
│   ├── Testes A/B
│   └── Otimização baseada em dados
│
└── 🎙️ AUDIO AGENT (Subagente de Áudio) ⭐ NOVO
    ├── Roteiros de podcast (solo, entrevista, co-host)
    ├── Estruturas de episódio
    ├── Scripts de spots/ads
    └── Audiobooks e narrações
```

## Subagentes

| Subagente | Referência | Quando Acionar |
|-----------|------------|----------------|
| Research Agent | [subagents/research-agent.md](subagents/research-agent.md) | Novo nicho, tendências, concorrência, dados |
| Copy Agent | [subagents/copy-agent.md](subagents/copy-agent.md) | Headlines, CTAs, copy persuasivo, A/B |
| SEO Agent | [subagents/seo-agent.md](subagents/seo-agent.md) | Artigos, blog posts, otimização on-page |
| Social Agent | [subagents/social-agent.md](subagents/social-agent.md) | Posts sociais, adaptação, hashtags |
| **Video Agent** ⭐ | [subagents/video-agent.md](subagents/video-agent.md) | YouTube, Reels, TikTok, VSL, roteiros de vídeo |
| **AI Tools Agent** | [subagents/ai-tools-agent.md](subagents/ai-tools-agent.md) | Geração de imagens e vídeos com IA |
| **Design Agent** 🆕 | [subagents/design-agent.md](subagents/design-agent.md) | Direção criativa, specs técnicos, paletas, layouts, prompts de imagem, **posts prontos com texto** |
| **Analytics Agent** | [subagents/analytics-agent.md](subagents/analytics-agent.md) | Métricas, relatórios, análise de performance |
| **Audio Agent** ⭐ | [subagents/audio-agent.md](subagents/audio-agent.md) | Podcasts, roteiros de áudio, spots |
| **Email Agent** 🆕 | [subagents/email-agent.md](subagents/email-agent.md) | Sequências de email, newsletters, automações |
| **Ads Agent** 🆕 | [subagents/ads-agent.md](subagents/ads-agent.md) | Copy de anúncios Meta/Google/TikTok, estratégia de ads |

## Assets e Recursos

### Templates
| Template | Referência | Uso |
|----------|------------|-----|
| YouTube Script | [assets/templates/youtube-script.md](assets/templates/youtube-script.md) | Roteiros completos para vídeos longos |
| Reels/TikTok | [assets/templates/reels-tiktok-script.md](assets/templates/reels-tiktok-script.md) | Scripts para vídeos curtos (15s, 30s, 60s) |
| VSL | [assets/templates/vsl-script.md](assets/templates/vsl-script.md) | Video Sales Letter completo |
| Podcast | [assets/templates/podcast-episode.md](assets/templates/podcast-episode.md) | Estrutura de episódio |
| Twitter Thread | [assets/templates/twitter-thread.md](assets/templates/twitter-thread.md) | Threads virais |
| Press Release | [assets/templates/press-release.md](assets/templates/press-release.md) | Comunicados de imprensa |
| Case Study | [assets/templates/case-study.md](assets/templates/case-study.md) | Estudos de caso |
| Whitepaper | [assets/templates/whitepaper.md](assets/templates/whitepaper.md) | Conteúdo B2B aprofundado |
| **Webinar Script** 🆕 | [assets/templates/webinar-script.md](assets/templates/webinar-script.md) | Roteiro completo de webinar/live de vendas |
| **Sales Page** 🆕 | [assets/templates/sales-page.md](assets/templates/sales-page.md) | Estrutura de página de vendas |
| **Lead Magnet** 🆕 | [assets/templates/lead-magnet.md](assets/templates/lead-magnet.md) | Templates de iscas digitais |
| **UGC Brief** 🆕 | [assets/templates/ugc-brief.md](assets/templates/ugc-brief.md) | Briefing para criadores UGC |
| **YouTube Shorts** 🆕 | [assets/templates/youtube-shorts.md](assets/templates/youtube-shorts.md) | Scripts e estratégias para Shorts |
| **Pinterest Pins** 🆕 | [assets/templates/pinterest-pins.md](assets/templates/pinterest-pins.md) | Templates de pins, boards e SEO |
| **Podcast Ad Reads** 🆕 | [assets/templates/podcast-ad-reads.md](assets/templates/podcast-ad-reads.md) | Scripts de anúncios para podcast |
| **Instagram Stories** 🆕 | [assets/templates/instagram-stories.md](assets/templates/instagram-stories.md) | Templates estratégicos de Stories, sequências, hooks e stickers |
| **Instagram Feed Post** 🆕 | [assets/templates/instagram-feed-post.md](assets/templates/instagram-feed-post.md) | Templates de posts (valor, storytelling, lista, citação, engajamento) |
| **Post Carrossel** 🆕 | [assets/templates/post-instagram-carrossel.md](assets/templates/post-instagram-carrossel.md) | Estrutura de carrosséis para Instagram |
| **Reels Audio Strategy** 🆕 | [assets/templates/reels-audio-strategy.md](assets/templates/reels-audio-strategy.md) | Estratégia de áudio para Reels (trending, voiceover, licenciamento) |
| **Carrossel Thumbnail Mastery** 🆕 | [assets/templates/carrossel-thumbnail-mastery.md](assets/templates/carrossel-thumbnail-mastery.md) | Otimização do Slide 1, 50+ hooks, design e A/B testing |
| **Card Único por Nicho** 🆕 | [assets/templates/card-unico-niche-templates.md](assets/templates/card-unico-niche-templates.md) | Templates específicos por nicho (Marketing, Finanças, Fitness, etc.) |
| **Pesquisa TikTok Trends** 🆕 | [assets/templates/pesquisa-tiktok-trends.md](assets/templates/pesquisa-tiktok-trends.md) | Template para documentar e analisar vídeos virais do TikTok |

### Swipe Files
| Swipe File | Referência | Uso |
|------------|------------|-----|
| Headlines Virais | [assets/swipe-files/headlines-virais.md](assets/swipe-files/headlines-virais.md) | Estruturas de títulos testados |
| Hooks Reels | [assets/swipe-files/hooks-reels.md](assets/swipe-files/hooks-reels.md) | Hooks para vídeos curtos |
| CTAs Conversão | [assets/swipe-files/ctas-conversao.md](assets/swipe-files/ctas-conversao.md) | Chamadas para ação |
| Emails Conversão | [assets/swipe-files/emails-conversao.md](assets/swipe-files/emails-conversao.md) | Templates de email |
| Copy Carrossel | [assets/swipe-files/copy-carrossel.md](assets/swipe-files/copy-carrossel.md) | Estruturas de carrosséis |
| **Bios Instagram** 🆕 | [assets/swipe-files/bios-instagram.md](assets/swipe-files/bios-instagram.md) | Exemplos de bio otimizadas por nicho |
| **Transições Reels** 🆕 | [assets/swipe-files/transicoes-reels.md](assets/swipe-files/transicoes-reels.md) | Catálogo de transições criativas por dificuldade |
| **Trends Adaptáveis** 🆕 | [assets/swipe-files/trends-adaptaveis.md](assets/swipe-files/trends-adaptaveis.md) | Guia de adaptação de 12 trends virais por nicho |
| **Paletas de Cores** 🆕 | [assets/swipe-files/paletas-cores.md](assets/swipe-files/paletas-cores.md) | Paletas por nicho, emoção e gradientes prontos |

### Frameworks
| Framework | Referência | Uso |
|-----------|------------|-----|
| **Crescimento Instagram** 🆕 | [assets/frameworks/instagram-growth-framework.md](assets/frameworks/instagram-growth-framework.md) | Guia completo de crescimento orgânico (5 fases: fundamento, estratégia, execução, crescimento, monetização) |

### Prompts IA 🆕
| Recurso | Referência | Uso |
|---------|------------|-----|
| Biblioteca de Prompts | [assets/prompts/prompt-biblioteca.md](assets/prompts/prompt-biblioteca.md) | Prompts para diversas ferramentas de IA |
| **Prompts Imagem IA** 🆕 | [assets/prompts/prompts-imagem-ia.md](assets/prompts/prompts-imagem-ia.md) | Prompts otimizados para Midjourney, DALL-E, Flux 2 Pro, GPT Image 1.5, Seedream 4.5, Nano Banana Pro |
| **Posts Prontos** 🆕 | [assets/prompts/prompts-post-pronto.md](assets/prompts/prompts-post-pronto.md) | Prompts Nano Banana Pro para gerar imagens finais com texto integrado (sem Canva) |

### Personas
| Recurso | Referência | Uso |
|---------|------------|-----|
| Template de Persona | [assets/personas/persona-template.md](assets/personas/persona-template.md) | Criar novas personas |
| Personas por Nicho | [assets/personas/personas-por-nicho.md](assets/personas/personas-por-nicho.md) | Personas pré-definidas |

### Workflows
| Workflow | Referência | Uso |
|----------|------------|-----|
| Lançamento de Produto | [workflows/lancamento-produto.md](workflows/lancamento-produto.md) | Campanha completa de lançamento |
| Calendário Mensal | [workflows/calendario-mensal.md](workflows/calendario-mensal.md) | Planejamento editorial mensal |
| Campanha de Conversão | [workflows/campanha-conversao.md](workflows/campanha-conversao.md) | Flash sale, promoções, leads |
| **Funil de Vendas** 🆕 | [workflows/funil-vendas.md](workflows/funil-vendas.md) | Processo completo TOFU → MOFU → BOFU |
| **Parceria Influencer** 🆕 | [workflows/parceria-influencer.md](workflows/parceria-influencer.md) | Prospecção, briefing e gestão de influenciadores |
| **Batch Production** 🆕 | [workflows/batch-production-workflow.md](workflows/batch-production-workflow.md) | Produção em lote de Reels, Carrosséis e Cards (cronograma, templates, checklists) |
| **TikTok Trends Chrome** 🆕 | [workflows/tiktok-trends-chrome.md](workflows/tiktok-trends-chrome.md) | Busca manual de vídeos virais via browser (workflow + templates de coleta) |

## Workflow Principal

1. **Entender o briefing** → Nicho, objetivo, público-alvo, tom de voz, CTAs
2. **[RESEARCH AGENT]** → Pesquisar tendências, concorrência, keywords, dados
3. **Consultar referência do nicho** → [references/niches.md](references/niches.md) para contexto específico
4. **Selecionar subagente especializado**:
   - Texto para redes → [SOCIAL AGENT]
   - Artigo/blog → [SEO AGENT]
   - Vídeo → [VIDEO AGENT]
   - Podcast → [AUDIO AGENT]
   - Imagem/Vídeo IA → [AI TOOLS AGENT]
   - Design visual → [DESIGN AGENT]
5. **[COPY AGENT]** → Criar copy persuasivo, headlines, CTAs
6. **[DESIGN AGENT]** → Definir visual, cores, layout, prompts de imagem
7. **Otimizar** → SEO, hashtags, horários, formatos
7. **[ANALYTICS AGENT]** → Definir métricas e KPIs
8. **Entregar** → Formatar para plataforma final, incluir variações A/B

## Referências por Tipo de Conteúdo

| Tipo | Referência | Quando Usar |
|------|------------|-------------|
| Redes Sociais | [references/social-media.md](references/social-media.md) | Posts Instagram, LinkedIn, Twitter/X, TikTok, Facebook |
| Blog/Artigos | [references/blog-seo.md](references/blog-seo.md) | Artigos, blog posts, SEO content |
| Email Marketing | [references/email-marketing.md](references/email-marketing.md) | Newsletters, sequências, campanhas |
| Landing Pages | [references/landing-pages.md](references/landing-pages.md) | Páginas de conversão, copy de vendas |
| Anúncios | [references/ads-copy.md](references/ads-copy.md) | Meta Ads, Google Ads, copy de performance |
| Estratégia | [references/strategy.md](references/strategy.md) | Calendário editorial, planejamento, personas |
| Nichos | [references/niches.md](references/niches.md) | Conteúdo específico por nicho/indústria |
| **Design Specs** 🆕 | [references/design-specs.md](references/design-specs.md) | Dimensões, safe zones, formatos por plataforma |

## Nichos Suportados

| Nicho | Foco Principal | Tom Sugerido |
|-------|----------------|--------------|
| Inteligência Artificial | Ferramentas, tutoriais, tendências | Educativo, acessível |
| Desenvolvimento Pessoal | Mindset, hábitos, propósito | Inspiracional, empático |
| Desenvolvimento Profissional | Carreira, skills, liderança | Profissional, prático |
| Tecnologia/Programação | Código, tutoriais, carreira tech | Técnico, didático |
| Empreendedorismo | Negócios, vendas, escala | Motivador, estratégico |
| Finanças Pessoais | Investimentos, renda, organização | Educativo, confiável |
| Saúde e Bem-Estar | Exercício, nutrição, mental | Acolhedor, motivador |
| Educação | Estudos, aprendizado, concursos | Didático, encorajador |
| Produtividade | Tempo, foco, ferramentas | Prático, direto |
| Marketing Digital | Estratégias, ferramentas, métricas | Autoridade, data-driven |

Para detalhes específicos de cada nicho (personas, pilares, temas, hooks, hashtags), consultar [references/niches.md](references/niches.md).

## Processo por Tipo de Solicitação

### Criando Posts para Redes Sociais
1. Identificar nicho, plataforma e objetivo (engajamento, conversão, awareness)
2. Consultar [references/niches.md](references/niches.md) para contexto do nicho
3. Ler [references/social-media.md](references/social-media.md) para formato específico da plataforma
4. Aplicar framework de copy adequado (AIDA, PAS, BAB)
5. Gerar 3 variações com CTAs diferentes
6. Incluir sugestões de hashtags, horários e formatos visuais

### Criando Artigos/Blog Posts
1. Identificar nicho e pesquisar keyword principal e relacionadas
2. Ler [references/blog-seo.md](references/blog-seo.md) para estrutura SEO
3. Criar outline com H2s e H3s otimizados
4. Escrever conteúdo seguindo E-E-A-T (Expertise, Experience, Authority, Trust)
5. Otimizar meta title, meta description, URLs, alt texts

### Criando Email Marketing
1. Definir nicho, objetivo e posição no funil
2. Ler [references/email-marketing.md](references/email-marketing.md)
3. Criar subject line com variações A/B
4. Estruturar email com preview text, body, CTA
5. Incluir personalização e segmentação

### Criando Landing Pages
1. Identificar nicho, estágio do funil e oferta
2. Ler [references/landing-pages.md](references/landing-pages.md)
3. Aplicar framework de copy (Headlines, Benefits, Social Proof, CTA)
4. Criar variações de headlines e CTAs
5. Otimizar para conversão e SEO

### Criando Anúncios
1. Definir nicho, plataforma, objetivo e público
2. Ler [references/ads-copy.md](references/ads-copy.md)
3. Criar múltiplas variações seguindo limites de caracteres
4. Incluir headlines primárias e secundárias
5. Sugerir segmentação e estratégia de lance

### Criando Vídeos (YouTube, Reels, TikTok, VSL) ⭐ NOVO
1. Identificar formato (long-form, short-form, VSL)
2. Consultar [subagents/video-agent.md](subagents/video-agent.md)
3. Usar template apropriado de [assets/templates/](assets/templates/)
4. Aplicar hooks de [assets/swipe-files/hooks-reels.md](assets/swipe-files/hooks-reels.md)
5. Estruturar com técnicas de retenção
6. [AI TOOLS AGENT] para geração de assets visuais

### Criando Podcasts ⭐ NOVO
1. Definir formato (solo, entrevista, co-host, storytelling)
2. Consultar [subagents/audio-agent.md](subagents/audio-agent.md)
3. Usar template de [assets/templates/podcast-episode.md](assets/templates/podcast-episode.md)
4. Estruturar com intro, segmentos, CTA, outro
5. Incluir show notes e timestamps

### Gerando Imagens/Vídeos com IA ⭐ NOVO
1. Definir objetivo e estilo visual
2. Consultar [subagents/ai-tools-agent.md](subagents/ai-tools-agent.md)
3. Selecionar ferramenta apropriada:
   - Imagens: Nanobanana Pro, GPT 1.5, Midjourney, DALL-E 3
   - Vídeos: Veo 3.1, Sora 2, Kling 2.6, Kling O1, Seedance
4. Aplicar estrutura de prompt otimizada
5. Iterar conforme necessário

### Planejando Estratégia de Conteúdo
1. Ler [references/strategy.md](references/strategy.md) para framework completo
2. Definir personas usando [assets/personas/](assets/personas/)
3. Estabelecer pilares de conteúdo
4. Criar calendário editorial com [workflows/calendario-mensal.md](workflows/calendario-mensal.md)
5. Definir KPIs usando [subagents/analytics-agent.md](subagents/analytics-agent.md)

### Executando Campanhas ⭐ NOVO
1. Identificar tipo (lançamento, promoção, lead gen)
2. Consultar workflow apropriado em [workflows/](workflows/)
3. Seguir checklist e timeline
4. Preparar todos os assets necessários
5. Definir métricas de sucesso

## Frameworks de Copywriting

### AIDA (Awareness → Interest → Desire → Action)
```
[ATENÇÃO] Hook impactante que para o scroll
[INTERESSE] Apresentar o problema/oportunidade
[DESEJO] Mostrar benefícios e transformação
[AÇÃO] CTA claro e urgente
```

### PAS (Problem → Agitate → Solution)
```
[PROBLEMA] Identificar a dor específica
[AGITAR] Intensificar as consequências
[SOLUÇÃO] Apresentar a solução como alívio
```

### BAB (Before → After → Bridge)
```
[ANTES] Situação atual do público
[DEPOIS] Visão da transformação desejada
[PONTE] Seu produto/serviço como caminho
```

### 4Ps (Promise → Picture → Proof → Push)
```
[PROMESSA] Benefício principal
[IMAGEM] Visualização do resultado
[PROVA] Social proof, dados, depoimentos
[EMPURRÃO] CTA com urgência
```

### QUEST (Qualify → Understand → Educate → Stimulate → Transition)
```
[QUALIFICAR] Identificar persona específica
[ENTENDER] Validar o problema
[EDUCAR] Apresentar insight/método
[ESTIMULAR] Criar desejo pelo resultado
[TRANSICIONAR] CTA para próximo passo
```

## Tom de Voz

Adaptar o tom conforme o briefing e nicho:

| Tom | Características | Uso |
|-----|-----------------|-----|
| Profissional | Formal, técnico, confiável | B2B, LinkedIn, whitepapers |
| Conversacional | Amigável, próximo, casual | Instagram, blogs, newsletters |
| Urgente | Direto, escasso, FOMO | Promoções, lançamentos |
| Inspiracional | Motivador, emocional, storytelling | Dev pessoal, branding, awareness |
| Educativo | Informativo, claro, didático | Tutoriais, how-to, SEO content |
| Técnico | Detalhado, preciso, especializado | Tech, programação, nichos específicos |
| Empático | Acolhedor, compreensivo | Saúde, bem-estar, momentos difíceis |

## Scripts Disponíveis

| Script | Uso | Comando |
|--------|-----|---------|
| `seo_analyzer.py` | Analisar e otimizar conteúdo para SEO | `python scripts/seo_analyzer.py arquivo.md "keyword"` |
| `hashtag_generator.py` | Gerar hashtags relevantes por nicho | `python scripts/hashtag_generator.py nicho plataforma` |
| `content_calendar.py` | Criar calendário editorial | `python scripts/content_calendar.py YYYY-MM-DD semanas plataformas...` |
| `ab_generator.py` | Gerar variações A/B de copy | `python scripts/ab_generator.py tipo "texto original"` |
| **`headline_scorer.py`** ⭐ | Pontuar headlines por efetividade | `python scripts/headline_scorer.py "headline"` |
| **`readability_checker.py`** ⭐ | Analisar legibilidade de texto | `python scripts/readability_checker.py --file arquivo.txt` |
| **`content_repurposer.py`** ⭐ | Adaptar conteúdo entre plataformas | `python scripts/content_repurposer.py --file arquivo.txt --output todos` |
| **`hook_generator.py`** 🆕 | Gerar hooks virais para vídeos/posts | `python scripts/hook_generator.py "tema" plataforma quantidade` |
| **`content_idea_generator.py`** 🆕 | Gerar ideias de conteúdo por nicho | `python scripts/content_idea_generator.py nicho quantidade` |
| **`trend_tracker.py`** 🆕 | Monitorar tendências via APIs (Google, Reddit, YouTube, HN) | `python scripts/trend_tracker.py "termo" plataformas --formato tabela` |
| **`competitor_analyzer.py`** 🆕 | Analisar perfis de concorrentes e extrair insights | `python scripts/competitor_analyzer.py "@perfil1" "@perfil2" --plataforma instagram` |
| **`content_audit.py`** 🆕 | Auditar conteúdo existente e sugerir melhorias | `python scripts/content_audit.py arquivo.md --tipo blog --keyword "palavra"` |
| **`instagram_hashtag_research.py`** 🆕 | Pesquisa avançada de hashtags para Instagram (10 nichos, variantes, sets otimizados) | `python scripts/instagram_hashtag_research.py "nicho" --objetivo alcance` |
| **`hook_variant_generator.py`** 🆕 | Gerar múltiplas variantes de hooks para A/B testing (10 categorias, por nicho/formato) | `python scripts/hook_variant_generator.py "tema" --formato reels --nicho marketing` |
| **`reels_script_generator.py`** 🆕 | Gerar scripts completos para Reels com timestamps e direções de câmera | `python scripts/reels_script_generator.py "tema" 30 tutorial` |
| **`carousel_structure_generator.py`** 🆕 | Gerar estruturas de carrossel por tipo (8 formatos) | `python scripts/carousel_structure_generator.py "tema" educativo 7` |
| **`caption_generator.py`** 🆕 | Gerar legendas por objetivo (engajamento, vendas, storytelling) | `python scripts/caption_generator.py "tema" engajamento` |
| **`trend_adapter.py`** 🆕 | Adaptar trends virais para nichos específicos | `python scripts/trend_adapter.py "GRWM" marketing` |
| **`tiktok_trends_scraper.py`** 🆕 | Buscar vídeos virais do TikTok por nicho/hashtag/views | `python scripts/tiktok_trends_scraper.py --hashtag "marketing" --min-views 1000000` |

## Checklist de Qualidade

Antes de entregar qualquer conteúdo, verificar:

- [ ] Alinhado com objetivo e público-alvo do nicho
- [ ] Tom de voz consistente e apropriado
- [ ] CTA claro e acionável
- [ ] SEO otimizado (quando aplicável)
- [ ] Sem erros gramaticais
- [ ] Formatação correta para a plataforma
- [ ] Variações A/B incluídas (quando solicitado)
- [ ] Métricas de sucesso definidas
- [ ] Hashtags relevantes para o nicho
- [ ] Hook forte nos primeiros segundos/linhas ⭐
- [ ] Estrutura de retenção aplicada (vídeos) ⭐

## Entregáveis

Ao criar conteúdo, sempre entregar:

1. **Conteúdo principal** formatado para a plataforma
2. **Variações** (mínimo 2-3 quando possível)
3. **Recomendações** de otimização específicas para o nicho
4. **Métricas** sugeridas para acompanhamento
5. **Próximos passos** acionáveis
6. **Hashtags/Keywords** relevantes
7. **Prompts de IA** quando aplicável (imagens/vídeos) ⭐

## Ferramentas de IA Disponíveis ⭐ NOVO

### Para Imagens
| Ferramenta | Melhor Para | Referência |
|------------|-------------|------------|
| Nanobanana Pro | Imagens estilizadas, arte | [ai-tools-agent.md](subagents/ai-tools-agent.md) |
| GPT 1.5 | Imagens realistas, produtos | [ai-tools-agent.md](subagents/ai-tools-agent.md) |
| Midjourney | Arte conceitual, ilustrações | [ai-tools-agent.md](subagents/ai-tools-agent.md) |
| DALL-E 3 | Versatilidade, edição | [ai-tools-agent.md](subagents/ai-tools-agent.md) |

### Para Vídeos
| Ferramenta | Melhor Para | Referência |
|------------|-------------|------------|
| Veo 3.1 | Vídeos cinematográficos | [ai-tools-agent.md](subagents/ai-tools-agent.md) |
| Sora 2 | Narrativas complexas | [ai-tools-agent.md](subagents/ai-tools-agent.md) |
| Kling 2.6 | Movimento realista | [ai-tools-agent.md](subagents/ai-tools-agent.md) |
| Kling O1 | Reasoning visual | [ai-tools-agent.md](subagents/ai-tools-agent.md) |
| Seedance | Vídeos de dança, música | [ai-tools-agent.md](subagents/ai-tools-agent.md) |

## Exemplo de Uso Completo

```
Usuário: "Crie uma campanha completa de lançamento de um curso de IA"

Processo com Subagentes:

1. CONTENT CREATOR recebe briefing
   └── Nicho: IA, Tipo: Lançamento, Objetivo: Vendas

2. [RESEARCH AGENT] executa:
   ├── Análise de mercado de cursos de IA
   ├── Concorrência e posicionamento
   └── Personas do público-alvo

3. Consultar [workflows/lancamento-produto.md]
   └── Timeline de 30 dias + estrutura completa

4. [VIDEO AGENT] cria:
   ├── VSL de vendas
   ├── Reels de aquecimento
   └── YouTube de conteúdo educativo

5. [SOCIAL AGENT] planeja:
   ├── Posts de feed (Instagram, LinkedIn)
   ├── Stories de engajamento
   └── Calendário de 30 dias

6. [COPY AGENT] cria:
   ├── Headlines para landing page
   ├── Sequência de emails
   ├── Copy de anúncios
   └── CTAs otimizados

7. [AI TOOLS AGENT] gera:
   ├── Thumbnails (Midjourney/DALL-E)
   ├── Vídeos de demonstração (Veo 3.1)
   └── Assets visuais para ads

8. [ANALYTICS AGENT] define:
   ├── KPIs do lançamento
   ├── Métricas por fase
   └── Dashboard de acompanhamento

9. CONTENT CREATOR compila:
   ├── Pacote completo de lançamento
   ├── Cronograma de execução
   ├── Todos os assets organizados
   └── Checklist de implementação
```

## Quando Usar Cada Subagente

| Situação | Subagente | Por quê |
|----------|-----------|---------|
| Novo nicho/cliente | Research Agent | Entender mercado, concorrência, audiência |
| Artigo de blog | SEO Agent | Otimização on-page, keywords, estrutura |
| Copy de vendas | Copy Agent | Persuasão, headlines, CTAs |
| Post de Instagram | Social Agent | Formato, hashtags, timing |
| Lançamento de produto | Research + Copy + Video | Dados + copy + conteúdo visual |
| Calendário editorial | Research + Social | Tendências + planejamento |
| Landing page | SEO + Copy | Otimização + conversão |
| **Vídeo YouTube/Reels** ⭐ | Video Agent | Scripts, hooks, retenção |
| **Podcast** ⭐ | Audio Agent | Roteiros, estrutura, show notes |
| **Assets visuais IA** ⭐ | AI Tools Agent | Prompts otimizados, workflows |
| **Relatórios** ⭐ | Analytics Agent | Métricas, análise, otimização |
