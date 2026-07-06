---
description: Turn a Reels/TikTok script into a rendered, captioned vertical video. Dispatches mos-video (roteiro com timeline de legendas), encadeia /narrar-roteiro (áudio TTS) e renderiza com HyperFrames, com fallback honesto por degrau.
argument-hint: "<tema ou roteiro pronto + duração, ex: 'reels 30s sobre mitos da nutrição'>"
---

# /produzir-reels: Roteiro vira vídeo legendado (Pipeline em degraus)

Fecha o pipeline completo de Reels: roteiro → narração → vídeo vertical legendado renderizado. Cada degrau entrega valor sozinho; se uma ferramenta do ambiente faltar, o pipeline para no degrau anterior com instruções, nunca com promessa vazia.

## Required inputs (ask if missing)

1. **Tema ou roteiro** (obrigatório): tema pra criar, ou roteiro pronto (ex: output do `/criar-video`)
2. **Duração alvo** (opcional, default 30s): 15-90s
3. **Estilo visual** (opcional): fundo sólido com legendas grandes (default, estilo "caption video"), b-roll gerado por IA, ou mídia própria do usuário em `workspace/media/`
4. **Tom da narração** (opcional): energetico (default pra Reels), calmo, autoridade, amigavel

## Degrau 1: roteiro com timeline (dispatch)

Se o roteiro não veio pronto:

```
Agent(subagent_type: "mos-video", prompt: "Crie roteiro de Reels de [duração]s sobre [tema]. Considere memory existente do cliente neste projeto. Entregue OBRIGATORIAMENTE: (a) texto de narração falável (140-160 palavras/min); (b) timeline de text-on-screen sincronizada em blocos com timestamps [início-fim: texto na tela], legendas curtas de 3-6 palavras por bloco; (c) hook nos 3 primeiros segundos; (d) re-hook visual/textual a cada 5-10s; (e) CTA final. Aplicar quality gates (timing realista, sem aspas em falas).")
```

Roteiro pronto fornecido: valide timing (palavras ÷ 150/min ≤ duração) e extraia a timeline de legendas; sem timeline, dispatche o mos-video só pra gerá-la a partir do texto.

## Degrau 2: narração (executa, encadeia /narrar-roteiro)

Siga o fluxo do `/narrar-roteiro` (preparação via `mos-audio` + síntese local):

```bash
python scripts/tts_runner.py --file roteiro_falavel.txt --tom [tom] --output workspace/media/reels/narracao-<slug>.aiff
```

Sem TTS funcional no ambiente: entregue roteiro + timeline + instruções de gravação (o usuário narra no celular) e siga pro Degrau 3 apenas se ele fornecer o áudio.

## Degrau 3: composição e render (executa, HyperFrames)

Com áudio + timeline, monte a composição HyperFrames (HTML de vídeo 1080x1920):

1. Crie `workspace/media/reels/<slug>/` com a composição: fundo (cor da marca ou b-roll), áudio da narração, legendas sincronizadas pela timeline do Degrau 1 (blocos grandes, alto contraste, palavra-chave destacada), CTA final como cartela
2. Valide e renderize:

```bash
npx hyperframes lint workspace/media/reels/<slug>/
npx hyperframes render workspace/media/reels/<slug>/ --out workspace/media/reels/<slug>.mp4
```

3. B-roll por IA (opcional, estilo "b-roll"): gere via skill `ai-video-generation` ANTES da composição e referencie os clipes localmente

**Fallback sem HyperFrames**: entregue o pacote completo do degrau 2 (roteiro + timeline + áudio) mais a composição HTML pronta no diretório, com a instrução exata de instalar/rodar (`npx hyperframes render ...`). O usuário roda 1 comando quando quiser.

## Consolidação

```markdown
## Reels produzido: [tema]

Degrau alcançado: [3: vídeo renderizado | 2: roteiro+áudio | 1: roteiro+timeline]
Arquivo final: workspace/media/reels/[slug].mp4 ([duração]s, 1080x1920, legendado)

### Peças do pipeline
- Roteiro + timeline: [path] | Narração: [path] ([tom]) | Composição: [path]

### Checklist de publicação
- [ ] Assistir SEM som (maioria assiste mudo: as legendas carregam sozinhas?)
- [ ] Hook visível nos 3 primeiros segundos
- [ ] Legenda do post + hashtags + sugestão de enquete: /criar-post se ainda não tem

### Próximos passos
- Retenção real reportada alimenta a memory do mos-video
- Variação de hook pra teste: /criar-teste-ab
```

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Timing realista validado (Gate 4 do mos-video) ANTES de sintetizar áudio
- Legendas sincronizadas com a narração (vídeo mudo precisa funcionar sozinho)
- Sem aspas nas falas; acentuação PT-BR correta nas legendas
- Todos os artefatos em `workspace/media/` (gitignored)
- Declarar sempre o degrau alcançado; nunca reportar vídeo que não foi renderizado

## Por que esse dispatch

O pipeline separa o que é estratégia de retenção (mos-video: hook, re-hooks, timeline), preparação de voz (mos-audio via /narrar-roteiro) e build técnico (HyperFrames, determinístico e local). Degraus explícitos porque as dependências são do ambiente do usuário: cada degrau entrega algo publicável ou executável com 1 comando, e o fallback declara o que faltou em vez de degradar silenciosamente.
