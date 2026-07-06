#!/usr/bin/env python3
"""
Carousel Structure Generator
Gera estruturas completas de carrossel para Instagram.

Uso: python carousel_structure_generator.py "tema" tipo num_slides
Exemplo: python carousel_structure_generator.py "Marketing Digital" educativo 10
"""

import sys
import random

from output_formatter import print_json
from validators import (
    ValidationError,
    validar_texto,
    validar_inteiro,
    handle_validation_error,
)

# Estruturas de carrossel por tipo
ESTRUTURAS = {
    "educativo": {
        "nome": "Carrossel Educativo",
        "slides": [
            {
                "num": 1,
                "tipo": "CAPA",
                "elementos": [
                    "Título impactante",
                    "Subtítulo com promessa",
                    "Visual atrativo",
                ],
                "objetivo": "Parar o scroll",
            },
            {
                "num": 2,
                "tipo": "CONTEXTO",
                "elementos": [
                    "Por que isso importa",
                    "Dado ou estatística",
                    "Conexão com a dor",
                ],
                "objetivo": "Gerar identificação",
            },
            {
                "num": 3,
                "tipo": "CONTEÚDO 1",
                "elementos": [
                    "Primeiro conceito/dica",
                    "Explicação clara",
                    "Exemplo prático",
                ],
                "objetivo": "Entregar valor",
            },
            {
                "num": 4,
                "tipo": "CONTEÚDO 2",
                "elementos": [
                    "Segundo conceito/dica",
                    "Explicação clara",
                    "Exemplo prático",
                ],
                "objetivo": "Entregar valor",
            },
            {
                "num": 5,
                "tipo": "CONTEÚDO 3",
                "elementos": [
                    "Terceiro conceito/dica",
                    "Explicação clara",
                    "Exemplo prático",
                ],
                "objetivo": "Entregar valor",
            },
            {
                "num": 6,
                "tipo": "CONTEÚDO 4",
                "elementos": [
                    "Quarto conceito/dica",
                    "Explicação clara",
                    "Exemplo prático",
                ],
                "objetivo": "Entregar valor",
            },
            {
                "num": 7,
                "tipo": "CONTEÚDO 5",
                "elementos": [
                    "Quinto conceito/dica",
                    "Explicação clara",
                    "Exemplo prático",
                ],
                "objetivo": "Entregar valor",
            },
            {
                "num": 8,
                "tipo": "RESUMO",
                "elementos": [
                    "Recap dos pontos",
                    "Checklist visual",
                    "Destaque do principal",
                ],
                "objetivo": "Consolidar aprendizado",
            },
            {
                "num": 9,
                "tipo": "APLICAÇÃO",
                "elementos": [
                    "Como aplicar hoje",
                    "Primeiro passo prático",
                    "Quick win",
                ],
                "objetivo": "Gerar ação",
            },
            {
                "num": 10,
                "tipo": "CTA",
                "elementos": ["Chamada para ação", "Próximo passo", "Engajamento"],
                "objetivo": "Converter",
            },
        ],
    },
    "storytelling": {
        "nome": "Carrossel Storytelling",
        "slides": [
            {
                "num": 1,
                "tipo": "CAPA",
                "elementos": ["Frase intrigante", "Imagem emocional", "Curiosidade"],
                "objetivo": "Criar curiosidade",
            },
            {
                "num": 2,
                "tipo": "ERA UMA VEZ",
                "elementos": [
                    "Contexto inicial",
                    "Quem é o protagonista",
                    "Situação normal",
                ],
                "objetivo": "Situar o leitor",
            },
            {
                "num": 3,
                "tipo": "O PROBLEMA",
                "elementos": [
                    "O desafio surgiu",
                    "Obstáculo principal",
                    "Emoção negativa",
                ],
                "objetivo": "Criar tensão",
            },
            {
                "num": 4,
                "tipo": "TENTATIVAS",
                "elementos": [
                    "O que tentou primeiro",
                    "Por que não funcionou",
                    "Frustração",
                ],
                "objetivo": "Identificação",
            },
            {
                "num": 5,
                "tipo": "A VIRADA",
                "elementos": ["O momento decisivo", "O que mudou", "Nova perspectiva"],
                "objetivo": "Ponto de inflexão",
            },
            {
                "num": 6,
                "tipo": "A SOLUÇÃO",
                "elementos": ["O que funcionou", "Como aplicou", "Processo"],
                "objetivo": "Mostrar o caminho",
            },
            {
                "num": 7,
                "tipo": "RESULTADO",
                "elementos": ["Transformação", "Números/provas", "Antes vs depois"],
                "objetivo": "Provar valor",
            },
            {
                "num": 8,
                "tipo": "LIÇÃO",
                "elementos": ["Aprendizado principal", "Insight único", "Sabedoria"],
                "objetivo": "Entregar valor",
            },
            {
                "num": 9,
                "tipo": "E VOCÊ?",
                "elementos": ["Reflexão para o leitor", "Pergunta poderosa", "Conexão"],
                "objetivo": "Engajar",
            },
            {
                "num": 10,
                "tipo": "CTA",
                "elementos": ["Próximo passo", "Oferta/recurso", "Chamada para ação"],
                "objetivo": "Converter",
            },
        ],
    },
    "lista": {
        "nome": "Carrossel Lista/Ranking",
        "slides": [
            {
                "num": 1,
                "tipo": "CAPA",
                "elementos": ["Número + tema", "Promessa de valor", "Visual chamativo"],
                "objetivo": "Parar o scroll",
            },
            {
                "num": 2,
                "tipo": "ITEM 1",
                "elementos": ["Primeiro item", "Por que é importante", "Dica rápida"],
                "objetivo": "Entregar valor",
            },
            {
                "num": 3,
                "tipo": "ITEM 2",
                "elementos": ["Segundo item", "Por que é importante", "Dica rápida"],
                "objetivo": "Entregar valor",
            },
            {
                "num": 4,
                "tipo": "ITEM 3",
                "elementos": ["Terceiro item", "Por que é importante", "Dica rápida"],
                "objetivo": "Entregar valor",
            },
            {
                "num": 5,
                "tipo": "ITEM 4",
                "elementos": ["Quarto item", "Por que é importante", "Dica rápida"],
                "objetivo": "Entregar valor",
            },
            {
                "num": 6,
                "tipo": "ITEM 5",
                "elementos": ["Quinto item", "Por que é importante", "Dica rápida"],
                "objetivo": "Entregar valor",
            },
            {
                "num": 7,
                "tipo": "ITEM 6",
                "elementos": ["Sexto item", "Por que é importante", "Dica rápida"],
                "objetivo": "Entregar valor",
            },
            {
                "num": 8,
                "tipo": "ITEM 7",
                "elementos": ["Sétimo item", "Por que é importante", "Dica rápida"],
                "objetivo": "Entregar valor",
            },
            {
                "num": 9,
                "tipo": "BÔNUS",
                "elementos": ["Item bônus surpresa", "Diferencial", "Valor extra"],
                "objetivo": "Surpreender",
            },
            {
                "num": 10,
                "tipo": "CTA",
                "elementos": [
                    "Qual foi seu favorito?",
                    "Salve para consultar",
                    "Compartilhe",
                ],
                "objetivo": "Engajar",
            },
        ],
    },
    "tutorial": {
        "nome": "Carrossel Passo a Passo",
        "slides": [
            {
                "num": 1,
                "tipo": "CAPA",
                "elementos": [
                    "Como fazer X",
                    "Resultado prometido",
                    "Tempo/facilidade",
                ],
                "objetivo": "Parar o scroll",
            },
            {
                "num": 2,
                "tipo": "MATERIAIS",
                "elementos": [
                    "O que você precisa",
                    "Ferramentas/recursos",
                    "Pré-requisitos",
                ],
                "objetivo": "Preparar",
            },
            {
                "num": 3,
                "tipo": "PASSO 1",
                "elementos": ["Primeira ação", "Como fazer", "Screenshot/visual"],
                "objetivo": "Guiar",
            },
            {
                "num": 4,
                "tipo": "PASSO 2",
                "elementos": ["Segunda ação", "Como fazer", "Screenshot/visual"],
                "objetivo": "Guiar",
            },
            {
                "num": 5,
                "tipo": "PASSO 3",
                "elementos": ["Terceira ação", "Como fazer", "Screenshot/visual"],
                "objetivo": "Guiar",
            },
            {
                "num": 6,
                "tipo": "PASSO 4",
                "elementos": ["Quarta ação", "Como fazer", "Screenshot/visual"],
                "objetivo": "Guiar",
            },
            {
                "num": 7,
                "tipo": "PASSO 5",
                "elementos": ["Quinta ação", "Como fazer", "Screenshot/visual"],
                "objetivo": "Guiar",
            },
            {
                "num": 8,
                "tipo": "RESULTADO",
                "elementos": [
                    "O que conseguiu",
                    "Antes vs depois",
                    "Prova do resultado",
                ],
                "objetivo": "Motivar",
            },
            {
                "num": 9,
                "tipo": "DICAS EXTRAS",
                "elementos": ["Erros comuns", "Como evitar", "Otimizações"],
                "objetivo": "Agregar",
            },
            {
                "num": 10,
                "tipo": "CTA",
                "elementos": [
                    "Tente e compartilhe",
                    "Marque o resultado",
                    "Link para mais",
                ],
                "objetivo": "Converter",
            },
        ],
    },
    "mito_verdade": {
        "nome": "Carrossel Mito vs Verdade",
        "slides": [
            {
                "num": 1,
                "tipo": "CAPA",
                "elementos": [
                    "X Mitos sobre [tema]",
                    "Você acredita em algum?",
                    "Visual impactante",
                ],
                "objetivo": "Parar o scroll",
            },
            {
                "num": 2,
                "tipo": "MITO 1",
                "elementos": [
                    "❌ Mito comum",
                    "Por que as pessoas acreditam",
                    "Problema dessa crença",
                ],
                "objetivo": "Identificar",
            },
            {
                "num": 3,
                "tipo": "VERDADE 1",
                "elementos": [
                    "✅ A verdade",
                    "Evidência/explicação",
                    "O que fazer diferente",
                ],
                "objetivo": "Educar",
            },
            {
                "num": 4,
                "tipo": "MITO 2",
                "elementos": [
                    "❌ Mito comum",
                    "Por que as pessoas acreditam",
                    "Problema dessa crença",
                ],
                "objetivo": "Identificar",
            },
            {
                "num": 5,
                "tipo": "VERDADE 2",
                "elementos": [
                    "✅ A verdade",
                    "Evidência/explicação",
                    "O que fazer diferente",
                ],
                "objetivo": "Educar",
            },
            {
                "num": 6,
                "tipo": "MITO 3",
                "elementos": [
                    "❌ Mito comum",
                    "Por que as pessoas acreditam",
                    "Problema dessa crença",
                ],
                "objetivo": "Identificar",
            },
            {
                "num": 7,
                "tipo": "VERDADE 3",
                "elementos": [
                    "✅ A verdade",
                    "Evidência/explicação",
                    "O que fazer diferente",
                ],
                "objetivo": "Educar",
            },
            {
                "num": 8,
                "tipo": "RESUMO",
                "elementos": ["Os 3 mitos desmascarados", "Visão geral", "Checklist"],
                "objetivo": "Consolidar",
            },
            {
                "num": 9,
                "tipo": "REFLEXÃO",
                "elementos": [
                    "Você acreditava em algum?",
                    "O que vai mudar?",
                    "Pergunta engajadora",
                ],
                "objetivo": "Engajar",
            },
            {
                "num": 10,
                "tipo": "CTA",
                "elementos": [
                    "Compartilhe para ajudar outros",
                    "Salve para lembrar",
                    "Siga para mais",
                ],
                "objetivo": "Converter",
            },
        ],
    },
    "comparativo": {
        "nome": "Carrossel Comparativo",
        "slides": [
            {
                "num": 1,
                "tipo": "CAPA",
                "elementos": ["X vs Y", "Qual é melhor?", "Visual dividido"],
                "objetivo": "Parar o scroll",
            },
            {
                "num": 2,
                "tipo": "OVERVIEW",
                "elementos": ["O que é X", "O que é Y", "Por que comparar"],
                "objetivo": "Contextualizar",
            },
            {
                "num": 3,
                "tipo": "CRITÉRIO 1",
                "elementos": ["Primeiro aspecto", "X: resultado", "Y: resultado"],
                "objetivo": "Comparar",
            },
            {
                "num": 4,
                "tipo": "CRITÉRIO 2",
                "elementos": ["Segundo aspecto", "X: resultado", "Y: resultado"],
                "objetivo": "Comparar",
            },
            {
                "num": 5,
                "tipo": "CRITÉRIO 3",
                "elementos": ["Terceiro aspecto", "X: resultado", "Y: resultado"],
                "objetivo": "Comparar",
            },
            {
                "num": 6,
                "tipo": "CRITÉRIO 4",
                "elementos": ["Quarto aspecto", "X: resultado", "Y: resultado"],
                "objetivo": "Comparar",
            },
            {
                "num": 7,
                "tipo": "PRÓS E CONTRAS",
                "elementos": ["Vantagens de X", "Vantagens de Y", "Desvantagens"],
                "objetivo": "Balancear",
            },
            {
                "num": 8,
                "tipo": "PARA QUEM",
                "elementos": [
                    "X é ideal para...",
                    "Y é ideal para...",
                    "Perfil de cada",
                ],
                "objetivo": "Direcionar",
            },
            {
                "num": 9,
                "tipo": "VEREDICTO",
                "elementos": ["Minha opinião", "Quando usar cada", "Recomendação"],
                "objetivo": "Concluir",
            },
            {
                "num": 10,
                "tipo": "CTA",
                "elementos": [
                    "Qual você prefere?",
                    "Comenta sua experiência",
                    "Salve para decidir",
                ],
                "objetivo": "Engajar",
            },
        ],
    },
    "problema_solucao": {
        "nome": "Carrossel Problema → Solução",
        "slides": [
            {
                "num": 1,
                "tipo": "CAPA",
                "elementos": ["Problema comum", "Você também?", "Visual da dor"],
                "objetivo": "Identificação",
            },
            {
                "num": 2,
                "tipo": "O PROBLEMA",
                "elementos": [
                    "Descrição detalhada",
                    "Como se manifesta",
                    "Consequências",
                ],
                "objetivo": "Agitar a dor",
            },
            {
                "num": 3,
                "tipo": "POR QUE ACONTECE",
                "elementos": ["Causa raiz 1", "Causa raiz 2", "Entendimento"],
                "objetivo": "Educar",
            },
            {
                "num": 4,
                "tipo": "ERRO COMUM",
                "elementos": [
                    "O que a maioria faz",
                    "Por que não funciona",
                    "Armadilha",
                ],
                "objetivo": "Alertar",
            },
            {
                "num": 5,
                "tipo": "A SOLUÇÃO",
                "elementos": ["Abordagem correta", "Por que funciona", "Diferencial"],
                "objetivo": "Apresentar",
            },
            {
                "num": 6,
                "tipo": "COMO APLICAR 1",
                "elementos": ["Primeiro passo", "Detalhamento", "Dica prática"],
                "objetivo": "Guiar",
            },
            {
                "num": 7,
                "tipo": "COMO APLICAR 2",
                "elementos": ["Segundo passo", "Detalhamento", "Dica prática"],
                "objetivo": "Guiar",
            },
            {
                "num": 8,
                "tipo": "COMO APLICAR 3",
                "elementos": ["Terceiro passo", "Detalhamento", "Dica prática"],
                "objetivo": "Guiar",
            },
            {
                "num": 9,
                "tipo": "RESULTADO",
                "elementos": ["O que esperar", "Timeline", "Prova social"],
                "objetivo": "Motivar",
            },
            {
                "num": 10,
                "tipo": "CTA",
                "elementos": ["Comece hoje", "Link para mais", "Oferta/recurso"],
                "objetivo": "Converter",
            },
        ],
    },
    "curiosidades": {
        "nome": "Carrossel Curiosidades",
        "slides": [
            {
                "num": 1,
                "tipo": "CAPA",
                "elementos": [
                    "X coisas que você não sabia",
                    "Sobre [tema]",
                    "Visual intrigante",
                ],
                "objetivo": "Curiosidade",
            },
            {
                "num": 2,
                "tipo": "FATO 1",
                "elementos": [
                    "Curiosidade surpreendente",
                    "Contexto",
                    "Fonte (se houver)",
                ],
                "objetivo": "Surpreender",
            },
            {
                "num": 3,
                "tipo": "FATO 2",
                "elementos": [
                    "Curiosidade surpreendente",
                    "Contexto",
                    "Fonte (se houver)",
                ],
                "objetivo": "Surpreender",
            },
            {
                "num": 4,
                "tipo": "FATO 3",
                "elementos": [
                    "Curiosidade surpreendente",
                    "Contexto",
                    "Fonte (se houver)",
                ],
                "objetivo": "Surpreender",
            },
            {
                "num": 5,
                "tipo": "FATO 4",
                "elementos": [
                    "Curiosidade surpreendente",
                    "Contexto",
                    "Fonte (se houver)",
                ],
                "objetivo": "Surpreender",
            },
            {
                "num": 6,
                "tipo": "FATO 5",
                "elementos": [
                    "Curiosidade surpreendente",
                    "Contexto",
                    "Fonte (se houver)",
                ],
                "objetivo": "Surpreender",
            },
            {
                "num": 7,
                "tipo": "FATO 6",
                "elementos": [
                    "Curiosidade surpreendente",
                    "Contexto",
                    "Fonte (se houver)",
                ],
                "objetivo": "Surpreender",
            },
            {
                "num": 8,
                "tipo": "FATO 7",
                "elementos": [
                    "Curiosidade surpreendente",
                    "Contexto",
                    "Fonte (se houver)",
                ],
                "objetivo": "Surpreender",
            },
            {
                "num": 9,
                "tipo": "BÔNUS",
                "elementos": [
                    "Fato mais impressionante",
                    "Por que importa",
                    "Reflexão",
                ],
                "objetivo": "Impactar",
            },
            {
                "num": 10,
                "tipo": "CTA",
                "elementos": [
                    "Qual te surpreendeu mais?",
                    "Compartilhe com alguém",
                    "Siga para mais",
                ],
                "objetivo": "Engajar",
            },
        ],
    },
}

# Paletas de cores sugeridas
PALETAS = [
    {
        "nome": "Profissional",
        "cores": ["#1a1a2e", "#16213e", "#0f3460", "#e94560"],
        "uso": "B2B, consultoria",
    },
    {
        "nome": "Vibrante",
        "cores": ["#ff6b6b", "#feca57", "#48dbfb", "#ff9ff3"],
        "uso": "Lifestyle, criadores",
    },
    {
        "nome": "Minimalista",
        "cores": ["#2d3436", "#636e72", "#b2bec3", "#dfe6e9"],
        "uso": "Tech, design",
    },
    {
        "nome": "Natural",
        "cores": ["#55a630", "#80b918", "#aacc00", "#006400"],
        "uso": "Saúde, sustentabilidade",
    },
    {
        "nome": "Luxo",
        "cores": ["#1a1a1a", "#c9a227", "#f5f5dc", "#8b7355"],
        "uso": "Premium, moda",
    },
    {
        "nome": "Pastel",
        "cores": ["#a8e6cf", "#dcedc1", "#ffd3b6", "#ffaaa5"],
        "uso": "Feminino, bem-estar",
    },
]

# Fontes sugeridas
FONTES = {
    "titulo": [
        "Montserrat Bold",
        "Poppins Bold",
        "Playfair Display",
        "Oswald",
        "Bebas Neue",
    ],
    "corpo": ["Open Sans", "Roboto", "Lato", "Nunito", "Source Sans Pro"],
    "destaque": ["Dancing Script", "Pacifico", "Lobster", "Satisfy", "Great Vibes"],
}


def gerar_estrutura(tema: str, tipo: str, num_slides: int) -> dict:
    """Gera estrutura completa de carrossel."""

    if tipo not in ESTRUTURAS:
        tipo = "educativo"

    estrutura_base = ESTRUTURAS[tipo]
    paleta = random.choice(PALETAS)

    # Ajustar número de slides
    slides = estrutura_base["slides"][:num_slides]

    resultado = {
        "tema": tema,
        "tipo": estrutura_base["nome"],
        "num_slides": len(slides),
        "paleta": paleta,
        "fontes": {
            "titulo": random.choice(FONTES["titulo"]),
            "corpo": random.choice(FONTES["corpo"]),
            "destaque": random.choice(FONTES["destaque"]),
        },
        "slides": slides,
    }

    return resultado


def formatar_saida(estrutura: dict) -> str:
    """Formata a estrutura para exibição."""

    saida = f"""
╔══════════════════════════════════════════════════════════════════╗
║              📱 ESTRUTURA DE CARROSSEL                            ║
╠══════════════════════════════════════════════════════════════════╣
║ Tema: {estrutura['tema'][:50]}
║ Tipo: {estrutura['tipo']}
║ Slides: {estrutura['num_slides']}
╚══════════════════════════════════════════════════════════════════╝

🎨 PALETA SUGERIDA: {estrutura['paleta']['nome']}
   Cores: {' | '.join(estrutura['paleta']['cores'])}
   Ideal para: {estrutura['paleta']['uso']}

🔤 FONTES SUGERIDAS:
   Título: {estrutura['fontes']['titulo']}
   Corpo: {estrutura['fontes']['corpo']}
   Destaque: {estrutura['fontes']['destaque']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 ESTRUTURA DOS SLIDES:

"""

    for slide in estrutura["slides"]:
        saida += f"""┌─────────────────────────────────────────────────────────────────┐
│ SLIDE {slide['num']}: {slide['tipo']}
│ 🎯 Objetivo: {slide['objetivo']}
├─────────────────────────────────────────────────────────────────┤
│ Elementos:
"""
        for elemento in slide["elementos"]:
            saida += f"│   • {elemento}\n"

        saida += (
            "└─────────────────────────────────────────────────────────────────┘\n\n"
        )

    saida += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 DICAS DE DESIGN:

📐 FORMATO:
   • Tamanho: 1080x1350 (4:5) ou 1080x1080 (1:1)
   • Margem segura: 50px de cada lado
   • Área de texto: máximo 70% do slide

📝 TEXTO:
   • Máximo 50 palavras por slide
   • Hierarquia clara (título > subtítulo > corpo)
   • Contraste alto entre texto e fundo

🎯 CAPA:
   • Elemento visual forte
   • Texto grande e legível
   • Indicador de "arraste →" sutil

🔚 ÚLTIMO SLIDE:
   • CTA claro e único
   • Repetir identidade visual
   • Incluir @perfil

"""

    return saida


def listar_tipos() -> None:
    """Lista todos os tipos de carrossel disponíveis."""

    print("\n📚 TIPOS DE CARROSSEL DISPONÍVEIS:\n")
    for key, value in ESTRUTURAS.items():
        print(f"  • {key}: {value['nome']}")
    print()


USO_CAROUSEL = (
    'Uso: python carousel_structure_generator.py "tema" [tipo] [num_slides] [--json]\n'
    'Exemplo: python carousel_structure_generator.py "produtividade" educativo 8'
)


def main() -> None:
    if len(sys.argv) < 2:
        print(USO_CAROUSEL)
        listar_tipos()
        return

    if sys.argv[1] == "--tipos":
        listar_tipos()
        return

    json_mode = "--json" in sys.argv
    args_clean = [a for a in sys.argv[1:] if a != "--json"]

    try:
        tema = validar_texto(args_clean[0], campo="tema", max_len=200)
        tipo = (
            validar_texto(args_clean[1], campo="tipo", max_len=50)
            if len(args_clean) > 1
            else "educativo"
        )
        num_slides = (
            validar_inteiro(args_clean[2], campo="num_slides", min_val=3, max_val=15)
            if len(args_clean) > 2
            else 10
        )
    except ValidationError as e:
        handle_validation_error(e, mostrar_uso=USO_CAROUSEL)
        return

    if num_slides < 3 or num_slides > 10:
        print("⚠️  Recomendado: 5-10 slides. Ajustando...")
        num_slides = min(max(num_slides, 3), 10)

    estrutura = gerar_estrutura(tema, tipo, num_slides)
    if json_mode:
        print_json(estrutura)
    else:
        print(formatar_saida(estrutura))


if __name__ == "__main__":
    main()
