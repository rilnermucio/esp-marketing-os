"""Guarda estrutural do eval de output do mos-copy.

Valida o golden set de briefs (copy-output-cases.json) e a camada
determinística do runner (copy_output_eval.py). O julgamento par-a-par é
executado fora da suite (custa modelo); aqui garantimos que o prompt do
julgador se monta corretamente e que o scoring é reprodutível.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
CASES_PATH = REPO_ROOT / "docs" / "ai-engineering" / "evals" / "copy-output-cases.json"
RUNNER = REPO_ROOT / "scripts" / "copy_output_eval.py"

pytestmark = pytest.mark.skipif(
    not CASES_PATH.exists(),
    reason="docs/ai-engineering ausente (contexto de pacote Codex)",
)

FORMATOS_VALIDOS = {"headline", "post", "email", "ad", "sales"}
QG_TYPES_VALIDOS = {
    "post",
    "artigo",
    "email",
    "landing-page",
    "anuncio",
    "video",
    "social",
}


def _cases():
    return json.loads(CASES_PATH.read_text(encoding="utf-8"))["cases"]


def test_cases_ids_unicos_e_formato():
    cases = _cases()
    ids = [c["id"] for c in cases]
    assert len(ids) == len(set(ids)), "IDs duplicados no golden set"
    for cid in ids:
        assert re.fullmatch(r"CO-\d{3}", cid), f"ID fora do padrão CO-NNN: {cid}"
    assert len(cases) >= 5, "Baseline exige pelo menos 5 cenários"


@pytest.mark.parametrize("case", _cases(), ids=lambda c: c["id"])
def test_case_tem_campos_e_briefing_completo(case):
    assert case["formato"] in FORMATOS_VALIDOS
    assert case["quality_gate_type"] in QG_TYPES_VALIDOS
    assert case["peca"].strip()
    briefing = case["briefing"]
    # Pre-flight do mos-copy: o briefing precisa carregar todos os inputs
    # (produto, público, consciência, objetivo, tom) pra geração não bloquear.
    assert (
        len(briefing) > 300
    ), f"{case['id']}: briefing curto demais pra passar no pre-flight"
    for marcador in ("Produto:", "Publico:", "consciencia", "Objetivo", "Tom:"):
        assert marcador in briefing, f"{case['id']}: briefing sem '{marcador}'"


def _run(*argv, check=True):
    return subprocess.run(
        [sys.executable, str(RUNNER), *argv],
        capture_output=True,
        text=True,
        check=check,
        cwd=REPO_ROOT,
    )


def test_score_emite_json_deterministico(tmp_path):
    peca = tmp_path / "peca.md"
    peca.write_text(
        "Você posta todo dia e o alcance continua caindo?\n\n"
        "Teste isso no próximo post: comece pela pergunta que seu cliente faria "
        "no Google às 23h. Fizemos isso com uma nutricionista e o salvamento "
        "triplicou em 3 semanas.\n\nSalva esse post pra testar amanhã.\n",
        encoding="utf-8",
    )
    saida1 = json.loads(_run("score", str(peca), "--formato", "post").stdout)
    saida2 = json.loads(_run("score", str(peca), "--formato", "post").stdout)
    assert saida1 == saida2, "Scoring determinístico divergiu entre execuções"
    assert 0 <= saida1["score"] <= 100
    assert saida1["capped_by_ai_tells"] is False
    assert "Vícios de IA" in saida1["checks"]


def test_score_capa_ai_tells(tmp_path):
    peca = tmp_path / "ruim.md"
    peca.write_text(
        "No mundo digital de hoje — em constante evolução — o conteúdo é rei.\n\n"
        "Não é sobre postar mais. É sobre postar melhor. Poste com consistência "
        "brutal e veja a mágica acontecer! Salva esse post e comece agora: "
        "acesse o link na bio pra garantir sua vaga.\n",
        encoding="utf-8",
    )
    saida = json.loads(_run("score", str(peca), "--formato", "post").stdout)
    assert saida["checks"]["Vícios de IA"][
        "issues"
    ], "Âncora negativa deveria acusar vícios"
    assert saida["score"] <= 60, "Score com vício de IA não pode passar de 60"


def test_pair_monta_prompt_com_ordem_invertida(tmp_path):
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_text("TEXTO-CANDIDATO-XYZ", encoding="utf-8")
    b.write_text("TEXTO-REFERENCIA-QWE", encoding="utf-8")

    normal = _run("pair", "--candidato", str(a), "--referencia", str(b)).stdout
    invertido = _run(
        "pair", "--candidato", str(a), "--referencia", str(b), "--inverter"
    ).stdout

    # Ordem normal: candidato é A; invertida: candidato vira B.
    assert normal.index("TEXTO-CANDIDATO-XYZ") < normal.index("TEXTO-REFERENCIA-QWE")
    assert invertido.index("TEXTO-REFERENCIA-QWE") < invertido.index(
        "TEXTO-CANDIDATO-XYZ"
    )
    for prompt in (normal, invertido):
        for criterio, _ in [
            ("hook", ""),
            ("especificidade", ""),
            ("prova", ""),
            ("cta", ""),
            ("naturalidade", ""),
            ("fit", ""),
        ]:
            assert criterio in prompt
        assert "NUNCA dê nota numérica" in prompt
        assert '"vencedor_geral"' in prompt
