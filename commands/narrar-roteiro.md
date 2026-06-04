---
description: Transforma um roteiro (podcast, VSL, Reels, spot) em áudio narrado PT-BR. Prepara o texto via mos-audio (limpeza + gate de timing + voz) e gera o áudio com TTS local. Dispara em "narrar", "gerar áudio", "voz", "TTS", "locução", "narração", "podcast em áudio", "VSL narrada".
argument-hint: "<roteiro ou arquivo> [tom: energetico|calmo|autoridade|amigavel]"
---

# /narrar-roteiro: Roteiro em Áudio Narrado PT-BR

Pega um roteiro e entrega um arquivo de áudio narrado. O plugin **prepara e valida** (mos-audio), o TTS local **executa** a síntese.

## Fase 1: preparação (dispatch)

Despache o mos-audio pra preparar o roteiro:

```
Agent(subagent_type: "mos-audio", prompt: "Prepare este roteiro para narração TTS:
1. Limpe pra texto 100% falável (remova marcações de cena, timestamps, direções visuais, emojis).
2. Aplique o Quality Gate de timing (140-160 palavras/min PT-BR): sinalize se está longo/curto pro tempo alvo.
3. Recomende o tom (energetico, calmo, autoridade, amigavel) coerente com o conteúdo.
Retorne o texto falável limpo + o tom recomendado.

ROTEIRO:
[colar o roteiro aqui]")
```

## Fase 2: síntese (executa)

Com o texto falável e o tom da Fase 1, gere o áudio:

```bash
# Salve o texto falável num arquivo e rode (motor auto: say no mac, kokoro fora)
python scripts/tts_runner.py --file roteiro_falavel.txt --tom <tom> --output narracao.aiff

# ou via CLI unificado
python scripts/mos.py audio narrate --file roteiro_falavel.txt --tom energetico

# Pré-visualizar sem gerar (mostra texto + comando)
python scripts/tts_runner.py --file roteiro_falavel.txt --tom autoridade --dry-run
```

## Saída

Entregue ao usuário: o caminho do arquivo de áudio gerado (`.aiff` no mac, `.wav` no Kokoro), o motor e a voz usados, e o texto falável final (pós-limpeza). Se o usuário pediu só preview, mostre o texto falável + o comando do `--dry-run` sem executar. Salve o áudio fora de paths versionados (ex: a pasta de mídia pessoal do projeto), nunca dentro do plugin.

## Motor (OS-aware, sem configuração)

- **macOS:** `say -v Luciana|Felipe` (PT-BR nativo, qualidade alta, instantâneo).
- **Linux/outros:** `npx hyperframes tts` (Kokoro + phonemizer pt-br; baixa o modelo no primeiro uso).
- Override por `--engine say|kokoro`. Se o motor faltar, o script avisa com clareza (não falha em silêncio).

## Qualidade e limites

Para voz premium com naturalidade de locutor real (PT-BR), use a skill `ai-avatar-video` (Inworld TTS-2) em vez do motor local. O `say` do mac já entrega ótima qualidade pra rascunho e produção leve.

Lembre os Quality Gates globais no texto: sem travessão, sem "brutal", sem CAPS gritado, acentos PT-BR corretos (o áudio expõe erros de acento).
