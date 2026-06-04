#!/usr/bin/env python3
"""Testes do tts_runner (núcleo determinístico + I/O mockado, sem rodar TTS)."""
from __future__ import annotations

import os
import subprocess
import sys
from unittest.mock import patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import tts_runner as tr


ROTEIRO = """🎬 ROTEIRO REELS (30-60s)

📍 HOOK (0-2s):
"Você sabia que marketing mudou?"
[Texto grande na tela + olhar para câmera]

📍 PONTO 1 (5-15s):
**Primeiro**, defina seu público de forma clara.
[Demonstrar no quadro]

## CTA
Salva esse vídeo e segue pra mais.
"""


# ----------------------------------------------------------- to_speakable
def test_to_speakable_remove_marcacao():
    out = tr.to_speakable(ROTEIRO)
    for ruido in ["📍", "🎬", "**", "##", "(0-2s)", "[", "]"]:
        assert ruido not in out, f"sobrou marcação: {ruido!r}"


def test_to_speakable_mantem_falado_e_remove_stage_direction():
    out = tr.to_speakable(ROTEIRO).lower()
    assert "defina seu público" in out
    assert "salva esse vídeo" in out
    assert "demonstrar no quadro" not in out  # stage direction removida


# ----------------------------------------------------------- voice_for
@pytest.mark.parametrize(
    "tom,engine,esperado",
    [
        ("autoridade", "say", "Felipe"),
        ("masculino", "say", "Felipe"),
        ("energetico", "say", "Luciana"),
        ("qualquer", "say", "Luciana"),
        ("autoridade", "kokoro", "am_adam"),
        ("energetico", "kokoro", "af_nova"),
        ("calmo", "kokoro", "af_sky"),
        ("qualquer", "kokoro", "af_heart"),
    ],
)
def test_voice_for(tom, engine, esperado):
    assert tr.voice_for(tom, engine) == esperado


# ----------------------------------------------------------- build_command
def test_build_command_say():
    cmd = tr.build_command("say", "in.txt", "Luciana", "out.aiff", 1.0)
    assert cmd[0] == "say"
    assert "Luciana" in cmd and "out.aiff" in cmd and "in.txt" in cmd


def test_build_command_kokoro():
    cmd = tr.build_command("kokoro", "in.txt", "af_heart", "out.wav", 1.0)
    assert "hyperframes" in cmd and "tts" in cmd
    assert "af_heart" in cmd and "pt-br" in cmd and "out.wav" in cmd and "in.txt" in cmd


# ----------------------------------------------------------- detect_engine
def test_detect_engine_darwin_usa_say():
    with patch("platform.system", return_value="Darwin"), patch(
        "shutil.which", return_value="/usr/bin/say"
    ):
        assert tr.detect_engine() == "say"


def test_detect_engine_linux_usa_kokoro():
    with patch("platform.system", return_value="Linux"):
        assert tr.detect_engine() == "kokoro"


# ----------------------------------------------------------- run
def test_run_dry_run_nao_executa(tmp_path, capsys):
    with patch("subprocess.run") as mock_run:
        res = tr.run(ROTEIRO, engine="say", output=str(tmp_path / "o.aiff"), dry_run=True)
    mock_run.assert_not_called()
    assert res["ran"] is False
    assert res["command"][0] == "say"


def test_run_executa_e_retorna(tmp_path):
    out = str(tmp_path / "o.aiff")
    fake = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
    with patch("subprocess.run", return_value=fake) as mock_run:
        res = tr.run(ROTEIRO, engine="say", output=out)
    mock_run.assert_called_once()
    assert res["ran"] is True and res["output"] == out


def test_run_falha_do_motor_levanta(tmp_path):
    out = str(tmp_path / "o.wav")
    fail = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="boom")
    with patch("subprocess.run", return_value=fail):
        with pytest.raises(RuntimeError):
            tr.run(ROTEIRO, engine="kokoro", output=out)
