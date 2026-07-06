---
description: Preset de prospecção. Dispatcha mos-research sequencial, depois mos-funnel + mos-copy + mos-ads em paralelo, fechando com mos-email + mos-social + mos-analytics. Funil HDIC de Sabri Suby. Clone primário suby.
argument-hint: "<nicho/avatar> [--canal=...] [--budget=...] [--clone=suby|kennedy] [--produto=...]"
---

# /campanha-prospeccao: Preset de Prospecção

**Objetivo:** Gerar leads qualificados e novos clientes de forma consistente.
**Clone primário:** `suby` · **Clone alternativo:** `kennedy`

## Required inputs (ask if missing)

1. **Nicho/avatar** (obrigatório)
2. **Produto ou oferta** (obrigatório)
3. **Canal principal** (recomendado): instagram, meta-ads, google-ads, linkedin
4. **Budget de tráfego** (recomendado)
5. **Customizações opcionais:** `--clone=<override>`, `--nicho=<nicho>`

## Dispatch

**Fase 1 (sequencial, research informa o resto):**

```
- Agent(subagent_type: "mos-research", prompt: "Mapeamento de avatar e canais para prospecção em [nicho]: dores reais, linguagem usada, plataformas onde está, concorrentes ativos, lead magnets que funcionam. Considere memory.")
```

**Fase 2 (paralelo, depende do research):**

```
- Agent(subagent_type: "mos-funnel", prompt: "Funil HDIC (Horde-Direct-Convert) de Sabri Suby: TOFU (audiência fria + interesse + lookalike) → MOFU (lead magnet + nutrição) → BOFU (oferta direta + retargeting). Pontos de qualificação.")

- Agent(subagent_type: "mos-copy", prompt: "Copy clone=suby: lead magnet de alto valor (PDF/mini-curso/webinar), landing page de captura, headline + CTA. Usando avatar da Fase 1.")

- Agent(subagent_type: "mos-ads", prompt: "Campanhas de tráfego pago pra prospecção: audiência fria + interest + lookalike. Budget [valor]. CPL alvo [< R$15-50 dependendo de nicho]. Variantes A/B de criativo.")
```

**Fase 3 (paralelo):**

```
- Agent(subagent_type: "mos-email", prompt: "Sequência de nutrição 7-10 emails pós opt-in: educação → história → caso de prova → soft pitch → hard pitch → urgência → última chance. Considere memory.")

- Agent(subagent_type: "mos-social", prompt: "Conteúdo de topo de funil: 3-5 posts/semana sobre dores do avatar, sem pitch direto. Quality gates + enquete.")

- Agent(subagent_type: "mos-analytics", prompt: "Tracking de CAC, CPL por canal, conversão da landing, performance da nutrição. Dashboard mensal de revisão.")
```

## Frameworks

- Método HDIC (Horde-Direct-Convert), Sabri Suby
- Pirâmide de Consciência (3% → 97%)
- Os 3 Pilares, Jay Abraham

## Estrutura do Funil

```
TOPO (Awareness): conteúdo orgânico de dores + ads frios → tráfego pra LM
MEIO (Interesse): lead magnet + nutrição email + retargeting → qualificação
FUNDO (Decisão): oferta direta + testemunhos + garantia → conversão
```

### Checklist

```
SETUP INICIAL:
[ ] Avatar detalhado (Fase 1: mos-research)
[ ] Lead magnet criado (Fase 2: mos-copy)
[ ] Landing page de captura (Fase 2: mos-copy)
[ ] Sequência de nutrição (Fase 3: mos-email)
[ ] Budget e canais definidos (Fase 2: mos-ads)

OPERAÇÃO SEMANAL:
[ ] 3-5 posts de topo (Fase 3: mos-social)
[ ] CPL monitorado e criativos otimizados
[ ] Métricas da nutrição revisadas
[ ] Próxima variante A/B da landing testada

ANÁLISE MENSAL:
[ ] CAC vs LTV sustentável?
[ ] Canal com menor CPL?
[ ] Email da nutrição com mais conversão?
[ ] Próximo teste A/B prioritário
```

### KPIs

| KPI | Meta | Canal |
|-----|------|-------|
| CPL | < R$15-50 (varia por nicho) | Ads |
| Opt-in | > 35% | Landing page |
| Open nutrição | > 30% | Email |
| CAC | < LTV/3 | Todos |

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Sem `—`, sem "brutal", sem CAPS gratuito
- Acentuação PT-BR correta
- Compliance regulatório se nicho saúde/finanças/suplementos
- Enquete obrigatória em conteúdo social

## Memory note

Os agents `mos-copy`, `mos-email`, `mos-ads`, `mos-social`, `mos-funnel` têm memory project em `.claude/agent-memory/marketing-os-<agent>/`. Sempre mencione no prompt que considere memory existente do cliente para evitar repetir hooks usados, manter consistência com campanhas passadas e respeitar restrições de compliance previamente registradas.
