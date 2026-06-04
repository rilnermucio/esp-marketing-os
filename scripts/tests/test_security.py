#!/usr/bin/env python3
"""Guard-rails de segurança do runtime (travam regressão de SSL e SSRF)."""
from __future__ import annotations

import re
import socket
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import audit_screenshot
import validators

_SSL_OFF = re.compile(
    r"CERT_NONE|check_hostname\s*=\s*False|verify\s*=\s*False|_create_unverified"
)


def test_no_script_disables_ssl_verification():
    # Regressão: ninguém pode reintroduzir TLS sem verificação (risco de MITM).
    offenders = [
        p.name
        for p in (ROOT / "scripts").glob("*.py")
        if _SSL_OFF.search(p.read_text(encoding="utf-8"))
    ]
    assert not offenders, f"verificação SSL desabilitada em: {offenders}"


def test_ssrf_guard_blocks_internal_targets():
    for u in [
        "http://127.0.0.1/",
        "http://169.254.169.254/",  # metadata de cloud
        "http://10.0.0.5/",
        "http://192.168.1.1/",
        "http://localhost/",
        "http://[::1]/",
    ]:
        assert validators.url_aponta_para_rede_interna(u), u


def test_ssrf_guard_allows_public(monkeypatch):
    monkeypatch.setattr(
        socket, "getaddrinfo", lambda *a, **k: [(2, 1, 6, "", ("93.184.216.34", 0))]
    )
    assert not validators.url_aponta_para_rede_interna("http://example.com/")


def test_ssrf_guard_unresolvable_is_not_internal(monkeypatch):
    def boom(*a, **k):
        raise socket.gaierror("nxdomain")

    monkeypatch.setattr(socket, "getaddrinfo", boom)
    assert not validators.url_aponta_para_rede_interna("http://nope.invalid/")


def test_screenshot_capture_blocks_internal_url(tmp_path):
    with pytest.raises(ValueError, match="interna|anti-SSRF"):
        audit_screenshot.capture("http://127.0.0.1/", tmp_path)
