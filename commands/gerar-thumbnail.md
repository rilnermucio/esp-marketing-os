---
description: Turn the mos-video Thumbnail Brief into an actual 16:9 image. Dispatches mos-video (brief) + mos-ai-tools (prompt do fundo SEM texto), renderiza via skill de imagem e aplica o texto com thumbnail_composer.py (overlay tipográfico legível).
argument-hint: "<vídeo/tema + texto da thumb, ex: 'vídeo sobre juros compostos, texto: NUNCA TE CONTARAM ISSO'>"
---

# /gerar-thumbnail: Thumbnail Brief vira imagem 16:9 (Dispatch + Execução)

Gera a thumbnail de verdade, em duas camadas separadas por design: o FUNDO vem do gerador de imagem (sem texto, porque IA renderiza texto mal) e o TEXTO entra por overlay tipográfico determinístico (`scripts/thumbnail_composer.py`, stroke grosso + faixa de contraste + quebra automática, 1280x720).

## Required inputs (ask if missing)

1. **Tema/vídeo** (obrigatório): sobre o que é o vídeo (ou o roteiro/título já criado)
2. **Texto da thumb** (opcional): se não vier, o mos-video propõe (3-5 palavras de curiosity gap)
3. **Estilo do canal** (opcional): paleta, expressão, referência de canal
4. **Posição do texto** (opcional): bottom (default), center, top

## Fase 1: brief e prompt (dispatch paralelo)

```
- Agent(subagent_type: "mos-video", prompt: "Gere o Thumbnail Brief para vídeo sobre [tema]. Considere memory existente do cliente neste projeto. Entregue: conceito visual (composição, expressão/ação, cor dominante contrastando com o feed), 3 opções de texto da thumb (máx 5 palavras cada, curiosity gap, sem clickbait vazio) e recomendação de posição do texto (top/center/bottom) baseada na composição.")

- Agent(subagent_type: "mos-ai-tools", prompt: "Gere prompt de imagem 16:9 para FUNDO de thumbnail YouTube sobre [tema]. Estilo: [estilo]. REGRAS: nenhum texto/letreiro na imagem; deixar área de respiro para overlay de texto em [posição]; alto contraste e leitura clara em tamanho pequeno (a thumb é vista com ~120px de altura). Entregue prompt principal em inglês + negative prompt.")
```

## Fase 2: renderização do fundo (executa)

Renderize o prompt do fundo via skill disponível (`gpt-image-2` ou `ai-image-generation`), aspect 16:9, salvando em `workspace/media/thumbnails/fundo-<slug>.png`.

**Fallback sem skill de imagem**: entregue brief + prompt e siga direto pro passo manual (o usuário renderiza onde preferir e volta com o arquivo pra Fase 3).

## Fase 3: overlay tipográfico (executa, determinístico)

```bash
python3 scripts/thumbnail_composer.py \
  --bg workspace/media/thumbnails/fundo-<slug>.png \
  --texto "<texto escolhido do brief>" \
  --out workspace/media/thumbnails/thumb-<slug>-<YYYYMMDD>.png \
  --pos <posição do brief>

# ou: python scripts/mos.py thumbnail compose --bg ... --texto "..." --out ...
```

Sem Pillow instalado, o script instrui `pip install -r requirements.txt`. Gere as 3 opções de texto do brief como 3 arquivos se o usuário quiser comparar (é 1 comando por variação, custo zero).

## Consolidação

```markdown
## Thumbnail: [tema]

Arquivo: workspace/media/thumbnails/thumb-[slug].png (1280x720)
Fundo: [skill usada | fornecido manualmente] | Texto: "[texto]" | Posição: [pos]

### Conceito (do brief do mos-video)
[composição, expressão, cor dominante e por quê]

### Variações de texto disponíveis
1. "[opção 1]" (renderizada) | 2. "[opção 2]" | 3. "[opção 3]"

### Próximos passos
- Testar 2 textos como A/B de CTR: /criar-teste-ab
- CTR real reportado alimenta a memory do mos-video (thumbnails aprovadas)
```

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Fundo SEM texto embutido (se o gerador colocou letreiro, re-renderizar; overlay é a única fonte de texto)
- Texto da thumb com máximo ~5 palavras e legível em miniatura
- Curiosity gap honesto: a thumb promete o que o vídeo paga (coerência com o título é gate do mos-video)
- Arquivos em `workspace/media/` (gitignored), nunca em path versionado

## Por que esse dispatch

O brief é estratégia de retenção (mos-video), o fundo é prompt engineering (mos-ai-tools), e o texto é tipografia determinística (script), porque cada camada falha de um jeito diferente: gerador escreve errado, tipografia manual não escala, e brief sem ciência de CTR vira decoração. Paralelo na Fase 1 porque brief e prompt de fundo são independentes; sequencial nas Fases 2-3 porque o overlay consome o fundo.
