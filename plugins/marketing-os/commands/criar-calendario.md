---
description: Create comprehensive editorial calendars for social media with content pillars, posting schedules, format distribution. Dispatches mos-social simples ou mos-social + mos-research em paralelo para nichos novos / multi-platform.
argument-hint: "<period and niche, e.g., 'monthly for fitness brand' or 'Q1 for SaaS startup'>"
---

# /criar-calendario: Calendário Editorial (Dispatch-Based)

Cria calendário editorial estratégico orquestrando subagent(s) especializados via `Agent(subagent_type: "mos-*")`. Não produz inline.

## Required inputs (ask if missing)

1. **Período** (obrigatório): week, month, quarter ou custom range
2. **Plataformas** (obrigatório): Instagram, LinkedIn, TikTok, Twitter, YouTube ou multi-platform
3. **Nicho/Indústria** (opcional): setor de negócio ou foco de conteúdo
4. **Content pillars** (opcional): temas principais (definir se não informado)
5. **Posting frequency** (opcional): quantas vezes/semana por plataforma
6. **Goals** (opcional): growth, engagement, sales, authority ou mixed
7. **Important dates** (opcional): lançamentos, holidays, eventos a incluir
8. **Template** (opcional): Balanced Growth, Authority Building, Sales-Focused (default Balanced Growth)

## Dispatch Decision Tree

```
Briefing recebido
  ├── Cliente/nicho conhecido + plataformas conhecidas + memory existente?
  │     └── Dispatch SIMPLES: mos-social
  │
  ├── Nicho novo OU multi-platform completo OU sem benchmarks recentes?
  │     └── Dispatch PARALELO: mos-social + mos-research
  │         (research valida trends da semana/mês,
  │          benchmarks de engajamento por plataforma no nicho,
  │          datas culturais BR específicas do período)
  │
  └── Calendário derivado de campanha já existente (launch, seasonal)?
        └── Dispatch SIMPLES: mos-social (ele puxa contexto da campanha)
```

`mos-social` tem `memory: project`: explicite "considere memory existente do cliente neste projeto" no prompt.

## Dispatch Simples (cliente/nicho conhecido)

```
Agent(subagent_type: "mos-social", prompt: "Calendário editorial [week | month | quarter | custom] para [plataformas]. Nicho: [nicho]. Goal: [goal]. Posting frequency: [X posts/semana por plataforma]. Template estrutural: [Balanced Growth | Authority Building | Sales-Focused]. Important dates do período: [datas]. Considere memory existente do cliente neste projeto. Entregue: 3-5 content pillars com % de distribuição, important dates do período com content opportunity, weekly overview completo (dia a dia, plataforma, formato, tópico, pillar, horário ótimo BRT), content ideas por pillar (mínimo 3 por pillar), format distribution table, KPIs to track com targets realistas, production checklist semanal e diário, **enquete obrigatória** sugerida para pelo menos 2 posts/semana. Aplicar quality gates globais (sem travessão, sem 'brutal', PT-BR correto, máx 1-2 emojis).")
```

## Dispatch Paralelo (nicho novo / multi-platform, single message)

```
- Agent(subagent_type: "mos-research", prompt: "Pesquisa rápida pra calendário editorial em [nicho] BR para [plataformas]: trends ativos no nicho nos últimos 30 dias, benchmarks de engajamento por plataforma (reach, saves, shares médios para o nicho), formatos performando melhor por plataforma, datas culturais BR específicas do período [período] (não-genéricas), influenciadores/concorrentes ativos a observar, tópicos saturados a evitar, ângulos em aberto. Retorne research brief compacto pra alimentar planejamento editorial.")

- Agent(subagent_type: "mos-social", prompt: "Calendário editorial [period] para [plataformas]. Nicho: [nicho]. Goal: [goal]. Posting frequency: [X]. Template estrutural: [Balanced Growth | Authority Building | Sales-Focused]. Considere memory existente do cliente neste projeto. Aguarde research do mos-research e use trends + benchmarks + datas que ele apontar. Entregue: 3-5 content pillars com %, important dates do período, weekly overview completo, content ideas por pillar (3+ por pillar), format distribution, KPIs com targets realistas baseados em benchmarks do research, production checklist, **enquete obrigatória** em pelo menos 2 posts/semana. Aplicar quality gates globais.")
```

## Consolidação

Após os agents retornarem, entregue:

```markdown
## Calendário Editorial: [Período]

Plataformas: [...] | Nicho: [...] | Goal: [growth | engagement | sales | authority] | Frequency: [X posts/semana] | Template: [Balanced Growth | Authority Building | Sales-Focused]

### Research Insights (se houver)
- Trends ativos no nicho: [...]
- Benchmarks por plataforma: [...]
- Datas culturais BR do período: [...]
- Tópicos saturados a evitar: [...]

### Content Pillars
| Pillar | Descrição | % | Hashtag |
|--------|-----------|---|---------|
| [...] | [...] | [...] | #[...] |

### Important Dates
| Data | Evento | Content Opportunity | Prioridade |
|------|--------|---------------------|------------|
| [...] | [...] | [...] | High/Medium |

### Weekly Overview

#### Semana 1: [Tema/Foco]
| Dia | Data | Plataforma | Formato | Tópico | Pillar | Horário BRT | Enquete? |
|-----|------|------------|---------|--------|--------|-------------|----------|
| Mon | [...] | IG | Carousel | [...] | Educational | 19:00 |, |
| Tue | [...] | IG | Reel | [...] | Entertainment | 20:00 | Sim, [tipo] |
| ... | ... | ... | ... | ... | ... | ... | ... |

#### Semana 2, 3, 4
[Mesmo schema]

### Content Ideas por Pillar
**[Pillar 1]:**
1. [...]
2. [...]
3. [...]

[Repetir por pillar]

### Format Distribution
| Formato | Qtd/semana | % | Plataforma principal |
|---------|------------|---|----------------------|
| Reels/TikTok | [...] | [...] | IG, TikTok |
| Carousel | [...] | [...] | IG, LinkedIn |
| Single post | [...] | [...] | All |
| Stories | [...] | [...] | IG |

### Enquetes da Semana (obrigatório social)
| Post | Tipo | Pergunta pronta |
|------|------|-----------------|
| [Tue Reel] | [binária | qual-você-faz | escala | desafio | curiosidade] | [...] |
| [Fri Carousel] | [...] | [...] |

### KPIs to Track
| Métrica | Atual | Target | Como melhorar |
|---------|-------|--------|---------------|
| Reach | [...] | [...] | [...] |
| Engagement Rate | [...] | [...] | [...] |
| Saves | [...] | [...] | [...] |

### Production Checklist
- Weekly prep (Sunday): [...]
- Daily tasks: [...]

### Próximos passos
- Copy completa pra cada post do calendário
- Briefs de design pra peças visuais
- Adaptação pra outra cadência (ex: 3x → 5x semana)
- Adicionar campanha/launch específico
```

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Sem `—`, sem "brutal", sem CAPS gratuito
- Acentuação PT-BR correta
- Máx 1-2 emojis em qualquer texto sugerido
- **Enquete obrigatória** em pelo menos 2 posts/semana (regra do SKILL.md)
- Datas culturais BR específicas, não genéricas (ex: Festa Junina dia 24/06, não "junho tem festa junina")
- Horários em BRT
- Compliance regulatório se nicho saúde/finanças/suplementos
- Fact-check via WebSearch para benchmarks/stats citados (CONFIRMADO/PROVÁVEL/NÃO USAR)

## Por que esse dispatch

`mos-social` sozinho entrega calendário sólido quando já há contexto do cliente (memory) e nicho conhecido. Pra nichos novos ou multi-platform completo, `mos-research` em paralelo evita calendar genérico (ex: chutar que "Reels dão mais engajamento" sem benchmark do nicho específico) e adiciona ângulos baseados em trends reais da semana, não conhecimento estático.
