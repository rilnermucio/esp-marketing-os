#!/usr/bin/env python3
"""
Notion API Integration
Integração com a Notion API v1 para publicação e gestão de conteúdo.

Autenticação: Integration Token (Internal Integration).
Defina a variável de ambiente NOTION_TOKEN antes de usar.
Opcionalmente, defina NOTION_DATABASE_ID para usar um banco de dados padrão.

Uso:
    python notion_api.py list-databases
    python notion_api.py list-pages [--database-id DB_ID] [--limit 10]
    python notion_api.py get-page <page_id>
    python notion_api.py create-page --database-id DB_ID --title "Título" [--content "Texto"]
    python notion_api.py append-block <page_id> --text "Texto a adicionar"
    python notion_api.py search --query "termo" [--type page|database]
    python notion_api.py full-report [--database-id DB_ID]
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from typing import Any, Dict, List, Optional

from output_formatter import add_output_args, OutputFormatter, print_json, print_table, print_key_value
from validators import ValidationError, validar_texto, validar_inteiro, handle_validation_error

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_API_VERSION = "2022-06-28"

ENV_TOKEN = "NOTION_TOKEN"
ENV_DATABASE_ID = "NOTION_DATABASE_ID"

# Tipos de bloco suportados para criação de conteúdo
TIPOS_BLOCO = {
    "paragraph",
    "heading_1",
    "heading_2",
    "heading_3",
    "bulleted_list_item",
    "numbered_list_item",
    "to_do",
    "toggle",
    "quote",
    "callout",
    "divider",
    "code",
}

# Propriedades de banco de dados comuns para marketing
PROPRIEDADES_MARKETING = [
    "Name",
    "Status",
    "Tags",
    "Date",
    "URL",
    "Platform",
    "Content Type",
]


# ---------------------------------------------------------------------------
# Exceções
# ---------------------------------------------------------------------------


class NotionAPIError(Exception):
    """Erro da Notion API."""

    def __init__(self, message: str, status: Optional[int] = None, code: Optional[str] = None):
        super().__init__(message)
        self.status = status
        self.code = code

    def __str__(self) -> str:
        base = super().__str__()
        prefix = f"[HTTP {self.status}] " if self.status else ""
        suffix = f" (código: {self.code})" if self.code else ""
        return f"{prefix}{base}{suffix}"


class NotionAuthError(NotionAPIError):
    """Erro de autenticação com a Notion API."""


# ---------------------------------------------------------------------------
# Funções internas de HTTP
# ---------------------------------------------------------------------------


def _get_token() -> str:
    """Carrega o token da variável de ambiente NOTION_TOKEN."""
    token = os.environ.get(ENV_TOKEN, "").strip()
    if not token:
        raise NotionAuthError(
            f"Token Notion não configurado. Defina a variável de ambiente {ENV_TOKEN}."
        )
    return token


def _headers(token: str) -> Dict[str, str]:
    """Retorna cabeçalhos padrão para requisições à Notion API."""
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_API_VERSION,
        "Content-Type": "application/json",
    }


def _api_get(path: str, token: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """GET autenticado na Notion API com tratamento de erros."""
    url = f"{NOTION_API_BASE}/{path}"
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"

    req = urllib.request.Request(url, headers=_headers(token), method="GET")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = {}
        try:
            body = json.loads(e.read().decode("utf-8"))
        except Exception:
            pass
        raise NotionAPIError(
            body.get("message", str(e)),
            status=e.code,
            code=body.get("code"),
        ) from e


def _api_post(path: str, token: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """POST autenticado na Notion API com tratamento de erros."""
    url = f"{NOTION_API_BASE}/{path}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=_headers(token), method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = {}
        try:
            body = json.loads(e.read().decode("utf-8"))
        except Exception:
            pass
        raise NotionAPIError(
            body.get("message", str(e)),
            status=e.code,
            code=body.get("code"),
        ) from e


def _api_patch(path: str, token: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """PATCH autenticado na Notion API com tratamento de erros."""
    url = f"{NOTION_API_BASE}/{path}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=_headers(token), method="PATCH")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = {}
        try:
            body = json.loads(e.read().decode("utf-8"))
        except Exception:
            pass
        raise NotionAPIError(
            body.get("message", str(e)),
            status=e.code,
            code=body.get("code"),
        ) from e


# ---------------------------------------------------------------------------
# Funções auxiliares
# ---------------------------------------------------------------------------


def _extract_title(page: Dict[str, Any]) -> str:
    """Extrai o título de uma página ou banco de dados Notion."""
    # Bancos de dados têm "title" como lista de rich_text
    if "title" in page and isinstance(page["title"], list):
        parts = [t.get("plain_text", "") for t in page["title"]]
        return "".join(parts) or "(sem título)"

    # Páginas têm propriedades — procura a primeira do tipo "title"
    props = page.get("properties", {})
    for _name, prop in props.items():
        if prop.get("type") == "title":
            parts = [t.get("plain_text", "") for t in prop.get("title", [])]
            return "".join(parts) or "(sem título)"

    return "(sem título)"


def _extract_page_summary(page: Dict[str, Any]) -> Dict[str, Any]:
    """Extrai campos essenciais de uma página Notion."""
    created = page.get("created_time", "")[:10]
    edited = page.get("last_edited_time", "")[:10]
    url = page.get("url", "")
    parent = page.get("parent", {})

    parent_type = parent.get("type", "unknown")
    # A Notion API usa a chave igual ao type (ex: "database_id", "page_id", "workspace")
    parent_id = parent.get(parent_type, "") if parent_type != "unknown" else ""

    return {
        "id": page.get("id", ""),
        "titulo": _extract_title(page),
        "tipo": page.get("object", "page"),
        "criado_em": created,
        "editado_em": edited,
        "url": url,
        "parent_tipo": parent_type,
        "parent_id": parent_id,
    }


def _make_rich_text(text: str) -> List[Dict[str, Any]]:
    """Cria objeto rich_text para a API do Notion a partir de texto simples."""
    return [{"type": "text", "text": {"content": text}}]


def _make_paragraph_block(text: str) -> Dict[str, Any]:
    """Cria um bloco de parágrafo Notion."""
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": _make_rich_text(text)},
    }


def _make_heading_block(text: str, level: int = 2) -> Dict[str, Any]:
    """Cria um bloco de título Notion (heading_1, heading_2, ou heading_3)."""
    level = max(1, min(3, level))
    tipo = f"heading_{level}"
    return {
        "object": "block",
        "type": tipo,
        tipo: {"rich_text": _make_rich_text(text)},
    }


# ---------------------------------------------------------------------------
# Funções públicas
# ---------------------------------------------------------------------------


def list_databases(token: str, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Lista os bancos de dados acessíveis pela integração.

    Args:
        token: Integration token do Notion.
        limit: Número máximo de resultados (1–100).

    Returns:
        Lista de dicionários com id, título e url de cada banco de dados.
    """
    payload = {
        "filter": {"value": "database", "property": "object"},
        "page_size": min(max(1, limit), 100),
    }
    result = _api_post("search", token, payload)
    databases = []
    for db in result.get("results", []):
        databases.append({
            "id": db.get("id", ""),
            "titulo": _extract_title(db),
            "url": db.get("url", ""),
            "criado_em": db.get("created_time", "")[:10],
            "editado_em": db.get("last_edited_time", "")[:10],
        })
    return databases


def list_pages(
    token: str,
    database_id: str,
    limit: int = 10,
    filter_payload: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Lista páginas de um banco de dados Notion.

    Args:
        token: Integration token do Notion.
        database_id: ID do banco de dados.
        limit: Número máximo de páginas (1–100).
        filter_payload: Filtro opcional no formato da Notion API.

    Returns:
        Lista de resumos de páginas (id, titulo, criado_em, editado_em, url).
    """
    payload: Dict[str, Any] = {"page_size": min(max(1, limit), 100)}
    if filter_payload:
        payload["filter"] = filter_payload

    result = _api_post(f"databases/{database_id}/query", token, payload)
    pages = []
    for page in result.get("results", []):
        pages.append(_extract_page_summary(page))
    return pages


def get_page(token: str, page_id: str) -> Dict[str, Any]:
    """
    Retorna os detalhes de uma página Notion.

    Args:
        token: Integration token do Notion.
        page_id: ID da página.

    Returns:
        Dicionário com campos da página (id, titulo, propriedades, url, etc.).
    """
    page = _api_get(f"pages/{page_id}", token)
    summary = _extract_page_summary(page)
    # Inclui propriedades brutas para inspeção
    summary["propriedades"] = {
        name: prop.get("type") for name, prop in page.get("properties", {}).items()
    }
    return summary


def create_page(
    token: str,
    database_id: str,
    title: str,
    content: Optional[str] = None,
    properties: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Cria uma nova página em um banco de dados Notion.

    Args:
        token: Integration token do Notion.
        database_id: ID do banco de dados pai.
        title: Título da página.
        content: Texto opcional para o primeiro bloco de parágrafo.
        properties: Propriedades adicionais no formato da Notion API.

    Returns:
        Dicionário com id, titulo e url da página criada.
    """
    props: Dict[str, Any] = {
        "title": {"title": _make_rich_text(title)},
    }
    if properties:
        props.update(properties)

    children = []
    if content:
        children.append(_make_paragraph_block(content))

    payload: Dict[str, Any] = {
        "parent": {"database_id": database_id},
        "properties": props,
    }
    if children:
        payload["children"] = children

    page = _api_post("pages", token, payload)
    return {
        "id": page.get("id", ""),
        "titulo": _extract_title(page),
        "url": page.get("url", ""),
        "criado_em": page.get("created_time", "")[:10],
    }


def append_block(token: str, page_id: str, text: str, block_type: str = "paragraph") -> Dict[str, Any]:
    """
    Adiciona um bloco de texto a uma página Notion existente.

    Args:
        token: Integration token do Notion.
        page_id: ID da página de destino.
        text: Texto a adicionar.
        block_type: Tipo do bloco (paragraph, heading_1, heading_2, heading_3,
                    bulleted_list_item, numbered_list_item, quote).

    Returns:
        Dicionário com resultados da operação (id dos blocos criados).
    """
    if block_type.startswith("heading_"):
        try:
            level = int(block_type.split("_")[1])
        except (IndexError, ValueError):
            level = 2
        block = _make_heading_block(text, level)
    elif block_type in TIPOS_BLOCO:
        block = {
            "object": "block",
            "type": block_type,
            block_type: {"rich_text": _make_rich_text(text)},
        }
    else:
        block = _make_paragraph_block(text)

    result = _api_patch(
        f"blocks/{page_id}/children",
        token,
        {"children": [block]},
    )
    ids = [b.get("id", "") for b in result.get("results", [])]
    return {"page_id": page_id, "blocos_criados": ids, "total": len(ids)}


def search(
    token: str,
    query: str,
    search_type: Optional[str] = None,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """
    Pesquisa páginas e bancos de dados na integração Notion.

    Args:
        token: Integration token do Notion.
        query: Termo de pesquisa.
        search_type: Filtrar por "page" ou "database" (None = ambos).
        limit: Número máximo de resultados (1–100).

    Returns:
        Lista de resumos dos resultados encontrados.
    """
    payload: Dict[str, Any] = {
        "query": query,
        "page_size": min(max(1, limit), 100),
    }
    if search_type in ("page", "database"):
        payload["filter"] = {"value": search_type, "property": "object"}

    result = _api_post("search", token, payload)
    return [_extract_page_summary(item) for item in result.get("results", [])]


def get_database_schema(token: str, database_id: str) -> Dict[str, Any]:
    """
    Retorna o schema (propriedades) de um banco de dados Notion.

    Args:
        token: Integration token do Notion.
        database_id: ID do banco de dados.

    Returns:
        Dicionário com titulo e mapa de propriedades {nome: tipo}.
    """
    db = _api_get(f"databases/{database_id}", token)
    schema = {
        name: prop.get("type", "unknown")
        for name, prop in db.get("properties", {}).items()
    }
    return {
        "id": database_id,
        "titulo": _extract_title(db),
        "propriedades": schema,
        "total_propriedades": len(schema),
    }


def full_report(token: str, database_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Gera relatório completo: lista bancos de dados e páginas recentes.

    Args:
        token: Integration token do Notion.
        database_id: ID opcional de banco de dados para detalhar páginas.

    Returns:
        Dicionário com databases, páginas recentes e metadados do relatório.
    """
    databases = list_databases(token, limit=50)
    report: Dict[str, Any] = {
        "gerado_em": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_databases": len(databases),
        "databases": databases,
    }

    if database_id:
        try:
            schema = get_database_schema(token, database_id)
            pages = list_pages(token, database_id, limit=20)
            report["database_detalhado"] = schema
            report["paginas_recentes"] = pages
            report["total_paginas"] = len(pages)
        except NotionAPIError as e:
            report["erro_database"] = str(e)

    return report


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="notion_api.py",
        description="Notion API — gestão de conteúdo via CLI",
    )
    add_output_args(parser)

    sub = parser.add_subparsers(dest="subcommand", required=True)

    # list-databases
    sub.add_parser("list-databases", help="Lista bancos de dados acessíveis")

    # list-pages
    p_lp = sub.add_parser("list-pages", help="Lista páginas de um banco de dados")
    p_lp.add_argument("--database-id", "-d", default="", help="ID do banco de dados")
    p_lp.add_argument("--limit", "-l", type=int, default=10, help="Máximo de páginas (padrão: 10)")

    # get-page
    p_gp = sub.add_parser("get-page", help="Detalhes de uma página")
    p_gp.add_argument("page_id", help="ID da página")

    # create-page
    p_cp = sub.add_parser("create-page", help="Cria nova página em um banco de dados")
    p_cp.add_argument("--database-id", "-d", required=True, help="ID do banco de dados")
    p_cp.add_argument("--title", "-t", required=True, help="Título da página")
    p_cp.add_argument("--content", "-c", default="", help="Conteúdo inicial (parágrafo)")

    # append-block
    p_ab = sub.add_parser("append-block", help="Adiciona bloco de texto a uma página")
    p_ab.add_argument("page_id", help="ID da página")
    p_ab.add_argument("--text", "-t", required=True, help="Texto do bloco")
    p_ab.add_argument(
        "--type",
        default="paragraph",
        choices=sorted(TIPOS_BLOCO),
        help="Tipo do bloco (padrão: paragraph)",
    )

    # search
    p_s = sub.add_parser("search", help="Pesquisa páginas e bancos de dados")
    p_s.add_argument("--query", "-q", required=True, help="Termo de pesquisa")
    p_s.add_argument(
        "--type",
        choices=["page", "database"],
        default=None,
        help="Filtrar por tipo (padrão: ambos)",
    )
    p_s.add_argument("--limit", "-l", type=int, default=10, help="Máximo de resultados")

    # schema
    p_sc = sub.add_parser("schema", help="Schema de um banco de dados")
    p_sc.add_argument("--database-id", "-d", required=True, help="ID do banco de dados")

    # full-report
    p_fr = sub.add_parser("full-report", help="Relatório completo")
    p_fr.add_argument("--database-id", "-d", default="", help="ID do banco de dados para detalhar")

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    # Validações
    try:
        if args.subcommand == "list-pages":
            args.limit = validar_inteiro(args.limit, "limit", min_val=1, max_val=100)
            database_id = (args.database_id or os.environ.get(ENV_DATABASE_ID, "")).strip()
            if not database_id:
                print(
                    f"Erro: informe --database-id ou defina {ENV_DATABASE_ID}",
                    file=sys.stderr,
                )
                return 1
            args.database_id = database_id

        if args.subcommand == "search":
            validar_texto(args.query, "query", min_length=1, max_length=500)
            args.limit = validar_inteiro(args.limit, "limit", min_val=1, max_val=100)

        if args.subcommand == "create-page":
            validar_texto(args.title, "title", min_length=1, max_length=2000)

        if args.subcommand == "append-block":
            validar_texto(args.text, "text", min_length=1, max_length=2000)

    except ValidationError as e:
        return handle_validation_error(e)

    try:
        token = _get_token()
    except NotionAuthError as e:
        print(f"Erro de autenticação: {e}", file=sys.stderr)
        return 1

    fmt = OutputFormatter(getattr(args, "output_format", "human"))

    try:
        if args.subcommand == "list-databases":
            dbs = list_databases(token)
            if fmt.is_json():
                print_json(dbs)
            else:
                if not dbs:
                    print("Nenhum banco de dados encontrado.")
                else:
                    rows = [[d["id"], d["titulo"], d["editado_em"]] for d in dbs]
                    print_table(["ID", "Título", "Última edição"], rows)

        elif args.subcommand == "list-pages":
            pages = list_pages(token, args.database_id, limit=args.limit)
            if fmt.is_json():
                print_json(pages)
            else:
                if not pages:
                    print("Nenhuma página encontrada.")
                else:
                    rows = [[p["id"], p["titulo"], p["editado_em"]] for p in pages]
                    print_table(["ID", "Título", "Última edição"], rows)

        elif args.subcommand == "get-page":
            page = get_page(token, args.page_id)
            if fmt.is_json():
                print_json(page)
            else:
                print_key_value(page)

        elif args.subcommand == "create-page":
            result = create_page(
                token, args.database_id, args.title,
                content=args.content or None,
            )
            if fmt.is_json():
                print_json(result)
            else:
                print(f"✓ Página criada: {result['titulo']}")
                print(f"  ID : {result['id']}")
                print(f"  URL: {result['url']}")

        elif args.subcommand == "append-block":
            result = append_block(token, args.page_id, args.text, block_type=args.type)
            if fmt.is_json():
                print_json(result)
            else:
                print(f"✓ {result['total']} bloco(s) adicionado(s) à página {result['page_id']}")

        elif args.subcommand == "search":
            results = search(token, args.query, search_type=args.type, limit=args.limit)
            if fmt.is_json():
                print_json(results)
            else:
                if not results:
                    print(f"Nenhum resultado para '{args.query}'.")
                else:
                    rows = [[r["id"], r["titulo"], r["tipo"], r["editado_em"]] for r in results]
                    print_table(["ID", "Título", "Tipo", "Última edição"], rows)

        elif args.subcommand == "schema":
            schema = get_database_schema(token, args.database_id)
            if fmt.is_json():
                print_json(schema)
            else:
                print(f"Banco de dados: {schema['titulo']}")
                print(f"Total de propriedades: {schema['total_propriedades']}\n")
                rows = [[nome, tipo] for nome, tipo in schema["propriedades"].items()]
                print_table(["Propriedade", "Tipo"], rows)

        elif args.subcommand == "full-report":
            db_id = (args.database_id or os.environ.get(ENV_DATABASE_ID, "")).strip() or None
            report = full_report(token, database_id=db_id)
            if fmt.is_json():
                print_json(report)
            else:
                print(f"Relatório gerado em: {report['gerado_em']}")
                print(f"Total de bancos de dados: {report['total_databases']}\n")
                if report.get("database_detalhado"):
                    det = report["database_detalhado"]
                    print(f"Banco detalhadao: {det['titulo']} ({det['total_propriedades']} props)")
                if report.get("paginas_recentes"):
                    rows = [[p["titulo"], p["editado_em"]] for p in report["paginas_recentes"]]
                    print_table(["Título", "Última edição"], rows)

    except NotionAPIError as e:
        print(f"Erro na API Notion: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
