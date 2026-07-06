#!/usr/bin/env python3
"""
Marketing OS — PreToolUse Quality Gate Hook

Valida escritas (Write/Edit/MultiEdit) contra regras de qualidade do Marketing OS.
Ativado via frontmatter `hooks:` em cada `agents/mos-*.md`.

Tres niveis de validacao:

1. HARD BLOCK (exit 2): violacoes inegociaveis que sempre indicam saida ruim
   - Em-dash '—' (use '.', ',' ou ':')
   - Palavra "brutal" (use: intenso, forte, pesado, impactante, poderoso)
   - Antitese negacao/afirmacao: 'Não é X / É Y', 'Não faça X / Faça Y'
     (AI-tell classico; reescrever afirmando direto)

2. WARN (exit 0 + stderr): cliches PT-BR e AI-tells que provavelmente sao
   ruins mas tem uso legitimo ocasional. Agent ve a mensagem e decide.

3. COMPLIANCE WARN (exit 0 + stderr): trigger words que exigem disclaimer
   regulatorio (CVM/ANVISA/CONAR) sem disclaimer presente.

Paths ignorados: arquivos de tooling, config, docs internas, knowledge
bases didaticas.

Protocolo Claude Code hooks:
- Stdin: JSON com tool_name, tool_input
- Exit 0: permitir (com warnings opcionais em stderr)
- Exit 2: bloquear (com mensagem em stderr)

Defensivo: qualquer excecao interna -> exit 0 (nao quebrar agent).
"""
import json
import re
import sys

SKIP_PATH_PATTERNS = [
    r'\.claude/',
    r'subagents/.*\.md$',
    r'scripts/',
    r'docs/',
    r'\.github/',
    r'CHANGELOG\.md$',
    r'README\.md$',
    r'CLAUDE\.md$',
    r'CONTRIBUTING\.md$',
    r'LICENSE$',
    r'\.json$',
    r'\.ya?ml$',
    r'\.py$',
    r'\.sh$',
    r'\.txt$',
    r'\.gitignore$',
    r'commands/.*\.md$',
    r'workflows/.*\.md$',
    r'references/.*\.md$',
    r'tests/',
]

# HARD BLOCKS: violacoes inegociaveis. Exit 2.
# Antiteses: o span interno exclui pontuacao pra nao atravessar clausulas
# (senao "nao sabe por onde comecar, comece pelo basico. Sabe..." viraria
# falso positivo ao casar o verbo de uma frase nova nao relacionada).
HARD_BLOCK_PATTERNS = [
    (r'—', "Em-dash '—' proibido. Use '.', ',' ou ':' em vez disso, ou quebre a frase."),
    (r'(?<!\w)brutal(?!\w)',
     "Palavra 'brutal' proibida. Use: intenso, forte, pesado, impactante, poderoso."),
    (r'\bnão é [^.!?,;:\n]{2,60}[.!?,;:]\s+é\b',
     "Antítese negação/afirmação detectada ('Não é X / É Y'). "
     "Reescreva afirmando direto, sem o paralelo."),
    (r'\bnão (\w{3,})\b[^.!?,;:\n]{0,60}[.!?,;:]\s+\1\b',
     "Antítese com verbo repetido detectada ('Não faça X / Faça Y'). "
     "Reescreva sem o paralelo negação/afirmação."),
]

# WARNS: cliches PT-BR e AI-tells. Exit 0 + stderr.
# Casos onde uso legitimo existe mas raramente. Agent decide se reescreve.
WARN_PATTERNS = [
    (r'\bem um mundo onde\b',
     "Clichê de abertura 'em um mundo onde' detectado. Reescreva com contexto especifico."),
    (r'\bnum mundo onde\b',
     "Clichê de abertura 'num mundo onde' detectado."),
    (r'\bsem mais delongas\b',
     "Filler 'sem mais delongas' detectado. Remova ou substitua por transicao especifica."),
    (r'\bvamos mergulhar\b',
     "Cliche 'vamos mergulhar' detectado. Use verbo concreto: explorar, analisar, decompor."),
    (r'\bé importante destacar\b',
     "Filler 'é importante destacar' detectado. Va direto ao ponto."),
    (r'\bvale (ressaltar|destacar|notar|frisar)\b',
     "Filler 'vale ressaltar/destacar' detectado. Va direto ao ponto."),
    (r'\bem última análise\b',
     "Filler 'em última análise' detectado. Pode ser cortado em 90% dos casos."),
    (r'\bdito isso\b',
     "Conector 'dito isso' detectado. Verifique se nao e filler."),
    (r'\bimagine se\b',
     "Cliche 'imagine se' detectado. Frame com cenario concreto em vez de hipotetico."),
    (r'\be se eu te dissesse\b',
     "Cliche 'e se eu te dissesse' detectado. Diga diretamente."),
    (r'\bpreparados\? vamos lá\b',
     "Cliche 'preparados? vamos lá' detectado."),
    (r'\bliteralmente\b',
     "'Literalmente' detectado. Verifique se esta sendo usado literalmente, nao como enfase."),
    (r'\bna verdade,?\s',
     "'Na verdade' detectado. Frequentemente filler. Verifique necessidade."),
    (r'\bbasicamente,?\s',
     "'Basicamente' detectado. Frequentemente filler. Cortar se nao adicionar precisao."),
    (r'\bsimplesmente,?\s',
     "'Simplesmente' detectado. Frequentemente filler ou minimizador."),
    (r'\b(extraordinário|revolucionário|incrível|inacreditável)\b',
     "Superlativo vago detectado. Substitua por dado especifico ou prova concreta."),
    (r'\bo melhor (do mundo|do planeta|do mercado|de todos)\b',
     "Superlativo nao verificavel detectado. Use claim especifico com fonte."),
    (r'\bnão (se trata de|é (uma )?questão de)\b[^.!?\n]{2,80}\b(mas|e sim)\b',
     "Antítese suave detectada ('não se trata de X, mas de Y'). "
     "Variante do AI-tell de negação/afirmação. Considere afirmar direto."),
]

# COMPLIANCE TRIGGERS: palavras que exigem disclaimer regulatorio se ausente.
COMPLIANCE_RULES = [
    {
        'name': 'CVM (financeiro)',
        'triggers': [
            r'\binvestimento(s)?\b',
            r'\brentabilidade\b',
            r'\brenda fixa\b',
            r'\brenda variável\b',
            r'\b(retorno|ganho)\s+(garantido|certo)\b',
        ],
        'disclaimer_signals': [
            r'risco',
            r'\bCVM\b',
            r'rentabilidade passada',
            r'profissional certificado',
        ],
        'message': (
            "Conteudo financeiro detectado SEM disclaimer CVM. Adicione algo como: "
            "'Investimentos envolvem riscos. Rentabilidade passada nao garante "
            "resultados futuros.'"
        ),
    },
    {
        'name': 'ANVISA (saude)',
        'triggers': [
            r'\bemagrec(er|imento)\b',
            r'\bcurar?\b',
            r'\btratamento\b',
            r'\bdoenç(a|as)\b',
            r'\bsintoma(s)?\b',
        ],
        'disclaimer_signals': [
            r'consulta médica',
            r'orientação médica',
            r'profissional de saúde',
            r'\bANVISA\b',
            r'avaliação médica',
        ],
        'message': (
            "Conteudo de saude detectado SEM disclaimer ANVISA. Adicione algo como: "
            "'Este conteudo e informativo e nao substitui orientacao medica profissional.'"
        ),
    },
    {
        'name': 'CONAR (depoimentos)',
        'triggers': [
            r'\bdepoimento\b',
            r'\bcase de cliente\b',
            r'\bresultado de aluno\b',
        ],
        'disclaimer_signals': [
            r'resultado.*var(iar|ia)',
            r'\bCONAR\b',
            r'individuais',
        ],
        'message': (
            "Depoimento detectado SEM disclaimer CONAR. Adicione algo como: "
            "'Depoimento real. Resultados individuais podem variar.'"
        ),
    },
    {
        'name': 'Afiliado',
        'triggers': [
            r'\blink afiliado\b',
            r'\bcomissão de afiliado\b',
        ],
        'disclaimer_signals': [
            r'links?\s+afiliados?',
            r'comiss(ão|ao).*sem custo',
        ],
        'message': (
            "Conteudo com link afiliado detectado SEM disclosure. Adicione algo como: "
            "'Este conteudo contem links afiliados. Posso receber comissao sem custo "
            "adicional para voce.'"
        ),
    },
]


def should_skip(file_path: str) -> bool:
    if not file_path:
        return True
    for pat in SKIP_PATH_PATTERNS:
        if re.search(pat, file_path):
            return True
    return False


def extract_content(tool_name: str, tool_input: dict) -> str:
    if tool_name == 'Write':
        return tool_input.get('content', '') or ''
    if tool_name == 'Edit':
        return tool_input.get('new_string', '') or ''
    if tool_name == 'MultiEdit':
        edits = tool_input.get('edits') or []
        return ' '.join((e.get('new_string') or '') for e in edits)
    return ''


def find_hard_violations(content: str) -> list:
    violations = []
    for pat, msg in HARD_BLOCK_PATTERNS:
        # IGNORECASE em tudo: neutro pro em-dash, necessario pro 'brutal' e
        # pro backreference \1 casar 'faça'/'Faça' nas antiteses.
        if re.search(pat, content, flags=re.IGNORECASE):
            violations.append(msg)
    return violations


def find_warnings(content: str) -> list:
    warnings = []
    for pat, msg in WARN_PATTERNS:
        if re.search(pat, content, flags=re.IGNORECASE):
            warnings.append(msg)
    return warnings


def find_compliance_warnings(content: str) -> list:
    warnings = []
    content_lower = content.lower()
    for rule in COMPLIANCE_RULES:
        triggered = any(re.search(t, content_lower) for t in rule['triggers'])
        if not triggered:
            continue
        has_disclaimer = any(re.search(d, content_lower) for d in rule['disclaimer_signals'])
        if has_disclaimer:
            continue
        warnings.append(f"[{rule['name']}] {rule['message']}")
    return warnings


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    tool_name = data.get('tool_name', '')
    tool_input = data.get('tool_input', {}) or {}
    file_path = tool_input.get('file_path', '') or ''

    if tool_name not in ('Write', 'Edit', 'MultiEdit'):
        return 0

    if should_skip(file_path):
        return 0

    content = extract_content(tool_name, tool_input)
    if not content:
        return 0

    hard = find_hard_violations(content)
    warns = find_warnings(content)
    compliance = find_compliance_warnings(content)

    # Print warnings to stderr (always shown to agent)
    if warns or compliance:
        print(f"Quality Gate (Marketing OS) avisos em {file_path}:", file=sys.stderr)
        for w in warns:
            print(f"  WARN: {w}", file=sys.stderr)
        for c in compliance:
            print(f"  COMPLIANCE: {c}", file=sys.stderr)

    # Hard block: fail with exit 2
    if hard:
        print(f"Quality Gate (Marketing OS) bloqueou escrita em {file_path}:", file=sys.stderr)
        for v in hard:
            print(f"  BLOCK: {v}", file=sys.stderr)
        print("Reescreva eliminando as violacoes e tente novamente.", file=sys.stderr)
        return 2

    # Warns alone don't block
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
