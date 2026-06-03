---
description: Generate optimized AI image prompts for Midjourney, DALL-E, Flux, Ideogram, Leonardo or Stable Diffusion. Dispatches mos-ai-tools (single agent).
argument-hint: "<description and tool, e.g., 'product photo for Flux' or 'illustration for Midjourney 9:16'>"
---

# /gerar-imagem: Prompt para IA gerar imagem (Dispatch simples)

Cria prompt otimizado para geração de imagem por IA, despachando o subagent especialista. Não produz prompt inline.

## Required inputs (ask if missing)

1. **Subject** (obrigatório): o que a imagem deve mostrar
2. **Purpose** (opcional): social media, website, produto, marketing, arte
3. **Tool** (opcional): Midjourney, DALL-E 3, Flux, Ideogram, Leonardo, Stable Diffusion (default: Midjourney pra arte/conceito, Flux pra fotorrealismo)
4. **Style** (opcional): photorealistic, illustration, 3D, minimalist, cinematic, etc.
5. **Aspect ratio** (opcional): 1:1, 16:9, 9:16, 4:3 ou custom
6. **Mood** (opcional): profissional, lúdico, dramático, warm, minimal

## Dispatch (simples, single agent)

```
Agent(subagent_type: "mos-ai-tools", prompt: "Gere prompt otimizado para [tool] do subject: [subject]. Purpose: [purpose]. Style: [style]. Aspect ratio: [ar]. Mood: [mood]. Entregue: 1 prompt principal completo (com parâmetros tool-specific tipo --ar/--v/--s pra Midjourney quando aplicável), 3 variações (ângulo/estilo/mood diferentes), negative prompt quando aplicável, e 3-5 dicas tool-specific pra extrair melhor resultado. Estruture em markdown.")
```

`mos-ai-tools` não tem memory project, passe todo o contexto no prompt.

## Consolidação

Após o agent retornar:

```markdown
## Prompt para [Tool]

Subject: [subject] | Purpose: [purpose] | Aspect ratio: [ar] | Style: [style]

### Prompt Principal
[Prompt completo, com parâmetros se aplicável]

### Variações (3)
**Variação A**: [ângulo/perspectiva diferente]
[Prompt]

**Variação B**: [estilo diferente]
[Prompt]

**Variação C**: [mood diferente]
[Prompt]

### Negative Prompt (se aplicável)
[Lista de exclusões: blurry, watermark, text, etc.]

### Dicas tool-specific
- [Dica 1]
- [Dica 2]
- [Dica 3]

### Iteração sugerida
- Pra mais [X]: adicionar "[keyword]"
- Pra menos [Y]: remover "[keyword]" ou jogar pro negative
- Pra trocar estilo: substituir "[atual]" por "[alternativo]"
```

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Texto descritivo do prompt em PT-BR ou EN consistente (escolha um e mantenha)
- Sem `—`, sem "brutal", sem CAPS gratuito no texto que envolve o prompt
- Acentuação PT-BR correta nos títulos e descrições

## Follow-up

Pergunte ao usuário se quer:
1. Variações para outro mood/estilo
2. Adaptar o mesmo subject para outra tool
3. Série visual coerente (3-5 prompts com mesma identidade)
4. Prompt para vídeo (Veo, Sora, Kling, Runway) com mesma cena

## Por que dispatch (mesmo sendo simples)

Centraliza a lógica de prompt engineering no `mos-ai-tools` (que conhece parâmetros, swipe files de estilos, e padrões por tool). Evita que o orquestrador chute parâmetros desatualizados ou misture sintaxe entre tools.
