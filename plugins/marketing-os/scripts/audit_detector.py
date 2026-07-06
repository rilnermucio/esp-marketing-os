"""Detect input type for /auditoria command.

Input → {type: landing|instagram|meta_ads|youtube, normalized, slug}.
Raises ValueError on invalid input.

CLI: python audit_detector.py "<input>" → JSON to stdout.
"""

from __future__ import annotations

import json
import re
import sys
from urllib.parse import urlparse, parse_qs

_URL_RE = re.compile(r"^https?://", re.IGNORECASE)
_IG_HANDLE_RE = re.compile(r"^@?[a-z0-9_.]{1,30}$", re.IGNORECASE)


def _slug_from_landing(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    parts = host.split(".")
    if len(parts) >= 2:
        return parts[-2]
    return host


def _normalize_landing(url: str) -> str:
    """Strip trailing slash for root URLs without query/fragment."""
    parsed = urlparse(url)
    if parsed.path in ("", "/") and not parsed.query and not parsed.fragment:
        return f"{parsed.scheme}://{parsed.netloc}"
    return url


def _slug_meta_ads(url: str) -> str:
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    for key in ("id", "q"):
        vals = qs.get(key)
        if vals:
            val = vals[0].lower().replace(" ", "-")[:32]
            return val or "meta-ad"
    return "meta-ad"


def _yt_slug(url: str) -> str | None:
    """Returns video_id or channel name, or None if not YouTube."""
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    if host not in {"youtube.com", "www.youtube.com", "youtu.be", "m.youtube.com"}:
        return None
    if host == "youtu.be":
        slug = parsed.path.lstrip("/")[:16]
        return slug or "youtube"
    path = parsed.path
    if path.startswith("/@"):
        return path[2:].split("/")[0]
    if path.startswith("/watch"):
        for pair in parsed.query.split("&"):
            if pair.startswith("v="):
                return pair.split("=", 1)[1][:16]
    return path.lstrip("/").split("/")[0][:16] or "youtube"


def detect(input_str: str) -> dict:
    """Return {type, normalized, slug} or raise ValueError."""
    if not input_str or not input_str.strip():
        raise ValueError(
            "Input vazio. Exemplos:\n"
            "  /auditoria https://stripe.com (landing)\n"
            "  /auditoria @ericorocha (instagram)\n"
            "  /auditoria https://www.facebook.com/ads/library/?... (meta ads)\n"
            "  /auditoria https://youtube.com/watch?v=... (youtube)"
        )

    s = input_str.strip()

    # Meta Ad Library check (URL with specific path)
    if _URL_RE.match(s) and "facebook.com/ads/library" in s.lower():
        return {
            "type": "meta_ads",
            "normalized": s,
            "slug": _slug_meta_ads(s),
        }

    # YouTube check (URL host match)
    yt_slug = _yt_slug(s)
    if yt_slug is not None:
        return {
            "type": "youtube",
            "normalized": s,
            "slug": yt_slug,
        }

    # Generic landing URL
    if _URL_RE.match(s):
        return {
            "type": "landing",
            "normalized": _normalize_landing(s),
            "slug": _slug_from_landing(s),
        }

    # Instagram handle
    if _IG_HANDLE_RE.match(s):
        handle = s.lstrip("@").lower()
        return {
            "type": "instagram",
            "normalized": handle,
            "slug": handle,
        }

    raise ValueError(f"Não consegui interpretar: {input_str!r}")


def _cli(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: audit_detector.py <input>", file=sys.stderr)
        return 1
    try:
        result = detect(argv[1])
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(_cli(sys.argv))
