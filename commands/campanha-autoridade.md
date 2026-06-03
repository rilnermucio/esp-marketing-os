---
description: Preset de autoridade. Dispatcha mos-research + mos-brand em paralelo, depois mos-copy + mos-seo + mos-social + mos-storytelling, com mos-audio opcional. Foco em thought leadership e credibilidade. Clone primário ogilvy.
argument-hint: "<nicho/tema> [--clone=ogilvy|abdaal] [--canal=linkedin|blog|podcast]"
---

# /campanha-autoridade: Preset de Autoridade

**Objetivo:** Construir autoridade, credibilidade e presença de marca no nicho.
**Clone primário:** `ogilvy` · **Clone alternativo:** `abdaal`

## Required inputs (ask if missing)

1. **Nicho/tema** (obrigatório)
2. **Pilares atuais ou desejados** (recomendado): áreas de expertise específicas
3. **Canais** (recomendado): blog, LinkedIn, podcast, YouTube
4. **Customizações opcionais:** `--clone=<override>`, `--nicho=<nicho>`

## Dispatch

**Fase 1 (paralelo):**

```
- Agent(subagent_type: "mos-research", prompt: "Mapeamento de temas de autoridade no nicho [nicho]: o que os top players publicam, gaps de conteúdo, perguntas não respondidas, dados/estudos atuais. Considere memory.")

- Agent(subagent_type: "mos-brand", prompt: "Definir/refinar identidade de autoridade: arquétipo (sage / hero / mentor), voz/tom estilo Ogilvy (sofisticado, evidence-based), pilares de posicionamento. Brand spec replicável.")
```

**Fase 2 (paralelo, depende do positioning):**

```
- Agent(subagent_type: "mos-copy", prompt: "Posts e artigos de posicionamento clone=ogilvy: thought leadership, opinião baseada em evidência, sem clickbait. Aplicar quality gates rigorosos (sem hype).")

- Agent(subagent_type: "mos-seo", prompt: "Estratégia SEO de autoridade: 1 artigo longo quinzenal (pillar pages) + cluster de artigos satélites. Keyword research focado em intent informacional. Internal linking pra hub de autoridade.")

- Agent(subagent_type: "mos-social", prompt: "Calendário editorial de autoridade nos pilares: 40% Educação + 30% Perspectiva + 20% Prova + 10% Humanização. 2-3 posts/semana de valor profundo. Quality gates + enquete.")

- Agent(subagent_type: "mos-storytelling", prompt: "Narrativas de credibilidade: casos de estudo do próprio trabalho, jornada do criador, decisões controversas com lições. Hero's journey aplicado em formato editorial.")
```

**Fase 3 (opcional, se nicho/audiência justificar áudio):**

```
- Agent(subagent_type: "mos-audio", prompt: "Roteiro de podcast ou conteúdo em áudio: 1 episódio mensal de aprofundamento, formato entrevista ou solo. Show notes + clipes pra repurposing.")
```

## Pilares de Conteúdo

```
PILAR 1, EDUCAÇÃO (40%): ensina algo específico/útil. Carrossel, artigo, vídeo tutorial.
PILAR 2, PERSPECTIVA (30%): opinião baseada em dados. Post de texto, LinkedIn, thread.
PILAR 3, PROVA (20%): casos de sucesso, resultados, bastidores. Depoimento, estudo de caso.
PILAR 4, HUMANIZAÇÃO (10%): falhas, jornada, curiosidades pessoais. Stories, vídeo informal.
```

## Frameworks

- Content Marketing, David Ogilvy
- Evidence-Based Content, Ali Abdaal
- Preeminência, Jay Abraham

### Checklist

```
SETUP (uma vez):
[ ] Pilares de autoridade definidos (Fase 1: mos-brand)
[ ] Mapeamento de gaps de conteúdo (Fase 1: mos-research)
[ ] Brand spec replicável (Fase 1: mos-brand)
[ ] Calendário editorial pelos 4 pilares (Fase 2: mos-social)
[ ] Pillar pages e cluster SEO planejados (Fase 2: mos-seo)

OPERAÇÃO QUINZENAL:
[ ] 1 artigo longo (pillar) publicado
[ ] 4-6 posts curtos derivados (clusters)
[ ] 1 narrativa de credibilidade ou case
[ ] Distribuição multi-canal (LinkedIn, blog, social)

OPERAÇÃO MENSAL (opcional):
[ ] 1 episódio de podcast (se aplicável)
[ ] Repurposing em clipes/threads
```

### KPIs

| KPI | Meta | Como Medir |
|-----|------|------------|
| Tráfego orgânico | Crescente mês a mês | GA4 / Search Console |
| Saves e shares social | > média da categoria | Insights da plataforma |
| Inbound de oportunidades | > 1/semana | Mensagens diretas, e-mails |
| Citações por terceiros | Crescente trimestre a trimestre | Mentions monitoradas |

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Sem `—`, sem "brutal", sem CAPS gratuito
- Acentuação PT-BR correta
- Fact-check rigoroso em estatísticas e cases (CONFIRMADO / PROVÁVEL / NÃO USAR)
- Sem hype ou clickbait (autoridade exige sobriedade)
- Enquete obrigatória em conteúdo social

## Memory note

Os agents `mos-copy`, `mos-social`, `mos-seo` têm memory project em `.claude/agent-memory/marketing-os-<agent>/`. Sempre mencione no prompt que considere memory existente do cliente para manter consistência de voz e evitar repetir ângulos editoriais já usados.
