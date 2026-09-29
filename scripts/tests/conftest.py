"""Fixtures compartilhadas para testes do Marketing OS."""

from __future__ import annotations

import os
import sys
import json
import shutil
import tempfile
from pathlib import Path

import pytest


def pytest_collection_modifyitems(config, items):
    """Smoke tests chamam o Claude real, rede ou browser: só rodam com MOS_SMOKE=1.

    Sem esta trava, `pytest scripts/tests/` sem marker disparava 22+ execuções
    reais por acidente (auditoria 2026-08-21, item 6).
    """
    if os.environ.get("MOS_SMOKE") == "1":
        return
    skip = pytest.mark.skip(
        reason="smoke test: defina MOS_SMOKE=1 para rodar (custo, rede ou browser reais)"
    )
    for item in items:
        if "smoke" in item.keywords:
            item.add_marker(skip)


# --- Plugin-structure fixtures (added by plugin-first refactor) ---


@pytest.fixture(scope="session")
def project_root() -> Path:
    """Absolute path to the project root."""
    return Path(__file__).resolve().parent.parent.parent


@pytest.fixture(scope="session")
def plugin_dirs(project_root: Path) -> dict[str, Path]:
    """Plugin-side directories that ship with the distributable plugin."""
    return {
        "skills": project_root / "skills",
        "subagents": project_root / "subagents",
        "commands": project_root / "commands",
        "workflows": project_root / "workflows",
        "assets": project_root / "assets",
        "references": project_root / "references",
        "scripts": project_root / "scripts",
        "docs": project_root / "docs",
        "claude_agents": project_root / ".claude" / "agents",
    }


@pytest.fixture(scope="session")
def workspace_root(project_root: Path) -> Path:
    """User-side workspace directory (gitignored)."""
    return project_root / "workspace"


# --- Existing content fixtures (preserved) ---

# Adicionar diretório de scripts ao path
SCRIPTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)


@pytest.fixture
def sample_post():
    """Post de exemplo com acentuação correta e estrutura completa."""
    return """5 dicas de produtividade que você precisa conhecer

Você já se perguntou por que algumas pessoas conseguem fazer tanto em tão pouco tempo?

A verdade é que produtividade não é sobre trabalhar mais, é sobre trabalhar melhor.

1. Planeje seu dia na noite anterior
2. Use a técnica Pomodoro
3. Elimine distrações
4. Priorize tarefas importantes
5. Descanse estrategicamente

Comece agora a transformar sua rotina. Garanta sua produtividade!

#produtividade #dicas #rotina #foco #organizacao"""


@pytest.fixture
def sample_article():
    """Artigo SEO de exemplo."""
    return """# Marketing Digital em 2026: Guia Completo

## Introdução

O marketing digital continua evoluindo rapidamente. Neste artigo, você vai descobrir as principais tendências e estratégias para 2026.

## O que é Marketing Digital

Marketing digital é o conjunto de estratégias voltadas para a promoção de uma marca no ambiente online. Ele utiliza canais como redes sociais, email, SEO, e publicidade paga para alcançar e engajar o público-alvo.

## Tendências para 2026

### Inteligência Artificial no Marketing

A IA está transformando como criamos conteúdo, analisamos dados e personalizamos experiências. Ferramentas de IA generativa permitem criar campanhas mais eficientes e personalizadas.

### Vídeos Curtos

Reels, TikTok e Shorts continuam dominando. O formato de vídeo curto é essencial para qualquer estratégia de conteúdo moderna.

### Marketing Conversacional

WhatsApp Business, chatbots e DMs automatizados estão criando experiências mais pessoais e imediatas para os consumidores.

## Como Implementar

Para implementar uma estratégia eficaz de marketing digital, siga estes passos:

1. Defina seus objetivos
2. Conheça seu público-alvo
3. Escolha os canais adequados
4. Crie conteúdo de valor
5. Meça e otimize constantemente

## Conclusão

O marketing digital em 2026 exige adaptação constante. Comece hoje a implementar essas estratégias e garanta resultados consistentes para seu negócio.

[Fonte: HubSpot](https://hubspot.com) | [Leia mais](/blog/tendencias)

Garanta seu lugar na revolução digital. Acesse nosso curso gratuito!"""


@pytest.fixture
def sample_email():
    """Email marketing de exemplo."""
    return """Garanta sua vaga no evento

Olá,

O evento mais esperado do ano está chegando e as vagas são limitadas.

Neste evento exclusivo, você vai aprender:
- Como triplicar suas vendas em 90 dias
- Estratégias de marketing digital comprovadas
- Técnicas de copywriting avançado

Reserve sua vaga agora e garanta acesso ao bônus exclusivo.

Abraço,
Equipe Marketing OS"""


@pytest.fixture
def sample_unaccented_text():
    """Texto sem acentuação para testar detecção."""
    return """Voce nao sabe o que esta perdendo. Ja pensou em melhorar sua estrategia?
O conteudo que traz resultado e unico. Facil de implementar e muito pratico.
Alem disso, ate os iniciantes conseguem resultados incriveis."""


@pytest.fixture
def tmp_dir():
    """Cria diretório temporário para testes."""
    tmpdir = tempfile.mkdtemp()
    yield tmpdir
    shutil.rmtree(tmpdir)


@pytest.fixture
def tmp_file(tmp_dir):
    """Cria arquivo temporário com conteúdo."""

    def _create(content, filename="test.md"):
        filepath = os.path.join(tmp_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return filepath

    return _create
