---
description: Create high-converting ad copy for Meta Ads, Google Ads, TikTok Ads, LinkedIn Ads, and Pinterest Ads. Dispatches mos-ads (with mos-research when nicho/cliente é novo).
argument-hint: "<platform and product, e.g., 'Meta Ads for SaaS product' or 'Google Search for e-commerce'>"
---

# /criar-anuncio: Anúncio Pago (Dispatch-Based)

Cria copy completa de anúncio orquestrando subagent(s) especializados via `Agent(subagent_type: "mos-*")`. Não produz inline.

## Required inputs (ask if missing)

1. **Plataforma** (obrigatório): Meta Ads, Google Ads, TikTok Ads, LinkedIn Ads ou Pinterest Ads
2. **Produto/Oferta** (obrigatório): o que está sendo anunciado
3. **Objetivo** (opcional): awareness, traffic, leads, conversions, sales
4. **Audiência-alvo** (opcional): perfil, dor principal, faixa de renda
5. **Benefício-chave** (opcional): proposta de valor central
6. **Tom** (opcional): profissional, casual, urgente, autoritário, divertido
7. **Budget range** (opcional): para sugestões de campaign structure

## Dispatch Decision Tree

```
Briefing recebido
  ├── Cliente/nicho já com memory ou contexto conhecido? (sim)
  │     └── Dispatch SIMPLES: mos-ads
  │
  ├── Cliente novo / nicho novo / sem benchmarks recentes? (sim)
  │     └── Dispatch PARALELO: mos-ads + mos-research
  │         (research valida concorrência ativa, dores reais, ângulos em uso)
  │
  └── Já existe campanha rodando + pede só variações novas?
        └── Dispatch SIMPLES: mos-ads (variations mode)
```

## Dispatch Simples (caso comum)

```
Agent(subagent_type: "mos-ads", prompt: "Crie copy completa de anúncio para [plataforma]. Produto/oferta: [produto]. Objetivo: [objetivo]. Audiência: [audiência]. Benefício-chave: [benefício]. Tom: [tom]. Considere memory existente do cliente neste projeto. Entregue: 5 variações com ângulos diferentes (problem-aware, social proof, result-focused, curiosity, urgency), respeitando char limits da plataforma, com CTA específico, direção criativa para visual, e sugestões de A/B test. Aplicar quality gates globais (sem travessão, sem 'brutal', PT-BR correto, máx 1-2 emojis).")
```

## Dispatch Paralelo (cliente/nicho novo, single message)

```
- Agent(subagent_type: "mos-research", prompt: "Pesquisa rápida pra ad creative em [nicho] na [plataforma] BR: concorrentes ativos rodando ads agora, ângulos predominantes, dores reais do público [audiência], stats relevantes dos últimos 90 dias, regulamentação se nicho saúde/finanças. Retorne research brief compacto pra alimentar copy de anúncio.")

- Agent(subagent_type: "mos-ads", prompt: "Crie copy completa de anúncio para [plataforma]. Produto/oferta: [produto]. Objetivo: [objetivo]. Audiência: [audiência]. Benefício-chave: [benefício]. Tom: [tom]. Considere memory existente do cliente neste projeto. Aguarde research do mos-research e diferencie-se dos ângulos saturados que ele apontar. Entregue 5 variações, char limits respeitados, CTA, direção criativa, A/B test. Aplicar quality gates globais.")
```

## Consolidação

Após os agents retornarem, entregue:

```markdown
## Anúncio: [Produto]: [Plataforma]

Plataforma: [Meta | Google | TikTok | LinkedIn | Pinterest] | Objetivo: [objetivo] | Audiência: [audiência]

### Research Context (se houver)
[Concorrência ativa + ângulos saturados + ângulos em aberto + stats, do mos-research]

### Variações de Copy (de mos-ads)

**Versão 1, [Ângulo: ex. Problem-Aware]**
- Primary text: [...]
- Headline: [...]
- Description: [...]
- CTA: [...]

**Versão 2, [Ângulo: ex. Social Proof]**
[mesmo schema]

**Versão 3, [Ângulo: ex. Result-Focused]**
[mesmo schema]

**Versão 4, Short-form (Stories/Reels)**
[versão condensada]

**Versão 5, Urgency/Scarcity**
[versão com gatilho temporal]

### Direção Criativa
- Visual recomendado: [...]
- Hook de vídeo (3 primeiros segundos): [...]
- Versão UGC-style (se aplicável): [...]

### A/B Test Suggestions
[Tabela com hipóteses de teste: hook, CTA, ângulo, formato]

### Campaign Structure
- Ad sets sugeridos: [...]
- Alocação de budget: [...]

### Próximos passos
- Adaptar pra outras plataformas
- Roteiro de vídeo completo
- Variações adicionais por ângulo
```

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Sem `—`, sem "brutal", sem CAPS gratuito
- Máx 1-2 emojis (preferir zero)
- Acentuação PT-BR correta
- Char limits da plataforma respeitados
- Compliance regulatório se nicho saúde/finanças/suplementos
- Fact-check via WebSearch se cita pessoa/stat/case (CONFIRMADO/PROVÁVEL/NÃO USAR)

## Por que esse dispatch

`mos-ads` sozinho entrega copy polida com knowledge profunda de cada plataforma (limits, frameworks, ângulos). Quando o nicho é novo, `mos-research` em paralelo evita ângulos saturados e valida dores reais antes da copy, sem custo extra de latência (1 message, 2 calls).
