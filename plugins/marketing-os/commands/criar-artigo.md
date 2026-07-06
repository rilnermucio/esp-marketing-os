---
description: Create a complete SEO-optimized article. Dispatches mos-research → mos-seo sequentially (research informs keyword strategy and outline), with optional mos-copy pass for headline/CTA refinement.
argument-hint: "<topic and keyword, e.g., 'article about content marketing targeting 'content marketing strategy''>"
---

# /criar-artigo: Artigo SEO Completo (Dispatch Sequencial)

Cria artigo SEO orquestrando 2 subagents em sequência (research alimenta SEO). Não produz inline. Veja workflow #3 e Mapa de Dispatch em `skills/marketing-os/SKILL.md`.

## Required inputs (ask if missing)

1. **Tópico** (obrigatório): assunto principal do artigo
2. **Primary keyword** (obrigatório): termo principal pra ranquear
3. **Search intent** (obrigatório): informational, commercial ou transactional
4. **Word count** (opcional): default 1.500-2.500 (informational), 2.000-4.000 (commercial), 500-1.500 (transactional)
5. **Audiência** (opcional): quem busca por isso
6. **Secondary keywords** (opcional): termos relacionados a incluir
7. **Concorrentes top-ranking** (opcional): URLs a superar

## Dispatch (sequencial obrigatório)

A sequência é obrigatória: `mos-seo` precisa do output de `mos-research` (keywords reais, SERP atual, intent confirmado, gaps de conteúdo) pra produzir artigo que ranqueia. Não rode em paralelo.

### Passo 1, Research

```
Agent(subagent_type: "mos-research", prompt: "Keyword research e SERP analysis para artigo sobre [tópico], primary keyword [keyword], intent [intent]. Considere memory existente do cliente neste projeto. Entregue: volume estimado e dificuldade da primary, 3-5 secondary keywords com volume, 5-8 long-tail (incluindo question keywords e LSI), análise dos top 5 ranqueando hoje (estrutura, gaps, ângulo predominante), search intent confirmado/refinado, snippets oportunidades (paragraph/list/table), entidades semânticas e tópicos correlatos. Audiência: [audiência].")

→ Aguarde research brief antes do passo 2.
```

### Passo 2, Artigo SEO completo

```
Agent(subagent_type: "mos-seo", prompt: "Artigo SEO completo sobre [tópico], primary keyword [keyword], intent [intent], target [word count] palavras. Audiência: [audiência]. Use este research como base [colar research brief do passo 1]. Entregue: 3-5 opções de title tag (50-60 chars), meta description (150-160 chars), URL slug, heading structure completa H1/H2/H3, artigo full com intro+body+conclusão, integração E-E-A-T, otimização de featured snippets (paragraph/list/table conforme intent), FAQ schema-ready, internal linking suggestions, image suggestions com alt text, SEO checklist final. Aplicar quality gates globais (sem travessão, sem 'brutal', PT-BR correto).")
```

### Passo 3 (opcional), Refino de headline + CTA

```
Agent(subagent_type: "mos-copy", prompt: "Otimizar headline (H1 + title tag) e CTA final do artigo abaixo. Gerar 5 variações de headline com ângulos diferentes (curiosidade, benefício, número, contrarian, autoridade) e 3 variações de CTA. Texto do artigo: [colar artigo do passo 2]. Aplicar quality gates globais.")
```

## Consolidação

Após os passos retornarem, entregue:

```markdown
## Artigo SEO: [Tópico]

Primary keyword: [keyword] | Intent: [intent] | Word count: [N]

### Keyword Map (de mos-research)
| Tipo | Keyword | Volume | Dificuldade | Placement |
|------|---------|--------|-------------|-----------|
| Primary | [...] | [...] | [...] | Title, H1, URL, primeiros 100 |
| Secondary | [...] | [...] | [...] | H2 |
| Long-tail | [...] | [...] | [...] | H3, FAQ |

### SERP Insights (de mos-research)
[Top 5 ranqueando + gaps + oportunidades + ângulo recomendado]

### Meta Tags (de mos-seo)
- Title tag (X chars): [...]
- Meta description (X chars): [...]
- URL slug: /[slug]

### Article Outline
[H1 + estrutura H2/H3 completa]

### Full Article
[Artigo completo, intro + body + conclusão]

### Headline + CTA (se passo 3)
- Headline recomendada: [...]
- 4 variações alternativas: [...]
- CTA recomendado: [...]
- 2 variações alternativas: [...]

### SEO Checklist
[Checklist completo de validação]

### Internal Linking + Image Suggestions
[Tabelas com sugestões]

### FAQ Schema
[FAQ pronto pra schema markup]

### Próximos passos
- Content cluster strategy ao redor deste artigo
- Variações de title pra A/B test
- Brief de imagens/gráficos
```

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Sem `—`, sem "brutal", sem CAPS gratuito
- Acentuação PT-BR correta em todo o artigo
- Primary keyword nos primeiros 100 palavras
- Headings em hierarquia lógica (sem pular níveis)
- Char limits de title/meta respeitados
- Fact-check via WebSearch para cada stat/citação/case (CONFIRMADO/PROVÁVEL/NÃO USAR)

## Por que sequencial obrigatório

`mos-seo` sem research entrega artigo bonito que não ranqueia (chuta keywords, ignora SERP atual, perde gaps). `mos-research` primeiro mapeia o terreno real (volume, dificuldade, top concorrentes, snippets em aberto) e o `mos-seo` constrói por cima. O passo 3 com `mos-copy` é opcional mas tipicamente +20% de CTR no SERP.
