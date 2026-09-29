---
name: marketing-os
description: "Marketing digital completo em PT-BR para o mercado brasileiro. Use para criar ou revisar posts, carrosséis e calendários (Instagram, LinkedIn, TikTok, Threads), roteiros de vídeo, Reels e VSL, podcasts, emails e sequências, anúncios (Meta, Google, TikTok), artigos SEO, landing pages e funis. Também para estratégia: avatar e persona, USP e posicionamento, oferta com value stack, preço e garantia, lançamento de infoproduto, pesquisa de mercado e concorrentes, testes A/B, growth, métricas e aprendizado com resultados, respostas a comentários e prospecção de creators. Gatilhos: conteúdo, post, copy, headline, anúncio, campanha, lançamento, funil, oferta, avatar, persona, USP, SEO, email, vídeo, Reels, landing page, métricas, concorrência."
---

# Marketing OS: Sistema Operacional de Marketing Digital

> As pastas `subagents`, `scripts`, `assets`, `references`, `workflows` e `docs` citadas aqui e dentro das knowledge bases ficam na raiz do plugin, nunca no diretório do projeto do usuário.

Este skill é um **orquestrador** para 21 especialistas de marketing. No Claude Code, ele usa subagents nativos. No ChatGPT Work e no Codex, ele usa a mesma arquitetura em modo compatível: roteia o briefing para o especialista correto, lê os arquivos Tier 1/Tier 2 necessários e, quando houver ferramenta de multi-agent disponível, pode paralelizar as etapas independentes.

## Modo de Operação: Orquestração por Ambiente

**REGRA FUNDAMENTAL**: Para qualquer pedido de produção de marketing (copy, SEO, research, social, ads, etc.), use o especialista certo antes de entregar.

- **Claude Code**: dispare o subagent especializado via `Agent(subagent_type: "mos-*")`.
- **ChatGPT Work**: preserve a intenção escolhida por `@Marketing OS`, remova esse prefixo antes de classificar o briefing e aplique o mesmo mapa de dispatch. Leia `agents/mos-*.md` e `subagents/*-agent.md` sob demanda. Use multi-agent e scripts somente quando o host oferecer essas ferramentas; caso contrário, execute no agente principal e declare qualquer validação que não pôde ser rodada.
- **Codex**: se houver ferramenta de multi-agent disponível, use-a para as etapas independentes. Se não houver, execute no agente principal lendo primeiro `agents/mos-*.md` e depois a knowledge base correspondente em `subagents/*-agent.md`.

Motivo: cada especialista tem contexto próprio, knowledge base profunda e output schema padronizado. ChatGPT Work e Codex devem preservar essa camada mesmo quando precisarem executar sem subagent nativo.

## Invocação no ChatGPT Work

O plugin funciona em conversas **Work** com o Marketing OS instalado. O usuário pode descrever o resultado diretamente ou selecionar o plugin com `@Marketing OS`.

- Trate `@Marketing OS` como seleção do plugin e classifique o texto restante como briefing.
- Pedidos como `@Marketing OS crie um avatar completo`, `crie uma USP` e `estruture minha oferta` seguem os mesmos contratos de `/criar-avatar`, `/criar-usp` e `/criar-oferta`.
- Quando a interface não expuser slash commands, mapeie a intenção para o command correspondente e aplique seu decision tree, output schema e quality gates.
- Leia apenas o Tier 1 e o Tier 2 dos especialistas necessários. Evite carregar as 21 knowledge bases para um pedido de domínio único.
- Scripts Python são aceleradores determinísticos. Se o host não oferecer shell ou Python, cumpra o contrato por raciocínio e informe quais checks automatizados ficaram indisponíveis.

### Quando dispatch vs execução inline

| Situação | Ação |
|----------|------|
| Pedido claro de produção de peça (copy, post, artigo, anúncio, etc.) | Orquestração especializada |
| Pergunta conceitual sobre marketing (ex: "o que é AIDA?") | Responda inline (não precisa de agent) |
| Briefing amplo ("cria campanha completa") | Orquestração paralela de múltiplos especialistas |
| Pedido de informação sobre o próprio sistema | Inline |
| Briefing técnico/estratégico que requer pesquisa antes (ex: "qual canal pra B2B SaaS?") | Orquestre `mos-research` + `mos-growth` ou `mos-analytics` mesmo sem produzir peça final |

### Protocolo: briefing vago

Quando o usuário não fornece contexto suficiente, **NÃO chute**: pergunte antes de dispatchar. As 5 perguntas-chave (em paralelo, lista numerada na mesma resposta):

1. **Nicho**: qual área? (saúde, finanças, tech, educação, etc.)
2. **Avatar**: quem é o público? (cargo/profissão, faixa de renda, dor principal)
3. **Ticket**: preço do produto? (gratuito, low/mid/high-ticket)
4. **Plataforma**: onde vai publicar? (Instagram, LinkedIn, email, página web, etc.)
5. **Urgência**: publicar hoje, semana, planejamento futuro?

**Pule perguntas que já têm resposta:**
- Se existir `workspace/brand/perfil.md` no projeto (criado por `/configurar-marca`), ele responde nicho, avatar, ticket e plataforma; pergunte só o que faltar. Num projeto recorrente sem perfil, ofereça `/configurar-marca` uma vez
- Se há memory em `.claude/agent-memory/marketing-os-mos-*/` com briefing do cliente, use esse contexto
- Se o user já mencionou alguma dessas 5 dimensões na mensagem inicial, não pergunte de novo
- Se for óbvio do contexto (ex: pasta chamada "wellness-science" → nicho saúde)

### Memory opt-in

Todos os 21 agents têm `memory: project` no frontmatter e instruem persistir aprendizados em `.claude/agent-memory/marketing-os-mos-<agent>/MEMORY.md`.

Memory é **opt-in**: o diretório `.claude/agent-memory/` está gitignored (memory é per-projeto, não distribuída pelo plugin). Pra ativar nesse projeto, rode uma vez:

```bash
python3 scripts/init_agent_memory.py
```

Isso cria os arquivos `MEMORY.md` no diretório nativo de cada agent e migra o legado `mos-*/` sem perda (ADR-0006). A plataforma injeta o início desse arquivo no agent a cada sessão; os agents gravam patterns transferíveis (não conteúdo bruto) via `memory_writer.py`.

Quando dispatchar qualquer agent com memory ativo no projeto, **explicite no prompt**: "considere memory existente do cliente neste projeto".

### Pedidos de manutenção do plugin (execute direto, sem dispatch)

| O usuário pede | Rode |
|---|---|
| "inicialize a memória do Marketing OS neste projeto" | `python3 scripts/init_agent_memory.py` |
| "rode o diagnóstico de instalação do Marketing OS", "qual versão está ativa" | `python3 scripts/install_doctor.py` |
| "os fatos de plataforma estão em dia?" | `python3 scripts/check_platform_facts.py` |

## Mapa de Dispatch (21 Agents)

| Briefing típico do usuário | Agent | Arquivo |
|----|----|----|
| "escreve headline / CTA / sales letter / microcopy" | `mos-copy` | `agents/mos-copy.md` |
| "cria artigo SEO / keyword research / on-page" | `mos-seo` | `agents/mos-seo.md` |
| "pesquisa tendências / concorrentes / audience / validar produto" | `mos-research` | `agents/mos-research.md` |
| "cria avatar completo / cliente ideal / buyer persona / ICP / anti-avatar" ou `/criar-avatar` | `mos-research` | `agents/mos-research.md` |
| "post Instagram / LinkedIn / TikTok / Twitter / cross-platform / bio Instagram / about / calendário editorial / planejamento de conteúdo / weekly plan" | `mos-social` | `agents/mos-social.md` |
| "roteiro YouTube / Reels / VSL / Shorts" | `mos-video` | `agents/mos-video.md` |
| "podcast / roteiro de áudio / spot / audiobook" | `mos-audio` | `agents/mos-audio.md` |
| "prompt para IA gerar imagem / vídeo" | `mos-ai-tools` | `agents/mos-ai-tools.md` |
| "direção criativa / paleta / tipografia / design spec" | `mos-design` | `agents/mos-design.md` |
| "métricas / relatório / análise de performance / dashboard" | `mos-analytics` | `agents/mos-analytics.md` |
| "sequência de email / newsletter / automação / subject line / drip" | `mos-email` | `agents/mos-email.md` |
| "campanha Meta Ads / Google Ads / TikTok Ads (completa)" | `mos-ads` | `agents/mos-ads.md` |
| "identidade de marca / posicionamento / tom de voz / manifesto da marca / arquétipo / brand guidelines" | `mos-brand` | `agents/mos-brand.md` |
| "cria USP / UVP / proposta única de venda / proposta de valor / diferencial da oferta" ou `/criar-usp` | `mos-brand` | `agents/mos-brand.md` |
| "storytelling / narrativa / arco de história / hero's journey aplicado em peça" | `mos-storytelling` | `agents/mos-storytelling.md` |
| "funil de vendas / sales funnel / jornada do cliente / TOFU MOFU BOFU" | `mos-funnel` | `agents/mos-funnel.md` |
| "growth hacking / aquisição / crescimento" | `mos-growth` | `agents/mos-growth.md` |
| "lançamento de produto / campanha de lançamento / PLF" | `mos-launch` | `agents/mos-launch.md` |
| "infoproduto / curso / ebook / membership / mentoria" | `mos-infoproduct` | `agents/mos-infoproduct.md` |
| "oferta / value stack / precificação / quanto cobrar / garantia / bônus / order bump" | `mos-offer` | `agents/mos-offer.md` |
| "responder comentários / DMs / moderação / haters / caixa de perguntas / gestão de comentários" | `mos-community` | `agents/mos-community.md` |
| "parceria / influenciador / creator / collab / permuta / embaixador / prospectar creators / outreach" | `mos-partnerships` | `agents/mos-partnerships.md` |
| "teste A/B / variação / otimização de conversão" | `mos-ab-testing` | `agents/mos-ab-testing.md` |

### Rota condicional: USP e UVP

Pedidos de USP usam o contrato de `/criar-usp`:

- Público/JTBD, alternativas e provas mapeados: dispatch simples para `mos-brand`.
- Faltam público validado, contexto competitivo, alternativas ou claims atuais:
  dispatch sequencial `mos-research` seguido de `mos-brand`.
- USP já aprovada e pedido limitado a uma peça: `mos-copy` adapta a proposta sem
  redefini-la.

O `mos-brand` formula, pontua e valida a proposta central. O `mos-offer` usa essa
proposta para estruturar promessa, mecanismo, preço, garantia, bônus e value
stack. O `mos-copy` transforma a proposta aprovada em mensagem para uma peça.
Quando o briefing mistura as etapas, preserve a dependência:
`mos-research` seguido de `mos-brand`, depois `mos-offer` e por fim `mos-copy`.

### Desempate: `mos-brand` vs `mos-storytelling`

Ambos tocam em "narrativa de marca". Regra:
- **`mos-brand`** quando o briefing é sobre **DEFINIR** a identidade: criar arquétipo, manifesto, voz/tom, brand book
- **`mos-storytelling`** quando é sobre **APLICAR** narrativa numa peça: estruturar uma sales letter com hero's journey, escrever uma origin story específica, construir arco em um vídeo/post

### Rota condicional: Oferta

Pedidos de arquitetura comercial usam o contrato de `/criar-oferta`:

- Produto ou entrega ainda indefinidos: `mos-infoproduct` antes de `mos-offer`.
- Oferta core ou high-ticket sem research de público e mercado: `mos-research`
  seguido de `mos-offer`.
- Research e dados suficientes já fornecidos: dispatch simples para `mos-offer`.
- Dossiê de USP disponível: passe o Handoff Context integral e preserve versão,
  proposta principal, reason to believe, mecanismo, IDs, limites e hipóteses.
- Pedido inclui página, anúncio ou email: `mos-offer` seguido de `mos-copy`, pois
  a mensagem depende da arquitetura aprovada.

O output de oferta inclui Protocolo de Evidências, Claims Aprovados, Claims
Bloqueados e Plano de Validação. Agentes consumidores preservam esses campos no
handoff.

### Desempate: `mos-offer` vs `mos-copy` vs `mos-infoproduct` vs `mos-funnel`

Briefings de "oferta" tocam 4 domínios. Regra pelo substantivo do pedido:

- **`mos-offer`**: estruturar a OFERTA em si (o que entra, preço, garantia, bônus, condições, "quanto cobrar")
- **`mos-copy`**: ESCREVER a peça que vende a oferta (página, anúncio, email); consome o handoff do offer
- **`mos-infoproduct`**: o PRODUTO entregue (curriculum, módulos, formato de entrega)
- **`mos-funnel`**: ONDE cada oferta entra na jornada (tripwire vs core vs upsell como sequência de funil)

Pedido composto "cria a oferta e a página": sequencial `mos-offer` → `mos-copy`, nunca paralelo (a página depende do stack fechado).

### Desempate: `mos-community` vs `mos-social`

Ambos tocam em redes sociais. Regra:
- **`mos-social`**: CRIAR conteúdo novo (post, carrossel, calendário, legenda, bio)
- **`mos-community`**: RESPONDER interações existentes (comentários, DMs, moderação, triagem de haters)

Pedido "responde os comentários do meu último reels" → `mos-community`, não `mos-social`.

### Desempate: `mos-partnerships` vs `mos-research`

Ambos pesquisam mercado e audiência. Regra:
- **`mos-research`**: analisar mercado, tendências, concorrentes, validar nicho (output = research brief)
- **`mos-partnerships`**: fechar parceria com creator (output = shortlist + fit score + rascunhos de outreach acionáveis)

Pedido composto "acha influencers e manda mensagem": sequencial `mos-research` → `mos-partnerships`. Sourcing sem outreach é só research; outreach sem validação de fit é só partnerships com lista fornecida.

### Caso composto: páginas (landing / aplicação / vendas)

Briefings tipo **"cria página de aplicação"**, **"landing page"**, **"página de vendas"**, **"sales page"** **NÃO** mapeiam pra um único agent: eles disparam o workflow #5 abaixo (`mos-funnel` + `mos-copy` + `mos-design` em paralelo, depois eventual handoff a um builder técnico).

**REGRA CRÍTICA:** o marketing-os reivindica esse território. NÃO delegue direto a skills de frontend (ex: `frontend-design` do plugin oficial) sem antes rodar a camada estratégica do plugin. Caso contrário a página sai sem padrões de conversão BOFU, sem quality gates de copy, e sem direção visual de nicho.

## Padrões de Orquestração

Nos exemplos abaixo, `Agent(subagent_type: "mos-*")` é a sintaxe nativa do Claude Code. No ChatGPT Work e no Codex, trate cada chamada como uma etapa de roteamento: consulte o Tier 1 em `agents/mos-*.md`, aprofunde com o Tier 2 em `subagents/*-agent.md`, rode scripts determinísticos quando fizer sentido e consolide o resultado no protocolo de entrega. Profundidade adicional de alguns workflows mora em `workflows/` (arquivos standalone).

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

### 5 a 10. Workflows compostos: siga o command

Estes workflows têm contrato completo no command correspondente: fases, prompts de dispatch, consolidação e o porquê de cada agent. Em linguagem natural, reconheça o gatilho e siga o command. No ChatGPT Work e no Codex, leia o command e execute o mesmo contrato.

| # | Gatilho | Command (contrato) | Agents |
|---|---|---|---|
| 5 | página de aplicação, landing page, página de vendas | `/criar-landing-page` | funnel + copy + design; build técnico só depois |
| 6 | webinar ao vivo ou perpétuo | `/criar-webinar` | launch + funnel + video; depois copy + email |
| 7 | lançar curso, lançamento de infoproduto | `/criar-infoproduto`; campanha inteira: `/campanha-lancamento` | research + brand + infoproduct; launch + funnel; copy + email + ads |
| 8 | carrossel completo | `/criar-carrossel` | social + copy + design (+ ai-tools) |
| 9 | VSL | `/criar-video` | storytelling + copy + video |
| 10 | analisar e clonar a estratégia de um concorrente ou expert | `/clonar-estrategia` | research + brand; depois copy |

Regras que valem para todos:

- Estratégia antes de build: quando a peça pede HTML/CSS de fato, o brief consolidado dos agents vai para a skill de frontend. Sem pedido de código, entregue o brief.
- Com memória do cliente no projeto (`.claude/agent-memory/marketing-os-mos-*/`), diga no prompt de cada fase: "considere memory existente do cliente".

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
| Placeholder publicado | Sem "XXX", "X reais", "Lorem ipsum"; checar antes de entregar |

### Compliance regulatório (saúde / finanças / suplementos)

Aplicar SEMPRE quando o nicho envolve. Detectar via memory do cliente, pasta atual, ou pergunta-chave #1.

| Nicho | Órgão | Regras-chave |
|-------|-------|--------------|
| Medicina | **CFM/CRM, CONAR** | Disclaimer "resultados variam" em depoimentos; proibido "cura"/"tratamento" sem registro; CRM visível |
| Odontologia | **CFO/CRO, CONAR** | CRO visível; sem promessa de resultado garantido |
| Nutrição | **CFN/CRN, CONAR** | CRN visível; sem prescrição individual em conteúdo genérico |
| Psicologia | **CFP/CRP** | CRP visível; sem promessa de cura ou resultado |
| Advocacia | **OAB** | Publicidade só informativa: sem captação de clientela nem promessa de resultado |
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
Scripts Python determinísticos e o CLI unificado `mos.py`. Os agents com acesso a `Bash` podem invocar:
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
4. **Hashtags / keywords**: apenas se for conteúdo de social ou SEO
5. **Prompts de IA**: apenas se envolveu `mos-ai-tools` ou geração de imagem/vídeo
6. **Métricas sugeridas**: apenas se é peça de conversão/campanha (não pra peça artística/branded)
7. **Recomendações de otimização**: sempre que cabível
8. **Enquete para engajamento**: OBRIGATÓRIO em conteúdos de redes sociais (Reels, posts, carrosséis, stories)
9. **Disclaimer regulatório**: OBRIGATÓRIO em peças de saúde/finanças/suplementos (ver "Compliance regulatório")

## Política de delegação a skills externas

Quando os subagents do marketing-os terminam sua parte, alguns outputs podem precisar de skills externas pra produzir o entregável final. Política:

| Saída do marketing-os | Skill externa válida pra delegar | Quando |
|---|---|---|
| Brief de página BOFU consolidado | `frontend-design` (plugin oficial Anthropic) | Quando user pediu HTML/CSS de fato |
| Design spec | `figma-implement-design` ou `figma-generate-design` | Quando user quer Figma e não código |
| Conteúdo final pra entregável Office | `docx` / `pptx` / `xlsx` (Anthropic Skills) | Quando user quer Word/PowerPoint/Excel pronto |
| Código de integração API/SDK | `claude-api` | Quando user quer integrar produto com API Anthropic |

**REGRA:** delegação acontece **DEPOIS** dos workflows do marketing-os, **nunca antes**. O marketing-os entrega brief estratégico/copy/design; skills externas executam o build técnico. Inverter a ordem é o bug que originou o workflow #5 (página de aplicação).

## Slash commands: qual usar para cada necessidade

Tabela canônica de roteamento por command; o `/mo` usa esta tabela. Quando o usuário invoca o command direto, siga o arquivo do command. Em linguagem natural, escolha pela tabela e, se nenhum command encaixar, despache o agent pelo Mapa de Dispatch.

| Necessidade | Command | Observação |
|---|---|---|
| Não sei qual usar | `/mo` | Meta-orquestrador: classifica o briefing e diz qual rota escolheu |
| Configurar o perfil de marca do projeto | `/configurar-marca` | Uma vez por projeto; todos os especialistas leem `workspace/brand/perfil.md` |
| Um post | `/criar-post` | Peça única; para várias peças use `/batch` |
| Carrossel | `/criar-carrossel` | Estrutura, texto por slide e design |
| Calendário editorial | `/criar-calendario` | |
| Várias peças de uma vez | `/batch` | Variações de hook, ângulo e framework |
| Um email ou newsletter | `/criar-email` | Inclui sequências só de email (boas-vindas, nutrição, carrinho) |
| Sequência coordenada entre canais | `/criar-sequencia` | Email + social + ads com mensagem única |
| Anúncio | `/criar-anuncio` | Copy e estrutura; publicar é `/publicar-anuncio` |
| Publicar anúncio no Meta | `/publicar-anuncio` | Exige confirmação humana |
| Roteiro de vídeo ou VSL | `/criar-video` | |
| Reels produzido (roteiro, narração e vídeo) | `/produzir-reels` | |
| Narrar um roteiro em áudio | `/narrar-roteiro` | |
| Podcast | `/criar-podcast` | |
| Thumbnail | `/gerar-thumbnail` | |
| Prompt de imagem | `/gerar-imagem` | Entrega só o prompt |
| Imagem gerada (PNG) | `/renderizar-imagem` | Gera a imagem a partir do prompt |
| Brief de design | `/criar-brief-design` | |
| Artigo SEO | `/criar-artigo` | |
| Landing page ou página de aplicação | `/criar-landing-page` | |
| Funil | `/criar-funil` | Para funil de lançamento de curso, prefira `/criar-infoproduto` |
| Webinar | `/criar-webinar` | |
| Curso, ebook, mentoria ou membership | `/criar-infoproduto` | |
| Avatar ou persona | `/criar-avatar` | |
| USP ou proposta de valor | `/criar-usp` | |
| Oferta (value stack, preço, garantia) | `/criar-oferta` | |
| Melhorar ou revisar uma peça pronta (copy, roteiro, carrossel, sequência, artigo, página) | `/otimizar-copy` | Diagnóstico, score e reescritas; o especialista do formato revisa a estrutura |
| Teste A/B | `/criar-teste-ab` | |
| Responder comentários e DMs | `/responder-comentarios` | Rascunhos; nunca publica |
| Prospectar creators | `/prospectar-creators` | Rascunhos de outreach; nunca envia |
| Analisar concorrentes | `/analisar-concorrencia` | Mapa competitivo |
| Clonar a estratégia de um concorrente ou expert | `/clonar-estrategia` | Engenharia reversa adaptada à sua marca |
| Analisar um vídeo | `/analisar-video` | |
| Capturar e analisar uma página | `/capturar-tela` | |
| Auditoria rápida de página, perfil, anúncios ou canal | `/auditoria` | Relatório com score |
| Auditoria premium para entregar ao cliente | `/auditoria-pro` | Screenshots, radar e roadmap em PDF |
| Clone de voz de um expert | `/criar-clone` | Pesquisa o expert na web |
| Clone da minha voz | `/criar-meu-clone` | Usa as suas amostras; salva em `workspace/clones/` |
| Datas comerciais do ano | `/datas-sazonais` | |
| Aprender com métricas | `/aprender` | Grava aprendizados na memória dos agents |
| Projeto em etapas com aprovação | `/projeto` | |
| Publicar no Notion | `/publicar-notion` | |
| Campanha completa por objetivo | `/campanha` | Lista os presets abaixo |
| Campanha de lançamento | `/campanha-lancamento` | |
| Campanha de geração de leads | `/campanha-prospeccao` | |
| Campanha de retenção | `/campanha-retencao` | |
| Campanha de autoridade | `/campanha-autoridade` | |
| Campanha de growth | `/campanha-growth` | |
| Campanha de Black Friday | `/campanha-black-friday` | |

## Arquitetura (two-tier)

- **Tier 1** (`agents/mos-*.md`): system prompts enxutos (~250 linhas) com dispatch protocol, output schema e quality gates. Carregados automaticamente pelo Claude Code e consultados sob demanda no ChatGPT Work e no Codex.
- **Tier 2** (`subagents/*-agent.md`): knowledge base profunda (de algumas centenas a milhares de linhas) com frameworks, cases, tabelas, exemplos. Lida sob demanda via Read pelos agents tier-1.

Isso mantém contextos dos agents leves, carrega profundidade só quando precisa, e permite evoluir knowledge sem mexer no dispatch.

## Versão

Versão atual em `.claude-plugin/plugin.json`. Histórico em `CHANGELOG.md`. Migração da v5 (squad) → v6 (native subagents) documentada em `docs/architecture/subagents-migration.md`.
