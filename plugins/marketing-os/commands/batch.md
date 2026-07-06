---
description: Generate multiple pieces of content at once with hook/angle/framework variation. Routes the batch to N parallel (or sequential when needed) Agent dispatches based on content type.
argument-hint: "<quantity> <type> <theme>, e.g., '10 posts about AI tools' or '5 emails for product launch'"
---

# /batch: Produção em Lote (Roteador Multi-Paralelo)

Roteador que despacha **N Agent calls** em paralelo (ou sequencial quando há dependência), uma por peça do batch, com hook/angle/framework rotacionados pra evitar que tudo saia clone uma da outra.

## Required inputs (ask if missing)

1. **Quantity** (obrigatório): 3, 5, 10, 15, 20, 30
2. **Content type** (obrigatório): posts, carousels, reels scripts, emails, articles, ads, mixed
3. **Theme** (obrigatório): tema central que unifica todas as peças
4. **Platforms** (opcional): Instagram, LinkedIn, TikTok, Twitter/X, email, blog (default: Instagram p/ social)
5. **Audience** (opcional): persona alvo
6. **Tone** (opcional): profissional, casual, educational, entertaining
7. **Clone voice** (opcional): clone de copywriter (Hormozi, Ogilvy, Halbert, Brunson, etc.)
8. **Campaign context** (opcional): faz parte de campanha maior? Qual fase do funil?

## Dispatch Decision Tree (por tipo)

```
posts          → N × Agent(mos-social)         em paralelo (single message)
carousels      → N × workflow #8               cada um = (mos-social + mos-copy + mos-design) em paralelo interno
reels scripts  → N × Agent(mos-video)          em paralelo  (ou mos-social se Reels curtos < 30s)
emails         → N × Agent(mos-email)          em paralelo
articles       → N × (mos-research → mos-seo)  sequencial por peça (research é caro), batches paralelos entre peças
ads            → N × Agent(mos-ads)            em paralelo
mixed          → breakdown da tabela abaixo, dispatchar por bucket em paralelo
```

## Variation Engine (rotacionar a cada peça do batch)

Cada Agent call recebe um conjunto único de hook + angle + framework. Isso evita que as N peças saiam iguais.

### Hook Rotation (1-10)

| # | Hook Type | Template |
|---|-----------|----------|
| 1 | Curiosidade | "Isso mudou tudo sobre como eu [tema]..." |
| 2 | Controvérsia | "Opinião impopular: [afirmação ousada]" |
| 3 | Promessa | "Aqui está exatamente como [resultado]..." |
| 4 | Pergunta | "Por que ninguém fala sobre [tema]?" |
| 5 | História | "[Tempo] atrás, eu estava [ponto de dor]..." |
| 6 | Lista | "[N] coisas que eu gostaria de saber sobre [tema]" |
| 7 | Estatística | "[Dado impactante] e aqui está o porquê..." |
| 8 | Desafio | "Eu tentei [ação] por [tempo] e isso aconteceu..." |
| 9 | Bastidor | "O que eu não mostro sobre [tema]..." |
| 10 | Predição | "Em [ano/tempo], [previsão ousada]..." |

### Angle Rotation

| Angle | Foco | Best for |
|-------|------|----------|
| Educacional | Como fazer, tutorial | Autoridade |
| Inspiracional | Resultados, transformação | Engajamento |
| Contrário | Desmistificação, mitos | Viralidade |
| Pessoal | História própria | Conexão |
| Dados | Estatísticas, pesquisa | Credibilidade |
| Prático | Dicas rápidas, checklist | Salvamentos |
| Tendência | Novidade, trend | Alcance |
| Comparativo | Antes/depois, X vs Y | Clareza |

### Framework Rotation

PAS · AIDA · BAB · Education · Story (alternar a cada peça)

## Dispatch (por tipo)

### Posts (paralelo, single message com N Agent calls)

```
Para cada peça i de 1..N:
  - Agent(subagent_type: "mos-social", prompt: "Post [plataforma] sobre [tema].
    Hook tipo: [Hook #i da rotação]
    Angle: [Angle #i]
    Framework: [Framework #i]
    Audiência: [audiência]. Tom: [tom]. Clone: [clone se aplicável].
    Aplicar quality gates globais. Incluir: hook + body + CTA + hashtags + sugestão de enquete.
    Considere memory existente em .claude/agent-memory/marketing-os-mos-social/ se houver.")
```

### Carousels (paralelo de workflows #8)

Para cada peça do batch, executar **internamente** o workflow #8 (mos-social + mos-copy + mos-design). Como cada workflow já dispatcha 3 agents, batches grandes (10+) podem ser sequenciais em chunks de 3 pra não saturar.

```
Para cada peça i de 1..N (em chunks de 2-3 paralelos):
  Workflow #8 com tipo da rotação (how-to, myths, checklist, before/after, tips)
  - Tema: [tema]
  - Tipo do carrossel #i: [varia por peça]
```

### Reels scripts (paralelo)

```
Para cada peça i de 1..N:
  - Agent(subagent_type: "mos-video", prompt: "Roteiro Reel/TikTok 30-60s sobre [tema].
    Hook (3s primeiros): [Hook #i da rotação]
    Formato: [talking head | text-on-screen | tutorial | story] (varia por peça)
    Estrutura: hook (3s) + content (15-55s) + CTA.
    Aplicar quality gates + sugestão de enquete.")
```

### Emails (paralelo)

```
Para cada peça i de 1..N:
  - Agent(subagent_type: "mos-email", prompt: "Email sobre [tema].
    Subject formula: [varia: pergunta | urgência | curiosidade | benefício | controvérsia]
    Estrutura: [varia: PAS | AIDA | BAB | Story | Education]
    Inclui: subject line + preview text + body + CTA.
    Audiência: [audiência]. Tom: [tom]. Clone: [clone se aplicável].
    Considere memory em .claude/agent-memory/marketing-os-mos-email/ se houver.")
```

### Articles (sequencial por peça, research é caro)

```
Para cada peça i de 1..N:
  Passo 1: Agent(subagent_type: "mos-research", prompt: "Research compacto sobre [sub-ângulo #i de [tema]]")
  Passo 2: Agent(subagent_type: "mos-seo", prompt: "Artigo SEO sobre [sub-ângulo #i] usando research: [colar].
    Formato: [varia: listicle | how-to | guide | case study]
    Inclui: title + meta description + outline + key sections + headings + internal linking.")

(N peças podem rodar em chunks de 2-3 sequencias paralelas pra acelerar)
```

### Ads (paralelo)

```
Para cada peça i de 1..N:
  - Agent(subagent_type: "mos-ads", prompt: "Anúncio Meta Ads sobre [tema].
    Hook: [Hook #i]
    Benefit angle: [varia: aspiracional | dor | prova | curiosidade]
    Audience segment: [varia conforme funil]
    Inclui: headline + primary text + description + CTA + creative direction.
    Aplicar quality gates + compliance.")
```

### Mixed Batch (despachar por bucket em paralelo)

Para `/batch mixed`, breakdown padrão (ajustar conforme briefing):

| Quantity | Type | Bucket dispatch | Platform | Purpose |
|----------|------|-----------------|----------|---------|
| 5 | Posts | 5 × mos-social | Instagram | Awareness |
| 3 | Carousels | 3 × workflow #8 | Instagram | Education |
| 3 | Reels scripts | 3 × mos-video | Instagram/TikTok | Engagement |
| 5 | Emails | 5 × mos-email | Email | Nurture |
| 2 | Articles | 2 × (mos-research → mos-seo) | Blog | SEO |
| 2 | Ad copy | 2 × mos-ads | Meta Ads | Traffic |

Cada bucket vira um conjunto de Agent calls em paralelo. Buckets independentes podem rodar simultaneamente.

## Memory note

Vários dos agents têm memory project (`.claude/agent-memory/marketing-os-<agent>/`). Em batches do mesmo cliente, **mencione no prompt** que considere memory existente, evita repetir hooks já usados, mantém consistência de tom, e respeita restrições de compliance previamente registradas.

## Consolidação do output

```markdown
## Batch Content Production

Tema: [tema]
Quantidade: [N] peças
Plataformas: [plataformas]
Tipo: [content type]
Clone: [clone se aplicável]

### Tabela resumo
| # | Type | Hook | Angle | Framework | Platform | Status |
|---|------|------|-------|-----------|----------|--------|
| 1 | [...] | [...] | [...] | [...] | [...] | [pronto] |
| ... | ... | ... | ... | ... | ... | ... |

### Peça #1
**Plataforma:** [...]
**Hook tipo:** [...] · **Angle:** [...] · **Framework:** [...]

[Output completo do agent dispatchado: hook + body + CTA + hashtags + enquete (se social)]

---

### Peça #2
[...]

---

[N peças...]

---

### Calendar placement (sugestão)
| Semana | Seg | Ter | Qua | Qui | Sex | Sáb | Dom |
|--------|-----|-----|-----|-----|-----|-----|-----|
| 1 | #1 | #2 |, | #3 | #4 |, | #5 |
| 2 | #6 | #7 |, | #8 | #9 |, | #10 |

**Best posting times:** Instagram [...], LinkedIn [...], TikTok [...]

### Estatísticas do batch
| Métrica | Valor |
|---------|-------|
| Total de peças | [N] |
| Hooks únicos usados | [X] |
| Angles únicos | [X] |
| Frameworks aplicados | [X] |
| Dias estimados de conteúdo | [N] |
```

## Quality Gates (antes de entregar o batch inteiro)

Aplicar gates globais do `skills/marketing-os/SKILL.md` em **toda peça**:
- Sem `—`, sem "brutal", sem CAPS gratuito
- Sem aspas em roteiros/falas
- Máximo 1-2 emojis por peça (preferir 0)
- Acentuação PT-BR correta
- Enquete obrigatória em conteúdo social
- Compliance regulatório se nicho saúde/finanças/suplementos
- Hooks não-repetidos entre peças (Hook Rotation garante isso)

Se alguma peça falhar nos gates, refaça **só essa peça** (re-dispatch único), não o batch todo.

## Follow-up ao usuário

"Quer que eu:
1. Gere mais peças com hooks/angles diferentes?
2. Crie direção visual de cada peça? (dispatch mos-design por peça)
3. Adapte o batch pra plataformas adicionais?
4. Crie variações A/B das top 3 peças? (dispatch mos-ab-testing)
5. Publique tudo num calendário Notion? (roteia pra /publicar-notion)"

## Por que dispatch multi-paralelo

Batch executado inline (1 LLM gerando 10 posts) sai homogêneo: mesmo ritmo, mesmo vocabulário, mesma estrutura. Dispatchar N agents com prompts variando hook+angle+framework garante diversidade real. Cada agent tem context isolado e aplica os gates do seu domínio.

Para batches grandes (15+), considerar chunks de 3-5 paralelos por vez pra não estourar limites e manter latência razoável.
