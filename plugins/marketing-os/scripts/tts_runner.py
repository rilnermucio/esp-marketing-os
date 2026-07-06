#!/usr/bin/env python3
"""
TTS Runner - narra um roteiro em áudio PT-BR.

OS-aware: macOS usa `say` (voz PT-BR nativa), demais usam `npx hyperframes tts`
(Kokoro + phonemizer pt-br). Núcleo determinístico (limpeza/voz/comando) +
execução via subprocess que degrada com clareza se o motor faltar.

Uso:
    python tts_runner.py --file roteiro.txt --tom energetico
    python tts_runner.py "Texto curto" --tom autoridade --output fala.aiff
    python tts_runner.py --file roteiro.txt --dry-run   # mostra texto+comando
"""

import argparse
import platform
import re
import shutil
import subprocess
import sys

# Marcação de roteiro que NÃO deve ser falada.
_EMOJI = re.compile("[\U0001f000-\U0001faff\U00002600-\U000027bf←-⇿⌀-⏿]")
_TIMING = re.compile(r"\(\s*\d+\s*[-–]?\s*\d*\s*s\s*\)")  # (0-2s), (30s)

SAY_MASCULINO = {"autoridade", "masculino", "serio", "grave", "firme"}
KOKORO_VOICES = {
    "energetico": "af_nova",
    "autoridade": "am_adam",
    "masculino": "am_adam",
    "calmo": "af_sky",
    "amigavel": "af_heart",
}


def to_speakable(roteiro: str) -> str:
    """Converte um roteiro com marcação em texto puro falável."""
    falado = []
    for raw in roteiro.splitlines():
        line = _EMOJI.sub("", raw).strip()
        if not line:
            continue
        if line.startswith("#"):  # cabeçalho markdown / label de seção
            continue
        if _TIMING.search(line):  # linha de timing/cena (ex: HOOK (0-2s):)
            continue
        if line.startswith("[") and line.endswith("]"):  # stage direction
            continue
        line = re.sub(r"\[[^\]]*\]", "", line)  # stage direction inline
        line = line.replace("**", "").replace("`", "").replace("---", "")
        line = re.sub(r"^[-*•]\s+", "", line)  # bullet
        line = line.strip().strip('"').strip("'").strip()
        if line:
            falado.append(line)
    return " ".join(falado)


def voice_for(tom: str, engine: str) -> str:
    """Mapeia tom -> voz, por motor."""
    tom = (tom or "").lower()
    if engine == "say":
        return "Felipe" if tom in SAY_MASCULINO else "Luciana"
    return KOKORO_VOICES.get(tom, "af_heart")


def build_command(
    engine: str, src_file: str, voice: str, output: str, speed: float = 1.0
) -> list:
    """Monta o argv do motor de TTS."""
    if engine == "say":
        rate = int(170 * speed)
        return ["say", "-v", voice, "-r", str(rate), "-o", output, "-f", src_file]
    return [
        "npx",
        "--yes",
        "hyperframes",
        "tts",
        src_file,
        "-v",
        voice,
        "-l",
        "pt-br",
        "-o",
        output,
        "-s",
        str(speed),
    ]


def detect_engine() -> str:
    """`say` no macOS (PT-BR nativo); senão kokoro (portável)."""
    if platform.system() == "Darwin" and shutil.which("say"):
        return "say"
    return "kokoro"


def run(
    roteiro: str,
    tom: str = None,
    voz: str = None,
    engine: str = None,
    output: str = None,
    speed: float = 1.0,
    dry_run: bool = False,
) -> dict:
    """Narra o roteiro. dry_run mostra o comando sem executar."""
    engine = engine or detect_engine()
    voice = voz or voice_for(tom, engine)
    if not output:
        output = "narracao.aiff" if engine == "say" else "narracao.wav"

    speakable = to_speakable(roteiro)
    src_txt = output + ".txt"
    with open(src_txt, "w", encoding="utf-8") as f:
        f.write(speakable)

    cmd = build_command(engine, src_txt, voice, output, speed)
    result = {
        "engine": engine,
        "voice": voice,
        "output": output,
        "command": cmd,
        "speakable": speakable,
        "ran": False,
    }
    if dry_run:
        return result

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True)
    except FileNotFoundError as e:
        raise RuntimeError(
            f"motor '{engine}' indisponível ({e}). Instale-o ou rode com --dry-run."
        )
    if proc.returncode != 0:
        raise RuntimeError(
            f"TTS falhou (engine={engine}, rc={proc.returncode}): "
            f"{(proc.stderr or '')[:300]}"
        )
    result["ran"] = True
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Narra um roteiro em áudio PT-BR")
    parser.add_argument("texto", nargs="*", help="Roteiro inline (ou use --file)")
    parser.add_argument("--file", "-f", help="Arquivo com o roteiro")
    parser.add_argument("--tom", help="energetico, calmo, autoridade, amigavel")
    parser.add_argument("--voz", help="Voz específica (override)")
    parser.add_argument(
        "--engine", choices=["say", "kokoro"], help="Motor (default: auto)"
    )
    parser.add_argument("--output", "-o", help="Arquivo de áudio de saída")
    parser.add_argument("--speed", type=float, default=1.0, help="Velocidade (1.0)")
    parser.add_argument(
        "--dry-run", action="store_true", help="Mostra texto+comando, não executa"
    )
    parser.add_argument("--json", action="store_true", help="Saída em JSON")
    args = parser.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            roteiro = f.read()
    elif args.texto:
        roteiro = " ".join(args.texto)
    else:
        print("Uso: tts_runner.py --file roteiro.txt --tom energetico", file=sys.stderr)
        sys.exit(1)

    try:
        res = run(
            roteiro,
            tom=args.tom,
            voz=args.voz,
            engine=args.engine,
            output=args.output,
            speed=args.speed,
            dry_run=args.dry_run,
        )
    except RuntimeError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        import json

        payload = {k: v for k, v in res.items() if k != "speakable"}
        print(json.dumps(payload, ensure_ascii=False))
    elif args.dry_run:
        print("📝 TEXTO FALÁVEL:\n" + res["speakable"])
        print("\n▶ COMANDO:\n" + " ".join(res["command"]))
    else:
        print(
            f"🔊 Áudio gerado: {res['output']} "
            f"(engine={res['engine']}, voz={res['voice']})"
        )


if __name__ == "__main__":
    main()
