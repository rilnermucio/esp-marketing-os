---
description: Preset de growth. Dispatcha mos-research + mos-analytics em paralelo, depois mos-ab-testing + mos-growth + mos-copy. Foco em experimentação acelerada e crescimento não-linear via ICE Score e AARRR. Clone primário ellis.
argument-hint: "<funil/produto> [--clone=ellis|chen] [--north-star=...]"
---

# /campanha-growth: Preset de Growth

**Objetivo:** Experimentação acelerada para crescimento não-linear.
**Clone primário:** `ellis` · **Clone alternativo:** `chen`

## Required inputs (ask if missing)

1. **Funil ou produto** (obrigatório)
2. **North Star Metric** (recomendado): a métrica que importa de verdade
3. **Baseline atual** (recomendado): números atuais por estágio AARRR
4. **Customizações opcionais:** `--clone=<override>`

## Dispatch

**Fase 1 (paralelo):**

```
- Agent(subagent_type: "mos-research", prompt: "Análise de oportunidades de growth: pontos de fricção do funil atual, north star metric, alavancas com maior potencial de impacto. Considere memory de experimentos anteriores.")

- Agent(subagent_type: "mos-analytics", prompt: "Setup AARRR (Acquisition / Activation / Retention / Referral / Revenue): tracking de cada estágio, identificação de leaks, baseline pra comparação de experimentos.")
```

**Fase 2 (paralelo, depende das oportunidades identificadas):**

```
- Agent(subagent_type: "mos-ab-testing", prompt: "Design de batch de experimentos: 4-6 hipóteses ranqueadas por ICE Score (Impacto × Confiança × Facilidade). Pra cada uma: variante A/B, tamanho mínimo de amostra, critério de parada, métrica primária.")

- Agent(subagent_type: "mos-growth", prompt: "Estratégias de growth hacking aplicáveis ao funil [TOFU/MOFU/BOFU]: viral loops, referral, retention hooks, ativação. Priorizar por viral coefficient esperado.")

- Agent(subagent_type: "mos-copy", prompt: "Variantes de copy pros experimentos da Fase 2: headlines, CTAs, value props alternativas. Pra cada variante, hipótese explicitada.")
```

## Ciclo Semanal de Experimentos

```
SEG (Hipótese): "Se [mudança], então [métrica] vai [melhorar] porque [razão]". ICE Score.
TER (Design): variante A/B + amostra mínima + tracking + critério de parada.
QUA-SEX (Execução): launcha + não analisa antes do tempo definido + documenta variáveis externas.
SEG seguinte (Análise): significância estatística + segmentos + decisão (implementar / iterar / descartar).
SEMPRE (Documentação): log de experimentos + aprendizados (mesmo em casos negativos) + próxima hipótese.
```

## Frameworks

- ICE Score, Sean Ellis
- Growth Loop
- Viral Coefficient
- AARRR Metrics (Pirate Metrics)

### Checklist

```
SETUP INICIAL:
[ ] North Star Metric definida (Fase 1)
[ ] Baseline AARRR documentado (Fase 1: mos-analytics)
[ ] Backlog de hipóteses priorizado por ICE (Fase 2: mos-ab-testing)
[ ] Tracking confiável em cada estágio do funil
[ ] Doc de log de experimentos criado

OPERAÇÃO SEMANAL:
[ ] 1-2 experimentos novos lançados
[ ] Experimentos anteriores analisados (com significância estatística)
[ ] Decisão registrada (implementar / iterar / descartar)
[ ] Próxima hipótese formulada com clareza

OPERAÇÃO MENSAL:
[ ] North Star Metric vs meta revisada
[ ] Estágio AARRR com maior leak identificado
[ ] Próxima onda de experimentos planejada
```

### KPIs

| KPI | Meta | Como Medir |
|-----|------|------------|
| Velocity de experimentos | 1-2/semana | Experimentos lançados / semana |
| Win rate | 20-30% | Experimentos positivos / total |
| Lift do North Star | Crescente | Métrica primária vs baseline |
| Conhecimento gerado | Cumulativo | Aprendizados documentados |

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Sem `—`, sem "brutal", sem CAPS gratuito
- Acentuação PT-BR correta
- Hipóteses com formato "se X, então Y, porque Z"
- Critério de parada definido antes do experimento (sem peeking)

## Memory note

Os agents `mos-copy`, `mos-ab-testing` têm memory project em `.claude/agent-memory/marketing-os-<agent>/`. Sempre mencione no prompt que considere memory existente para evitar repetir experimentos já testados e para construir cumulativamente sobre aprendizados anteriores.
