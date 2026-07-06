---
description: Create a complete Instagram or LinkedIn carousel with hook slide, content slides, CTA, caption, and visual direction. Dispatches mos-social + mos-copy + mos-design in parallel (workflow #8).
argument-hint: "<topic and type, e.g., '10 productivity tips' or 'storytelling carousel about my journey'>"
---

# /criar-carrossel: Carrossel Completo (Workflow #8)

Cria carrossel orquestrando 3 subagents em paralelo conforme **workflow #8** documentado em `skills/marketing-os/SKILL.md`.

## Required inputs (ask if missing)

1. **Tópico** (obrigatório)
2. **Plataforma** (obrigatório): Instagram ou LinkedIn
3. **Tipo** (obrigatório): educativo, lista, storytelling, comparação, how-to, ou myth-busting
4. **Audiência** (opcional): cargo, faixa, dor principal
5. **Goal** (opcional): saves, shares, follows, traffic
6. **Slide count** (opcional): 5-10, default 8
7. **Tom** (opcional): profissional, casual, bold, inspiracional

## Dispatch (paralelo, single message)

Em **um único message**, invoque os 3 agents simultaneamente:

```
- Agent(subagent_type: "mos-social", prompt: "Estrutura de carrossel pra [plataforma], tipo [tipo], [N] slides: hook na capa, padrão de retenção entre slides, ritmo de revelação de informação, CTA final. Tópico: [tópico]. Audiência: [audiência]. Considere memory existente do cliente neste projeto.")

- Agent(subagent_type: "mos-copy", prompt: "Texto de cada um dos [N] slides para carrossel sobre [tópico]: hook na capa, body com peso/leveza alternada, CTA específico no slide final. Audiência: [audiência]. Considere memory existente do cliente neste projeto. Aplicar quality gates globais (sem travessão, sem 'brutal', PT-BR correto).")

- Agent(subagent_type: "mos-design", prompt: "Direção visual para carrossel [plataforma] de [N] slides: paleta, tipografia, hierarquia, formato de capa vs body, consistência visual entre slides. Nicho: [nicho/tema]. Considere memory existente do cliente neste projeto.")
```

**Opcional (paralelo, mesma message):**

```
- Agent(subagent_type: "mos-ai-tools", prompt: "Prompts pra IA gerar imagem da capa do carrossel (Midjourney/Flux/Ideogram) com referência do briefing visual: [resumir mos-design output ou tópico]")
```

## Consolidação

Após os agents retornarem:

```markdown
## Carrossel: [Tópico]

Plataforma: [Instagram | LinkedIn] | Tipo: [tipo] | Slides: [N]

### Estrutura (de mos-social)
[Estrutura slide a slide com função de cada um]

### Conteúdo dos Slides (de mos-copy)

**Slide 1 (Capa)**: Hook
[texto]

**Slide 2-N**: Body
[texto de cada slide]

**Slide [Final]**: CTA
[texto + ação]

### Direção Visual (de mos-design)
[Paleta + tipografia + hierarquia + spec por tipo de slide]

### Caption + Hashtags
[Caption + hashtags otimizadas pra plataforma]

### Enquete (obrigatório social)
Tipo: [binária | qual-você-faz | escala | desafio | curiosidade]
Texto: [Pergunta pronta]

### Prompt IA para Capa (se aplicável)
[Prompt do mos-ai-tools]

### Próximos passos
- Repurposing pra Reel ou stories
- Variação A/B de capa
- Horário ideal de publicação
```

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Sem `—`, sem "brutal", sem CAPS gratuito
- Acentuação PT-BR correta
- Enquete obrigatória presente
- Compliance regulatório se nicho saúde/finanças/suplementos

## Por que esse dispatch composto

`mos-social` sem `mos-copy` = texto fraco. `mos-copy` sem `mos-design` = visual genérico. `mos-design` sem `mos-social` = sem entender ritmo de retenção da plataforma. Os 3 em paralelo evitam que o carrossel saia capenga em alguma camada.
