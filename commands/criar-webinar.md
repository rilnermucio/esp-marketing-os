---
description: Create a complete webinar (live or perpetual), strategy, structure, registration page, email sequence. Dispatches mos-launch + mos-funnel + mos-video → mos-copy + mos-email (workflow #6).
argument-hint: "<topic and goal, e.g., 'webinar de vendas pra meu curso de Python'>"
---

# /criar-webinar: Webinar Completo (Workflow #6)

Cria webinar (live ou perpetual) conforme **workflow #6** em `skills/marketing-os/SKILL.md`.

## Required inputs (ask if missing)

1. **Modelo** (obrigatório): live (data específica) | perpetual (sob demanda)
2. **Produto a vender** (obrigatório): nome, ticket, formato
3. **Avatar** (obrigatório): cargo, dor, faixa de renda
4. **Duração** (obrigatório): 45min, 60min, 90min
5. **Pitch ou só conteúdo?** (obrigatório): vendas (pitch + oferta) | nutrição (sem pitch)
6. **Nicho** (obrigatório): define disclaimers regulatórios

## Dispatch, Fase 1 (paralelo, single message)

```
- Agent(subagent_type: "mos-launch", prompt: "Estratégia de webinar [live/perpetual] para [produto]: posicionamento da oferta, pitch timing dentro da [duração], escassez/urgência, garantia, FAQ ao vivo. Modelo: [PLF perpetual / live launch]. Considere memory existente do cliente neste projeto.")

- Agent(subagent_type: "mos-funnel", prompt: "Funil de webinar completo: registro → página confirmação → reminder emails → live/replay → reposicionamento → encerramento de carrinho. Mapear pontos de queda esperados em cada step e taxas benchmark. Considere memory existente do cliente neste projeto.")

- Agent(subagent_type: "mos-video", prompt: "Estrutura do webinar de [duração] minutos: hook (0-5min), agenda (5-10min), conteúdo de valor (10-X min), transição pra oferta, pitch (Y-Z min), garantia, Q&A ao vivo. Aplicar ciência de retenção.")
```

## Fase 2 (sequencial, depende dos 3 outputs da Fase 1)

```
- Agent(subagent_type: "mos-copy", prompt: "Página de registro do webinar + headline atrativa + 3 emails: registro (confirmação), reminder dia anterior, reminder 1h antes. Baseado no posicionamento da Fase 1: [colar resumo mos-launch]. Considere memory existente do cliente neste projeto.")

- Agent(subagent_type: "mos-email", prompt: "Sequência completa de webinar: 4 emails pré-webinar (registro/lembretes), 1 email dia (link), 3 emails pós-webinar (replay → últimas vagas → encerramento de carrinho). Aplicar quality gates.")
```

## Fase 3: Quality Gates + Tracking

Aplicar gates globais do `skills/marketing-os/SKILL.md` (sem `—`, sem "brutal", PT-BR correto, sem aspas em roteiros) em todo conteúdo. Compliance regulatório por nicho. Recomendar setup de tracking via `mos-analytics` (eventos: registro, no-show, live attendance, replay watch, conversion).

## Consolidação

```markdown
## Webinar: [Tema]: Modelo [live/perpetual]

### Estratégia (mos-launch)
[Posicionamento + pitch timing + escassez]

### Funil (mos-funnel)
[Steps + pontos de queda + benchmarks]

### Roteiro (mos-video, [duração]min)
[Bloco a bloco com timestamps]

### Página de Registro + Headlines (mos-copy)
[Página + headline + CTAs]

### Sequência de Emails (mos-email)
**Pré-webinar:**
1. Email confirmação registro
2. Email reminder D-1
3. Email reminder 1h antes
4. Email "estamos ao vivo!"

**Pós-webinar:**
5. Email replay
6. Email últimas vagas
7. Email encerramento

### Setup de tracking (sugestão)
[Eventos pra GA4/Meta Pixel]
```

## Por que essa orquestração

Sem `mos-launch`: webinar vira aula sem venda (não tem estratégia de oferta). Sem `mos-funnel`: cada step do funil sai isolado. Sem `mos-video`: roteiro não respeita ciência de retenção. Fase 2 (copy + email) depende de saber QUAL é a oferta e onde está o pitch, por isso sequencial.
