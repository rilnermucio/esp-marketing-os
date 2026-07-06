#!/usr/bin/env python3
"""
MOS - Marketing OS CLI Unificado

Interface unificada para todos os scripts de automação do Marketing OS.

Uso:
    python mos.py seo analyze artigo.md "keyword"
    python mos.py headlines score "Sua headline aqui"
    python mos.py headlines compare "Headline A" "Headline B"
    python mos.py hooks generate "tema" reels 10
    python mos.py hashtags generate nicho plataforma
    python mos.py content ideas tecnologia 20
    python mos.py content audit arquivo.md --tipo blog
    python mos.py content calendar 2026-03-01 4 instagram linkedin
    python mos.py content repurpose --file artigo.txt --output todos
    python mos.py reels script "tema" 30 tutorial
    python mos.py carousel structure "tema" educativo 10
    python mos.py trends track "termo" google,reddit --periodo 7
    python mos.py trends adapt "trend" nicho
    python mos.py trends tiktok --hashtag "marketing" --min-views 1000000
    python mos.py competitor analyze "@perfil1" "@perfil2"
    python mos.py readability check --file artigo.txt
    python mos.py ab generate headline "texto original"
    python mos.py captions generate "tema" engajamento
    python mos.py quality check arquivo.md --type post
    python mos.py project novo "Nome do Projeto" --tipo lancamento
    python mos.py project list
    python mos.py project status slug
    python mos.py project avancar slug
    python mos.py project aprovar slug
    python mos.py project rejeitar slug "feedback"
"""

import os
import sys
import subprocess
from typing import Callable, Dict, List, Tuple

# Diretório dos scripts
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

# Mapeamento de comandos para scripts
COMMAND_MAP: Dict[str, Dict[str, Tuple[str, str]]] = {
    "seo": {
        "analyze": ("seo_analyzer.py", "Analisa conteúdo para SEO"),
    },
    "headlines": {
        "score": ("headline_scorer.py", "Pontua headlines por poder emocional"),
        "compare": ("headline_scorer.py", "Compara múltiplas headlines"),
    },
    "hooks": {
        "generate": ("hook_generator.py", "Gera hooks virais"),
        "variants": ("hook_variant_generator.py", "Gera variações de hooks"),
    },
    "hashtags": {
        "generate": ("hashtag_generator.py", "Gera hashtags por nicho"),
        "research": ("instagram_hashtag_research.py", "Pesquisa avançada de hashtags"),
    },
    "content": {
        "ideas": ("content_idea_generator.py", "Gera ideias de conteúdo"),
        "audit": ("content_audit.py", "Audita conteúdo existente"),
        "calendar": ("content_calendar.py", "Cria calendário editorial"),
        "repurpose": ("content_repurposer.py", "Adapta conteúdo entre plataformas"),
    },
    "reels": {
        "script": ("reels_script_generator.py", "Gera roteiros para Reels"),
    },
    "carousel": {
        "structure": (
            "carousel_structure_generator.py",
            "Gera estruturas de carrossel",
        ),
    },
    "trends": {
        "track": ("trend_tracker.py", "Monitora tendências"),
        "adapt": ("trend_adapter.py", "Adapta trends para nichos"),
        "tiktok": ("tiktok_trends_scraper.py", "Busca trends do TikTok"),
    },
    "competitor": {
        "analyze": ("competitor_analyzer.py", "Analisa perfis de concorrentes"),
    },
    "readability": {
        "check": ("readability_checker.py", "Verifica legibilidade de texto"),
    },
    "ab": {
        "generate": ("ab_generator.py", "Gera variações A/B"),
    },
    "captions": {
        "generate": ("caption_generator.py", "Gera legendas para Instagram"),
    },
    "quality": {
        "check": ("quality_gate.py", "Valida qualidade do conteúdo"),
    },
    "project": {
        "novo": (
            "project_manager.py",
            "Cria novo projeto (--tipo lancamento|perpetuo|consultoria|mentoria)",
        ),
        "list": ("project_manager.py", "Lista projetos"),
        "status": ("project_manager.py", "Status de um projeto"),
        "avancar": ("project_manager.py", "Cria run pendente + auto-mkdir do stage"),
        "completar": (
            "project_manager.py",
            "Marca run pending como pending_approval (com output path)",
        ),
        "aprovar": ("project_manager.py", "Aprova ultimo run e avanca stage"),
        "rejeitar": ("project_manager.py", "Rejeita ultimo run com feedback"),
    },
    "apify": {
        "serp": (
            "apify_serp.py",
            "SERP scraping via Apify (opcional, requer APIFY_TOKEN)",
        ),
        "instagram": (
            "apify_instagram.py",
            "Instagram profile scraping via Apify (opcional)",
        ),
        "meta-ads": (
            "apify_meta_ads.py",
            "Meta Ad Library scraping (Facebook + Instagram, opcional)",
        ),
        "tiktok": ("apify_tiktok.py", "TikTok profile scraping (opcional)"),
        "youtube": ("apify_youtube.py", "YouTube channel scraping (opcional)"),
    },
    "youtube": {
        "channel": (
            "youtube_analytics.py",
            "Métricas gerais do canal (requer YouTube API)",
        ),
        "videos": ("youtube_analytics.py", "Lista de vídeos com métricas"),
        "top-videos": ("youtube_analytics.py", "Vídeos com melhor performance"),
        "demographics": ("youtube_analytics.py", "Dados demográficos da audiência"),
        "traffic-sources": ("youtube_analytics.py", "Fontes de tráfego do canal"),
        "full-report": ("youtube_analytics.py", "Relatório completo do canal"),
    },
    "gsc": {
        "queries": (
            "gsc_analyzer.py",
            "Principais queries de busca (requer Search Console API)",
        ),
        "top-pages": ("gsc_analyzer.py", "Páginas com melhor performance"),
        "ctr-opportunities": ("gsc_analyzer.py", "Oportunidades de CTR"),
        "position-changes": ("gsc_analyzer.py", "Variações de posição"),
        "full-report": ("gsc_analyzer.py", "Relatório completo do site"),
    },
    "report": {
        "weekly": ("weekly_report.py", "Relatório semanal consolidado"),
    },
    "seasonal": {
        "list": ("seasonal_calendar_br.py", "Calendário sazonal comercial BR"),
    },
    "audio": {
        "narrate": ("tts_runner.py", "Narra roteiro em áudio PT-BR (say/kokoro)"),
    },
    "thumbnail": {
        "compose": (
            "thumbnail_composer.py",
            "Compõe thumbnail 1280x720 com overlay tipográfico",
        ),
    },
    "memory": {
        "write": (
            "memory_writer.py",
            "Persiste aprendizado na memory opt-in do agent",
        ),
    },
    "metrics": {
        "summarize": (
            "metrics_collector.py",
            "Resume métricas para o loop /aprender",
        ),
    },
}

# Comandos especiais que precisam de argumentos transformados
SPECIAL_ARGS: Dict[Tuple[str, str], Callable[[List[str]], List[str]]] = {
    ("headlines", "compare"): lambda args: ["--compare"] + args,
    ("readability", "check"): lambda args: args,  # já é passthrough
    ("project", "novo"): lambda args: ["novo"] + args,
    ("project", "list"): lambda args: ["list"] + args,
    ("project", "status"): lambda args: ["status"] + args,
    ("project", "avancar"): lambda args: ["avancar"] + args,
    ("project", "completar"): lambda args: ["completar"] + args,
    ("project", "aprovar"): lambda args: ["aprovar"] + args,
    ("project", "rejeitar"): lambda args: ["rejeitar"] + args,
}

# Categorias cujo script tem subparser próprio (dest="comando"): o comando do mos
# precisa ser repassado como 1º argumento posicional pro parser interno do script.
_PASSTHROUGH_SUBCOMMANDS: Dict[str, List[str]] = {
    "youtube": [
        "channel",
        "videos",
        "top-videos",
        "demographics",
        "traffic-sources",
        "full-report",
    ],
    "gsc": [
        "queries",
        "top-pages",
        "ctr-opportunities",
        "position-changes",
        "full-report",
    ],
}
for _cat, _cmds in _PASSTHROUGH_SUBCOMMANDS.items():
    for _cmd in _cmds:
        # bind _cmd por valor pra cada lambda não capturar a variável de loop
        SPECIAL_ARGS[(_cat, _cmd)] = (lambda c: lambda args: [c] + args)(_cmd)


def print_help() -> None:
    """Exibe ajuda completa."""
    print("""
╔══════════════════════════════════════════════════════════╗
║              MOS — Marketing OS CLI                     ║
║         Interface unificada de automação                ║
╚══════════════════════════════════════════════════════════╝

Uso: python mos.py <categoria> <comando> [argumentos...]

CATEGORIAS E COMANDOS:
""")

    for category, commands in COMMAND_MAP.items():
        print(f"  {category}")
        for cmd, (script, desc) in commands.items():
            print(f"    {cmd:15s} {desc}")
        print()

    print("""EXEMPLOS:

  Análise e Otimização:
    mos seo analyze artigo.md "marketing digital"
    mos headlines score "7 segredos que ninguém conta"
    mos headlines compare "Headline A" "Headline B"
    mos readability check --file artigo.txt
    mos quality check post.md --type post

  Geração de Conteúdo:
    mos hooks generate "produtividade" reels 10
    mos content ideas tecnologia 20
    mos reels script "IA no marketing" 30 tutorial
    mos carousel structure "dicas de SEO" educativo 10
    mos captions generate "tema" engajamento
    mos ab generate headline "Aprenda marketing digital"

  Redes Sociais:
    mos hashtags generate marketing instagram
    mos hashtags research "nicho" --gerar-set

  Planejamento:
    mos content calendar 2026-03-01 4 instagram linkedin
    mos content repurpose --file artigo.txt --output todos

  Tendências:
    mos trends track "IA" google,reddit --periodo 7
    mos trends adapt "get ready with me" marketing
    mos trends tiktok --hashtag "marketing" --min-views 1000000

  Concorrência:
    mos competitor analyze "@perfil1" "@perfil2"

  Apify (opcional, requer APIFY_TOKEN):
    mos apify serp "infoproduto bofu" --max-results 10
    mos apify instagram @concorrente --max-posts 30 --dry-run
    mos apify meta-ads --query "hotmart" --country BR --max-ads 30
    mos apify tiktok --handle @usuario --max-videos 30
    mos apify youtube --channel @mrbeast --max-videos 20

  Projetos:
    mos project novo "Lançamento Curso" --tipo lancamento
    mos project list
    mos project status lancamento-curso
    mos project avancar lancamento-curso
    mos project aprovar lancamento-curso
    mos project rejeitar lancamento-curso "feedback"

Para ajuda de um comando específico:
    python mos.py <categoria> <comando> --help
""")


def run_script(script_name: str, args: List[str]) -> None:
    """Executa um script com os argumentos fornecidos."""
    script_path = os.path.join(SCRIPTS_DIR, script_name)

    if not os.path.exists(script_path):
        print(f"\n❌ Script não encontrado: {script_name}")
        print(f"   Esperado em: {script_path}")
        sys.exit(1)

    cmd = [sys.executable, script_path] + args
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] in ["--help", "-h", "help"]:
        print_help()
        sys.exit(0)

    category = sys.argv[1]

    if category not in COMMAND_MAP:
        print(f"\n❌ Categoria desconhecida: '{category}'")
        print(f"   Categorias válidas: {', '.join(COMMAND_MAP.keys())}")
        print(f"\n   Use: python mos.py --help")
        sys.exit(1)

    if len(sys.argv) < 3:
        print(f"\n📂 Comandos disponíveis para '{category}':")
        for cmd, (script, desc) in COMMAND_MAP[category].items():
            print(f"   {cmd:15s} {desc}")
        print(f"\n   Uso: python mos.py {category} <comando> [argumentos...]")
        sys.exit(1)

    command = sys.argv[2]

    if command not in COMMAND_MAP[category]:
        print(f"\n❌ Comando desconhecido: '{category} {command}'")
        print(
            f"   Comandos válidos para '{category}': {', '.join(COMMAND_MAP[category].keys())}"
        )
        sys.exit(1)

    script_name, description = COMMAND_MAP[category][command]
    extra_args = sys.argv[3:]

    # Aplicar transformação de argumentos se necessário
    key = (category, command)
    if key in SPECIAL_ARGS:
        extra_args = SPECIAL_ARGS[key](extra_args)

    run_script(script_name, extra_args)


if __name__ == "__main__":
    main()
