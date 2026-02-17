#!/usr/bin/env python3
"""
Hashtag Generator
Gera hashtags relevantes por nicho e plataforma.
"""

import json
import sys
from typing import List, Dict, Optional

from validators import ValidationError, validar_texto, validar_plataforma, handle_validation_error

# Base de hashtags por nicho
HASHTAG_DATABASE = {
    'marketing_digital': {
        'core': ['#marketingdigital', '#marketing', '#digitalmarketing', '#socialmedia', '#marketingonline'],
        'engagement': ['#dicasdemarketing', '#marketingtips', '#growthhacking', '#estrategia', '#negocios'],
        'trending': ['#empreendedorismo', '#sucesso', '#resultados', '#vendasonline', '#trafegopago'],
    },
    'empreendedorismo': {
        'core': ['#empreendedorismo', '#empreender', '#negocios', '#empresario', '#startup'],
        'engagement': ['#mindsetempreendedor', '#vidadeempreendedor', '#sucessonegocio', '#motivacao'],
        'trending': ['#liberdadefinanceira', '#rendaextra', '#trabalheemcasa', '#negocioproprio'],
    },
    'tecnologia': {
        'core': ['#tecnologia', '#tech', '#inovacao', '#digital', '#futuro'],
        'engagement': ['#ia', '#inteligenciaartificial', '#programacao', '#developer', '#codigo'],
        'trending': ['#chatgpt', '#ai', '#machinelearning', '#dados', '#transformacaodigital'],
    },
    'saude_bem_estar': {
        'core': ['#saude', '#bemestar', '#vidasaudavel', '#qualidadedevida', '#wellness'],
        'engagement': ['#fitness', '#treino', '#alimentacaosaudavel', '#mentalhealth', '#autocuidado'],
        'trending': ['#mindfulness', '#meditacao', '#yoga', '#healthylifestyle', '#selfcare'],
    },
    'financas': {
        'core': ['#financas', '#investimentos', '#dinheiro', '#financaspessoais', '#economia'],
        'engagement': ['#educacaofinanceira', '#rendapassiva', '#bolsadevalores', '#criptomoedas'],
        'trending': ['#bitcoin', '#fii', '#acoes', '#daytrader', '#independenciafinanceira'],
    },
    'moda_beleza': {
        'core': ['#moda', '#fashion', '#estilo', '#beleza', '#beauty'],
        'engagement': ['#lookdodia', '#ootd', '#tendencia', '#makeup', '#skincare'],
        'trending': ['#influencer', '#fashionista', '#streetstyle', '#glam', '#style'],
    },
    'gastronomia': {
        'core': ['#gastronomia', '#comida', '#food', '#foodie', '#culinaria'],
        'engagement': ['#receita', '#cozinha', '#chef', '#instafood', '#delicia'],
        'trending': ['#foodporn', '#homemade', '#receitafacil', '#comidasaudavel', '#gourmet'],
    },
    'educacao': {
        'core': ['#educacao', '#aprendizado', '#conhecimento', '#estudos', '#cursoonline'],
        'engagement': ['#dicasdeestudo', '#desenvolvimentopessoal', '#carreira', '#concurso'],
        'trending': ['#ead', '#mentoria', '#coaching', '#softskills', '#produtividade'],
    },
}

# Limites por plataforma
PLATFORM_LIMITS = {
    'instagram': {'max': 30, 'recommended': 10, 'note': 'Use 5-15 hashtags misturando popularidade'},
    'linkedin': {'max': 5, 'recommended': 3, 'note': 'Apenas hashtags profissionais e específicas'},
    'twitter': {'max': 2, 'recommended': 2, 'note': 'Apenas 1-2 hashtags relevantes'},
    'tiktok': {'max': 5, 'recommended': 4, 'note': 'Hashtags trending + nicho específico'},
    'facebook': {'max': 3, 'recommended': 2, 'note': 'Hashtags opcionais, foco no conteúdo'},
}

def get_hashtags(nicho: str, platform: str = 'instagram', custom_keywords: Optional[List[str]] = None) -> Dict:
    """Gera hashtags para um nicho e plataforma."""

    nicho_lower = nicho.lower().replace(' ', '_').replace('-', '_')

    # Buscar nicho na base
    if nicho_lower not in HASHTAG_DATABASE:
        available = list(HASHTAG_DATABASE.keys())
        return {
            'error': f"Nicho '{nicho}' não encontrado.",
            'available_niches': available,
            'suggestion': 'Use um dos nichos disponíveis ou adicione keywords customizadas.'
        }

    hashtags = HASHTAG_DATABASE[nicho_lower]
    platform_config = PLATFORM_LIMITS.get(platform.lower(), PLATFORM_LIMITS['instagram'])

    # Montar lista de hashtags
    all_hashtags: List[str] = []
    all_hashtags.extend(hashtags['core'][:3])  # Top 3 core
    all_hashtags.extend(hashtags['engagement'][:3])  # Top 3 engagement
    all_hashtags.extend(hashtags['trending'][:4])  # Top 4 trending

    # Adicionar keywords customizadas
    if custom_keywords:
        for kw in custom_keywords[:5]:
            formatted = '#' + kw.lower().replace(' ', '').replace('-', '')
            if formatted not in all_hashtags:
                all_hashtags.append(formatted)

    # Limitar pela plataforma
    recommended = all_hashtags[:platform_config['recommended']]
    extended = all_hashtags[:platform_config['max']]

    return {
        'nicho': nicho,
        'platform': platform,
        'recommended': {
            'hashtags': recommended,
            'count': len(recommended),
            'formatted': ' '.join(recommended)
        },
        'extended': {
            'hashtags': extended,
            'count': len(extended),
            'formatted': ' '.join(extended)
        },
        'all_available': {
            'core': hashtags['core'],
            'engagement': hashtags['engagement'],
            'trending': hashtags['trending']
        },
        'platform_tips': platform_config['note'],
        'best_practices': [
            'Misture hashtags populares com específicas',
            'Evite hashtags banidas ou spam',
            'Rotacione hashtags para evitar shadowban',
            'Use hashtags no idioma do seu público',
            'Monitore quais hashtags trazem mais engajamento'
        ]
    }

def _uso_hashtag() -> str:
    linhas = [
        "Uso: python hashtag_generator.py <nicho> [plataforma] [keywords...]",
        "Exemplo: python hashtag_generator.py marketing_digital instagram ia chatgpt",
        "\nNichos disponíveis:",
    ]
    for nicho in HASHTAG_DATABASE.keys():
        linhas.append(f"  • {nicho}")
    linhas.append("\nPlataformas: instagram, linkedin, twitter, tiktok, facebook")
    return "\n".join(linhas)


def main() -> None:
    if len(sys.argv) < 2:
        print(_uso_hashtag())
        sys.exit(1)

    try:
        nicho = validar_texto(sys.argv[1], campo="nicho", max_len=100)
        platform = validar_plataforma(sys.argv[2], campo="plataforma") if len(sys.argv) > 2 else "instagram"
        custom_keywords = [validar_texto(k, campo="keyword", max_len=50) for k in sys.argv[3:]] if len(sys.argv) > 3 else None
    except ValidationError as e:
        handle_validation_error(e, mostrar_uso=_uso_hashtag())
        return

    result = get_hashtags(nicho, platform, custom_keywords)

    if 'error' in result:
        print(f"\n❌ {result['error']}")
        print(f"Nichos disponíveis: {', '.join(result['available_niches'])}")
        sys.exit(1)

    print("\n" + "="*60)
    print(f"#️⃣ HASHTAGS: {nicho.upper()} | {platform.upper()}")
    print("="*60)

    print(f"\n✅ RECOMENDADAS ({result['recommended']['count']}):")
    print(f"   {result['recommended']['formatted']}")

    print(f"\n📝 EXTENDIDAS ({result['extended']['count']}):")
    print(f"   {result['extended']['formatted']}")

    print(f"\n💡 DICA PARA {platform.upper()}:")
    print(f"   {result['platform_tips']}")

    print("\n📋 CATEGORIAS DISPONÍVEIS:")
    print(f"   Core: {' '.join(result['all_available']['core'])}")
    print(f"   Engagement: {' '.join(result['all_available']['engagement'])}")
    print(f"   Trending: {' '.join(result['all_available']['trending'])}")

    print("\n🎯 BOAS PRÁTICAS:")
    for tip in result['best_practices']:
        print(f"   • {tip}")

    print("\n" + "="*60)
    print("\n📄 JSON Output:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
