---
description: Publish ad campaigns to Meta Ads. Dispatches mos-ads first to validate copy, targeting, and budget against quality gates, then executes Meta Ads MCP tools to launch.
argument-hint: "<campaign type and goal, e.g., 'lead generation campaign for course launch' or 'conversion campaign for product'>"
---

# /publicar-anuncio: Publicar Campanha Meta Ads

Utility de publicação. **Sempre** dispatcha `mos-ads` antes de tocar no Meta Ads MCP — copy não validada vai pro ar com travessão, "brutal", CAPS, ou targeting frouxo. O dispatch protege a conta.

> Requires: Meta Ads MCP integration ativa (Especializei). Ver `CONNECTORS.md`.

## Required inputs (ask if missing)

1. **Objetivo da campanha** (obrigatório): Awareness, Traffic, Engagement, Leads, Conversions, Sales
2. **Copy** (obrigatório): vinda de `/criar-anuncio` ou colada pelo usuário
3. **Audience** (obrigatório): demographics, interests, behaviors, custom audiences
4. **Budget** (obrigatório): diário ou lifetime em BRL
5. **Duração** (obrigatório): start + end dates
6. **Placement** (opcional): Instagram Feed, Stories, Facebook Feed, Audience Network, All (default: All)
7. **Criativo** (opcional): URLs de imagem/vídeo ou descrição pra geração via IA
8. **Landing Page URL** (opcional): destino dos cliques

## Fase 1 (dispatch obrigatório): Validação via mos-ads

**Antes** de qualquer chamada ao Meta Ads MCP, despache:

```
- Agent(subagent_type: "mos-ads", prompt: "Validar pré-publicação no Meta Ads.

INPUTS:
- Objetivo: [objetivo]
- Copy proposta: [colar copy completa: primary text, headline, description, CTA]
- Audiência: [demographics + interests + custom audiences]
- Budget: [valor + diário/lifetime]
- Duração: [start → end]
- Placement: [placements]
- Landing page: [URL]

TAREFAS:
1. Aplicar quality gates globais na copy (sem '—', sem 'brutal', sem CAPS, sem aspas em falas, máx 1-2 emojis, PT-BR correto)
2. Refinar targeting (sugerir interests/behaviors adicionais ou cortes; flag se audiência muito ampla/estreita)
3. Sancionar budget vs objetivo (CPL/CPA estimado para o nicho; flag se subdimensionado)
4. Gerar 2-3 variações de headline + 2 variações de primary text pra A/B
5. Validar bid strategy adequada ao objetivo
6. Flag de compliance se nicho saúde/finanças/suplementos

OUTPUT esperado:
- Copy aprovada (versão final + variações A/B)
- Targeting refinado
- Budget ajustado (com justificativa se mudou)
- Warnings (compliance, audiência, criativos faltando)
- Memory check: considere memory existente do cliente em `.claude/agent-memory/marketing-os-mos-ads/` se houver.")
```

**Se mos-ads retornar warnings críticos** (compliance, copy reprovada nos gates, audiência inviável), **pare** e retorne ao usuário antes de publicar. Não force publicação de copy ruim.

## Fase 2: Publicação via Meta Ads MCP

Com a copy aprovada da Fase 1, execute na ordem:

```
1. get_ad_accounts          → seleciona ad account
2. get_account_pages        → identifica Facebook Page
3. estimate_audience_size   → confirma reach esperado
4. create_campaign          → seta objetivo + nome
5. create_adset             → targeting refinado + budget + schedule + bid strategy
6. create_ad_creative       → upload do criativo + copy aprovada
7. create_ad                → linka criativo ao adset
```

**Para A/B test** (recomendado): repetir steps 6-7 para cada variação retornada pelo mos-ads.

## Estrutura de campanha

### Objetivos
| Objective | Quando usar | Otimização |
|-----------|-------------|------------|
| Awareness | Visibilidade de marca | Impressions |
| Traffic | Drive pra site/LP | Link clicks |
| Engagement | Likes, comments, shares | Post engagement |
| Leads | Lead form fills | Cost per lead |
| Conversions | Sales, signups | Cost per conversion |
| Sales | E-commerce | ROAS |

## MCP tools usados

| Tool | Propósito |
|------|-----------|
| `get_ad_accounts` | Lista contas disponíveis |
| `get_account_pages` | Páginas Facebook |
| `estimate_audience_size` | Estima reach pré-launch |
| `create_campaign` | Cria campanha + objetivo |
| `create_adset` | Targeting + budget + schedule |
| `create_ad_creative` | Cria criativo com copy + visual |
| `create_ad` | Finaliza e launcha |
| `get_insights` | Tracking pós-launch |

## Output

```markdown
## Campanha Meta Ads Publicada

Objetivo: [objetivo]
Budget: R$ [valor]/[diário|lifetime]
Duração: [start] → [end]
Placement: [placements]

### Detalhes
- **Campaign ID:** [ID]
- **Campaign Name:** [nome]
- **Status:** [Active | Scheduled | In Review]

### Ad Set
- Targeting: [resumo]
- Reach estimado: [X pessoas]
- Budget: R$ [valor]
- Schedule: [periodo]

### Ad Creative (final, aprovado por mos-ads)
- Primary text: [copy]
- Headline: [headline]
- Description: [description]
- CTA: [botão]
- Destino: [URL]

### Variações A/B publicadas
| Variant | Mudança | Hipótese |
|---------|---------|----------|
| A (Control) | Original | Baseline |
| B | Headline alternativa | [hipótese de mos-ads] |
| C | Primary text alternativo | [hipótese de mos-ads] |

### Tracking pós-launch (24-48h)
- Impressions e reach
- CTR
- CPC / CPL / CPA
- Conversions (se rastreado)
- ROAS (se e-commerce)
```

## Quality Gates (já aplicados na Fase 1, reconfirme antes do create_ad)

- Sem `—`, sem "brutal", sem CAPS gratuito
- Sem aspas em falas
- Máximo 1-2 emojis
- Acentuação PT-BR correta
- Compliance regulatório (saúde/finanças/suplementos)
- Disclaimer "Resultados não garantidos" se promessa quantitativa

## Follow-up ao usuário

"Quer que eu:
1. Crie variações adicionais pra A/B?
2. Configure audiência de retargeting pra não-convertidos?
3. Setup dashboard de reporting?
4. Crie a landing page dessa campanha? (roteia pra /criar-landing-page)
5. Monitore performance e sugira otimizações em 48h?"

## Por que dispatch obrigatório pré-publicação

Publicar copy direto pelo MCP, sem mos-ads, é arriscado:
- Travessão `—` reprovado em ads policy
- "Brutal" / CAPS gera baixa qualidade no leilão
- Targeting amplo demais queima budget; estreito demais não escala
- Faltando memory do cliente, repete erros de campanhas anteriores

mos-ads aplica os gates + refina targeting + gera A/B variants num único call. Custa 1 dispatch, evita campanha queimada.
