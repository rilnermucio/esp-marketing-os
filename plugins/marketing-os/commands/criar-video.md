---
description: Cria roteiro de vídeo (YouTube long-form, Reels, TikTok, Shorts ou VSL). Para VSL completa, dispatcha workflow #9 (mos-storytelling + mos-copy + mos-video). Para outros formatos, dispatch simples ou paralelo conforme o caso.
argument-hint: "<formato e tema, ex: 'Reels 90s sobre produtividade' ou 'VSL pra curso de marketing'>"
---

# /criar-video: Roteiro de Vídeo

Cria roteiro orquestrando subagents conforme tipo de vídeo. Roteamento abaixo segue padrões do `skills/marketing-os/SKILL.md`.

## Required inputs (ask if missing)

1. **Formato** (obrigatório): YouTube long-form | YouTube Shorts | Reels | TikTok | VSL (Video Sales Letter) | webinar
2. **Tema/Tópico** (obrigatório)
3. **Duração alvo** (obrigatório)
4. **Audiência** (opcional): quem assiste
5. **Goal** (obrigatório): educar | entreter | converter (vendas) | branding
6. **CTA** (opcional): inscrever, comprar, comentar, etc.

## Dispatch, roteamento por formato

### Caso A: VSL (Video Sales Letter), Workflow #9 dedicado

VSLs precisam de copy de venda + storytelling + ciência de retenção em vídeo simultaneamente. Dispatch paralelo:

```
- Agent(subagent_type: "mos-storytelling", prompt: "Arco narrativo da VSL para [produto]: hook → problema → vilão → solução → prova → oferta → urgência. Aplicar hero's journey adaptado pra venda.")

- Agent(subagent_type: "mos-copy", prompt: "Estrutura de copy de venda no formato VSL: headline, big idea, mecanismo único, anti-avatar, stack value, garantia, FAQ falado. Audiência: [audiência], ticket: [ticket]. Considere memory existente do cliente neste projeto.")

- Agent(subagent_type: "mos-video", prompt: "Ciência de retenção em VSL de [duração]: timestamps de queda esperados, transições, B-roll, ritmo, padrões de re-engajamento. Adaptar pro nicho [nicho].")
```

Fase 2: consolidar em roteiro único (texto narrado + cues visuais + timing de seções) + quality gates de substância (promessas com backup, garantia clara) + sugestão de testes A/B em hook e mecanismo único.

### Caso B: YouTube long-form (educacional, entrevista, tutorial)

Dispatch simples na maioria dos casos:

```
- Agent(subagent_type: "mos-video", prompt: "Roteiro YouTube [duração] sobre [tema]: hook (0-15s), agenda, conteúdo de valor estruturado em capítulos, retenção patterns, CTA, thumbnail concept. Audiência: [audiência], goal: [goal].")
```

Se precisar de validação de tópico/concorrência antes:

```
Paralelo:
- Agent(subagent_type: "mos-research", prompt: "Mapear vídeos top-performing sobre [tema] no YouTube BR, hooks usados, durações comuns, ângulos diferenciados. Considere memory existente do cliente neste projeto.")
- Agent(subagent_type: "mos-video", prompt: "[após receber research] Roteiro YouTube...")
```

### Caso C: Reels / Shorts / TikTok

Dispatch simples:

```
- Agent(subagent_type: "mos-video", prompt: "Roteiro [formato] de [duração]s sobre [tema]: hook nos primeiros 1-3s, conteúdo de alto ritmo, CTA, padrões de retenção da plataforma. Aplicar swipe files de hooks-reels.")
```

Para Reels com clone de voz:

```
- Agent(subagent_type: "mos-video", prompt: "Roteiro Reels no estilo de [creator/copywriter de assets/clones/], aplicar voice profile correspondente.")
```

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Sem `—`, sem "brutal", sem CAPS gratuito
- Sem aspas em falas/roteiros (escrever direto)
- Acentuação PT-BR correta
- Compliance regulatório por nicho
- Para VSL: gates de substância (promessas com backup, sem linguagem absoluta, garantia clara)

## Consolidação

```markdown
## Roteiro: [Tema]: [Formato] [duração]

### Hook (primeiros segundos)
[Texto exato pro creator falar]

### Estrutura
[Bloco a bloco com timestamps]

### Roteiro Completo
[Texto narrado por seção, com cues visuais entre colchetes]

### Thumbnail / Capa (se aplicável)
[Conceito + texto + composição]

### CTA
[Ação clara + onde colocar no vídeo]

### Próximos Passos
- Adaptação pra plataformas adicionais (cross-platform)
- B-roll / cues visuais detalhados
- Music/SFX sugestão
```

## Por que essa orquestração

Vídeos curtos (Reels/Shorts) são naturalmente território do `mos-video`. VSLs são caso composto, copy de venda + arco narrativo + ciência de retenção têm que casar; falta de qualquer um quebra a peça toda.
