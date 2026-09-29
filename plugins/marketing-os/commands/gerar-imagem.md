---
description: "Cria o prompt otimizado de imagem para Midjourney, DALL-E, Flux, Ideogram, Leonardo ou Stable Diffusion, sem gerar a imagem. Use quando pedirem prompt de imagem. Imagem pronta (PNG): /renderizar-imagem."
argument-hint: "<o que a imagem mostra e a ferramenta, ex: 'foto de produto para Flux' ou 'ilustração 9:16 para Midjourney'>"
context: fork
agent: mos-ai-tools
background: false
---

# /gerar-imagem: Prompt para IA gerar imagem

> **Piloto da ADR-0007.** Este command roda direto dentro do agent `mos-ai-tools` (`context: fork`): a plataforma garante o dispatch, sem depender de o orquestrador chamar o Agent. O texto abaixo é a tarefa do agent. No ChatGPT Work e no Codex, que não têm subagent, execute a mesma tarefa.

Pedido do usuário: $ARGUMENTS

## Tarefa

Crie o prompt otimizado de imagem para o pedido acima.

1. **Pedido incompleto**: se não estiver claro o que a imagem deve mostrar, responda apenas com as perguntas que faltam (assunto, uso, ferramenta, proporção) e pare. Você não vê a conversa anterior, então não suponha o que foi combinado antes.
2. **Marca**: se existir `workspace/brand/perfil.md`, respeite paleta, tom visual e proibições.
3. **Ferramenta padrão** quando não informada: Midjourney para arte e conceito, Flux para fotorrealismo.
4. **Parâmetros**: use a sintaxe atual da ferramenta escolhida (ex: `--ar`, `--v`, `--s` no Midjourney) e não misture sintaxe entre ferramentas.

## Saída (exatamente neste formato)

```markdown
## Prompt para [Ferramenta]

Assunto: [assunto] | Uso: [uso] | Proporção: [proporção] | Estilo: [estilo]

### Prompt principal
[prompt completo, com parâmetros quando a ferramenta usa]

### Variações
**A** (outro ângulo ou perspectiva): [prompt]
**B** (outro estilo): [prompt]
**C** (outro clima): [prompt]

### Negative prompt (se a ferramenta usa)
[exclusões: blurry, watermark, text etc.]

### Dicas para esta ferramenta
- [dica 1]
- [dica 2]
- [dica 3]

### Como iterar
- Para mais [X]: acrescente "[termo]"
- Para menos [Y]: tire "[termo]" ou mande para o negative
```

## Quality Gates

Aplique os gates globais do SKILL.md do Marketing OS ao texto que envolve o prompt: sem travessão, sem "brutal", sem CAPS gratuito, PT-BR acentuado. Escolha um idioma para o texto do prompt (PT-BR ou inglês) e mantenha.

## Depois da entrega (o orquestrador oferece)

1. Gerar a imagem de fato com `/renderizar-imagem`
2. Variações para outro clima ou estilo
3. O mesmo assunto adaptado para outra ferramenta
4. Série visual coerente (3 a 5 prompts com a mesma identidade)
5. Prompt de vídeo (Veo, Sora, Kling, Runway) com a mesma cena

## Por que fork

O command é puramente "entregue o prompt do especialista": todo o input vem do pedido e dos arquivos do projeto, sem aprovação humana no meio. É o caso em que rodar direto dentro do `mos-ai-tools` elimina o risco de o orquestrador responder inline ou errar o nome do agent.
