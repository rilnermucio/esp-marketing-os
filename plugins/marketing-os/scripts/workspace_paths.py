#!/usr/bin/env python3
"""Onde o Marketing OS grava estado do usuário.

Estado do usuário (projetos, relatórios, coletas) pertence ao projeto em que a
sessão roda, nunca à pasta do plugin. Numa instalação real a pasta do plugin é
um cache versionado: é trocada a cada update e compartilhada por todos os
projetos do usuário (auditoria 2026-09-28, achado #5, F-DIST-03).

Recursos que o plugin distribui (templates, KBs, clones de experts) continuam
relativos ao próprio script.
"""

from __future__ import annotations

import os
from pathlib import Path


def user_workspace() -> Path:
    """Pasta `workspace/` do projeto atual, ou o caminho em MOS_WORKSPACE."""
    override = os.environ.get("MOS_WORKSPACE")
    if override:
        return Path(override).expanduser()
    return Path.cwd() / "workspace"
