# Subagents Migration: Two-Tier Native Pattern

## Contexto

Marketing OS v5.x usava 18 "subagents" que eram na prática **arquivos markdown lidos como contexto pelo main Claude**. Não havia isolamento de contexto, paralelismo, nem tool access controlado.

v6.0 migra para **native subagents do Claude Code** (`.claude/agents/`), ganhando:
- Contexto isolado por agent (evita poluição do main)
- Tool access controlado por agent (menos superfície de risco)
- Paralelismo real (múltiplas Agent calls simultâneas)
- Model selection por agent (Opus vs Sonnet vs Haiku)
- Reconhecimento automático pelo harness do Claude Code

## Arquitetura Two-Tier

```
agents/mos-*.md          TIER 1: dispatch + protocol (~250 linhas cada)
subagents/*-agent.md              TIER 2: knowledge base profundo (~3500 linhas cada)
skills/marketing-os/SKILL.md      ORQUESTRADOR: dispatch map
marketing-os/commands/*.md        COMMANDS: entry points que acionam agents
```

### Tier 1 (enxuto, carregado sempre)

Cada `agents/mos-X.md` contém:

```yaml
---
name: mos-X
description: [quando usar + triggers]
tools: [lista filtrada]
model: sonnet | opus | haiku
color: [semântica visual]
---

# Protocol
1. Read subagents/X-agent.md (tier 2) sob demanda
2. Aplicar output schema
3. Rodar quality gates
4. Retornar
```

### Tier 2 (knowledge base, lido sob demanda)

Os arquivos atuais em `subagents/*-agent.md` permanecem intactos. São a base de conhecimento profunda que o tier-1 consulta via `Read` quando precisa de um framework/case/tabela específica.

**Vantagem**: zero rework do conhecimento existente. O tier-1 referencia paths como:

```markdown
Para profundidade, consulte `subagents/copy-agent.md` PARTE II (master frameworks).
```

## Mapa de Agents (18)

| Agent nativo | Knowledge tier-2 | Model | Tools principais |
|----|----|----|----|
| mos-copy | subagents/copy-agent.md | sonnet | Read, Write, Edit, Grep, Glob, WebSearch |
| mos-seo | subagents/seo-agent.md | sonnet | + Bash (scripts SEO) |
| mos-research | subagents/research-agent.md | sonnet | + Bash (scripts trend/competitor) |
| mos-social | subagents/social-agent.md | sonnet | Read, Write, Edit, WebSearch |
| mos-video | subagents/video-agent.md | sonnet | Read, Write, Edit, WebSearch, Bash |
| mos-audio | subagents/audio-agent.md | sonnet | Read, Write, Edit |
| mos-ai-tools | subagents/ai-tools-agent.md | sonnet | Read, Write, WebSearch |
| mos-design | subagents/design-agent.md | sonnet | Read, Write, WebSearch |
| mos-analytics | subagents/analytics-agent.md | sonnet | Read, Write, Bash, WebSearch |
| mos-email | subagents/email-agent.md | sonnet | Read, Write, Edit, WebSearch |
| mos-ads | subagents/ads-agent.md | sonnet | Read, Write, Edit, WebSearch, Bash |
| mos-brand | subagents/brand-agent.md | sonnet | Read, Write, Edit, WebSearch |
| mos-storytelling | subagents/storytelling-agent.md | sonnet | Read, Write, Edit |
| mos-funnel | subagents/funnel-agent.md | sonnet | Read, Write, Edit, WebSearch |
| mos-growth | subagents/growth-agent.md | sonnet | Read, Write, Edit, WebSearch, Bash |
| mos-launch | subagents/launch-agent.md | sonnet | Read, Write, Edit, WebSearch |
| mos-infoproduct | subagents/infoproduct-builder-agent.md | sonnet | Read, Write, Edit, WebSearch |
| mos-ab-testing | subagents/ab-testing-agent.md | sonnet | Read, Write, Edit, Bash |

## Padrões de Orquestração

### Dispatch Simples (1 agent)

```
Agent(subagent_type: "mos-copy", prompt: "3 headlines para curso Python")
```

### Dispatch Paralelo (múltiplos agents em um único message)

Quando os agents operam sobre problemas **independentes**:

```
Single message com:
- Agent(subagent_type: "mos-research", prompt: "...")
- Agent(subagent_type: "mos-brand", prompt: "...")
- Agent(subagent_type: "mos-copy", prompt: "...")
```

Ganho: 3x mais rápido que sequencial.

### Dispatch Sequencial (quando há dependência)

```
Passo 1: Agent(mos-research) → research brief
Passo 2: Agent(mos-copy, prompt: "... usando: [brief]") → copy
Passo 3: Agent(mos-design, prompt: "... usando: [copy]") → design
```

## Quality Gates (dois níveis)

1. **Por agent**: cada tier-1 tem seus próprios gates (ver seção Quality Gates do agent)
2. **Global**: SKILL.md aplica gates ao consolidar (última linha de defesa antes de entregar ao usuário)

Regras comuns (ambos níveis):
- Sem `—`
- Sem "brutal"
- Sem CAPS
- Máximo 2 emojis
- Acentuação PT-BR correta
- Fact-check (WebSearch antes) para pessoas/stats/eventos
- Enquete em conteúdo social

## Como Adicionar Novo Agent

1. Criar `agents/mos-X.md` seguindo padrão de um existente (ex: copiar `mos-copy.md` e adaptar).
2. Preencher YAML frontmatter (name, description, tools, model).
3. Apontar para knowledge base via `Read` em `subagents/X.md` (ou criar um novo knowledge).
4. Rodar `python scripts/validate_agents.py`.
5. Atualizar `SKILL.md` (mapa de dispatch) e este doc.
6. (Opcional) Criar um command em `marketing-os/commands/` como entry point.

## Backup e Rollback

- `skills/marketing-os/SKILL.md.pre-migration.backup`: skill v5.x preservado.
- Rollback: restaurar backup + remover `agents/mos-*.md`.
- Os arquivos tier-2 em `subagents/*-agent.md` são **intactos** na migração (zero duplicação).

## Validação

```bash
python scripts/validate_agents.py
# Output esperado: 18 agents, clean, zero errors, zero warnings
```

## Próximos Passos Pós-Migração

- Wirar engine de orquestração aos agents (state machine + durabilidade) — implementação em `scripts/` ou hooks do Claude Code
- Logging estruturado por dispatch (JSONL com agent, input, output, gates)
- Feedback loop: capturar performance das peças publicadas e retroalimentar
- Paralelismo em mais workflows (atualmente só content-pipeline)

Ver auditoria completa em conversa original de migração (abril 2026).
