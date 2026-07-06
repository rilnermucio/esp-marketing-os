---
description: Create email marketing content (single, welcome, nurture, launch, abandoned cart, re-engagement, newsletter). Dispatches mos-email simples ou mos-email + mos-copy em paralelo para sequências.
argument-hint: "<type and purpose, e.g., 'welcome sequence for SaaS' or 'launch email for course'>"
---

# /criar-email: Email Marketing (Dispatch-Based)

Cria copy de email orquestrando subagent(s) especializados via `Agent(subagent_type: "mos-*")`. Não produz inline.

## Required inputs (ask if missing)

1. **Tipo** (obrigatório): single, welcome (3-5 emails), nurture, launch (7-10 emails), abandoned cart (3 emails), re-engagement, newsletter
2. **Purpose/Goal** (obrigatório): o que o email deve gerar (conversão, nurture, recuperação, atualização)
3. **Audiência** (obrigatório): quem recebe (segmento, dor, momento da jornada)
4. **Produto/Oferta** (opcional, obrigatório se launch/cart): o que está sendo promovido
5. **Tom** (opcional): friendly, profissional, urgente, casual, inspiracional
6. **CTA** (opcional): ação específica desejada
7. **Sequence length** (opcional): número de emails se for sequência

## Dispatch Decision Tree

```
Briefing recebido
  ├── Single email (announcement, promo, update isolado)?
  │     └── Dispatch SIMPLES: mos-email
  │
  ├── Sequência (welcome / launch / cart / re-engagement / nurture)?
  │     └── Dispatch PARALELO: mos-email + mos-copy
  │         (mos-email cuida da arquitetura da sequência;
  │          mos-copy refina subject lines + CTAs em paralelo)
  │
  └── Newsletter recorrente?
        └── Dispatch SIMPLES: mos-email (com schema próprio de newsletter)
```

`mos-email` não tem memory persistente, passe todos os inputs no prompt.

## Dispatch Simples (single email ou newsletter)

```
Agent(subagent_type: "mos-email", prompt: "Crie [single email | newsletter] sobre [tópico/oferta]. Goal: [goal]. Audiência: [audiência]. Tom: [tom]. CTA: [cta]. Produto/oferta (se aplica): [produto]. Entregue: 3 opções de subject line (curiosidade, benefício, urgência), preview text, opening hook, body com framework adequado (PAS, AIDA, ou newsletter schema), CTA único e forte, PS estratégico, send timing recomendado, sugestões de A/B test (subject + CTA). Aplicar quality gates globais (sem travessão, sem 'brutal', máx 1 emoji em subject, PT-BR correto).")
```

## Dispatch Paralelo (sequências, single message)

```
- Agent(subagent_type: "mos-email", prompt: "Crie sequência [welcome/launch/abandoned cart/re-engagement/nurture] com [N] emails sobre [tópico/oferta]. Goal: [goal]. Audiência: [audiência]. Tom: [tom]. Produto/oferta: [produto]. Entregue: arquitetura completa da sequência (timing email-a-email, função de cada um, progressão narrativa), corpo completo de cada email (opening + body + CTA + PS), send timing por email, transição entre emails. Aplicar quality gates globais.")

- Agent(subagent_type: "mos-copy", prompt: "Refine subject lines e CTAs para sequência de [N] emails sobre [tópico/oferta]. Audiência: [audiência]. Para CADA email da sequência entregue: 3 variações de subject line (curiosidade, benefício, urgência), 1 preview text complementar, 2 variações de CTA (botão + link de texto). Foco em open rate (subject) e click-through (CTA). Aplicar quality gates globais (sem travessão, sem 'brutal', máx 1 emoji em subject).")
```

## Consolidação

Após os agents retornarem, entregue:

```markdown
## Email: [Tipo]: [Tópico/Oferta]

Tipo: [single | welcome | nurture | launch | cart | re-engagement | newsletter] | Goal: [goal] | Audiência: [audiência]

### Sequence Overview (se sequência)
| Email | Timing | Subject (recomendado) | Goal |
|-------|--------|------------------------|------|
| 1 | Day 0 | [...] | [...] |
| 2 | Day [X] | [...] | [...] |
| ... | ... | ... | ... |

### Email 1 (de mos-email + subject lines de mos-copy)

**Subject lines (3 opções)**
- Recomendado (curiosidade): [...]
- Variação A (benefício): [...]
- Variação B (urgência): [...]

**Preview text**
[...]

**Body**
[Greeting + opening hook + body + CTA + PS]

**CTA variations**
- Botão recomendado: [...]
- Link de texto: [...]

**Send timing recomendado**
[Dia + hora]

### Email 2, 3, ... N
[Mesmo schema]

### A/B Test Suggestions
| Email | Elemento | Versão A | Versão B | Hipótese |
|-------|----------|----------|----------|----------|
| 1 | Subject | [...] | [...] | [...] |
| ... | ... | ... | ... | ... |

### Notes
- Objection-chave abordada: [...]
- Próximo passo da jornada após sequência: [...]

### Próximos passos
- Sequência de re-engagement para non-openers
- Adaptação de tom para outro segmento
- Variações por persona
```

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Sem `—`, sem "brutal", sem CAPS gratuito
- Subject lines com máx 1 emoji (só se brand-appropriate); body com máx 1-2 emojis
- Subject 30-50 chars (mobile-friendly), preview <90 chars
- Acentuação PT-BR correta
- Sem palavras gatilho de spam
- Compliance regulatório se nicho saúde/finanças/suplementos
- Fact-check via WebSearch para stat/case/citação

## Por que esse dispatch

Single email = `mos-email` resolve sozinho (knowledge profunda de framework PAS/AIDA, subject formulas, hook patterns). Sequências têm 2 problemas independentes que paralelizam bem: arquitetura narrativa (mos-email, qual email faz qual coisa, timing, progressão) e copy de subject+CTA (mos-copy, onde mora open rate e CTR). Roda em 1 message, ganho de qualidade sem custo de latência.
