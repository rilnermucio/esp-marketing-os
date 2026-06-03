---
description: Reverse-engineer videos (YouTube long, Shorts, Reels, TikTok, VSL) extracting hooks, CTAs, retention, structure. Dispatches mos-video, with optional mos-research handoff for unknown creators.
argument-hint: "<video URL or transcript, e.g., 'https://youtube.com/watch?v=...' or 'analyze MrBeast latest video'>"
---

# /analisar-video: Análise de Vídeo (Dispatch sequencial opcional)

Analisa vídeo extraindo hooks, estrutura, retention, CTAs, narrativa, técnica. Despacha `mos-video` (com `mos-research` antes só quando o creator é desconhecido e o briefing pede análise profunda).

## Required inputs (ask if missing)

1. **Video source** (obrigatório): URL, transcript ou descrição do vídeo
2. **Analysis focus** (opcional): hooks, retention, CTAs, storytelling, editing, all (default: all)
3. **Content type** (opcional): YouTube long-form, Shorts, Reels, TikTok, VSL (autodetectar pela URL se possível)
4. **Purpose** (opcional): aprender, replicar estilo, melhorar próprio conteúdo, análise competitiva
5. **Your niche** (opcional): pra contextualizar insights e adaptation blueprint
6. **Creator** (opcional): nome do creator/canal, se conhecido

## Dispatch Decision Tree

```
Briefing recebido
  ├── Default (creator conhecido OU análise rápida)
  │     └── Dispatch SIMPLES: mos-video
  │
  └── Análise profunda + creator desconhecido pelo orquestrador
        └── Dispatch SEQUENCIAL: mos-research → mos-video
            (research dá contexto de canal/audiência/posicionamento;
             video usa esse contexto pra interpretar escolhas táticas)
```

### Dispatch simples (caso comum)

```
Agent(subagent_type: "mos-video", prompt: "Análise reverse-engineered do vídeo: [URL ou transcript]. Plataforma: [content type]. Focus: [focus]. Purpose: [purpose]. Nicho do user: [niche]. Entregue: hook breakdown (tipo, primeiras palavras, score), structure map com timestamps, retention techniques (open loops, pattern interrupts, curiosity gaps), CTA catalog, storytelling analysis (arco, emoção, transformação), technical analysis (cuts, B-roll, thumbnail, título), top 5 técnicas replicáveis e adaptation blueprint pro nicho do user. Score geral 1-10.")
```

### Dispatch sequencial (creator desconhecido + análise profunda)

```
Passo 1:
Agent(subagent_type: "mos-research", prompt: "Contexto rápido sobre o creator/canal [nome/URL]: posicionamento, audiência, ticket médio se vendedor, conteúdo recorrente, conquistas verificáveis. WebSearch + análise pública. Considere memory existente do cliente neste projeto. Retorne brief compacto pra contextualizar análise tática do vídeo.")
  → Aguarde research brief

Passo 2:
Agent(subagent_type: "mos-video", prompt: "Análise reverse-engineered do vídeo: [URL]. Use este contexto do creator: [colar research brief]. [resto igual ao dispatch simples]")
```

`mos-research` tem memory project; `mos-video` não, passe todo o contexto no prompt do segundo.

## Consolidação

Após o(s) agent(s) retornar(em):

```markdown
## Análise: [Título do vídeo ou descrição]

Plataforma: [YouTube / TikTok / Reels / Shorts / VSL] | Duração: [tempo]
Creator: [nome] | Score geral: [X/10]
Best element: [destaque] | Weakest: [ponto fraco]

### Resumo Executivo (2-3 frases)
[Por que funciona ou não funciona]

### Hook Breakdown
- Primeiras palavras: "[exatas]"
- Tipo: [curiosidade | controvérsia | promessa | história | choque]
- Por que funciona: [análise]
- Score: [X/10]
- Hooks alternativos:
  1. "[opção A]"
  2. "[opção B]"
  3. "[opção C]"

### Structure Map (timestamps)
[Mapa completo do vídeo: hook → setup → blocos → climax → CTA → outro]

### Retention Techniques
[Tabela com técnica | timestamp | efeito]
Curva de retenção estimada: [onde caem e por quê]

### CTA Catalog
[Tabela com CTA | timestamp | tipo | placement | quality]

### Storytelling
[Arco narrativo, jornada emocional, transformação prometida vs entregue]

### Technical Analysis
[Cuts/min, B-roll, overlays, áudio, transições, thumbnail, título]

### Top 5 Técnicas Replicáveis
1. [Técnica + como aplicar no nicho do user]
...

### Adaptation Blueprint (pro nicho [niche])
[Recomendações específicas + template de roteiro inspirado]

### Research Context (se Fase research foi rodada)
[Resumo do creator/canal]
```

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Sem `—`, sem "brutal", sem CAPS gratuito, sem aspas em falas (escrever direto)
- Acentuação PT-BR correta
- Fact-check (CONFIRMADO / PROVÁVEL) em qualquer claim sobre métricas, conquistas ou estatísticas do creator

## Follow-up

Pergunte se quer:
1. Roteiro novo usando essa estrutura pro tema do user
2. Variações de hook inspiradas na análise
3. Análise de outro vídeo do mesmo creator (detecção de padrão)
4. Estratégia completa de conteúdo baseada nas técnicas
