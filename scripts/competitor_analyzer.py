#!/usr/bin/env python3
"""
Competitor Analyzer - Analisar perfis de concorrentes e extrair insights
Analisa presença digital, conteúdo, engajamento e identifica oportunidades.

Uso:
    python competitor_analyzer.py "concorrente1" "concorrente2" [--plataforma instagram|youtube|linkedin|twitter]
    python competitor_analyzer.py --arquivo concorrentes.txt [--formato json|markdown|tabela]
    python competitor_analyzer.py "marca" --comparar "seu_perfil"

Exemplos:
    python competitor_analyzer.py "@marketingbrasil" "@socialmediaexpert"
    python competitor_analyzer.py "canal_youtube1" "canal_youtube2" --plataforma youtube
    python competitor_analyzer.py --arquivo lista.txt --formato markdown
"""

import sys
import json
import re
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from collections import Counter
import ssl

# Configuração SSL
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


def fazer_requisicao(url: str, headers: Optional[dict] = None, timeout: int = 15) -> Optional[str]:
    """Faz requisição HTTP e retorna o conteúdo."""
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
        req.add_header('Accept-Language', 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7')
        if headers:
            for key, value in headers.items():
                req.add_header(key, value)

        with urllib.request.urlopen(req, timeout=timeout, context=ssl_context) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return None


def analisar_instagram(username: str) -> dict:
    """
    Analisa perfil do Instagram via dados públicos.
    Nota: Instagram limita acesso a dados públicos, então usamos heurísticas.
    """
    username = username.lstrip('@')

    resultado = {
        "plataforma": "Instagram",
        "username": f"@{username}",
        "url": f"https://instagram.com/{username}",
        "data_analise": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "metricas": {},
        "conteudo": {},
        "insights": [],
        "status": "sucesso"
    }

    try:
        # Tentar buscar página pública
        url = f"https://www.instagram.com/{username}/"
        resposta = fazer_requisicao(url)

        if resposta:
            # Extrair dados do JSON embutido
            match = re.search(r'<script type="application/ld\+json">(.*?)</script>', resposta, re.DOTALL)
            if match:
                try:
                    dados = json.loads(match.group(1))
                    if isinstance(dados, dict):
                        resultado["metricas"]["nome"] = dados.get("name", "")
                        resultado["metricas"]["descricao"] = dados.get("description", "")[:200] if dados.get("description") else ""
                except:
                    pass

            # Extrair seguidores se disponível
            seguidores_match = re.search(r'"edge_followed_by":\{"count":(\d+)\}', resposta)
            if seguidores_match:
                resultado["metricas"]["seguidores"] = int(seguidores_match.group(1))

            seguindo_match = re.search(r'"edge_follow":\{"count":(\d+)\}', resposta)
            if seguindo_match:
                resultado["metricas"]["seguindo"] = int(seguindo_match.group(1))

            posts_match = re.search(r'"edge_owner_to_timeline_media":\{"count":(\d+)', resposta)
            if posts_match:
                resultado["metricas"]["posts"] = int(posts_match.group(1))

            # Extrair bio
            bio_match = re.search(r'"biography":"(.*?)"', resposta)
            if bio_match:
                bio = bio_match.group(1).encode().decode('unicode_escape')
                resultado["conteudo"]["bio"] = bio[:300]

                # Analisar elementos da bio
                resultado["conteudo"]["bio_analise"] = {
                    "tem_emoji": bool(re.search(r'[\U0001F300-\U0001F9FF]', bio)),
                    "tem_cta": any(cta in bio.lower() for cta in ['link', 'clique', 'acesse', 'baixe', 'saiba']),
                    "tem_hashtag": '#' in bio,
                    "comprimento": len(bio)
                }

            # Gerar insights baseados nos dados
            if resultado["metricas"].get("seguidores") and resultado["metricas"].get("posts"):
                seg = resultado["metricas"]["seguidores"]
                posts = resultado["metricas"]["posts"]

                if seg > 0 and posts > 0:
                    resultado["insights"].append(f"Média de {seg//posts:,} seguidores por post publicado")

                if seg > 100000:
                    resultado["insights"].append("Perfil com grande audiência (100k+)")
                elif seg > 10000:
                    resultado["insights"].append("Perfil de médio porte (10k-100k)")
                else:
                    resultado["insights"].append("Perfil em crescimento (<10k)")
        else:
            resultado["status"] = "perfil_privado_ou_indisponivel"
            resultado["insights"].append("Não foi possível acessar dados públicos do perfil")

    except Exception as e:
        resultado["status"] = f"erro: {str(e)}"

    return resultado


def analisar_youtube(channel: str) -> dict:
    """
    Analisa canal do YouTube via dados públicos e RSS.
    """
    resultado = {
        "plataforma": "YouTube",
        "canal": channel,
        "data_analise": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "metricas": {},
        "conteudo": {
            "ultimos_videos": [],
            "temas_frequentes": [],
            "duracao_media": ""
        },
        "insights": [],
        "status": "sucesso"
    }

    try:
        # Buscar via RSS do canal
        rss_urls = [
            f"https://www.youtube.com/feeds/videos.xml?channel_id={channel}",
            f"https://www.youtube.com/feeds/videos.xml?user={channel}",
        ]

        resposta = None
        for url in rss_urls:
            resposta = fazer_requisicao(url)
            if resposta and '<feed' in resposta:
                break

        if resposta and '<feed' in resposta:
            # Extrair nome do canal
            nome_match = re.search(r'<name>(.*?)</name>', resposta)
            if nome_match:
                resultado["metricas"]["nome"] = nome_match.group(1)

            # Extrair vídeos
            entries = re.findall(r'<entry>(.*?)</entry>', resposta, re.DOTALL)

            titulos = []
            for entry in entries[:15]:
                titulo_match = re.search(r'<title>(.*?)</title>', entry)
                video_id_match = re.search(r'<yt:videoId>(.*?)</yt:videoId>', entry)
                published_match = re.search(r'<published>(.*?)</published>', entry)
                views_match = re.search(r'<media:statistics views="(\d+)"', entry)

                if titulo_match:
                    titulo = titulo_match.group(1)
                    titulos.append(titulo)

                    video_info = {
                        "titulo": titulo,
                        "video_id": video_id_match.group(1) if video_id_match else "",
                        "publicado": published_match.group(1)[:10] if published_match else "",
                        "views": int(views_match.group(1)) if views_match else 0
                    }
                    resultado["conteudo"]["ultimos_videos"].append(video_info)

            # Analisar títulos para identificar padrões
            if titulos:
                # Palavras mais frequentes (excluindo stop words)
                stop_words = {'de', 'da', 'do', 'em', 'para', 'com', 'que', 'o', 'a', 'os', 'as', 'e', 'é', 'um', 'uma', 'como', 'mais', 'seu', 'sua'}
                todas_palavras = []
                for titulo in titulos:
                    palavras = re.findall(r'\b\w{4,}\b', titulo.lower())
                    todas_palavras.extend([p for p in palavras if p not in stop_words])

                contador = Counter(todas_palavras)
                resultado["conteudo"]["temas_frequentes"] = [
                    {"tema": tema, "ocorrencias": count}
                    for tema, count in contador.most_common(10)
                ]

                # Padrões de títulos
                resultado["conteudo"]["padroes_titulo"] = {
                    "com_numeros": sum(1 for t in titulos if re.search(r'\d', t)),
                    "com_pergunta": sum(1 for t in titulos if '?' in t),
                    "com_como": sum(1 for t in titulos if 'como' in t.lower()),
                    "comprimento_medio": sum(len(t) for t in titulos) // len(titulos)
                }

                # Calcular métricas de views
                videos_com_views = [v for v in resultado["conteudo"]["ultimos_videos"] if v["views"] > 0]
                if videos_com_views:
                    total_views = sum(v["views"] for v in videos_com_views)
                    resultado["metricas"]["views_total_recentes"] = total_views
                    resultado["metricas"]["views_medio"] = total_views // len(videos_com_views)
                    resultado["metricas"]["videos_analisados"] = len(videos_com_views)

            # Gerar insights
            if resultado["conteudo"]["ultimos_videos"]:
                n_videos = len(resultado["conteudo"]["ultimos_videos"])
                resultado["insights"].append(f"Canal publica ativamente ({n_videos} vídeos recentes analisados)")

                if resultado["conteudo"]["padroes_titulo"]["com_numeros"] > n_videos * 0.3:
                    resultado["insights"].append("Usa números nos títulos frequentemente (boa prática)")

                if resultado["conteudo"]["padroes_titulo"]["com_pergunta"] > n_videos * 0.2:
                    resultado["insights"].append("Usa perguntas nos títulos (gera curiosidade)")

                if resultado["metricas"].get("views_medio"):
                    views_medio = resultado["metricas"]["views_medio"]
                    if views_medio > 100000:
                        resultado["insights"].append(f"Alta performance: média de {views_medio:,} views por vídeo")
                    elif views_medio > 10000:
                        resultado["insights"].append(f"Boa performance: média de {views_medio:,} views por vídeo")
        else:
            # Tentar buscar pela página do canal
            resultado["status"] = "canal_nao_encontrado_via_rss"
            resultado["insights"].append("Use o ID do canal (começa com UC) para melhores resultados")

    except Exception as e:
        resultado["status"] = f"erro: {str(e)}"

    return resultado


def analisar_twitter(username: str) -> dict:
    """
    Analisa perfil do Twitter/X.
    Nota: APIs públicas limitadas, retorna orientações.
    """
    username = username.lstrip('@')

    resultado = {
        "plataforma": "Twitter/X",
        "username": f"@{username}",
        "url": f"https://twitter.com/{username}",
        "data_analise": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "metricas": {},
        "conteudo": {},
        "insights": [],
        "status": "limitado",
        "nota": "Twitter/X restringe acesso a dados públicos. Use ferramentas oficiais ou APIs autenticadas."
    }

    resultado["alternativas"] = {
        "twitter_analytics": "Acesse analytics.twitter.com para dados do seu perfil",
        "socialblade": f"https://socialblade.com/twitter/user/{username}",
        "tweetdeck": "Use TweetDeck para monitoramento em tempo real",
        "api_oficial": "API v2 requer autenticação para dados detalhados"
    }

    resultado["insights"] = [
        "Para análise completa, use Twitter Analytics (perfil próprio) ou API oficial",
        "Monitore manualmente: frequência de posts, horários, tipos de conteúdo",
        "Observe: tom de voz, hashtags usadas, engajamento nos replies"
    ]

    return resultado


def analisar_linkedin(perfil: str) -> dict:
    """
    Analisa perfil/página do LinkedIn.
    Nota: LinkedIn restringe scraping, retorna orientações.
    """
    resultado = {
        "plataforma": "LinkedIn",
        "perfil": perfil,
        "url": f"https://linkedin.com/in/{perfil}" if not perfil.startswith('http') else perfil,
        "data_analise": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "metricas": {},
        "conteudo": {},
        "insights": [],
        "status": "limitado",
        "nota": "LinkedIn restringe acesso a dados públicos. Análise manual recomendada."
    }

    resultado["checklist_analise_manual"] = {
        "perfil_pessoal": [
            "Foto profissional (rosto visível, fundo neutro)",
            "Headline com proposta de valor clara",
            "Seção 'Sobre' completa e com keywords",
            "Experiências detalhadas com resultados",
            "Recomendações de terceiros",
            "Certificações e cursos listados",
            "Conteúdo publicado (artigos, posts)"
        ],
        "pagina_empresa": [
            "Logo e banner profissionais",
            "Descrição com keywords do setor",
            "Frequência de publicação",
            "Engajamento nos posts (comentários, compartilhamentos)",
            "Showcase pages para produtos/serviços",
            "Employee advocacy (funcionários compartilhando)"
        ]
    }

    resultado["metricas_para_observar"] = [
        "Número de conexões/seguidores",
        "Média de reações por post",
        "Comentários por post (mais valioso que curtidas)",
        "Frequência de publicação",
        "Tipos de conteúdo (texto, carrossel, vídeo, artigo)",
        "Horários de publicação"
    ]

    resultado["insights"] = [
        "Acesse o perfil diretamente para análise visual",
        "Use LinkedIn Sales Navigator para dados mais completos",
        "Observe padrões de conteúdo que geram mais engajamento"
    ]

    return resultado


def analisar_site(url: str) -> dict:
    """
    Analisa presença web/site do concorrente.
    """
    if not url.startswith('http'):
        url = f"https://{url}"

    resultado = {
        "tipo": "Website",
        "url": url,
        "data_analise": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "seo": {},
        "conteudo": {},
        "tecnologia": {},
        "insights": [],
        "status": "sucesso"
    }

    try:
        resposta = fazer_requisicao(url)

        if resposta:
            # Extrair título
            titulo_match = re.search(r'<title[^>]*>(.*?)</title>', resposta, re.IGNORECASE | re.DOTALL)
            if titulo_match:
                resultado["seo"]["titulo"] = titulo_match.group(1).strip()[:100]

            # Extrair meta description
            desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', resposta, re.IGNORECASE)
            if desc_match:
                resultado["seo"]["meta_description"] = desc_match.group(1)[:200]

            # Verificar elementos SEO
            resultado["seo"]["tem_og_tags"] = 'og:' in resposta.lower()
            resultado["seo"]["tem_twitter_cards"] = 'twitter:' in resposta.lower()
            resultado["seo"]["tem_schema"] = 'application/ld+json' in resposta.lower()
            resultado["seo"]["tem_canonical"] = 'rel="canonical"' in resposta.lower()

            # Analisar H1s
            h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', resposta, re.IGNORECASE | re.DOTALL)
            resultado["conteudo"]["h1s"] = [re.sub(r'<[^>]+>', '', h).strip()[:100] for h in h1s[:5]]

            # Detectar tecnologias
            if 'wp-content' in resposta or 'wordpress' in resposta.lower():
                resultado["tecnologia"]["cms"] = "WordPress"
            elif 'shopify' in resposta.lower():
                resultado["tecnologia"]["cms"] = "Shopify"
            elif 'wix' in resposta.lower():
                resultado["tecnologia"]["cms"] = "Wix"

            # Verificar analytics/pixels
            resultado["tecnologia"]["google_analytics"] = 'google-analytics' in resposta.lower() or 'gtag' in resposta.lower()
            resultado["tecnologia"]["facebook_pixel"] = 'fbq(' in resposta or 'facebook.net' in resposta.lower()
            resultado["tecnologia"]["hotjar"] = 'hotjar' in resposta.lower()

            # Links de redes sociais
            redes = {
                "instagram": re.search(r'instagram\.com/([a-zA-Z0-9_.]+)', resposta),
                "youtube": re.search(r'youtube\.com/(channel|c|user)/([a-zA-Z0-9_-]+)', resposta),
                "linkedin": re.search(r'linkedin\.com/(company|in)/([a-zA-Z0-9_-]+)', resposta),
                "twitter": re.search(r'twitter\.com/([a-zA-Z0-9_]+)', resposta)
            }
            resultado["conteudo"]["redes_sociais"] = {k: v.group(0) if v else None for k, v in redes.items()}

            # Gerar insights
            if not resultado["seo"].get("meta_description"):
                resultado["insights"].append("Meta description ausente - oportunidade de otimização SEO")

            if resultado["seo"]["tem_schema"]:
                resultado["insights"].append("Usa Schema markup (bom para rich snippets)")
            else:
                resultado["insights"].append("Não usa Schema markup - oportunidade de diferenciação")

            if resultado["tecnologia"]["google_analytics"]:
                resultado["insights"].append("Usa Google Analytics (mensura dados)")

            if not resultado["tecnologia"]["facebook_pixel"]:
                resultado["insights"].append("Pixel do Facebook não detectado - possível gap em remarketing")

        else:
            resultado["status"] = "site_inacessivel"

    except Exception as e:
        resultado["status"] = f"erro: {str(e)}"

    return resultado


def comparar_concorrentes(analises: List[dict]) -> dict:
    """
    Compara múltiplos concorrentes e gera análise comparativa.
    """
    comparacao = {
        "tipo": "Análise Comparativa",
        "data_analise": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "concorrentes_analisados": len(analises),
        "comparativo": {},
        "rankings": {},
        "oportunidades": [],
        "ameacas": [],
        "recomendacoes": []
    }

    # Separar por plataforma
    por_plataforma = {}
    for analise in analises:
        plataforma = analise.get("plataforma", analise.get("tipo", "Outro"))
        if plataforma not in por_plataforma:
            por_plataforma[plataforma] = []
        por_plataforma[plataforma].append(analise)

    for plataforma, concorrentes in por_plataforma.items():
        comparacao["comparativo"][plataforma] = {
            "total": len(concorrentes),
            "concorrentes": []
        }

        for conc in concorrentes:
            info = {
                "nome": conc.get("username", conc.get("canal", conc.get("url", ""))),
                "metricas": conc.get("metricas", {}),
                "status": conc.get("status", "")
            }
            comparacao["comparativo"][plataforma]["concorrentes"].append(info)

        # Rankings (se houver métricas comparáveis)
        if plataforma == "YouTube":
            com_views = [c for c in concorrentes if c.get("metricas", {}).get("views_medio")]
            if com_views:
                com_views.sort(key=lambda x: x["metricas"]["views_medio"], reverse=True)
                comparacao["rankings"][f"{plataforma}_views"] = [
                    {"canal": c.get("canal", ""), "views_medio": c["metricas"]["views_medio"]}
                    for c in com_views
                ]

    # Gerar oportunidades e recomendações
    comparacao["oportunidades"] = [
        "Identifique gaps de conteúdo que nenhum concorrente está cobrindo",
        "Analise os formatos de maior engajamento de cada concorrente",
        "Observe horários de publicação mais eficazes",
        "Encontre nichos sub-explorados dentro do seu mercado"
    ]

    comparacao["recomendacoes"] = [
        "Monitore concorrentes semanalmente para identificar tendências",
        "Documente táticas que funcionam e adapte para seu contexto",
        "Não copie - inspire-se e diferencie-se",
        "Foque em qualidade e consistência, não apenas volume"
    ]

    return comparacao


def gerar_relatorio_swot(analises: List[dict], seu_perfil: Optional[dict] = None) -> dict:
    """
    Gera análise SWOT baseada nos concorrentes.
    """
    swot = {
        "tipo": "Análise SWOT Competitiva",
        "data_analise": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "forcas": [],
        "fraquezas": [],
        "oportunidades": [],
        "ameacas": [],
        "acoes_recomendadas": []
    }

    # Analisar padrões dos concorrentes
    total_concorrentes = len(analises)

    # Oportunidades baseadas em gaps dos concorrentes
    swot["oportunidades"] = [
        "Criar conteúdo diferenciado que concorrentes não estão produzindo",
        "Explorar formatos subutilizados (ex: se todos fazem vídeos longos, fazer Shorts)",
        "Abordar subtemas negligenciados dentro do nicho",
        "Melhorar aspectos técnicos (SEO, velocidade) onde concorrentes falham"
    ]

    # Ameaças
    swot["ameacas"] = [
        "Concorrentes com maior audiência podem dominar algoritmos",
        "Novos entrantes podem trazer inovações disruptivas",
        "Saturação de conteúdo similar no mercado",
        "Mudanças de algoritmo podem beneficiar concorrentes estabelecidos"
    ]

    # Ações recomendadas
    swot["acoes_recomendadas"] = [
        {
            "prioridade": "Alta",
            "acao": "Definir proposta de valor única que diferencie da concorrência",
            "prazo": "Imediato"
        },
        {
            "prioridade": "Alta",
            "acao": "Criar calendário editorial consistente baseado em gaps identificados",
            "prazo": "1 semana"
        },
        {
            "prioridade": "Media",
            "acao": "Implementar monitoramento contínuo de concorrentes",
            "prazo": "2 semanas"
        },
        {
            "prioridade": "Media",
            "acao": "Testar formatos e abordagens que concorrentes não utilizam",
            "prazo": "1 mês"
        }
    ]

    return swot


def formatar_tabela(analises: List[dict], comparacao: Optional[dict] = None) -> str:
    """Formata resultado como tabela ASCII."""
    linhas = []

    linhas.append("=" * 80)
    linhas.append(" ANÁLISE DE CONCORRENTES")
    linhas.append("=" * 80)
    linhas.append(f" Data: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    linhas.append(f" Concorrentes analisados: {len(analises)}")
    linhas.append("-" * 80)

    for i, analise in enumerate(analises, 1):
        linhas.append("")
        plataforma = analise.get("plataforma", analise.get("tipo", ""))
        nome = analise.get("username", analise.get("canal", analise.get("url", "")))

        linhas.append(f" [{i}] {plataforma}: {nome}")
        linhas.append("-" * 40)

        # Métricas
        if analise.get("metricas"):
            linhas.append(" MÉTRICAS:")
            for k, v in analise["metricas"].items():
                if isinstance(v, int) and v > 1000:
                    v = f"{v:,}"
                linhas.append(f"   • {k}: {v}")

        # Insights
        if analise.get("insights"):
            linhas.append(" INSIGHTS:")
            for insight in analise["insights"][:5]:
                linhas.append(f"   → {insight}")

        # Status
        if analise.get("status") != "sucesso":
            linhas.append(f" STATUS: {analise.get('status', 'desconhecido')}")

    # Comparação
    if comparacao:
        linhas.append("")
        linhas.append("=" * 80)
        linhas.append(" ANÁLISE COMPARATIVA")
        linhas.append("=" * 80)

        if comparacao.get("oportunidades"):
            linhas.append(" OPORTUNIDADES:")
            for op in comparacao["oportunidades"]:
                linhas.append(f"   ✓ {op}")

        if comparacao.get("recomendacoes"):
            linhas.append(" RECOMENDAÇÕES:")
            for rec in comparacao["recomendacoes"]:
                linhas.append(f"   → {rec}")

    linhas.append("")
    linhas.append("=" * 80)

    return "\n".join(linhas)


def formatar_markdown(analises: List[dict], comparacao: Optional[dict] = None) -> str:
    """Formata resultado como Markdown."""
    linhas = []

    linhas.append("# Análise de Concorrentes")
    linhas.append("")
    linhas.append(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    linhas.append(f"**Concorrentes analisados:** {len(analises)}")
    linhas.append("")
    linhas.append("---")

    for i, analise in enumerate(analises, 1):
        plataforma = analise.get("plataforma", analise.get("tipo", ""))
        nome = analise.get("username", analise.get("canal", analise.get("url", "")))

        linhas.append("")
        linhas.append(f"## {i}. {nome}")
        linhas.append(f"**Plataforma:** {plataforma}")

        if analise.get("url"):
            linhas.append(f"**URL:** {analise['url']}")
        linhas.append("")

        # Métricas
        if analise.get("metricas"):
            linhas.append("### Métricas")
            linhas.append("")
            linhas.append("| Métrica | Valor |")
            linhas.append("|---------|-------|")
            for k, v in analise["metricas"].items():
                if isinstance(v, int) and v > 1000:
                    v = f"{v:,}"
                linhas.append(f"| {k} | {v} |")
            linhas.append("")

        # Conteúdo
        if analise.get("conteudo"):
            linhas.append("### Análise de Conteúdo")
            linhas.append("")
            for k, v in analise["conteudo"].items():
                if isinstance(v, list) and v:
                    linhas.append(f"**{k}:**")
                    for item in v[:5]:
                        if isinstance(item, dict):
                            linhas.append(f"- {item}")
                        else:
                            linhas.append(f"- {item}")
                elif isinstance(v, dict):
                    linhas.append(f"**{k}:** {v}")
                elif v:
                    linhas.append(f"**{k}:** {v}")
            linhas.append("")

        # Insights
        if analise.get("insights"):
            linhas.append("### Insights")
            linhas.append("")
            for insight in analise["insights"]:
                linhas.append(f"- {insight}")
            linhas.append("")

    # Comparação
    if comparacao:
        linhas.append("---")
        linhas.append("")
        linhas.append("## Análise Comparativa")
        linhas.append("")

        if comparacao.get("oportunidades"):
            linhas.append("### Oportunidades")
            for op in comparacao["oportunidades"]:
                linhas.append(f"- ✅ {op}")
            linhas.append("")

        if comparacao.get("recomendacoes"):
            linhas.append("### Recomendações")
            for rec in comparacao["recomendacoes"]:
                linhas.append(f"- 💡 {rec}")
            linhas.append("")

    return "\n".join(linhas)


def mostrar_ajuda() -> None:
    """Mostra ajuda de uso."""
    ajuda = """
COMPETITOR ANALYZER - Análise de Concorrentes
==============================================

Analisa perfis de concorrentes em múltiplas plataformas e gera insights.

USO:
    python competitor_analyzer.py "concorrente1" "concorrente2" [opções]

PLATAFORMAS:
    instagram   - Perfis do Instagram (@username)
    youtube     - Canais do YouTube (ID do canal ou username)
    twitter     - Perfis do Twitter/X (@username)
    linkedin    - Perfis/páginas do LinkedIn
    site        - Sites/URLs

OPÇÕES:
    --plataforma P    - Especificar plataforma (instagram, youtube, twitter, linkedin, site)
    --arquivo FILE    - Ler concorrentes de arquivo (um por linha)
    --formato F       - Formato de saída: json, markdown, tabela (padrão)
    --comparar PERFIL - Comparar com seu perfil
    --swot            - Gerar análise SWOT

EXEMPLOS:
    # Analisar perfis do Instagram
    python competitor_analyzer.py "@marketingbrasil" "@socialmediaexpert" --plataforma instagram

    # Analisar canais do YouTube
    python competitor_analyzer.py "UCxxxx" "UCyyyy" --plataforma youtube

    # Analisar sites
    python competitor_analyzer.py "concorrente1.com" "concorrente2.com" --plataforma site

    # Ler de arquivo e gerar markdown
    python competitor_analyzer.py --arquivo concorrentes.txt --formato markdown

    # Gerar análise SWOT
    python competitor_analyzer.py "@conc1" "@conc2" --plataforma instagram --swot

NOTAS:
    - Algumas plataformas limitam acesso a dados públicos
    - Para dados completos, use APIs oficiais ou ferramentas especializadas
    - A análise é baseada em dados públicos disponíveis no momento
"""
    print(ajuda)


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help', 'help']:
        mostrar_ajuda()
        return

    # Parsear argumentos
    args = sys.argv[1:]
    concorrentes = []
    plataforma = "auto"
    formato = "tabela"
    arquivo = None
    gerar_swot = False
    seu_perfil = None

    i = 0
    while i < len(args):
        arg = args[i]

        if arg == "--plataforma" and i + 1 < len(args):
            plataforma = args[i + 1].lower()
            i += 1
        elif arg == "--formato" and i + 1 < len(args):
            formato = args[i + 1].lower()
            i += 1
        elif arg == "--arquivo" and i + 1 < len(args):
            arquivo = args[i + 1]
            i += 1
        elif arg == "--comparar" and i + 1 < len(args):
            seu_perfil = args[i + 1]
            i += 1
        elif arg == "--swot":
            gerar_swot = True
        elif not arg.startswith("--"):
            concorrentes.append(arg)

        i += 1

    # Ler de arquivo se especificado
    if arquivo:
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                for linha in f:
                    linha = linha.strip()
                    if linha and not linha.startswith('#'):
                        concorrentes.append(linha)
        except FileNotFoundError:
            print(f"Erro: Arquivo '{arquivo}' não encontrado", file=sys.stderr)
            return

    if not concorrentes:
        print("Erro: Nenhum concorrente especificado", file=sys.stderr)
        mostrar_ajuda()
        return

    # Analisar concorrentes
    print(f"Analisando {len(concorrentes)} concorrente(s)...", file=sys.stderr)

    analises = []
    for conc in concorrentes:
        print(f"  → {conc}...", file=sys.stderr)

        # Detectar plataforma automaticamente se não especificada
        plat_efetiva = plataforma
        if plataforma == "auto":
            if conc.startswith('@') or 'instagram' in conc:
                plat_efetiva = "instagram"
            elif 'youtube' in conc or conc.startswith('UC'):
                plat_efetiva = "youtube"
            elif 'twitter' in conc or 'x.com' in conc:
                plat_efetiva = "twitter"
            elif 'linkedin' in conc:
                plat_efetiva = "linkedin"
            elif '.' in conc:
                plat_efetiva = "site"
            else:
                plat_efetiva = "instagram"  # default

        # Executar análise
        if plat_efetiva == "instagram":
            analise = analisar_instagram(conc)
        elif plat_efetiva == "youtube":
            analise = analisar_youtube(conc)
        elif plat_efetiva == "twitter":
            analise = analisar_twitter(conc)
        elif plat_efetiva == "linkedin":
            analise = analisar_linkedin(conc)
        elif plat_efetiva == "site":
            analise = analisar_site(conc)
        else:
            analise = {"erro": f"Plataforma '{plat_efetiva}' não suportada"}

        analises.append(analise)

    # Gerar comparação
    comparacao = None
    if len(analises) > 1:
        comparacao = comparar_concorrentes(analises)

    # Gerar SWOT se solicitado
    swot = None
    if gerar_swot:
        swot = gerar_relatorio_swot(analises)

    # Formatar saída
    print("", file=sys.stderr)

    if formato == "json":
        resultado = {
            "analises": analises,
            "comparacao": comparacao,
            "swot": swot
        }
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    elif formato == "markdown":
        print(formatar_markdown(analises, comparacao))
        if swot:
            print("\n## Análise SWOT\n")
            print(json.dumps(swot, ensure_ascii=False, indent=2))
    else:
        print(formatar_tabela(analises, comparacao))
        if swot:
            print("\n" + "=" * 80)
            print(" ANÁLISE SWOT")
            print("=" * 80)
            for categoria in ["forcas", "fraquezas", "oportunidades", "ameacas"]:
                if swot.get(categoria):
                    print(f"\n {categoria.upper()}:")
                    for item in swot[categoria]:
                        print(f"   • {item}")


if __name__ == "__main__":
    main()
