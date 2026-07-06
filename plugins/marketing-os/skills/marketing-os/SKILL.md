---
name: marketing-os
description: "Use para produção de marketing digital: posts Instagram/LinkedIn/TikTok/Twitter, artigos SEO, email marketing, landing pages, anúncios Meta/Google Ads, calendários editoriais, vídeos YouTube/Reels/VSL, podcasts, geração de imagens e vídeos com IA, infoprodutos, testes A/B. NICHOS: Marketing Digital, IA, Dev Pessoal/Profissional, Tech, Empreendedorismo, Finanças, Saúde, Educação, Produtividade. TRIGGERS: conteúdo, post, blog, SEO, newsletter, copy, landing page, campanha, anúncio, carrossel, stories, reels, vídeo, podcast, design, imagem IA, infoproduto, teste A/B."
argument-hint: "[tipo-conteúdo] [nicho] [plataforma]"
---

# Marketing OS: Sistema Operacional de Marketing Digital

Este skill é um **orquestrador** para 18 especialistas de marketing. No Claude Code, ele usa subagents nativos. No Codex, ele usa a mesma arquitetura em modo compatível: roteia o briefing para o especialista correto, lê os arquivos Tier 1/Tier 2 necessários e, quando houver ferramenta de multi-agent disponível, pode paralelizar as etapas independentes.

## Modo de Operação: Orquestração por Ambiente

**REGRA FUNDAMENTAL**: Para qualquer pedido de produção de marketing (copy, SEO, research, social, ads, etc.), use o especialista certo antes de entregar.

- **Claude Code**: dispare o subagent especializado via `Agent(subagent_type: "mos-*")`.
- **Codex**: se houver ferramenta de multi-agent disponível, use-a para as etapas independentes. Se não houver, execute no agente principal lendo primeiro `agents/mos-*.md` e depois a knowledge base correspondente em `subagents/*-agent.md`.

Motivo: cada especialista tem contexto próprio, knowledge base profunda e output schema padronizado. O Codex não deve ignorar essa camada, mesmo quando precisar executar sem subagent nativo.

### Quando dispatch vs execução inline

| Situação | Ação |
|----------|------|
| Pedido claro de produção de peça (copy, post, artigo, anúncio, etc.) | Orquestração especializada |
| Pergunta conceitual sobre marketing (ex: "o que é AIDA?") | Responda inline (não precisa de agent) |
| Briefing amplo ("cria campanha completa") | Orquestração paralela de múltiplos especialistas |
| Pedido de informação sobre o próprio sistema | Inline |
| Briefing técnico/estratégico que requer pesquisa antes (ex: "qual canal pra B2B SaaS?") | Orquestre `mos-research` + `mos-growth` ou `mos-analytics` mesmo sem produzir peça final |

### Protocolo: briefing vago

Quando o usuário não fornece contexto suficiente, **NÃO chute** — pergunte antes de dispatchar. As 5 perguntas-chave (em paralelo, lista numerada na mesma resposta):

1. **Nicho** — qual área? (saúde, finanças, tech, educação, etc.)
2. **Avatar** — quem é o público? (cargo/profissão, faixa de renda, dor principal)
3. **Ticket** — preço do produto? (gratuito, low/mid/high-ticket)
4. **Plataforma** — onde vai publicar? (Instagram, LinkedIn, email, página web, etc.)
5. **Urgência** — publicar hoje, semana, planejamento futuro?

**Pule perguntas que já têm resposta:**
- Se há memory em `.claude/agent-memory/mos-*/` com briefing do cliente, use esse contexto
- Se o user já mencionou alguma dessas 5 dimensões na mensagem inicial, não pergunte de novo
- Se for óbvio do contexto (ex: pasta chamada "wellness-science" → nicho saúde)

### Memory opt-in

9 dos 18 agents têm `memory: project` no frontmatter e instruem persistir aprendizados em `.claude/agent-memory/mos-<agent>/MEMORY.md`:

`mos-copy`, `mos-funnel`, `mos-design`, `mos-brand`, `mos-launch`, `mos-research`, `mos-social`, `mos-infoproduct`, `mos-ads`

Memory é **opt-in**: o diretório `.claude/agent-memory/` está gitignored (memory é per-projeto, não distribuída pelo plugin). Pra ativar nesse projeto, rode uma vez:

```bash
python3 scripts/init_agent_memory.py
```

Isso cria os 9 arquivos `MEMORY.md` placeholder. Depois disso os agents passam a gravar/ler patterns transferíveis (não conteúdo bruto). Sem o bootstrap, os agents seguem funcionando normalmente — só não persistem memory entre sessões.

Quando dispatchar qualquer dos 9 agents acima e o memory estiver ativo, **explicite no prompt**: "considere memory existente do cliente neste projeto". Os outros 9 agents (`mos-analytics`, `mos-ai-tools`, `mos-audio`, `mos-email`, `mos-seo`, `mos-storytelling`, `mos-video`, `mos-growth`, `mos-ab-testing`) não têm memory — passe todos os inputs no prompt.

## Mapa de Dispatch (18 Agents)

| Briefing típico do usuário | Agent | Arquivo |
|----|----|----|
| "escreve headline / CTA / sales letter / microcopy" | `mos-copy` | `agents/mos-copy.md` |
| "cria artigo SEO / keyword research / on-page" | `mos-seo` | `agents/mos-seo.md` |
| "pesquisa tendências / concorrentes / audience / validar produto" | `mos-research` | `agents/mos-research.md` |
| "post Instagram / LinkedIn / TikTok / Twitter / cross-platform / bio Instagram / about / calendário editorial / planejamento de conteúdo / weekly plan" | `mos-social` | `agents/mos-social.md` |
| "roteiro YouTube / Reels / VSL / Shorts" | `mos-video` | `agents/mos-video.md` |
| "podcast / roteiro de áudio / spot / audiobook" | `mos-audio` | `agents/mos-audio.md` |
| "prompt para IA gerar imagem / vídeo" | `mos-ai-tools` | `agents/mos-ai-tools.md` |
| "direção criativa / paleta / tipografia / design spec" | `mos-design` | `agents/mos-design.md` |
| "métricas / relatório / análise de performance / dashboard" | `mos-analytics` | `agents/mos-analytics.md` |
| "sequência de email / newsletter / automação / subject line / drip" | `mos-email` | `agents/mos-email.md` |
| "campanha Meta Ads / Google Ads / TikTok Ads (completa)" | `mos-ads` | `agents/mos-ads.md` |
| "identidade de marca / posicionamento / tom de voz / manifesto da marca / arquétipo / brand guidelines" | `mos-brand` | `agents/mos-brand.md` |
| "storytelling / narrativa / arco de história / hero's journey aplicado em peça" | `mos-storytelling` | `agents/mos-storytelling.md` |
| "funil de vendas / sales funnel / jornada do cliente / TOFU MOFU BOFU" | `mos-funnel` | `agents/mos-funnel.md` |
| "growth hacking / aquisição / crescimento" | `mos-growth` | `agents/mos-growth.md` |
| "lançamento de produto / campanha de lançamento / PLF" | `mos-launch` | `agents/mos-launch.md` |
| "infoproduto / curso / ebook / membership / mentoria" | `mos-infoproduct` | `agents/mos-infoproduct.md` |
| "teste A/B / variação / otimização de conversão" | `mos-ab-testing` | `agents/mos-ab-testing.md` |

### Desempate: `mos-brand` vs `mos-storytelling`

Ambos tocam em "narrativa de marca". Regra:
- **`mos-brand`** quando o briefing é sobre **DEFINIR** a identidade — criar arquétipo, manifesto, voz/tom, brand book
- **`mos-storytelling`** quando é sobre **APLICAR** narrativa numa peça — estruturar uma sales letter com hero's journey, escrever uma origin story específica, construir arco em um vídeo/post

### Caso composto: páginas (landing / aplicação / vendas)

Briefings tipo **"cria página de aplicação"**, **"landing page"**, **"página de vendas"**, **"sales page"** **NÃO** mapeiam pra um único agent — eles disparam o workflow #5 abaixo (`mos-funnel` + `mos-copy` + `mos-design` em paralelo, depois eventual handoff a um builder técnico).

**REGRA CRÍTICA:** o marketing-os reivindica esse território. NÃO delegue direto a skills de frontend (ex: `frontend-design` do plugin oficial) sem antes rodar a camada estratégica do plugin. Caso contrário a página sai sem padrões de conversão BOFU, sem quality gates de copy, e sem direção visual de nicho.

## Padrões de Orquestração

Nos exemplos abaixo, `Agent(subagent_type: "mos-*")` é a sintaxe nativa do Claude Code. No Codex, trate cada chamada como uma etapa de roteamento: consulte o Tier 1 em `agents/mos-*.md`, aprofunde com o Tier 2 em `subagents/*-agent.md`, rode scripts determinísticos quando fizer sentido e consolide o resultado no protocolo de entrega.

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

### 5. Workflow: Página de Aplicação / Landing / Vendas (BOFU)

Para briefings tipo "cria página de aplicação", "landing page", "página de vendas", "sales page". O marketing-os **DEVE** orquestrar a camada estratégica antes de qualquer build técnico.

```
Fase 1 (paralelo, single message com 3 Agent calls):
  - Agent(subagent_type: "mos-funnel", prompt: "estruturar página BOFU para [produto/avatar]: CTA placement, escassez, anti-avatar, FAQ, prova social, stack value")
  - Agent(subagent_type: "mos-copy", prompt: "revisar/melhorar copy fornecida [se houver: colar copy do PDF/DOCX], aplicar quality gates globais, sugerir variações de headline/CTA")
  - Agent(subagent_type: "mos-design", prompt: "direção visual para página BOFU em [nicho]: paleta, tipografia, hierarquia, mood, exemplos de referência")

Fase 2 (sequencial — depende dos outputs da Fase 1):
  - Consolidar os 3 outputs num brief único (estrutura + copy revisada + design spec)
  - SE o usuário pediu HTML/CSS de fato → delegar à skill `frontend-design` (plugin oficial Anthropic) com o brief consolidado como input
  - SE o usuário pediu só specs (sem código) → parar na Fase 1 e entregar o brief

Fase 3: Quality gates globais sobre o output final + sugestões de teste A/B (mos-ab-testing opcional)
```

**Por que essa ordem importa:**
- Sem `mos-funnel`: estrutura sai genérica, sem padrões BOFU comprovados (escassez, anti-avatar, stack value)
- Sem `mos-copy`: copy entregue não passa pelos quality gates (travessão, "brutal", CAPS), e oportunidade de melhoria fica em cima da mesa
- Sem `mos-design`: visual sai com cara genérica de template, não de nicho premium
- `frontend-design` é excelente em build técnico, mas não conhece padrões de conversão — é executor da Fase 2, não decisor da Fase 1

**Quando usar memory de contexto:** se a pasta atual já tem `.claude/agent-memory/mos-copy/` ou `.claude/agent-memory/mos-funnel/` com briefings/feedback de cliente anteriores (criados via `python3 scripts/init_agent_memory.py`), explicite isso no prompt do Fase 1 ("considere memory existente do cliente").

### 6. Workflow: Webinar (live ou perpetual)

Triggers: "monta um webinar", "webinar de vendas pra X", "webinar funnel".

```
Fase 1 (paralelo, single message):
  - Agent(subagent_type: "mos-launch", prompt: "estratégia de webinar [live/perpetual] para [produto]: posicionamento da oferta, pitch timing, escassez")
  - Agent(subagent_type: "mos-funnel", prompt: "funil de webinar: registro → confirmação → reminder → live → reposicionamento → encerramento; pontos de queda esperados")
  - Agent(subagent_type: "mos-video", prompt: "estrutura do webinar de [duração] minutos: hook, pitch, agenda, conteúdo de valor, transição pra oferta, garantia, FAQ ao vivo")

Fase 2 (sequencial, depende dos 3 outputs):
  - Agent(subagent_type: "mos-copy", prompt: "página de registro + headline + 3 emails (registro/reminder/no-show) com base no posicionamento da Fase 1")
  - Agent(subagent_type: "mos-email", prompt: "sequência completa de webinar: 4 emails pré, 1 lembrete dia, 3 emails pós-webinar (replay → últimas vagas → encerramento)")

Fase 3: Quality gates + recomendação de tracking (mos-analytics opcional pra setup de eventos)
```

**Por que essa ordem:** sem `mos-launch` o webinar não tem estratégia de oferta (vira aula sem venda). Sem `mos-funnel` cada step do funil sai isolado. Sem `mos-video` o roteiro não respeita ciência de retenção. Os Fase 2 (copy + email) dependem de saber QUAL é a oferta e onde está o pitch — por isso sequencial.

### 7. Workflow: Lançamento de Infoproduto

Triggers: "vou lançar um curso", "lançamento de infoproduto", "criar e lançar [produto digital]".

```
Fase 1 (paralelo):
  - Agent(subagent_type: "mos-research", prompt: "validação de mercado: tamanho do nicho, concorrentes, ticket médio praticado, dores não atendidas")
  - Agent(subagent_type: "mos-brand", prompt: "posicionamento e voz da marca/expert para o produto") — só se marca nova ou pivô
  - Agent(subagent_type: "mos-infoproduct", prompt: "estrutura do infoproduto: módulos, formato (curso/membership/mentoria), pricing strategy, bônus")

Fase 2 (sequencial — depende da estrutura definida na Fase 1):
  - Agent(subagent_type: "mos-launch", prompt: "estratégia de lançamento (PLF / semente / relâmpago / perpétuo) baseada no produto e nicho")
  - Agent(subagent_type: "mos-funnel", prompt: "funil completo: TOFU (CPL/anúncios) → MOFU (lead magnet/webinar) → BOFU (página de vendas/aplicação)")

Fase 3 (paralelo, depende da estratégia de lançamento):
  - Agent(subagent_type: "mos-copy", prompt: "página de vendas + headlines + CTAs alinhados com promessa do produto e estratégia de lançamento")
  - Agent(subagent_type: "mos-email", prompt: "sequência completa de pré-lançamento + abertura de carrinho + última chamada")
  - Agent(subagent_type: "mos-ads", prompt: "campanhas de tráfego pra cada fase do lançamento: pré (lista) + durante (conversão) + retargeting")

Fase 4: Quality gates + setup de tracking + plano de teste A/B (mos-ab-testing)
```

**Por que esse encadeamento:** lançamento não é peça única — é orquestração de estratégia + estrutura + funil + execução. Pular fase 1 (research) é o erro #1 de quem lança no escuro. Pular fase 2 (escolha de modelo de lançamento) é o erro #2 de copiar PLF sem entender se cabe.

### 8. Workflow: Carrossel Completo (Instagram / LinkedIn)

Triggers: "cria carrossel sobre X", "carrossel Instagram pra [tema]".

```
Fase 1 (paralelo, single message):
  - Agent(subagent_type: "mos-social", prompt: "estrutura de carrossel pra [plataforma]: número ideal de slides, hook na capa, padrão de retenção entre slides, CTA final")
  - Agent(subagent_type: "mos-copy", prompt: "texto de cada slide: hook na capa, body com peso/leveza alternada, CTA específico — quality gates aplicados")
  - Agent(subagent_type: "mos-design", prompt: "direção visual: paleta, tipografia, hierarquia, formato de capa vs body, consistência visual entre slides")

Fase 2 (opcional, paralelo com Fase 1):
  - Agent(subagent_type: "mos-ai-tools", prompt: "prompts pra IA gerar imagem da capa (Midjourney/Flux/Ideogram) com referência da Fase 1 design")

Fase 3: Consolidação (texto + design spec + prompts) + caption + hashtags + sugestão de enquete obrigatória
```

**Por que: ** carrossel é o formato que mais sofre quando feito por 1 agent só. `mos-social` sem `mos-copy` = texto fraco. `mos-copy` sem `mos-design` = visual genérico. `mos-design` sem `mos-social` = sem entender ritmo de retenção da plataforma.

### 9. Workflow: VSL Completa (Video Sales Letter)

Triggers: "cria VSL pra [produto]", "roteiro de VSL", "video sales letter".

```
Fase 1 (paralelo):
  - Agent(subagent_type: "mos-storytelling", prompt: "arco narrativo da VSL: hook → problema → vilão → solução → prova → oferta → urgência. Frameworks: hero's journey adaptado pra venda")
  - Agent(subagent_type: "mos-copy", prompt: "estrutura de copy de venda no formato VSL: headline, big idea, mecanismo único, anti-avatar, stack value, garantia, FAQ falado")
  - Agent(subagent_type: "mos-video", prompt: "ciência de retenção em VSL: timestamps de queda esperados, transições, B-roll, ritmo, duração ideal por nicho/ticket")

Fase 2: Consolidação em roteiro único (texto narrado + cues visuais + timing de seções)

Fase 3: Quality gates (incluindo gates de substância: promessas com backup, garantia clara) + sugestão de testes A/B em hook e mecanismo único
```

**Por que: ** VSL é o caso clássico de copy + storytelling + ciência de vídeo precisarem casar. Falta de qualquer um quebra a peça toda.

### 10. Workflow: Análise de Concorrente + Clone de Estratégia

Triggers: "analisa @fulano e clona", "engenharia reversa do [concorrente]", "como o [expert] vende?".

```
Fase 1 (paralelo):
  - Agent(subagent_type: "mos-research", prompt: "mapeamento completo: produtos, ticket, posicionamento, fontes de tráfego, conteúdo orgânico, ads ativos, depoimentos. WebSearch + análise de perfis públicos")
  - Agent(subagent_type: "mos-brand", prompt: "extrair positioning, arquétipo, voz/tom do concorrente analisado a partir de samples reais — gerar brand spec replicável")

Fase 2 (sequencial, depende da Fase 1):
  - Agent(subagent_type: "mos-copy", prompt: "voice clone: extrair padrões de copy do concorrente (estruturas de headline, padrões de CTA, vocabulário, ritmo). Aplicar nos assets/clones/ se for um copywriter conhecido (Halbert, Hopkins, etc.). Gerar samples adaptados pra cliente atual")

Fase 3: Brief consolidado de "estratégia clonada e adaptada" + checklist de o-que-replicar / o-que-evitar / oportunidades de diferenciação
```

**Por que: ** clone sem `mos-research` é cópia rasa. Sem `mos-brand` é só pegar headlines (sem entender posicionamento). Sem `mos-copy` é análise sem aplicação prática.

## Quality Gates Globais (aplicam SEMPRE)

Mesmo os subagents já aplicarem seus próprios gates, valide sempre antes de entregar ao usuário:

### Palavras e Símbolos Proibidos

| Item | Ação |
|------|------|
| `—` (travessão longo) | substituir por `.` `,` `:` ou quebrar frase |
| "brutal" | usar: intenso, forte, pesado, impactante, poderoso |
| Antítese negação→afirmação ("Não é X / É Y", "Não faça X / Faça Y") | reescrever afirmando direto, sem o paralelo |
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

### Substância (peças de venda/conversão)

Para qualquer copy de venda, anúncio, sales letter, página de aplicação, VSL, email de oferta:

| Item | Como verificar |
|------|----------------|
| Promessas sem backup | Tem prova social/case/dado citável? Senão, suavizar ou cortar |
| Comparativo competitivo | Citou concorrente direto? Tem fundamento factual ou é especulativo? |
| Garantia | Promessa de garantia tem termo claro (período, condições)? |
| Linguagem absoluta | Evitar "garantido", "100%", "todos", "sempre" sem qualificador |
| Placeholder publicado | Sem "XXX", "X reais", "Lorem ipsum" — checar antes de entregar |

### Compliance regulatório (saúde / finanças / suplementos)

Aplicar SEMPRE quando o nicho envolve. Detectar via memory do cliente, pasta atual, ou pergunta-chave #1.

| Nicho | Órgão | Regras-chave |
|-------|-------|--------------|
| Saúde / médico / dental / nutrição | **CFM/CRM, CONAR** | Disclaimer "resultados variam" em depoimentos; proibido "cura"/"tratamento" sem registro; CRM visível em médicos |
| Suplementos / produtos naturais | **ANVISA** | Não pode prometer cura, tratar doença, dosagem específica sem registro; só "auxilia/contribui" |
| Finanças / investimentos | **CVM** | "Rentabilidade passada não garante futura" obrigatório; sem promessa de retorno; risco explícito |
| Cosméticos / dermato | **ANVISA** | Sem prometer tratar doença de pele; "pode auxiliar" é o limite |

Quando o briefing entrar nesses nichos, o orquestrador adiciona disclaimer apropriado em qualquer peça final, sem perguntar.

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

## Entregáveis Padrão (contextuais)

**Sempre:**
1. Conteúdo principal formatado
2. Próximos passos acionáveis (ex: "testar variação B em 7 dias", "publicar em horário X")

**Quando faz sentido testar:**
3. 2-3 variações A/B (copy, headlines, CTAs, hooks)

**Condicionais:**
4. **Hashtags / keywords** — apenas se for conteúdo de social ou SEO
5. **Prompts de IA** — apenas se envolveu `mos-ai-tools` ou geração de imagem/vídeo
6. **Métricas sugeridas** — apenas se é peça de conversão/campanha (não pra peça artística/branded)
7. **Recomendações de otimização** — sempre que cabível
8. **Enquete para engajamento** — OBRIGATÓRIO em conteúdos de redes sociais (Reels, posts, carrosséis, stories)
9. **Disclaimer regulatório** — OBRIGATÓRIO em peças de saúde/finanças/suplementos (ver "Compliance regulatório")

## Política de delegação a skills externas

Quando os subagents do marketing-os terminam sua parte, alguns outputs podem precisar de skills externas pra produzir o entregável final. Política:

| Saída do marketing-os | Skill externa válida pra delegar | Quando |
|---|---|---|
| Brief de página BOFU consolidado | `frontend-design` (plugin oficial Anthropic) | Quando user pediu HTML/CSS de fato |
| Design spec | `figma-implement-design` ou `figma-generate-design` | Quando user quer Figma e não código |
| Conteúdo final pra entregável Office | `docx` / `pptx` / `xlsx` (Anthropic Skills) | Quando user quer Word/PowerPoint/Excel pronto |
| Código de integração API/SDK | `claude-api` | Quando user quer integrar produto com API Anthropic |

**REGRA:** delegação acontece **DEPOIS** dos workflows do marketing-os, **nunca antes**. O marketing-os entrega brief estratégico/copy/design; skills externas executam o build técnico. Inverter a ordem é o bug que originou o workflow #5 (página de aplicação).

## Slash commands rápidos

38 commands em `commands/` são atalhos pra workflows comuns. Quando user invoca o command direto (ex: `/criar-carrossel`), segue a lógica do command file. Quando user pede em linguagem natural ("cria um carrossel sobre X"), este SKILL dispatcha conforme tabela e workflows acima.

| Categoria | Commands |
|---|---|
| Meta-orquestrador | `/mo` (briefing aberto, roteia automaticamente pro command apropriado) |
| Conteúdo social | `/criar-post`, `/criar-carrossel`, `/criar-calendario` |
| Copy | `/otimizar-copy` (diagnóstico + score + reescrita de copy existente) |
| Vídeo/áudio | `/criar-video`, `/criar-podcast`, `/narrar-roteiro` |
| Páginas/funis | `/criar-landing-page`, `/criar-funil`, `/criar-webinar` |
| Email | `/criar-email`, `/criar-sequencia` |
| Ads | `/criar-anuncio`, `/publicar-anuncio` |
| Infoproduto | `/criar-infoproduto` |
| Voice clones | `/criar-clone` (expert externo via web research), `/criar-meu-clone` (suas amostras locais em `workspace/`) |
| Análise | `/analisar-concorrencia`, `/analisar-video`, `/clonar-estrategia`, `/auditoria`, `/auditoria-pro` |
| Visual | `/criar-brief-design`, `/gerar-imagem`, `/capturar-tela` |
| Operação | `/batch`, `/criar-artigo`, `/publicar-notion`, `/projeto`, `/datas-sazonais` |
| Campanhas (presets) | `/campanha` (índice), `/campanha-lancamento`, `/campanha-prospeccao`, `/campanha-retencao`, `/campanha-autoridade`, `/campanha-growth`, `/campanha-black-friday` |

## Arquitetura (two-tier)

- **Tier 1** (`agents/mos-*.md`): system prompts enxutos (~250 linhas) com dispatch protocol, output schema, quality gates. Carregados pelo Claude Code automaticamente quando sessão abre.
- **Tier 2** (`subagents/*-agent.md`): knowledge base profunda (~3500 linhas cada) com frameworks, cases, tabelas, exemplos. Lida sob demanda via Read pelos agents tier-1.

Isso mantém contextos dos agents leves, carrega profundidade só quando precisa, e permite evoluir knowledge sem mexer no dispatch.

## Versão

Versão atual em `.claude-plugin/plugin.json`. Histórico em `CHANGELOG.md`. Migração da v5 (squad) → v6 (native subagents) documentada em `docs/architecture/subagents-migration.md`.
