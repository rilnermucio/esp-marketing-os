#!/usr/bin/env python3
"""
Hook Variant Generator - Gerador de Variantes de Hooks

Gera múltiplas variações de hooks a partir de um único tema/conteúdo,
otimizadas para diferentes formatos (Reels, Carrossel, Card Único).

Uso:
    python hook_variant_generator.py "tema" [opções]

Exemplos:
    python hook_variant_generator.py "como economizar dinheiro"
    python hook_variant_generator.py "produtividade" --formato reels --quantidade 10
    python hook_variant_generator.py "marketing digital" --nicho marketing --formato carrossel
"""

import sys
import json
import random
from datetime import datetime
from typing import List, Dict, Optional

# ============================================
# BANCO DE FÓRMULAS DE HOOKS
# ============================================

FORMULAS_HOOKS = {
    "curiosidade": [
        "O que ninguém te conta sobre {tema}",
        "A verdade sobre {tema} que você precisa saber",
        "Por trás dos bastidores de {tema}",
        "O segredo de {tema} que especialistas escondem",
        "Descobri isso sobre {tema} e mudou tudo",
        "Você está fazendo {tema} errado",
        "O que acontece quando você {acao_tema}?",
        "Isso explica por que {problema_tema}",
        "A história de {tema} que não te contaram",
        "O lado B de {tema}",
    ],
    "numeros": [
        "7 {coisas_tema} que {resultado}",
        "As 5 {acoes_tema} que mais {beneficio}",
        "10 {erros_tema} que {consequencia}",
        "{percentual}% das pessoas não sabem disso sobre {tema}",
        "3 passos para {resultado_tema}",
        "Os 4 pilares de {tema}",
        "8 sinais de que você {situacao_tema}",
        "De 0 a {resultado} em {tempo} com {tema}",
        "{numero}K {metrica} com {tema}",
        "1 {acao_tema} que vale por {numero}",
    ],
    "dor": [
        "Cansado de {problema_tema}?",
        "Por que você não consegue {objetivo_tema}",
        "O erro que está travando seu {area_tema}",
        "Pare de {acao_errada_tema} agora",
        "Isso está sabotando seu {resultado_tema}",
        "Se você sofre com {problema_tema}, leia isso",
        "O motivo real do seu {problema_tema}",
        "Você está perdendo {valor} com {tema}",
        "Já tentou de tudo em {tema} e nada funciona?",
        "O que ninguém resolve para você em {tema}",
    ],
    "transformacao": [
        "De {antes} para {depois} com {tema}",
        "Como eu {resultado} em {tempo} usando {tema}",
        "A virada que mudou meu {area_tema}",
        "Antes vs Depois de {acao_tema}",
        "O método de {tema} que me fez {conquista}",
        "Finalmente {resultado} com {tema}",
        "De {estado_a} para {estado_b} em {tempo}",
        "A transformação completa com {tema}",
        "O que {pessoa} fez diferente em {tema}",
        "Minha jornada: {inicio} → {resultado} com {tema}",
    ],
    "urgencia": [
        "Você está perdendo tempo sem {tema}",
        "Última chance de {oportunidade_tema}",
        "Antes que seja tarde em {tema}",
        "Enquanto você espera, outros {acao_tema}",
        "O que você precisa saber AGORA sobre {tema}",
        "Pare tudo e leia isso sobre {tema}",
        "{tema} está mudando — você está preparado?",
        "Não cometa esse erro em {tema} hoje",
        "O prazo para {tema} está acabando",
        "Aja agora ou perca {oportunidade_tema}",
    ],
    "autoridade": [
        "Como {numero} pessoas {resultado} com {tema}",
        "O método de {tema} usado por {autoridade}",
        "Testei {tema} por {tempo} e descobri",
        "Dados mostram que {insight_tema}",
        "A ciência por trás de {tema}",
        "O que {expert} recomenda sobre {tema}",
        "Pesquisas revelam sobre {tema}",
        "O framework de {tema} das grandes empresas",
        "+{numero} resultados com {tema}",
        "Por que {autoridade} usa {tema}",
    ],
    "polemica": [
        "Opinião impopular: {afirmacao_tema}",
        "Vão me criticar, mas {verdade_tema}",
        "Discordo sobre {tema} e vou explicar",
        "{mito_tema} é mentira",
        "Por que {pratica_comum_tema} não funciona",
        "A verdade inconveniente sobre {tema}",
        "Ninguém quer falar sobre isso em {tema}",
        "O que está errado com {tema} hoje",
        "Pare de acreditar em {mito_tema}",
        "A mentira que te contaram sobre {tema}",
    ],
    "tutorial": [
        "Como {resultado} em {numero} passos",
        "O guia completo de {tema}",
        "Passo a passo: {acao_tema}",
        "Tutorial: {tema} para iniciantes",
        "Como fazer {tema} do zero",
        "O método simples para {resultado_tema}",
        "Aprenda {tema} em {tempo}",
        "Do básico ao avançado em {tema}",
        "{tema} explicado de forma simples",
        "Como eu faço {tema} (passo a passo)",
    ],
    "storytelling": [
        "A história de como {resultado_tema}",
        "Deixa eu te contar o que aconteceu com {tema}",
        "O dia que {evento_tema} mudou tudo",
        "Eu quase desisti de {tema}, até que...",
        "A lição mais cara que aprendi sobre {tema}",
        "Como {tema} transformou minha vida",
        "A vez que {erro_tema} me ensinou",
        "Minha jornada com {tema} começou assim",
        "O momento em que entendi {tema}",
        "Por que comecei com {tema} (história real)",
    ],
    "comparacao": [
        "{opcao_a} vs {opcao_b}: qual é melhor?",
        "A diferença entre {coisa_a} e {coisa_b} em {tema}",
        "{tema} errado vs {tema} certo",
        "O que funciona vs o que não funciona em {tema}",
        "Iniciante vs Expert em {tema}",
        "Antes vs Depois de entender {tema}",
        "{metodo_a} ou {metodo_b}? A resposta",
        "Comparando {opcao_a} e {opcao_b}",
        "O melhor de {tema}: {opcao_a} ou {opcao_b}?",
        "Por que {opcao_a} supera {opcao_b} em {tema}",
    ],
}

# ============================================
# VARIÁVEIS POR NICHO
# ============================================

VARIAVEIS_NICHO = {
    "marketing": {
        "coisas_tema": ["estratégias", "ferramentas", "técnicas", "métricas", "canais"],
        "acoes_tema": ["geram leads", "convertem", "engajam", "vendem", "escalam"],
        "erros_tema": [
            "erros de anúncio",
            "falhas de copy",
            "problemas de funil",
            "erros de métrica",
        ],
        "resultado": [
            "mais vendas",
            "ROI de 300%",
            "10K seguidores",
            "leads qualificados",
        ],
        "problema_tema": ["não vende", "não engaja", "não converte", "perde dinheiro"],
        "beneficio": ["convertem", "engajam", "geram leads", "aumentam vendas"],
        "autoridade": ["grandes marcas", "top marketeiros", "agências de sucesso"],
        "tempo": ["30 dias", "1 semana", "3 meses"],
    },
    "financas": {
        "coisas_tema": ["investimentos", "economias", "hábitos", "estratégias", "apps"],
        "acoes_tema": ["economizam", "rendem mais", "multiplicam", "protegem"],
        "erros_tema": [
            "erros de investimento",
            "gastos invisíveis",
            "dívidas",
            "desperdícios",
        ],
        "resultado": [
            "R$10K economizados",
            "renda extra",
            "liberdade financeira",
            "carteira sólida",
        ],
        "problema_tema": [
            "não sobra dinheiro",
            "dívidas crescem",
            "não consegue investir",
        ],
        "beneficio": ["economizam", "rendem", "multiplicam patrimônio"],
        "autoridade": ["investidores de sucesso", "economistas", "milionários"],
        "tempo": ["6 meses", "1 ano", "5 anos"],
    },
    "fitness": {
        "coisas_tema": ["exercícios", "alimentos", "suplementos", "rotinas", "treinos"],
        "acoes_tema": [
            "queimam gordura",
            "ganham músculo",
            "melhoram saúde",
            "aumentam energia",
        ],
        "erros_tema": ["erros de treino", "falhas de dieta", "lesões", "estagnação"],
        "resultado": ["10kg a menos", "shape definido", "mais energia", "saúde melhor"],
        "problema_tema": [
            "não emagrece",
            "não ganha músculo",
            "falta energia",
            "lesiona",
        ],
        "beneficio": ["emagrecem", "definem", "fortalecem", "energizam"],
        "autoridade": ["atletas", "nutricionistas", "personal trainers"],
        "tempo": ["3 meses", "12 semanas", "30 dias"],
    },
    "desenvolvimento": {
        "coisas_tema": ["hábitos", "mindsets", "técnicas", "livros", "práticas"],
        "acoes_tema": [
            "transformam",
            "melhoram produtividade",
            "aumentam foco",
            "desenvolvem",
        ],
        "erros_tema": [
            "erros de mindset",
            "crenças limitantes",
            "procrastinação",
            "autossabotagem",
        ],
        "resultado": [
            "mais produtividade",
            "clareza mental",
            "sucesso pessoal",
            "realização",
        ],
        "problema_tema": ["procrastina", "falta foco", "ansiedade", "estagnação"],
        "beneficio": ["focam", "motivam", "transformam", "desenvolvem"],
        "autoridade": ["líderes", "autores best-seller", "coaches de sucesso"],
        "tempo": ["21 dias", "3 meses", "1 ano"],
    },
    "empreendedorismo": {
        "coisas_tema": [
            "estratégias",
            "modelos de negócio",
            "táticas",
            "ferramentas",
            "decisões",
        ],
        "acoes_tema": ["escalam", "faturam", "vendem", "crescem"],
        "erros_tema": [
            "erros de gestão",
            "falhas de venda",
            "problemas de fluxo",
            "contratações erradas",
        ],
        "resultado": ["6 dígitos", "empresa escalável", "liberdade", "time forte"],
        "problema_tema": ["não vende", "não escala", "sem lucro", "sem tempo"],
        "beneficio": ["faturam", "escalam", "lucram", "crescem"],
        "autoridade": ["empresários de sucesso", "investidores", "mentores"],
        "tempo": ["6 meses", "1 ano", "2 anos"],
    },
    "tecnologia": {
        "coisas_tema": ["ferramentas", "apps", "atalhos", "linguagens", "frameworks"],
        "acoes_tema": ["automatizam", "economizam tempo", "facilitam", "otimizam"],
        "erros_tema": [
            "erros de código",
            "bugs",
            "más práticas",
            "ferramentas erradas",
        ],
        "resultado": [
            "mais produtividade",
            "automação",
            "carreira tech",
            "projetos prontos",
        ],
        "problema_tema": [
            "código não funciona",
            "leva muito tempo",
            "não consegue aprender",
        ],
        "beneficio": ["automatizam", "aceleram", "simplificam", "otimizam"],
        "autoridade": ["big techs", "devs sênior", "CTOs"],
        "tempo": ["1 semana", "1 mês", "6 meses"],
    },
    "geral": {
        "coisas_tema": ["dicas", "estratégias", "técnicas", "métodos", "segredos"],
        "acoes_tema": ["melhoram", "transformam", "otimizam", "aceleram"],
        "erros_tema": ["erros comuns", "falhas", "problemas", "obstáculos"],
        "resultado": ["resultados", "transformação", "sucesso", "conquistas"],
        "problema_tema": ["não funciona", "não consegue", "está travado", "não avança"],
        "beneficio": ["funcionam", "transformam", "melhoram", "resolvem"],
        "autoridade": ["especialistas", "profissionais", "experts"],
        "tempo": ["30 dias", "3 meses", "1 ano"],
    },
}

# ============================================
# ADAPTAÇÕES POR FORMATO
# ============================================

ADAPTACOES_FORMATO = {
    "reels": {
        "prefixos": ["", "POV:", "Storytime:", "ATENÇÃO:", ""],
        "sufixos": ["", " 🔥", " 👀", " (parte 1)", " #viral"],
        "max_caracteres": 100,
        "estilo": "direto e impactante",
    },
    "carrossel": {
        "prefixos": ["", "SALVA ESSE:", "GUIA:", "THREAD:", ""],
        "sufixos": ["", " (arraste →)", " [10 slides]", "", ""],
        "max_caracteres": 80,
        "estilo": "promessa de valor completo",
    },
    "card": {
        "prefixos": ["", "💡", "⚠️", "🔥", ""],
        "sufixos": ["", "", "", "", ""],
        "max_caracteres": 125,
        "estilo": "impacto em uma frase",
    },
}


def preencher_variaveis(formula: str, tema: str, nicho: str = "geral") -> str:
    """Preenche as variáveis da fórmula com valores do nicho."""
    variaveis = VARIAVEIS_NICHO.get(nicho, VARIAVEIS_NICHO["geral"])

    resultado = formula.replace("{tema}", tema)

    # Substituir variáveis específicas
    for var_nome, var_valores in variaveis.items():
        placeholder = "{" + var_nome + "}"
        if placeholder in resultado:
            resultado = resultado.replace(placeholder, random.choice(var_valores))

    # Substituir variáveis genéricas restantes
    substituicoes_genericas = {
        "{acao_tema}": f"dominar {tema}",
        "{objetivo_tema}": f"ter sucesso com {tema}",
        "{area_tema}": tema,
        "{acao_errada_tema}": f"ignorar {tema}",
        "{resultado_tema}": f"resultados com {tema}",
        "{valor}": "oportunidades",
        "{antes}": "iniciante",
        "{depois}": "expert",
        "{estado_a}": "zero",
        "{estado_b}": "sucesso",
        "{conquista}": "alcançar resultados",
        "{pessoa}": "quem tem sucesso",
        "{inicio}": "o começo",
        "{oportunidade_tema}": f"aproveitar {tema}",
        "{insight_tema}": f"{tema} funciona",
        "{expert}": "especialistas",
        "{afirmacao_tema}": f"{tema} não é o que parece",
        "{verdade_tema}": f"a verdade sobre {tema}",
        "{mito_tema}": f"mitos de {tema}",
        "{pratica_comum_tema}": f"o comum em {tema}",
        "{evento_tema}": tema,
        "{erro_tema}": f"errar em {tema}",
        "{opcao_a}": "Método A",
        "{opcao_b}": "Método B",
        "{coisa_a}": "isso",
        "{coisa_b}": "aquilo",
        "{metodo_a}": "forma tradicional",
        "{metodo_b}": "forma moderna",
        "{numero}": str(random.choice([3, 5, 7, 10])),
        "{percentual}": str(random.choice([80, 90, 95, 99])),
        "{situacao_tema}": f"está errando em {tema}",
        "{metrica}": "resultados",
        "{consequencia}": "prejudicam seus resultados",
    }

    for placeholder, valor in substituicoes_genericas.items():
        resultado = resultado.replace(placeholder, valor)

    return resultado


def adaptar_para_formato(hook: str, formato: str) -> str:
    """Adapta o hook para o formato específico."""
    config = ADAPTACOES_FORMATO.get(formato, ADAPTACOES_FORMATO["card"])

    # Adicionar prefixo aleatório
    prefixo = random.choice(config["prefixos"])
    if prefixo:
        hook = f"{prefixo} {hook}"

    # Adicionar sufixo aleatório
    sufixo = random.choice(config["sufixos"])
    if sufixo:
        hook = f"{hook}{sufixo}"

    # Truncar se necessário
    if len(hook) > config["max_caracteres"]:
        hook = hook[: config["max_caracteres"] - 3] + "..."

    return hook


def gerar_variantes(
    tema: str,
    quantidade: int = 5,
    nicho: str = "geral",
    formato: str = "card",
    categorias: Optional[List[str]] = None,
) -> List[Dict]:
    """Gera múltiplas variantes de hooks para um tema."""

    if categorias is None:
        categorias = list(FORMULAS_HOOKS.keys())

    variantes = []
    formulas_usadas = set()

    tentativas = 0
    max_tentativas = quantidade * 10

    while len(variantes) < quantidade and tentativas < max_tentativas:
        tentativas += 1

        # Selecionar categoria e fórmula
        categoria = random.choice(categorias)
        formula = random.choice(FORMULAS_HOOKS[categoria])

        # Evitar repetição de fórmulas
        if formula in formulas_usadas:
            continue
        formulas_usadas.add(formula)

        # Preencher e adaptar
        hook = preencher_variaveis(formula, tema, nicho)
        hook = adaptar_para_formato(hook, formato)

        variantes.append(
            {
                "hook": hook,
                "categoria": categoria,
                "formato": formato,
                "caracteres": len(hook),
            }
        )

    return variantes


def formatar_saida_tabela(variantes: List[Dict], tema: str) -> str:
    """Formata a saída em tabela ASCII."""
    linhas = []
    linhas.append("=" * 70)
    linhas.append("  HOOK VARIANT GENERATOR")
    linhas.append("=" * 70)
    linhas.append(f"\n📌 Tema: {tema}")
    linhas.append(f"📊 Variantes geradas: {len(variantes)}")
    linhas.append("\n" + "-" * 70)

    for i, v in enumerate(variantes, 1):
        linhas.append(f"\n{i}. [{v['categoria'].upper()}] ({v['caracteres']} chars)")
        linhas.append(f"   \"{v['hook']}\"")

    linhas.append("\n" + "-" * 70)
    linhas.append("\n💡 DICAS DE USO:")
    linhas.append("  • Teste 3-5 variantes no mesmo conteúdo")
    linhas.append("  • Meça taxa de engajamento de cada hook")
    linhas.append("  • Documente os padrões vencedores")
    linhas.append("  • Adapte os vencedores para outros temas")

    return "\n".join(linhas)


def formatar_saida_markdown(variantes: List[Dict], tema: str) -> str:
    """Formata a saída em Markdown."""
    linhas = []
    linhas.append(f"# Variantes de Hook: {tema}")
    linhas.append(f"\n*Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
    linhas.append(f"**Total de variantes:** {len(variantes)}\n")
    linhas.append("---\n")

    # Agrupar por categoria
    por_categoria = {}
    for v in variantes:
        cat = v["categoria"]
        if cat not in por_categoria:
            por_categoria[cat] = []
        por_categoria[cat].append(v)

    for categoria, hooks in por_categoria.items():
        linhas.append(f"## {categoria.title()}\n")
        for h in hooks:
            linhas.append(f"- \"{h['hook']}\" *({h['caracteres']} chars)*")
        linhas.append("")

    linhas.append("---\n")
    linhas.append("## Como usar\n")
    linhas.append("1. Selecione 3-5 variantes para testar")
    linhas.append("2. Use o mesmo visual/conteúdo, mude só o hook")
    linhas.append("3. Publique em horários similares")
    linhas.append("4. Compare engajamento após 48h")
    linhas.append("5. Documente o padrão vencedor")

    return "\n".join(linhas)


def formatar_saida_json(variantes: List[Dict], tema: str) -> str:
    """Formata a saída em JSON."""
    output = {
        "tema": tema,
        "gerado_em": datetime.now().isoformat(),
        "total_variantes": len(variantes),
        "variantes": variantes,
    }
    return json.dumps(output, indent=2, ensure_ascii=False)


def mostrar_ajuda() -> None:
    """Mostra mensagem de ajuda."""
    ajuda = """
╔══════════════════════════════════════════════════════════════════════╗
║                    HOOK VARIANT GENERATOR                             ║
║           Gerar múltiplas variações de hooks para testes             ║
╚══════════════════════════════════════════════════════════════════════╝

USO:
    python hook_variant_generator.py "<tema>" [opções]

ARGUMENTOS:
    tema                 O tema/assunto do conteúdo (obrigatório)

OPÇÕES:
    --quantidade <n>     Número de variantes (padrão: 5)
    --nicho <nicho>      Nicho específico para adaptação
    --formato <formato>  Formato: reels, carrossel, card (padrão: card)
    --categoria <cat>    Filtrar por categoria de hook
    --output <fmt>       Formato de saída: tabela, markdown, json
    -h, --help           Mostrar esta ajuda

NICHOS DISPONÍVEIS:
    marketing, financas, fitness, desenvolvimento, empreendedorismo,
    tecnologia, geral

CATEGORIAS DE HOOK:
    curiosidade, numeros, dor, transformacao, urgencia, autoridade,
    polemica, tutorial, storytelling, comparacao

FORMATOS:
    reels      - Hooks curtos e impactantes para vídeos
    carrossel  - Hooks com promessa de conteúdo completo
    card       - Hooks versáteis para posts únicos

EXEMPLOS:
    # Gerar 5 variantes para "marketing digital"
    python hook_variant_generator.py "marketing digital"

    # Gerar 10 variantes para Reels sobre finanças
    python hook_variant_generator.py "economizar dinheiro" --quantidade 10 --formato reels --nicho financas

    # Gerar hooks de curiosidade para carrossel
    python hook_variant_generator.py "produtividade" --formato carrossel --categoria curiosidade

    # Exportar em Markdown
    python hook_variant_generator.py "vendas" --output markdown

    # Exportar em JSON para integração
    python hook_variant_generator.py "fitness" --output json --quantidade 20
"""
    print(ajuda)


def main() -> None:
    """Função principal."""
    args = sys.argv[1:]

    if not args or "-h" in args or "--help" in args:
        mostrar_ajuda()
        return

    # Parsear argumentos
    tema = None
    quantidade = 5
    nicho = "geral"
    formato = "card"
    categoria = None
    output = "tabela"

    i = 0
    while i < len(args):
        arg = args[i]

        if arg == "--quantidade" and i + 1 < len(args):
            quantidade = int(args[i + 1])
            i += 2
        elif arg == "--nicho" and i + 1 < len(args):
            nicho = args[i + 1].lower()
            i += 2
        elif arg == "--formato" and i + 1 < len(args):
            formato = args[i + 1].lower()
            i += 2
        elif arg == "--categoria" and i + 1 < len(args):
            categoria = args[i + 1].lower()
            i += 2
        elif arg == "--output" and i + 1 < len(args):
            output = args[i + 1].lower()
            i += 2
        elif not arg.startswith("--") and tema is None:
            tema = arg
            i += 1
        else:
            i += 1

    if not tema:
        print("❌ Erro: Especifique um tema.")
        print("Use --help para ver as opções disponíveis.")
        return

    # Validar nicho
    if nicho not in VARIAVEIS_NICHO:
        print(f"⚠️ Nicho '{nicho}' não encontrado. Usando 'geral'.")
        nicho = "geral"

    # Validar formato
    if formato not in ADAPTACOES_FORMATO:
        print(f"⚠️ Formato '{formato}' não encontrado. Usando 'card'.")
        formato = "card"

    # Preparar categorias
    categorias = None
    if categoria:
        if categoria in FORMULAS_HOOKS:
            categorias = [categoria]
        else:
            print(f"⚠️ Categoria '{categoria}' não encontrada. Usando todas.")

    # Gerar variantes
    variantes = gerar_variantes(
        tema=tema,
        quantidade=quantidade,
        nicho=nicho,
        formato=formato,
        categorias=categorias,
    )

    # Formatar saída
    if output == "json":
        print(formatar_saida_json(variantes, tema))
    elif output == "markdown":
        print(formatar_saida_markdown(variantes, tema))
    else:
        print(formatar_saida_tabela(variantes, tema))


if __name__ == "__main__":
    main()
