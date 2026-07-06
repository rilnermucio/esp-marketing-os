---
description: Auditoria PREMIUM agency-grade de landing page com radar chart, screenshots, prosa por dimensão, comparativo competitivo, roadmap 30/90/180 dias e PDF de 25-30 páginas pronto pra entregar pra cliente.
argument-hint: <url>
allowed-tools: Bash, WebFetch, Read, Write, Agent
---

# /auditoria-pro

Você é o orquestrador de auditoria premium agency-grade do marketing-os. Recebe URL de landing page e produz RELATORIO.md + RELATORIO.pdf de 25-30 páginas em `workspace/auditorias/<run>-pro/`.

## Passo 1: Validar input

Se `$ARGUMENTS` está vazio, retorne usage:

```
Uso: /auditoria-pro <url-de-landing-page>

Este command suporta APENAS landing pages. Para Instagram, Meta Ads ou YouTube, use /auditoria standard.

Exemplo:
  /auditoria-pro https://stripe.com
```

Rode `python ${CLAUDE_PLUGIN_ROOT}/scripts/audit_detector.py "$ARGUMENTS"`. Se type != "landing", aborte com mensagem clara. Senão, capture `type`, `normalized`, `slug`.

## Passo 2: Criar diretório do run

```bash
TIMESTAMP=$(date +%Y-%m-%d-%H%M%S)
RUN_DIR="workspace/auditorias/${TIMESTAMP}-landing-${SLUG}-pro"
mkdir -p "${RUN_DIR}"/{screenshots,charts,anexos}
```

## Passo 3: Dispatch paralelo (single message)

Use Bash + 7 Agent calls em UMA SÓ mensagem.

### Bash: Capturar screenshots

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/audit_screenshot.py \
  --url "${NORMALIZED}" \
  --output-dir "${RUN_DIR}/screenshots" \
  --timeout-ms 30000
```

### Agent calls (7 em paralelo)

Cada agent recebe a instrução ADICIONAL premium (vs `/auditoria` v1):

> "Devolve output denso (1500-2000 palavras), incluindo tabelas comparativas quando aplicável, diagramas ASCII quando útil, citações textuais do que viu no site, e antes/depois de copy quando sugerir mudança específica."

Dispatchs (todos com a instrução adicional acima concatenada ao prompt):

- `Agent(subagent_type: "mos-research", prompt: "Posicionamento competitivo de {normalized}. Identifique top 3 concorrentes diretos, como {normalized} se diferencia (ou não), tabela comparativa de proposta de valor.")`
- `Agent(subagent_type: "mos-seo", prompt: "Audit técnico + on-page completo de {normalized}. Title, meta, headings, schema, performance (CWV), mobile, internal linking, alt text. Dê diagnóstico denso com tabela de issues priorizadas.")`
- `Agent(subagent_type: "mos-copy", prompt: "Audit headline + value proposition + CTAs + copy de prova social em {normalized}. Para cada elemento fraco, mostre antes/depois com versão reescrita.")`
- `Agent(subagent_type: "mos-funnel", prompt: "Mapeie o funil de {normalized}. Identifique friction points, gaps, diagrama ASCII do fluxo, oportunidades de conversão por etapa.")`
- `Agent(subagent_type: "mos-ads", prompt: "Avalie CTA strategy + conversion path em {normalized}. Placement, urgency, prova social, trust signals. Inclua diagnóstico do path completo do visitante até a conversão.")`
- `Agent(subagent_type: "mos-design", prompt: "Hierarquia visual + clareza + acessibilidade WCAG + paleta de cores em {normalized}. Aponte issues de contraste, espaçamento, tipografia.")`
- `Agent(subagent_type: "mos-brand", prompt: "Voice + arquétipo + identidade verbal e visual de {normalized}. Avalie consistência entre headline, copy e visual.")`

## Passo 4: Salvar outputs raw

Para cada agent, escreva output em `${RUN_DIR}/anexos/anexo_<agent>.md`. Esses arquivos preservam a fonte completa que vai pro apêndice do PDF.

## Passo 5: Synthesis expandida

Para cada uma das 7 dimensões, gere:

1. **Score 0-100** baseado nos outputs dos agents relevantes
2. **3-5 evidências observadas** (não 1, bullets curtos com fato concreto)
3. **Prose de 3-5 parágrafos** consolidando os agents (analítica, profissional, sem floreio)
4. **1-3 fixes priorizados** com `priority` ("alta", "media", "baixa") e `text` específico
5. **Antes/Depois de copy** quando agents sugeriram mudança textual (lista de objetos `{before, after}`)
6. **Citação textual de agent** (1-2 frases) com atribuição (`Conforme análise mos-X`)

Quality gates:
- Sem `—` (substituir por `:` ou `.`)
- Sem "brutal" (usar intenso, forte, pesado)
- Sem CAPS em prosa
- PT-BR sempre acentuado
- Citação de números/cases vem de output do agent ou WebSearch (não inventar)

Monte o JSON `scores.json` em `${RUN_DIR}/`:

```json
{
  "type": "landing",
  "dimension_scores": {
    "Conversão (CTA, friction, funil)": 71,
    "...": 0
  },
  "evidences": {
    "Conversão (CTA, friction, funil)": ["evidência 1", "evidência 2"]
  },
  "fixes": {
    "Conversão (CTA, friction, funil)": {"text": "...", "priority": "alta"}
  }
}
```

## Passo 6: Calcular score final

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/audit_scoring.py < "${RUN_DIR}/scores.json" > "${RUN_DIR}/scoring_output.json"
```

## Passo 7: Gerar radar chart

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/audit_radar_chart.py \
  --scores-json "${RUN_DIR}/scoring_output.json" \
  --output "${RUN_DIR}/charts/radar_scorecard.png"
```

## Passo 8: Gerar roadmap

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/audit_roadmap_generator.py < "${RUN_DIR}/scoring_output.json" > "${RUN_DIR}/roadmap.json"
```

## Passo 9: Build report data dict + render HTML

Use a tool Write para construir `${RUN_DIR}/render_input.json` com a estrutura:

```json
{
  "client_url": "<url>",
  "client_name": "<slug ou domain>",
  "audit_type": "landing",
  "timestamp": "<timestamp>",
  "overall_score": 0,
  "partial": false,
  "exec_summary": "<3 frases bem escritas>",
  "dimensions": {
    "<dim_name>": {
      "score": 0,
      "weight": 0,
      "prose": "<3-5 parágrafos>",
      "evidences": ["..."],
      "fixes": [{"text": "...", "priority": "alta"}],
      "before_after": [{"before": "...", "after": "..."}],
      "agent_citation": "..."
    }
  },
  "competitive": {
    "competitors": [{"name": "...", "differentiation": "..."}],
    "table_md": "<markdown table>"
  },
  "roadmap": {},
  "appendix": {
    "research": "<full anexo content>",
    "seo": "<full>"
  },
  "used_terms": ["CWV", "schema markup", "CTA"]
}
```

Depois renderize HTML:

```bash
python -c "
import json
import sys
sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT}/scripts')
from audit_premium_template import render

data = json.load(open('${RUN_DIR}/render_input.json'))
screenshots = {'homepage': '${RUN_DIR}/screenshots/homepage.png', 'internals': [], 'dimensions': {}}
charts = {'radar': '${RUN_DIR}/charts/radar_scorecard.png'}
config_path = '.auditoria-config.json'
config = None
import os
if os.path.exists(config_path):
    config = json.load(open(config_path))

html = render(data, screenshots, charts, config)
open('${RUN_DIR}/RELATORIO.html', 'w').write(html)
print('${RUN_DIR}/RELATORIO.html')
"
```

## Passo 10: Gerar PDF

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/pdf_generator.py --from-html \
  "${RUN_DIR}/RELATORIO.html" \
  "${RUN_DIR}/RELATORIO.pdf" \
  ".auditoria-config.json"
```

Se PDF falhar, imprima erro e mantenha HTML como fallback.

## Output (Passo 11): chat final

Imprima 5 linhas:

```
✓ Auditoria Pro concluída: <client_name>
  Score: <overall>/100 <(parcial se aplicável)>
  Páginas no PDF: ~<estimativa>
  Arquivos: <RUN_DIR>/RELATORIO.{html,pdf}
  Custo: $0.00 (Playwright local, sem Apify nesta auditoria)
```

Acrescente exec summary em 5 frases.

## Telemetria

Antes do output final, escreva `${RUN_DIR}/.audit-meta.json`:

```json
{
  "started_at": "<ISO>",
  "ended_at": "<ISO>",
  "type": "landing-pro",
  "input": "<url>",
  "agents_dispatched": ["mos-..."],
  "agents_failed": [],
  "screenshots_captured": 0,
  "config_applied": false,
  "pdf_pages": 0,
  "errors": []
}
```
