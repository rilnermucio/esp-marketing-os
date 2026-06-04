#!/usr/bin/env python3
"""
Trend Tracker - Monitorar tendências via APIs públicas
Suporta: Google Trends, Reddit, Twitter/X, YouTube, e fontes RSS

Uso:
    python trend_tracker.py "termo" [plataformas] [--periodo dias] [--formato json|markdown|tabela]

Exemplos:
    python trend_tracker.py "inteligencia artificial"
    python trend_tracker.py "marketing digital" google,reddit --periodo 7
    python trend_tracker.py "python" todas --formato markdown
    python trend_tracker.py --trending brasil
"""

import sys
import json
import re
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime
from html import unescape
from typing import Optional
import ssl

# Configuração SSL (verificação de certificado habilitada por padrão)
ssl_context = ssl.create_default_context()


def fazer_requisicao(
    url: str, headers: Optional[dict] = None, timeout: int = 10
) -> Optional[str]:
    """Faz requisição HTTP e retorna o conteúdo."""
    try:
        req = urllib.request.Request(url)
        req.add_header(
            "User-Agent",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        )
        if headers:
            for key, value in headers.items():
                req.add_header(key, value)

        with urllib.request.urlopen(
            req, timeout=timeout, context=ssl_context
        ) as response:
            return response.read().decode("utf-8")
    except Exception as e:
        print(f"[trend_tracker] fetch falhou: {e}", file=sys.stderr)
        return None


def buscar_google_trends(termo: str, regiao: str = "BR") -> dict:
    """
    Busca tendências relacionadas no Google Trends via sugestões de busca.
    Retorna termos relacionados e interesse ao longo do tempo.
    """
    resultados = {
        "plataforma": "Google Trends",
        "termo_buscado": termo,
        "regiao": regiao,
        "data_consulta": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "termos_relacionados": [],
        "sugestoes_busca": [],
        "status": "sucesso",
    }

    try:
        # Google Suggest API (autocomplete)
        termo_encoded = urllib.parse.quote(termo)
        url_suggest = f"http://suggestqueries.google.com/complete/search?client=firefox&q={termo_encoded}&hl=pt-BR"

        resposta = fazer_requisicao(url_suggest)
        if resposta:
            dados = json.loads(resposta)
            if len(dados) > 1 and isinstance(dados[1], list):
                resultados["sugestoes_busca"] = dados[1][:10]

        # Google Trends Daily (via RSS)
        url_trends = (
            f"https://trends.google.com/trends/trendingsearches/daily/rss?geo={regiao}"
        )
        resposta_trends = fazer_requisicao(url_trends)

        if resposta_trends:
            # Parse simples do RSS para extrair títulos
            titulos = re.findall(
                r"<title><!\[CDATA\[(.*?)\]\]></title>", resposta_trends
            )
            # Remover o primeiro título que é do feed
            if titulos:
                titulos = titulos[1:11]  # Pegar até 10 tendências
            resultados["tendencias_do_dia"] = titulos

            # Extrair tráfego aproximado
            trafegos = re.findall(
                r"<ht:approx_traffic>(.*?)</ht:approx_traffic>", resposta_trends
            )
            if trafegos:
                resultados["trafego_aproximado"] = trafegos[:10]

    except Exception as e:
        resultados["status"] = f"erro: {str(e)}"

    return resultados


def buscar_reddit(
    termo: str, subreddit: str = "all", limite: int = 10, periodo: str = "week"
) -> dict:
    """
    Busca posts populares no Reddit relacionados ao termo.
    Períodos: hour, day, week, month, year, all
    """
    resultados = {
        "plataforma": "Reddit",
        "termo_buscado": termo,
        "subreddit": subreddit,
        "periodo": periodo,
        "data_consulta": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "posts": [],
        "status": "sucesso",
    }

    try:
        termo_encoded = urllib.parse.quote(termo)
        url = f"https://www.reddit.com/r/{subreddit}/search.json?q={termo_encoded}&sort=top&t={periodo}&limit={limite}"

        resposta = fazer_requisicao(url)
        if resposta:
            dados = json.loads(resposta)

            if "data" in dados and "children" in dados["data"]:
                for post in dados["data"]["children"]:
                    post_data = post.get("data", {})
                    resultados["posts"].append(
                        {
                            "titulo": post_data.get("title", ""),
                            "subreddit": post_data.get("subreddit", ""),
                            "score": post_data.get("score", 0),
                            "comentarios": post_data.get("num_comments", 0),
                            "url": f"https://reddit.com{post_data.get('permalink', '')}",
                            "criado_em": (
                                datetime.fromtimestamp(
                                    post_data.get("created_utc", 0)
                                ).strftime("%Y-%m-%d %H:%M")
                                if post_data.get("created_utc")
                                else ""
                            ),
                            "upvote_ratio": post_data.get("upvote_ratio", 0),
                        }
                    )

                # Calcular métricas agregadas
                if resultados["posts"]:
                    scores = [p["score"] for p in resultados["posts"]]
                    comentarios = [p["comentarios"] for p in resultados["posts"]]
                    resultados["metricas"] = {
                        "total_posts": len(resultados["posts"]),
                        "score_total": sum(scores),
                        "score_medio": round(sum(scores) / len(scores), 1),
                        "comentarios_total": sum(comentarios),
                        "subreddits_unicos": len(
                            set(p["subreddit"] for p in resultados["posts"])
                        ),
                    }

    except Exception as e:
        resultados["status"] = f"erro: {str(e)}"

    return resultados


def buscar_youtube_trends(termo: str, regiao: str = "BR", limite: int = 10) -> dict:
    """
    Busca vídeos populares no YouTube relacionados ao termo via RSS.
    """
    resultados = {
        "plataforma": "YouTube",
        "termo_buscado": termo,
        "regiao": regiao,
        "data_consulta": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "videos": [],
        "status": "sucesso",
    }

    try:
        termo_encoded = urllib.parse.quote(termo)
        # YouTube RSS feed de busca
        url = (
            f"https://www.youtube.com/results?search_query={termo_encoded}&sp=CAM%253D"
        )

        resposta = fazer_requisicao(url)
        if resposta:
            # Extrair dados do JSON embutido na página
            match = re.search(r"var ytInitialData = ({.*?});", resposta)
            if match:
                try:
                    dados = json.loads(match.group(1))
                    contents = (
                        dados.get("contents", {})
                        .get("twoColumnSearchResultsRenderer", {})
                        .get("primaryContents", {})
                        .get("sectionListRenderer", {})
                        .get("contents", [])
                    )

                    for section in contents:
                        items = section.get("itemSectionRenderer", {}).get(
                            "contents", []
                        )
                        for item in items[:limite]:
                            video = item.get("videoRenderer", {})
                            if video:
                                titulo = ""
                                if "title" in video and "runs" in video["title"]:
                                    titulo = video["title"]["runs"][0].get("text", "")

                                views = ""
                                if "viewCountText" in video:
                                    views = video["viewCountText"].get("simpleText", "")

                                canal = ""
                                if (
                                    "ownerText" in video
                                    and "runs" in video["ownerText"]
                                ):
                                    canal = video["ownerText"]["runs"][0].get(
                                        "text", ""
                                    )

                                duracao = ""
                                if "lengthText" in video:
                                    duracao = video["lengthText"].get("simpleText", "")

                                publicado = ""
                                if "publishedTimeText" in video:
                                    publicado = video["publishedTimeText"].get(
                                        "simpleText", ""
                                    )

                                video_id = video.get("videoId", "")

                                if titulo:
                                    resultados["videos"].append(
                                        {
                                            "titulo": titulo,
                                            "canal": canal,
                                            "visualizacoes": views,
                                            "duracao": duracao,
                                            "publicado": publicado,
                                            "url": f"https://youtube.com/watch?v={video_id}",
                                        }
                                    )
                except json.JSONDecodeError:
                    pass

    except Exception as e:
        resultados["status"] = f"erro: {str(e)}"

    return resultados


def buscar_hacker_news(termo: str, limite: int = 10) -> dict:
    """
    Busca posts populares no Hacker News relacionados ao termo.
    """
    resultados = {
        "plataforma": "Hacker News",
        "termo_buscado": termo,
        "data_consulta": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "posts": [],
        "status": "sucesso",
    }

    try:
        termo_encoded = urllib.parse.quote(termo)
        url = f"https://hn.algolia.com/api/v1/search?query={termo_encoded}&tags=story&hitsPerPage={limite}"

        resposta = fazer_requisicao(url)
        if resposta:
            dados = json.loads(resposta)

            for hit in dados.get("hits", []):
                resultados["posts"].append(
                    {
                        "titulo": hit.get("title", ""),
                        "url": hit.get("url", "")
                        or f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}",
                        "pontos": hit.get("points", 0),
                        "comentarios": hit.get("num_comments", 0),
                        "autor": hit.get("author", ""),
                        "criado_em": (
                            hit.get("created_at", "")[:10]
                            if hit.get("created_at")
                            else ""
                        ),
                    }
                )

            # Métricas agregadas
            if resultados["posts"]:
                pontos = [p["pontos"] for p in resultados["posts"]]
                resultados["metricas"] = {
                    "total_posts": len(resultados["posts"]),
                    "pontos_total": sum(pontos),
                    "pontos_medio": round(sum(pontos) / len(pontos), 1),
                }

    except Exception as e:
        resultados["status"] = f"erro: {str(e)}"

    return resultados


def buscar_twitter_trends(regiao: str = "BR") -> dict:
    """
    Busca trending topics aproximados via fontes públicas.
    Nota: Twitter/X limitou APIs públicas, então usamos alternativas.
    """
    resultados = {
        "plataforma": "Twitter/X (aproximado)",
        "regiao": regiao,
        "data_consulta": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "tendencias": [],
        "status": "sucesso",
        "nota": "Dados aproximados via fontes públicas. Para dados em tempo real, use a API oficial do X.",
    }

    try:
        # Usar Nitter ou outras fontes públicas (exemplo com trending.topics)
        # Como não há API pública confiável, retornamos instruções
        resultados["instrucoes"] = [
            "Para trending topics do Twitter/X em tempo real:",
            "1. Use a API oficial do X (requer autenticação)",
            "2. Acesse: https://twitter.com/explore/tabs/trending",
            "3. Ferramentas: Trendsmap, GetDayTrends, Trendogate",
        ]

        # Alternativa: buscar menções em outras plataformas
        resultados["alternativas"] = {
            "trendsmap": "https://www.trendsmap.com/local/brazil",
            "getdaytrends": f"https://getdaytrends.com/{regiao.lower()}",
            "twittertrends": f"https://twitter-trends.iamrohit.in/{regiao.lower()}",
        }

    except Exception as e:
        resultados["status"] = f"erro: {str(e)}"

    return resultados


def buscar_noticias_tech(termo: str, limite: int = 10) -> dict:
    """
    Busca notícias de tecnologia via RSS feeds públicos.
    """
    resultados = {
        "plataforma": "Notícias Tech",
        "termo_buscado": termo,
        "data_consulta": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "noticias": [],
        "status": "sucesso",
    }

    # Feeds RSS de tecnologia
    feeds = [
        ("TechCrunch", "https://techcrunch.com/feed/"),
        ("The Verge", "https://www.theverge.com/rss/index.xml"),
        ("Wired", "https://www.wired.com/feed/rss"),
    ]

    termo_lower = termo.lower()

    try:
        for nome_fonte, url in feeds:
            resposta = fazer_requisicao(url)
            if resposta:
                # Parse simples do RSS
                items = re.findall(r"<item>(.*?)</item>", resposta, re.DOTALL)
                if not items:
                    items = re.findall(r"<entry>(.*?)</entry>", resposta, re.DOTALL)

                for item in items[:20]:  # Verificar até 20 itens por feed
                    titulo_match = re.search(
                        r"<title[^>]*>(.*?)</title>", item, re.DOTALL
                    )
                    link_match = re.search(r"<link[^>]*>(.*?)</link>", item, re.DOTALL)
                    if not link_match:
                        link_match = re.search(r'<link[^>]*href="([^"]*)"', item)

                    if titulo_match:
                        titulo = unescape(
                            re.sub(
                                r"<!\[CDATA\[(.*?)\]\]>", r"\1", titulo_match.group(1)
                            )
                        )

                        # Filtrar por termo
                        if termo_lower in titulo.lower():
                            link = ""
                            if link_match:
                                link = link_match.group(1).strip()

                            # Extrair data
                            data_match = re.search(r"<pubDate>(.*?)</pubDate>", item)
                            data = data_match.group(1)[:16] if data_match else ""

                            resultados["noticias"].append(
                                {
                                    "titulo": titulo,
                                    "fonte": nome_fonte,
                                    "url": link,
                                    "data": data,
                                }
                            )

                            if len(resultados["noticias"]) >= limite:
                                break

                if len(resultados["noticias"]) >= limite:
                    break

    except Exception as e:
        resultados["status"] = f"erro: {str(e)}"

    return resultados


def obter_trending_geral(regiao: str = "BR") -> dict:
    """
    Obtém tendências gerais de múltiplas fontes.
    """
    resultados = {
        "tipo": "Trending Geral",
        "regiao": regiao,
        "data_consulta": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "fontes": {},
    }

    # Google Trends do dia
    print("  Buscando Google Trends...", file=sys.stderr)
    google = buscar_google_trends("", regiao)
    if google.get("tendencias_do_dia"):
        resultados["fontes"]["google_trends"] = {
            "tendencias": google["tendencias_do_dia"],
            "trafego": google.get("trafego_aproximado", []),
        }

    # Reddit popular
    print("  Buscando Reddit Popular...", file=sys.stderr)
    reddit_url = "https://www.reddit.com/r/popular.json?limit=10"
    resposta = fazer_requisicao(reddit_url)
    if resposta:
        try:
            dados = json.loads(resposta)
            posts = []
            for post in dados.get("data", {}).get("children", []):
                post_data = post.get("data", {})
                posts.append(
                    {
                        "titulo": post_data.get("title", ""),
                        "subreddit": post_data.get("subreddit", ""),
                        "score": post_data.get("score", 0),
                    }
                )
            resultados["fontes"]["reddit_popular"] = posts
        except Exception:
            pass

    # Hacker News top
    print("  Buscando Hacker News...", file=sys.stderr)
    hn_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    resposta = fazer_requisicao(hn_url)
    if resposta:
        try:
            top_ids = json.loads(resposta)[:10]
            hn_posts = []
            for story_id in top_ids:
                story_url = (
                    f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                )
                story_resp = fazer_requisicao(story_url)
                if story_resp:
                    story = json.loads(story_resp)
                    hn_posts.append(
                        {
                            "titulo": story.get("title", ""),
                            "pontos": story.get("score", 0),
                            "url": story.get("url", ""),
                        }
                    )
            resultados["fontes"]["hacker_news"] = hn_posts
        except Exception:
            pass

    return resultados


def formatar_resultado_tabela(dados: dict) -> str:
    """Formata resultado como tabela ASCII."""
    linhas = []
    plataforma = dados.get("plataforma", dados.get("tipo", "Resultado"))

    linhas.append("=" * 70)
    linhas.append(f" {plataforma}")
    linhas.append("=" * 70)

    if dados.get("termo_buscado"):
        linhas.append(f" Termo: {dados['termo_buscado']}")
    linhas.append(
        f" Data: {dados.get('data_consulta', datetime.now().strftime('%Y-%m-%d %H:%M'))}"
    )
    linhas.append("-" * 70)

    # Posts do Reddit
    if "posts" in dados and dados["posts"]:
        linhas.append("")
        linhas.append(" TOP POSTS:")
        linhas.append("-" * 70)
        for i, post in enumerate(dados["posts"][:10], 1):
            titulo = post.get("titulo", "")[:55]
            score = post.get("score") or post.get("pontos", 0)
            linhas.append(f" {i:2}. [{score:>6}] {titulo}")

        if "metricas" in dados:
            linhas.append("")
            linhas.append(" METRICAS:")
            for k, v in dados["metricas"].items():
                linhas.append(f"   - {k}: {v}")

    # Vídeos do YouTube
    if "videos" in dados and dados["videos"]:
        linhas.append("")
        linhas.append(" TOP VIDEOS:")
        linhas.append("-" * 70)
        for i, video in enumerate(dados["videos"][:10], 1):
            titulo = video.get("titulo", "")[:45]
            views = video.get("visualizacoes", "")
            linhas.append(f" {i:2}. {titulo}")
            linhas.append(f"     Views: {views} | Canal: {video.get('canal', '')[:20]}")

    # Sugestões do Google
    if "sugestoes_busca" in dados and dados["sugestoes_busca"]:
        linhas.append("")
        linhas.append(" SUGESTOES DE BUSCA:")
        linhas.append("-" * 70)
        for i, sugestao in enumerate(dados["sugestoes_busca"], 1):
            linhas.append(f" {i:2}. {sugestao}")

    # Tendências do dia
    if "tendencias_do_dia" in dados and dados["tendencias_do_dia"]:
        linhas.append("")
        linhas.append(" TENDENCIAS DO DIA:")
        linhas.append("-" * 70)
        trafegos = dados.get("trafego_aproximado", [])
        for i, trend in enumerate(dados["tendencias_do_dia"], 1):
            trafego = trafegos[i - 1] if i <= len(trafegos) else ""
            linhas.append(f" {i:2}. {trend} ({trafego})")

    # Notícias
    if "noticias" in dados and dados["noticias"]:
        linhas.append("")
        linhas.append(" NOTICIAS:")
        linhas.append("-" * 70)
        for i, noticia in enumerate(dados["noticias"], 1):
            titulo = noticia.get("titulo", "")[:55]
            fonte = noticia.get("fonte", "")
            linhas.append(f" {i:2}. [{fonte}] {titulo}")

    # Trending geral
    if "fontes" in dados:
        for fonte, conteudo in dados["fontes"].items():
            linhas.append("")
            linhas.append(f" {fonte.upper().replace('_', ' ')}:")
            linhas.append("-" * 70)
            if isinstance(conteudo, list):
                for i, item in enumerate(conteudo[:10], 1):
                    if isinstance(item, dict):
                        titulo = item.get(
                            "titulo",
                            (
                                item.get("tendencias", [""])[0]
                                if isinstance(item.get("tendencias"), list)
                                else ""
                            ),
                        )[:55]
                        score = item.get("score") or item.get("pontos", "")
                        if score:
                            linhas.append(f" {i:2}. [{score:>6}] {titulo}")
                        else:
                            linhas.append(f" {i:2}. {titulo}")
                    else:
                        linhas.append(f" {i:2}. {str(item)[:60]}")
            elif isinstance(conteudo, dict):
                for k, v in conteudo.items():
                    if isinstance(v, list):
                        linhas.append(f"   {k}:")
                        for item in v[:5]:
                            linhas.append(f"     - {str(item)[:55]}")

    linhas.append("")
    linhas.append("=" * 70)

    return "\n".join(linhas)


def formatar_resultado_markdown(dados: dict) -> str:
    """Formata resultado como Markdown."""
    linhas = []
    plataforma = dados.get("plataforma", dados.get("tipo", "Resultado"))

    linhas.append(f"# {plataforma}")
    linhas.append("")

    if dados.get("termo_buscado"):
        linhas.append(f"**Termo:** {dados['termo_buscado']}")
    linhas.append(
        f"**Data:** {dados.get('data_consulta', datetime.now().strftime('%Y-%m-%d %H:%M'))}"
    )
    linhas.append("")

    # Posts
    if "posts" in dados and dados["posts"]:
        linhas.append("## Top Posts")
        linhas.append("")
        linhas.append("| # | Score | Título |")
        linhas.append("|---|-------|--------|")
        for i, post in enumerate(dados["posts"][:10], 1):
            titulo = post.get("titulo", "")[:50].replace("|", "\\|")
            score = post.get("score") or post.get("pontos", 0)
            linhas.append(f"| {i} | {score} | {titulo} |")
        linhas.append("")

        if "metricas" in dados:
            linhas.append("### Métricas")
            for k, v in dados["metricas"].items():
                linhas.append(f"- **{k}:** {v}")
            linhas.append("")

    # Vídeos
    if "videos" in dados and dados["videos"]:
        linhas.append("## Top Vídeos")
        linhas.append("")
        for i, video in enumerate(dados["videos"][:10], 1):
            linhas.append(f"{i}. **{video.get('titulo', '')}**")
            linhas.append(f"   - Canal: {video.get('canal', '')}")
            linhas.append(f"   - Views: {video.get('visualizacoes', '')}")
            linhas.append(f"   - [Assistir]({video.get('url', '')})")
            linhas.append("")

    # Sugestões
    if "sugestoes_busca" in dados and dados["sugestoes_busca"]:
        linhas.append("## Sugestões de Busca")
        linhas.append("")
        for sugestao in dados["sugestoes_busca"]:
            linhas.append(f"- {sugestao}")
        linhas.append("")

    # Tendências do dia
    if "tendencias_do_dia" in dados and dados["tendencias_do_dia"]:
        linhas.append("## Tendências do Dia")
        linhas.append("")
        trafegos = dados.get("trafego_aproximado", [])
        for i, trend in enumerate(dados["tendencias_do_dia"], 1):
            trafego = trafegos[i - 1] if i <= len(trafegos) else ""
            linhas.append(f"{i}. **{trend}** ({trafego})")
        linhas.append("")

    # Notícias
    if "noticias" in dados and dados["noticias"]:
        linhas.append("## Notícias")
        linhas.append("")
        for noticia in dados["noticias"]:
            linhas.append(
                f"- [{noticia.get('titulo', '')}]({noticia.get('url', '')}) - *{noticia.get('fonte', '')}*"
            )
        linhas.append("")

    # Trending geral
    if "fontes" in dados:
        for fonte, conteudo in dados["fontes"].items():
            linhas.append(f"## {fonte.replace('_', ' ').title()}")
            linhas.append("")
            if isinstance(conteudo, list):
                for item in conteudo[:10]:
                    if isinstance(item, dict):
                        titulo = item.get("titulo", "")
                        score = item.get("score") or item.get("pontos", "")
                        if score:
                            linhas.append(f"- **{titulo}** (score: {score})")
                        else:
                            linhas.append(f"- {titulo}")
                    else:
                        linhas.append(f"- {item}")
            linhas.append("")

    return "\n".join(linhas)


def mostrar_ajuda() -> None:
    """Mostra ajuda de uso."""
    ajuda = """
TREND TRACKER - Monitorador de Tendências
==========================================

Monitora tendências em tempo real de múltiplas plataformas.

USO:
    python trend_tracker.py "termo" [plataformas] [opcoes]

PLATAFORMAS DISPONIVEIS:
    google      - Google Trends e sugestões de busca
    reddit      - Posts populares do Reddit
    youtube     - Vídeos populares do YouTube
    hackernews  - Posts do Hacker News
    noticias    - Notícias de tecnologia (RSS)
    todas       - Todas as plataformas acima

OPCOES:
    --periodo N      - Período em dias (padrão: 7)
    --formato F      - Formato de saída: json, markdown, tabela (padrão: tabela)
    --regiao R       - Código da região (padrão: BR)
    --trending       - Mostra trending topics gerais (sem termo de busca)

EXEMPLOS:
    # Buscar tendências sobre IA no Google e Reddit
    python trend_tracker.py "inteligencia artificial" google,reddit

    # Buscar em todas as plataformas
    python trend_tracker.py "marketing digital" todas

    # Obter trending topics do Brasil
    python trend_tracker.py --trending brasil

    # Saída em JSON
    python trend_tracker.py "python" todas --formato json

    # Saída em Markdown
    python trend_tracker.py "startup" hackernews --formato markdown

NOTAS:
    - Algumas APIs requerem autenticação para dados completos
    - Os dados do Twitter/X são aproximados devido a limitações de API
    - Use --formato json para integração com outras ferramentas
"""
    print(ajuda)


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help", "help"]:
        mostrar_ajuda()
        return

    # Parsear argumentos
    args = sys.argv[1:]
    termo = ""
    plataformas = ["google", "reddit"]
    formato = "tabela"
    periodo = 7
    regiao = "BR"
    modo_trending = False

    i = 0
    while i < len(args):
        arg = args[i]

        if arg == "--trending":
            modo_trending = True
            if i + 1 < len(args) and not args[i + 1].startswith("--"):
                regiao = args[i + 1].upper()
                i += 1
        elif arg == "--formato" and i + 1 < len(args):
            formato = args[i + 1].lower()
            i += 1
        elif arg == "--periodo" and i + 1 < len(args):
            periodo = int(args[i + 1])
            i += 1
        elif arg == "--regiao" and i + 1 < len(args):
            regiao = args[i + 1].upper()
            i += 1
        elif arg.startswith("--"):
            pass  # Ignorar flags desconhecidas
        elif not termo:
            termo = arg
        else:
            # Plataformas
            plataformas_str = arg.lower()
            if plataformas_str == "todas":
                plataformas = ["google", "reddit", "youtube", "hackernews", "noticias"]
            else:
                plataformas = [p.strip() for p in plataformas_str.split(",")]

        i += 1

    # Executar
    resultados_totais = []

    if modo_trending:
        print(f"Buscando trending topics para {regiao}...", file=sys.stderr)
        resultado = obter_trending_geral(regiao)
        resultados_totais.append(resultado)
    else:
        if not termo:
            print("Erro: Forneça um termo de busca ou use --trending", file=sys.stderr)
            mostrar_ajuda()
            return

        print(f"Buscando tendências para '{termo}'...", file=sys.stderr)

        periodo_reddit = (
            "week" if periodo <= 7 else ("month" if periodo <= 30 else "year")
        )

        for plataforma in plataformas:
            plataforma = plataforma.lower().strip()
            print(f"  Consultando {plataforma}...", file=sys.stderr)

            if plataforma == "google":
                resultado = buscar_google_trends(termo, regiao)
            elif plataforma == "reddit":
                resultado = buscar_reddit(termo, "all", 10, periodo_reddit)
            elif plataforma == "youtube":
                resultado = buscar_youtube_trends(termo, regiao)
            elif plataforma in ["hackernews", "hn"]:
                resultado = buscar_hacker_news(termo)
            elif plataforma in ["noticias", "news"]:
                resultado = buscar_noticias_tech(termo)
            elif plataforma in ["twitter", "x"]:
                resultado = buscar_twitter_trends(regiao)
            else:
                print(f"  Plataforma '{plataforma}' não reconhecida", file=sys.stderr)
                continue

            resultados_totais.append(resultado)

    # Formatar saída
    print("", file=sys.stderr)  # Linha em branco

    if formato == "json":
        if len(resultados_totais) == 1:
            print(json.dumps(resultados_totais[0], ensure_ascii=False, indent=2))
        else:
            print(
                json.dumps(
                    {"resultados": resultados_totais}, ensure_ascii=False, indent=2
                )
            )
    elif formato == "markdown":
        for resultado in resultados_totais:
            print(formatar_resultado_markdown(resultado))
            print("\n---\n")
    else:  # tabela
        for resultado in resultados_totais:
            print(formatar_resultado_tabela(resultado))
            print()


if __name__ == "__main__":
    main()
