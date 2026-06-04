# Spec — /narrar-roteiro + tts_runner.py

**Status:** aprovado 2026-06-04. Fase 1 do `docs/ROADMAP.md` (Grupo A, geração real de mídia).

## Objetivo
Roteiro do mos-audio/mos-video vira áudio narrado PT-BR. O plugin prepara (limpa + valida timing + escolhe voz, via mos-audio) e o script executa a síntese, degradando com clareza se o motor não estiver disponível.

## Motor (decisão: OS-aware)
- macOS: `say -v Luciana|Felipe` (PT-BR nativo, sem download).
- Linux/outros: `npx hyperframes tts <file> -l pt-br` (Kokoro; PT-BR via phonemizer, sotaque aceitável; baixa modelo no 1º uso).
- Override por `--engine say|kokoro`.

## Núcleo determinístico (testável)
- `to_speakable(roteiro: str) -> str` — remove markdown (`**`, `##`, `---`, backticks), emojis/marcadores (📍🎬), stage directions `[entre colchetes]`, cabeçalhos de timing (`HOOK (0-2s):`, `📍 SETUP (2-5s):`). Mantém só o falado.
- `voice_for(tom: str, engine: str) -> str` — tom→voz. say: tons masculinos→Felipe, resto→Luciana. kokoro: energético→af_nova, autoridade→am_adam, calmo→af_sky, default→af_heart.
- `build_command(engine, src_file, voice, output, speed) -> list[str]` — argv. say: `say -v <voz> -r <rate> -o <out.aiff> -f <file>`. kokoro: `npx hyperframes tts <file> -v <voz> -l pt-br -o <out.wav> -s <speed>`.
- `detect_engine() -> "say"|"kokoro"` — darwin + `say` no PATH → say; senão kokoro.

## I/O
- `run(roteiro, tom, engine, output, speed, dry_run)` — escreve texto falável em temp, monta+roda o comando. `dry_run` mostra texto falável + comando sem executar. Falha do motor → erro claro (não crash silencioso).
- CLI: `--file`/texto posicional, `--tom`, `--voz`, `--engine`, `--output`, `--speed`, `--dry-run`. `add_output_args` para `--json`.

## Command /narrar-roteiro
Despacha mos-audio pra preparar (roteiro→falável, gate de timing 140-160 wpm PT-BR, recomendar tom/voz), depois roda `python scripts/tts_runner.py`. Command que despacha (37º). Nota no corpo: pra voz premium real, usar a skill ai-avatar-video (Inworld TTS-2).

## Testes (TDD, hermético, sem rodar TTS)
to_speakable limpa um roteiro de Reels do mos-video; voice_for mapeia tons nos 2 engines; build_command monta argv certo (say e kokoro); detect_engine; `--dry-run` mostra comando sem subprocess; `run` com subprocess mockado (sucesso + falha graciosa).

## Arquivos
Novos: `scripts/tts_runner.py`, `scripts/tests/test_tts_runner.py`, `commands/narrar-roteiro.md`.
Editados (guard-rails): `scripts/mos.py` (categoria audio→narrate), README/AGENTS (36→37 commands).

## Fora de escopo
Geração de vídeo (/produzir-reels, Fase 2). Voz premium Inworld fica como nota, não código.
