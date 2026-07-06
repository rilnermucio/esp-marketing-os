#!/usr/bin/env python3
"""
Hook Generator - Gera hooks virais para vídeos e posts
Baseado em padrões de conteúdo viral comprovados.

Uso:
    python hook_generator.py "tema" [plataforma] [quantidade]
    python hook_generator.py "produtividade com IA" reels 10
    python hook_generator.py "marketing digital" tiktok
"""

import sys
import json
import random
from typing import List, Dict

from validators import (
    ValidationError,
    validar_texto,
    validar_inteiro,
    validar_plataforma,
    handle_validation_error,
)

# Estruturas de hooks virais por categoria
HOOK_TEMPLATES = {
    "curiosidade": [
        "Você não vai acreditar no que descobri sobre {tema}",
        "O que ninguém te conta sobre {tema}",
        "Isso mudou TUDO que eu sabia sobre {tema}",
        "Por que {tema} não funciona (e o que funciona)",
        "O segredo por trás de {tema} que poucos conhecem",
        "Descobri isso sobre {tema} e fiquei em choque",
        "A verdade sobre {tema} que vão tentar esconder de você",
        "Isso sobre {tema} deveria ser ilegal",
    ],
    "controversia": [
        "{tema} é uma mentira. Deixa eu explicar.",
        "Pare de fazer isso com {tema}. Agora.",
        "Todo mundo está errado sobre {tema}",
        "Vou te provar que {tema} não funciona assim",
        "A maior mentira sobre {tema}",
        "Por que eu ODEIO a maioria dos conselhos sobre {tema}",
        "Unpopular opinion sobre {tema}",
        "Isso sobre {tema} vai irritar muita gente, mas...",
    ],
    "numero": [
        "3 coisas sobre {tema} que mudaram minha vida",
        "5 erros de {tema} que você comete todo dia",
        "7 dicas de {tema} em 60 segundos",
        "Os 3 pilares de {tema} que ninguém ensina",
        "10 segundos para entender {tema}",
        "1 hack de {tema} que vale por 100",
        "A regra 80/20 de {tema}",
        "Os 5% que dominam {tema} fazem isso diferente",
    ],
    "historia": [
        "Eu perdi tudo por causa de {tema}. Eis o que aprendi.",
        "Como {tema} destruiu minha carreira (e como me recuperei)",
        "De zero a expert em {tema}: minha jornada",
        "O dia que {tema} mudou minha vida",
        "Eu estava errado sobre {tema} por 5 anos",
        "A história que ninguém conta sobre {tema}",
        "Como um erro de {tema} me custou R$10.000",
        "O que aconteceu quando comecei a levar {tema} a sério",
    ],
    "urgencia": [
        "Se você não sabe isso sobre {tema}, está perdendo dinheiro",
        "PARE tudo e veja isso sobre {tema}",
        "Você TEM que ver isso sobre {tema} antes que seja tarde",
        "Última chance de entender {tema}",
        "Se você trabalha com {tema}, presta atenção",
        "Isso sobre {tema} vai mudar em 2025. Se prepare.",
        "O que ninguém está te contando sobre {tema}",
        "Urgente: isso sobre {tema} vai impactar sua vida",
    ],
    "identificacao": [
        "Se você luta com {tema}, isso é pra você",
        "Só quem trabalha com {tema} vai entender isso",
        "Você também passa por isso com {tema}?",
        "POV: você finalmente entendeu {tema}",
        "Todo mundo que trabalha com {tema} precisa ver isso",
        "Se você é iniciante em {tema}, salva esse vídeo",
        "Isso é para quem está cansado de errar em {tema}",
        "Só assiste se você quer dominar {tema}",
    ],
    "promessa": [
        "Como dominar {tema} em 30 dias",
        "O método que me fez expert em {tema}",
        "Aprenda {tema} em 5 minutos (sério)",
        "O único vídeo sobre {tema} que você precisa",
        "Depois disso, você nunca mais vai errar em {tema}",
        "O guia definitivo de {tema}",
        "Tudo que você precisa saber sobre {tema}",
        "O framework de {tema} que funciona 100%",
    ],
    "prova_social": [
        "Por que as maiores empresas usam {tema}",
        "O que os top 1% fazem diferente em {tema}",
        "Como experts usam {tema} (e você deveria também)",
        "O segredo de quem domina {tema}",
        "Isso é o que separa amadores de profissionais em {tema}",
        "O que bilionários sabem sobre {tema}",
        "Como as pessoas mais bem-sucedidas usam {tema}",
        "O padrão que encontrei em quem domina {tema}",
    ],
}

# Emojis por categoria
EMOJIS = {
    "curiosidade": ["🤯", "😱", "👀", "🔥", "💡"],
    "controversia": ["⚠️", "🚨", "❌", "😤", "💢"],
    "numero": ["📊", "✅", "📌", "🎯", "💯"],
    "historia": ["📖", "💔", "🔄", "✨", "🎬"],
    "urgencia": ["🚨", "⏰", "🔴", "⚡", "📢"],
    "identificacao": ["🙋", "💪", "🤝", "👆", "✋"],
    "promessa": ["🚀", "💎", "🏆", "⭐", "🎯"],
    "prova_social": ["👑", "💼", "📈", "🏅", "💰"],
}

# Adaptações por plataforma
PLATFORM_SPECS = {
    "reels": {
        "max_chars": 50,
        "style": "direto, impactante, visual",
        "emoji_position": "início",
        "tip": "Precisa parar o scroll em 0.5s",
    },
    "tiktok": {
        "max_chars": 60,
        "style": "casual, trend, relatável",
        "emoji_position": "início ou fim",
        "tip": "Use linguagem de internet, seja autêntico",
    },
    "youtube": {
        "max_chars": 80,
        "style": "claro, intrigante, promessa",
        "emoji_position": "opcional",
        "tip": "Precisa criar curiosidade para o vídeo inteiro",
    },
    "shorts": {
        "max_chars": 50,
        "style": "rápido, direto, hook visual",
        "emoji_position": "início",
        "tip": "Similar ao Reels, foco em retenção",
    },
    "linkedin": {
        "max_chars": 100,
        "style": "profissional, insight, valor",
        "emoji_position": "moderado",
        "tip": "Tom mais sério, foco em aprendizado",
    },
    "twitter": {
        "max_chars": 80,
        "style": "provocativo, opinião, thread-starter",
        "emoji_position": "opcional",
        "tip": "Deve gerar engajamento e discussão",
    },
}


def generate_hooks(tema: str, plataforma: str = "reels", quantidade: int = 10) -> Dict:
    """Gera hooks virais para o tema especificado."""

    hooks: List[Dict] = []
    categorias_usadas: List[str] = []

    # Gerar hooks de diferentes categorias
    all_categories = list(HOOK_TEMPLATES.keys())
    random.shuffle(all_categories)

    for i in range(quantidade):
        categoria = all_categories[i % len(all_categories)]
        templates = HOOK_TEMPLATES[categoria]
        template = random.choice(templates)

        hook_text = template.format(tema=tema)
        emoji = random.choice(EMOJIS[categoria])

        # Aplicar estilo da plataforma
        specs = PLATFORM_SPECS.get(plataforma, PLATFORM_SPECS["reels"])

        if specs["emoji_position"] == "início":
            formatted_hook = f"{emoji} {hook_text}"
        elif specs["emoji_position"] == "fim":
            formatted_hook = f"{hook_text} {emoji}"
        else:
            formatted_hook = hook_text

        hooks.append(
            {
                "hook": formatted_hook,
                "categoria": categoria,
                "emoji": emoji,
                "chars": len(formatted_hook),
            }
        )
        categorias_usadas.append(categoria)

    return {
        "tema": tema,
        "plataforma": plataforma,
        "specs": PLATFORM_SPECS.get(plataforma, PLATFORM_SPECS["reels"]),
        "hooks": hooks,
        "categorias_usadas": list(set(categorias_usadas)),
        "total_gerado": len(hooks),
    }


def print_results(results: Dict) -> None:
    """Imprime os resultados formatados."""

    print("=" * 70)
    print(f"🎣 HOOK GENERATOR: {results['tema'].upper()}")
    print("=" * 70)
    print()
    print(f"📱 Plataforma: {results['plataforma'].upper()}")
    print(f"📏 Limite recomendado: {results['specs']['max_chars']} caracteres")
    print(f"💡 Dica: {results['specs']['tip']}")
    print()
    print("-" * 70)
    print("🔥 HOOKS GERADOS:")
    print("-" * 70)
    print()

    for i, hook_data in enumerate(results["hooks"], 1):
        status = "✅" if hook_data["chars"] <= results["specs"]["max_chars"] else "⚠️"
        print(f"   [{i}] {hook_data['hook']}")
        print(
            f"       {status} {hook_data['chars']} chars | Categoria: {hook_data['categoria']}"
        )
        print()

    print("-" * 70)
    print("📊 CATEGORIAS UTILIZADAS:")
    for cat in results["categorias_usadas"]:
        print(f"   • {cat.title()}")
    print()

    print("💡 DICAS DE USO:")
    print("   • Teste diferentes hooks para ver qual performa melhor")
    print("   • Adapte o tom para sua audiência")
    print("   • Use texto na tela nos primeiros segundos")
    print("   • O hook deve criar um 'loop aberto' de curiosidade")
    print("   • Combine com um visual impactante")
    print()
    print("=" * 70)


USO = (
    'Uso: python hook_generator.py "tema" [plataforma] [quantidade]\n'
    "Plataformas: reels, tiktok, youtube, shorts, linkedin, twitter\n"
    'Exemplo: python hook_generator.py "produtividade" reels 10'
)


def main() -> None:
    if len(sys.argv) < 2:
        print(USO)
        sys.exit(1)

    try:
        tema = validar_texto(sys.argv[1], campo="tema", max_len=200)
        plataforma = (
            validar_plataforma(sys.argv[2], campo="plataforma")
            if len(sys.argv) > 2
            else "reels"
        )
        quantidade = (
            validar_inteiro(sys.argv[3], campo="quantidade", min_val=1, max_val=50)
            if len(sys.argv) > 3
            else 10
        )
    except ValidationError as e:
        handle_validation_error(e, mostrar_uso=USO)
        return

    if plataforma not in PLATFORM_SPECS:
        plataforma = "reels"

    results = generate_hooks(tema, plataforma, quantidade)
    print_results(results)

    # Output JSON
    print()
    print("📄 JSON Output:")
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
