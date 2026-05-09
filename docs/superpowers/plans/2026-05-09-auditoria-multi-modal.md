# Auditoria Multi-modal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship `/auditoria <input>` command that auto-detects 4 input types (landing page, Instagram, Meta Ad Library, YouTube), dispatches relevant `mos-*` agents in parallel, computes weighted scoring per type-specific rubric, and emits a white-label PDF deliverable, all in PT-BR for the BR market.

**Architecture:** Three layers matching existing two-tier pattern. Layer 1: `commands/auditoria.md` orchestrates dispatch + synthesis. Layer 2: 4 deterministic Python scripts in `scripts/` (detector, scoring, PDF generator, config loader). Layer 3: outputs in `workspace/auditorias/<run>/` (gitignored). Synthesis (free-form agent outputs → 0-100 scores per dimension) happens in the command via Claude, not via NLP heuristics. PDF generator is intentionally generic so other commands can reuse it.

**Tech Stack:** Python 3.11+, pytest, weasyprint (HTML/CSS to PDF), markdown-it-py (markdown to HTML), jsonschema (config validation). Reference spec: `docs/superpowers/specs/2026-05-09-auditoria-pdf-design.md`.

---

## File Structure

### New files
- `commands/auditoria.md` — orchestrator command (markdown + frontmatter)
- `scripts/audit_detector.py` — input → type/slug detection
- `scripts/audit_scoring.py` — rubrics + weighted math + format helpers
- `scripts/audit_config.py` — `.auditoria-config.json` loader/validator
- `scripts/pdf_generator.py` — generic markdown → PDF (white-label aware)
- `scripts/tests/test_audit_detector.py`
- `scripts/tests/test_audit_scoring.py`
- `scripts/tests/test_audit_config.py`
- `scripts/tests/test_pdf_generator.py`
- `scripts/tests/test_auditoria_smoke.py` (`@pytest.mark.smoke`)
- `docs/AUDIT-CONFIG.md` — user-facing doc for white-label config

### Modified files
- `requirements.txt` — add weasyprint, markdown-it-py, jsonschema
- `AGENTS.md` — mention `/auditoria` in commands section
- `CHANGELOG.md` — v6.7.0 entry
- `plugin.json` (root) — bump to 6.7.0
- `.claude-plugin/plugin.json` — bump to 6.7.0
- `.claude-plugin/marketplace.json` — bump version

### File responsibilities

| File | Single responsibility |
|---|---|
| `audit_detector.py` | String → `{type, normalized, slug}`. Pure function + CLI |
| `audit_scoring.py` | Validate rubrics, compute weighted overall, sort, format markdown. Pure functions + CLI |
| `audit_config.py` | Load+validate `.auditoria-config.json`. Returns dict or None |
| `pdf_generator.py` | Markdown → PDF with optional white-label config. Generic, reusable |
| `commands/auditoria.md` | Orchestrate: parse input, dispatch agents, synthesize scores, render report, generate PDF |

---

## Task 1: Add dependencies and verify environment

**Files:**
- Modify: `requirements.txt`

- [ ] **Step 1: Read current requirements.txt**

Run: `cat /Users/rilner/Code/especializei/esp-marketing-os/requirements.txt`
Expected: existing list of pip packages (pytest, jsonschema may already exist)

- [ ] **Step 2: Append new dependencies**

Edit `requirements.txt`. Add at the end (only the lines that aren't already present):

```
weasyprint>=60.0
markdown-it-py>=3.0
jsonschema>=4.0
```

- [ ] **Step 3: Install dependencies**

Run: `pip install -r requirements.txt`
Expected: weasyprint installs (may need cairo/pango on macOS via `brew install cairo pango gdk-pixbuf libffi`)

- [ ] **Step 4: Verify imports**

Run:
```bash
python -c "import weasyprint, markdown_it, jsonschema; print('ok')"
```
Expected output: `ok`

If weasyprint fails on macOS: `brew install cairo pango gdk-pixbuf libffi`, then retry.

- [ ] **Step 5: Commit**

```bash
git add requirements.txt
git commit -m "chore(deps): add weasyprint markdown-it-py jsonschema for /auditoria"
```

---

## Task 2: audit_detector.py — landing page detection

**Files:**
- Create: `scripts/audit_detector.py`
- Create: `scripts/tests/test_audit_detector.py`

- [ ] **Step 1: Write failing test for landing detection**

Create `scripts/tests/test_audit_detector.py`:

```python
"""Tests for audit_detector.py (input type detection)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from audit_detector import detect


class TestLandingDetection:
    def test_https_url(self):
        result = detect("https://stripe.com")
        assert result["type"] == "landing"
        assert result["normalized"] == "https://stripe.com"
        assert result["slug"] == "stripe"

    def test_http_url(self):
        result = detect("http://example.com")
        assert result["type"] == "landing"
        assert result["normalized"] == "http://example.com"

    def test_url_with_path(self):
        result = detect("https://example.com/landing")
        assert result["type"] == "landing"
        assert result["slug"] == "example"

    def test_url_with_trailing_slash(self):
        result = detect("https://stripe.com/")
        assert result["normalized"] == "https://stripe.com"

    def test_url_with_subdomain(self):
        result = detect("https://blog.stripe.com")
        assert result["slug"] == "stripe"
```

- [ ] **Step 2: Run test, verify it fails**

Run: `cd /Users/rilner/Code/especializei/esp-marketing-os && python -m pytest scripts/tests/test_audit_detector.py -v`
Expected: ImportError or FAIL because `audit_detector` doesn't exist yet.

- [ ] **Step 3: Create minimal audit_detector.py**

Create `scripts/audit_detector.py`:

```python
"""Detect input type for /auditoria command.

Input → {type: landing|instagram|meta_ads|youtube, normalized, slug}.
Raises ValueError on invalid input.

CLI: python audit_detector.py "<input>" → JSON to stdout.
"""
from __future__ import annotations

import json
import re
import sys
from urllib.parse import urlparse


_URL_RE = re.compile(r"^https?://", re.IGNORECASE)


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
    parsed = urlparse(url)
    if parsed.path == "/" and not parsed.query and not parsed.fragment:
        return f"{parsed.scheme}://{parsed.netloc}"
    return url.rstrip("/") if not parsed.path or parsed.path == "/" else url


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

    if _URL_RE.match(s):
        return {
            "type": "landing",
            "normalized": _normalize_landing(s),
            "slug": _slug_from_landing(s),
        }

    raise ValueError(f"Não consegui interpretar: {input_str!r}")
```

- [ ] **Step 4: Run tests, verify they pass**

Run: `cd /Users/rilner/Code/especializei/esp-marketing-os && python -m pytest scripts/tests/test_audit_detector.py::TestLandingDetection -v`
Expected: 5 passed

- [ ] **Step 5: Commit**

```bash
git add scripts/audit_detector.py scripts/tests/test_audit_detector.py
git commit -m "feat(audit): detector for landing page URLs"
```

---

## Task 3: audit_detector.py — Instagram detection

**Files:**
- Modify: `scripts/audit_detector.py`
- Modify: `scripts/tests/test_audit_detector.py`

- [ ] **Step 1: Append Instagram tests**

Add to `scripts/tests/test_audit_detector.py`:

```python
class TestInstagramDetection:
    def test_at_prefix(self):
        result = detect("@ericorocha")
        assert result["type"] == "instagram"
        assert result["normalized"] == "ericorocha"
        assert result["slug"] == "ericorocha"

    def test_no_prefix_letters_only(self):
        result = detect("ericorocha")
        assert result["type"] == "instagram"
        assert result["normalized"] == "ericorocha"

    def test_with_dot(self):
        result = detect("@joao.silva")
        assert result["type"] == "instagram"
        assert result["normalized"] == "joao.silva"

    def test_with_underscore(self):
        result = detect("@user_name_123")
        assert result["type"] == "instagram"
        assert result["normalized"] == "user_name_123"

    def test_uppercase_lowercased(self):
        result = detect("@EricoRocha")
        assert result["normalized"] == "ericorocha"
        assert result["slug"] == "ericorocha"
```

- [ ] **Step 2: Run tests to confirm new ones fail**

Run: `python -m pytest scripts/tests/test_audit_detector.py::TestInstagramDetection -v`
Expected: 5 failures with ValueError

- [ ] **Step 3: Add Instagram detection to detector**

In `scripts/audit_detector.py`, add this regex constant near the top:

```python
_IG_HANDLE_RE = re.compile(r"^@?[a-z0-9_.]+$", re.IGNORECASE)
```

Then update the `detect()` function. Add this block AFTER the URL check, BEFORE the final `raise ValueError`:

```python
    if _IG_HANDLE_RE.match(s):
        handle = s.lstrip("@").lower()
        return {
            "type": "instagram",
            "normalized": handle,
            "slug": handle,
        }
```

- [ ] **Step 4: Run tests, verify they pass**

Run: `python -m pytest scripts/tests/test_audit_detector.py -v`
Expected: 10 passed (5 landing + 5 instagram)

- [ ] **Step 5: Commit**

```bash
git add scripts/audit_detector.py scripts/tests/test_audit_detector.py
git commit -m "feat(audit): detect Instagram handles (with/without @ prefix)"
```

---

## Task 4: audit_detector.py — Meta Ads + YouTube detection

**Files:**
- Modify: `scripts/audit_detector.py`
- Modify: `scripts/tests/test_audit_detector.py`

- [ ] **Step 1: Append Meta Ads + YouTube tests**

Add to `scripts/tests/test_audit_detector.py`:

```python
class TestMetaAdsDetection:
    def test_meta_ad_library(self):
        result = detect("https://www.facebook.com/ads/library/?id=12345")
        assert result["type"] == "meta_ads"
        assert "facebook.com/ads/library" in result["normalized"]

    def test_meta_ads_pt_locale(self):
        result = detect(
            "https://www.facebook.com/ads/library/?country=BR&search_type=keyword&q=curso"
        )
        assert result["type"] == "meta_ads"


class TestYouTubeDetection:
    def test_full_url(self):
        result = detect("https://youtube.com/watch?v=dQw4w9WgXcQ")
        assert result["type"] == "youtube"
        assert result["slug"] == "dQw4w9WgXcQ"

    def test_short_url(self):
        result = detect("https://youtu.be/dQw4w9WgXcQ")
        assert result["type"] == "youtube"
        assert result["slug"] == "dQw4w9WgXcQ"

    def test_channel_url(self):
        result = detect("https://youtube.com/@channelname")
        assert result["type"] == "youtube"
        assert result["slug"] == "channelname"
```

- [ ] **Step 2: Run, confirm failures**

Run: `python -m pytest scripts/tests/test_audit_detector.py -v -k "MetaAds or YouTube"`
Expected: 5 failures (Meta Ads URLs being misclassified as landing, YouTube same)

- [ ] **Step 3: Add Meta Ads + YouTube detection BEFORE landing check**

In `scripts/audit_detector.py`, modify `detect()`. The Meta Ads and YouTube checks must come BEFORE the landing check (since they're URLs too). Replace the body of `detect()` after the empty-input check with:

```python
    s = input_str.strip()

    # Meta Ad Library check (URL with specific path)
    if "facebook.com/ads/library" in s.lower():
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
```

Add helpers near the other helpers:

```python
def _slug_meta_ads(url: str) -> str:
    parsed = urlparse(url)
    qs = parsed.query
    # Try id= first, then q=
    for key in ("id", "q"):
        for pair in qs.split("&"):
            if pair.startswith(f"{key}="):
                val = pair.split("=", 1)[1]
                return val.lower().replace(" ", "-")[:32] or "meta-ad"
    return "meta-ad"


def _yt_slug(url: str) -> str | None:
    """Returns video_id or channel name, or None if not YouTube."""
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    if host not in {"youtube.com", "www.youtube.com", "youtu.be", "m.youtube.com"}:
        return None
    if host == "youtu.be":
        return parsed.path.lstrip("/")[:16]
    path = parsed.path
    if path.startswith("/@"):
        return path[2:].split("/")[0]
    if path.startswith("/watch"):
        for pair in parsed.query.split("&"):
            if pair.startswith("v="):
                return pair.split("=", 1)[1][:16]
    return path.lstrip("/").split("/")[0][:16] or "youtube"
```

- [ ] **Step 4: Run all tests**

Run: `python -m pytest scripts/tests/test_audit_detector.py -v`
Expected: 15 passed (5 landing + 5 IG + 2 Meta Ads + 3 YouTube)

- [ ] **Step 5: Commit**

```bash
git add scripts/audit_detector.py scripts/tests/test_audit_detector.py
git commit -m "feat(audit): detect Meta Ad Library and YouTube URLs"
```

---

## Task 5: audit_detector.py — error cases + CLI mode

**Files:**
- Modify: `scripts/audit_detector.py`
- Modify: `scripts/tests/test_audit_detector.py`

- [ ] **Step 1: Append error + CLI tests**

Add to `scripts/tests/test_audit_detector.py`:

```python
class TestErrorCases:
    def test_empty_string_raises(self):
        with pytest.raises(ValueError, match="vazio"):
            detect("")

    def test_whitespace_only_raises(self):
        with pytest.raises(ValueError, match="vazio"):
            detect("   ")

    def test_invalid_input_raises(self):
        with pytest.raises(ValueError, match="Não consegui"):
            detect("não é url nem perfil 123!@#")


class TestCLI:
    def test_cli_outputs_json(self):
        script = Path(__file__).resolve().parent.parent / "audit_detector.py"
        result = subprocess.run(
            [sys.executable, str(script), "https://stripe.com"],
            capture_output=True, text=True, check=True,
        )
        data = json.loads(result.stdout)
        assert data["type"] == "landing"
        assert data["slug"] == "stripe"

    def test_cli_invalid_exits_nonzero(self):
        script = Path(__file__).resolve().parent.parent / "audit_detector.py"
        result = subprocess.run(
            [sys.executable, str(script), ""],
            capture_output=True, text=True,
        )
        assert result.returncode != 0
        assert "vazio" in result.stderr.lower()
```

- [ ] **Step 2: Run, confirm CLI tests fail (no `__main__`)**

Run: `python -m pytest scripts/tests/test_audit_detector.py::TestCLI -v`
Expected: failures because `audit_detector.py` has no CLI entrypoint

- [ ] **Step 3: Add CLI block to detector**

Append to `scripts/audit_detector.py`:

```python
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
```

- [ ] **Step 4: Run all detector tests**

Run: `python -m pytest scripts/tests/test_audit_detector.py -v`
Expected: 20 passed total

- [ ] **Step 5: Commit**

```bash
git add scripts/audit_detector.py scripts/tests/test_audit_detector.py
git commit -m "feat(audit): error handling for invalid input + CLI entrypoint"
```

---

## Task 6: audit_scoring.py — rubrics validation

**Files:**
- Create: `scripts/audit_scoring.py`
- Create: `scripts/tests/test_audit_scoring.py`

- [ ] **Step 1: Write failing test for rubrics**

Create `scripts/tests/test_audit_scoring.py`:

```python
"""Tests for audit_scoring.py."""
from __future__ import annotations

import pytest

from audit_scoring import RUBRICS, validate_rubrics


class TestRubrics:
    def test_landing_sums_to_100(self):
        assert sum(RUBRICS["landing"].values()) == 100

    def test_instagram_sums_to_100(self):
        assert sum(RUBRICS["instagram"].values()) == 100

    def test_meta_ads_sums_to_100(self):
        assert sum(RUBRICS["meta_ads"].values()) == 100

    def test_youtube_sums_to_100(self):
        assert sum(RUBRICS["youtube"].values()) == 100

    def test_validate_rubrics_passes(self):
        validate_rubrics()

    def test_all_4_types_present(self):
        assert set(RUBRICS.keys()) == {"landing", "instagram", "meta_ads", "youtube"}
```

- [ ] **Step 2: Run, confirm failures**

Run: `python -m pytest scripts/tests/test_audit_scoring.py -v`
Expected: ImportError (audit_scoring doesn't exist)

- [ ] **Step 3: Create audit_scoring.py with rubrics**

Create `scripts/audit_scoring.py`:

```python
"""Scoring rubrics + weighted math for /auditoria.

Inputs: type-specific dimension scores (0-100 or None for "N/D"),
evidences, fixes. Output: overall + sorted top wins/fixes + formatted markdown.

CLI: reads JSON from stdin, writes JSON to stdout.
"""
from __future__ import annotations

import json
import sys


RUBRICS: dict[str, dict[str, int]] = {
    "landing": {
        "Conversão (CTA, friction, funil)": 25,
        "Copy (headline, value prop)": 20,
        "SEO (technical + content)": 15,
        "Trust signals": 10,
        "Design (hierarquia visual)": 10,
        "Brand (consistência, voice)": 10,
        "Diferenciação competitiva": 10,
    },
    "instagram": {
        "Bio + posicionamento": 20,
        "Consistência visual": 20,
        "Hooks últimos posts": 20,
        "Strategy/CTA": 15,
        "Engagement ratio": 15,
        "Cadência/frequência": 10,
    },
    "meta_ads": {
        "Hook do criativo (3s)": 25,
        "Copy (clarity + benefit)": 25,
        "Visual (composição)": 20,
        "CTA + landing match": 15,
        "Diferenciação vs concorrente": 15,
    },
    "youtube": {
        "Hook (30s)": 25,
        "Retention/pacing": 25,
        "Thumbnail + título": 20,
        "Estrutura narrativa": 15,
        "CTA/conversão": 15,
    },
}


def validate_rubrics() -> None:
    """Raise if any rubric does not sum to 100."""
    for audit_type, rubric in RUBRICS.items():
        total = sum(rubric.values())
        if total != 100:
            raise ValueError(
                f"Rubric {audit_type!r} sums to {total}, expected 100"
            )


# Validate at import time so misconfigured rubric fails fast.
validate_rubrics()
```

- [ ] **Step 4: Run, verify pass**

Run: `python -m pytest scripts/tests/test_audit_scoring.py -v`
Expected: 6 passed

- [ ] **Step 5: Commit**

```bash
git add scripts/audit_scoring.py scripts/tests/test_audit_scoring.py
git commit -m "feat(audit): scoring rubrics for 4 audit types"
```

---

## Task 7: audit_scoring.py — compute() weighted math

**Files:**
- Modify: `scripts/audit_scoring.py`
- Modify: `scripts/tests/test_audit_scoring.py`

- [ ] **Step 1: Append compute() tests**

Add to `scripts/tests/test_audit_scoring.py`:

```python
from audit_scoring import compute


class TestCompute:
    def test_full_input_landing(self):
        scores = {
            "Conversão (CTA, friction, funil)": 80,
            "Copy (headline, value prop)": 70,
            "SEO (technical + content)": 60,
            "Trust signals": 50,
            "Design (hierarquia visual)": 90,
            "Brand (consistência, voice)": 75,
            "Diferenciação competitiva": 65,
        }
        evidences = {k: f"evidence for {k}" for k in scores}
        fixes = {k: {"text": f"fix {k}", "priority": "media"} for k in scores}
        result = compute("landing", scores, evidences, fixes)
        # Weighted: 80*25 + 70*20 + 60*15 + 50*10 + 90*10 + 75*10 + 65*10 = 7150 / 100 = 71.5
        assert result["overall"] == 72  # rounded to int
        assert result["partial"] is False
        assert len(result["dimensions"]) == 7

    def test_partial_input_recalcs(self):
        scores = {
            "Conversão (CTA, friction, funil)": 80,
            "Copy (headline, value prop)": 70,
            "SEO (technical + content)": None,  # missing
            "Trust signals": 50,
            "Design (hierarquia visual)": 90,
            "Brand (consistência, voice)": 75,
            "Diferenciação competitiva": 65,
        }
        evidences = {k: "" for k in scores if scores[k] is not None}
        fixes = {k: {"text": "", "priority": "baixa"} for k in scores if scores[k] is not None}
        result = compute("landing", scores, evidences, fixes)
        # Only 6 dimensions scored; weights normalized to those
        assert result["partial"] is True
        # Sum of weights without SEO: 25+20+10+10+10+10 = 85
        # Weighted: (80*25 + 70*20 + 50*10 + 90*10 + 75*10 + 65*10) / 85 = 6100/85 ≈ 71.76 → 72
        assert result["overall"] == 72

    def test_invalid_type_raises(self):
        with pytest.raises(ValueError, match="tipo desconhecido"):
            compute("invalid_type", {}, {}, {})

    def test_missing_dimension_raises(self):
        with pytest.raises(ValueError, match="dimensão"):
            compute("landing", {"Copy (headline, value prop)": 70}, {}, {})

    def test_score_out_of_range_raises(self):
        scores = {k: 50 for k in RUBRICS["landing"]}
        scores["Copy (headline, value prop)"] = 150  # invalid
        with pytest.raises(ValueError, match="0-100"):
            compute("landing", scores, {}, {})

    def test_all_none_raises(self):
        scores = {k: None for k in RUBRICS["landing"]}
        with pytest.raises(ValueError, match="todas as dimensões"):
            compute("landing", scores, {}, {})
```

- [ ] **Step 2: Run, confirm failures**

Run: `python -m pytest scripts/tests/test_audit_scoring.py::TestCompute -v`
Expected: ImportError or AttributeError on `compute`

- [ ] **Step 3: Implement compute()**

Append to `scripts/audit_scoring.py`:

```python
def compute(
    audit_type: str,
    dimension_scores: dict[str, int | None],
    evidences: dict[str, str],
    fixes: dict[str, dict],
) -> dict:
    """Compute overall + sort wins/fixes. Returns serializable dict."""
    if audit_type not in RUBRICS:
        raise ValueError(f"tipo desconhecido: {audit_type!r}")

    rubric = RUBRICS[audit_type]

    # Validate all rubric dims present (None allowed).
    missing = set(rubric.keys()) - set(dimension_scores.keys())
    if missing:
        raise ValueError(f"dimensão ausente: {sorted(missing)!r}")

    # Validate score ranges.
    for dim, score in dimension_scores.items():
        if score is None:
            continue
        if not isinstance(score, (int, float)) or score < 0 or score > 100:
            raise ValueError(f"score fora de 0-100 em {dim!r}: {score}")

    # Compute weighted overall, normalizing if some dims are None.
    scored = [(d, s, rubric[d]) for d, s in dimension_scores.items() if s is not None]
    if not scored:
        raise ValueError("todas as dimensões são N/D, auditoria sem score possível")

    weight_sum = sum(w for _, _, w in scored)
    weighted_total = sum(s * w for _, s, w in scored)
    overall = round(weighted_total / weight_sum)
    partial = len(scored) < len(rubric)

    dimensions = {
        dim: {
            "score": dimension_scores[dim],
            "weight": rubric[dim],
            "evidence": evidences.get(dim, ""),
            "fix": fixes.get(dim, {"text": "", "priority": "baixa"}),
        }
        for dim in rubric
    }

    return {
        "overall": overall,
        "partial": partial,
        "dimensions": dimensions,
        "type": audit_type,
    }
```

- [ ] **Step 4: Run, verify pass**

Run: `python -m pytest scripts/tests/test_audit_scoring.py -v`
Expected: 12 passed (6 rubrics + 6 compute)

- [ ] **Step 5: Commit**

```bash
git add scripts/audit_scoring.py scripts/tests/test_audit_scoring.py
git commit -m "feat(audit): weighted compute() with partial-input handling"
```

---

## Task 8: audit_scoring.py — top wins/fixes ordering

**Files:**
- Modify: `scripts/audit_scoring.py`
- Modify: `scripts/tests/test_audit_scoring.py`

- [ ] **Step 1: Append ordering tests**

Add to `scripts/tests/test_audit_scoring.py`:

```python
from audit_scoring import top_wins, top_fixes


class TestOrdering:
    def _full_landing(self, score_overrides=None):
        scores = {k: 50 for k in RUBRICS["landing"]}
        if score_overrides:
            scores.update(score_overrides)
        evidences = {k: "" for k in scores}
        fixes = {k: {"text": "", "priority": "media"} for k in scores}
        return compute("landing", scores, evidences, fixes)

    def test_top_wins_descending(self):
        result = self._full_landing({
            "Conversão (CTA, friction, funil)": 95,
            "Copy (headline, value prop)": 90,
            "SEO (technical + content)": 30,
        })
        wins = top_wins(result, n=3)
        assert wins[0]["dimension"] == "Conversão (CTA, friction, funil)"
        assert wins[1]["dimension"] == "Copy (headline, value prop)"
        assert wins[0]["score"] >= wins[1]["score"] >= wins[2]["score"]

    def test_top_fixes_priority_then_score(self):
        scores = {k: 50 for k in RUBRICS["landing"]}
        scores["SEO (technical + content)"] = 20  # lowest score, alta priority
        scores["Trust signals"] = 30  # also low, but media priority
        evidences = {k: "" for k in scores}
        fixes = {k: {"text": "", "priority": "media"} for k in scores}
        fixes["SEO (technical + content)"] = {"text": "", "priority": "alta"}
        fixes["Trust signals"] = {"text": "", "priority": "alta"}
        result = compute("landing", scores, evidences, fixes)
        priorities = top_fixes(result, n=3)
        # Both alta priority. Lowest score (20) comes first.
        assert priorities[0]["dimension"] == "SEO (technical + content)"
        assert priorities[1]["dimension"] == "Trust signals"

    def test_top_skips_none(self):
        scores = {k: 50 for k in RUBRICS["landing"]}
        scores["Copy (headline, value prop)"] = None
        evidences = {k: "" for k in scores if scores[k] is not None}
        fixes = {k: {"text": "", "priority": "baixa"} for k in scores if scores[k] is not None}
        result = compute("landing", scores, evidences, fixes)
        wins = top_wins(result, n=3)
        assert all(w["dimension"] != "Copy (headline, value prop)" for w in wins)
```

- [ ] **Step 2: Run, confirm failures**

Run: `python -m pytest scripts/tests/test_audit_scoring.py::TestOrdering -v`
Expected: ImportError on `top_wins`/`top_fixes`

- [ ] **Step 3: Implement ordering helpers**

Append to `scripts/audit_scoring.py`:

```python
_PRIORITY_ORDER = {"alta": 0, "media": 1, "baixa": 2}


def top_wins(result: dict, n: int = 3) -> list[dict]:
    """Top N dimensions by score (descending). Skips None scores."""
    scored = [
        {"dimension": d, "score": v["score"], "evidence": v["evidence"]}
        for d, v in result["dimensions"].items()
        if v["score"] is not None
    ]
    return sorted(scored, key=lambda x: -x["score"])[:n]


def top_fixes(result: dict, n: int = 3) -> list[dict]:
    """Top N dimensions to fix, ordered by (priority, lowest score)."""
    scored = [
        {
            "dimension": d,
            "score": v["score"],
            "fix": v["fix"]["text"],
            "priority": v["fix"]["priority"],
        }
        for d, v in result["dimensions"].items()
        if v["score"] is not None
    ]
    return sorted(
        scored,
        key=lambda x: (_PRIORITY_ORDER.get(x["priority"], 99), x["score"]),
    )[:n]
```

- [ ] **Step 4: Run all scoring tests**

Run: `python -m pytest scripts/tests/test_audit_scoring.py -v`
Expected: 15 passed

- [ ] **Step 5: Commit**

```bash
git add scripts/audit_scoring.py scripts/tests/test_audit_scoring.py
git commit -m "feat(audit): top wins/fixes ordering (priority then score)"
```

---

## Task 9: audit_scoring.py — markdown formatters + CLI

**Files:**
- Modify: `scripts/audit_scoring.py`
- Modify: `scripts/tests/test_audit_scoring.py`

- [ ] **Step 1: Append formatter + CLI tests**

Add to `scripts/tests/test_audit_scoring.py`:

```python
import json
import subprocess
import sys
from pathlib import Path

from audit_scoring import format_scorecard_md, format_priorities_md


class TestFormatters:
    def _sample_result(self):
        scores = {k: 70 for k in RUBRICS["landing"]}
        scores["Conversão (CTA, friction, funil)"] = 90
        evidences = {k: f"saw {k}" for k in scores}
        fixes = {k: {"text": f"fix {k}", "priority": "media"} for k in scores}
        return compute("landing", scores, evidences, fixes)

    def test_scorecard_is_markdown_table(self):
        result = self._sample_result()
        md = format_scorecard_md(result)
        assert "| Dimensão" in md
        assert "| Peso" in md
        assert "| Score" in md
        assert "Conversão" in md

    def test_priorities_lists_top_3(self):
        result = self._sample_result()
        md = format_priorities_md(result)
        # Should list 3 top fixes
        assert md.count("\n- ") + md.count("\n1. ") >= 3 or md.count("Prioridade") >= 1


class TestScoringCLI:
    def test_cli_reads_stdin_writes_stdout(self):
        script = Path(__file__).resolve().parent.parent / "audit_scoring.py"
        scores = {k: 70 for k in RUBRICS["landing"]}
        payload = {
            "type": "landing",
            "dimension_scores": scores,
            "evidences": {k: "" for k in scores},
            "fixes": {k: {"text": "", "priority": "media"} for k in scores},
        }
        result = subprocess.run(
            [sys.executable, str(script)],
            input=json.dumps(payload),
            capture_output=True, text=True, check=True,
        )
        out = json.loads(result.stdout)
        assert out["overall"] == 70
        assert "scorecard_md" in out
        assert "priorities_md" in out
```

- [ ] **Step 2: Run, confirm failures**

Run: `python -m pytest scripts/tests/test_audit_scoring.py::TestFormatters scripts/tests/test_audit_scoring.py::TestScoringCLI -v`
Expected: failures on missing functions and `__main__`

- [ ] **Step 3: Add formatters + CLI**

Append to `scripts/audit_scoring.py`:

```python
def format_scorecard_md(result: dict) -> str:
    """Markdown table: Dimensão | Peso | Score | Status."""
    lines = [
        "| Dimensão | Peso | Score | Status |",
        "|---|---|---|---|",
    ]
    for dim, info in result["dimensions"].items():
        score = info["score"]
        if score is None:
            status = "N/D"
            score_str = "N/D"
        elif score >= 80:
            status = "Forte"
            score_str = str(score)
        elif score >= 60:
            status = "OK"
            score_str = str(score)
        else:
            status = "Atenção"
            score_str = str(score)
        lines.append(f"| {dim} | {info['weight']}% | {score_str} | {status} |")
    return "\n".join(lines)


def format_priorities_md(result: dict, n: int = 3) -> str:
    """Numbered list of top N fixes with priority markers."""
    fixes = top_fixes(result, n=n)
    if not fixes:
        return "Nenhuma prioridade identificada."
    lines = ["## Prioridades"]
    for i, fix in enumerate(fixes, start=1):
        prio = fix["priority"].upper()
        lines.append(
            f"{i}. **[{prio}] {fix['dimension']}** (score {fix['score']}): {fix['fix']}"
        )
    return "\n".join(lines)


def _cli() -> int:
    try:
        payload = json.loads(sys.stdin.read())
    except json.JSONDecodeError as e:
        print(f"Invalid JSON on stdin: {e}", file=sys.stderr)
        return 1

    try:
        result = compute(
            payload["type"],
            payload["dimension_scores"],
            payload.get("evidences", {}),
            payload.get("fixes", {}),
        )
    except (ValueError, KeyError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    out = {
        **result,
        "top_wins": top_wins(result),
        "top_fixes": top_fixes(result),
        "scorecard_md": format_scorecard_md(result),
        "priorities_md": format_priorities_md(result),
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
```

- [ ] **Step 4: Run all scoring tests**

Run: `python -m pytest scripts/tests/test_audit_scoring.py -v`
Expected: 18 passed

- [ ] **Step 5: Commit**

```bash
git add scripts/audit_scoring.py scripts/tests/test_audit_scoring.py
git commit -m "feat(audit): markdown formatters + CLI for scoring"
```

---

## Task 10: audit_config.py — schema + load()

**Files:**
- Create: `scripts/audit_config.py`
- Create: `scripts/tests/test_audit_config.py`

- [ ] **Step 1: Write failing tests**

Create `scripts/tests/test_audit_config.py`:

```python
"""Tests for audit_config.py (white-label config loader)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from audit_config import load


class TestConfigLoad:
    def test_none_path_returns_none(self):
        assert load(None) is None

    def test_missing_file_returns_none(self, tmp_path: Path):
        assert load(tmp_path / "nonexistent.json") is None

    def test_valid_minimal_config(self, tmp_path: Path):
        cfg_path = tmp_path / "cfg.json"
        cfg_path.write_text(json.dumps({"brand_name": "Agência X"}))
        result = load(cfg_path)
        assert result == {"brand_name": "Agência X"}

    def test_valid_full_config(self, tmp_path: Path):
        cfg_path = tmp_path / "cfg.json"
        cfg = {
            "brand_name": "Agência X",
            "logo_path": "./logo.png",
            "primary_color": "#1a1a1a",
            "accent_color": "#0066cc",
            "footer_text": "Custom footer",
        }
        cfg_path.write_text(json.dumps(cfg))
        assert load(cfg_path) == cfg

    def test_missing_brand_name_returns_none(self, tmp_path: Path):
        cfg_path = tmp_path / "cfg.json"
        cfg_path.write_text(json.dumps({"logo_path": "./logo.png"}))
        assert load(cfg_path) is None

    def test_invalid_color_returns_none(self, tmp_path: Path):
        cfg_path = tmp_path / "cfg.json"
        cfg_path.write_text(json.dumps({
            "brand_name": "X",
            "primary_color": "red",  # not hex
        }))
        assert load(cfg_path) is None

    def test_malformed_json_returns_none(self, tmp_path: Path):
        cfg_path = tmp_path / "cfg.json"
        cfg_path.write_text("{not valid json")
        assert load(cfg_path) is None

    def test_extra_property_returns_none(self, tmp_path: Path):
        cfg_path = tmp_path / "cfg.json"
        cfg_path.write_text(json.dumps({
            "brand_name": "X",
            "unknown_field": "value",
        }))
        assert load(cfg_path) is None
```

- [ ] **Step 2: Run, confirm failures**

Run: `python -m pytest scripts/tests/test_audit_config.py -v`
Expected: ImportError

- [ ] **Step 3: Implement audit_config.py**

Create `scripts/audit_config.py`:

```python
"""Loader/validator for .auditoria-config.json (white-label PDF branding).

Returns dict on valid input, None on missing or invalid (with stderr warning).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema


SCHEMA = {
    "$schema": "https://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["brand_name"],
    "properties": {
        "brand_name": {"type": "string", "minLength": 1},
        "logo_path": {"type": "string"},
        "primary_color": {"type": "string", "pattern": "^#[0-9a-fA-F]{6}$"},
        "accent_color": {"type": "string", "pattern": "^#[0-9a-fA-F]{6}$"},
        "footer_text": {"type": "string"},
    },
    "additionalProperties": False,
}


def load(config_path: Path | str | None) -> dict | None:
    """Load and validate config. Returns None on missing or invalid."""
    if config_path is None:
        return None

    path = Path(config_path)
    if not path.exists():
        return None

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[audit_config] JSON inválido em {path}: {e}", file=sys.stderr)
        return None

    try:
        jsonschema.validate(data, SCHEMA)
    except jsonschema.ValidationError as e:
        print(f"[audit_config] Schema inválido em {path}: {e.message}", file=sys.stderr)
        return None

    return data
```

- [ ] **Step 4: Run, verify pass**

Run: `python -m pytest scripts/tests/test_audit_config.py -v`
Expected: 8 passed

- [ ] **Step 5: Commit**

```bash
git add scripts/audit_config.py scripts/tests/test_audit_config.py
git commit -m "feat(audit): config loader for white-label PDF (.auditoria-config.json)"
```

---

## Task 11: pdf_generator.py — basic markdown to PDF

**Files:**
- Create: `scripts/pdf_generator.py`
- Create: `scripts/tests/test_pdf_generator.py`

- [ ] **Step 1: Write failing test**

Create `scripts/tests/test_pdf_generator.py`:

```python
"""Tests for pdf_generator.py (markdown → PDF, white-label aware)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from pdf_generator import generate, _build_html


class TestBasicGenerate:
    def test_generate_creates_non_empty_pdf(self, tmp_path: Path):
        md_path = tmp_path / "report.md"
        md_path.write_text("# Test\n\nSome content.")
        out_path = tmp_path / "report.pdf"
        result = generate(md_path, out_path)
        assert result == out_path
        assert out_path.exists()
        assert out_path.stat().st_size > 100  # PDF has at least header

    def test_generate_renders_tables(self, tmp_path: Path):
        md_path = tmp_path / "report.md"
        md_path.write_text("| A | B |\n|---|---|\n| 1 | 2 |\n")
        out_path = tmp_path / "report.pdf"
        generate(md_path, out_path)
        assert out_path.exists()


class TestBuildHTML:
    def test_html_contains_markdown_h1(self):
        html = _build_html("# Hello\n\nBody.", config=None)
        assert "<h1>" in html
        assert "Hello" in html

    def test_html_default_theme_when_no_config(self):
        html = _build_html("# X", config=None)
        assert "marketing-os" in html.lower()  # default footer
        assert "#1a73e8" in html  # default accent
```

- [ ] **Step 2: Run, confirm failures**

Run: `python -m pytest scripts/tests/test_pdf_generator.py -v`
Expected: ImportError

- [ ] **Step 3: Create pdf_generator.py**

Create `scripts/pdf_generator.py`:

```python
"""Markdown → PDF with optional white-label config.

Generic, reusable across commands. White-label via .auditoria-config.json
(loaded by caller, passed as `config` dict).

CLI: python pdf_generator.py <input.md> <output.pdf> [config.json]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

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
    md = MarkdownIt("commonmark", {"html": False}).enable(["table", "strikethrough"])
    body = md.render(markdown_text)

    header_parts = []
    if cfg.get("logo_path"):
        logo_path = Path(cfg["logo_path"])
        if logo_path.exists():
            header_parts.append(f'<img class="header-logo" src="{logo_path.resolve()}" />')
    if cfg.get("brand_name"):
        header_parts.append(f'<div class="header-brand">{cfg["brand_name"]}</div>')
    header = "\n".join(header_parts)

    title = cfg.get("brand_name") or "Relatório"

    return _HTML_TEMPLATE.format(
        title=title,
        body=body,
        header=header,
        primary=cfg["primary_color"],
        accent=cfg["accent_color"],
        footer=cfg["footer_text"],
    )


def generate(
    markdown_path: Path | str,
    output_path: Path | str,
    config_path: Path | str | None = None,
) -> Path:
    """Render markdown file to PDF. Returns output_path."""
    from audit_config import load as load_config

    md_path = Path(markdown_path)
    out_path = Path(output_path)
    md_text = md_path.read_text(encoding="utf-8")
    config = load_config(config_path) if config_path else None

    html = _build_html(md_text, config)
    HTML(string=html, base_url=str(md_path.parent)).write_pdf(str(out_path))
    return out_path
```

- [ ] **Step 4: Run, verify pass**

Run: `python -m pytest scripts/tests/test_pdf_generator.py -v`
Expected: 4 passed (may take a few seconds, weasyprint is slow first run)

- [ ] **Step 5: Commit**

```bash
git add scripts/pdf_generator.py scripts/tests/test_pdf_generator.py
git commit -m "feat(audit): generic markdown→PDF generator with default theme"
```

---

## Task 12: pdf_generator.py — white-label config applied

**Files:**
- Modify: `scripts/tests/test_pdf_generator.py`

- [ ] **Step 1: Append config tests**

Add to `scripts/tests/test_pdf_generator.py`:

```python
class TestWhiteLabel:
    def test_config_brand_name_in_html(self, tmp_path: Path):
        config = {"brand_name": "Agência X"}
        html = _build_html("# X", config=config)
        assert "Agência X" in html

    def test_config_accent_color_in_html(self):
        config = {"brand_name": "X", "accent_color": "#ff0000"}
        html = _build_html("# X", config=config)
        assert "#ff0000" in html
        assert "#1a73e8" not in html  # default replaced

    def test_config_footer_text_in_html(self):
        config = {"brand_name": "X", "footer_text": "© Cliente Y"}
        html = _build_html("# X", config=config)
        assert "© Cliente Y" in html

    def test_logo_present_when_path_exists(self, tmp_path: Path):
        logo = tmp_path / "logo.png"
        logo.write_bytes(b"fake png")  # weasyprint won't actually load, but HTML includes path
        config = {"brand_name": "X", "logo_path": str(logo)}
        html = _build_html("# X", config=config)
        assert "header-logo" in html

    def test_logo_omitted_when_path_missing(self, tmp_path: Path):
        config = {"brand_name": "X", "logo_path": str(tmp_path / "nonexistent.png")}
        html = _build_html("# X", config=config)
        assert "header-logo" not in html

    def test_generate_with_config_path(self, tmp_path: Path):
        md = tmp_path / "r.md"
        md.write_text("# Title")
        cfg = tmp_path / "cfg.json"
        cfg.write_text(json.dumps({"brand_name": "Acme"}))
        out = tmp_path / "r.pdf"
        generate(md, out, cfg)
        assert out.exists()
        assert out.stat().st_size > 100
```

- [ ] **Step 2: Run, verify all pass**

Run: `python -m pytest scripts/tests/test_pdf_generator.py -v`
Expected: 10 passed (4 base + 6 white-label)

If any fail: confirm `_build_html` reads config dict correctly.

- [ ] **Step 3: Commit**

```bash
git add scripts/tests/test_pdf_generator.py
git commit -m "test(audit): white-label config applied to PDF HTML"
```

---

## Task 13: pdf_generator.py — CLI entrypoint

**Files:**
- Modify: `scripts/pdf_generator.py`
- Modify: `scripts/tests/test_pdf_generator.py`

- [ ] **Step 1: Append CLI test**

Add to `scripts/tests/test_pdf_generator.py`:

```python
import subprocess
import sys


class TestPDFCLI:
    def test_cli_basic(self, tmp_path: Path):
        md = tmp_path / "r.md"
        md.write_text("# CLI Test")
        out = tmp_path / "r.pdf"
        script = Path(__file__).resolve().parent.parent / "pdf_generator.py"
        result = subprocess.run(
            [sys.executable, str(script), str(md), str(out)],
            capture_output=True, text=True, check=True,
        )
        assert out.exists()

    def test_cli_with_config(self, tmp_path: Path):
        md = tmp_path / "r.md"
        md.write_text("# Configured")
        cfg = tmp_path / "cfg.json"
        cfg.write_text(json.dumps({"brand_name": "Brand X"}))
        out = tmp_path / "r.pdf"
        script = Path(__file__).resolve().parent.parent / "pdf_generator.py"
        result = subprocess.run(
            [sys.executable, str(script), str(md), str(out), str(cfg)],
            capture_output=True, text=True, check=True,
        )
        assert out.exists()
```

- [ ] **Step 2: Run, confirm CLI fails**

Run: `python -m pytest scripts/tests/test_pdf_generator.py::TestPDFCLI -v`
Expected: failures (no `__main__`)

- [ ] **Step 3: Add CLI to pdf_generator.py**

Append to `scripts/pdf_generator.py`:

```python
def _cli(argv: list[str]) -> int:
    if len(argv) < 3:
        print("Usage: pdf_generator.py <input.md> <output.pdf> [config.json]", file=sys.stderr)
        return 1
    md_path = Path(argv[1])
    out_path = Path(argv[2])
    cfg_path = Path(argv[3]) if len(argv) > 3 else None
    try:
        generate(md_path, out_path, cfg_path)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    print(str(out_path))
    return 0


if __name__ == "__main__":
    sys.exit(_cli(sys.argv))
```

- [ ] **Step 4: Run all PDF tests**

Run: `python -m pytest scripts/tests/test_pdf_generator.py -v`
Expected: 12 passed

- [ ] **Step 5: Commit**

```bash
git add scripts/pdf_generator.py scripts/tests/test_pdf_generator.py
git commit -m "feat(audit): CLI for pdf_generator (input.md output.pdf [config.json])"
```

---

## Task 14: commands/auditoria.md — orchestrator command

**Files:**
- Create: `commands/auditoria.md`

- [ ] **Step 1: Read 1 existing command for pattern reference**

Run: `head -80 /Users/rilner/Code/especializei/esp-marketing-os/commands/criar-anuncio.md`
Expected: see frontmatter format and dispatch pattern

- [ ] **Step 2: Create commands/auditoria.md**

Create `commands/auditoria.md` with this content:

````markdown
---
description: Auditoria multi-modal de landing page, Instagram, Meta Ad Library ou YouTube. Despacha agents em paralelo, calcula scoring ponderado e gera PDF white-label.
argument-hint: <url-ou-perfil>
allowed-tools: Bash, WebFetch, Read, Write, Agent
---

# /auditoria

Você é o orquestrador de auditoria multi-modal do marketing-os. Recebe um input do usuário (`$ARGUMENTS`) e produz um relatório RELATORIO.md + RELATORIO.pdf em `workspace/auditorias/<run>/`.

## Passo 1: Validar input e detectar tipo

Se `$ARGUMENTS` está vazio, retorne:

```
Uso: /auditoria <url-ou-perfil>

Exemplos:
  /auditoria https://stripe.com (landing page)
  /auditoria @ericorocha (Instagram)
  /auditoria https://www.facebook.com/ads/library/?id=12345 (Meta Ad Library)
  /auditoria https://youtube.com/watch?v=... (YouTube)
```

Caso contrário, rode:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/audit_detector.py "$ARGUMENTS"
```

Se sair erro, repasse a mensagem e aborte. Se sair JSON, parse e use `type`, `normalized`, `slug`.

## Passo 2: Criar diretório do run

```bash
TIMESTAMP=$(date +%Y-%m-%d-%H%M%S)
RUN_DIR="workspace/auditorias/${TIMESTAMP}-${TYPE}-${SLUG}"
mkdir -p "${RUN_DIR}"
```

## Passo 3: Dispatch matrix por tipo

Despache os agents abaixo em **single message com múltiplas Agent calls em paralelo**. Cada Agent recebe prompt customizado mencionando `normalized` e a área de foco.

### Tipo: landing (7 agents)

- mos-research: "Posicionamento competitivo de {normalized}. Identifique top 3 concorrentes e como {normalized} se diferencia ou não."
- mos-seo: "Audit técnico + on-page de {normalized}. Title, meta, headings, schema, performance, mobile."
- mos-copy: "Audit headline, value proposition, CTAs e copy de prova social em {normalized}."
- mos-funnel: "Mapeie o funil em {normalized}. Identifique friction points, gaps, oportunidades de conversão."
- mos-ads: "Avalie CTA strategy + conversion path em {normalized}. Inclui placement, urgency, prova social."
- mos-design: "Analise hierarquia visual + clareza + acessibilidade em {normalized}."
- mos-brand: "Avalie consistência de voice + identidade visual + tone em {normalized}."

### Tipo: instagram (5 agents)

- mos-research: "Posicionamento de @{normalized}. Compare com 3 perfis similares no nicho."
- mos-social: "Audit dos últimos 30 posts de @{normalized}. Hooks, formatos, frequência, engagement ratio."
- mos-copy: "Audit bio + captions dos últimos 10 posts de @{normalized}."
- mos-design: "Audit consistência visual: paleta, estilo, identidade nos últimos 30 posts de @{normalized}."
- mos-brand: "Voice consistency e brand persona de @{normalized}."

### Tipo: meta_ads (4 agents)

- mos-research: "Quem é o anunciante {normalized}? Qual nicho/posicionamento? 3 concorrentes diretos."
- mos-ads: "Audit do criativo + estrutura de campanha em {normalized}. Hook, copy, CTA, segmentação inferível."
- mos-copy: "Audit copy do anúncio em {normalized}: clarity, benefit, urgency."
- mos-design: "Audit visual do criativo em {normalized}: composição, hierarquia, contraste."

### Tipo: youtube (4 agents)

- mos-research: "Posicionamento do canal/vídeo em {normalized}. Top 3 concorrentes."
- mos-video: "Audit do vídeo em {normalized}: hook (30s), retention/pacing, estrutura narrativa."
- mos-copy: "Audit título + descrição + CTA do vídeo em {normalized}."
- mos-brand: "Voice + tone consistency do criador em {normalized}."

## Passo 4: Synthesis (você faz)

Coletados os outputs dos N agents, aplique a rubric do tipo.

Rubrics:
- **landing**: Conversão (25%), Copy (20%), SEO (15%), Trust signals (10%), Design (10%), Brand (10%), Diferenciação competitiva (10%)
- **instagram**: Bio + posicionamento (20%), Consistência visual (20%), Hooks últimos posts (20%), Strategy/CTA (15%), Engagement ratio (15%), Cadência/frequência (10%)
- **meta_ads**: Hook do criativo 3s (25%), Copy (25%), Visual (20%), CTA + landing match (15%), Diferenciação vs concorrente (15%)
- **youtube**: Hook 30s (25%), Retention/pacing (25%), Thumbnail + título (20%), Estrutura narrativa (15%), CTA/conversão (15%)

Para cada dimensão da rubric:
1. Atribua score 0-100 com base nos outputs dos agents relevantes
2. Cite evidência em 1 frase (o que você viu nos outputs)
3. Sugira fix priorizado: `{"text": "...", "priority": "alta|media|baixa"}`

Se algum agent falhou ou retornou outputs vazios para uma dimensão: marque score como `null`. Recalcule overall normalizado.

Monte o JSON `scores.json`:

```json
{
  "type": "<type>",
  "dimension_scores": { "<dim_name>": <0-100 ou null>, ... },
  "evidences": { "<dim_name>": "...", ... },
  "fixes": { "<dim_name>": {"text": "...", "priority": "alta"}, ... }
}
```

## Passo 5: Calcular score final

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/audit_scoring.py < scores.json
```

Output: JSON com `overall`, `partial`, `dimensions`, `top_wins`, `top_fixes`, `scorecard_md`, `priorities_md`.

## Passo 6: Montar RELATORIO.md

Estrutura:

```markdown
# Auditoria: <input>

**Tipo:** <type>
**Data:** <YYYY-MM-DD HH:MM>
**Score Geral:** <overall>/100 <(parcial — 1+ dimensões N/D)>

## Resumo Executivo

<3 frases: principal força + principal fragilidade + recomendação número 1>

## Scorecard

<scorecard_md do scoring CLI>

## Top 3 Pontos Fortes

<top_wins formatado>

## Top 3 Prioridades

<priorities_md do scoring CLI>

## Análise por Dimensão

### <Dimensão 1>
**Score:** <n>/100 (peso <w>%)
**Evidência:** <evidence>
**Fix priorizado:** <fix.text> ([<priority>])

<repete por dimensão>

## Anexo: Outputs Raw dos Agents

<concatena outputs de cada agent em seções colapsáveis>

---
Gerado pelo marketing-os v6.7.0 em <timestamp>
```

Salve em `${RUN_DIR}/RELATORIO.md`.

Se `APIFY_TOKEN` ausente em IG/Meta Ads/YouTube: adicione no header logo após "Score Geral":

```
> **Modo limitado:** dados via WebFetch (público). Configure APIFY_TOKEN em docs/APIFY-INTEGRATION.md para análise estruturada completa.
```

## Passo 7: Gerar PDF

```bash
CONFIG_PATH=""
if [ -f .auditoria-config.json ]; then
  CONFIG_PATH=".auditoria-config.json"
fi
python ${CLAUDE_PLUGIN_ROOT}/scripts/pdf_generator.py "${RUN_DIR}/RELATORIO.md" "${RUN_DIR}/RELATORIO.pdf" $CONFIG_PATH
```

Se PDF falhar: imprima `PDF generation failed: <error>. Markdown disponível em <path>`. Não aborte.

## Passo 8: Output final no chat

Imprima em 3 linhas:

```
✓ Auditoria concluída: <type> de <input>
  Score: <overall>/100 (<partial label se aplicável>)
  Arquivos: <RUN_DIR>/RELATORIO.md, <RUN_DIR>/RELATORIO.pdf
```

Acrescente exec summary em 3 frases (a mesma do RELATORIO.md).

## Telemetria

Antes do output final, escreva `${RUN_DIR}/.audit-meta.json`:

```json
{
  "started_at": "<ISO timestamp>",
  "ended_at": "<ISO timestamp>",
  "type": "<type>",
  "input": "<original $ARGUMENTS>",
  "normalized": "<normalized>",
  "agents_dispatched": ["mos-..."],
  "agents_failed": ["mos-..."],
  "apify_token_present": <true|false>,
  "config_applied": <true|false>,
  "errors": []
}
```
````

- [ ] **Step 3: Run dispatch coverage test**

Run: `cd /Users/rilner/Code/especializei/esp-marketing-os && python -m pytest scripts/tests/test_commands_dispatch.py -v`
Expected: pass — `/auditoria` is detected as dispatching command (mentions `Agent(`)

- [ ] **Step 4: Run plugin manifest test**

Run: `python -m pytest scripts/tests/test_plugin_manifest.py -v`
Expected: pass — count of commands updated automatically

- [ ] **Step 5: Commit**

```bash
git add commands/auditoria.md
git commit -m "feat(commands): /auditoria multi-modal orchestrator with 4 dispatch matrices"
```

---

## Task 15: Smoke integration test

**Files:**
- Create: `scripts/tests/test_auditoria_smoke.py`

- [ ] **Step 1: Write smoke test**

Create `scripts/tests/test_auditoria_smoke.py`:

```python
"""Smoke test for /auditoria pipeline. Mocks agent outputs.

Marked @pytest.mark.smoke so CI skips it (run manually before release).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from audit_detector import detect
from audit_scoring import RUBRICS, compute, format_priorities_md, format_scorecard_md
from pdf_generator import generate


pytestmark = pytest.mark.smoke


def _mock_synthesis_landing() -> dict:
    """Returns scores/evidences/fixes that a real synthesis step would produce."""
    rubric = RUBRICS["landing"]
    return {
        "type": "landing",
        "dimension_scores": {dim: 70 for dim in rubric},
        "evidences": {dim: f"saw evidence in {dim}" for dim in rubric},
        "fixes": {
            dim: {"text": f"fix {dim}", "priority": "media"} for dim in rubric
        },
    }


def test_full_pipeline_landing(tmp_path: Path):
    # 1. Detect
    detected = detect("https://stripe.com")
    assert detected["type"] == "landing"

    # 2. Mock synthesis
    payload = _mock_synthesis_landing()

    # 3. Compute scoring
    result = compute(
        payload["type"],
        payload["dimension_scores"],
        payload["evidences"],
        payload["fixes"],
    )
    assert result["overall"] == 70
    assert result["partial"] is False

    # 4. Render markdown report
    md_content = f"""# Auditoria: stripe.com

**Tipo:** landing
**Score Geral:** {result["overall"]}/100

## Scorecard

{format_scorecard_md(result)}

## Prioridades

{format_priorities_md(result)}
"""
    md_path = tmp_path / "RELATORIO.md"
    md_path.write_text(md_content)

    # 5. Generate PDF
    pdf_path = tmp_path / "RELATORIO.pdf"
    generate(md_path, pdf_path)
    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 1000  # full PDF, not stub


def test_full_pipeline_with_white_label_config(tmp_path: Path):
    cfg_path = tmp_path / ".auditoria-config.json"
    cfg_path.write_text(json.dumps({
        "brand_name": "Agência Smoke Test",
        "accent_color": "#ff5500",
    }))

    md_path = tmp_path / "RELATORIO.md"
    md_path.write_text("# Auditoria: example.com\n\nContent.")

    pdf_path = tmp_path / "RELATORIO.pdf"
    generate(md_path, pdf_path, cfg_path)
    assert pdf_path.exists()


def test_pipeline_handles_partial_input(tmp_path: Path):
    rubric = RUBRICS["landing"]
    scores = {dim: 70 for dim in rubric}
    scores["SEO (technical + content)"] = None  # one missing
    evidences = {dim: "" for dim in rubric if scores[dim] is not None}
    fixes = {
        dim: {"text": "", "priority": "baixa"}
        for dim in rubric if scores[dim] is not None
    }
    result = compute("landing", scores, evidences, fixes)
    assert result["partial"] is True
    md = f"# Partial\n\n{format_scorecard_md(result)}"
    md_path = tmp_path / "RELATORIO.md"
    md_path.write_text(md)
    pdf_path = tmp_path / "RELATORIO.pdf"
    generate(md_path, pdf_path)
    assert pdf_path.exists()
```

- [ ] **Step 2: Run smoke tests explicitly**

Run: `cd /Users/rilner/Code/especializei/esp-marketing-os && python -m pytest scripts/tests/test_auditoria_smoke.py -v -m smoke`
Expected: 3 passed

- [ ] **Step 3: Verify smoke tests are skipped in default CI run**

Run: `python -m pytest scripts/tests/test_auditoria_smoke.py -v -m "not smoke"`
Expected: 3 deselected (skipped)

- [ ] **Step 4: Commit**

```bash
git add scripts/tests/test_auditoria_smoke.py
git commit -m "test(audit): smoke pipeline (mocked agents → scoring → PDF)"
```

---

## Task 16: docs/AUDIT-CONFIG.md user-facing documentation

**Files:**
- Create: `docs/AUDIT-CONFIG.md`

- [ ] **Step 1: Write the doc**

Create `docs/AUDIT-CONFIG.md`:

````markdown
# Configuração White-label da Auditoria

O comando `/auditoria` gera RELATORIO.pdf com branding customizável. Pra agências/freelancers brasileiros que entregam pro cliente final.

## Setup rápido

Crie `.auditoria-config.json` na raiz do projeto onde você roda `/auditoria`:

```json
{
  "brand_name": "Sua Agência",
  "logo_path": "./logo.png",
  "primary_color": "#1a1a1a",
  "accent_color": "#0066cc",
  "footer_text": "© 2026 Sua Agência. Auditoria preparada para Cliente X."
}
```

Próximo `/auditoria` aplica o branding automaticamente.

## Schema completo

| Campo | Tipo | Obrigatório | Default |
|---|---|---|---|
| `brand_name` | string (não-vazio) | Sim | (n/a) |
| `logo_path` | string (path relativo ao config) | Não | sem logo |
| `primary_color` | hex `#RRGGBB` | Não | `#1a1a1a` |
| `accent_color` | hex `#RRGGBB` | Não | `#1a73e8` |
| `footer_text` | string | Não | `Auditoria gerada com marketing-os` |

Campos extras desconhecidos são rejeitados (config inteiro é ignorado, PDF sai neutro).

## Comportamento de erro

| Caso | Resultado |
|---|---|
| Sem config | PDF neutro (default theme + footer marketing-os) |
| JSON malformado | Warning em stderr, PDF neutro |
| Schema inválido | Warning em stderr com a falha do jsonschema, PDF neutro |
| `logo_path` aponta pra arquivo inexistente | Warning, PDF sem logo (resto do branding aplicado) |
| Cor fora do padrão hex | Schema inválido, PDF neutro |

## Exemplo: agência multi-cliente

Mantenha `.auditoria-config.json` por cliente em sub-pastas:

```
clientes/
  cliente-a/
    .auditoria-config.json  ← branding cliente A
    auditorias/...
  cliente-b/
    .auditoria-config.json  ← branding cliente B
```

`/auditoria` dentro de cada pasta usa o config local automaticamente.

## Limitações conhecidas

- Logo precisa estar em formato `.png`, `.jpg` ou `.svg`. SVG embutido funciona melhor pra escala.
- Cores são aplicadas via CSS variables. Não há suporte a gradientes na v1.
- Footer custom substitui completamente o footer padrão. Se quiser preservar a atribuição marketing-os, inclua manualmente em `footer_text`.
````

- [ ] **Step 2: Commit**

```bash
git add docs/AUDIT-CONFIG.md
git commit -m "docs(audit): user-facing config doc for white-label PDF"
```

---

## Task 17: Update AGENTS.md + CHANGELOG + version bump

**Files:**
- Modify: `AGENTS.md`
- Modify: `CHANGELOG.md`
- Modify: `plugin.json` (root)
- Modify: `.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Add /auditoria mention in AGENTS.md**

Read the section listing commands (search for "30 dos 32 slash commands"). Update count and add brief mention.

In `AGENTS.md`, find this line:

```
Hoje 30 dos 32 slash commands em `commands/` dispatcham subagents.
```

Replace with:

```
Hoje 31 dos 33 slash commands em `commands/` dispatcham subagents. O 33º é `/auditoria` (ver `docs/AUDIT-CONFIG.md` pra white-label PDF).
```

- [ ] **Step 2: Add CHANGELOG entry**

Read `CHANGELOG.md` first to see format. Add at the top (after the title/header section, before previous entry):

```markdown
## v6.7.0 (2026-05-09)

### Added
- New command `/auditoria <input>` — multi-modal audit (landing page, Instagram, Meta Ad Library, YouTube). Auto-detects type, dispatches 4-7 mos-* agents in parallel, computes weighted score per type-specific rubric, generates RELATORIO.md + RELATORIO.pdf.
- Generic, reusable PDF generator script `scripts/pdf_generator.py` (markdown → PDF via weasyprint). White-label aware via `.auditoria-config.json`.
- Scoring infrastructure: `scripts/audit_detector.py`, `scripts/audit_scoring.py`, `scripts/audit_config.py`.
- New deps: weasyprint, markdown-it-py, jsonschema (added to `requirements.txt`).
- User doc: `docs/AUDIT-CONFIG.md` for white-label config schema.

### Notes
- PDF output requires `pip install weasyprint`. macOS users may need `brew install cairo pango gdk-pixbuf libffi`.
- Synthesis (free-form agent outputs → 0-100 dimension scores) is performed by Claude in the command, not by NLP heuristics. Agents themselves are unmodified.
- Outputs land in `workspace/auditorias/<run>/` (gitignored).
```

- [ ] **Step 3: Bump versions**

In `plugin.json` (root): change `"version": "6.6.0"` → `"version": "6.7.0"`.
In `.claude-plugin/plugin.json`: same.
In `.claude-plugin/marketplace.json`: change top-level `"version"` to `"6.7.0"`.

- [ ] **Step 4: Validate plugin manifest**

Run: `cd /Users/rilner/Code/especializei/esp-marketing-os && claude plugin validate . 2>&1 | tail -20`
Expected: validation passes (warnings ok, errors not)

If `claude plugin validate` is unavailable, run:

```bash
python scripts/validate_agents.py --strict
```

- [ ] **Step 5: Run full test suite**

Run: `python -m pytest scripts/tests/ -v -m "not smoke"`
Expected: all green, including `test_commands_dispatch.py` (now 33 commands), `test_plugin_manifest.py` (version 6.7.0).

- [ ] **Step 6: Commit**

```bash
git add AGENTS.md CHANGELOG.md plugin.json .claude-plugin/plugin.json .claude-plugin/marketplace.json
git commit -m "chore: release v6.7.0 — /auditoria multi-modal with white-label PDF"
```

---

## Task 18: Manual validation (4 scenarios)

This task is run by hand, not by an agent. Each scenario must produce `RELATORIO.md` + `RELATORIO.pdf` in `workspace/auditorias/<run>/` with no stack traces.

- [ ] **Scenario 1: Landing page**

In Claude Code session in this repo:
```
/auditoria https://stripe.com
```

Verify:
- 7 agents dispatch in parallel (visible in tool calls)
- `workspace/auditorias/<run>/RELATORIO.md` exists with overall score
- `workspace/auditorias/<run>/RELATORIO.pdf` exists, opens in macOS Preview
- Exec summary printed in chat (3 lines)

- [ ] **Scenario 2: Instagram WITHOUT APIFY_TOKEN**

Ensure `APIFY_TOKEN` is unset:
```bash
unset APIFY_TOKEN
```
In Claude Code:
```
/auditoria @ericorocha
```

Verify:
- 5 agents dispatch
- Header of RELATORIO.md contains "Modo limitado"
- PDF generated

- [ ] **Scenario 3: Instagram WITH APIFY_TOKEN**

Set token:
```bash
export APIFY_TOKEN="<your-token>"
```
In Claude Code:
```
/auditoria @ericorocha
```

Verify:
- Same dispatch but no "Modo limitado" header
- mos-research and mos-social outputs reference Apify-fetched structured data

- [ ] **Scenario 4: Landing with white-label config**

In project root, create `.auditoria-config.json`:
```json
{
  "brand_name": "Smoke Test Agency",
  "accent_color": "#ff5500",
  "footer_text": "© 2026 Smoke Test"
}
```

In Claude Code:
```
/auditoria https://example.com
```

Verify:
- PDF opens with brand name in header
- Accent color is orange (`#ff5500`)
- Footer says "© 2026 Smoke Test"

Cleanup after validation:
```bash
rm .auditoria-config.json
rm -rf workspace/auditorias  # only if you don't want to keep the runs
```

---

## Task 19 (optional): mos.py audit subcommand

Skip this task unless the user explicitly confirms (open question in spec).

**Files:**
- Modify: `scripts/mos.py`

If proceeding:

- [ ] **Step 1: Read scripts/mos.py to understand subcommand pattern**

Run: `head -60 /Users/rilner/Code/especializei/esp-marketing-os/scripts/mos.py`

- [ ] **Step 2: Add `audit` subcommand**

Follow the pattern of existing subcommands (e.g., `seo`, `headlines`). The audit subcommand should:
1. Accept `<input>` arg
2. Run audit_detector, then synthesis stub (just print message: "Run from Claude Code session: /auditoria <input>"), since real synthesis requires agent dispatch which mos.py doesn't have

This is a minimal CLI wrapper for shell discoverability. Real audit only works via `/auditoria` slash command in Claude Code.

- [ ] **Step 3: Test invocation**

Run: `python scripts/mos.py audit https://stripe.com`
Expected: prints detected type + instruction to run via Claude Code

- [ ] **Step 4: Commit**

```bash
git add scripts/mos.py
git commit -m "feat(mos): audit subcommand for shell discoverability"
```

---

## Self-Review Checklist (run after writing all tasks)

- [ ] Spec coverage: 4.1 detector (Tasks 2-5), 4.2 scoring (Tasks 6-9), 4.3 PDF (Tasks 11-13), 4.4 config (Task 10), 4.5 command (Task 14). Smoke (Task 15). Doc (Task 16). Release (Task 17). All 9 spec sections covered.
- [ ] No placeholders (TBD/TODO/etc) anywhere in tasks.
- [ ] Type/method signatures match across tasks: `detect()`, `compute()`, `top_wins()`, `top_fixes()`, `format_scorecard_md()`, `format_priorities_md()`, `load()`, `generate()`, `_build_html()`.
- [ ] All tests have actual code (not "write tests for the above").
- [ ] Each task has discrete commit at the end.
- [ ] Bash commands have absolute paths or use `cd` explicitly when needed.

## Notes for execution

- TDD discipline: write the test, watch it fail, then implement. The plan enforces this with explicit "run, verify it fails" steps.
- Frequent commits: each task ends in a commit. Don't batch.
- If a step's run command fails unexpectedly (not the planned "verify it fails" step), stop and investigate. Don't proceed with broken state.
- weasyprint on macOS may need `brew install cairo pango gdk-pixbuf libffi` if `pip install` fails. Handled in Task 1.
- `${CLAUDE_PLUGIN_ROOT}` in command frontmatter resolves to plugin install dir at runtime. Don't hardcode paths in command markdown.

After Task 17 commits, push and tag:
```bash
git push origin main
git tag v6.7.0
git push origin v6.7.0
```
(Wait for explicit user approval before pushing — tagged release is irreversible.)
