#!/usr/bin/env python3
"""
Google Search Console Analyzer
Integração com a API do Google Search Console para análise de performance SEO.

Autenticação: Service Account via arquivo JSON de credenciais.
Defina a variável de ambiente GSC_CREDENTIALS_FILE com o caminho para o arquivo.
Alternativamente, defina GSC_SERVICE_ACCOUNT_JSON com o JSON completo das credenciais.

Uso:
    python gsc_analyzer.py queries <site_url> [--days 30]
    python gsc_analyzer.py top-pages <site_url> [--days 30] [--limit 20]
    python gsc_analyzer.py ctr-opportunities <site_url> [--days 30]
    python gsc_analyzer.py position-changes <site_url> [--days 30] [--compare 30]
    python gsc_analyzer.py full-report <site_url> [--days 30]
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from validators import ValidationError, validar_inteiro, validar_texto, validar_url, handle_validation_error

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

GSC_API_BASE = "https://searchconsole.googleapis.com/webmasters/v3"
OAUTH_TOKEN_URL = "https://oauth2.googleapis.com/token"

ENV_CREDENTIALS_FILE = "GSC_CREDENTIALS_FILE"
ENV_CREDENTIALS_JSON = "GSC_SERVICE_ACCOUNT_JSON"

# Dimensões disponíveis na API
DIMENSOES_VALIDAS = {"query", "page", "country", "device", "searchAppearance", "date"}

# Tipos de busca
TIPOS_BUSCA = {"web", "news", "image", "video", "googleNews"}

# Limites
MAX_ROWS = 25000
DEFAULT_ROWS = 1000


# ---------------------------------------------------------------------------
# Exceções
# ---------------------------------------------------------------------------

class GSCError(Exception):
    """Erro da API do Google Search Console."""

    def __init__(self, message: str, status: Optional[int] = None):
        super().__init__(message)
        self.status = status

    def __str__(self):
        base = super().__str__()
        if self.status:
            return f"[HTTP {self.status}] {base}"
        return base


class GSCAuthError(GSCError):
    """Erro de autenticação com o Google Search Console."""
    pass


# ---------------------------------------------------------------------------
# Autenticação (Service Account via JWT)
# ---------------------------------------------------------------------------

def _load_credentials() -> Dict:
    """Carrega credenciais da Service Account a partir de variável de ambiente ou arquivo."""
    # Tentar JSON inline
    json_inline = os.environ.get(ENV_CREDENTIALS_JSON, "").strip()
    if json_inline:
        try:
            return json.loads(json_inline)
        except json.JSONDecodeError as e:
            raise GSCAuthError(f"GSC_SERVICE_ACCOUNT_JSON inválido: {e}")

    # Tentar arquivo
    creds_file = os.environ.get(ENV_CREDENTIALS_FILE, "").strip()
    if creds_file:
        if not os.path.exists(creds_file):
            raise GSCAuthError(f"Arquivo de credenciais não encontrado: '{creds_file}'")
        with open(creds_file, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError as e:
                raise GSCAuthError(f"Arquivo de credenciais inválido: {e}")

    raise GSCAuthError(
        f"Credenciais não configuradas. Defina:\n"
        f"  {ENV_CREDENTIALS_FILE}=/caminho/para/service-account.json\n"
        f"  ou {ENV_CREDENTIALS_JSON}='{{...json...}}'"
    )


def _get_access_token(credentials: Dict) -> str:
    """
    Obtém um access token OAuth 2.0 para Service Account via JWT.
    Usa apenas a biblioteca padrão (sem google-auth).
    """
    import base64
    import hashlib
    import hmac
    import struct
    import time
    import urllib.error
    import urllib.parse
    import urllib.request

    required_fields = ["private_key", "client_email", "token_uri"]
    for field in required_fields:
        if field not in credentials:
            raise GSCAuthError(
                f"Campo obrigatório ausente nas credenciais: '{field}'. "
                "Certifique-se de usar um arquivo Service Account válido."
            )

    # Verificar se tem RSA disponível (necessário para assinar JWT)
    try:
        import ssl
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import padding
        _HAS_CRYPTOGRAPHY = True
    except ImportError:
        _HAS_CRYPTOGRAPHY = False

    if not _HAS_CRYPTOGRAPHY:
        raise GSCAuthError(
            "A biblioteca 'cryptography' é necessária para autenticação com Service Account. "
            "Instale com: pip install cryptography"
        )

    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding

    now = int(time.time())
    claim_set = {
        "iss": credentials["client_email"],
        "scope": "https://www.googleapis.com/auth/webmasters.readonly",
        "aud": credentials.get("token_uri", OAUTH_TOKEN_URL),
        "exp": now + 3600,
        "iat": now,
    }

    def b64url(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")

    header = b64url(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
    payload = b64url(json.dumps(claim_set).encode())
    signing_input = f"{header}.{payload}".encode("ascii")

    private_key_pem = credentials["private_key"].encode("utf-8")
    private_key = serialization.load_pem_private_key(private_key_pem, password=None)
    signature = private_key.sign(signing_input, padding.PKCS1v15(), hashes.SHA256())
    jwt_token = f"{header}.{payload}.{b64url(signature)}"

    token_url = credentials.get("token_uri", OAUTH_TOKEN_URL)
    post_data = urllib.parse.urlencode({
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": jwt_token,
    }).encode("utf-8")

    try:
        req = urllib.request.Request(token_url, data=post_data, method="POST")
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        raise GSCAuthError(f"Falha ao obter token OAuth: {body}")
    except urllib.error.URLError as e:
        raise GSCAuthError(f"Erro de conexão ao obter token: {e.reason}")

    if "access_token" not in result:
        raise GSCAuthError(f"Token não retornado. Resposta: {result}")

    return result["access_token"]


# ---------------------------------------------------------------------------
# Cliente HTTP
# ---------------------------------------------------------------------------

def _api_get(url: str, token: str, params: Optional[Dict] = None) -> Dict:
    """Faz um GET autenticado para a API do GSC."""
    import urllib.error
    import urllib.parse
    import urllib.request

    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"

    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        if e.code == 401:
            raise GSCAuthError(f"Token inválido ou expirado: {body}", status=401)
        try:
            err = json.loads(body)
            msg = err.get("error", {}).get("message", body)
        except json.JSONDecodeError:
            msg = body
        raise GSCError(msg, status=e.code)
    except urllib.error.URLError as e:
        raise GSCError(f"Erro de conexão: {e.reason}")


def _api_post(url: str, token: str, body: Dict) -> Dict:
    """Faz um POST autenticado para a API do GSC."""
    import urllib.error
    import urllib.request

    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        if e.code == 401:
            raise GSCAuthError(f"Token inválido ou expirado: {body}", status=401)
        try:
            err = json.loads(body)
            msg = err.get("error", {}).get("message", body)
        except json.JSONDecodeError:
            msg = body
        raise GSCError(msg, status=e.code)
    except urllib.error.URLError as e:
        raise GSCError(f"Erro de conexão: {e.reason}")


# ---------------------------------------------------------------------------
# Funções de análise
# ---------------------------------------------------------------------------

def _date_range(days: int) -> tuple:
    """Retorna (start_date, end_date) como strings YYYY-MM-DD."""
    end = datetime.now(tz=timezone.utc).date() - timedelta(days=3)  # GSC tem delay de ~3 dias
    start = end - timedelta(days=days - 1)
    return start.isoformat(), end.isoformat()


def _search_analytics(
    site_url: str,
    token: str,
    dimensions: List[str],
    days: int = 30,
    row_limit: int = DEFAULT_ROWS,
    search_type: str = "web",
    filters: Optional[List[Dict]] = None,
) -> List[Dict]:
    """
    Consulta a API Search Analytics do GSC.

    Returns:
        Lista de linhas com métricas (clicks, impressions, ctr, position + dimensões).
    """
    start_date, end_date = _date_range(days)
    encoded_site = _encode_site_url(site_url)
    url = f"{GSC_API_BASE}/sites/{encoded_site}/searchAnalytics/query"

    body: Dict[str, Any] = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": dimensions,
        "searchType": search_type,
        "rowLimit": min(row_limit, MAX_ROWS),
    }
    if filters:
        body["dimensionFilterGroups"] = [{"filters": filters}]

    result = _api_post(url, token, body)
    return result.get("rows", [])


def _encode_site_url(site_url: str) -> str:
    """Codifica a URL do site para uso no path da API."""
    import urllib.parse
    return urllib.parse.quote(site_url, safe="")


def get_search_queries(
    site_url: str,
    token: str,
    days: int = 30,
    limit: int = 100,
) -> List[Dict]:
    """
    Retorna as principais queries de busca orgânica.

    Args:
        site_url: URL do site no GSC (ex: https://example.com ou sc-domain:example.com).
        token: Access token OAuth 2.0.
        days: Número de dias retroativos (padrão: 30).
        limit: Número máximo de queries (padrão: 100).

    Returns:
        Lista de dicionários com: query, clicks, impressions, ctr, position.
    """
    rows = _search_analytics(site_url, token, dimensions=["query"], days=days, row_limit=limit)
    return [
        {
            "query": row["keys"][0],
            "clicks": row.get("clicks", 0),
            "impressions": row.get("impressions", 0),
            "ctr": round(row.get("ctr", 0) * 100, 2),
            "position": round(row.get("position", 0), 1),
        }
        for row in rows
    ]


def get_top_pages(
    site_url: str,
    token: str,
    days: int = 30,
    limit: int = 50,
) -> List[Dict]:
    """
    Retorna as páginas com melhor performance de busca orgânica.

    Args:
        site_url: URL do site no GSC.
        token: Access token OAuth 2.0.
        days: Número de dias retroativos (padrão: 30).
        limit: Número máximo de páginas (padrão: 50).

    Returns:
        Lista de dicionários com: page, clicks, impressions, ctr, position.
    """
    rows = _search_analytics(site_url, token, dimensions=["page"], days=days, row_limit=limit)
    return [
        {
            "page": row["keys"][0],
            "clicks": row.get("clicks", 0),
            "impressions": row.get("impressions", 0),
            "ctr": round(row.get("ctr", 0) * 100, 2),
            "position": round(row.get("position", 0), 1),
        }
        for row in rows
    ]


def get_ctr_opportunities(
    site_url: str,
    token: str,
    days: int = 30,
    min_impressions: int = 100,
    max_ctr: float = 3.0,
    max_position: float = 20.0,
) -> List[Dict]:
    """
    Identifica queries com alto volume de impressões mas baixo CTR (oportunidades).

    Args:
        site_url: URL do site no GSC.
        token: Access token OAuth 2.0.
        days: Número de dias retroativos.
        min_impressions: Mínimo de impressões para considerar a query.
        max_ctr: CTR máximo (%) para considerar como oportunidade.
        max_position: Posição máxima para considerar a query.

    Returns:
        Lista de oportunidades ordenadas por impressões (maior primeiro).
    """
    rows = _search_analytics(site_url, token, dimensions=["query"], days=days, row_limit=MAX_ROWS)

    oportunidades = []
    for row in rows:
        impressions = row.get("impressions", 0)
        ctr = row.get("ctr", 0) * 100
        position = row.get("position", 99)

        if impressions >= min_impressions and ctr <= max_ctr and position <= max_position:
            oportunidades.append({
                "query": row["keys"][0],
                "impressions": impressions,
                "clicks": row.get("clicks", 0),
                "ctr": round(ctr, 2),
                "position": round(position, 1),
                "ctr_potencial": round(impressions * 0.05, 0),  # Estimativa com CTR de 5%
            })

    return sorted(oportunidades, key=lambda x: x["impressions"], reverse=True)


def get_position_changes(
    site_url: str,
    token: str,
    days: int = 30,
    compare_days: int = 30,
    limit: int = 50,
) -> Dict:
    """
    Compara posições médias entre dois períodos para identificar variações.

    Args:
        site_url: URL do site no GSC.
        token: Access token OAuth 2.0.
        days: Período atual (últimos N dias).
        compare_days: Período de comparação (N dias anteriores ao período atual).
        limit: Número máximo de queries analisadas.

    Returns:
        Dicionário com queries que subiram, desceram e novos.
    """
    # Período atual
    rows_atual = _search_analytics(site_url, token, dimensions=["query"], days=days, row_limit=limit)

    # Período anterior (deslocado)
    end_anterior = datetime.now(tz=timezone.utc).date() - timedelta(days=3 + days)
    start_anterior = end_anterior - timedelta(days=compare_days - 1)

    encoded_site = _encode_site_url(site_url)
    url = f"{GSC_API_BASE}/sites/{encoded_site}/searchAnalytics/query"

    body_anterior = {
        "startDate": start_anterior.isoformat(),
        "endDate": end_anterior.isoformat(),
        "dimensions": ["query"],
        "searchType": "web",
        "rowLimit": limit,
    }
    result_anterior = _api_post(url, token, body_anterior)
    rows_anterior = result_anterior.get("rows", [])

    # Construir dicionário do período anterior
    dict_anterior = {
        row["keys"][0]: round(row.get("position", 99), 1)
        for row in rows_anterior
    }

    subiram = []
    desceram = []
    novos = []

    for row in rows_atual:
        query = row["keys"][0]
        pos_atual = round(row.get("position", 99), 1)
        pos_anterior = dict_anterior.get(query)

        if pos_anterior is None:
            novos.append({"query": query, "position": pos_atual})
        elif pos_atual < pos_anterior:
            subiram.append({
                "query": query,
                "position_atual": pos_atual,
                "position_anterior": pos_anterior,
                "variacao": round(pos_anterior - pos_atual, 1),
            })
        elif pos_atual > pos_anterior:
            desceram.append({
                "query": query,
                "position_atual": pos_atual,
                "position_anterior": pos_anterior,
                "variacao": round(pos_atual - pos_anterior, 1),
            })

    subiram.sort(key=lambda x: x["variacao"], reverse=True)
    desceram.sort(key=lambda x: x["variacao"], reverse=True)

    return {
        "periodo_atual": f"últimos {days} dias",
        "periodo_anterior": f"{days}-{days + compare_days} dias atrás",
        "subiram": subiram[:20],
        "desceram": desceram[:20],
        "novos": novos[:20],
        "resumo": {
            "total_subiram": len(subiram),
            "total_desceram": len(desceram),
            "total_novos": len(novos),
        },
    }


# ---------------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------------

def get_credentials_and_token() -> str:
    """Carrega credenciais e retorna access token."""
    credentials = _load_credentials()
    return _get_access_token(credentials)


def print_json(data: Any) -> None:
    """Imprime dados como JSON formatado."""
    print(json.dumps(data, indent=2, ensure_ascii=False))


def print_queries_table(queries: List[Dict]) -> None:
    """Imprime queries em formato de tabela."""
    if not queries:
        print("Nenhuma query encontrada.")
        return
    print(f"\n{'QUERY':<50} {'CLICKS':>8} {'IMPRESS':>8} {'CTR':>6} {'POS':>6}")
    print("-" * 82)
    for q in queries[:50]:
        query = q["query"][:48]
        print(f"{query:<50} {q['clicks']:>8} {q['impressions']:>8} {q['ctr']:>5.1f}% {q['position']:>6.1f}")


def print_pages_table(pages: List[Dict]) -> None:
    """Imprime páginas em formato de tabela."""
    if not pages:
        print("Nenhuma página encontrada.")
        return
    print(f"\n{'PÁGINA':<60} {'CLICKS':>8} {'POS':>6}")
    print("-" * 78)
    for p in pages[:30]:
        page = p["page"][-58:] if len(p["page"]) > 58 else p["page"]
        print(f"{page:<60} {p['clicks']:>8} {p['position']:>6.1f}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Google Search Console Analyzer — Marketing OS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Variáveis de ambiente (uma delas é obrigatória):\n"
            f"  {ENV_CREDENTIALS_FILE}   Caminho para service-account.json\n"
            f"  {ENV_CREDENTIALS_JSON}   JSON das credenciais inline\n\n"
            "Exemplos:\n"
            "  python gsc_analyzer.py queries https://example.com --days 30\n"
            "  python gsc_analyzer.py ctr-opportunities https://example.com\n"
            "  python gsc_analyzer.py full-report https://example.com\n"
        ),
    )
    sub = parser.add_subparsers(dest="comando", required=True)

    # queries
    p_q = sub.add_parser("queries", help="Principais queries de busca")
    p_q.add_argument("site_url", help="URL do site (https://example.com)")
    p_q.add_argument("--days", type=int, default=30, help="Dias retroativos (padrão: 30)")
    p_q.add_argument("--limit", type=int, default=100, help="Máximo de queries (padrão: 100)")
    p_q.add_argument("--json", action="store_true", help="Saída em JSON")

    # top-pages
    p_tp = sub.add_parser("top-pages", help="Páginas com melhor performance")
    p_tp.add_argument("site_url", help="URL do site")
    p_tp.add_argument("--days", type=int, default=30)
    p_tp.add_argument("--limit", type=int, default=50)
    p_tp.add_argument("--json", action="store_true")

    # ctr-opportunities
    p_ctr = sub.add_parser("ctr-opportunities", help="Oportunidades de CTR")
    p_ctr.add_argument("site_url", help="URL do site")
    p_ctr.add_argument("--days", type=int, default=30)
    p_ctr.add_argument("--min-impressions", type=int, default=100)
    p_ctr.add_argument("--max-ctr", type=float, default=3.0)
    p_ctr.add_argument("--json", action="store_true")

    # position-changes
    p_pc = sub.add_parser("position-changes", help="Variações de posição")
    p_pc.add_argument("site_url", help="URL do site")
    p_pc.add_argument("--days", type=int, default=30)
    p_pc.add_argument("--compare", type=int, default=30, help="Período de comparação (dias)")
    p_pc.add_argument("--json", action="store_true")

    # full-report
    p_fr = sub.add_parser("full-report", help="Relatório completo")
    p_fr.add_argument("site_url", help="URL do site")
    p_fr.add_argument("--days", type=int, default=30)
    p_fr.add_argument("--output", help="Arquivo de saída (JSON)")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        validar_texto(args.site_url, campo="site_url", max_len=500)
        days = validar_inteiro(getattr(args, "days", 30), campo="days", min_val=1, max_val=365)
    except ValidationError as e:
        handle_validation_error(e)
        return

    try:
        token = get_credentials_and_token()
    except GSCAuthError as e:
        print(f"\n❌ Erro de autenticação: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        if args.comando == "queries":
            limit = validar_inteiro(args.limit, campo="limit", min_val=1, max_val=MAX_ROWS)
            data = get_search_queries(args.site_url, token, days=days, limit=limit)
            if getattr(args, "json", False):
                print_json(data)
            else:
                print(f"\n🔍 TOP QUERIES — Últimos {days} dias ({len(data)} resultados)")
                print_queries_table(data)

        elif args.comando == "top-pages":
            limit = validar_inteiro(args.limit, campo="limit", min_val=1, max_val=MAX_ROWS)
            data = get_top_pages(args.site_url, token, days=days, limit=limit)
            if getattr(args, "json", False):
                print_json(data)
            else:
                print(f"\n📄 TOP PÁGINAS — Últimos {days} dias ({len(data)} resultados)")
                print_pages_table(data)

        elif args.comando == "ctr-opportunities":
            min_imp = validar_inteiro(args.min_impressions, campo="min_impressions", min_val=1, max_val=1000000)
            data = get_ctr_opportunities(
                args.site_url, token, days=days,
                min_impressions=min_imp,
                max_ctr=args.max_ctr,
            )
            if getattr(args, "json", False):
                print_json(data)
            else:
                print(f"\n🎯 OPORTUNIDADES DE CTR — {len(data)} encontradas")
                print_queries_table(data)

        elif args.comando == "position-changes":
            compare = validar_inteiro(args.compare, campo="compare", min_val=1, max_val=365)
            data = get_position_changes(args.site_url, token, days=days, compare_days=compare)
            if getattr(args, "json", False):
                print_json(data)
            else:
                print(f"\n📈 VARIAÇÕES DE POSIÇÃO")
                print(f"   ↑ Subiram: {data['resumo']['total_subiram']}")
                print(f"   ↓ Desceram: {data['resumo']['total_desceram']}")
                print(f"   ★ Novas: {data['resumo']['total_novos']}")

        elif args.comando == "full-report":
            print(f"\n⏳ Gerando relatório completo para {args.site_url}...")
            queries = get_search_queries(args.site_url, token, days=days)
            pages = get_top_pages(args.site_url, token, days=days)
            opportunities = get_ctr_opportunities(args.site_url, token, days=days)
            changes = get_position_changes(args.site_url, token, days=days)

            report = {
                "site": args.site_url,
                "periodo": f"últimos {days} dias",
                "gerado_em": datetime.now(tz=timezone.utc).isoformat(),
                "queries": queries,
                "top_pages": pages,
                "oportunidades_ctr": opportunities,
                "variacao_posicao": changes,
            }

            if getattr(args, "output", None):
                with open(args.output, "w", encoding="utf-8") as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
                print(f"✅ Relatório salvo em: {args.output}")
            else:
                print_json(report)

    except ValidationError as e:
        handle_validation_error(e)
    except GSCAuthError as e:
        print(f"\n❌ Erro de autenticação: {e}", file=sys.stderr)
        sys.exit(1)
    except GSCError as e:
        print(f"\n❌ Erro da API do GSC: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
