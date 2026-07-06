#!/usr/bin/env python3
"""
Headline Scorer - Avalia headlines por poder emocional e clareza

Uso:
    python headline_scorer.py "Sua headline aqui"
    python headline_scorer.py --file headlines.txt
    python headline_scorer.py --compare "Headline A" "Headline B"
"""

import re
import sys
import argparse
from typing import Dict, List, Tuple

from output_formatter import add_output_args, OutputFormatter

# Palavras de poder por categoria
POWER_WORDS = {
    "urgencia": [
        "agora",
        "hoje",
        "imediato",
        "último",
        "limitado",
        "urgente",
        "rápido",
        "instantâneo",
        "deadline",
        "antes",
        "enquanto",
    ],
    "curiosidade": [
        "segredo",
        "revelado",
        "descobrir",
        "surpreendente",
        "chocante",
        "verdade",
        "mistério",
        "escondido",
        "nunca",
        "finalmente",
    ],
    "valor": [
        "grátis",
        "gratuito",
        "bônus",
        "exclusivo",
        "especial",
        "premium",
        "vip",
        "presente",
        "oferta",
        "desconto",
    ],
    "confianca": [
        "comprovado",
        "garantido",
        "científico",
        "testado",
        "validado",
        "certificado",
        "oficial",
        "autêntico",
        "aprovado",
        "seguro",
    ],
    "emocao": [
        "incrível",
        "fantástico",
        "extraordinário",
        "poderoso",
        "épico",
        "transformador",
        "revolucionário",
        "essencial",
        "definitivo",
        "máximo",
    ],
    "medo": [
        "erro",
        "perigo",
        "evite",
        "nunca",
        "problema",
        "risco",
        "armadilha",
        "falha",
        "cuidado",
        "alerta",
    ],
    "beneficio": [
        "como",
        "aprenda",
        "descubra",
        "conquiste",
        "alcance",
        "domine",
        "melhore",
        "aumente",
        "ganhe",
        "economize",
    ],
}

# Padrões de headline que funcionam
HEADLINE_PATTERNS = {
    "numero_lista": r"^\d+\s",  # "7 dicas..."
    "como_fazer": r"^como\s",  # "Como fazer..."
    "pergunta": r"\?$",  # Termina com ?
    "voce": r"\bvocê\b",  # Fala diretamente com leitor
    "este_esse": r"\b(este|esse|esta|essa)\b",  # Demonstrativo
    "por_que": r"^por\s?que",  # "Por que..."
    "guia": r"\b(guia|manual|passo.a.passo)\b",
    "segredo": r"\bsegredo",
    "erro": r"\berro",
    "novo": r"\b(novo|nova|novos|novas)\b",
}

# Penalidades
PENALTY_WORDS = [
    "talvez",
    "possivelmente",
    "provavelmente",
    "pode ser",
    "meio",
    "um pouco",
    "tipo",
    "sei lá",
]


def count_power_words(headline: str) -> Dict[str, List[str]]:
    """Conta palavras de poder por categoria."""
    headline_lower = headline.lower()
    found: Dict[str, List[str]] = {}

    for category, words in POWER_WORDS.items():
        matches = [w for w in words if w in headline_lower]
        if matches:
            found[category] = matches

    return found


def check_patterns(headline: str) -> List[str]:
    """Verifica padrões de headline que funcionam."""
    headline_lower = headline.lower()
    matched: List[str] = []

    for pattern_name, pattern in HEADLINE_PATTERNS.items():
        if re.search(pattern, headline_lower, re.IGNORECASE):
            matched.append(pattern_name)

    return matched


def check_penalties(headline: str) -> List[str]:
    """Verifica palavras que enfraquecem a headline."""
    headline_lower = headline.lower()
    return [w for w in PENALTY_WORDS if w in headline_lower]


def calculate_length_score(headline: str) -> Tuple[int, str]:
    """Avalia o comprimento da headline."""
    length = len(headline)
    word_count = len(headline.split())

    if 40 <= length <= 70 and 6 <= word_count <= 12:
        return 10, "✅ Comprimento ideal"
    elif 30 <= length <= 80 and 4 <= word_count <= 15:
        return 7, "⚠️ Comprimento aceitável"
    else:
        return 3, "❌ Comprimento fora do ideal"


def score_headline(headline: str) -> Dict:
    """Calcula a pontuação total da headline."""

    results: Dict = {
        "headline": headline,
        "scores": {},
        "power_words": {},
        "patterns": [],
        "penalties": [],
        "suggestions": [],
    }

    # 1. Palavras de poder (0-30 pontos)
    power_words = count_power_words(headline)
    results["power_words"] = power_words
    power_score = min(30, sum(len(words) * 5 for words in power_words.values()))
    results["scores"]["power_words"] = power_score

    # 2. Padrões (0-25 pontos)
    patterns = check_patterns(headline)
    results["patterns"] = patterns
    pattern_score = min(25, len(patterns) * 8)
    results["scores"]["patterns"] = pattern_score

    # 3. Comprimento (0-10 pontos)
    length_score, length_msg = calculate_length_score(headline)
    results["scores"]["length"] = length_score
    results["length_analysis"] = length_msg

    # 4. Especificidade (0-15 pontos)
    has_number = bool(re.search(r"\d", headline))
    has_timeframe = bool(
        re.search(r"\b(dias?|semanas?|meses?|horas?|minutos?)\b", headline.lower())
    )
    specificity_score = (has_number * 8) + (has_timeframe * 7)
    results["scores"]["specificity"] = specificity_score
    results["has_number"] = has_number
    results["has_timeframe"] = has_timeframe

    # 5. Penalidades (-5 por palavra fraca)
    penalties = check_penalties(headline)
    results["penalties"] = penalties
    penalty_score = len(penalties) * -5
    results["scores"]["penalties"] = penalty_score

    # 6. Clareza (0-20 pontos) - baseado em simplicidade
    avg_word_length = sum(len(w) for w in headline.split()) / max(
        len(headline.split()), 1
    )
    if avg_word_length <= 5:
        clarity_score = 20
    elif avg_word_length <= 7:
        clarity_score = 15
    elif avg_word_length <= 9:
        clarity_score = 10
    else:
        clarity_score = 5
    results["scores"]["clarity"] = clarity_score

    # Total
    total = sum(results["scores"].values())
    results["total_score"] = max(0, min(100, total))

    # Classificação
    if total >= 80:
        results["classification"] = "🏆 Excelente"
    elif total >= 60:
        results["classification"] = "✅ Boa"
    elif total >= 40:
        results["classification"] = "⚠️ Regular"
    else:
        results["classification"] = "❌ Fraca"

    # Sugestões de melhoria
    if not power_words:
        results["suggestions"].append(
            "Adicione palavras de poder (ex: 'comprovado', 'segredo', 'grátis')"
        )
    if not patterns:
        results["suggestions"].append(
            "Use um padrão eficaz (ex: comece com número, 'Como...', ou pergunta)"
        )
    if not has_number:
        results["suggestions"].append("Considere adicionar um número específico")
    if penalties:
        results["suggestions"].append(f"Remova palavras fracas: {', '.join(penalties)}")
    if length_score < 7:
        results["suggestions"].append(
            "Ajuste o comprimento (ideal: 6-12 palavras, 40-70 caracteres)"
        )

    return results


def print_report(results: Dict) -> None:
    """Imprime relatório formatado."""
    print("\n" + "=" * 60)
    print("📊 ANÁLISE DE HEADLINE")
    print("=" * 60)
    print(f"\n📝 \"{results['headline']}\"")
    print(
        f"\n🎯 PONTUAÇÃO TOTAL: {results['total_score']}/100 {results['classification']}"
    )

    print("\n📈 DETALHAMENTO:")
    print(f"   • Palavras de poder: {results['scores']['power_words']}/30")
    print(f"   • Padrões eficazes: {results['scores']['patterns']}/25")
    print(f"   • Clareza: {results['scores']['clarity']}/20")
    print(f"   • Especificidade: {results['scores']['specificity']}/15")
    print(f"   • Comprimento: {results['scores']['length']}/10")
    if results["scores"]["penalties"] < 0:
        print(f"   • Penalidades: {results['scores']['penalties']}")

    if results["power_words"]:
        print("\n💪 PALAVRAS DE PODER ENCONTRADAS:")
        for category, words in results["power_words"].items():
            print(f"   • {category.title()}: {', '.join(words)}")

    if results["patterns"]:
        print("\n✨ PADRÕES IDENTIFICADOS:")
        pattern_names = {
            "numero_lista": "Começa com número",
            "como_fazer": "Formato 'Como fazer'",
            "pergunta": "Formato pergunta",
            "voce": "Fala com 'você'",
            "este_esse": "Usa demonstrativo",
            "por_que": "Formato 'Por que'",
            "guia": "Menciona guia/passo-a-passo",
            "segredo": "Menciona segredo",
            "erro": "Menciona erro",
            "novo": "Menciona novidade",
        }
        for p in results["patterns"]:
            print(f"   • {pattern_names.get(p, p)}")

    if results["penalties"]:
        print("\n⚠️ PALAVRAS QUE ENFRAQUECEM:")
        print(f"   {', '.join(results['penalties'])}")

    if results["suggestions"]:
        print("\n💡 SUGESTÕES DE MELHORIA:")
        for i, suggestion in enumerate(results["suggestions"], 1):
            print(f"   {i}. {suggestion}")

    print("\n" + "=" * 60)


def compare_headlines(headlines: List[str]) -> None:
    """Compara múltiplas headlines."""
    results = [(h, score_headline(h)) for h in headlines]
    results.sort(key=lambda x: x[1]["total_score"], reverse=True)

    print("\n" + "=" * 60)
    print("🏆 COMPARATIVO DE HEADLINES")
    print("=" * 60)

    for i, (headline, result) in enumerate(results, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        print(f"\n{medal} [{result['total_score']}/100] \"{headline}\"")
        print(f"   {result['classification']}")

    print("\n" + "=" * 60)
    print(f'\n✅ VENCEDOR: "{results[0][0]}"')
    print("=" * 60)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analisa e pontua headlines")
    parser.add_argument("headline", nargs="*", help="Headline(s) para analisar")
    parser.add_argument("--file", "-f", help="Arquivo com headlines (uma por linha)")
    parser.add_argument("--compare", "-c", action="store_true", help="Modo comparação")
    add_output_args(parser)

    args = parser.parse_args()
    fmt = OutputFormatter(args)

    headlines: List[str] = []

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            headlines = [line.strip() for line in f if line.strip()]
    elif args.headline:
        headlines = [" ".join(args.headline)] if not args.compare else args.headline
    else:
        print('Uso: python headline_scorer.py "Sua headline aqui"')
        print('     python headline_scorer.py --compare "Headline A" "Headline B"')
        sys.exit(1)

    if len(headlines) > 1 or args.compare:
        data = [score_headline(h) for h in headlines]
        fmt.print(
            data, human_fn=lambda d: compare_headlines([h["headline"] for h in d])
        )
    else:
        result = score_headline(headlines[0])
        fmt.print(result, human_fn=lambda d: print_report(d))


if __name__ == "__main__":
    main()
