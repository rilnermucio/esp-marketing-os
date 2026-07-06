#!/usr/bin/env python3
"""
Módulo de formatação de output padronizado para scripts do Marketing OS.

Garante saída consistente em dois modos:
  - Humano (padrão): texto formatado, tabelas, emojis
  - JSON (--json / --format json): JSON puro para integração com outras ferramentas

Uso:
    from output_formatter import OutputFormatter, add_output_args

    # Em parsers argparse:
    parser = argparse.ArgumentParser(...)
    add_output_args(parser)
    args = parser.parse_args()

    fmt = OutputFormatter(args)
    fmt.print(data)          # JSON se --json, texto se não
    fmt.save(data, "saida")  # Salva arquivo .json ou .md
"""

import argparse
import json
from datetime import datetime, date
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Serialização JSON segura (lida com tipos não serializáveis)
# ---------------------------------------------------------------------------


class _SafeEncoder(json.JSONEncoder):
    """Encoder JSON que lida com datetime, date e sets."""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, set):
            return sorted(obj)
        return super().default(obj)


def to_json(data: Any, indent: int = 2) -> str:
    """Serializa dados para JSON formatado, tratando tipos especiais."""
    return json.dumps(data, indent=indent, ensure_ascii=False, cls=_SafeEncoder)


# ---------------------------------------------------------------------------
# Funções utilitárias de impressão
# ---------------------------------------------------------------------------


def print_json(data: Any) -> None:
    """Imprime dados como JSON formatado."""
    print(to_json(data))


def print_separator(char: str = "=", width: int = 60) -> None:
    """Imprime linha separadora."""
    print(char * width)


def print_table(
    rows: List[Dict],
    columns: List[Dict],
    title: Optional[str] = None,
) -> None:
    """
    Imprime dados como tabela formatada.

    Args:
        rows: Lista de dicionários com os dados.
        columns: Lista de definições de coluna.
            Cada coluna é um dict com:
              - key (str): chave no dicionário de dados
              - label (str): cabeçalho da coluna
              - width (int): largura da coluna
              - align (str): 'left', 'right', 'center' (padrão: 'left')
              - format (str): formato numérico (ex: '.1f', '.2%')
        title: Título opcional a exibir acima da tabela.
    """
    if not rows:
        print("  (sem dados)")
        return

    if title:
        print(f"\n{title}")

    # Cabeçalho
    header = ""
    divider = ""
    for col in columns:
        w = col.get("width", 15)
        label = col.get("label", col["key"])[:w]
        align = col.get("align", "left")
        if align == "right":
            header += f"{label:>{w}} "
            divider += "-" * w + " "
        else:
            header += f"{label:<{w}} "
            divider += "-" * w + " "
    print(header.rstrip())
    print(divider.rstrip())

    # Linhas
    for row in rows:
        line = ""
        for col in columns:
            w = col.get("width", 15)
            align = col.get("align", "left")
            fmt = col.get("format")
            val = row.get(col["key"], "")

            if fmt and isinstance(val, (int, float)):
                val_str = format(val, fmt)
            else:
                val_str = str(val)

            val_str = val_str[:w]

            if align == "right":
                line += f"{val_str:>{w}} "
            else:
                line += f"{val_str:<{w}} "
        print(line.rstrip())


def print_key_value(
    data: Dict,
    title: Optional[str] = None,
    indent: int = 3,
) -> None:
    """
    Imprime dicionário como pares chave: valor.

    Args:
        data: Dicionário a exibir.
        title: Título opcional.
        indent: Espaços de indentação.
    """
    if title:
        print(f"\n{title}")
    pad = " " * indent
    for key, val in data.items():
        if isinstance(val, dict):
            print(f"{pad}{key}:")
            for k2, v2 in val.items():
                print(f"{pad}  {k2}: {v2}")
        elif isinstance(val, list):
            print(f"{pad}{key}: {', '.join(str(v) for v in val)}")
        else:
            print(f"{pad}{key}: {val}")


def print_list(
    items: List,
    title: Optional[str] = None,
    bullet: str = "•",
    indent: int = 3,
) -> None:
    """
    Imprime uma lista com marcadores.

    Args:
        items: Lista de itens (strings ou objetos com __str__).
        title: Título opcional.
        bullet: Caractere de marcador.
        indent: Espaços de indentação.
    """
    if title:
        print(f"\n{title}")
    pad = " " * indent
    for item in items:
        print(f"{pad}{bullet} {item}")


# ---------------------------------------------------------------------------
# Classe principal de formatação
# ---------------------------------------------------------------------------


class OutputFormatter:
    """
    Gerencia o modo de saída de um script (humano vs JSON).

    Uso típico:
        fmt = OutputFormatter(args)  # args tem .json e .output
        fmt.print_human("Texto humano")
        fmt.print_data(data_dict)    # JSON se --json, ignorado se não
        fmt.save(data_dict, "relatorio")
    """

    def __init__(self, args: argparse.Namespace):
        self.json_mode: bool = getattr(args, "json", False)
        self.output: Optional[str] = getattr(args, "output", None)
        self.format: str = getattr(
            args, "format", "json" if self.json_mode else "human"
        )

    def is_json(self) -> bool:
        """Retorna True se o modo JSON estiver ativo."""
        return self.json_mode or self.format == "json"

    def print_human(self, *args: Any, **kwargs: Any) -> None:
        """Imprime apenas no modo humano (suprimido em --json)."""
        if not self.is_json():
            print(*args, **kwargs)

    def print_data(self, data: Any) -> None:
        """
        Imprime dados:
        - Modo JSON: JSON formatado
        - Modo humano: não faz nada (cabe ao script imprimir formatado)
        """
        if self.is_json():
            print_json(data)

    def print(self, data: Any, human_fn: Optional[Any] = None) -> None:
        """
        Imprime dados no modo correto.

        Args:
            data: Dados a exibir.
            human_fn: Função opcional para exibição humana. Se None e não JSON, não imprime.
        """
        if self.is_json():
            print_json(data)
        elif human_fn is not None:
            human_fn(data)

    def save(
        self, data: Any, base_name: str, directory: str = "output/reports"
    ) -> Optional[str]:
        """
        Salva dados em arquivo se --output estiver definido.

        Args:
            data: Dados a salvar.
            base_name: Nome base do arquivo (sem extensão).
            directory: Diretório padrão se --output não especificar caminho.

        Returns:
            Caminho do arquivo salvo, ou None se --output não definido.
        """
        output_path = self.output
        if not output_path:
            return None

        import os

        os.makedirs(
            os.path.dirname(output_path) if os.path.dirname(output_path) else directory,
            exist_ok=True,
        )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(to_json(data))

        if not self.is_json():
            print(f"\n💾 Salvo em: {output_path}")

        return output_path


# ---------------------------------------------------------------------------
# Helpers para argparse
# ---------------------------------------------------------------------------


def add_output_args(
    parser: argparse.ArgumentParser,
    include_format: bool = False,
) -> None:
    """
    Adiciona argumentos de output padronizados ao parser.

    Args:
        parser: ArgumentParser a modificar.
        include_format: Se True, adiciona --format além de --json.
    """
    parser.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="Saída em JSON (para integração com outras ferramentas)",
    )
    parser.add_argument(
        "--output",
        "-o",
        metavar="ARQUIVO",
        help="Salvar resultado em arquivo",
    )
    if include_format:
        parser.add_argument(
            "--format",
            choices=["json", "human", "markdown"],
            default="human",
            help="Formato de saída (padrão: human)",
        )
