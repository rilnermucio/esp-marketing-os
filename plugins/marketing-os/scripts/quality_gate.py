#!/usr/bin/env python3
"""
Quality Gate - Valida qualidade de conteúdo antes de publicação

Uso:
    python quality_gate.py arquivo.md --type post
    python quality_gate.py arquivo.md --type artigo
    python quality_gate.py arquivo.md --type email
    python quality_gate.py arquivo.md --type landing-page
    python quality_gate.py arquivo.md --type anuncio
"""

import os
import re
import sys
import argparse
from typing import List, Tuple

# Caracteres acentuados esperados em português
ACCENT_PATTERNS = {
    "a_agudo": r"[áÁ]",
    "e_agudo": r"[éÉ]",
    "i_agudo": r"[íÍ]",
    "o_agudo": r"[óÓ]",
    "u_agudo": r"[úÚ]",
    "a_circunflexo": r"[âÂ]",
    "e_circunflexo": r"[êÊ]",
    "o_circunflexo": r"[ôÔ]",
    "a_til": r"[ãÃ]",
    "o_til": r"[õÕ]",
    "cedilha": r"[çÇ]",
    "a_grave": r"[àÀ]",
}

# Palavras comuns que DEVEM ter acento
MUST_ACCENT_WORDS = {
    "voce": "você",
    "nao": "não",
    "ja": "já",
    "ha": "há",
    "esta": "está",
    "sera": "será",
    "tambem": "também",
    "conteudo": "conteúdo",
    "negocio": "negócio",
    "estrategia": "estratégia",
    "unico": "único",
    "pratico": "prático",
    "facil": "fácil",
    "possivel": "possível",
    "incrivel": "incrível",
    "util": "útil",
    "ate": "até",
    "alem": "além",
    "entao": "então",
    "informacao": "informação",
    "solucao": "solução",
    "acao": "ação",
}

# Limites de caracteres por plataforma
PLATFORM_LIMITS = {
    "instagram_feed": {"hook": 125, "total": 2200, "hashtags": 15},
    "instagram_reels": {"hook": 150, "total": 2200, "hashtags": 5},
    "linkedin": {"hook": 210, "total": 3000, "hashtags": 5},
    "twitter": {"hook": 280, "total": 280, "hashtags": 3},
    "tiktok": {"hook": 100, "total": 2200, "hashtags": 5},
}

# Palavras de CTA forte
STRONG_CTA_WORDS = [
    "quero",
    "garanta",
    "comece",
    "acesse",
    "baixe",
    "inscreva",
    "reserve",
    "conquiste",
    "descubra",
    "aprenda",
    "receba",
    "experimente",
    "teste",
    "entre",
    "participe",
    "cadastre",
]

# Palavras de CTA fraca
WEAK_CTA_WORDS = [
    "clique aqui",
    "saiba mais",
    "veja mais",
    "leia mais",
    "confira",
    "acesse o link",
    "link na bio",
]

# Vícios de IA proibidos pelas regras do Marketing OS. Espelham o HARD BLOCK
# de scripts/hooks/quality_gate_hook.py para quem valida via CLI.
# O span interno das antíteses exclui pontuação pra não atravessar cláusulas
# e casar verbo de frase nova não relacionada (falso positivo).
AI_TELL_PATTERNS = [
    (
        r"—",
        "Travessão '—' encontrado: substitua por '.', ',' ou ':' ou quebre a frase",
    ),
    (
        r"(?<!\w)brutal(?!\w)",
        "Palavra 'brutal' encontrada: use intenso, forte, pesado, impactante",
    ),
    (
        r"\bnão é [^.!?,;:\n]{2,60}[.!?,;:]\s+é\b",
        "Antítese negação/afirmação ('Não é X / É Y'): reescreva afirmando direto",
    ),
    (
        r"\bnão (\w{3,})\b[^.!?,;:\n]{0,60}[.!?,;:]\s+\1\b",
        "Antítese com verbo repetido ('Não faça X / Faça Y'): reescreva sem o paralelo",
    ),
]


def read_content(filepath: str) -> str:
    """Lê o conteúdo do arquivo."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def check_accents(content: str) -> Tuple[int, List[str]]:
    """Verifica acentuação do texto em português."""
    issues = []
    words = re.findall(r"\b[a-záàâãéèêíïóôõúüç]+\b", content.lower())

    for word in words:
        if word in MUST_ACCENT_WORDS:
            correct = MUST_ACCENT_WORDS[word]
            if correct.lower() not in content.lower():
                issues.append(f"'{word}' deveria ser '{correct}'")

    # Verificar se há algum acento no texto (indicador básico)
    has_any_accent = bool(re.search(r"[áàâãéèêíïóôõúüç]", content, re.IGNORECASE))

    if not has_any_accent and len(content) > 100:
        issues.append("Texto longo sem nenhum acento — possível texto não acentuado")

    score = max(0, 10 - len(issues) * 2)
    return score, issues


def check_ai_tells(content: str) -> Tuple[int, List[str]]:
    """Detecta vícios de escrita de IA proibidos (travessão, 'brutal', antíteses)."""
    issues = []
    for pattern, message in AI_TELL_PATTERNS:
        matches = re.findall(pattern, content, flags=re.IGNORECASE)
        if matches:
            issues.append(f"{message} ({len(matches)} ocorrência(s))")
    # Regra obrigatória: qualquer ocorrência zera o check, sem gradação
    score = 10 if not issues else 0
    return score, issues


def check_hook(content: str) -> Tuple[int, str, List[str]]:
    """Avalia a força do hook (primeira linha)."""
    lines = [
        l.strip()
        for l in content.strip().split("\n")
        if l.strip() and not l.strip().startswith("#")
    ]
    if not lines:
        return 0, "", ["Nenhum conteúdo encontrado"]

    hook = lines[0]
    issues = []
    score = 5  # Base

    # Verificar comprimento
    if len(hook) < 20:
        issues.append("Hook muito curto (< 20 caracteres)")
    elif len(hook) > 200:
        issues.append("Hook muito longo (> 200 caracteres)")
    else:
        score += 1

    # Verificar padrões fortes
    strong_patterns = [
        (r"^\d+\s", "Começa com número"),
        (r"^como\s", "Formato 'Como'"),
        (r"\?$", "Formato pergunta"),
        (r"\bvocê\b", "Fala com 'você'"),
        (r"\bsegredo", "Usa 'segredo'"),
        (r"\berro", "Usa 'erro'"),
        (r"\bnunca\b", "Usa 'nunca'"),
        (r"\bninguém\b", "Usa 'ninguém'"),
    ]

    patterns_found = []
    for pattern, name in strong_patterns:
        if re.search(pattern, hook, re.IGNORECASE):
            score += 1
            patterns_found.append(name)

    if not patterns_found:
        issues.append("Hook não usa padrões fortes conhecidos")

    score = min(10, score)
    return score, hook, issues


def check_cta(content: str) -> Tuple[int, List[str]]:
    """Verifica presença e qualidade do CTA."""
    content_lower = content.lower()
    issues = []
    score = 0

    # Verificar presença de CTA forte
    strong_found = [w for w in STRONG_CTA_WORDS if w in content_lower]
    weak_found = [w for w in WEAK_CTA_WORDS if w in content_lower]

    if strong_found:
        score += 7
    elif weak_found:
        score += 3
        issues.append(f"CTA fraco detectado: {', '.join(weak_found)}")
        issues.append(
            "Substitua por CTAs de ação: 'Quero [benefício]', 'Garanta sua vaga'"
        )
    else:
        issues.append("Nenhum CTA detectado no conteúdo")

    # Verificar se CTA está no final (últimas 20% do texto)
    lines = content.strip().split("\n")
    last_section = "\n".join(lines[int(len(lines) * 0.8) :]).lower()

    if any(w in last_section for w in STRONG_CTA_WORDS + WEAK_CTA_WORDS):
        score += 3
    else:
        issues.append("CTA não está posicionado no final do conteúdo")

    return min(10, score), issues


def check_readability(content: str) -> Tuple[int, List[str]]:
    """Verifica legibilidade do texto."""
    issues = []

    # Remover markdown headers e formatação
    clean = re.sub(r"^#+\s.*$", "", content, flags=re.MULTILINE)
    clean = re.sub(r"[*_`\[\]()]", "", clean)

    sentences = re.split(r"[.!?]+", clean)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 5]

    if not sentences:
        return 5, ["Não foi possível analisar sentenças"]

    # Comprimento médio das sentenças
    avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)

    if avg_sentence_length > 25:
        issues.append(
            f"Sentenças muito longas (média: {avg_sentence_length:.0f} palavras)"
        )
        score = 4
    elif avg_sentence_length > 20:
        issues.append(
            f"Sentenças um pouco longas (média: {avg_sentence_length:.0f} palavras)"
        )
        score = 6
    elif avg_sentence_length > 10:
        score = 9
    else:
        score = 10

    # Verificar parágrafos longos
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    long_paragraphs = [p for p in paragraphs if len(p.split()) > 80]
    if long_paragraphs:
        issues.append(
            f"{len(long_paragraphs)} parágrafo(s) muito longo(s) — quebre em partes menores"
        )
        score -= 2

    return max(0, min(10, score)), issues


def check_format_compliance(content: str, content_type: str) -> Tuple[int, List[str]]:
    """Verifica conformidade com formato."""
    issues = []
    score = 10

    word_count = len(content.split())
    char_count = len(content)

    if content_type == "post":
        if char_count > 2200:
            issues.append(
                f"Conteúdo excede limite do Instagram ({char_count}/2200 caracteres)"
            )
            score -= 3

    elif content_type == "artigo":
        if word_count < 800:
            issues.append(f"Artigo curto demais ({word_count} palavras, mínimo: 800)")
            score -= 3
        # Verificar headers
        headers = re.findall(r"^#{1,3}\s", content, re.MULTILINE)
        if len(headers) < 3:
            issues.append(
                f"Poucos headers ({len(headers)}) — artigos devem ter estrutura clara"
            )
            score -= 2

    elif content_type == "email":
        lines = content.strip().split("\n")
        if lines:
            subject_line = lines[0]
            if len(subject_line) > 50:
                issues.append(
                    f"Subject line muito longa ({len(subject_line)}/50 caracteres)"
                )
                score -= 2

    elif content_type == "landing-page":
        # Verificar seções essenciais
        essential = ["headline", "benefício", "cta", "prova social", "garantia", "faq"]
        content_lower = content.lower()
        missing = [s for s in essential if s not in content_lower]
        if missing:
            issues.append(f"Seções potencialmente ausentes: {', '.join(missing)}")
            score -= len(missing)

    elif content_type == "anuncio":
        if word_count > 150:
            issues.append(f"Anúncio muito longo ({word_count} palavras)")
            score -= 3

    return max(0, score), issues


def check_hashtags(content: str) -> Tuple[int, List[str]]:
    """Verifica hashtags."""
    hashtags = re.findall(r"#\w+", content)
    issues = []
    score = 10

    if not hashtags:
        return 5, [
            "Nenhuma hashtag encontrada (pode não ser necessário dependendo do formato)"
        ]

    if len(hashtags) > 30:
        issues.append(f"Muitas hashtags ({len(hashtags)}) — máximo recomendado: 15")
        score -= 3
    elif len(hashtags) > 15:
        issues.append(f"Hashtags acima do ideal ({len(hashtags)}) — ideal: 10-15")
        score -= 1

    # Verificar hashtags genéricas demais
    generic = ["#love", "#instagood", "#photooftheday", "#beautiful", "#happy"]
    found_generic = [h for h in hashtags if h.lower() in generic]
    if found_generic:
        issues.append(f"Hashtags genéricas demais: {', '.join(found_generic)}")
        score -= 2

    return max(0, score), issues


def generate_report(filepath: str, content_type: str):
    """Gera relatório completo de qualidade."""
    content = read_content(filepath)

    print("\n" + "=" * 60)
    print("🔍 QUALITY GATE — RELATÓRIO DE QUALIDADE")
    print("=" * 60)
    print(f"\n📄 Arquivo: {filepath}")
    print(f"📝 Tipo: {content_type}")
    print(
        f"📏 {len(content.split())} palavras | {len(content)} caracteres | {len(content.splitlines())} linhas"
    )

    # Executar todas as verificações
    checks = {}

    # 1. Acentuação
    accent_score, accent_issues = check_accents(content)
    checks["Acentuação"] = (accent_score, accent_issues, 10)

    # 2. Hook
    hook_score, hook_text, hook_issues = check_hook(content)
    checks["Hook/Abertura"] = (hook_score, hook_issues, 10)

    # 3. CTA
    cta_score, cta_issues = check_cta(content)
    checks["CTA"] = (cta_score, cta_issues, 10)

    # 4. Legibilidade
    read_score, read_issues = check_readability(content)
    checks["Legibilidade"] = (read_score, read_issues, 10)

    # 5. Formato
    format_score, format_issues = check_format_compliance(content, content_type)
    checks["Formato"] = (format_score, format_issues, 10)

    # 6. Hashtags (só para posts)
    if content_type in ["post", "social"]:
        hash_score, hash_issues = check_hashtags(content)
        checks["Hashtags"] = (hash_score, hash_issues, 10)

    # 7. Vícios de IA (regras obrigatórias do Marketing OS)
    ai_score, ai_issues = check_ai_tells(content)
    checks["Vícios de IA"] = (ai_score, ai_issues, 10)

    # Calcular score total
    total_score = sum(score for score, _, _ in checks.values())
    max_score = sum(max_s for _, _, max_s in checks.values())
    normalized_score = int((total_score / max_score) * 100) if max_score > 0 else 0

    # Vício de IA quebra regra obrigatória: nunca aprovar automaticamente
    capped_by_ai_tells = bool(ai_issues) and normalized_score > 60
    if capped_by_ai_tells:
        normalized_score = 60

    # Classificação
    if normalized_score >= 90:
        classification = "🏆 Excelente — Publicar imediatamente"
    elif normalized_score >= 75:
        classification = "✅ Bom — Publicar com ajustes menores"
    elif normalized_score >= 60:
        classification = "⚠️ Regular — Revisar antes de publicar"
    elif normalized_score >= 40:
        classification = "❌ Fraco — Reescrever seções críticas"
    else:
        classification = "🚫 Reprovado — Refazer completamente"

    print(f"\n🎯 SCORE TOTAL: {normalized_score}/100")
    print(f"   {classification}")
    if capped_by_ai_tells:
        print(
            "   (score limitado a 60: vício de IA é regra obrigatória do Marketing OS)"
        )

    # Detalhamento
    print("\n📊 DETALHAMENTO:")
    print("-" * 40)
    for name, (score, issues, max_s) in checks.items():
        status = (
            "✅" if score >= max_s * 0.7 else "⚠️" if score >= max_s * 0.4 else "❌"
        )
        print(f"   {status} {name}: {score}/{max_s}")

    # Hook encontrado
    if hook_text:
        print(f"\n🎣 HOOK DETECTADO:")
        print(f"   \"{hook_text[:100]}{'...' if len(hook_text) > 100 else ''}\"")

    # Problemas encontrados
    all_issues = []
    for name, (_, issues, _) in checks.items():
        for issue in issues:
            all_issues.append(f"[{name}] {issue}")

    if all_issues:
        print(f"\n⚠️ PROBLEMAS ENCONTRADOS ({len(all_issues)}):")
        for i, issue in enumerate(all_issues, 1):
            print(f"   {i}. {issue}")

    # Sugestões
    print(f"\n💡 RECOMENDAÇÕES:")
    if normalized_score >= 90:
        print("   ✅ Conteúdo aprovado! Pronto para publicação.")
    else:
        if accent_score < 8:
            print("   • Corrigir acentuação — regra obrigatória do Marketing OS")
        if ai_score < 10:
            print(
                "   • Eliminar vícios de IA (travessão, 'brutal', antítese) — regra obrigatória"
            )
        if hook_score < 7:
            print(
                "   • Fortalecer o hook — usar padrões: número, pergunta, 'Como...', curiosidade"
            )
        if cta_score < 7:
            print(
                "   • Melhorar CTA — usar verbos de ação: 'Quero', 'Garanta', 'Comece'"
            )
        if read_score < 7:
            print("   • Melhorar legibilidade — frases mais curtas, parágrafos menores")

    # Veredicto
    print("\n" + "=" * 60)
    if normalized_score >= 75:
        print("✅ VEREDICTO: APROVADO")
    else:
        print("❌ VEREDICTO: REVISÃO NECESSÁRIA")
    print("=" * 60)

    return normalized_score


def main():
    parser = argparse.ArgumentParser(
        description="Valida qualidade de conteúdo do Marketing OS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python quality_gate.py post.md --type post
  python quality_gate.py artigo.md --type artigo
  python quality_gate.py email.md --type email
  python quality_gate.py landing.md --type landing-page
  python quality_gate.py anuncio.md --type anuncio
        """,
    )

    parser.add_argument("file", help="Arquivo de conteúdo para validar")
    parser.add_argument(
        "--type",
        "-t",
        required=True,
        choices=[
            "post",
            "artigo",
            "email",
            "landing-page",
            "anuncio",
            "video",
            "social",
        ],
        help="Tipo do conteúdo",
    )

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"\n❌ Arquivo não encontrado: {args.file}")
        sys.exit(1)

    score = generate_report(args.file, args.type)
    sys.exit(0 if score >= 75 else 1)


if __name__ == "__main__":
    main()
