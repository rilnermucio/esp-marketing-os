#!/usr/bin/env python3
"""
YouTube Analytics API Integration
Integração com YouTube Analytics e Data API v3 para análise de performance de canal.

Autenticação: Service Account ou OAuth 2.0.
  - Service Account: defina GSC_CREDENTIALS_FILE ou GSC_SERVICE_ACCOUNT_JSON
    (reutiliza as credenciais do Google usadas no GSC)
  - Ou defina YT_CREDENTIALS_FILE / YT_SERVICE_ACCOUNT_JSON para credenciais dedicadas

Uso:
    python youtube_analytics.py channel [--days 30]
    python youtube_analytics.py videos [--days 30] [--limit 20]
    python youtube_analytics.py top-videos [--days 30] [--limit 10]
    python youtube_analytics.py demographics [--days 30]
    python youtube_analytics.py traffic-sources [--days 30]
    python youtube_analytics.py full-report [--days 30] [--output relatorio.json]
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple

from output_formatter import (
    add_output_args,
    OutputFormatter,
    print_json,
    print_table,
    print_key_value,
)
from validators import (
    ValidationError,
    validar_inteiro,
    handle_validation_error,
)

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

YT_ANALYTICS_BASE = "https://youtubeanalytics.googleapis.com/v2"
YT_DATA_BASE = "https://www.googleapis.com/youtube/v3"
OAUTH_TOKEN_URL = "https://oauth2.googleapis.com/token"

# Variáveis de ambiente (dedicadas para YouTube ou reutilizando as do GSC)
ENV_CREDENTIALS_FILE = "YT_CREDENTIALS_FILE"
ENV_CREDENTIALS_JSON = "YT_SERVICE_ACCOUNT_JSON"
ENV_CREDENTIALS_FILE_FALLBACK = "GSC_CREDENTIALS_FILE"
ENV_CREDENTIALS_JSON_FALLBACK = "GSC_SERVICE_ACCOUNT_JSON"

# Escopo necessário para YouTube Analytics
YT_ANALYTICS_SCOPE = "https://www.googleapis.com/auth/yt-analytics.readonly"
YT_DATA_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"

# Dimensões e métricas disponíveis
METRICAS_VIDEO = [
    "views",
    "estimatedMinutesWatched",
    "averageViewDuration",
    "averageViewPercentage",
    "likes",
    "dislikes",
    "comments",
    "shares",
    "subscribersGained",
    "subscribersLost",
]

METRICAS_CANAL = [
    "views",
    "estimatedMinutesWatched",
    "averageViewDuration",
    "likes",
    "comments",
    "shares",
    "subscribersGained",
    "subscribersLost",
    "videosAddedToPlaylists",
]

DIMENSOES_DEMOGRAFICAS = ["ageGroup", "gender"]
DIMENSOES_TRAFEGO = ["insightTrafficSourceType"]


# ---------------------------------------------------------------------------
# Exceções
# ---------------------------------------------------------------------------


class YouTubeAnalyticsError(Exception):
    """Erro da API do YouTube Analytics."""

    def __init__(self, message: str, status: Optional[int] = None):
        super().__init__(message)
        self.status = status

    def __str__(self) -> str:
        base = super().__str__()
        return f"[HTTP {self.status}] {base}" if self.status else base


class YouTubeAuthError(YouTubeAnalyticsError):
    """Erro de autenticação com as APIs do Google."""


# ---------------------------------------------------------------------------
# Autenticação (Service Account via JWT — mesma lógica do gsc_analyzer)
# ---------------------------------------------------------------------------


def _load_credentials() -> Dict:
    """Carrega credenciais de variáveis de ambiente (YouTube ou GSC como fallback)."""
    for env_json, env_file in [
        (ENV_CREDENTIALS_JSON, ENV_CREDENTIALS_FILE),
        (ENV_CREDENTIALS_JSON_FALLBACK, ENV_CREDENTIALS_FILE_FALLBACK),
    ]:
        json_inline = os.environ.get(env_json, "").strip()
        if json_inline:
            try:
                return json.loads(json_inline)
            except json.JSONDecodeError as e:
                raise YouTubeAuthError(f"Credenciais JSON inválidas ({env_json}): {e}")

        creds_file = os.environ.get(env_file, "").strip()
        if creds_file:
            if not os.path.exists(creds_file):
                raise YouTubeAuthError(
                    f"Arquivo de credenciais não encontrado: '{creds_file}'"
                )
            with open(creds_file, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError as e:
                    raise YouTubeAuthError(f"Arquivo de credenciais inválido: {e}")

    raise YouTubeAuthError(
        "Credenciais não configuradas. Defina uma das opções:\n"
        f"  {ENV_CREDENTIALS_FILE}=/caminho/para/service-account.json\n"
        f"  {ENV_CREDENTIALS_JSON}='{{...json...}}'\n"
        f"  (ou as equivalentes do GSC: {ENV_CREDENTIALS_FILE_FALLBACK} / {ENV_CREDENTIALS_JSON_FALLBACK})"
    )


def _get_access_token(credentials: Dict, scope: str) -> str:
    """Obtém access token OAuth 2.0 via JWT para Service Account."""
    import base64
    import time
    import urllib.error
    import urllib.parse
    import urllib.request

    required = ["private_key", "client_email", "token_uri"]
    for field in required:
        if field not in credentials:
            raise YouTubeAuthError(
                f"Campo ausente nas credenciais: '{field}'. Use um arquivo Service Account válido."
            )

    try:
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import padding
    except ImportError:
        raise YouTubeAuthError(
            "Biblioteca 'cryptography' necessária. Instale com: pip install cryptography"
        )

    now = int(time.time())
    claim_set = {
        "iss": credentials["client_email"],
        "scope": scope,
        "aud": credentials.get("token_uri", OAUTH_TOKEN_URL),
        "exp": now + 3600,
        "iat": now,
    }

    def b64url(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")

    header = b64url(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
    payload = b64url(json.dumps(claim_set).encode())
    signing_input = f"{header}.{payload}".encode("ascii")

    private_key = serialization.load_pem_private_key(
        credentials["private_key"].encode("utf-8"), password=None
    )
    signature = private_key.sign(signing_input, padding.PKCS1v15(), hashes.SHA256())
    jwt_token = f"{header}.{payload}.{b64url(signature)}"

    post_data = urllib.parse.urlencode(
        {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": jwt_token,
        }
    ).encode("utf-8")

    try:
        req = urllib.request.Request(
            credentials.get("token_uri", OAUTH_TOKEN_URL), data=post_data, method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise YouTubeAuthError(
            f"Falha ao obter token OAuth: {e.read().decode('utf-8')}"
        )
    except urllib.error.URLError as e:
        raise YouTubeAuthError(f"Erro de conexão ao obter token: {e.reason}")

    if "access_token" not in result:
        raise YouTubeAuthError(f"Token não retornado: {result}")

    return result["access_token"]


# ---------------------------------------------------------------------------
# Cliente HTTP
# ---------------------------------------------------------------------------


def _api_get(url: str, token: str, params: Optional[Dict] = None) -> Dict:
    """GET autenticado para APIs do Google."""
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
            raise YouTubeAuthError(f"Token inválido ou expirado: {body}", status=401)
        try:
            err = json.loads(body)
            msg = err.get("error", {}).get("message", body)
        except json.JSONDecodeError:
            msg = body
        raise YouTubeAnalyticsError(msg, status=e.code)
    except urllib.error.URLError as e:
        raise YouTubeAnalyticsError(f"Erro de conexão: {e.reason}")


# ---------------------------------------------------------------------------
# Utilitários de data
# ---------------------------------------------------------------------------


def _date_range(days: int) -> Tuple[str, str]:
    """Retorna (start_date, end_date) como YYYY-MM-DD."""
    end = datetime.now(tz=timezone.utc).date() - timedelta(
        days=2
    )  # delay de ~2 dias no YT
    start = end - timedelta(days=days - 1)
    return start.isoformat(), end.isoformat()


def _get_channel_id(token: str) -> str:
    """Retorna o ID do canal autenticado."""
    params = {"part": "id", "mine": "true"}
    result = _api_get(f"{YT_DATA_BASE}/channels", token, params)
    items = result.get("items", [])
    if not items:
        raise YouTubeAnalyticsError(
            "Nenhum canal encontrado para as credenciais fornecidas."
        )
    return items[0]["id"]


# ---------------------------------------------------------------------------
# Funções principais
# ---------------------------------------------------------------------------


def get_channel_stats(
    token: str,
    days: int = 30,
    channel_id: str = "MINE",
) -> Dict:
    """
    Retorna métricas gerais do canal para o período especificado.

    Args:
        token: Access token OAuth 2.0.
        days: Número de dias retroativos (padrão: 30).
        channel_id: ID do canal ('MINE' para o canal autenticado).

    Returns:
        Dicionário com métricas do canal: views, watch_time, likes, comments, shares,
        subscribers_gained, subscribers_lost, net_subscribers.
    """
    start_date, end_date = _date_range(days)

    params = {
        "ids": f"channel=={channel_id}",
        "startDate": start_date,
        "endDate": end_date,
        "metrics": ",".join(METRICAS_CANAL),
    }

    result = _api_get(f"{YT_ANALYTICS_BASE}/reports", token, params)
    rows = result.get("rows", [])
    col_headers = [h["name"] for h in result.get("columnHeaders", [])]

    if not rows:
        return {
            "periodo": f"{start_date} a {end_date}",
            "dados": None,
            "mensagem": "Nenhum dado disponível para o período.",
        }

    row = rows[0]
    data = dict(zip(col_headers, row))

    return {
        "periodo": f"{start_date} a {end_date}",
        "views": int(data.get("views", 0)),
        "watch_time_minutos": round(float(data.get("estimatedMinutesWatched", 0)), 0),
        "duracao_media_seg": round(float(data.get("averageViewDuration", 0)), 1),
        "likes": int(data.get("likes", 0)),
        "comments": int(data.get("comments", 0)),
        "shares": int(data.get("shares", 0)),
        "subscribers_gained": int(data.get("subscribersGained", 0)),
        "subscribers_lost": int(data.get("subscribersLost", 0)),
        "net_subscribers": int(data.get("subscribersGained", 0))
        - int(data.get("subscribersLost", 0)),
    }


def get_top_videos(
    token: str,
    days: int = 30,
    limit: int = 10,
    channel_id: str = "MINE",
) -> List[Dict]:
    """
    Retorna os vídeos com melhor performance no período.

    Args:
        token: Access token OAuth 2.0.
        days: Número de dias retroativos.
        limit: Número máximo de vídeos (1–200).
        channel_id: ID do canal ('MINE' para o canal autenticado).

    Returns:
        Lista de dicionários com: video_id, views, watch_time_minutos, likes, comments, shares.
        Ordenada por views (maior primeiro).
    """
    start_date, end_date = _date_range(days)

    params = {
        "ids": f"channel=={channel_id}",
        "startDate": start_date,
        "endDate": end_date,
        "metrics": "views,estimatedMinutesWatched,likes,comments,shares",
        "dimensions": "video",
        "sort": "-views",
        "maxResults": min(limit, 200),
    }

    result = _api_get(f"{YT_ANALYTICS_BASE}/reports", token, params)
    rows = result.get("rows", [])
    col_headers = [h["name"] for h in result.get("columnHeaders", [])]

    videos = []
    for row in rows:
        data = dict(zip(col_headers, row))
        videos.append(
            {
                "video_id": data.get("video", ""),
                "views": int(data.get("views", 0)),
                "watch_time_minutos": round(
                    float(data.get("estimatedMinutesWatched", 0)), 0
                ),
                "likes": int(data.get("likes", 0)),
                "comments": int(data.get("comments", 0)),
                "shares": int(data.get("shares", 0)),
            }
        )

    return videos


def get_video_list(
    token: str,
    days: int = 30,
    limit: int = 20,
    channel_id: str = "MINE",
) -> List[Dict]:
    """
    Retorna lista de vídeos do canal com métricas de performance.
    Enriquece os dados de analytics com títulos via YouTube Data API.

    Args:
        token: Access token OAuth 2.0.
        days: Número de dias retroativos.
        limit: Número máximo de vídeos.
        channel_id: ID do canal.

    Returns:
        Lista de dicionários com: video_id, titulo, views, watch_time_minutos,
        duracao_media_seg, likes, comments, shares, engagement_rate.
    """
    top_videos = get_top_videos(token, days=days, limit=limit, channel_id=channel_id)

    if not top_videos:
        return []

    # Enriquecer com títulos via Data API (em lotes de até 50)
    video_ids = [v["video_id"] for v in top_videos if v["video_id"]]
    titles: Dict[str, str] = {}

    for i in range(0, len(video_ids), 50):
        batch = video_ids[i : i + 50]
        params = {
            "part": "snippet",
            "id": ",".join(batch),
        }
        result = _api_get(f"{YT_DATA_BASE}/videos", token, params)
        for item in result.get("items", []):
            titles[item["id"]] = item["snippet"]["title"]

    # Combinar analytics + títulos
    enriched = []
    for v in top_videos:
        vid_id = v["video_id"]
        views = v["views"]
        engagements = v["likes"] + v["comments"] + v["shares"]
        engagement_rate = round((engagements / views * 100), 2) if views > 0 else 0.0

        enriched.append(
            {
                "video_id": vid_id,
                "titulo": titles.get(vid_id, f"Video {vid_id}"),
                "views": views,
                "watch_time_minutos": v["watch_time_minutos"],
                "likes": v["likes"],
                "comments": v["comments"],
                "shares": v["shares"],
                "engagement_rate": engagement_rate,
            }
        )

    return enriched


def get_demographics(
    token: str,
    days: int = 30,
    channel_id: str = "MINE",
) -> Dict:
    """
    Retorna dados demográficos da audiência (faixa etária e gênero).

    Args:
        token: Access token OAuth 2.0.
        days: Número de dias retroativos.
        channel_id: ID do canal.

    Returns:
        Dicionário com distribuição por faixa etária e gênero (em percentual de views).
    """
    start_date, end_date = _date_range(days)

    params = {
        "ids": f"channel=={channel_id}",
        "startDate": start_date,
        "endDate": end_date,
        "metrics": "viewerPercentage",
        "dimensions": "ageGroup,gender",
        "sort": "-viewerPercentage",
    }

    result = _api_get(f"{YT_ANALYTICS_BASE}/reports", token, params)
    rows = result.get("rows", [])

    por_faixa: Dict[str, float] = {}
    por_genero: Dict[str, float] = {}

    for row in rows:
        age_group, gender, pct = row[0], row[1], float(row[2])

        if age_group not in por_faixa:
            por_faixa[age_group] = 0.0
        por_faixa[age_group] = round(por_faixa[age_group] + pct, 2)

        if gender not in por_genero:
            por_genero[gender] = 0.0
        por_genero[gender] = round(por_genero[gender] + pct, 2)

    return {
        "periodo": f"{start_date} a {end_date}",
        "por_faixa_etaria": dict(sorted(por_faixa.items())),
        "por_genero": por_genero,
    }


def get_traffic_sources(
    token: str,
    days: int = 30,
    channel_id: str = "MINE",
) -> List[Dict]:
    """
    Retorna as fontes de tráfego do canal (de onde os espectadores vêm).

    Args:
        token: Access token OAuth 2.0.
        days: Número de dias retroativos.
        channel_id: ID do canal.

    Returns:
        Lista de fontes de tráfego ordenadas por views (maior primeiro).
        Cada item: source, views, watch_time_minutos, percentual_views.
    """
    start_date, end_date = _date_range(days)

    params = {
        "ids": f"channel=={channel_id}",
        "startDate": start_date,
        "endDate": end_date,
        "metrics": "views,estimatedMinutesWatched",
        "dimensions": "insightTrafficSourceType",
        "sort": "-views",
    }

    result = _api_get(f"{YT_ANALYTICS_BASE}/reports", token, params)
    rows = result.get("rows", [])

    if not rows:
        return []

    total_views = sum(int(row[1]) for row in rows)

    fontes = []
    for row in rows:
        source, views, watch_time = row[0], int(row[1]), float(row[2])
        fontes.append(
            {
                "source": source,
                "views": views,
                "watch_time_minutos": round(watch_time, 0),
                "percentual_views": (
                    round((views / total_views * 100), 1) if total_views > 0 else 0.0
                ),
            }
        )

    return fontes


def get_credentials_and_token(scope: str = YT_ANALYTICS_SCOPE) -> str:
    """Carrega credenciais e retorna access token OAuth 2.0."""
    credentials = _load_credentials()
    return _get_access_token(credentials, scope)


# ---------------------------------------------------------------------------
# Helpers de impressão
# ---------------------------------------------------------------------------


def _print_channel_stats(stats: Dict) -> None:
    """Imprime estatísticas do canal em formato legível."""
    print(f"\n📺 CANAL — {stats['periodo']}")
    print(f"   👁  Views:              {stats.get('views', 0):,}")
    print(f"   ⏱  Watch time (min):   {stats.get('watch_time_minutos', 0):,.0f}")
    print(f"   ⏳  Duração média (s):  {stats.get('duracao_media_seg', 0):.1f}")
    print(f"   👍 Likes:              {stats.get('likes', 0):,}")
    print(f"   💬 Comentários:        {stats.get('comments', 0):,}")
    print(f"   🔗 Compartilhamentos:  {stats.get('shares', 0):,}")
    print(f"   ➕ Inscritos ganhos:   {stats.get('subscribers_gained', 0):,}")
    print(f"   ➖ Inscritos perdidos: {stats.get('subscribers_lost', 0):,}")
    net = stats.get("net_subscribers", 0)
    sinal = "+" if net >= 0 else ""
    print(f"   📈 Saldo inscritos:    {sinal}{net:,}")


def _print_video_table(videos: List[Dict]) -> None:
    """Imprime tabela de vídeos."""
    if not videos:
        print("Nenhum vídeo encontrado.")
        return
    cols = [
        {"key": "titulo", "label": "TÍTULO", "width": 45},
        {"key": "views", "label": "VIEWS", "width": 10, "align": "right"},
        {"key": "likes", "label": "LIKES", "width": 8, "align": "right"},
        {
            "key": "engagement_rate",
            "label": "ENGAJ%",
            "width": 7,
            "align": "right",
            "format": ".1f",
        },
    ]
    print_table(videos, cols)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="YouTube Analytics — Marketing OS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Variáveis de ambiente (uma delas é obrigatória):\n"
            f"  {ENV_CREDENTIALS_FILE}     Service Account JSON (YouTube)\n"
            f"  {ENV_CREDENTIALS_JSON}     JSON inline (YouTube)\n"
            f"  {ENV_CREDENTIALS_FILE_FALLBACK}     Service Account JSON (GSC — fallback)\n"
            f"  {ENV_CREDENTIALS_JSON_FALLBACK}     JSON inline (GSC — fallback)\n\n"
            "Exemplos:\n"
            "  python youtube_analytics.py channel --days 30\n"
            "  python youtube_analytics.py top-videos --days 90 --limit 20\n"
            "  python youtube_analytics.py full-report --output relatorio.json\n"
        ),
    )
    sub = parser.add_subparsers(dest="comando", required=True)

    # channel
    p_ch = sub.add_parser("channel", help="Métricas gerais do canal")
    p_ch.add_argument("--days", type=int, default=30)
    add_output_args(p_ch)

    # videos
    p_vl = sub.add_parser("videos", help="Lista de vídeos com métricas")
    p_vl.add_argument("--days", type=int, default=30)
    p_vl.add_argument("--limit", type=int, default=20)
    add_output_args(p_vl)

    # top-videos
    p_tv = sub.add_parser("top-videos", help="Vídeos com melhor performance")
    p_tv.add_argument("--days", type=int, default=30)
    p_tv.add_argument("--limit", type=int, default=10)
    add_output_args(p_tv)

    # demographics
    p_dg = sub.add_parser("demographics", help="Dados demográficos da audiência")
    p_dg.add_argument("--days", type=int, default=30)
    add_output_args(p_dg)

    # traffic-sources
    p_ts = sub.add_parser("traffic-sources", help="Fontes de tráfego do canal")
    p_ts.add_argument("--days", type=int, default=30)
    add_output_args(p_ts)

    # full-report
    p_fr = sub.add_parser("full-report", help="Relatório completo do canal")
    p_fr.add_argument("--days", type=int, default=30)
    add_output_args(p_fr)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    fmt = OutputFormatter(args)

    try:
        days = validar_inteiro(args.days, campo="days", min_val=1, max_val=365)
    except ValidationError as e:
        handle_validation_error(e)
        return

    try:
        token = get_credentials_and_token()
    except YouTubeAuthError as e:
        print(f"\n❌ Erro de autenticação: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        if args.comando == "channel":
            data = get_channel_stats(token, days=days)
            fmt.print(data, human_fn=_print_channel_stats)

        elif args.comando == "videos":
            limit = validar_inteiro(args.limit, campo="limit", min_val=1, max_val=200)
            data = get_video_list(token, days=days, limit=limit)
            fmt.print(data, human_fn=_print_video_table)

        elif args.comando == "top-videos":
            limit = validar_inteiro(args.limit, campo="limit", min_val=1, max_val=200)
            data = get_top_videos(token, days=days, limit=limit)
            fmt.print(
                data,
                human_fn=lambda d: print_table(
                    d,
                    [
                        {"key": "video_id", "label": "VIDEO ID", "width": 15},
                        {
                            "key": "views",
                            "label": "VIEWS",
                            "width": 10,
                            "align": "right",
                        },
                        {
                            "key": "likes",
                            "label": "LIKES",
                            "width": 8,
                            "align": "right",
                        },
                        {
                            "key": "watch_time_minutos",
                            "label": "WATCH(min)",
                            "width": 10,
                            "align": "right",
                        },
                    ],
                ),
            )

        elif args.comando == "demographics":
            data = get_demographics(token, days=days)
            if fmt.is_json():
                print_json(data)
            else:
                print(f"\n👥 DEMOGRAFIA — {data['periodo']}")
                print_key_value(data["por_faixa_etaria"], title="Por faixa etária:")
                print_key_value(data["por_genero"], title="Por gênero:")

        elif args.comando == "traffic-sources":
            data = get_traffic_sources(token, days=days)
            fmt.print(
                data,
                human_fn=lambda d: print_table(
                    d,
                    [
                        {"key": "source", "label": "FONTE", "width": 35},
                        {
                            "key": "views",
                            "label": "VIEWS",
                            "width": 10,
                            "align": "right",
                        },
                        {
                            "key": "percentual_views",
                            "label": "%",
                            "width": 6,
                            "align": "right",
                            "format": ".1f",
                        },
                    ],
                ),
            )

        elif args.comando == "full-report":
            fmt.print_human(f"\n⏳ Gerando relatório completo (últimos {days} dias)...")
            stats = get_channel_stats(token, days=days)
            videos = get_video_list(token, days=days, limit=20)
            demographics = get_demographics(token, days=days)
            traffic = get_traffic_sources(token, days=days)

            report = {
                "gerado_em": datetime.now(tz=timezone.utc).isoformat(),
                "periodo": f"últimos {days} dias",
                "canal": stats,
                "top_videos": videos,
                "demografia": demographics,
                "fontes_trafego": traffic,
            }

            saved = fmt.save(report, "youtube-report")
            if not fmt.is_json() and not saved:
                _print_channel_stats(stats)
                print(f"\n🎬 TOP VÍDEOS ({len(videos)})")
                _print_video_table(videos)
            elif fmt.is_json():
                print_json(report)
            else:
                fmt.print_human(f"\n✅ Relatório gerado com sucesso!")

    except ValidationError as e:
        handle_validation_error(e)
    except YouTubeAuthError as e:
        print(f"\n❌ Erro de autenticação: {e}", file=sys.stderr)
        sys.exit(1)
    except YouTubeAnalyticsError as e:
        print(f"\n❌ Erro da API do YouTube Analytics: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
