#!/usr/bin/env python3
"""
Instagram Hashtag Research - Pesquisa avançada de hashtags para Instagram
Analisa hashtags por nicho, sugere estratégias e gera sets otimizados.

Uso:
    python instagram_hashtag_research.py nicho [--quantidade 15] [--formato tabela|markdown|json]
    python instagram_hashtag_research.py --analisar "#hashtag1,#hashtag2"
    python instagram_hashtag_research.py --competidor @perfil
    python instagram_hashtag_research.py --gerar-set nicho --objetivo engajamento|alcance|nicho

Exemplos:
    python instagram_hashtag_research.py "marketing digital"
    python instagram_hashtag_research.py "fitness" --quantidade 20 --formato markdown
    python instagram_hashtag_research.py --gerar-set "empreendedorismo" --objetivo alcance
"""

import sys
import os
import json
import re
import random
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from collections import Counter

# =============================================================================
# BASE DE DADOS DE HASHTAGS POR NICHO
# =============================================================================

HASHTAGS_DATABASE = {
    "marketing_digital": {
        "grandes": [  # 1M+ posts
            "#marketingdigital", "#marketing", "#socialmedia", "#digitalmarketing",
            "#empreendedorismo", "#negocios", "#vendas", "#sucesso", "#brasil"
        ],
        "medias": [  # 100K-1M posts
            "#marketingonline", "#marketingdeconteudo", "#estrategiademarketing",
            "#marketingbrasil", "#midiassociais", "#gestaoderedes", "#trafegopago",
            "#copywriting", "#funil", "#lancamento", "#infoproduto", "#mentoria"
        ],
        "pequenas": [  # 10K-100K posts
            "#marketingparainiciantes", "#dicasdemarketing", "#aprendamarketing",
            "#marketingestratégico", "#crescernoinstagram", "#engajamentoinstagram",
            "#dicasdenegocios", "#empreendedorismodigital", "#vendasonline"
        ],
        "nicho": [  # <10K posts, muito específicas
            "#marketingparapequenasempresas", "#estrategiasdeconteudo",
            "#crescimentoorganico", "#algoritmodoinstagram"
        ],
        "trending": [
            "#ia", "#inteligenciaartificial", "#chatgpt", "#automacao"
        ],
        "engajamento": [
            "#dica", "#dicadodia", "#ficaadica", "#voceabia", "#savepost"
        ]
    },

    "empreendedorismo": {
        "grandes": [
            "#empreendedorismo", "#negocios", "#sucesso", "#motivacao",
            "#empreendedor", "#empresario", "#trabalho", "#carreira", "#dinheiro"
        ],
        "medias": [
            "#empreendedorismodigital", "#empreendedorismofeminino", "#mentalidaderica",
            "#mindsetempreendedor", "#negociosonline", "#rendaextra", "#liberdadefinanceira",
            "#pequenoempreendedor", "#meuprópriochefe", "#vidadeempreendedor"
        ],
        "pequenas": [
            "#empreendedorismobrasileiro", "#negocioproprio", "#donodenegocio",
            "#empreendedorismocriativo", "#empreendacomproposito", "#meunegocio"
        ],
        "nicho": [
            "#startupbrasil", "#microempreendedor", "#mulheresquempreendem"
        ],
        "trending": [
            "#nomadedigital", "#trabalhoremoto", "#homeoffice"
        ],
        "engajamento": [
            "#motivacaoempreendedora", "#focoemdeus", "#acreditenoseupotencial"
        ]
    },

    "fitness": {
        "grandes": [
            "#fitness", "#treino", "#academia", "#musculacao", "#saude",
            "#gym", "#fit", "#workout", "#fitnessmotivation", "#bodybuilding"
        ],
        "medias": [
            "#treinoemcasa", "#dieta", "#vidasaudavel", "#emagrecimento",
            "#treinohard", "#foco", "#determinacao", "#hipertrofia", "#fitnessbrasil",
            "#treinofuncional", "#crossfit", "#aerobico"
        ],
        "pequenas": [
            "#treinopesado", "#foconotreino", "#projetoverao", "#secando",
            "#ganhodemassa", "#ficafortebrasil", "#motivacaofitness"
        ],
        "nicho": [
            "#treinoparamulheres", "#fitnessparabloggers", "#treinoparaganharmusculo"
        ],
        "trending": [
            "#12semanas", "#desafiofitness", "#transformacao"
        ],
        "engajamento": [
            "#vemcomigo", "#boraTreinar", "#treinoDoDia"
        ]
    },

    "financas": {
        "grandes": [
            "#financas", "#dinheiro", "#investimentos", "#economia", "#renda",
            "#educacaofinanceira", "#investir", "#bolsadevalores", "#acoes"
        ],
        "medias": [
            "#liberdadefinanceira", "#financaspessoais", "#investidor",
            "#rendafixa", "#rendavariavel", "#fundosimobiliarios", "#dividendos",
            "#reservadeemergencia", "#poupanca", "#criptomoedas", "#bitcoin"
        ],
        "pequenas": [
            "#dicasdefinancas", "#comoinvestir", "#investirmelhor",
            "#independenciafinanceira", "#enriquecer", "#multiplicardinheiro"
        ],
        "nicho": [
            "#investidoriniciante", "#financasparacasais", "#primeirainvestimento"
        ],
        "trending": [
            "#tesourodireta", "#fiis", "#daytradesbrasil"
        ],
        "engajamento": [
            "#dicafinanceira", "#saiadividas", "#controlegastos"
        ]
    },

    "moda": {
        "grandes": [
            "#moda", "#fashion", "#estilo", "#look", "#tendencia",
            "#outfit", "#style", "#ootd", "#lookdodia", "#modafeminina"
        ],
        "medias": [
            "#modabrasileira", "#modapraia", "#modaintima", "#modasustentavel",
            "#lookdoDia", "#inspiracaodemoda", "#fashionblogger", "#instafashion",
            "#streetstyle", "#casualstyle", "#lookdeverao"
        ],
        "pequenas": [
            "#dicasdemoda", "#consultoriadeestilo", "#guarda-roupacapsula",
            "#combinacaodelooks", "#styletips", "#fashioninspo"
        ],
        "nicho": [
            "#modaplus", "#modaconsciente", "#slowfashion", "#modaatemporal"
        ],
        "trending": [
            "#tendencias2026", "#coresbrasil", "#minimalismo"
        ],
        "engajamento": [
            "#estiloproprio", "#autoestima", "#amooquevisto"
        ]
    },

    "gastronomia": {
        "grandes": [
            "#comida", "#food", "#gastronomia", "#receita", "#culinaria",
            "#foodporn", "#instafood", "#delicia", "#gourmet", "#chef"
        ],
        "medias": [
            "#receitafacil", "#cozinhabrasileira", "#receitasaudavel",
            "#comidacaseira", "#foodlover", "#comidasaudavel", "#doces",
            "#sobremesa", "#almoço", "#jantar", "#lanche"
        ],
        "pequenas": [
            "#receitadodia", "#cozinheemcasa", "#receitasfit",
            "#lowcarb", "#receitasveganas", "#semgluten", "#zerolactose"
        ],
        "nicho": [
            "#confeitariaartesanal", "#paneladepedra", "#airfryer"
        ],
        "trending": [
            "#receitavirais", "#comidadoTikTok", "#foodhacks"
        ],
        "engajamento": [
            "#fomeboa", "#bora", "#quemvaifazer"
        ]
    },

    "tecnologia": {
        "grandes": [
            "#tecnologia", "#tech", "#inovacao", "#programacao", "#ti",
            "#developer", "#coding", "#software", "#startup", "#digital"
        ],
        "medias": [
            "#programador", "#desenvolvedor", "#python", "#javascript",
            "#inteligenciaartificial", "#machinelearning", "#datascience",
            "#webdesign", "#uxdesign", "#frontend", "#backend"
        ],
        "pequenas": [
            "#devbrasil", "#programadorbrasil", "#aprendaprogramar",
            "#dicasdetech", "#carreiraTI", "#desenvolvimentoweb"
        ],
        "nicho": [
            "#pythonbrasil", "#reactjs", "#nodeJS", "#flutterbrasil"
        ],
        "trending": [
            "#ia", "#chatgpt", "#gemini", "#copilot", "#nocode"
        ],
        "engajamento": [
            "#codequality", "#cleancode", "#buglife"
        ]
    },

    "desenvolvimento_pessoal": {
        "grandes": [
            "#desenvolvimentopessoal", "#crescimentopessoal", "#autoconhecimento",
            "#motivacao", "#mindset", "#foco", "#determinacao", "#sucesso"
        ],
        "medias": [
            "#inteligenciaemocional", "#habitos", "#produtividade", "#lideranca",
            "#comunicacao", "#softskills", "#mentalidade", "#proposito",
            "#coaching", "#pnl", "#meditacao"
        ],
        "pequenas": [
            "#desenvolvimentohumano", "#crescercomohumano", "#evolucaopessoal",
            "#transformacaopessoal", "#jornadadoheroi", "#melhorversao"
        ],
        "nicho": [
            "#estoicismo", "#ikigai", "#atomichabits", "#deepwork"
        ],
        "trending": [
            "#saudemenral", "#ansiedade", "#burnout", "#wellness"
        ],
        "engajamento": [
            "#reflexaododia", "#pensepositivo", "#voceconsegue"
        ]
    },

    "beleza": {
        "grandes": [
            "#beleza", "#maquiagem", "#makeup", "#skincare", "#beauty",
            "#pele", "#cabelo", "#unhas", "#nails", "#beautyblogger"
        ],
        "medias": [
            "#cuidadoscomapele", "#rotinadebeleza", "#makeUp", "#tutorial",
            "#skincareroutine", "#peleperfeita", "#tratamento", "#hidratacao",
            "#antienvelhecimento", "#acne", "#cabeloslindos"
        ],
        "pequenas": [
            "#dicasdebeleza", "#produtosdebeleza", "#beautyTips",
            "#makenatural", "#glowskin", "#selfcare"
        ],
        "nicho": [
            "#skincarebrasileiro", "#dermato", "#retinol", "#vitaminac"
        ],
        "trending": [
            "#glassskin", "#dopaminebeauty", "#cleanbeauty"
        ],
        "engajamento": [
            "#antesedepois", "#makecompletou", "#getreadywithme"
        ]
    },

    "viagem": {
        "grandes": [
            "#viagem", "#travel", "#turismo", "#ferias", "#viajar",
            "#trip", "#traveling", "#wanderlust", "#adventure", "#brasil"
        ],
        "medias": [
            "#viagembrasil", "#dicasdeviagem", "#roteiro", "#mochilao",
            "#praia", "#montanha", "#natureza", "#paisagem", "#destinos",
            "#viajarbarato", "#hotelaria", "#hospedagem"
        ],
        "pequenas": [
            "#viajantesolo", "#viagememfamilia", "#viagemromantica",
            "#lugaresincriveis", "#lugaresbonitos", "#destinosnacionais"
        ],
        "nicho": [
            "#ecoturismo", "#turismodeexperiencia", "#roadtrip", "#vanlife"
        ],
        "trending": [
            "#viagemsemroteiro", "#workcation", "#staycation"
        ],
        "engajamento": [
            "#partiu", "#bora", "#proxmodestino", "#quemvai"
        ]
    }
}

# Hashtags universais de engajamento
HASHTAGS_ENGAJAMENTO_UNIVERSAL = [
    "#dica", "#dicadodia", "#ficaadica", "#voceabia", "#salvaessapostagem",
    "#compartilhecomalguem", "#marcaunamigo", "#comentaai", "#oquevocesacham",
    "#postagemviral", "#conteudodevalor", "#aprendanotiktok", "#dicasdeouro"
]

# Hashtags sazonais (atualizar conforme época)
HASHTAGS_SAZONAIS = {
    "janeiro": ["#anonovo", "#metas2026", "#recomeço", "#novoano"],
    "fevereiro": ["#carnaval", "#carnaval2026", "#folia"],
    "marco": ["#diadamulher", "#mulheresqueinspiraram"],
    "abril": ["#pascoa", "#feriadopascoa"],
    "maio": ["#diadasmaes", "#maes", "#amor"],
    "junho": ["#festaJunina", "#saojoao", "#arraial"],
    "julho": ["#ferias", "#inverno", "#friozinho"],
    "agosto": ["#diadospais", "#pais"],
    "setembro": ["#primavera", "#setembroamarelo"],
    "outubro": ["#outubrorosa", "#diacriancas", "#halloween"],
    "novembro": ["#blackfriday", "#novembroazul", "#consciencianegra"],
    "dezembro": ["#natal", "#natal2026", "#reveillon", "#anonovo"]
}


def get_hashtags_sazonais() -> List[str]:
    """Retorna hashtags sazonais do mês atual."""
    mes_atual = datetime.now().strftime("%B").lower()
    meses_pt = {
        "january": "janeiro", "february": "fevereiro", "march": "marco",
        "april": "abril", "may": "maio", "june": "junho",
        "july": "julho", "august": "agosto", "september": "setembro",
        "october": "outubro", "november": "novembro", "december": "dezembro"
    }
    mes_pt = meses_pt.get(mes_atual, "janeiro")
    return HASHTAGS_SAZONAIS.get(mes_pt, [])


def encontrar_nicho(termo: str) -> Optional[str]:
    """Encontra o nicho mais relevante para o termo buscado."""
    termo_lower = termo.lower().replace(" ", "_")

    # Mapeamento de sinônimos
    sinonimos = {
        "marketing": "marketing_digital",
        "marketing digital": "marketing_digital",
        "mkt": "marketing_digital",
        "redes sociais": "marketing_digital",
        "social media": "marketing_digital",
        "empreender": "empreendedorismo",
        "negocios": "empreendedorismo",
        "empresa": "empreendedorismo",
        "fitness": "fitness",
        "academia": "fitness",
        "treino": "fitness",
        "musculacao": "fitness",
        "exercicio": "fitness",
        "financas": "financas",
        "investimento": "financas",
        "dinheiro": "financas",
        "bolsa": "financas",
        "moda": "moda",
        "fashion": "moda",
        "roupa": "moda",
        "estilo": "moda",
        "comida": "gastronomia",
        "receita": "gastronomia",
        "culinaria": "gastronomia",
        "cozinha": "gastronomia",
        "tech": "tecnologia",
        "programacao": "tecnologia",
        "ti": "tecnologia",
        "software": "tecnologia",
        "desenvolvimento pessoal": "desenvolvimento_pessoal",
        "autoajuda": "desenvolvimento_pessoal",
        "produtividade": "desenvolvimento_pessoal",
        "mindset": "desenvolvimento_pessoal",
        "beleza": "beleza",
        "maquiagem": "beleza",
        "skincare": "beleza",
        "cosmetico": "beleza",
        "viagem": "viagem",
        "turismo": "viagem",
        "viajar": "viagem",
        "ferias": "viagem"
    }

    # Busca direta
    if termo_lower in HASHTAGS_DATABASE:
        return termo_lower

    # Busca por sinônimos
    for key, value in sinonimos.items():
        if key in termo_lower or termo_lower in key:
            return value

    # Busca por palavras-chave
    for nicho, dados in HASHTAGS_DATABASE.items():
        todas_hashtags = " ".join(
            dados.get("grandes", []) +
            dados.get("medias", []) +
            dados.get("pequenas", [])
        ).lower()
        if termo_lower.replace("_", "") in todas_hashtags:
            return nicho

    return None


def gerar_set_hashtags(
    nicho: str,
    quantidade: int = 15,
    objetivo: str = "engajamento"
) -> Dict:
    """
    Gera um set otimizado de hashtags para Instagram.

    Objetivos:
    - engajamento: foco em hashtags de nicho e engajamento
    - alcance: mais hashtags grandes
    - nicho: apenas hashtags específicas
    """
    nicho_encontrado = encontrar_nicho(nicho)

    if not nicho_encontrado:
        return {
            "erro": f"Nicho '{nicho}' não encontrado",
            "nichos_disponiveis": list(HASHTAGS_DATABASE.keys())
        }

    dados = HASHTAGS_DATABASE[nicho_encontrado]

    # Distribuição baseada no objetivo
    if objetivo == "alcance":
        # Mais hashtags grandes para máximo alcance
        distribuicao = {
            "grandes": min(5, len(dados.get("grandes", []))),
            "medias": min(6, len(dados.get("medias", []))),
            "pequenas": min(3, len(dados.get("pequenas", []))),
            "engajamento": 1
        }
    elif objetivo == "nicho":
        # Foco em hashtags pequenas e de nicho
        distribuicao = {
            "grandes": min(2, len(dados.get("grandes", []))),
            "medias": min(4, len(dados.get("medias", []))),
            "pequenas": min(6, len(dados.get("pequenas", []))),
            "nicho": min(3, len(dados.get("nicho", [])))
        }
    else:  # engajamento (padrão)
        # Equilíbrio com foco em engajamento
        distribuicao = {
            "grandes": min(3, len(dados.get("grandes", []))),
            "medias": min(5, len(dados.get("medias", []))),
            "pequenas": min(4, len(dados.get("pequenas", []))),
            "engajamento": min(2, len(dados.get("engajamento", []))),
            "trending": 1
        }

    # Gerar set
    hashtags_selecionadas = []

    for categoria, qtd in distribuicao.items():
        lista = dados.get(categoria, [])
        if categoria == "engajamento" and not lista:
            lista = HASHTAGS_ENGAJAMENTO_UNIVERSAL

        if lista:
            selecionadas = random.sample(lista, min(qtd, len(lista)))
            hashtags_selecionadas.extend(selecionadas)

    # Ajustar para quantidade desejada
    if len(hashtags_selecionadas) > quantidade:
        hashtags_selecionadas = random.sample(hashtags_selecionadas, quantidade)

    # Adicionar hashtag sazonal se couber
    sazonais = get_hashtags_sazonais()
    if sazonais and len(hashtags_selecionadas) < quantidade:
        hashtags_selecionadas.append(random.choice(sazonais))

    # Remover duplicatas mantendo ordem
    hashtags_unicas = list(dict.fromkeys(hashtags_selecionadas))

    return {
        "nicho": nicho_encontrado,
        "objetivo": objetivo,
        "quantidade": len(hashtags_unicas),
        "hashtags": hashtags_unicas,
        "hashtags_texto": " ".join(hashtags_unicas),
        "distribuicao": distribuicao,
        "dica": get_dica_por_objetivo(objetivo)
    }


def get_dica_por_objetivo(objetivo: str) -> str:
    """Retorna dica baseada no objetivo."""
    dicas = {
        "alcance": "Use este set para posts que querem atingir o máximo de pessoas possível. Ideal para conteúdo viral ou lançamentos.",
        "engajamento": "Este set equilibra alcance com engajamento. Ideal para posts do dia a dia que buscam interação.",
        "nicho": "Set focado em público qualificado. Menos alcance, mas atrai pessoas mais interessadas no seu conteúdo específico."
    }
    return dicas.get(objetivo, "")


def analisar_hashtags(hashtags: List[str]) -> Dict:
    """Analisa uma lista de hashtags fornecida pelo usuário."""
    resultado = {
        "total": len(hashtags),
        "categorias": {
            "grandes": [],
            "medias": [],
            "pequenas": [],
            "desconhecidas": []
        },
        "nichos_detectados": [],
        "sugestoes": []
    }

    # Classificar cada hashtag
    for hashtag in hashtags:
        hashtag_clean = hashtag.lower().strip()
        if not hashtag_clean.startswith("#"):
            hashtag_clean = f"#{hashtag_clean}"

        encontrada = False
        for nicho, dados in HASHTAGS_DATABASE.items():
            if hashtag_clean in dados.get("grandes", []):
                resultado["categorias"]["grandes"].append(hashtag_clean)
                if nicho not in resultado["nichos_detectados"]:
                    resultado["nichos_detectados"].append(nicho)
                encontrada = True
                break
            elif hashtag_clean in dados.get("medias", []):
                resultado["categorias"]["medias"].append(hashtag_clean)
                if nicho not in resultado["nichos_detectados"]:
                    resultado["nichos_detectados"].append(nicho)
                encontrada = True
                break
            elif hashtag_clean in (dados.get("pequenas", []) + dados.get("nicho", [])):
                resultado["categorias"]["pequenas"].append(hashtag_clean)
                if nicho not in resultado["nichos_detectados"]:
                    resultado["nichos_detectados"].append(nicho)
                encontrada = True
                break

        if not encontrada:
            resultado["categorias"]["desconhecidas"].append(hashtag_clean)

    # Gerar sugestões
    n_grandes = len(resultado["categorias"]["grandes"])
    n_medias = len(resultado["categorias"]["medias"])
    n_pequenas = len(resultado["categorias"]["pequenas"])

    if n_grandes > 5:
        resultado["sugestoes"].append("Muitas hashtags grandes (competitivas). Reduza para 3-4 e adicione mais de nicho.")
    if n_grandes < 2:
        resultado["sugestoes"].append("Adicione 2-3 hashtags grandes para aumentar alcance potencial.")
    if n_pequenas < 3:
        resultado["sugestoes"].append("Adicione mais hashtags de nicho (pequenas) para atingir público qualificado.")
    if len(hashtags) < 10:
        resultado["sugestoes"].append("Use pelo menos 10-15 hashtags para melhor performance no Instagram.")
    if len(hashtags) > 30:
        resultado["sugestoes"].append("Mais de 30 hashtags pode parecer spam. Mantenha entre 10-20.")

    # Score geral
    score = 0
    if 10 <= len(hashtags) <= 20:
        score += 25
    if 2 <= n_grandes <= 4:
        score += 25
    if 4 <= n_medias <= 8:
        score += 25
    if n_pequenas >= 3:
        score += 25

    resultado["score"] = score
    resultado["classificacao"] = (
        "Excelente" if score >= 75 else
        "Bom" if score >= 50 else
        "Regular" if score >= 25 else
        "Precisa melhorar"
    )

    return resultado


def gerar_variantes(nicho: str, quantidade_sets: int = 3) -> List[Dict]:
    """Gera múltiplos sets de hashtags para rotação."""
    variantes = []
    objetivos = ["engajamento", "alcance", "nicho"]

    for i in range(quantidade_sets):
        objetivo = objetivos[i % len(objetivos)]
        set_hashtags = gerar_set_hashtags(nicho, 15, objetivo)
        if "erro" not in set_hashtags:
            variantes.append({
                "set_numero": i + 1,
                "objetivo": objetivo,
                **set_hashtags
            })

    return variantes


def formatar_tabela(resultado: Dict) -> str:
    """Formata resultado em tabela ASCII."""
    linhas = []
    linhas.append("=" * 60)
    linhas.append("  INSTAGRAM HASHTAG RESEARCH")
    linhas.append("=" * 60)

    if "erro" in resultado:
        linhas.append(f"\n❌ {resultado['erro']}")
        linhas.append(f"\nNichos disponíveis: {', '.join(resultado.get('nichos_disponiveis', []))}")
        return "\n".join(linhas)

    linhas.append(f"\n📊 Nicho: {resultado.get('nicho', 'N/A')}")
    linhas.append(f"🎯 Objetivo: {resultado.get('objetivo', 'N/A')}")
    linhas.append(f"📝 Quantidade: {resultado.get('quantidade', 0)} hashtags")

    linhas.append("\n" + "-" * 60)
    linhas.append("HASHTAGS GERADAS:")
    linhas.append("-" * 60)

    hashtags = resultado.get("hashtags", [])
    # Formatar em colunas
    for i in range(0, len(hashtags), 3):
        row = hashtags[i:i+3]
        linhas.append("  " + "  ".join(f"{h:<20}" for h in row))

    linhas.append("\n" + "-" * 60)
    linhas.append("COPIAR/COLAR:")
    linhas.append("-" * 60)
    linhas.append(resultado.get("hashtags_texto", ""))

    if resultado.get("dica"):
        linhas.append("\n💡 " + resultado["dica"])

    return "\n".join(linhas)


def formatar_markdown(resultado: Dict) -> str:
    """Formata resultado em Markdown."""
    linhas = []
    linhas.append("# Instagram Hashtag Research")
    linhas.append(f"\n*Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")

    if "erro" in resultado:
        linhas.append(f"\n**Erro:** {resultado['erro']}")
        linhas.append(f"\n**Nichos disponíveis:** {', '.join(resultado.get('nichos_disponiveis', []))}")
        return "\n".join(linhas)

    linhas.append(f"## Configuração\n")
    linhas.append(f"- **Nicho:** {resultado.get('nicho', 'N/A')}")
    linhas.append(f"- **Objetivo:** {resultado.get('objetivo', 'N/A')}")
    linhas.append(f"- **Quantidade:** {resultado.get('quantidade', 0)} hashtags")

    linhas.append("\n## Hashtags Geradas\n")
    for h in resultado.get("hashtags", []):
        linhas.append(f"- {h}")

    linhas.append("\n## Copiar/Colar\n")
    linhas.append("```")
    linhas.append(resultado.get("hashtags_texto", ""))
    linhas.append("```")

    if resultado.get("dica"):
        linhas.append(f"\n## Dica\n\n{resultado['dica']}")

    return "\n".join(linhas)


def mostrar_ajuda() -> None:
    """Mostra mensagem de ajuda."""
    ajuda = """
╔══════════════════════════════════════════════════════════════════════╗
║                   INSTAGRAM HASHTAG RESEARCH                          ║
║           Pesquisa avançada de hashtags para Instagram                ║
╚══════════════════════════════════════════════════════════════════════╝

USO:
    python instagram_hashtag_research.py <nicho> [opções]

COMANDOS:
    <nicho>              Gerar hashtags para um nicho específico
    --analisar           Analisar hashtags existentes
    --gerar-set          Gerar set otimizado
    --variantes          Gerar múltiplos sets para rotação
    --nichos             Listar nichos disponíveis

OPÇÕES:
    --quantidade <n>     Número de hashtags (padrão: 15)
    --objetivo <obj>     Objetivo: engajamento, alcance, nicho
    --formato <fmt>      Formato de saída: tabela, markdown, json
    -h, --help           Mostrar esta ajuda

EXEMPLOS:
    # Gerar hashtags para marketing digital
    python instagram_hashtag_research.py "marketing digital"

    # Gerar set para alcance máximo
    python instagram_hashtag_research.py "fitness" --objetivo alcance

    # Gerar variantes para rotação
    python instagram_hashtag_research.py --variantes "empreendedorismo"

    # Analisar hashtags existentes
    python instagram_hashtag_research.py --analisar "#marketing,#vendas,#negocios"

    # Listar nichos disponíveis
    python instagram_hashtag_research.py --nichos

NICHOS DISPONÍVEIS:
    marketing_digital, empreendedorismo, fitness, financas,
    moda, gastronomia, tecnologia, desenvolvimento_pessoal,
    beleza, viagem

OBJETIVOS:
    engajamento  - Equilíbrio para interação (padrão)
    alcance      - Máximo de visualizações
    nicho        - Público qualificado e específico
"""
    print(ajuda)


def main() -> None:
    """Função principal."""
    args = sys.argv[1:]

    if not args or '-h' in args or '--help' in args:
        mostrar_ajuda()
        return

    # Listar nichos
    if '--nichos' in args:
        print("\n📋 NICHOS DISPONÍVEIS:")
        print("-" * 40)
        for nicho in HASHTAGS_DATABASE.keys():
            n_total = sum(len(HASHTAGS_DATABASE[nicho].get(cat, []))
                         for cat in ["grandes", "medias", "pequenas", "nicho"])
            print(f"  • {nicho.replace('_', ' ').title()} ({n_total} hashtags)")
        return

    # Parsear argumentos
    nicho = None
    analisar = None
    quantidade = 15
    objetivo = "engajamento"
    formato = "tabela"
    gerar_variantes_flag = False

    i = 0
    while i < len(args):
        arg = args[i]

        if arg == '--analisar' and i + 1 < len(args):
            analisar = args[i + 1].split(',')
            i += 2
        elif arg == '--quantidade' and i + 1 < len(args):
            quantidade = int(args[i + 1])
            i += 2
        elif arg == '--objetivo' and i + 1 < len(args):
            objetivo = args[i + 1]
            i += 2
        elif arg == '--formato' and i + 1 < len(args):
            formato = args[i + 1]
            i += 2
        elif arg == '--gerar-set' and i + 1 < len(args):
            nicho = args[i + 1]
            i += 2
        elif arg == '--variantes' and i + 1 < len(args):
            nicho = args[i + 1]
            gerar_variantes_flag = True
            i += 2
        elif not arg.startswith('--') and nicho is None:
            nicho = arg
            i += 1
        else:
            i += 1

    # Executar comando
    if analisar:
        resultado = analisar_hashtags(analisar)
        if formato == "json":
            print(json.dumps(resultado, indent=2, ensure_ascii=False))
        else:
            print("\n📊 ANÁLISE DE HASHTAGS")
            print("=" * 50)
            print(f"\nTotal: {resultado['total']} hashtags")
            print(f"Score: {resultado['score']}/100 ({resultado['classificacao']})")
            print(f"\nNichos detectados: {', '.join(resultado['nichos_detectados']) or 'Nenhum'}")
            print("\nDistribuição:")
            print(f"  • Grandes: {len(resultado['categorias']['grandes'])}")
            print(f"  • Médias: {len(resultado['categorias']['medias'])}")
            print(f"  • Pequenas: {len(resultado['categorias']['pequenas'])}")
            print(f"  • Não classificadas: {len(resultado['categorias']['desconhecidas'])}")
            if resultado['sugestoes']:
                print("\n💡 Sugestões:")
                for sug in resultado['sugestoes']:
                    print(f"  → {sug}")

    elif gerar_variantes_flag and nicho:
        variantes = gerar_variantes(nicho, 3)
        if not variantes:
            print(f"❌ Não foi possível gerar variantes para '{nicho}'")
            return

        print("\n🔄 VARIANTES DE HASHTAGS PARA ROTAÇÃO")
        print("=" * 60)
        for var in variantes:
            print(f"\n--- SET {var['set_numero']} ({var['objetivo'].upper()}) ---")
            print(var['hashtags_texto'])
        print("\n💡 Dica: Alterne entre os sets para evitar shadowban e testar performance.")

    elif nicho:
        resultado = gerar_set_hashtags(nicho, quantidade, objetivo)

        if formato == "json":
            print(json.dumps(resultado, indent=2, ensure_ascii=False))
        elif formato == "markdown":
            print(formatar_markdown(resultado))
        else:
            print(formatar_tabela(resultado))

    else:
        print("❌ Especifique um nicho ou comando.")
        print("Use --help para ver as opções disponíveis.")


if __name__ == "__main__":
    main()
