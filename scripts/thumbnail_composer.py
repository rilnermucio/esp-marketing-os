#!/usr/bin/env python3
"""
Thumbnail Composer - Overlay tipográfico legível sobre fundo gerado por IA

Geradores de imagem renderizam texto mal. Este script separa as etapas:
o fundo vem de um gerador (SEM texto no prompt), o texto entra aqui, com
stroke grosso, faixa de contraste e quebra automática, no padrão 1280x720.

Uso:
    python thumbnail_composer.py --bg fundo.png --texto "COMO DOBRAR SUAS VENDAS" --out thumb.png
    python thumbnail_composer.py --bg fundo.png --texto "..." --out thumb.png --pos center --cor "#FFD400"
    python mos.py thumbnail compose --bg fundo.png --texto "..." --out thumb.png
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import List, Tuple

try:
    from PIL import Image, ImageDraw, ImageFont

    _HAS_PIL = True
except ImportError:  # validado em main() com mensagem de instalacao
    _HAS_PIL = False

CANVAS: Tuple[int, int] = (1280, 720)
MARGIN = 64
MAX_LINES = 3
FONT_SIZES = range(112, 39, -8)

FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",  # macOS
    "/System/Library/Fonts/Supplemental/Arial.ttf",  # macOS
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",  # Linux
    "C:/Windows/Fonts/arialbd.ttf",  # Windows
]


def load_font(size: int):
    """Primeira fonte bold disponível no sistema; fallback pra fonte PIL padrão."""
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default(size=size)


def cover_resize(img: "Image.Image") -> "Image.Image":
    """Redimensiona proporcionalmente cobrindo o canvas 1280x720 e faz center-crop."""
    target_w, target_h = CANVAS
    scale = max(target_w / img.width, target_h / img.height)
    new_size = (round(img.width * scale), round(img.height * scale))
    img = img.resize(new_size, Image.LANCZOS)
    left = (img.width - target_w) // 2
    top = (img.height - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))


def wrap_by_width(draw, texto: str, font, max_width: int) -> List[str]:
    """Quebra gulosa por largura medida (não por contagem de chars)."""
    lines: List[str] = []
    current = ""
    for word in texto.split():
        candidate = f"{current} {word}".strip()
        if draw.textlength(candidate, font=font) <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_text(draw, texto: str, max_width: int, max_height: int):
    """Maior fonte em que o texto cabe em até MAX_LINES dentro da área útil."""
    for size in FONT_SIZES:
        font = load_font(size)
        lines = wrap_by_width(draw, texto, font, max_width)
        line_height = int(size * 1.18)
        block_height = line_height * len(lines)
        if len(lines) <= MAX_LINES and block_height <= max_height:
            return font, lines, line_height
    # Menor tamanho mesmo estourando linhas: melhor entregar que falhar
    font = load_font(FONT_SIZES[-1] if hasattr(FONT_SIZES, "__getitem__") else 40)
    lines = wrap_by_width(draw, texto, font, max_width)[:MAX_LINES]
    return font, lines, int(40 * 1.18)


def compose(
    bg_path: str,
    texto: str,
    out_path: str,
    pos: str = "bottom",
    cor: str = "#FFFFFF",
    stroke: str = "#000000",
    faixa_alpha: int = 110,
) -> str:
    """Compõe a thumbnail: fundo em cover 1280x720 + faixa de contraste + texto com stroke.

    Retorna o path salvo. Levanta FileNotFoundError se o fundo não existe.
    """
    if not os.path.exists(bg_path):
        raise FileNotFoundError(f"Fundo não encontrado: {bg_path}")

    base = Image.open(bg_path).convert("RGB")
    base = cover_resize(base)

    overlay = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    max_width = CANVAS[0] - 2 * MARGIN
    max_height = int(CANVAS[1] * 0.42)
    font, lines, line_height = fit_text(draw, texto.strip(), max_width, max_height)
    block_height = line_height * len(lines)

    if pos == "top":
        y0 = MARGIN
    elif pos == "center":
        y0 = (CANVAS[1] - block_height) // 2
    else:  # bottom (default: área clássica de título de thumbnail)
        y0 = CANVAS[1] - MARGIN - block_height

    # Faixa translúcida atrás do bloco de texto garante contraste em qualquer fundo
    pad = 28
    draw.rectangle(
        (0, y0 - pad, CANVAS[0], y0 + block_height + pad),
        fill=(0, 0, 0, faixa_alpha),
    )

    stroke_width = max(3, font.size // 16) if hasattr(font, "size") else 3
    for i, line in enumerate(lines):
        line_width = draw.textlength(line, font=font)
        x = (CANVAS[0] - line_width) // 2
        draw.text(
            (x, y0 + i * line_height),
            line,
            font=font,
            fill=cor,
            stroke_width=stroke_width,
            stroke_fill=stroke,
        )

    result = Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB")
    out_dir = os.path.dirname(os.path.abspath(out_path))
    os.makedirs(out_dir, exist_ok=True)
    result.save(out_path, "PNG")
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compõe thumbnail 1280x720 com overlay tipográfico legível"
    )
    parser.add_argument(
        "--bg", required=True, help="Imagem de fundo (gerada sem texto)"
    )
    parser.add_argument(
        "--texto", required=True, help="Texto da thumbnail (curto, até ~8 palavras)"
    )
    parser.add_argument("--out", required=True, help="Arquivo PNG de saída")
    parser.add_argument("--pos", choices=["top", "center", "bottom"], default="bottom")
    parser.add_argument("--cor", default="#FFFFFF", help="Cor do texto (hex)")
    parser.add_argument("--stroke", default="#000000", help="Cor do contorno (hex)")
    args = parser.parse_args()

    if not _HAS_PIL:
        print(
            "Pillow não instalado. Rode: pip install 'Pillow>=10' (ou pip install -r requirements.txt)",
            file=sys.stderr,
        )
        return 1

    try:
        out = compose(args.bg, args.texto, args.out, args.pos, args.cor, args.stroke)
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        return 1

    print(f"Thumbnail salva: {out} (1280x720)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
