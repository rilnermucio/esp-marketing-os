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
        r"\bnão é [^.!?,;:\n]{2,60}[.!?,;:]\s+é\b",
        "Antítese negação/afirmação detectada ('Não é X / É Y'). "
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
        r"\bnão (se trata de|é (uma )?questão de)\b[^.!?\n]{2,80}\b(mas|e sim)\b",
        "Antítese suave detectada ('não se trata de X, mas de Y'). "
        "Variante do AI-tell de negação/afirmação. Considere afirmar direto.",
    ),
]

# Palavras em CAPS (regra global): sequência de 5+ letras maiúsculas que não
# seja sigla conhecida. Só aviso: títulos e siglas novas têm uso legítimo.
CAPS_PATTERN = re.compile(r"(?<![\w])[A-ZÁÉÍÓÚÂÊÔÃÕÇ]{5,}(?![\w])")
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
            "'Depoimento real. Resultados individuais podem variar.'"
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
    caps = sorted({w for w in CAPS_PATTERN.findall(content) if w not in CAPS_ALLOWLIST})
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


def find_compliance_warnings(content: str) -> list:
    warnings = []
    content_lower = content.lower()
    for rule in COMPLIANCE_RULES:
        triggered = any(re.search(t, content_lower) for t in rule["triggers"])
        if not triggered:
            continue
        has_disclaimer = any(
            re.search(d, content_lower) for d in rule["disclaimer_signals"]
        )
        if has_disclaimer:
            continue
        warnings.append(f"[{rule['name']}] {rule['message']}")
    return warnings


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
