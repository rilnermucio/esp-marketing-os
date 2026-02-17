#!/usr/bin/env python3
"""
SEO Content Analyzer
Analisa conteúdo e gera relatório de otimização SEO.
"""

import json
import re
import sys
from collections import Counter
from typing import Dict, List, Optional

from validators import ValidationError, validar_arquivo, validar_texto, handle_validation_error

def analyze_content(content: str, keyword: Optional[str] = None) -> Dict:
    """Analisa conteúdo para SEO."""

    # Métricas básicas
    words = content.split()
    word_count = len(words)
    sentences = re.split(r'[.!?]+', content)
    sentence_count = len([s for s in sentences if s.strip()])
    paragraphs = content.split('\n\n')
    paragraph_count = len([p for p in paragraphs if p.strip()])

    # Análise de legibilidade
    avg_sentence_length = word_count / max(sentence_count, 1)
    avg_word_length = sum(len(w) for w in words) / max(word_count, 1)

    # Headers (H1-H6)
    headers: Dict[str, int] = {
        'h1': len(re.findall(r'^#\s', content, re.MULTILINE)),
        'h2': len(re.findall(r'^##\s', content, re.MULTILINE)),
        'h3': len(re.findall(r'^###\s', content, re.MULTILINE)),
    }

    # Links
    internal_links = len(re.findall(r'\[.*?\]\(/[^)]+\)', content))
    external_links = len(re.findall(r'\[.*?\]\(https?://[^)]+\)', content))

    # Keyword analysis
    keyword_analysis: Optional[Dict] = None
    if keyword:
        keyword_lower = keyword.lower()
        content_lower = content.lower()
        keyword_count = content_lower.count(keyword_lower)
        keyword_density = (keyword_count / max(word_count, 1)) * 100

        # Verificar posição da keyword
        first_100_words = ' '.join(words[:100]).lower()
        in_first_100 = keyword_lower in first_100_words

        # Verificar em headers
        in_h1 = bool(re.search(rf'^#\s.*{re.escape(keyword_lower)}', content.lower(), re.MULTILINE))
        in_h2 = bool(re.search(rf'^##\s.*{re.escape(keyword_lower)}', content.lower(), re.MULTILINE))

        keyword_analysis = {
            'keyword': keyword,
            'count': keyword_count,
            'density': round(keyword_density, 2),
            'in_first_100_words': in_first_100,
            'in_h1': in_h1,
            'in_h2': in_h2,
            'ideal_density_range': '1-2%',
            'status': 'good' if 1 <= keyword_density <= 2 else 'adjust'
        }

    # Score de legibilidade (simplificado)
    readability_score = 100 - (avg_sentence_length * 1.5) - (avg_word_length * 5)
    readability_score = max(0, min(100, readability_score))

    # Recomendações
    recommendations: List[str] = []

    if word_count < 300:
        recommendations.append("⚠️ Conteúdo curto (<300 palavras). Para SEO, considere expandir para 1000+ palavras.")
    elif word_count < 1000:
        recommendations.append("📝 Conteúdo médio. Para competir em SEO, considere expandir para 1500+ palavras.")
    else:
        recommendations.append("✅ Bom comprimento de conteúdo para SEO.")

    if headers['h1'] == 0:
        recommendations.append("⚠️ Adicione um H1 com a keyword principal.")
    elif headers['h1'] > 1:
        recommendations.append("⚠️ Apenas um H1 por página. Encontrados: " + str(headers['h1']))

    if headers['h2'] < 2:
        recommendations.append("📝 Adicione mais H2s para estruturar o conteúdo (recomendado: 3-5).")

    if avg_sentence_length > 25:
        recommendations.append("⚠️ Sentenças muito longas (média: {:.1f} palavras). Ideal: <20 palavras.".format(avg_sentence_length))

    if external_links == 0:
        recommendations.append("📝 Adicione links externos para fontes confiáveis (E-E-A-T).")

    if keyword_analysis:
        if keyword_analysis['density'] < 1:
            recommendations.append(f"⚠️ Densidade de keyword baixa ({keyword_analysis['density']}%). Aumente uso de '{keyword}'.")
        elif keyword_analysis['density'] > 2.5:
            recommendations.append(f"⚠️ Possível keyword stuffing ({keyword_analysis['density']}%). Reduza uso de '{keyword}'.")

        if not keyword_analysis['in_first_100_words']:
            recommendations.append(f"📝 Inclua '{keyword}' nas primeiras 100 palavras.")

        if not keyword_analysis['in_h1']:
            recommendations.append(f"⚠️ Keyword '{keyword}' não encontrada no H1.")

    return {
        'metrics': {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'paragraph_count': paragraph_count,
            'avg_sentence_length': round(avg_sentence_length, 1),
            'avg_word_length': round(avg_word_length, 1),
            'readability_score': round(readability_score, 1),
        },
        'structure': {
            'headers': headers,
            'internal_links': internal_links,
            'external_links': external_links,
        },
        'keyword_analysis': keyword_analysis,
        'recommendations': recommendations,
        'seo_score': calculate_seo_score(word_count, headers, keyword_analysis, external_links)
    }

def calculate_seo_score(
    word_count: int,
    headers: Dict[str, int],
    keyword_analysis: Optional[Dict],
    external_links: int
) -> int:
    """Calcula score SEO de 0-100."""
    score = 0

    # Word count (30 pontos)
    if word_count >= 1500:
        score += 30
    elif word_count >= 1000:
        score += 25
    elif word_count >= 500:
        score += 15
    else:
        score += 5

    # Headers (20 pontos)
    if headers['h1'] == 1:
        score += 10
    if headers['h2'] >= 2:
        score += 10

    # Keyword (30 pontos)
    if keyword_analysis:
        if keyword_analysis['in_h1']:
            score += 10
        if keyword_analysis['in_first_100_words']:
            score += 10
        if 1 <= keyword_analysis['density'] <= 2:
            score += 10
    else:
        score += 15  # Sem keyword para analisar

    # Links (20 pontos)
    if external_links >= 2:
        score += 20
    elif external_links >= 1:
        score += 10

    return score

USO = (
    "Uso: python seo_analyzer.py <arquivo.md> [keyword]\n"
    "Exemplo: python seo_analyzer.py artigo.md 'marketing digital'"
)


def main() -> None:
    if len(sys.argv) < 2:
        print(USO)
        sys.exit(1)

    try:
        filepath = validar_arquivo(sys.argv[1], extensoes=[".md", ".txt"], campo="arquivo")
        keyword = None
        if len(sys.argv) > 2:
            keyword = validar_texto(sys.argv[2], campo="keyword", max_len=100)
    except ValidationError as e:
        handle_validation_error(e, mostrar_uso=USO)
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    result = analyze_content(content, keyword)

    print("\n" + "="*60)
    print("📊 RELATÓRIO DE ANÁLISE SEO")
    print("="*60)

    print(f"\n📈 SEO SCORE: {result['seo_score']}/100")

    print("\n📝 MÉTRICAS DE CONTEÚDO:")
    for key, value in result['metrics'].items():
        print(f"   • {key}: {value}")

    print("\n🏗️ ESTRUTURA:")
    print(f"   • Headers: H1={result['structure']['headers']['h1']}, H2={result['structure']['headers']['h2']}, H3={result['structure']['headers']['h3']}")
    print(f"   • Links internos: {result['structure']['internal_links']}")
    print(f"   • Links externos: {result['structure']['external_links']}")

    if result['keyword_analysis']:
        print(f"\n🔍 ANÁLISE DE KEYWORD: '{result['keyword_analysis']['keyword']}'")
        print(f"   • Ocorrências: {result['keyword_analysis']['count']}")
        print(f"   • Densidade: {result['keyword_analysis']['density']}% (ideal: 1-2%)")
        print(f"   • No H1: {'✅' if result['keyword_analysis']['in_h1'] else '❌'}")
        print(f"   • Nas primeiras 100 palavras: {'✅' if result['keyword_analysis']['in_first_100_words'] else '❌'}")

    print("\n💡 RECOMENDAÇÕES:")
    for rec in result['recommendations']:
        print(f"   {rec}")

    print("\n" + "="*60)

    # Output JSON para integração
    print("\n📄 JSON Output:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
