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
    python mos.py project create "Nome do Projeto" --type launch
    python mos.py project list
    python mos.py project status slug
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
        "structure": ("carousel_structure_generator.py", "Gera estruturas de carrossel"),
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
        "create": ("project_manager.py", "Cria novo projeto"),
        "list": ("project_manager.py", "Lista projetos"),
        "status": ("project_manager.py", "Status de um projeto"),
        "add-content": ("project_manager.py", "Adiciona conteúdo a projeto"),
        "complete": ("project_manager.py", "Marca projeto como concluído"),
        "note": ("project_manager.py", "Adiciona nota a projeto"),
    },
}

# Comandos especiais que precisam de argumentos transformados
SPECIAL_ARGS: Dict[Tuple[str, str], Callable[[List[str]], List[str]]] = {
    ("headlines", "compare"): lambda args: ["--compare"] + args,
    ("readability", "check"): lambda args: args,  # já é passthrough
    ("project", "create"): lambda args: ["create"] + args,
    ("project", "list"): lambda args: ["list"] + args,
    ("project", "status"): lambda args: ["status"] + args,
    ("project", "add-content"): lambda args: ["add-content"] + args,
    ("project", "complete"): lambda args: ["complete"] + args,
    ("project", "note"): lambda args: ["note"] + args,
}


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

  Projetos:
    mos project create "Lançamento Curso" --type launch
    mos project list
    mos project status lancamento-curso

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
    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h', 'help']:
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
        print(f"   Comandos válidos para '{category}': {', '.join(COMMAND_MAP[category].keys())}")
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
