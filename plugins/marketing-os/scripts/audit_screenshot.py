"""Capture screenshots of landing page + internal pages via Playwright.

Pure I/O wrapper. Returns paths to PNG files. Errors degrade gracefully
(logged, not raised). Headless Chromium with desktop viewport by default.

CLI: python audit_screenshot.py --url <url> --output-dir <dir>
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

from validators import url_aponta_para_rede_interna

try:
    from playwright.sync_api import sync_playwright
except ImportError:  # pragma: no cover – optional dep
    sync_playwright = None  # type: ignore[assignment]

_INTERNAL_KEYWORDS = [
    "pricing",
    "signup",
    "sign-up",
    "register",
    "contact",
    "features",
    "demo",
    "about",
]
_MAX_INTERNAL_PAGES = 3


def _detect_internal_pages(html: str, base_url: str) -> list[str]:
    """Extract up to MAX_INTERNAL_PAGES URLs matching internal keywords. Same-host only."""
    base_host = urlparse(base_url).netloc
    found = []
    seen = set()

    # Match all <a href="..."> links
    href_pattern = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)
    for match in href_pattern.finditer(html):
        href = match.group(1)
        if (
            href.startswith("#")
            or href.startswith("mailto:")
            or href.startswith("tel:")
        ):
            continue

        absolute = urljoin(base_url, href)
        parsed = urlparse(absolute)
        if parsed.netloc != base_host:
            continue

        # Match against keywords
        path_lower = parsed.path.lower()
        if not any(kw in path_lower for kw in _INTERNAL_KEYWORDS):
            continue

        # Dedupe
        normalized = absolute.rstrip("/")
        if normalized in seen:
            continue
        seen.add(normalized)
        found.append(absolute)

        if len(found) >= _MAX_INTERNAL_PAGES:
            break

    return found


def capture(
    url: str,
    output_dir: Path | str,
    viewport: tuple[int, int] = (1440, 900),
    timeout_ms: int = 30000,
) -> dict:
    """Capture screenshots. Returns {homepage: Path, internals: list[Path], errors: list}."""
    if not re.match(r"^https?://", url):
        raise ValueError(f"URL inválida: {url!r}")
    if url_aponta_para_rede_interna(url):
        raise ValueError(
            f"URL aponta para rede interna/privada, bloqueada por segurança (anti-SSRF): {url!r}"
        )

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    result = {"homepage": None, "internals": [], "errors": []}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            context = browser.new_context(
                viewport={"width": viewport[0], "height": viewport[1]},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) auditoria-pro",
            )
            page = context.new_page()

            # Capture homepage
            try:
                page.goto(url, wait_until="networkidle", timeout=timeout_ms)
                homepage_path = out_dir / "homepage.png"
                page.screenshot(path=str(homepage_path), full_page=True)
                result["homepage"] = homepage_path

                # Detect internal pages from rendered HTML
                html = page.content()
                internal_urls = _detect_internal_pages(html, url)

                for internal_url in internal_urls:
                    try:
                        page.goto(
                            internal_url, wait_until="networkidle", timeout=timeout_ms
                        )
                        slug = (
                            re.sub(r"\W+", "-", urlparse(internal_url).path.strip("/"))[
                                :40
                            ]
                            or "page"
                        )
                        internal_path = out_dir / f"{slug}.png"
                        page.screenshot(path=str(internal_path), full_page=True)
                        result["internals"].append(internal_path)
                    except Exception as e:
                        result["errors"].append(f"internal {internal_url}: {e}")

            except Exception as e:
                result["errors"].append(f"homepage: {e}")

        finally:
            browser.close()

    return result


def _cli() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--viewport", default="1440x900")
    parser.add_argument("--timeout-ms", type=int, default=30000)
    args = parser.parse_args()

    w, h = args.viewport.split("x")
    result = capture(
        args.url, args.output_dir, viewport=(int(w), int(h)), timeout_ms=args.timeout_ms
    )

    out = {
        "homepage": str(result["homepage"]) if result["homepage"] else None,
        "internals": [str(p) for p in result["internals"]],
        "errors": result["errors"],
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0 if result["homepage"] else 1


if __name__ == "__main__":
    sys.exit(_cli())
