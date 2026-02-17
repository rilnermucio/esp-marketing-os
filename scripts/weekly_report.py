#!/usr/bin/env python3
"""
Weekly Report - Geração automática de relatório semanal de performance

Uso:
    python weekly_report.py                          # Relatório desta semana
    python weekly_report.py --week 2026-W07         # Semana específica
    python weekly_report.py --input dados.json      # Com dados de entrada
    python weekly_report.py --output relatorio.md   # Salvar em arquivo
    python weekly_report.py --format markdown        # Formato de saída
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# Diretório base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "reports")


# ──────────────────────────────────────────────
# Benchmarks de referência por plataforma
# ──────────────────────────────────────────────

BENCHMARKS = {
    "instagram": {
        "taxa_engajamento": 3.0,        # %
        "alcance_por_seguidor": 0.15,   # 15% dos seguidores
        "saves_rate": 1.0,              # % dos alcançados
        "shares_rate": 0.5,
    },
    "linkedin": {
        "taxa_engajamento": 2.0,
        "impressoes_por_seguidor": 0.3,
        "cliques_rate": 0.5,
    },
    "email": {
        "taxa_abertura": 25.0,          # %
        "taxa_clique": 3.0,
        "taxa_conversao": 1.0,
        "taxa_descadastro": 0.2,
    },
    "blog": {
        "tempo_leitura": 180,           # segundos
        "taxa_rejeicao": 60.0,          # %
        "paginas_por_sessao": 1.5,
    },
    "youtube": {
        "taxa_retencao": 40.0,          # %
        "ctr_thumbnail": 4.0,
        "likes_rate": 4.0,
    },
}

# Temas padrão por dia da semana para sugestão de calendário
CONTENT_THEMES_BY_DAY = {
    0: {"tema": "Segunda da Educação", "formatos": ["carrossel educativo", "artigo"]},
    1: {"tema": "Terça de Tendências", "formatos": ["post de tendência", "reels"]},
    2: {"tema": "Quarta de Cases", "formatos": ["caso de sucesso", "depoimento"]},
    3: {"tema": "Quinta de Ferramentas", "formatos": ["tutorial", "comparativo"]},
    4: {"tema": "Sexta de Motivação", "formatos": ["post motivacional", "bastidores"]},
    5: {"tema": "Sábado de Engajamento", "formatos": ["pergunta", "enquete", "quiz"]},
    6: {"tema": "Domingo de Reflexão", "formatos": ["conteúdo longo", "newsletter"]},
}


# ──────────────────────────────────────────────
# Utilitários de data
# ──────────────────────────────────────────────

def get_current_week() -> str:
    """Retorna a semana atual no formato ISO YYYY-Www."""
    now = datetime.now()
    iso_calendar = now.isocalendar()
    return f"{iso_calendar[0]}-W{iso_calendar[1]:02d}"


def get_week_dates(week_str: str) -> tuple:
    """Retorna as datas de início e fim de uma semana ISO."""
    match = re.match(r'^(\d{4})-W(\d{2})$', week_str)
    if not match:
        raise ValueError(f"Formato de semana inválido: '{week_str}'. Use YYYY-Www (ex: 2026-W07)")
    year = int(match.group(1))
    week = int(match.group(2))
    # Segunda-feira da semana ISO
    jan4 = datetime(year, 1, 4)
    start = jan4 + timedelta(weeks=week - jan4.isocalendar()[1], days=-jan4.isocalendar()[2] + 1)
    end = start + timedelta(days=6)
    return start, end


def parse_week_number(week_str: str) -> int:
    """Extrai o número da semana de uma string YYYY-Www."""
    match = re.match(r'^\d{4}-W(\d{2})$', week_str)
    if not match:
        raise ValueError(f"Formato inválido: {week_str}")
    return int(match.group(1))


# ──────────────────────────────────────────────
# Análise de dados de conteúdo
# ──────────────────────────────────────────────

def collect_content_metrics(content_list: List[Dict]) -> Dict:
    """
    Coleta e agrega métricas de uma lista de conteúdos.

    Cada item em content_list deve ter:
    {
        "titulo": str,
        "plataforma": str,
        "formato": str,
        "alcance": int,
        "engajamentos": int,
        "cliques": int (opcional),
        "saves": int (opcional),
        "shares": int (opcional),
        "data": str (ISO format)
    }
    """
    if not content_list:
        return {
            "total_pecas": 0,
            "alcance_total": 0,
            "engajamento_total": 0,
            "taxa_engajamento_media": 0.0,
            "top_conteudos": [],
            "bottom_conteudos": [],
            "por_plataforma": {},
            "por_formato": {},
        }

    total_alcance = sum(c.get("alcance", 0) for c in content_list)
    total_engajamentos = sum(c.get("engajamentos", 0) for c in content_list)

    # Taxa de engajamento média
    taxas = []
    for c in content_list:
        alcance = c.get("alcance", 0)
        eng = c.get("engajamentos", 0)
        if alcance > 0:
            taxas.append((eng / alcance) * 100)

    taxa_media = sum(taxas) / len(taxas) if taxas else 0.0

    # Ordenar por engajamento relativo
    def engajamento_relativo(c):
        alcance = c.get("alcance", 1)
        eng = c.get("engajamentos", 0)
        return eng / alcance if alcance > 0 else 0

    ordenados = sorted(content_list, key=engajamento_relativo, reverse=True)
    top = ordenados[:3]
    bottom = ordenados[-3:] if len(ordenados) >= 3 else ordenados

    # Agregação por plataforma
    por_plataforma: Dict[str, Dict] = {}
    for c in content_list:
        plataforma = c.get("plataforma", "desconhecido")
        if plataforma not in por_plataforma:
            por_plataforma[plataforma] = {"pecas": 0, "alcance": 0, "engajamentos": 0}
        por_plataforma[plataforma]["pecas"] += 1
        por_plataforma[plataforma]["alcance"] += c.get("alcance", 0)
        por_plataforma[plataforma]["engajamentos"] += c.get("engajamentos", 0)

    # Agregação por formato
    por_formato: Dict[str, int] = {}
    for c in content_list:
        fmt = c.get("formato", "desconhecido")
        por_formato[fmt] = por_formato.get(fmt, 0) + 1

    return {
        "total_pecas": len(content_list),
        "alcance_total": total_alcance,
        "engajamento_total": total_engajamentos,
        "taxa_engajamento_media": round(taxa_media, 2),
        "top_conteudos": top,
        "bottom_conteudos": bottom,
        "por_plataforma": por_plataforma,
        "por_formato": por_formato,
    }


def collect_seo_metrics(urls: List[Dict]) -> Dict:
    """
    Coleta e agrega métricas de SEO para uma lista de URLs.

    Cada item em urls deve ter:
    {
        "url": str,
        "titulo": str,
        "posicao_media": float,
        "impressoes": int,
        "cliques": int,
        "ctr": float
    }
    """
    if not urls:
        return {
            "total_urls": 0,
            "impressoes_total": 0,
            "cliques_total": 0,
            "ctr_medio": 0.0,
            "posicao_media_geral": 0.0,
            "quick_wins": [],
            "top_paginas": [],
        }

    impressoes_total = sum(u.get("impressoes", 0) for u in urls)
    cliques_total = sum(u.get("cliques", 0) for u in urls)
    ctr_medio = (cliques_total / impressoes_total * 100) if impressoes_total > 0 else 0.0

    posicoes = [u.get("posicao_media", 0) for u in urls if u.get("posicao_media", 0) > 0]
    posicao_media_geral = sum(posicoes) / len(posicoes) if posicoes else 0.0

    # Quick wins: posição entre 4-15 e CTR abaixo de 5%
    quick_wins = [
        u for u in urls
        if 4 <= u.get("posicao_media", 99) <= 15 and u.get("ctr", 99) < 5.0
    ]
    quick_wins.sort(key=lambda u: u.get("impressoes", 0), reverse=True)

    # Top páginas por cliques
    top_paginas = sorted(urls, key=lambda u: u.get("cliques", 0), reverse=True)[:5]

    return {
        "total_urls": len(urls),
        "impressoes_total": impressoes_total,
        "cliques_total": cliques_total,
        "ctr_medio": round(ctr_medio, 2),
        "posicao_media_geral": round(posicao_media_geral, 1),
        "quick_wins": quick_wins[:5],
        "top_paginas": top_paginas,
    }


def generate_next_week_recommendations(
    content_metrics: Dict,
    seo_metrics: Dict,
    email_metrics: Optional[Dict] = None,
) -> List[str]:
    """Gera recomendações para a próxima semana com base nas métricas."""
    recommendations = []

    # Análise de conteúdo
    taxa_eng = content_metrics.get("taxa_engajamento_media", 0)
    if taxa_eng < 2.0:
        recommendations.append(
            f"Taxa de engajamento baixa ({taxa_eng:.1f}%) — experimente hooks mais provocativos "
            "ou formatos de maior interação (enquetes, perguntas, carrosséis)"
        )
    elif taxa_eng > 5.0:
        recommendations.append(
            f"Taxa de engajamento excelente ({taxa_eng:.1f}%) — replique o estilo dos top conteúdos"
        )

    # Plataforma com melhor performance
    por_plat = content_metrics.get("por_plataforma", {})
    if por_plat:
        melhor = max(
            por_plat.items(),
            key=lambda x: (x[1].get("engajamentos", 0) / max(x[1].get("alcance", 1), 1))
        )
        recommendations.append(
            f"Melhor plataforma da semana: {melhor[0]} — considere aumentar frequência aqui"
        )

    # SEO quick wins
    quick_wins = seo_metrics.get("quick_wins", [])
    if quick_wins:
        pagina = quick_wins[0].get("titulo") or quick_wins[0].get("url", "página")
        recommendations.append(
            f"Quick win de SEO identificado: otimize o título/meta de '{pagina}' "
            f"(posição {quick_wins[0].get('posicao_media', '?'):.0f}, CTR baixo)"
        )

    # Email
    if email_metrics:
        abertura = email_metrics.get("taxa_abertura", 0)
        if abertura < 20:
            recommendations.append(
                f"Taxa de abertura de email baixa ({abertura:.1f}%) — teste novos assuntos "
                "com número, pergunta ou personalização"
            )

    # Produção
    total_pecas = content_metrics.get("total_pecas", 0)
    if total_pecas < 3:
        recommendations.append(
            f"Apenas {total_pecas} peça(s) publicada(s) esta semana — "
            "considere aumentar para 5-7 posts semanais para crescimento consistente"
        )

    # Default se não há recomendações
    if not recommendations:
        recommendations.append("Performance dentro do esperado — mantenha a consistência")

    return recommendations


def generate_suggested_calendar(week_str: str, platforms: List[str]) -> List[Dict]:
    """Gera sugestão de calendário para a próxima semana."""
    match = re.match(r'^(\d{4})-W(\d{2})$', week_str)
    if not match:
        return []

    year = int(match.group(1))
    week = int(match.group(2))

    # Semana seguinte
    next_week = week + 1
    next_year = year
    if next_week > 52:
        next_week = 1
        next_year += 1

    jan4 = datetime(next_year, 1, 4)
    start = jan4 + timedelta(
        weeks=next_week - jan4.isocalendar()[1],
        days=-jan4.isocalendar()[2] + 1
    )

    calendario = []
    for i in range(7):
        dia = start + timedelta(days=i)
        tema_info = CONTENT_THEMES_BY_DAY[i]
        for plataforma in platforms:
            formato = tema_info["formatos"][0] if tema_info["formatos"] else "post"
            calendario.append({
                "data": dia.strftime("%Y-%m-%d"),
                "dia_semana": dia.strftime("%A"),
                "plataforma": plataforma,
                "tema": tema_info["tema"],
                "formato_sugerido": formato,
            })

    return calendario


# ──────────────────────────────────────────────
# Geração do relatório em Markdown
# ──────────────────────────────────────────────

def generate_weekly_report(week_data: Dict) -> str:
    """
    Gera o relatório semanal completo em formato Markdown.

    week_data deve conter:
    {
        "week": "2026-W07",
        "content": [...],       # lista de conteúdos (opcional)
        "seo": [...],           # lista de URLs com métricas SEO (opcional)
        "email": {...},         # métricas de email (opcional)
        "meta_geral": {...}     # KPIs gerais manuais (opcional)
    }
    """
    week_str = week_data.get("week", get_current_week())

    try:
        start_date, end_date = get_week_dates(week_str)
        periodo = f"{start_date.strftime('%d/%m')} a {end_date.strftime('%d/%m/%Y')}"
    except ValueError:
        periodo = week_str

    week_num = parse_week_number(week_str) if re.match(r'^\d{4}-W\d{2}$', week_str) else 0

    # Processar métricas
    content_list = week_data.get("content", [])
    seo_list = week_data.get("seo", [])
    email_metrics = week_data.get("email")

    content_metrics = collect_content_metrics(content_list)
    seo_metrics = collect_seo_metrics(seo_list)
    recommendations = generate_next_week_recommendations(content_metrics, seo_metrics, email_metrics)

    # Plataformas ativas
    plataformas_ativas = list(content_metrics.get("por_plataforma", {}).keys()) or ["instagram"]
    calendario = generate_suggested_calendar(week_str, plataformas_ativas[:2])

    # ── Montar relatório ──
    linhas = []
    linhas.append(f"# Relatório Semanal — Semana {week_num} / {week_str[:4]}")
    linhas.append(f"\n**Período:** {periodo}")
    linhas.append(f"**Gerado em:** {datetime.now().strftime('%d/%m/%Y às %H:%M')}")
    linhas.append(f"**Versão:** Marketing OS Weekly Report v1.0")

    # ── Resumo Executivo ──
    linhas.append("\n---\n\n## Resumo Executivo\n")

    meta_geral = week_data.get("meta_geral", {})
    linhas.append("| Métrica | Esta Semana | Meta |")
    linhas.append("|---------|-------------|------|")
    linhas.append(f"| Peças publicadas | {content_metrics['total_pecas']} | 5-7 |")
    linhas.append(f"| Alcance total | {content_metrics['alcance_total']:,} | — |")
    linhas.append(f"| Engajamentos | {content_metrics['engajamento_total']:,} | — |")
    linhas.append(f"| Taxa de engajamento | {content_metrics['taxa_engajamento_media']:.1f}% | > 3% |")

    if email_metrics:
        linhas.append(f"| Taxa de abertura (email) | {email_metrics.get('taxa_abertura', 0):.1f}% | > 25% |")
        linhas.append(f"| Taxa de clique (email) | {email_metrics.get('taxa_clique', 0):.1f}% | > 3% |")

    if seo_metrics["impressoes_total"] > 0:
        linhas.append(f"| Impressões orgânicas | {seo_metrics['impressoes_total']:,} | — |")
        linhas.append(f"| Cliques orgânicos | {seo_metrics['cliques_total']:,} | — |")
        linhas.append(f"| CTR médio (SEO) | {seo_metrics['ctr_medio']:.1f}% | > 3% |")

    # ── Performance de Conteúdo ──
    linhas.append("\n---\n\n## Performance de Conteúdo\n")

    if content_metrics["total_pecas"] == 0:
        linhas.append("_Nenhum dado de conteúdo fornecido para esta semana._")
    else:
        # Por plataforma
        linhas.append("### Por Plataforma\n")
        linhas.append("| Plataforma | Peças | Alcance | Engajamentos | Taxa Eng. |")
        linhas.append("|-----------|-------|---------|--------------|-----------|")
        for plat, dados in content_metrics["por_plataforma"].items():
            alcance = dados.get("alcance", 0)
            eng = dados.get("engajamentos", 0)
            taxa = (eng / alcance * 100) if alcance > 0 else 0
            linhas.append(f"| {plat} | {dados['pecas']} | {alcance:,} | {eng:,} | {taxa:.1f}% |")

        # Por formato
        linhas.append("\n### Por Formato\n")
        linhas.append("| Formato | Quantidade |")
        linhas.append("|---------|------------|")
        for fmt, qtd in sorted(content_metrics["por_formato"].items(), key=lambda x: x[1], reverse=True):
            linhas.append(f"| {fmt} | {qtd} |")

        # Top conteúdos
        if content_metrics["top_conteudos"]:
            linhas.append("\n### Top 3 Conteúdos da Semana\n")
            for i, c in enumerate(content_metrics["top_conteudos"], 1):
                alcance = c.get("alcance", 0)
                eng = c.get("engajamentos", 0)
                taxa = (eng / alcance * 100) if alcance > 0 else 0
                linhas.append(f"**{i}. {c.get('titulo', 'Sem título')}**")
                linhas.append(f"- Plataforma: {c.get('plataforma', '—')} | Formato: {c.get('formato', '—')}")
                linhas.append(f"- Alcance: {alcance:,} | Engajamentos: {eng:,} | Taxa: {taxa:.1f}%")
                linhas.append("")

        # Bottom conteúdos
        if len(content_metrics.get("bottom_conteudos", [])) > 0:
            linhas.append("### Bottom 3 Conteúdos (menor performance)\n")
            for i, c in enumerate(content_metrics["bottom_conteudos"], 1):
                alcance = c.get("alcance", 0)
                eng = c.get("engajamentos", 0)
                taxa = (eng / alcance * 100) if alcance > 0 else 0
                linhas.append(f"**{i}. {c.get('titulo', 'Sem título')}**")
                linhas.append(f"- Plataforma: {c.get('plataforma', '—')} | Taxa: {taxa:.1f}%")
                linhas.append(f"- Possível causa: hook fraco, horário inadequado ou tema com baixo interesse")
                linhas.append("")

    # ── Email Marketing ──
    if email_metrics:
        linhas.append("\n---\n\n## Email Marketing\n")
        linhas.append("| Métrica | Resultado | Benchmark |")
        linhas.append("|---------|-----------|-----------|")
        linhas.append(f"| Emails enviados | {email_metrics.get('enviados', '—'):,} | — |")
        linhas.append(f"| Taxa de abertura | {email_metrics.get('taxa_abertura', 0):.1f}% | > 25% |")
        linhas.append(f"| Taxa de clique | {email_metrics.get('taxa_clique', 0):.1f}% | > 3% |")
        linhas.append(f"| Taxa de conversão | {email_metrics.get('taxa_conversao', 0):.1f}% | > 1% |")
        if email_metrics.get("taxa_descadastro") is not None:
            linhas.append(f"| Taxa de descadastro | {email_metrics.get('taxa_descadastro', 0):.2f}% | < 0.2% |")

    # ── SEO ──
    if seo_metrics["total_urls"] > 0:
        linhas.append("\n---\n\n## SEO — Tráfego Orgânico\n")

        if seo_metrics["quick_wins"]:
            linhas.append("### Quick Wins Identificados\n")
            linhas.append("_Páginas com alto potencial de melhoria de CTR:_\n")
            linhas.append("| Página | Posição | Impressões | CTR Atual |")
            linhas.append("|--------|---------|------------|-----------|")
            for qw in seo_metrics["quick_wins"]:
                titulo = qw.get("titulo") or qw.get("url", "—")[:50]
                linhas.append(
                    f"| {titulo} | {qw.get('posicao_media', '—'):.0f} | "
                    f"{qw.get('impressoes', 0):,} | {qw.get('ctr', 0):.1f}% |"
                )

        if seo_metrics["top_paginas"]:
            linhas.append("\n### Top Páginas por Tráfego\n")
            linhas.append("| Página | Cliques | Impressões | CTR |")
            linhas.append("|--------|---------|------------|-----|")
            for tp in seo_metrics["top_paginas"]:
                titulo = tp.get("titulo") or tp.get("url", "—")[:50]
                linhas.append(
                    f"| {titulo} | {tp.get('cliques', 0):,} | "
                    f"{tp.get('impressoes', 0):,} | {tp.get('ctr', 0):.1f}% |"
                )

    # ── Recomendações ──
    linhas.append("\n---\n\n## Recomendações para a Próxima Semana\n")
    for i, rec in enumerate(recommendations, 1):
        linhas.append(f"{i}. {rec}")

    # ── Calendário Sugerido ──
    if calendario:
        linhas.append("\n---\n\n## Calendário Sugerido — Próxima Semana\n")
        linhas.append("| Data | Dia | Plataforma | Tema | Formato |")
        linhas.append("|------|-----|-----------|------|---------|")
        for item in calendario:
            linhas.append(
                f"| {item['data']} | {item['dia_semana']} | "
                f"{item['plataforma']} | {item['tema']} | {item['formato_sugerido']} |"
            )

    # ── Rodapé ──
    linhas.append("\n---")
    linhas.append(f"\n_Relatório gerado automaticamente pelo Marketing OS Weekly Report._")
    linhas.append(f"_Para personalizar, edite `scripts/weekly_report.py`._")

    return "\n".join(linhas)


def export_report(report: str, output_path: Optional[str] = None, fmt: str = "markdown") -> str:
    """
    Exporta o relatório para arquivo.
    Retorna o caminho do arquivo salvo.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if output_path is None:
        week = get_current_week()
        filename = f"semana-{week}.md"
        output_path = os.path.join(OUTPUT_DIR, filename)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    return output_path


def load_week_data(json_path: str) -> Dict:
    """Carrega dados da semana de um arquivo JSON."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="Gera relatório semanal de performance do Marketing OS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python weekly_report.py
  python weekly_report.py --week 2026-W07
  python weekly_report.py --input dados.json --output relatorio.md
  python weekly_report.py --week 2026-W06 --output output/reports/semana-06.md
        """
    )

    parser.add_argument(
        "--week", "-w",
        default=None,
        help="Semana no formato YYYY-Www (padrão: semana atual)"
    )
    parser.add_argument(
        "--input", "-i",
        default=None,
        help="Arquivo JSON com dados da semana"
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Arquivo de saída (padrão: output/reports/semana-YYYY-Www.md)"
    )
    parser.add_argument(
        "--format", "-f",
        default="markdown",
        choices=["markdown"],
        help="Formato de saída (padrão: markdown)"
    )
    parser.add_argument(
        "--print", "-p",
        action="store_true",
        help="Imprimir relatório no terminal além de salvar"
    )

    args = parser.parse_args()

    # Determinar semana
    week = args.week or get_current_week()

    # Carregar ou construir dados
    if args.input:
        if not os.path.exists(args.input):
            print(f"\n❌ Arquivo não encontrado: {args.input}")
            sys.exit(1)
        week_data = load_week_data(args.input)
        week_data.setdefault("week", week)
    else:
        # Dados vazios — relatório de template
        week_data = {"week": week}

    # Gerar relatório
    report = generate_weekly_report(week_data)

    # Exportar
    output_path = export_report(report, args.output)
    print(f"\n✅ Relatório gerado: {output_path}")

    # Imprimir se solicitado
    if args.print:
        print("\n" + "=" * 60)
        print(report)

    return report


if __name__ == "__main__":
    main()
