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
PROFILES_PATH = REPO_ROOT / "scripts" / "evals" / "output-profiles.json"
RUNNER = REPO_ROOT / "scripts" / "copy_output_eval.py"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
from copy_output_eval import (  # noqa: E402
    build_pair_prompt,
    consolidate_pair,
    resolve_profile,
    score_text,
)

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
AGENTES_PRIORITARIOS = {
    "mos-copy",
    "mos-email",
    "mos-ads",
    "mos-offer",
    "mos-funnel",
    "mos-seo",
    "mos-video",
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


def test_perfis_cobrem_agentes_prioritarios_e_criterios():
    payload = json.loads(PROFILES_PATH.read_text(encoding="utf-8"))
    assert payload["version"] == 1
    assert AGENTES_PRIORITARIOS <= {
        profile["agent"] for profile in payload["profiles"].values()
    }

    criteria_sets = payload["criteria_sets"]
    for profile_id, profile in payload["profiles"].items():
        assert profile["quality_gate_type"] in QG_TYPES_VALIDOS
        assert profile["criteria_set"] in criteria_sets
        criteria = criteria_sets[profile["criteria_set"]]
        assert len(criteria) >= 5, f"{profile_id}: poucos critérios"
        criterion_ids = [criterion["id"] for criterion in criteria]
        assert len(criterion_ids) == len(set(criterion_ids))


def test_resolve_profile_preserva_formatos_e_seleciona_dominio():
    assert resolve_profile(formato="post").id == "copy-post"
    assert resolve_profile(formato="sales").id == "copy-sales"

    video = resolve_profile(profile_id="video")
    assert video.agent == "mos-video"
    assert video.quality_gate_type == "video"
    assert [criterion.id for criterion in video.criteria] == [
        "hook",
        "retencao",
        "ritmo",
        "direcao_visual",
        "cta",
        "fit",
    ]


def test_score_text_retorna_contrato_generico():
    profile = resolve_profile(profile_id="seo")
    resultado = score_text(
        "Como escolher uma pauta de SEO útil. Leia os dados, valide a intenção "
        "de busca e registre a hipótese antes de publicar.",
        profile,
    )

    assert resultado["profile"] == "seo"
    assert resultado["agent"] == "mos-seo"
    assert resultado["quality_gate_type"] == "artigo"
    assert 0 <= resultado["score"] <= 100
    assert "checks" in resultado


def test_build_pair_prompt_usa_criterios_do_perfil():
    profile = resolve_profile(profile_id="video")
    prompt = build_pair_prompt(
        "ROTEIRO-CANDIDATO",
        "ROTEIRO-REFERENCIA",
        profile=profile,
        briefing="Vídeo curto para público frio.",
        invert=True,
    )

    assert prompt.index("ROTEIRO-REFERENCIA") < prompt.index("ROTEIRO-CANDIDATO")
    assert "direcao_visual" in prompt
    assert "especificidade" not in prompt
    assert "Vídeo curto para público frio." in prompt


def test_consolidate_pair_mapeia_rotulos_e_detecta_inconsistencia():
    profile = resolve_profile(profile_id="copy-post")
    criteria = [criterion.id for criterion in profile.criteria]
    normal = {
        "veredictos": [
            {"criterio": criterion, "vencedor": "A", "motivo": "normal"}
            for criterion in criteria
        ],
        "vencedor_geral": "A",
    }
    inverted = {
        "veredictos": [
            {
                "criterio": criterion,
                "vencedor": "A" if criterion == "hook" else "B",
                "motivo": "invertida",
            }
            for criterion in criteria
        ],
        "vencedor_geral": "B",
    }

    resultado = consolidate_pair(normal, inverted, profile=profile)
    por_criterio = {verdict["criterio"]: verdict for verdict in resultado["veredictos"]}

    assert resultado["vencedor_geral"] == "candidato"
    assert resultado["consistente"] is False
    assert por_criterio["hook"]["vencedor"] == "inconclusivo"
    assert por_criterio["cta"]["vencedor"] == "candidato"


def test_consolidate_pair_rejeita_veredicto_sem_motivo():
    profile = resolve_profile(profile_id="copy-post")
    criteria = [criterion.id for criterion in profile.criteria]
    normal = {
        "veredictos": [
            {"criterio": criterion, "vencedor": "A", "motivo": "normal"}
            for criterion in criteria
        ],
        "vencedor_geral": "A",
    }
    inverted = {
        "veredictos": [
            {"criterio": criterion, "vencedor": "B", "motivo": "invertida"}
            for criterion in criteria
        ],
        "vencedor_geral": "B",
    }
    inverted["veredictos"][0].pop("motivo")

    with pytest.raises(ValueError, match="motivo"):
        consolidate_pair(normal, inverted, profile=profile)


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


def test_pair_aceita_formato_legado(tmp_path):
    candidate = tmp_path / "candidato.md"
    reference = tmp_path / "referencia.md"
    candidate.write_text("CANDIDATO", encoding="utf-8")
    reference.write_text("REFERENCIA", encoding="utf-8")

    completed = _run(
        "pair",
        "--candidato",
        str(candidate),
        "--referencia",
        str(reference),
        "--formato",
        "email",
        check=False,
    )

    assert completed.returncode == 0
    assert "PERFIL: email" in completed.stdout


def test_cli_lista_perfis_e_score_por_dominio(tmp_path):
    profiles = json.loads(_run("profiles").stdout)
    assert profiles["video"]["agent"] == "mos-video"
    assert "direcao_visual" in profiles["video"]["criteria"]

    output = tmp_path / "roteiro.md"
    output.write_text(
        "Você perde atenção nos primeiros três segundos? Mostre o resultado, "
        "explique o processo em três cenas e encerre pedindo um comentário.",
        encoding="utf-8",
    )
    score = json.loads(_run("score", str(output), "--profile", "video").stdout)
    assert score["profile"] == "video"
    assert score["agent"] == "mos-video"
    assert score["quality_gate_type"] == "video"


def test_cli_consolida_duas_ordens_e_rejeita_json_incompleto(tmp_path):
    profile = resolve_profile(profile_id="video")
    criteria = [criterion.id for criterion in profile.criteria]
    normal_payload = {
        "veredictos": [
            {"criterio": criterion, "vencedor": "A", "motivo": "normal"}
            for criterion in criteria
        ],
        "vencedor_geral": "A",
    }
    inverted_payload = {
        "veredictos": [
            {"criterio": criterion, "vencedor": "B", "motivo": "invertida"}
            for criterion in criteria
        ],
        "vencedor_geral": "B",
    }
    normal_path = tmp_path / "normal.json"
    inverted_path = tmp_path / "invertida.json"
    normal_path.write_text(json.dumps(normal_payload), encoding="utf-8")
    inverted_path.write_text(json.dumps(inverted_payload), encoding="utf-8")

    result = json.loads(
        _run(
            "consolidate",
            "--normal",
            str(normal_path),
            "--invertida",
            str(inverted_path),
            "--profile",
            "video",
        ).stdout
    )
    assert result["vencedor_geral"] == "candidato"
    assert result["consistente"] is True

    inverted_payload["veredictos"].pop()
    inverted_path.write_text(json.dumps(inverted_payload), encoding="utf-8")
    failed = _run(
        "consolidate",
        "--normal",
        str(normal_path),
        "--invertida",
        str(inverted_path),
        "--profile",
        "video",
        check=False,
    )
    assert failed.returncode == 2
    assert "Critérios divergentes" in failed.stderr
