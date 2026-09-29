#!/usr/bin/env python3
"""
Marketing OS: Quality Gate Hook

Valida escritas (Write/Edit/MultiEdit) e a resposta final dos agents mos-*
contra as regras de qualidade do Marketing OS. Registrado no nível do plugin
em hooks/hooks.json (PreToolUse e SubagentStop). Hooks no frontmatter de
agent de plugin são ignorados pela plataforma (ADR-0005).

Escopo: só eventos originados por um agent do Marketing OS. O runtime envia o
nome qualificado (`marketing-os:mos-copy`); instalação local usa `mos-copy`.
Escritas da sessão principal do usuário e de outros plugins passam direto.

Três níveis de validação:

1. HARD BLOCK (exit 2 + stderr, que o modelo recebe como motivo do bloqueio)
   - Travessão '—' e travessão curto ' – ' usado como pontuação
   - "brutal", "brutalmente", "brutais"
   - Antítese negação/afirmação: 'Não é X / É Y', 'Não faça X / Faça Y'

2. WARN (exit 0 + JSON additionalContext): clichês PT-BR, AI-tells, CAPS e
   excesso de emojis. O agent vê a mensagem e decide.

3. COMPLIANCE WARN (exit 0 + JSON additionalContext): gatilhos que pedem
   disclaimer regulatório (CVM/ANVISA/CONAR/afiliado) sem disclaimer presente.

Stderr com exit 0 só vai para o log de debug e o modelo nunca vê; por isso os
avisos saem em JSON no stdout.

Defensivo: qualquer exceção interna -> exit 0 (não quebrar o agent).
MOS_HOOK_LOG=<arquivo> registra cada evento em JSON por linha (smoke tests).
"""

import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone

PLUGIN_NAME = "marketing-os"


@dataclass
class GateResult:
    """Resultado observável do quality gate para qualquer adapter de hook."""

    blocked: bool = False
    hard: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    compliance: list[str] = field(default_factory=list)
    context: str = "conteúdo"
    retry_exhausted: bool = False
    # Motivo quando o evento nem chega a ser avaliado (fora do escopo do gate).
    skip_reason: str = ""


# Arquivos que não são peça de marketing: código, configuração e docs de
# projeto. Diretórios nunca entram aqui como substring solta: uma pasta docs/
# no projeto do usuário pode conter copy (auditoria 2026-09-28, achado #16).
SKIP_SUFFIXES = {
    ".json",
    ".yaml",
    ".yml",
    ".py",
    ".sh",
    ".js",
    ".mjs",
    ".ts",
    ".css",
    ".toml",
    ".ini",
    ".cfg",
    ".lock",
}
SKIP_BASENAMES = {
    "CHANGELOG.md",
    "README.md",
    "CLAUDE.md",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "LICENSE",
    ".gitignore",
}
# Estado do Claude Code (memória dos agents, settings), como segmento de caminho.
CLAUDE_STATE_SEGMENT = re.compile(r"(^|/)\.claude/")

# HARD BLOCKS: violações inegociáveis. Exit 2.
# Antíteses: o span interno exclui pontuação pra não atravessar cláusulas
# (senão "não sabe por onde começar, comece pelo básico. Sabe..." viraria
# falso positivo ao casar o verbo de uma frase nova não relacionada).
HARD_BLOCK_PATTERNS = [
    (
        r"—",
        "Travessão '—' proibido. Use '.', ',' ou ':' em vez disso, ou quebre a frase.",
    ),
    (
        r"(?<=\s)–(?=\s)",
        "Travessão curto ' – ' usado como pontuação. Use '.', ',' ou ':' ou quebre a frase.",
    ),
    (
        r"(?<!\w)(brutal(mente)?|brutais)(?!\w)",
        "Palavra 'brutal' (ou variação) proibida. Use: intenso, forte, pesado, impactante, poderoso.",
    ),
    (
        # Cópula na negação e na afirmação, em qualquer combinação: "Não é X. É
        # Y.", "Não é X. São Y.", "Não era X. Foi Y." (a baseline AO-001 de
        # 2026-09-28 mostrou "São" escapando). "São" seguido de maiúscula é nome
        # próprio (São Paulo) e fica de fora.
        r"\bnão (?:é|são|era|eram|foi|foram) [^.!?,;:\n]{2,60}[.!?,;:]\s+"
        r"(?:é|são(?!\s+(?-i:[A-ZÁÉÍÓÚÂÊÔÃÕ]))|era|eram|foi|foram)\b",
        "Antítese negação/afirmação detectada ('Não é X / É Y', 'Não é X / São Y'). "
        "Reescreva afirmando direto, sem o paralelo.",
    ),
    (
        r"\bnão (\w{3,})\b[^.!?,;:\n]{0,60}[.!?,;:]\s+\1\b",
        "Antítese com verbo repetido detectada ('Não faça X / Faça Y'). "
        "Reescreva sem o paralelo negação/afirmação.",
    ),
]

# WARNS: clichês PT-BR e AI-tells. Exit 0 + additionalContext.
# Casos onde uso legítimo existe mas raramente. Agent decide se reescreve.
WARN_PATTERNS = [
    (
        r"\bem um mundo onde\b",
        "Clichê de abertura 'em um mundo onde' detectado. Reescreva com contexto específico.",
    ),
    (r"\bnum mundo onde\b", "Clichê de abertura 'num mundo onde' detectado."),
    (
        r"\bsem mais delongas\b",
        "Filler 'sem mais delongas' detectado. Remova ou substitua por transição específica.",
    ),
    (
        r"\bvamos mergulhar\b",
        "Clichê 'vamos mergulhar' detectado. Use verbo concreto: explorar, analisar, decompor.",
    ),
    (
        r"\bé importante destacar\b",
        "Filler 'é importante destacar' detectado. Vá direto ao ponto.",
    ),
    (
        r"\bvale (ressaltar|destacar|notar|frisar)\b",
        "Filler 'vale ressaltar/destacar' detectado. Vá direto ao ponto.",
    ),
    (
        r"\bem última análise\b",
        "Filler 'em última análise' detectado. Pode ser cortado em 90% dos casos.",
    ),
    (r"\bdito isso\b", "Conector 'dito isso' detectado. Verifique se não é filler."),
    (
        r"\bimagine se\b",
        "Clichê 'imagine se' detectado. Enquadre com cenário concreto em vez de hipotético.",
    ),
    (
        r"\be se eu te dissesse\b",
        "Clichê 'e se eu te dissesse' detectado. Diga diretamente.",
    ),
    (r"\bpreparados\? vamos lá\b", "Clichê 'preparados? vamos lá' detectado."),
    (
        r"\bliteralmente\b",
        "'Literalmente' detectado. Verifique se está sendo usado literalmente, não como ênfase.",
    ),
    (
        r"\bna verdade,?\s",
        "'Na verdade' detectado. Frequentemente filler. Verifique a necessidade.",
    ),
    (
        r"\bbasicamente,?\s",
        "'Basicamente' detectado. Frequentemente filler. Corte se não adicionar precisão.",
    ),
    (
        r"\bsimplesmente,?\s",
        "'Simplesmente' detectado. Frequentemente filler ou minimizador.",
    ),
    (
        r"\b(extraordinário|revolucionário|incrível|inacreditável)\b",
        "Superlativo vago detectado. Substitua por dado específico ou prova concreta.",
    ),
    (
        r"\bo melhor (do mundo|do planeta|do mercado|de todos)\b",
        "Superlativo não verificável detectado. Use claim específico com fonte.",
    ),
    (
        r"\bnão (se trata de|é (uma )?questão de)\b[^.!?\n]{2,80}\b(mas|e sim)\b"
        r"|\bnão (é|são|foi|era)\b[^.!?\n]{2,60}\be sim\b",
        "Antítese suave detectada ('não se trata de X, mas de Y'). "
        "Variante do AI-tell de negação/afirmação. Considere afirmar direto.",
    ),
]

# Palavras em CAPS (regra global): sequência de 5+ letras maiúsculas que não
# seja sigla conhecida. Só aviso: títulos e siglas novas têm uso legítimo.
CAPS_PATTERN = re.compile(r"(?<![\w])[A-ZÁÉÍÓÚÂÊÔÃÕÇ]{5,}(?![\w])")
# Caixa alta exigida por norma: a Res. CFM 2.336/2023 manda escrever "MÉDICO" na
# identificação e "NÃO ESPECIALISTA" quando não há RQE (arts. 4º e 13, §1º).
REGULATORY_CAPS = re.compile(r"(?<![\w])(MÉDIC[OA]|NÃO ESPECIALISTA)(?![\w])")
CAPS_ALLOWLIST = {
    "ANVISA",
    "CONAR",
    "PROCON",
    "SEBRAE",
    "INMETRO",
    "BACEN",
    "CONFEF",
    "CREFITO",
    "HTTPS",
    "UTF8",
}
# Excesso de emojis (regra global: no máximo 2 por peça).
EMOJI_PATTERN = re.compile(
    "[\U0001f300-\U0001faff\U0001f000-\U0001f2ff\U00002600-\U000027bf]"
)
MAX_EMOJIS = 2

# COMPLIANCE TRIGGERS: palavras que exigem disclaimer regulatório se ausente.
# Tudo em minúsculas: o texto é comparado em minúsculas.
COMPLIANCE_RULES = [
    {
        "name": "CVM (financeiro)",
        "triggers": [
            r"\binvestimento(s)?\b",
            r"\brentabilidade\b",
            r"\brenda fixa\b",
            r"\brenda variável\b",
            r"\b(retorno|ganho)\s+(garantido|certo)\b",
        ],
        "disclaimer_signals": [
            r"risco",
            r"\bcvm\b",
            r"rentabilidade passada",
            r"profissional certificado",
        ],
        "message": (
            "Conteúdo financeiro detectado SEM disclaimer CVM. Adicione algo como: "
            "'Investimentos envolvem riscos. Rentabilidade passada não garante "
            "resultados futuros.'"
        ),
    },
    {
        "name": "ANVISA (saúde)",
        "triggers": [
            r"\bemagrec(er|imento)\b",
            r"\bcurar?\b",
            r"\btratamento\b",
            r"\bdoenç(a|as)\b",
            r"\bsintoma(s)?\b",
        ],
        "disclaimer_signals": [
            r"consulta médica",
            r"orientação médica",
            r"profissional de saúde",
            r"\banvisa\b",
            r"avaliação médica",
        ],
        "message": (
            "Conteúdo de saúde detectado SEM disclaimer ANVISA. Adicione algo como: "
            "'Este conteúdo é informativo e não substitui orientação médica profissional.'"
        ),
    },
    {
        "name": "CONAR (depoimentos)",
        "triggers": [
            r"\bdepoimento\b",
            r"\bcase de cliente\b",
            r"\bresultado de aluno\b",
        ],
        "disclaimer_signals": [
            r"resultado.*var(iar|ia)",
            r"\bconar\b",
            r"individuais",
        ],
        "message": (
            "Depoimento detectado SEM disclaimer CONAR. Adicione algo como: "
            "'Depoimento real. Resultados individuais podem variar.' O depoimento "
            "precisa ser genuíno, comprovável e autorizado por escrito (CONAR, "
            "art. 27, §9º)."
        ),
    },
    {
        "name": "Afiliado",
        "triggers": [
            r"\blink afiliado\b",
            r"\bcomissão de afiliado\b",
        ],
        "disclaimer_signals": [
            r"links?\s+afiliados?",
            r"comiss(ão|ao).*sem custo",
        ],
        "message": (
            "Conteúdo com link afiliado detectado SEM disclosure. Adicione algo como: "
            "'Este conteúdo contém links afiliados. Posso receber comissão sem custo "
            "adicional para você.'"
        ),
    },
    # Frases de risco: nenhum aviso resolve, então disclaimer_signals fica vazio.
    # Artigos conferidos no texto integral das normas em 2026-09-28; detalhes e
    # fontes em references/compliance-br.md.
    {
        "name": "Promessa de resultado",
        "triggers": [
            r"\bresultados?\s+garantidos?\b",
            r"\bgarantia\s+de\s+resultados?\b",
            r"\bgarant(e|o|imos)\s+(o\s+|os\s+|seu\s+|seus\s+)?resultados?\b",
            r"\b100%\s+(garantido|eficaz|efetivo)\b",
        ],
        "disclaimer_signals": [],
        "message": (
            "Promessa de resultado. Vedada para médico (CFM 2.336/2023, art. 11, XII), "
            "dentista (CFO-196/2019, art. 2º), nutricionista (CFN 599/2018, art. 56), "
            "psicólogo (CFP, art. 20, e) e advogado (Prov. OAB 205/2021, art. 6º), e "
            "enganosa pelo CDC (art. 37) se não for comprovável."
        ),
    },
    {
        "name": "Promessa de ganho",
        "triggers": [
            r"\bfatur(e|ar|ando)\s+(até\s+|mais\s+de\s+)?r\$\s?\d",
            r"\bganh(e|ar)\s+(até\s+|mais\s+de\s+)?r\$\s?\d",
            r"\brenda\s+extra\s+garantida\b",
            r"\blucro\s+garantido\b",
            r"\bdinheiro\s+(fácil|sem\s+esforço)\b",
            r"\bganh(e|ar)\s+dinheiro\s+(fácil|rápido|dormindo)\b",
        ],
        "disclaimer_signals": [],
        "message": (
            "Promessa de ganho financeiro. 'Fature R$ X' é oferta que obriga e, sem "
            "comprovação, é enganosa (CDC, arts. 30, 37 e 38); o CONAR veta exagero de "
            "remuneração e ganho irreal em curso (Anexo C, item 1; Anexo B, item 11); "
            "Hotmart (item 3.7) e Meta proíbem ganho fácil ou garantido. Mostre a base "
            "do número e deixe claro que o resultado varia."
        ),
    },
    {
        "name": "Gratuidade em serviço profissional",
        "triggers": [
            r"\b(consultas?|avaliaç(ão|ões)|diagnósticos?|primeira\s+consulta)\s+"
            r"(grátis|gratuitas?|gratuitos?|sem\s+compromisso)\b",
        ],
        "disclaimer_signals": [],
        "message": (
            "Consulta, avaliação ou diagnóstico grátis. Se a peça é de médico, "
            "dentista, psicólogo ou advogado, é vedado (CFM 2.336, art. 11, §4º, c; "
            "Código de Ética Odontológica, art. 20, IX; CFP, art. 20, d; OAB 205, "
            "art. 3º, I)."
        ),
    },
    {
        "name": "Antes e depois (saúde)",
        "triggers": [r"\bantes\s+e\s+depois\b"],
        "disclaimer_signals": [],
        "message": (
            "Antes e depois. Em saúde há regra própria: médico só com finalidade "
            "educativa e os requisitos do art. 14 da CFM 2.336/2023; dentista só "
            "diagnóstico e conclusão, com TCLE (CFO-196/2019, art. 2º); nutricionista "
            "não pode, mesmo com autorização (CFN 599/2018, art. 58)."
        ),
    },
    {
        "name": "Título de melhor profissional",
        "triggers": [
            r"\b(o|a)\s+melhor\s+(médic[oa]|dentista|advogad[oa]|psicólog[oa]|"
            r"nutricionista|cirurgi[ãa]o)\b",
            r"\breferência\s+n(º|°|o|úmero)\s*1\b",
        ],
        "disclaimer_signals": [],
        "message": (
            "'Melhor profissional' ou 'referência nº 1'. Vedado para médico (CFM "
            "2.336, art. 11, XIII e XVI), advogado (OAB 205, art. 3º, IV) e psicólogo "
            "(CFP, art. 20, f); em qualquer anúncio, dado objetivo precisa de "
            "comprovação (CONAR, art. 27, §1º)."
        ),
    },
    {
        "name": "Preço como chamariz (psicologia e advocacia)",
        "triggers": [
            r"\bpreço\s+social\b",
            r"\bvalor\s+acessível\b",
            r"\bpacote\s+promocional\b",
        ],
        "disclaimer_signals": [],
        "message": (
            "'Preço social', 'valor acessível' ou 'pacote promocional'. Vedado para "
            "psicólogo (CFP, art. 20, d, e Nota Técnica 1/2022) e advogado (OAB 205, "
            "art. 3º, I). Dentista também não anuncia preço (Código de Ética "
            "Odontológica, art. 44, I)."
        ),
    },
    {
        "name": "Recomendação de investimento",
        "triggers": [
            r"\bisso\s+não\s+é\s+(uma\s+)?recomendação\b",
            r"\bnão\s+é\s+recomendação\s+de\s+investimento\b",
        ],
        "disclaimer_signals": [],
        "message": (
            "'Isso não é recomendação' não afasta o caráter profissional quando há "
            "habitualidade e remuneração, mesmo indireta (Ofício-Circular CVM/SIN "
            "13/2020). Recomendar ativo exige analista ou consultor registrado (Res. "
            "CVM 20/2021 e 19/2021); sem registro é crime (Lei 6.385, art. 27-E)."
        ),
    },
    {
        "name": "Alegação terapêutica em produto",
        "triggers": [
            r"\b(cura|elimina|acaba\s+com|trata)\s+(a\s+|o\s+|as\s+|os\s+)?"
            r"(acne|melasma|celulite|estrias|queda\s+de\s+cabelo|calvície|diabetes|"
            r"pressão\s+alta|hipertensão|ansiedade|insônia|gastrite|enxaqueca)\b",
            r"\bsubstitui\s+(o\s+)?(remédio|medicamento)\b",
        ],
        "disclaimer_signals": [],
        "message": (
            "Alegação terapêutica. Se for cosmético ou suplemento, é proibida e nenhum "
            "aviso a legitima (RDC 907/2024, art. 12; Lei 6.360, art. 59; RDC "
            "243/2018, art. 17). Se for serviço de saúde, confira a regra do conselho."
        ),
    },
]


def marketing_agent(agent_type: str) -> str:
    """Nome curto do agent Marketing OS que originou o evento, ou "".

    Agents de plugin chegam qualificados (`marketing-os:mos-copy`); instalação
    local em .claude/agents usa o nome curto (`mos-copy`). Um agent `mos-*` de
    outro plugin fica fora, para o gate não agir em conteúdo que não é nosso.
    """
    if not agent_type:
        return ""
    namespace, _, short = agent_type.rpartition(":")
    if not short.startswith("mos-"):
        return ""
    if namespace and namespace.split(":")[0] != PLUGIN_NAME:
        return ""
    return short


def _plugin_checkout_root(path: str) -> str:
    """Raiz da cópia do Marketing OS que contém `path` (instalada ou checkout), ou ""."""
    env_root = (
        (os.environ.get("CLAUDE_PLUGIN_ROOT") or "").replace("\\", "/").rstrip("/")
    )
    if env_root and (path == env_root or path.startswith(env_root + "/")):
        return env_root
    parts = path.split("/")
    for i in range(len(parts) - 1, 0, -1):
        candidate = "/".join(parts[:i])
        # "" é a raiz de um caminho Unix absoluto e "C:" a de um Windows; ali
        # os.path.join cairia no diretório corrente do processo.
        if not candidate or candidate.endswith(":"):
            break
        manifest = os.path.join(candidate, ".claude-plugin", "plugin.json")
        if os.path.isfile(manifest):
            try:
                with open(manifest, encoding="utf-8") as fh:
                    if json.load(fh).get("name") == PLUGIN_NAME:
                        return candidate
            except Exception:
                return ""
            return ""
    return ""


def should_skip(file_path: str) -> bool:
    """True quando o arquivo não é peça de marketing a validar."""
    if not file_path:
        return True
    path = file_path.replace("\\", "/")
    name = path.rsplit("/", 1)[-1]
    if name in SKIP_BASENAMES:
        return True
    if os.path.splitext(name)[1].lower() in SKIP_SUFFIXES:
        return True
    if CLAUDE_STATE_SEGMENT.search(path):
        return True
    # Arquivos do próprio plugin (KBs didáticas, commands, docs) só entram
    # quando ficam na área do usuário, workspace/.
    root = _plugin_checkout_root(path)
    if root:
        relative = path[len(root) + 1 :]
        return not relative.startswith("workspace/")
    return False


def extract_content(tool_name: str, tool_input: dict) -> str:
    if tool_name == "Write":
        return tool_input.get("content", "") or ""
    if tool_name == "Edit":
        return tool_input.get("new_string", "") or ""
    if tool_name == "MultiEdit":
        edits = tool_input.get("edits") or []
        return " ".join(
            (e.get("new_string") or "") for e in edits if isinstance(e, dict)
        )
    return ""


def find_hard_violations(content: str) -> list:
    violations = []
    for pat, msg in HARD_BLOCK_PATTERNS:
        # IGNORECASE em tudo: neutro pro travessão, necessário pro 'brutal' e
        # pro backreference \1 casar 'faça'/'Faça' nas antíteses.
        if re.search(pat, content, flags=re.IGNORECASE):
            violations.append(msg)
    return violations


def find_warnings(content: str) -> list:
    warnings = []
    for pat, msg in WARN_PATTERNS:
        if re.search(pat, content, flags=re.IGNORECASE):
            warnings.append(msg)
    caps_source = REGULATORY_CAPS.sub(" ", content)
    caps = sorted(
        {w for w in CAPS_PATTERN.findall(caps_source) if w not in CAPS_ALLOWLIST}
    )
    if caps:
        warnings.append(
            "Palavras em CAPS detectadas ("
            + ", ".join(caps[:3])
            + "). Reescreva em minúscula; siglas são ok."
        )
    emojis = len(EMOJI_PATTERN.findall(content))
    if emojis > MAX_EMOJIS:
        warnings.append(
            f"{emojis} emojis detectados. A regra global pede de 0 a {MAX_EMOJIS} por peça."
        )
    return warnings


def compliance_findings(content: str) -> list:
    """Regras de compliance disparadas, com o trecho que disparou cada uma.

    Fonte única para o aviso do hook e para scripts/compliance_check.py.
    """
    findings = []
    for rule in COMPLIANCE_RULES:
        match = None
        for trigger in rule["triggers"]:
            match = re.search(trigger, content, flags=re.IGNORECASE)
            if match:
                break
        if not match:
            continue
        if any(
            re.search(d, content, flags=re.IGNORECASE)
            for d in rule["disclaimer_signals"]
        ):
            continue
        findings.append(
            {
                "regra": rule["name"],
                "trecho": match.group(0),
                "mensagem": rule["message"],
            }
        )
    return findings


def find_compliance_warnings(content: str) -> list:
    return [f"[{f['regra']}] {f['mensagem']}" for f in compliance_findings(content)]


def evaluate_event(data: dict) -> GateResult:
    """Valida um evento Claude Code sem executar I/O de saída.

    Esta é a interface comum dos adapters PreToolUse e SubagentStop. Um stop já
    reativado recebe no máximo uma tentativa de correção para evitar loop.
    """
    event_name = data.get("hook_event_name", "") or ""
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {}) or {}
    agent = marketing_agent(data.get("agent_type", "") or "")

    if event_name in ("Stop", "SubagentStop"):
        if not agent:
            return GateResult(
                context="resposta final", skip_reason="agent fora do escopo"
            )
        content = data.get("last_assistant_message", "") or ""
        context = f"resposta final de {agent}"
        retry_exhausted = bool(data.get("stop_hook_active"))
    elif tool_name in ("Write", "Edit", "MultiEdit"):
        file_path = tool_input.get("file_path", "") or ""
        if not agent:
            return GateResult(
                context=file_path or "arquivo",
                skip_reason="escrita fora de agent Marketing OS",
            )
        if should_skip(file_path):
            return GateResult(
                context=file_path or "arquivo", skip_reason="caminho ignorado"
            )
        content = extract_content(tool_name, tool_input)
        context = file_path or "arquivo"
        retry_exhausted = False
    else:
        return GateResult(skip_reason="evento fora do escopo")

    if not content:
        return GateResult(context=context, skip_reason="conteúdo vazio")

    hard = find_hard_violations(content)
    warns = find_warnings(content)
    compliance = find_compliance_warnings(content)

    return GateResult(
        blocked=bool(hard) and not retry_exhausted,
        hard=hard,
        warnings=warns,
        compliance=compliance,
        context=context,
        retry_exhausted=bool(hard) and retry_exhausted,
    )


def decision_of(result: GateResult) -> str:
    if result.skip_reason:
        return "skip"
    if result.blocked:
        return "block"
    if result.retry_exhausted:
        return "allow_retry_exhausted"
    return "allow"


def render(event_name: str, result: GateResult) -> tuple[int, str, str]:
    """Traduz o resultado em (exit_code, stdout, stderr) do protocolo de hooks.

    Bloqueio: exit 2 e motivo em stderr, que o modelo recebe. Avisos: exit 0 e
    JSON com additionalContext, o único canal de exit 0 que o modelo vê.
    """
    advice = [f"WARN: {w}" for w in result.warnings] + [
        f"COMPLIANCE: {c}" for c in result.compliance
    ]
    if result.blocked:
        lines = [f"Quality Gate (Marketing OS) bloqueou {result.context}:"]
        lines += [f"  BLOCK: {v}" for v in result.hard]
        lines += [f"  {a}" for a in advice]
        lines.append("Reescreva eliminando as violações e tente novamente.")
        return 2, "", "\n".join(lines) + "\n"

    notes = []
    system_message = ""
    if result.retry_exhausted:
        notes.append(
            f"A tentativa de correção da {result.context} ainda contém violação. "
            "Antes de entregar ao usuário, corrija: " + " ".join(result.hard)
        )
        system_message = (
            f"Quality Gate (Marketing OS): a {result.context} ainda contém violação "
            "após 1 tentativa de correção; liberada para evitar loop."
        )
    if advice:
        notes.append(
            f"Quality Gate (Marketing OS) avisos em {result.context}:\n"
            + "\n".join(advice)
        )
    if not notes:
        return 0, "", ""
    payload = {
        "hookSpecificOutput": {
            "hookEventName": event_name,
            "additionalContext": "\n\n".join(notes),
        }
    }
    if system_message:
        payload["systemMessage"] = system_message
    return 0, json.dumps(payload, ensure_ascii=False), ""


def log_event(data: dict, result: GateResult) -> None:
    """Registro opcional de cada evento avaliado, para smoke tests e diagnóstico.

    Ativado só quando MOS_HOOK_LOG aponta para um arquivo. Nunca levanta erro:
    diagnóstico não pode derrubar o gate.
    """
    log_path = os.environ.get("MOS_HOOK_LOG")
    if not log_path:
        return
    try:
        tool_input = data.get("tool_input") or {}
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "event": data.get("hook_event_name", ""),
            "agent_type": data.get("agent_type", ""),
            "tool": data.get("tool_name", ""),
            "file": (
                tool_input.get("file_path", "") if isinstance(tool_input, dict) else ""
            ),
            "decision": decision_of(result),
            "reason": result.skip_reason,
            "hard": result.hard,
            "warnings": len(result.warnings) + len(result.compliance),
        }
        with open(log_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if not isinstance(data, dict):
        return 0

    result = evaluate_event(data)
    log_event(data, result)
    code, out, err = render(data.get("hook_event_name", "") or "", result)
    if out:
        print(out)
    if err:
        sys.stderr.write(err)
    return code


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
