"""Registro de fatos de plataforma com fonte e data (auditoria 2026-09-28, achado #10)."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import check_platform_facts as facts

ROOT = Path(__file__).resolve().parents[2]


def test_registry_rows_have_source_and_valid_date():
    rows = facts.parse_facts(
        (ROOT / "references" / "platform-facts.md").read_text(encoding="utf-8")
    )
    assert len(rows) >= 7
    invalid, _ = facts.problems(rows, date(2026, 9, 28), max_days=10_000)
    assert not invalid, invalid


def test_stale_rows_are_reported():
    text = (
        "| Plataforma | Fato | Valor | Desde | Fonte | Verificado em |\n"
        "|---|---|---|---|---|---|\n"
        "| X | Limite | 1 | 2020 | https://exemplo.com | 2025-01-01 |\n"
    )
    invalid, stale = facts.problems(
        facts.parse_facts(text), date(2026, 1, 1), max_days=180
    )
    assert not invalid
    assert stale and "verificado há 365 dias" in stale[0]


def test_missing_url_and_bad_date_are_invalid():
    text = "| X | Limite | 1 | 2020 | sem url | ontem |\n"
    invalid, _ = facts.problems(facts.parse_facts(text), date(2026, 1, 1), max_days=180)
    assert any("fonte sem URL" in i for i in invalid)
    assert any("data de verificação inválida" in i for i in invalid)


def test_strict_exit_code(tmp_path):
    registry = tmp_path / "facts.md"
    registry.write_text(
        "| X | Limite | 1 | 2020 | https://exemplo.com | 2020-01-01 |\n",
        encoding="utf-8",
    )
    assert (
        facts.main(["--arquivo", str(registry), "--hoje", "2026-09-28", "--strict"])
        == 1
    )
    assert (
        facts.main(["--arquivo", str(registry), "--hoje", "2020-02-01", "--strict"])
        == 0
    )


def test_compliance_reference_age():
    text = "> **Verificado em 2026-09-28** no texto integral das normas."
    assert facts.compliance_age(text, date(2026, 10, 28)) == 30
    assert facts.compliance_age("sem data", date(2026, 10, 28)) is None


def test_compliance_reference_goes_stale_after_a_quarter(capsys):
    """Relativo à data declarada no arquivo, para não quebrar a cada revisão."""
    import re
    from datetime import datetime, timedelta

    text = facts.COMPLIANCE_FILE.read_text(encoding="utf-8")
    checked = datetime.strptime(
        re.search(r"Verificado em (\d{4}-\d{2}-\d{2})", text).group(1), "%Y-%m-%d"
    ).date()
    late = checked + timedelta(days=facts.COMPLIANCE_MAX_DAYS + 1)
    facts.main(["--hoje", late.isoformat()])
    assert "compliance-br.md verificado há" in capsys.readouterr().out
