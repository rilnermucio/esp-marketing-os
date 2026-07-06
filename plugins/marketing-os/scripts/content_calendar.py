#!/usr/bin/env python3
"""
Content Calendar Generator
Gera calendário editorial para múltiplas plataformas.
"""

import json
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional

from validators import (
    ValidationError,
    validar_data,
    validar_inteiro,
    validar_lista_plataformas,
    handle_validation_error,
)

# Templates de conteúdo por dia da semana
CONTENT_THEMES = {
    "monday": {
        "theme": "Motivação & Planejamento",
        "ideas": [
            "Metas da semana",
            "Citação motivacional",
            "Tips de produtividade",
            "Behind the scenes",
        ],
        "formats": ["Carrossel", "Story", "Reels curto"],
    },
    "tuesday": {
        "theme": "Educação & Valor",
        "ideas": ["Tutorial", "How-to", "Dica prática", "Breakdown de processo"],
        "formats": ["Carrossel educativo", "Vídeo tutorial", "Thread"],
    },
    "wednesday": {
        "theme": "Engajamento & Comunidade",
        "ideas": ["Enquete", "Pergunta aberta", "Caixinha de perguntas", "Debate"],
        "formats": ["Story interativo", "Post de pergunta", "Lives"],
    },
    "thursday": {
        "theme": "Cases & Provas",
        "ideas": ["Case de sucesso", "Antes/depois", "Depoimento", "Resultados"],
        "formats": ["Carrossel de case", "Vídeo testimonial", "Story"],
    },
    "friday": {
        "theme": "Entretenimento & Trends",
        "ideas": [
            "Trend do momento",
            "Meme do nicho",
            "Bastidores divertidos",
            "Recap da semana",
        ],
        "formats": ["Reels trend", "Meme", "Story casual"],
    },
    "saturday": {
        "theme": "Lifestyle & Personal Brand",
        "ideas": ["Dia a dia", "Hobbies", "Reflexão pessoal", "Inspiração"],
        "formats": ["Story lifestyle", "Post pessoal", "Carrossel"],
    },
    "sunday": {
        "theme": "Preparação & Preview",
        "ideas": [
            "Preview da semana",
            "Conteúdo planejado",
            "Expectativas",
            "Descanso",
        ],
        "formats": ["Story leve", "Post de preparação"],
    },
}

# Horários ideais por plataforma
BEST_TIMES = {
    "instagram": {
        "weekday": ["07:00", "12:00", "19:00"],
        "weekend": ["10:00", "14:00", "20:00"],
    },
    "linkedin": {
        "weekday": ["08:00", "12:00", "17:00"],
        "weekend": ["10:00"],
    },
    "twitter": {
        "weekday": ["08:00", "12:00", "17:00", "21:00"],
        "weekend": ["09:00", "12:00"],
    },
    "tiktok": {
        "weekday": ["07:00", "12:00", "19:00", "21:00"],
        "weekend": ["11:00", "19:00", "21:00"],
    },
    "facebook": {
        "weekday": ["09:00", "13:00", "16:00"],
        "weekend": ["12:00", "13:00"],
    },
}

# Frequência recomendada por plataforma
FREQUENCY = {
    "instagram": {"feed": "3-5/semana", "stories": "5-10/dia", "reels": "3-7/semana"},
    "linkedin": {"posts": "2-5/semana", "articles": "1/semana"},
    "twitter": {"tweets": "3-5/dia", "threads": "1-2/semana"},
    "tiktok": {"videos": "1-3/dia"},
    "facebook": {"posts": "1-2/dia"},
}


def generate_calendar(
    start_date: str,
    weeks: int = 4,
    platforms: Optional[List[str]] = None,
    nicho: str = "geral",
) -> Dict:
    """Gera calendário editorial."""

    if platforms is None:
        platforms = ["instagram"]

    start = datetime.strptime(start_date, "%Y-%m-%d")
    calendar = []

    day_names = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]

    for week in range(weeks):
        week_content = {
            "week": week + 1,
            "start_date": (start + timedelta(weeks=week)).strftime("%Y-%m-%d"),
            "end_date": (start + timedelta(weeks=week, days=6)).strftime("%Y-%m-%d"),
            "days": [],
        }

        for day_offset in range(7):
            current_date = start + timedelta(weeks=week, days=day_offset)
            day_name = day_names[current_date.weekday()]
            theme_data = CONTENT_THEMES[day_name]

            is_weekend = day_name in ["saturday", "sunday"]

            day_content = {
                "date": current_date.strftime("%Y-%m-%d"),
                "day_of_week": day_name.capitalize(),
                "theme": theme_data["theme"],
                "platforms": {},
            }

            for platform in platforms:
                times = BEST_TIMES.get(platform, BEST_TIMES["instagram"])
                posting_times = times["weekend"] if is_weekend else times["weekday"]

                day_content["platforms"][platform] = {
                    "suggested_times": posting_times,
                    "content_ideas": theme_data["ideas"],
                    "formats": theme_data["formats"],
                    "frequency": FREQUENCY.get(platform, {}),
                }

            week_content["days"].append(day_content)

        calendar.append(week_content)

    return {
        "calendar": calendar,
        "summary": {
            "total_weeks": weeks,
            "platforms": platforms,
            "nicho": nicho,
            "start_date": start_date,
            "end_date": (start + timedelta(weeks=weeks - 1, days=6)).strftime(
                "%Y-%m-%d"
            ),
        },
        "recommendations": {
            "batch_creation": "Crie conteúdo em lotes (1 dia = 1 semana de conteúdo)",
            "scheduling": "Use ferramentas como Later, Buffer ou Meta Business Suite",
            "consistency": "Mantenha consistência de horários para criar hábito no público",
            "analytics": "Revise métricas semanalmente e ajuste o calendário",
            "flexibility": "Reserve 20% para conteúdo reativo a trends e oportunidades",
        },
        "content_pillars": [
            {
                "name": "Educativo",
                "percentage": 40,
                "examples": "Tutoriais, dicas, how-to",
            },
            {
                "name": "Inspiracional",
                "percentage": 20,
                "examples": "Motivação, cases, histórias",
            },
            {
                "name": "Entretenimento",
                "percentage": 20,
                "examples": "Trends, memes, bastidores",
            },
            {
                "name": "Promocional",
                "percentage": 20,
                "examples": "Produtos, ofertas, CTAs",
            },
        ],
    }


USO = (
    "Uso: python content_calendar.py <data_inicio> [semanas] [plataformas...]\n"
    "Exemplo: python content_calendar.py 2025-02-01 4 instagram linkedin\n"
    "Plataformas: instagram, linkedin, twitter, tiktok, facebook"
)


def main() -> None:
    if len(sys.argv) < 2:
        print(USO)
        sys.exit(1)

    try:
        data_obj = validar_data(sys.argv[1], campo="data_inicio")
        start_date = data_obj.strftime("%Y-%m-%d")
        weeks = (
            validar_inteiro(sys.argv[2], campo="semanas", min_val=1, max_val=52)
            if len(sys.argv) > 2
            else 4
        )
        platforms = (
            validar_lista_plataformas(sys.argv[3:], campo="plataformas")
            if len(sys.argv) > 3
            else ["instagram"]
        )
    except ValidationError as e:
        handle_validation_error(e, mostrar_uso=USO)
        return

    result = generate_calendar(start_date, weeks, platforms)

    print("\n" + "=" * 70)
    print("📅 CALENDÁRIO EDITORIAL")
    print("=" * 70)

    print(f"\n📊 RESUMO:")
    print(
        f"   Período: {result['summary']['start_date']} a {result['summary']['end_date']}"
    )
    print(f"   Semanas: {result['summary']['total_weeks']}")
    print(f"   Plataformas: {', '.join(result['summary']['platforms'])}")

    print("\n📌 PILARES DE CONTEÚDO:")
    for pillar in result["content_pillars"]:
        print(f"   • {pillar['name']} ({pillar['percentage']}%): {pillar['examples']}")

    print("\n📆 CALENDÁRIO SEMANAL:")
    for week in result["calendar"]:
        print(
            f"\n   === SEMANA {week['week']} ({week['start_date']} - {week['end_date']}) ==="
        )
        for day in week["days"]:
            print(f"   {day['day_of_week']}: {day['theme']}")
            for platform, details in day["platforms"].items():
                print(
                    f"      [{platform}] Horários: {', '.join(details['suggested_times'])}"
                )

    print("\n💡 RECOMENDAÇÕES:")
    for key, value in result["recommendations"].items():
        print(f"   • {value}")

    print("\n" + "=" * 70)

    # Salvar JSON
    output_file = f"calendar_{start_date}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\n📄 Calendário salvo em: {output_file}")


if __name__ == "__main__":
    main()
