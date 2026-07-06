#!/usr/bin/env python3
"""
Meta Ads API Integration
Integração com a API de Marketing do Meta (Facebook/Instagram Ads).

Autenticação: token de acesso com permissões ads_read e ads_management.
Defina a variável de ambiente META_ACCESS_TOKEN antes de usar.
Defina META_AD_ACCOUNT_ID com o ID da conta de anúncios (ex: act_123456789).

Uso:
    python meta_ads_api.py campaigns [--status ACTIVE]
    python meta_ads_api.py campaign-insights <campaign_id> [--days 30]
    python meta_ads_api.py ad-performance <ad_account_id> [--days 7]
    python meta_ads_api.py create-campaign <nome> <objetivo> <budget_diario>
    python meta_ads_api.py pause-ad <ad_id>
    python meta_ads_api.py resume-ad <ad_id>
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from validators import (
    ValidationError,
    validar_inteiro,
    validar_float,
    validar_texto,
    handle_validation_error,
)

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

GRAPH_API_BASE = "https://graph.facebook.com/v18.0"
ENV_TOKEN = "META_ACCESS_TOKEN"
ENV_AD_ACCOUNT = "META_AD_ACCOUNT_ID"

# Objetivos de campanha válidos
OBJETIVOS_CAMPANHA = {
    "AWARENESS": "Reconhecimento de marca",
    "TRAFFIC": "Tráfego",
    "ENGAGEMENT": "Engajamento",
    "LEADS": "Geração de leads",
    "APP_PROMOTION": "Promoção de app",
    "SALES": "Vendas",
    "OUTCOME_AWARENESS": "Reconhecimento (novo)",
    "OUTCOME_TRAFFIC": "Tráfego (novo)",
    "OUTCOME_ENGAGEMENT": "Engajamento (novo)",
    "OUTCOME_LEADS": "Leads (novo)",
    "OUTCOME_APP_PROMOTION": "App (novo)",
    "OUTCOME_SALES": "Vendas (novo)",
}

# Status de campanhas
STATUS_VALIDOS = {"ACTIVE", "PAUSED", "DELETED", "ARCHIVED"}

# Campos padrão de campanha
CAMPOS_CAMPANHA = "id,name,status,objective,daily_budget,lifetime_budget,start_time,stop_time,created_time"

# Métricas de insights
METRICAS_INSIGHTS = [
    "impressions",
    "clicks",
    "ctr",
    "cpc",
    "cpm",
    "spend",
    "reach",
    "frequency",
    "actions",
    "cost_per_action_type",
    "video_play_actions",
    "website_purchase_roas",
]


# ---------------------------------------------------------------------------
# Exceções
# ---------------------------------------------------------------------------


class MetaAdsError(Exception):
    """Erro retornado pela API de Marketing do Meta."""

    def __init__(
        self, message: str, code: Optional[int] = None, subcode: Optional[int] = None
    ):
        super().__init__(message)
        self.code = code
        self.subcode = subcode

    def __str__(self):
        base = super().__str__()
        if self.code:
            return f"[{self.code}] {base}"
        return base


class MetaAdsAuthError(MetaAdsError):
    """Erro de autenticação (token inválido, expirado ou sem permissão)."""


# ---------------------------------------------------------------------------
# Cliente HTTP
# ---------------------------------------------------------------------------


def _handle_error_body(body: str, default_code: Optional[int] = None) -> MetaAdsError:
    """Parseia body de erro do Meta e retorna exceção apropriada."""
    try:
        err = json.loads(body)
        msg = err.get("error", {}).get("message", body)
        code = err.get("error", {}).get("code", default_code)
        subcode = err.get("error", {}).get("error_subcode")
        if code in (190, 102, 104, 200, 10):
            return MetaAdsAuthError(msg, code=code, subcode=subcode)
        return MetaAdsError(msg, code=code, subcode=subcode)
    except (json.JSONDecodeError, KeyError):
        return MetaAdsError(body, code=default_code)


def _get(url: str, params: Dict[str, Any]) -> Dict:
    """GET autenticado para a API do Meta."""
    query = urllib.parse.urlencode(params)
    full_url = f"{url}?{query}"

    try:
        with urllib.request.urlopen(full_url, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise _handle_error_body(e.read().decode("utf-8"), default_code=e.code)
    except urllib.error.URLError as e:
        raise MetaAdsError(f"Erro de conexão: {e.reason}")

    if "error" in data:
        raise _handle_error_body(json.dumps(data))

    return data


def _post(url: str, params: Dict[str, Any]) -> Dict:
    """POST autenticado para a API do Meta."""
    data = urllib.parse.urlencode(params).encode("utf-8")

    try:
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise _handle_error_body(e.read().decode("utf-8"), default_code=e.code)
    except urllib.error.URLError as e:
        raise MetaAdsError(f"Erro de conexão: {e.reason}")

    if "error" in result:
        raise _handle_error_body(json.dumps(result))

    return result


# ---------------------------------------------------------------------------
# Funções principais
# ---------------------------------------------------------------------------


def get_campaigns(
    ad_account_id: str,
    token: str,
    status: Optional[str] = None,
    limit: int = 25,
) -> List[Dict]:
    """
    Retorna campanhas da conta de anúncios.

    Args:
        ad_account_id: ID da conta (ex: act_123456789).
        token: Token de acesso.
        status: Filtrar por status ('ACTIVE', 'PAUSED', etc.). None = todos.
        limit: Número máximo de campanhas (1-100).

    Returns:
        Lista de campanhas com campos básicos.
    """
    params: Dict[str, Any] = {
        "fields": CAMPOS_CAMPANHA,
        "limit": max(1, min(limit, 100)),
        "access_token": token,
    }
    if status:
        params["effective_status"] = f'["{status}"]'

    url = f"{GRAPH_API_BASE}/{ad_account_id}/campaigns"
    result = _get(url, params)
    return result.get("data", [])


def get_campaign_insights(
    campaign_id: str,
    token: str,
    days: int = 30,
    metrics: Optional[List[str]] = None,
) -> Dict:
    """
    Retorna insights de uma campanha específica.

    Args:
        campaign_id: ID da campanha.
        token: Token de acesso.
        days: Período de análise em dias (padrão: 30).
        metrics: Lista de métricas. Padrão: métricas principais.

    Returns:
        Dicionário com insights da campanha.
    """
    if metrics is None:
        metrics = ["impressions", "clicks", "ctr", "cpc", "spend", "reach", "frequency"]

    end_date = datetime.now(tz=timezone.utc).date()
    start_date = end_date - timedelta(days=days - 1)

    params: Dict[str, Any] = {
        "fields": ",".join(metrics),
        "time_range": json.dumps(
            {
                "since": start_date.isoformat(),
                "until": end_date.isoformat(),
            }
        ),
        "access_token": token,
    }

    url = f"{GRAPH_API_BASE}/{campaign_id}/insights"
    result = _get(url, params)
    data = result.get("data", [])

    if not data:
        return {
            "campaign_id": campaign_id,
            "periodo": f"{start_date.isoformat()} a {end_date.isoformat()}",
            "dados": None,
            "mensagem": "Nenhum dado de insights disponível para o período.",
        }

    return {
        "campaign_id": campaign_id,
        "periodo": f"{start_date.isoformat()} a {end_date.isoformat()}",
        "dados": data[0] if len(data) == 1 else data,
    }


def get_ad_performance(
    ad_account_id: str,
    token: str,
    days: int = 7,
    level: str = "ad",
) -> List[Dict]:
    """
    Retorna performance de todos os anúncios da conta.

    Args:
        ad_account_id: ID da conta (ex: act_123456789).
        token: Token de acesso.
        days: Período de análise em dias.
        level: Nível de agregação ('ad', 'adset', 'campaign', 'account').

    Returns:
        Lista com performance de cada anúncio/conjunto/campanha.
    """
    end_date = datetime.now(tz=timezone.utc).date()
    start_date = end_date - timedelta(days=days - 1)

    metricas_performance = [
        "campaign_name",
        "adset_name",
        "ad_name",
        "impressions",
        "clicks",
        "ctr",
        "cpc",
        "cpm",
        "spend",
        "reach",
        "frequency",
        "actions",
        "cost_per_action_type",
    ]

    params: Dict[str, Any] = {
        "fields": ",".join(metricas_performance),
        "level": level,
        "time_range": json.dumps(
            {
                "since": start_date.isoformat(),
                "until": end_date.isoformat(),
            }
        ),
        "limit": 100,
        "access_token": token,
    }

    url = f"{GRAPH_API_BASE}/{ad_account_id}/insights"
    result = _get(url, params)
    return result.get("data", [])


def create_campaign(
    ad_account_id: str,
    token: str,
    name: str,
    objective: str,
    daily_budget: float,
    status: str = "PAUSED",
) -> Dict:
    """
    Cria uma nova campanha de anúncios.

    Args:
        ad_account_id: ID da conta (ex: act_123456789).
        token: Token de acesso.
        name: Nome da campanha.
        objective: Objetivo da campanha (ex: 'TRAFFIC', 'LEADS').
        daily_budget: Orçamento diário em centavos da moeda da conta (ex: 5000 = R$50,00).
        status: Status inicial ('ACTIVE' ou 'PAUSED'). Padrão: 'PAUSED'.

    Returns:
        Dicionário com ID e dados da campanha criada.
    """
    params: Dict[str, Any] = {
        "name": name,
        "objective": objective.upper(),
        "daily_budget": int(daily_budget),
        "status": status,
        "special_ad_categories": "[]",
        "access_token": token,
    }

    url = f"{GRAPH_API_BASE}/{ad_account_id}/campaigns"
    result = _post(url, params)

    campaign_id = result.get("id")
    if not campaign_id:
        raise MetaAdsError("Campanha criada mas ID não retornado.")

    return {
        "id": campaign_id,
        "name": name,
        "objective": objective.upper(),
        "daily_budget": int(daily_budget),
        "status": status,
    }


def _update_ad_status(ad_id: str, token: str, status: str) -> Dict:
    """Atualiza o status de um anúncio."""
    params: Dict[str, Any] = {
        "status": status,
        "access_token": token,
    }
    url = f"{GRAPH_API_BASE}/{ad_id}"
    result = _post(url, params)
    return {"id": ad_id, "status": status, "success": result.get("success", False)}


def pause_ad(ad_id: str, token: str) -> Dict:
    """
    Pausa um anúncio ativo.

    Args:
        ad_id: ID do anúncio.
        token: Token de acesso.

    Returns:
        Dicionário com confirmação.
    """
    return _update_ad_status(ad_id, token, "PAUSED")


def resume_ad(ad_id: str, token: str) -> Dict:
    """
    Reativa um anúncio pausado.

    Args:
        ad_id: ID do anúncio.
        token: Token de acesso.

    Returns:
        Dicionário com confirmação.
    """
    return _update_ad_status(ad_id, token, "ACTIVE")


# ---------------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------------


def get_token() -> str:
    """Lê o token da variável de ambiente META_ACCESS_TOKEN."""
    token = os.environ.get(ENV_TOKEN, "").strip()
    if not token:
        print(
            f"\n❌ Token não encontrado. Defina a variável de ambiente:\n"
            f"   export {ENV_TOKEN}='seu_token_aqui'\n",
            file=sys.stderr,
        )
        sys.exit(1)
    return token


def get_ad_account_id(cli_value: Optional[str] = None) -> str:
    """Retorna o ID da conta de anúncios do argumento CLI ou variável de ambiente."""
    account_id = cli_value or os.environ.get(ENV_AD_ACCOUNT, "").strip()
    if not account_id:
        print(
            f"\n❌ ID da conta de anúncios não configurado. Use --account ou defina:\n"
            f"   export {ENV_AD_ACCOUNT}='act_123456789'\n",
            file=sys.stderr,
        )
        sys.exit(1)
    # Garantir prefixo act_
    if not account_id.startswith("act_"):
        account_id = f"act_{account_id}"
    return account_id


def print_json(data: Any) -> None:
    """Imprime dados como JSON formatado."""
    print(json.dumps(data, indent=2, ensure_ascii=False))


def print_campaigns_table(campaigns: List[Dict]) -> None:
    """Imprime campanhas em formato de tabela."""
    if not campaigns:
        print("Nenhuma campanha encontrada.")
        return
    print(f"\n{'ID':<20} {'NOME':<40} {'STATUS':<10} {'OBJETIVO'}")
    print("-" * 90)
    for c in campaigns:
        camp_id = (c.get("id") or "")[:18]
        nome = (c.get("name") or "")[:38]
        status = c.get("status", "—")[:8]
        objetivo = c.get("objective", "—")[:20]
        print(f"{camp_id:<20} {nome:<40} {status:<10} {objetivo}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Meta Ads API — Marketing OS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Variáveis de ambiente obrigatórias:\n"
            f"  {ENV_TOKEN}       Token de acesso com ads_read/ads_management\n"
            f"  {ENV_AD_ACCOUNT}    ID da conta (ex: act_123456789)\n\n"
            "Exemplos:\n"
            "  python meta_ads_api.py campaigns --status ACTIVE\n"
            "  python meta_ads_api.py campaign-insights 120200000123 --days 14\n"
            "  python meta_ads_api.py create-campaign 'Campanha Leads' LEADS 5000\n"
        ),
    )

    parser.add_argument("--account", help=f"ID da conta (substitui {ENV_AD_ACCOUNT})")

    sub = parser.add_subparsers(dest="comando", required=True)

    # campaigns
    p_c = sub.add_parser("campaigns", help="Lista campanhas da conta")
    p_c.add_argument(
        "--status", choices=list(STATUS_VALIDOS), help="Filtrar por status"
    )
    p_c.add_argument(
        "--limit", type=int, default=25, help="Máximo de campanhas (padrão: 25)"
    )
    p_c.add_argument("--json", action="store_true", help="Saída em JSON")

    # campaign-insights
    p_ci = sub.add_parser("campaign-insights", help="Insights de uma campanha")
    p_ci.add_argument("campaign_id", help="ID da campanha")
    p_ci.add_argument(
        "--days", type=int, default=30, help="Dias retroativos (padrão: 30)"
    )
    p_ci.add_argument("--json", action="store_true")

    # ad-performance
    p_ap = sub.add_parser("ad-performance", help="Performance de anúncios")
    p_ap.add_argument(
        "--days", type=int, default=7, help="Dias retroativos (padrão: 7)"
    )
    p_ap.add_argument(
        "--level", default="ad", choices=["ad", "adset", "campaign", "account"]
    )
    p_ap.add_argument("--json", action="store_true")

    # create-campaign
    p_cc = sub.add_parser("create-campaign", help="Cria uma nova campanha")
    p_cc.add_argument("nome", help="Nome da campanha")
    p_cc.add_argument(
        "objetivo", choices=list(OBJETIVOS_CAMPANHA.keys()), help="Objetivo da campanha"
    )
    p_cc.add_argument(
        "budget_diario",
        type=float,
        help="Orçamento diário em centavos (5000 = R$50,00)",
    )
    p_cc.add_argument("--status", default="PAUSED", choices=["ACTIVE", "PAUSED"])

    # pause-ad
    p_pa = sub.add_parser("pause-ad", help="Pausa um anúncio")
    p_pa.add_argument("ad_id", help="ID do anúncio")

    # resume-ad
    p_ra = sub.add_parser("resume-ad", help="Reativa um anúncio pausado")
    p_ra.add_argument("ad_id", help="ID do anúncio")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    token = get_token()

    try:
        if args.comando == "campaigns":
            account_id = get_ad_account_id(getattr(args, "account", None))
            limit = validar_inteiro(args.limit, campo="limit", min_val=1, max_val=100)
            campaigns = get_campaigns(
                account_id, token, status=getattr(args, "status", None), limit=limit
            )
            if getattr(args, "json", False):
                print_json(campaigns)
            else:
                print(f"\n📢 CAMPANHAS — {account_id} ({len(campaigns)} resultados)")
                print_campaigns_table(campaigns)

        elif args.comando == "campaign-insights":
            validar_texto(args.campaign_id, campo="campaign_id", max_len=50)
            days = validar_inteiro(args.days, campo="days", min_val=1, max_val=365)
            data = get_campaign_insights(args.campaign_id, token, days=days)
            print_json(data)

        elif args.comando == "ad-performance":
            account_id = get_ad_account_id(getattr(args, "account", None))
            days = validar_inteiro(args.days, campo="days", min_val=1, max_val=365)
            data = get_ad_performance(account_id, token, days=days, level=args.level)
            if getattr(args, "json", False):
                print_json(data)
            else:
                print(
                    f"\n📊 PERFORMANCE — {account_id} (últimos {days} dias, nível: {args.level})"
                )
                print(f"   {len(data)} registros encontrados")
                if data:
                    print_json(data[:5])

        elif args.comando == "create-campaign":
            account_id = get_ad_account_id(getattr(args, "account", None))
            nome = validar_texto(args.nome, campo="nome", max_len=256)
            budget = validar_float(
                args.budget_diario,
                campo="budget_diario",
                min_val=100.0,
                max_val=10_000_000.0,
            )
            result = create_campaign(
                account_id, token, nome, args.objetivo, budget, status=args.status
            )
            print(f"\n✅ Campanha criada com sucesso!")
            print(f"   ID: {result['id']}")
            print(f"   Nome: {result['name']}")
            print(f"   Objetivo: {result['objective']}")
            print(f"   Status: {result['status']}")
            print_json(result)

        elif args.comando == "pause-ad":
            validar_texto(args.ad_id, campo="ad_id", max_len=50)
            result = pause_ad(args.ad_id, token)
            print(f"\n⏸ Anúncio {args.ad_id} pausado. Sucesso: {result.get('success')}")
            print_json(result)

        elif args.comando == "resume-ad":
            validar_texto(args.ad_id, campo="ad_id", max_len=50)
            result = resume_ad(args.ad_id, token)
            print(
                f"\n▶ Anúncio {args.ad_id} reativado. Sucesso: {result.get('success')}"
            )
            print_json(result)

    except ValidationError as e:
        handle_validation_error(e)
    except MetaAdsAuthError as e:
        print(f"\n❌ Erro de autenticação: {e}", file=sys.stderr)
        print(
            f"Verifique se o token em {ENV_TOKEN} é válido e tem as permissões necessárias.",
            file=sys.stderr,
        )
        sys.exit(1)
    except MetaAdsError as e:
        print(f"\n❌ Erro da API do Meta Ads: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
