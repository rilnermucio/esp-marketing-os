---
description: Create a coordinated multi-channel content sequence (email + social + ads) with unified messaging. Dispatches mos-email + mos-social + mos-ads in parallel, com mos-launch ou mos-funnel adicionais por tipo de sequência.
argument-hint: "<campaign goal and channels, e.g., 'launch sequence 14 days email + Instagram + Meta Ads' or 'nurture 30 dias'>"
---

# /criar-sequencia: Sequência Multi-canal (Dispatch composto)

Cria sequência coordenada (mensagem unificada + timeline) orquestrando subagents especializados conforme o tipo escolhido. Não produz conteúdo inline.

## Required inputs (ask if missing)

1. **Tipo** (obrigatório): launch (7-14 dias), nurture (30 dias), promotion (5-7 dias), re-engagement (14 dias) ou custom
2. **Canais** (obrigatório): combinação entre email, Instagram, LinkedIn, TikTok, Twitter/X, YouTube, Meta Ads, Google Ads, WhatsApp
3. **Duração** (obrigatório): número de dias
4. **Produto/Oferta** (obrigatório): o que está sendo promovido
5. **Audiência** (obrigatório): persona + nível de awareness
6. **Goal** (obrigatório): launch, conversion, awareness, retention, re-engagement
7. **Budget** (opcional): orçamento de mídia paga (se canais ads incluídos)
8. **Tom** (opcional): profissional, casual, urgente, storytelling, educacional
9. **Existing assets** (opcional): tamanho da lista, audiência social, biblioteca de conteúdo

## Dispatch (paralelo, single message)

Em **um único message**, dispare os agents-base. Adicione os agents condicionais conforme tipo.

### Base (sempre)

```
- Agent(subagent_type: "mos-email", prompt: "Sequência de email tipo [tipo] de [N] dias para [produto]. Audiência: [audiência]. Goal: [goal]. Inclua subject lines, preview text, body completo de cada email, send time sugerido e CTA. Considere memory existente do cliente neste projeto.")

- Agent(subagent_type: "mos-social", prompt: "Posts coordenados para [lista de canais sociais] ao longo de [N] dias, alinhados com a sequência [tipo] do produto [produto]. Audiência: [audiência]. Inclua hook, copy completo, formato (feed/stories/reels/thread), hashtags, horário sugerido e enquete obrigatória por post. Considere memory existente do cliente neste projeto.")

- Agent(subagent_type: "mos-ads", prompt: "Campanhas de ads complementares à sequência [tipo] em [Meta Ads/Google Ads/etc]. Produto: [produto]. Budget: [budget ou 'sugerir mínimo viável']. Por fase do funil: awareness, conversion, retargeting. Inclua copy primário, headline, descrição e creative direction. Considere memory existente do cliente neste projeto.")
```
*(omitir `mos-ads` se nenhum canal ads foi escolhido)*

### Condicional por tipo

**Se tipo = launch** (acrescentar à mesma message):
```
- Agent(subagent_type: "mos-launch", prompt: "Estratégia de fases para lançamento de [duração]: pré-launch, launch, closing, pós-launch. Posicionamento da oferta, pitch timing, escassez e ritmo de exposição. Produto: [produto]. Considere memory existente do cliente neste projeto.")
```

**Se tipo = nurture** (acrescentar à mesma message):
```
- Agent(subagent_type: "mos-funnel", prompt: "Mapa de funil que orienta sequência de nurture de [duração]: TOFU (intro/valor) → MOFU (educação/autoridade) → BOFU (oferta). Audiência: [audiência]. Identifique pontos de queda esperados e o gancho de conversão.")
```

## Consolidação

Após os agents retornarem, consolide em entrega única:

```markdown
## Sequência Multi-canal: [Nome da campanha]

Tipo: [launch | nurture | promotion | re-engagement] | Duração: [N] dias | Canais: [lista]
Produto: [produto] | Audiência: [audiência] | Goal: [goal]

### Mensagem Unificada
- Core message: [uma frase]
- Promessa-chave: [transformação]
- Gancho emocional: [sentimento]
- CTA primário: [ação]

### Estratégia de Fases (de mos-launch ou mos-funnel, se aplicável)
[Fases com timing, objetivo de cada uma]

### Timeline Resumida
| Dia | Email | Social | Ads | Tema |
|-----|-------|--------|-----|------|
| 1 | [resumo] | [resumo] | [resumo] | [tema] |
| ... | ... | ... | ... | ... |

### Email Sequence (de mos-email)
[Subject + preview + body + CTA + horário, dia a dia]

### Social Posts (de mos-social)
[Por canal, dia a dia: formato, hook, copy, hashtags, horário, enquete]

### Ads (de mos-ads, se aplicável)
[Por fase: copy primário, headline, descrição, creative, budget sugerido, segmentação]

### Coordenação Cross-channel
[Como cada canal reforça os outros, frequency caps, sequenciamento]

### Métricas Sugeridas
| Canal | KPI | Benchmark | Tracking |
|-------|-----|-----------|----------|
| Email | Open / CTR | >25% / >3% | ESP |
| Social | Engagement rate | >3% IG, >2% LI | Insights |
| Ads | ROAS | >3:1 | Ads Manager |

### Próximos passos
- Setup de UTMs e tracking
- Criação de creatives (brief separado se preciso)
- Variação A/B em hook ou subject
```

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Sem `—`, sem "brutal", sem CAPS gratuito, sem aspas em falas
- Acentuação PT-BR correta
- Máximo 1-2 emojis no output final (não nos posts em si, esses seguem regra do canal)
- Enquete obrigatória em cada post social
- Compliance regulatório se nicho saúde/finanças/suplementos
- Fact-check (CONFIRMADO / PROVÁVEL) em qualquer claim citável

## Por que esse dispatch composto

Sequência multi-canal sem `mos-email` = email genérico. Sem `mos-social` = posts desalinhados com a fase. Sem `mos-ads` = mídia paga descolada do narrativo. `mos-launch` no tipo launch garante estratégia de oferta (sem ela, vira só "calendário com vendas"). `mos-funnel` no nurture garante que cada fase converse com o estágio do lead.
