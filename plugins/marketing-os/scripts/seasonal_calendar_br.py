#!/usr/bin/env python3
"""
Calendário sazonal BR - efemérides comerciais e culturais brasileiras.

Camada de dados determinística: computa as datas pra qualquer ano (sem dataset
estático). Datas fixas, baseadas em regra (N-ésimo dia da semana) e móveis
(Computus a partir da Páscoa).

Uso:
    python seasonal_calendar_br.py --ano 2026
    python seasonal_calendar_br.py --from 2026-06-01 --to 2026-12-31
    python seasonal_calendar_br.py --proximos 90
    python seasonal_calendar_br.py --ano 2026 --json
"""

import argparse
import datetime as dt
from typing import Dict, List

from output_formatter import OutputFormatter, add_output_args


# --------------------------------------------------------------- cálculo de datas
def easter(year: int) -> dt.date:
    """Domingo de Páscoa (algoritmo de Computus, gregoriano anônimo)."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    ell = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * ell) // 451
    month = (h + ell - 7 * m + 114) // 31
    day = ((h + ell - 7 * m + 114) % 31) + 1
    return dt.date(year, month, day)


def nth_weekday(year: int, month: int, weekday: int, n: int) -> dt.date:
    """N-ésima ocorrência de um dia da semana (seg=0..dom=6) num mês."""
    first = dt.date(year, month, 1)
    shift = (weekday - first.weekday()) % 7
    return first + dt.timedelta(days=shift + 7 * (n - 1))


def _black_friday(year: int) -> dt.date:
    """Dia seguinte à 4ª quinta-feira de novembro (sexta pós-Thanksgiving)."""
    return nth_weekday(year, 11, 3, 4) + dt.timedelta(days=1)


# (nome, tipo, dias_antecedencia_ideal, nichos_fortes, função->date)
_DEFS: List[tuple] = [
    (
        "Ano Novo",
        "cultural",
        30,
        ["varejo", "fitness", "desenvolvimento pessoal"],
        lambda y: dt.date(y, 1, 1),
    ),
    (
        "Dia do Consumidor",
        "comercial",
        15,
        ["e-commerce", "varejo", "serviços"],
        lambda y: dt.date(y, 3, 15),
    ),
    (
        "Carnaval",
        "cultural",
        30,
        ["turismo", "bebidas", "moda", "eventos"],
        lambda y: easter(y) - dt.timedelta(days=47),
    ),
    (
        "Sexta-feira Santa",
        "religiosa",
        14,
        ["religião", "turismo", "alimentação"],
        lambda y: easter(y) - dt.timedelta(days=2),
    ),
    (
        "Páscoa",
        "religiosa",
        21,
        ["alimentação", "chocolate", "varejo", "religião"],
        easter,
    ),
    (
        "Dia das Mães",
        "comercial",
        30,
        ["varejo", "moda", "beleza", "presentes", "joias"],
        lambda y: nth_weekday(y, 5, 6, 2),
    ),
    (
        "Corpus Christi",
        "religiosa",
        7,
        ["religião", "turismo"],
        lambda y: easter(y) + dt.timedelta(days=60),
    ),
    (
        "Dia dos Namorados",
        "comercial",
        30,
        ["varejo", "moda", "beleza", "presentes", "restaurantes"],
        lambda y: dt.date(y, 6, 12),
    ),
    (
        "Dia dos Pais",
        "comercial",
        30,
        ["varejo", "moda", "eletrônicos", "presentes"],
        lambda y: nth_weekday(y, 8, 6, 2),
    ),
    (
        "Dia do Cliente",
        "comercial",
        14,
        ["e-commerce", "varejo", "serviços", "fidelização"],
        lambda y: dt.date(y, 9, 15),
    ),
    (
        "Dia das Crianças",
        "comercial",
        30,
        ["brinquedos", "varejo", "moda infantil", "educação"],
        lambda y: dt.date(y, 10, 12),
    ),
    (
        "Dia do Solteiro (11.11)",
        "comercial",
        14,
        ["e-commerce", "tech", "varejo"],
        lambda y: dt.date(y, 11, 11),
    ),
    (
        "Black Friday",
        "comercial",
        45,
        ["e-commerce", "tech", "varejo", "infoprodutos"],
        _black_friday,
    ),
    (
        "Cyber Monday",
        "comercial",
        45,
        ["tech", "e-commerce", "SaaS", "infoprodutos"],
        lambda y: _black_friday(y) + dt.timedelta(days=3),
    ),
    (
        "Natal",
        "cultural",
        45,
        ["varejo", "presentes", "alimentação", "moda"],
        lambda y: dt.date(y, 12, 25),
    ),
]


def seasonal_dates(year: int) -> List[Dict]:
    """Todas as efemérides do ano, ordenadas por data."""
    out: List[Dict] = []
    for nome, tipo, antec, nichos, fn in _DEFS:
        data = fn(year)
        out.append(
            {
                "data": data.isoformat(),
                "nome": nome,
                "tipo": tipo,
                "dias_antecedencia_ideal": antec,
                "nichos_fortes": list(nichos),
            }
        )
    return sorted(out, key=lambda x: x["data"])


def dates_in_range(start: dt.date, end: dt.date) -> List[Dict]:
    """Efemérides entre start e end (inclusive), cobrindo os anos do intervalo."""
    todas: List[Dict] = []
    for year in range(start.year, end.year + 1):
        todas.extend(seasonal_dates(year))
    s, e = start.isoformat(), end.isoformat()
    return [d for d in todas if s <= d["data"] <= e]


def proximos(n_dias: int, hoje: dt.date = None) -> List[Dict]:
    """Efemérides nos próximos n_dias a partir de hoje."""
    if hoje is None:
        hoje = dt.date.today()
    return dates_in_range(hoje, hoje + dt.timedelta(days=n_dias))


# --------------------------------------------------------------- saída humana
def _print_human(dates: List[Dict]) -> None:
    if not dates:
        print("Nenhuma data sazonal na janela.")
        return
    print("\n📅 CALENDÁRIO SAZONAL BR")
    print("=" * 60)
    for d in dates:
        nichos = ", ".join(d["nichos_fortes"][:4])
        print(f"\n  {d['data']}  {d['nome']}  [{d['tipo']}]")
        print(
            f"     comece ~{d['dias_antecedencia_ideal']} dias antes  |  nichos: {nichos}"
        )
    print()


# --------------------------------------------------------------- CLI
def main() -> None:
    parser = argparse.ArgumentParser(description="Calendário sazonal comercial BR")
    parser.add_argument("--ano", type=int, help="Todas as datas do ano")
    parser.add_argument("--from", dest="inicio", help="Início da janela (YYYY-MM-DD)")
    parser.add_argument("--to", dest="fim", help="Fim da janela (YYYY-MM-DD)")
    parser.add_argument(
        "--proximos", type=int, default=90, help="Próximos N dias (padrão: 90)"
    )
    add_output_args(parser)
    args = parser.parse_args()
    fmt = OutputFormatter(args)

    if args.ano:
        dates = seasonal_dates(args.ano)
    elif args.inicio and args.fim:
        dates = dates_in_range(
            dt.date.fromisoformat(args.inicio), dt.date.fromisoformat(args.fim)
        )
    else:
        dates = proximos(args.proximos)

    fmt.print(dates, human_fn=lambda d: _print_human(d))


if __name__ == "__main__":
    main()
