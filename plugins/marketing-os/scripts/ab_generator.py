#!/usr/bin/env python3
"""
A/B Copy Generator
Gera variações de copy para testes A/B.
"""

import json
import sys
import re
from typing import Dict, List, Optional

# Templates de variação por elemento
VARIATION_TEMPLATES = {
    "headline": {
        "question": "E se você pudesse {benefit}?",
        "how_to": "Como {action} em {time}",
        "number": "{number} {subject} que {action}",
        "secret": "O segredo para {benefit} que ninguém conta",
        "mistake": "O erro que está te impedindo de {benefit}",
        "challenge": "Desafio: {action} em {time}",
        "proof": "{result} em {time}: como eu consegui",
        "direct": "{benefit}. Simples assim.",
    },
    "cta": {
        "urgency": ["Garanta agora", "Última chance", "Só hoje", "Vagas limitadas"],
        "benefit": [
            "Quero resultados",
            "Quero aprender",
            "Sim, eu quero",
            "Me inscrever",
        ],
        "curiosity": ["Descobrir como", "Ver mais", "Saiba mais", "Revelar segredo"],
        "free": ["Acesso gratuito", "Testar grátis", "Baixar grátis", "Começar grátis"],
        "social": ["Fazer parte", "Entrar no grupo", "Juntar-se a nós", "Participar"],
    },
    "hook": {
        "story": "Há {time} atrás, eu estava exatamente onde você está agora...",
        "question": "Você já se perguntou por que {problem}?",
        "statistic": "{percentage}% das pessoas {problem}. E você?",
        "bold_claim": "Isso vai mudar a forma como você {action}.",
        "contrarian": "Tudo que te disseram sobre {topic} está errado.",
        "empathy": "Eu sei como é frustrante {problem}...",
    },
}


def generate_variations(
    original: str, element_type: str = "headline", context: Optional[Dict] = None
) -> Dict:
    """Gera variações de copy para teste A/B."""

    if context is None:
        context = {
            "benefit": "[benefício]",
            "action": "[ação]",
            "time": "[tempo]",
            "number": "[número]",
            "subject": "[assunto]",
            "result": "[resultado]",
            "problem": "[problema]",
            "topic": "[tópico]",
            "percentage": "[%]",
        }

    variations: List[Dict] = []
    templates = VARIATION_TEMPLATES.get(element_type, {})

    if element_type == "headline":
        for style, template in templates.items():
            variation = template
            for key, value in context.items():
                variation = variation.replace("{" + key + "}", str(value))
            variations.append(
                {"style": style, "text": variation, "psychology": get_psychology(style)}
            )

    elif element_type == "cta":
        for category, options in templates.items():
            for option in options:
                variations.append(
                    {
                        "category": category,
                        "text": option,
                        "psychology": get_cta_psychology(category),
                    }
                )

    elif element_type == "hook":
        for style, template in templates.items():
            variation = template
            for key, value in context.items():
                variation = variation.replace("{" + key + "}", str(value))
            variations.append(
                {
                    "style": style,
                    "text": variation,
                    "psychology": get_hook_psychology(style),
                }
            )

    # Análise do original
    original_analysis = analyze_copy(original)

    return {
        "original": {
            "text": original,
            "analysis": original_analysis,
        },
        "variations": variations,
        "element_type": element_type,
        "testing_tips": [
            "Teste apenas 1 elemento por vez para resultados claros",
            "Mantenha o teste por pelo menos 7 dias ou 1000 impressões",
            "Use a mesma audiência para ambas variações",
            "Documente hipóteses antes de iniciar o teste",
            "Significância estatística > 95% antes de declarar vencedor",
        ],
        "recommended_tests": get_recommended_tests(element_type),
    }


def analyze_copy(text: str) -> Dict:
    """Analisa características do copy."""
    words = text.split()

    # Detectar técnicas usadas
    techniques: List[str] = []

    if "?" in text:
        techniques.append("question")
    if any(char.isdigit() for char in text):
        techniques.append("numbers")
    if any(word in text.lower() for word in ["você", "seu", "sua"]):
        techniques.append("personalization")
    if any(word in text.lower() for word in ["agora", "hoje", "última", "urgente"]):
        techniques.append("urgency")
    if any(word in text.lower() for word in ["grátis", "gratuito", "free", "bônus"]):
        techniques.append("value")
    if any(word in text.lower() for word in ["segredo", "revelado", "descobrir"]):
        techniques.append("curiosity")

    return {
        "word_count": len(words),
        "char_count": len(text),
        "techniques_detected": techniques,
        "has_emoji": bool(
            re.search(
                r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]",
                text,
            )
        ),
        "has_caps": any(word.isupper() and len(word) > 1 for word in words),
    }


def get_psychology(style: str) -> str:
    """Retorna explicação psicológica do estilo."""
    explanations = {
        "question": "Gatilho de curiosidade - o cérebro busca completar a resposta",
        "how_to": "Promessa de solução prática - alta intenção de busca",
        "number": "Especificidade gera credibilidade e expectativa clara",
        "secret": "Exclusividade e curiosidade - medo de perder informação",
        "mistake": "Aversão à perda - evitar erros é mais motivador que ganhar",
        "challenge": "Gamificação e senso de conquista",
        "proof": "Social proof através de resultado pessoal",
        "direct": "Simplicidade e clareza - corta objeções",
    }
    return explanations.get(style, "N/A")


def get_cta_psychology(category: str) -> str:
    """Retorna explicação psicológica do CTA."""
    explanations = {
        "urgency": "FOMO (Fear of Missing Out) e escassez",
        "benefit": "Foco no resultado desejado pelo usuário",
        "curiosity": "Loop aberto que demanda fechamento",
        "free": "Reduz fricção e risco percebido",
        "social": "Necessidade de pertencimento e comunidade",
    }
    return explanations.get(category, "N/A")


def get_hook_psychology(style: str) -> str:
    """Retorna explicação psicológica do hook."""
    explanations = {
        "story": "Identificação e jornada do herói",
        "question": "Ativa pensamento e reflexão pessoal",
        "statistic": "Autoridade e validação social",
        "bold_claim": "Promessa de transformação",
        "contrarian": "Desafia crenças e gera curiosidade",
        "empathy": "Conexão emocional e validação",
    }
    return explanations.get(style, "N/A")


def get_recommended_tests(element_type: str) -> List[str]:
    """Retorna testes recomendados por tipo."""
    tests: Dict[str, List[str]] = {
        "headline": [
            "Pergunta vs Afirmação",
            "Com número vs Sem número",
            "Benefício vs Dor",
            "Curto vs Longo",
            "Formal vs Informal",
        ],
        "cta": [
            "Urgência vs Benefício",
            "Primeira pessoa vs Segunda pessoa",
            "Verbo de ação vs Substantivo",
            "Com emoji vs Sem emoji",
            "Cor do botão (se aplicável)",
        ],
        "hook": [
            "História vs Estatística",
            "Pergunta vs Afirmação",
            "Emocional vs Racional",
            "Curto vs Detalhado",
        ],
    }
    return tests.get(element_type, [])


def main() -> None:
    if len(sys.argv) < 3:
        print("Uso: python ab_generator.py <tipo> <texto_original> [contexto_json]")
        print("Tipos: headline, cta, hook")
        print("\nExemplo:")
        print('  python ab_generator.py headline "Aprenda marketing digital"')
        print(
            '  python ab_generator.py headline "..." \'{"benefit":"dobrar suas vendas","time":"30 dias"}\''
        )
        sys.exit(1)

    element_type = sys.argv[1]
    original = sys.argv[2]
    context = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None

    result = generate_variations(original, element_type, context)

    print("\n" + "=" * 70)
    print(f"🔬 VARIAÇÕES A/B: {element_type.upper()}")
    print("=" * 70)

    print(f"\n📝 ORIGINAL:")
    print(f"   \"{result['original']['text']}\"")
    print(f"   Palavras: {result['original']['analysis']['word_count']}")
    print(
        f"   Técnicas: {', '.join(result['original']['analysis']['techniques_detected']) or 'Nenhuma detectada'}"
    )

    print(f"\n🎯 VARIAÇÕES GERADAS:")
    for i, var in enumerate(result["variations"], 1):
        style_or_cat = var.get("style") or var.get("category")
        print(f"\n   [{i}] {style_or_cat.upper()}")
        print(f"       \"{var['text']}\"")
        print(f"       💡 {var['psychology']}")

    print(f"\n📊 TESTES RECOMENDADOS:")
    for test in result["recommended_tests"]:
        print(f"   • {test}")

    print(f"\n💡 DICAS DE TESTE:")
    for tip in result["testing_tips"]:
        print(f"   • {tip}")

    print("\n" + "=" * 70)
    print("\n📄 JSON Output:")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
