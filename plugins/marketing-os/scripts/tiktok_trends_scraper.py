#!/usr/bin/env python3
"""
TikTok Trends Scraper - Busca vídeos virais por nicho/hashtag
Usa a biblioteca TikTok-Api (não-oficial) ou Apify como fallback

INSTALAÇÃO:
pip install TikTok-Api playwright --break-system-packages
python -m playwright install

USO:
python tiktok_trends_scraper.py --hashtag "marketing" --min-views 1000000
python tiktok_trends_scraper.py --trending --region "BR" --limit 20
python tiktok_trends_scraper.py --search "receitas fitness" --min-views 500000
"""

import argparse
import json
import asyncio
from datetime import datetime
from pathlib import Path
import sys
import site
from typing import Any, Dict, List, Tuple

# Adiciona user site-packages ao path (necessário em alguns sistemas)
user_site = site.getusersitepackages()
if user_site not in sys.path:
    sys.path.insert(0, user_site)

# Tenta importar TikTok-Api
try:
    from TikTokApi import TikTokApi

    TIKTOK_API_AVAILABLE = True
except ImportError:
    TIKTOK_API_AVAILABLE = False

# Configurações (diretório criado apenas quando necessário)
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / "tiktok-trends"


# ============================================================
# CATEGORIAS E NICHOS PARA BUSCA
# ============================================================

NICHOS_HASHTAGS: Dict[str, List[str]] = {
    "marketing": [
        "marketingdigital",
        "socialmedia",
        "empreendedorismo",
        "negociosonline",
        "marketingtips",
        "growthhacking",
        "infoprodutos",
        "copywriting",
        "trafegopago",
    ],
    "fitness": [
        "fitness",
        "treino",
        "musculacao",
        "academia",
        "fitnessmotivation",
        "personaltrainer",
        "dieta",
        "emagrecimento",
        "vidasaudavel",
        "workout",
    ],
    "beleza": [
        "makeup",
        "skincare",
        "beleza",
        "maquiagem",
        "beautytips",
        "cuidadoscomapele",
        "cabelo",
        "unhas",
        "rotinadebeleza",
        "grwm",
    ],
    "gastronomia": [
        "receitas",
        "cozinha",
        "comida",
        "receitafacil",
        "foodtiktok",
        "receitasfit",
        "airfryer",
        "sobremesa",
        "lanche",
        "almoco",
    ],
    "financas": [
        "financas",
        "investimentos",
        "dinheiro",
        "rendaextra",
        "educacaofinanceira",
        "bolsadevalores",
        "criptomoedas",
        "economizar",
        "independenciafinanceira",
        "dividendos",
    ],
    "tecnologia": [
        "tech",
        "tecnologia",
        "iphone",
        "android",
        "apple",
        "gadgets",
        "apps",
        "ia",
        "inteligenciaartificial",
        "programacao",
    ],
    "lifestyle": [
        "rotina",
        "dayinmylife",
        "organizacao",
        "produtividade",
        "minimalismo",
        "lifestyle",
        "motivacao",
        "mindset",
        "autocuidado",
        "qualidadedevida",
    ],
}

FORMATOS_VIRAIS: Dict[str, List[str]] = {
    "tutorial": ["tutorial", "comofazer", "dicasde", "aprenda", "pap"],
    "storytime": ["storytime", "historia", "oqueaconteceu", "exposed"],
    "trends": ["trend", "viral", "challenge", "dancinha", "fyp"],
    "pov": ["pov", "povvocê", "imaginaque"],
    "reviews": ["review", "resenha", "testando", "vale apena", "honesto"],
    "antes_depois": ["antesedepois", "transformacao", "glow up", "resultado"],
    "react": ["react", "dueto", "stitch", "respondendo"],
    "grwm": ["grwm", "getreadywithme", "arrumesecomigo"],
}


# ============================================================
# FUNÇÕES DE BUSCA
# ============================================================


async def buscar_trending(api: Any, region: str = "BR", limit: int = 30) -> List[Dict]:
    """Busca vídeos em trending"""
    videos: List[Dict] = []
    async for video in api.trending.videos(count=limit):
        videos.append(extrair_dados_video(video))
    return videos


async def buscar_por_hashtag(
    api: Any, hashtag: str, limit: int = 30, min_views: int = 0
) -> List[Dict]:
    """Busca vídeos por hashtag"""
    videos: List[Dict] = []
    tag = api.hashtag(name=hashtag)
    async for video in tag.videos(count=limit):
        dados = extrair_dados_video(video)
        if dados["views"] >= min_views:
            videos.append(dados)
    return videos


async def buscar_por_keyword(
    api: Any, keyword: str, limit: int = 30, min_views: int = 0
) -> List[Dict]:
    """Busca vídeos por palavra-chave"""
    videos: List[Dict] = []
    async for video in api.search.videos(keyword, count=limit):
        dados = extrair_dados_video(video)
        if dados["views"] >= min_views:
            videos.append(dados)
    return videos


def extrair_dados_video(video: Any) -> Dict:
    """Extrai dados relevantes do vídeo - compatível com TikTokApi v7.x"""
    try:
        # TikTokApi v7.x usa atributos diferentes
        # Tenta acessar dados via .as_dict ou diretamente
        if hasattr(video, "as_dict"):
            data = video.as_dict
        else:
            data = {}

        # Extrai ID
        video_id = getattr(video, "id", None) or data.get("id", "")

        # Extrai autor
        author = getattr(video, "author", None)
        if author:
            autor_username = getattr(author, "username", "") or getattr(
                author, "unique_id", ""
            )
            autor_followers = getattr(author, "follower_count", 0)
        else:
            author_data = data.get("author", {})
            autor_username = author_data.get(
                "uniqueId", author_data.get("username", "N/A")
            )
            autor_followers = author_data.get("followerCount", 0)

        # Extrai estatísticas
        stats = getattr(video, "stats", None)
        if stats:
            views = getattr(stats, "play_count", 0) or getattr(stats, "playCount", 0)
            likes = getattr(stats, "digg_count", 0) or getattr(stats, "diggCount", 0)
            comments = getattr(stats, "comment_count", 0) or getattr(
                stats, "commentCount", 0
            )
            shares = getattr(stats, "share_count", 0) or getattr(stats, "shareCount", 0)
        else:
            stats_data = data.get("stats", {})
            views = stats_data.get("playCount", 0)
            likes = stats_data.get("diggCount", 0)
            comments = stats_data.get("commentCount", 0)
            shares = stats_data.get("shareCount", 0)

        # Extrai descrição
        descricao = getattr(video, "desc", "") or data.get("desc", "")
        if descricao:
            descricao = descricao[:200]

        # Extrai duração
        video_info = getattr(video, "video", None)
        if video_info:
            duracao = getattr(video_info, "duration", 0)
        else:
            duracao = data.get("video", {}).get("duration", 0)

        # Extrai hashtags
        hashtags_obj = getattr(video, "hashtags", None)
        if hashtags_obj:
            hashtags = [getattr(tag, "name", str(tag)) for tag in hashtags_obj]
        else:
            challenges = data.get("challenges", [])
            hashtags = [c.get("title", "") for c in challenges if c.get("title")]

        # Extrai música
        sound = getattr(video, "sound", None)
        if sound:
            musica = getattr(sound, "title", "")
        else:
            musica = data.get("music", {}).get("title", "")

        # Monta URL
        url = (
            f"https://www.tiktok.com/@{autor_username}/video/{video_id}"
            if video_id and autor_username
            else ""
        )

        # Calcula engagement e viral score
        class StatsObj:
            def __init__(self, v: int, l: int, c: int, s: int) -> None:
                self.play_count = v
                self.digg_count = l
                self.comment_count = c
                self.share_count = s

        stats_obj = StatsObj(views, likes, comments, shares)

        return {
            "id": video_id,
            "url": url,
            "descricao": descricao,
            "autor": autor_username,
            "autor_followers": autor_followers,
            "views": views,
            "likes": likes,
            "comments": comments,
            "shares": shares,
            "duracao_segundos": duracao,
            "hashtags": hashtags,
            "musica": musica,
            "data_criacao": "",
            "engagement_rate": calcular_engagement(stats_obj),
            "viral_score": calcular_viral_score(stats_obj),
        }
    except Exception as e:
        return {"erro": str(e), "erro_detalhes": repr(e)}


def calcular_engagement(stats: Any) -> float:
    """Calcula taxa de engajamento"""
    try:
        total_engajamento = stats.digg_count + stats.comment_count + stats.share_count
        if stats.play_count > 0:
            return round((total_engajamento / stats.play_count) * 100, 2)
        return 0
    except Exception:
        return 0


def calcular_viral_score(stats: Any) -> float:
    """Calcula score de viralidade (0-100)"""
    try:
        # Pesos: views (40%), likes (25%), shares (20%), comments (15%)
        views_score = min(stats.play_count / 10000000, 1) * 40
        likes_score = min(stats.digg_count / 1000000, 1) * 25
        shares_score = min(stats.share_count / 100000, 1) * 20
        comments_score = min(stats.comment_count / 50000, 1) * 15
        return round(views_score + likes_score + shares_score + comments_score, 1)
    except Exception:
        return 0


# ============================================================
# FUNÇÕES DE ANÁLISE
# ============================================================


def analisar_trends(videos: List[Dict]) -> Dict:
    """Analisa padrões nos vídeos coletados"""
    if not videos:
        return {}

    # Hashtags mais comuns
    todas_hashtags: List[str] = []
    for v in videos:
        todas_hashtags.extend(v.get("hashtags", []))

    hashtag_count: Dict[str, int] = {}
    for h in todas_hashtags:
        hashtag_count[h] = hashtag_count.get(h, 0) + 1

    top_hashtags = sorted(hashtag_count.items(), key=lambda x: x[1], reverse=True)[:20]

    # Duração média
    duracoes = [v["duracao_segundos"] for v in videos if v.get("duracao_segundos")]
    duracao_media = sum(duracoes) / len(duracoes) if duracoes else 0

    # Views médio
    views = [v["views"] for v in videos if v.get("views")]
    views_medio = sum(views) / len(views) if views else 0

    # Engagement médio
    engagements = [v["engagement_rate"] for v in videos if v.get("engagement_rate")]
    engagement_medio = sum(engagements) / len(engagements) if engagements else 0

    return {
        "total_videos": len(videos),
        "top_hashtags": top_hashtags,
        "duracao_media_segundos": round(duracao_media, 1),
        "views_medio": int(views_medio),
        "engagement_medio": round(engagement_medio, 2),
        "video_mais_viral": (
            max(videos, key=lambda x: x.get("views", 0)) if videos else None
        ),
        "melhor_engagement": (
            max(videos, key=lambda x: x.get("engagement_rate", 0)) if videos else None
        ),
    }


def gerar_relatorio(videos: List[Dict], analise: Dict, params: Dict) -> Tuple[str, str]:
    """Gera relatório em formato Markdown"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    relatorio = f"""# 📊 Relatório TikTok Trends
**Gerado em:** {datetime.now().strftime("%d/%m/%Y às %H:%M")}

## 🔍 Parâmetros da Busca
- **Tipo:** {params.get('tipo', 'N/A')}
- **Termo:** {params.get('termo', 'N/A')}
- **Mínimo de Views:** {params.get('min_views', 0):,}
- **Limite:** {params.get('limit', 30)}

---

## 📈 Análise Geral

| Métrica | Valor |
|---------|-------|
| Total de Vídeos | {analise['total_videos']} |
| Views Médio | {analise['views_medio']:,} |
| Duração Média | {analise['duracao_media_segundos']}s |
| Engagement Médio | {analise['engagement_medio']}% |

### 🏷️ Top Hashtags
"""

    for hashtag, count in analise["top_hashtags"][:10]:
        relatorio += f"- #{hashtag} ({count}x)\n"

    relatorio += "\n---\n\n## 🔥 Vídeos Mais Virais\n\n"

    # Top 10 por views
    top_videos = sorted(videos, key=lambda x: x.get("views", 0), reverse=True)[:10]

    for i, video in enumerate(top_videos, 1):
        relatorio += f"""### {i}. {video.get('descricao', 'Sem descrição')[:80]}...

| Métrica | Valor |
|---------|-------|
| 👤 Autor | @{video.get('autor', 'N/A')} |
| 👁️ Views | {video.get('views', 0):,} |
| ❤️ Likes | {video.get('likes', 0):,} |
| 💬 Comments | {video.get('comments', 0):,} |
| 🔄 Shares | {video.get('shares', 0):,} |
| ⏱️ Duração | {video.get('duracao_segundos', 0)}s |
| 📊 Engagement | {video.get('engagement_rate', 0)}% |
| 🎯 Viral Score | {video.get('viral_score', 0)}/100 |

🔗 [Assistir]({video.get('url', '#')})

**Hashtags:** {' '.join(['#' + h for h in video.get('hashtags', [])[:5]])}

---

"""

    # Insights
    relatorio += """## 💡 Insights para Criação de Conteúdo

### Padrões Identificados:
"""

    if analise["duracao_media_segundos"] < 30:
        relatorio += "- ✅ Vídeos curtos (<30s) estão performando bem nesse nicho\n"
    elif analise["duracao_media_segundos"] < 60:
        relatorio += "- ✅ Vídeos de 30-60s são o sweet spot nesse nicho\n"
    else:
        relatorio += "- ✅ Vídeos mais longos (60s+) estão tendo boa performance\n"

    if analise["engagement_medio"] > 5:
        relatorio += "- 🔥 Alto engajamento! Audiência muito ativa nesse nicho\n"

    relatorio += f"""
### Recomendações:
1. Use as hashtags: {', '.join(['#' + h[0] for h in analise['top_hashtags'][:5]])}
2. Duração ideal: {int(analise['duracao_media_segundos'])}s
3. Estude o formato do vídeo mais viral para replicar

"""

    return relatorio, timestamp


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================


async def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    parser = argparse.ArgumentParser(
        description="Busca vídeos virais do TikTok por nicho/hashtag",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python tiktok_trends_scraper.py --trending --limit 20
  python tiktok_trends_scraper.py --hashtag "marketingdigital" --min-views 1000000
  python tiktok_trends_scraper.py --search "receitas fitness" --min-views 500000
  python tiktok_trends_scraper.py --nicho marketing --min-views 100000
        """,
    )

    # Tipo de busca
    grupo_busca = parser.add_mutually_exclusive_group(required=True)
    grupo_busca.add_argument(
        "--trending", action="store_true", help="Buscar vídeos em trending"
    )
    grupo_busca.add_argument(
        "--hashtag", type=str, help="Buscar por hashtag específica"
    )
    grupo_busca.add_argument("--search", type=str, help="Buscar por palavra-chave")
    grupo_busca.add_argument(
        "--nicho",
        type=str,
        choices=NICHOS_HASHTAGS.keys(),
        help="Buscar por nicho pré-definido",
    )

    # Filtros
    parser.add_argument(
        "--min-views", type=int, default=0, help="Mínimo de views (default: 0)"
    )
    parser.add_argument(
        "--limit", type=int, default=30, help="Limite de vídeos (default: 30)"
    )
    parser.add_argument("--region", type=str, default="BR", help="Região (default: BR)")

    # Saída
    parser.add_argument(
        "--output", type=str, help="Nome do arquivo de saída (sem extensão)"
    )
    parser.add_argument(
        "--format",
        choices=["md", "json", "both"],
        default="both",
        help="Formato de saída (default: both)",
    )

    args = parser.parse_args()

    if not TIKTOK_API_AVAILABLE:
        print("\n❌ TikTok-Api não está instalada!")
        print("\nPara instalar:")
        print("  pip install TikTok-Api playwright --break-system-packages")
        print("  python -m playwright install")
        print("\n💡 Alternativamente, use o template de pesquisa manual em:")
        print("   assets/templates/pesquisa-tiktok-trends.md")
        sys.exit(1)

    print("🔄 Iniciando busca no TikTok...")

    async with TikTokApi() as api:
        # Cria sessão com cookies do ms_token (necessário para algumas buscas)
        # headless=False e browser='webkit' ajudam a evitar detecção de bot
        await api.create_sessions(
            num_sessions=1, sleep_after=5, headless=False, browser="webkit"
        )

        videos: List[Dict] = []
        params: Dict = {
            "limit": args.limit,
            "min_views": args.min_views,
            "region": args.region,
        }

        # Executa busca baseada no tipo
        if args.trending:
            print(f"📈 Buscando trending em {args.region}...")
            params["tipo"] = "Trending"
            params["termo"] = args.region
            videos = await buscar_trending(api, args.region, args.limit)

        elif args.hashtag:
            print(f"🏷️ Buscando #{args.hashtag}...")
            params["tipo"] = "Hashtag"
            params["termo"] = args.hashtag
            videos = await buscar_por_hashtag(
                api, args.hashtag, args.limit, args.min_views
            )

        elif args.search:
            print(f"🔍 Buscando '{args.search}'...")
            params["tipo"] = "Keyword"
            params["termo"] = args.search
            videos = await buscar_por_keyword(
                api, args.search, args.limit, args.min_views
            )

        elif args.nicho:
            print(f"📂 Buscando nicho: {args.nicho}...")
            params["tipo"] = "Nicho"
            params["termo"] = args.nicho
            hashtags = NICHOS_HASHTAGS[args.nicho]
            for hashtag in hashtags[:3]:  # Top 3 hashtags do nicho
                print(f"  → Buscando #{hashtag}...")
                novos = await buscar_por_hashtag(
                    api, hashtag, args.limit // 3, args.min_views
                )
                videos.extend(novos)

        # Filtra duplicatas
        ids_vistos: set = set()
        videos_unicos: List[Dict] = []
        for v in videos:
            if v.get("id") not in ids_vistos:
                ids_vistos.add(v.get("id"))
                videos_unicos.append(v)
        videos = videos_unicos

        print(f"\n✅ Encontrados {len(videos)} vídeos")

        if not videos:
            print("⚠️ Nenhum vídeo encontrado com os critérios especificados")
            sys.exit(0)

        # Análise
        analise = analisar_trends(videos)

        # Gera relatório
        relatorio, timestamp = gerar_relatorio(videos, analise, params)

        # Define nome do arquivo
        if args.output:
            base_name = args.output
        else:
            termo = args.hashtag or args.search or args.nicho or "trending"
            termo = termo.replace(" ", "_")[:30]
            base_name = f"tiktok_{termo}_{timestamp}"

        # Salva arquivos
        if args.format in ["md", "both"]:
            md_path = OUTPUT_DIR / f"{base_name}.md"
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(relatorio)
            print(f"📄 Relatório salvo: {md_path}")

        if args.format in ["json", "both"]:
            json_path = OUTPUT_DIR / f"{base_name}.json"
            dados = {"params": params, "analise": analise, "videos": videos}
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            print(f"📊 JSON salvo: {json_path}")

        # Mostra resumo
        print(f"\n{'='*50}")
        print("📊 RESUMO")
        print(f"{'='*50}")
        print(f"Total de vídeos: {analise['total_videos']}")
        print(f"Views médio: {analise['views_medio']:,}")
        print(f"Engagement médio: {analise['engagement_medio']}%")
        print(f"\n🔥 Vídeo mais viral:")
        if analise["video_mais_viral"] and "autor" in analise["video_mais_viral"]:
            v = analise["video_mais_viral"]
            print(f"   @{v.get('autor', 'N/A')} - {v.get('views', 0):,} views")
            print(f"   {v.get('url', 'N/A')}")


if __name__ == "__main__":
    asyncio.run(main())
