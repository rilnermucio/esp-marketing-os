"""Markdown → PDF with optional white-label config.

Generic, reusable across commands. White-label via .auditoria-config.json
(loaded by caller, passed as `config` dict).

CLI: python pdf_generator.py <input.md> <output.pdf> [config.json]
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# macOS: weasyprint dependencies (cairo, pango, gobject) live in /opt/homebrew/lib
# but cffi looks for them by their non-versioned name. Set DYLD_FALLBACK_LIBRARY_PATH
# before importing weasyprint so the C extension can locate them at load time.
if sys.platform == "darwin":
    _homebrew_lib = "/opt/homebrew/lib"
    if os.path.isdir(_homebrew_lib):
        _existing = os.environ.get("DYLD_FALLBACK_LIBRARY_PATH", "")
        if _homebrew_lib not in _existing.split(":"):
            os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = (
                f"{_homebrew_lib}:{_existing}" if _existing else _homebrew_lib
            )


try:
    from markdown_it import MarkdownIt
    from weasyprint import HTML
except ImportError as e:
    raise ImportError(
        "Faltam dependências do pdf_generator. Instale: pip install weasyprint markdown-it-py"
    ) from e


_DEFAULT = {
    "brand_name": "",
    "primary_color": "#1a1a1a",
    "accent_color": "#1a73e8",
    "footer_text": "Auditoria gerada com marketing-os",
    "logo_path": None,
}


_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
  @page {{ size: A4; margin: 2cm; @bottom-center {{ content: "{footer}"; font-size: 9pt; color: #666; }} }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
          color: {primary}; line-height: 1.5; font-size: 11pt; }}
  h1 {{ color: {accent}; border-bottom: 2px solid {accent}; padding-bottom: 0.3em; }}
  h2 {{ color: {accent}; margin-top: 1.5em; }}
  h3 {{ color: {primary}; }}
  table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
  th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
  th {{ background: {accent}; color: white; }}
  code {{ background: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; }}
  pre {{ background: #f5f5f5; padding: 1em; border-radius: 4px; overflow: auto; }}
  blockquote {{ border-left: 4px solid {accent}; padding-left: 1em; color: #555; }}
  .header-brand {{ font-size: 14pt; font-weight: 600; color: {accent}; margin-bottom: 0.5em; }}
  .header-logo {{ max-height: 60px; margin-bottom: 1em; }}
</style>
</head>
<body>
{header}
{body}
</body>
</html>
"""


def _build_html(markdown_text: str, config: dict | None) -> str:
    cfg = {**_DEFAULT, **(config or {})}
    # CSS escape double quotes in footer_text (CSS string literal context)
    cfg["footer_text"] = cfg.get("footer_text", "").replace('"', '\\"')
    md = MarkdownIt("commonmark", {"html": False}).enable(["table", "strikethrough"])
    body = md.render(markdown_text)

    header_parts = []
    if cfg.get("logo_path"):
        logo_path = Path(cfg["logo_path"])
        if logo_path.exists():
            header_parts.append(
                f'<img class="header-logo" src="{logo_path.resolve()}" />'
            )
        else:
            print(f"[pdf_generator] logo não encontrado: {logo_path}", file=sys.stderr)
    if cfg.get("brand_name"):
        header_parts.append(f'<div class="header-brand">{cfg["brand_name"]}</div>')
    header = "\n".join(header_parts)

    title = cfg.get("brand_name") or "Relatório"

    # Escape literal braces so str.format() doesn't interpret them as fields.
    body_safe = body.replace("{", "{{").replace("}", "}}")
    header_safe = header.replace("{", "{{").replace("}", "}}")

    return _HTML_TEMPLATE.format(
        title=title,
        body=body_safe,
        header=header_safe,
        primary=cfg["primary_color"],
        accent=cfg["accent_color"],
        footer=cfg["footer_text"],
    )


def generate(
    markdown_path: Path | str,
    output_path: Path | str,
    config_path: Path | str | None = None,
    *,
    from_html: bool = False,
) -> Path:
    """Render markdown OR HTML file to PDF. Returns output_path.

    If `from_html=True` or input has .html extension, treats input as raw HTML
    and skips the markdown→HTML pipeline. Useful for premium templates.
    """
    from audit_config import load as load_config

    in_path = Path(markdown_path)
    out_path = Path(output_path)
    config = load_config(config_path) if config_path else None

    is_html = from_html or in_path.suffix.lower() == ".html"

    if is_html:
        html = in_path.read_text(encoding="utf-8")
    else:
        md_text = in_path.read_text(encoding="utf-8")
        html = _build_html(md_text, config)

    HTML(string=html, base_url=str(in_path.parent)).write_pdf(str(out_path))
    return out_path


def _cli(argv: list[str]) -> int:
    if len(argv) < 3:
        print(
            "Usage: pdf_generator.py [--from-html] <input> <output.pdf> [config.json]",
            file=sys.stderr,
        )
        return 1

    args = list(argv[1:])
    from_html = False
    if args and args[0] == "--from-html":
        from_html = True
        args.pop(0)

    if len(args) < 2:
        print(
            "Usage: pdf_generator.py [--from-html] <input> <output.pdf> [config.json]",
            file=sys.stderr,
        )
        return 1

    in_path = Path(args[0])
    out_path = Path(args[1])
    cfg_path = Path(args[2]) if len(args) > 2 else None
    try:
        generate(in_path, out_path, cfg_path, from_html=from_html)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    print(str(out_path))
    return 0


if __name__ == "__main__":
    sys.exit(_cli(sys.argv))
