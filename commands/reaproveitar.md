---
description: "Transforma uma peça pilar (live, aula, podcast, vídeo, artigo) em várias peças para outras plataformas, com a mesma tese e a mesma voz. Use quando pedirem para reaproveitar, fatiar ou repicar um conteúdo em outros formatos."
argument-hint: "<fonte: texto, transcrição ou link> [plataformas e quantidade]"
---

# /reaproveitar: De uma fonte pilar para várias peças

Uma live, aula, podcast, vídeo longo ou artigo vira um conjunto de peças nativas para outras plataformas, sem perder a tese nem a voz. O método está em "Reaproveitamento 1→N" na KB de social (`${CLAUDE_PLUGIN_ROOT}/subagents/social-agent.md`).

## Inputs (pergunte o que faltar)

1. **Fonte** (obrigatório): texto, transcrição ou link. Vídeo ou áudio sem transcrição: peça a transcrição ou um arquivo de legenda.
2. **Plataformas e formatos**: ex: 5 posts de Instagram, 1 carrossel, 3 cortes de Reels, 1 newsletter, 1 artigo.
3. **Objetivo**: alcance, leads, venda ou autoridade.
4. **Oferta ou CTA** para onde as peças levam.

Se existir `workspace/brand/perfil.md`, use voz, proibições e canais de lá.

## Dispatch, Fase 1 (mapa da fonte)

```
Agent(subagent_type: "marketing-os:mos-social", prompt: "Monte o mapa de reaproveitamento desta fonte seguindo 'Reaproveitamento 1→N' da sua KB: tese central em uma frase, 5 a 10 ideias-chave com o trecho de origem, falas fortes, números e provas, histórias, e os tempos de cada trecho se a fonte for vídeo ou áudio. Não escreva peças ainda. FONTE: [texto ou transcrição]")
```

## Fase 2 (em paralelo, só os formatos pedidos)

```
Agent(subagent_type: "marketing-os:mos-social", prompt: "Com o mapa abaixo, escreva [N] posts e [N] carrosséis para [plataformas]: uma ideia-chave por peça, gancho diferente em cada uma, um CTA para [oferta]. Inclua sugestão de enquete. MAPA: [mapa da Fase 1]")

Agent(subagent_type: "marketing-os:mos-video", prompt: "Com o mapa abaixo, proponha [N] cortes de Reels ou Shorts: trecho de origem com tempo de início e fim, gancho dos primeiros segundos, legenda na tela e CTA. MAPA: [mapa da Fase 1]")

Agent(subagent_type: "marketing-os:mos-email", prompt: "Com o mapa abaixo, escreva uma newsletter que resume a tese e leva para [fonte ou oferta]: subject lines, preheader, corpo e CTA. MAPA: [mapa da Fase 1]")

Agent(subagent_type: "marketing-os:mos-seo", prompt: "Com o mapa abaixo, estruture um artigo derivado para a keyword [keyword]: intenção, outline, title e meta description, usando as provas da fonte. MAPA: [mapa da Fase 1]")
```

## Consolidação

1. Matriz: ideia-chave, formato, plataforma, gancho, CTA e data sugerida.
2. As peças, agrupadas por plataforma.
3. Ordem de publicação e intervalo entre peças.
4. Enquete sugerida para as peças de social.

## Quality Gates

Aplique os gates globais do SKILL.md do Marketing OS em todas as peças (travessão, "brutal", antítese, acentuação, até 2 emojis). Confira que nenhuma peça inventou número ou fala que não está na fonte e que as aberturas não se repetem.

## Por que esse dispatch

O mapa vem antes porque é ele que garante a mesma tese em todas as peças; sem ele, cada agent resume a fonte do seu jeito. Depois, cada formato vai para o especialista dele em paralelo, já que as peças não dependem umas das outras.
