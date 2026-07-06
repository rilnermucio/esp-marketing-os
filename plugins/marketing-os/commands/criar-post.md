---
description: Create a complete social media post optimized for the specified platform. Dispatches native Claude Code subagents (mos-social, mos-copy, optionally mos-research) in parallel or sequence for maximum quality.
argument-hint: "<platform and topic, e.g., 'Instagram post about productivity tips'>"
---

# /criar-post: Create Social Media Post (Dispatch-Based)

Create a complete, platform-optimized social media post by orchestrating native Claude Code subagents.

## Invocation Protocol (how this command runs)

This command does NOT produce content inline. It **dispatches specialist subagents** via the `Agent` tool and consolidates their outputs for the user.

### Required inputs (ask if missing)

1. **Platform** (required): Instagram, LinkedIn, Twitter/X, TikTok, Facebook, or Pinterest
2. **Topic/Theme** (required): What the post is about
3. **Goal** (required): Engagement, reach, traffic, conversion, or brand awareness
4. **Audience** (optional): Target demographic and psychographic details
5. **Tone** (optional): Professional, casual, inspirational, educational, entertaining
6. **Format** (optional): Feed post, carousel, story, reel, thread, etc.
7. **CTA** (optional): Desired action from the audience

### Dispatch Decision Tree

```
Briefing recebido
  ├── Tópico genérico ou novo nicho? (sim)
  │     └── Dispatch PARALELO: mos-research + mos-copy
  │         (research valida claims/tendências em paralelo com geração de hooks)
  │
  ├── Tópico conhecido + precisa de post polido? (sim)
  │     └── Dispatch SIMPLES: mos-social (ele já coordena com mos-copy via knowledge)
  │
  ├── Precisa de artigo longo + post promocional? (sim)
  │     └── Dispatch SEQUENCIAL: mos-seo (artigo) → mos-social (post promo do artigo)
  │
  └── Pede variações A/B de copy já existente?
        └── Dispatch SIMPLES: mos-copy (variações)
```

### Exemplo de dispatch paralelo (single message, múltiplas Agent calls)

Quando o briefing é novo/amplo:

```
Em um único message, invoque em paralelo:

- Agent(subagent_type: "mos-research", prompt: "Pesquisa rápida: tendências atuais de [tema], concorrentes ativos em [plataforma] BR, dores do público [audiência], dados/estatísticas relevantes dos últimos 90 dias. Considere memory existente do cliente neste projeto. Retorne research brief compacto.")

- Agent(subagent_type: "mos-social", prompt: "Crie post [plataforma] sobre [tema]. Audiência: [descrição]. Tom: [tom]. Goal: [goal]. Format: [format]. CTA: [cta]. Considere memory existente do cliente neste projeto. Aplique schema padrão + 3 hooks + variações A/B + hashtags + horário + enquete de engajamento.")
```

Se `mos-social` ainda não existir (durante migração), fallback:

```
- Agent(subagent_type: "mos-copy", prompt: "Post para [plataforma]: hook + copy + CTA + variações A/B. Tópico: [tema]. Considere memory existente do cliente neste projeto...")
```

### Exemplo de dispatch sequencial

Quando precisa de research ANTES de copy (research informa os hooks):

```
Passo 1: Agent(subagent_type: "mos-research", prompt: "...")
  → Aguarde research brief

Passo 2: Agent(subagent_type: "mos-social", prompt: "..., usando este research: [colar brief]")
  → Post final
```

## Consolidação do Output

Após os agents retornarem, consolide em entrega única:

```markdown
## Post de Redes Sociais

Plataforma: [Platform name]
Goal: [Engagement | Reach | Traffic | Conversion]
Format: [Post type]

### Hooks (3 opções)

1. [Hook A: recomendado]
2. [Hook B: ângulo curiosidade]
3. [Hook C: ângulo benefício]

### Post Completo

[Conteúdo final formatado para a plataforma]

### CTA

[Call to action claro]

### Hashtags

[Lista otimizada para a plataforma]

### Variações A/B

**Variação 1: [ângulo]**
[Texto alternativo]

**Variação 2: [ângulo]**
[Texto alternativo]

### Enquete para Engajamento (obrigatório social)

Tipo: [binária | qual-você-faz | escala | desafio | curiosidade]
Texto: [Pergunta pronta para publicar]

### Recomendações de Publicação

Melhor horário: [Dia + hora baseado na plataforma]
Engajamento esperado: [Benchmark]
Repurposing: [Como adaptar para outras plataformas]

### Research Context (se houver)

Fontes consultadas: [Lista]
Dados verificados: [CONFIRMADO | PROVÁVEL]
Tendências ativas: [Lista com datas]

### AI Image Prompt (se aplicável)

[Prompt otimizado para geração visual]
```

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Sem `—`, sem "brutal", sem CAPS gratuito
- Sem aspas em roteiros/falas (escrever direto)
- Máximo 1-2 emojis (preferir zero)
- Acentuação PT-BR correta
- Fatos verificados via WebSearch (CONFIRMADO/PROVÁVEL)
- Enquete obrigatória (conteúdo social)
- Adequação à plataforma (chars, formato, hashtags)

Se QUALQUER gate falhar, refaça antes de entregar.

## Follow-up ao Usuário

Após entregar, pergunte:

"Quer que eu:
1. Crie variações com outros ângulos de hook?
2. Adapte para outras plataformas (cross-platform)?
3. Gere prompt de IA para a imagem?
4. Transforme em carrossel multi-slide?
5. Crie sequência de stories derivada deste post?"

## Observações

- **Nunca** produza o post inline sem dispatchar. O dispatch garante profundidade, contexto isolado e quality gates consistentes.
- **Prefira paralelo** sobre sequencial sempre que não houver dependência real. 3 Agents em paralelo custam ~1x o tempo de 1 call sequencial (mais tokens, menos latência).
- **Sempre inclua enquete** em conteúdo social. Regra do SKILL.md.
