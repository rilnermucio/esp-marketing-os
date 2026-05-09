# Auditoria Pro: PDF agency-grade com radar chart, screenshots e prosa editorial (Design)

**Date:** 2026-05-09
**Status:** Draft (awaiting user review)
**Author:** Claude Opus 4.7 via brainstorming + design proposal, with rilner
**Target version:** marketing-os v6.8.0
**Predecessor:** v6.7.0 (`/auditoria` básico, branch `feat/auditoria-multi-modal`)

---

## Context

O `/auditoria` v6.7.0 entrega RELATORIO.md/.pdf funcionais mas rasos: 6.5KB de markdown, 7 dimensões com 1 evidência + 1 fix por dimensão, anexo vazio, sem visualizações, sem screenshots, sem comparativo competitivo visual. O user (rilner) testou os outputs com Stripe + @ericorocha e classificou como "tão básicos" para o caso de uso real (entregável de agência/freelancer pra cliente final brasileiro).

A análise de gap identificou conteúdo descartado durante synthesis: `mos-research` entregou tabela competitiva de 5 dimensões (Stripe vs Adyen/PayPal/Square), `mos-funnel` entregou diagrama ASCII de path de conversão, `mos-brand` mapeou arquétipos (Mago + Herói pra Erico), `mos-copy` sugeriu CTAs específicos por segmento. Tudo virou 1-2 linhas no relatório final.

Esta spec define `/auditoria-pro`: comando paralelo (não substitui o v6.7.0) que produz relatório agency-grade com 25-30 páginas, prosa editorial, radar chart, screenshots automáticos, comparativo competitivo visual, roadmap 30/90/180 dias e apêndice técnico expandido.

### Constraints declarados (turnos anteriores)

| Constraint | Decisão |
|---|---|
| Scope inicial | Apenas `landing` (Approach A das 3 propostas). IG/Meta Ads/YouTube ficam pra v6.8.1+ |
| Visual identity | Eu defino. Paleta `#0a2540` deep ink blue + `#ff6b35` warm orange. System-ui typography |
| Caso piloto | stripe.com (reusa outputs já coletados na v6.7.0 quando possível) |
| Estrutura | 10 seções, ~25-30 páginas |
| Comando | Novo `/auditoria-pro` (não modifica `/auditoria`) |
| Esforço alvo | 24-36 horas focadas, ~3-5 dias corridos |

### Não-objetivos (out of scope)

- Refatorar `/auditoria` v1 (continua intocado, ambos coexistem)
- Outros 3 tipos (instagram, meta_ads, youtube) na v6.8.0
- Internacionalização (PT-BR only, igual v6.7.0)
- Histórico/comparativo entre auditorias (V1.1+ herdado da spec anterior)
- Notion MCP integration (V1.1+ herdado)
- Visualizações interativas (HTML report). Output continua MD + PDF estático
- Screenshots de mobile viewport (apenas desktop na v6.8.0)
- Tradução automática do conteúdo (mantém o output dos agents como vier, em PT-BR)

---

## Architecture

Mantém o padrão two-tier do plugin. Quatro camadas:

### Layer 1: Command orchestrator
Arquivo: `commands/auditoria-pro.md`. ~300 linhas (vs ~150 do v1). Inclui:
- Parsing de input (igual v1)
- Dispatch de Playwright screenshots em paralelo aos 7 agents
- Synthesis prompt expandido (~150 linhas de instruções vs ~50 do v1) que pede prosa de 3-5 parágrafos por dimensão, antes/depois, citações, cross-reference de outputs entre agents
- Roadmap auto-gerado a partir dos fixes
- Invocação do template premium HTML
- Geração de radar chart
- Output final no chat com 5 linhas (vs 3 do v1)

### Layer 2: Scripts determinísticos novos
Cinco scripts em `scripts/`:
- `audit_screenshot.py`: Playwright captura homepage + 2-3 páginas internas + opcional bounding boxes em seções comentadas. Salva PNGs em `screenshots/` no run dir
- `audit_radar_chart.py`: matplotlib radar chart 7 dimensões com paleta deep blue + warm orange. Output PNG embeddable
- `audit_premium_template.py`: HTML template + CSS premium pra weasyprint. Cobre capa, sumário, scorecard visual, per-dim sections, competitivo, roadmap, apêndice, glossário
- `audit_roadmap_generator.py`: A partir do JSON de fixes, gera markdown de roadmap 30/90/180 dias com esforço estimado (S/M/L) e impacto (alto/médio/baixo)
- `audit_glossary.py`: Glossário curado dos termos técnicos usados nos relatórios (CWV, schema, hreflang, etc.). Estático mas extensível

### Layer 3: Scripts existentes reaproveitados (sem alteração)
- `audit_detector.py` (v1)
- `audit_scoring.py` (v1)
- `audit_config.py` (v1) — mantém white-label opcional
- `pdf_generator.py` (v1) — generic markdown→PDF, mas vai chamar template premium quando flag `--premium` ou config indica

### Layer 4: Output
Diretório `workspace/auditorias/<YYYY-MM-DD-HHMMSS>-<tipo>-<slug>-pro/`:
```
RELATORIO.md            # markdown completo (60-80KB esperados)
RELATORIO.pdf           # PDF premium (~1-2MB com screenshots embedados)
scores.json             # synthesis scores
scoring_output.json     # output do scoring CLI
roadmap.json            # estrutura roadmap pré-PDF
screenshots/
  homepage.png
  pricing.png
  signup.png
  competitor_1_homepage.png
  competitor_2_homepage.png
  competitor_3_homepage.png
charts/
  radar_scorecard.png
anexos/
  anexo_research.md     # output raw mos-research
  anexo_seo.md
  anexo_copy.md
  anexo_funnel.md
  anexo_ads.md
  anexo_design.md
  anexo_brand.md
.audit-meta.json
```

### Decisões arquiteturais não-óbvias

**Por que command separado, não flag `--premium` no `/auditoria`.** Modificar `/auditoria` v1 introduz risco de regressão num command já validado em produção (Test 1-4 da v6.7.0). Manter separado permite: (a) iterar `/auditoria-pro` sem afetar v1, (b) deprecar `/auditoria` no futuro mantendo backward compat, (c) testes isolados, (d) comparação direta entre output de v1 e v2 no mesmo input.

**Por que synthesis no command (mantém da v1).** O motivo do v1 continua válido: modificar 18 system prompts para emitir JSON estruturado em modo "auditoria-pro" é mudança massiva. Synthesis no command preserva agents intactos. Custo: ~150 linhas extras no command pra explicar o nível de detalhe e formato esperado.

**Por que Playwright para screenshots, não Apify.** Playwright já é dependência indireta (workspace/competitor-analysis/marketingskills usa pra evals). É open-source, gratuito, sem custo por execução. Apify tem screenshot Actor mas custa. Pra screenshots de domínio público (homepage), Playwright é suficiente.

**Por que matplotlib para radar chart, não SVG manual.** Matplotlib é robusto, output reproduzível, customização programática. SVG manual seria 200+ linhas de código frágil. Custo: dependência adicional (`matplotlib>=3.7`). Já é Python ecosystem padrão.

**Por que HTML/CSS premium template, não modificar `pdf_generator.py`.** O `pdf_generator.py` v1 é genérico e reutilizável. Adicionar lógica premium nele violaria single responsibility. Melhor: novo módulo `audit_premium_template.py` que gera o HTML/CSS específico, e `pdf_generator.py` continua como engine genérico que aceita HTML pronto.

---

## Components

### 4.1 `scripts/audit_screenshot.py`

**Assinatura:**
```python
def capture(url: str, output_dir: Path, viewport: tuple[int, int] = (1440, 900)) -> dict:
    """Captura screenshots de uma URL. Returns {homepage: Path, internals: list[Path], errors: list}."""
```

**Behavior:**
- Inicia Playwright Chromium headless
- Navega para `url`, aguarda `networkidle`, captura full-page screenshot → `<output_dir>/homepage.png`
- Detecta links principais no DOM (pricing, signup, contact, features) via heurística simples (`<a>` com texto ou href contendo essas keywords)
- Captura até 2-3 páginas internas (pricing, signup, contact) → PNGs
- Retorna dict com paths absolutos
- Timeout 30s por página, fallback graceful se falhar (loga erro, continua)

**CLI mode:** `python audit_screenshot.py --url <url> --output-dir <dir> [--viewport WxH]`. JSON pra stdout.

**Bounding box overlay (V1.1+, deferred):** Adicionar caixas vermelhas nas seções comentadas (hero, CTA, footer). Requer XPath/selector dos targets, complexo. Pra v6.8.0 entrega screenshots sem overlay — anotação textual no relatório referencia "ver homepage.png seção hero".

### 4.2 `scripts/audit_radar_chart.py`

**Assinatura:**
```python
def generate(scores: dict[str, int], rubric_weights: dict[str, int], output_path: Path,
             primary_color: str = "#0a2540", accent_color: str = "#ff6b35") -> Path:
    """Generate radar chart PNG. Returns output_path."""
```

**Behavior:**
- 7 axes (uma por dimensão da rubric landing)
- Scale 0-100, gridlines a cada 20 pontos
- Polígono preenchido com accent color (alpha 0.3) + linha sólida primary color
- Labels com nomes das dimensões (truncados a 18 chars se longos)
- Centro com score geral em fonte grande
- Output PNG 800x800px, transparent background, dpi 200

**CLI mode:** `python audit_radar_chart.py --scores-json <path> --output <path>`.

### 4.3 `scripts/audit_premium_template.py`

**Função principal:**
```python
def render(report_data: dict, screenshots: dict, charts: dict, config: dict | None) -> str:
    """Render full HTML for premium PDF. Returns HTML string ready for weasyprint."""
```

**Estrutura HTML:**
- `<head>`: `<style>` embedded com CSS premium (~300-400 linhas)
- `<body>`: Sections em ordem com `class="page"` e `page-break-before: always` no CSS
  - `cover` — capa
  - `executive-summary`
  - `methodology`
  - `visual-scorecard` (radar + tabela)
  - `dimension-N` (7 sections, uma por dim)
  - `competitive`
  - `roadmap`
  - `appendix`
  - `glossary`
  - `next-steps`

**CSS premium (linha geral):**
```css
:root {
  --primary: #0a2540;
  --accent: #ff6b35;
  --text: #1a1a1a;
  --muted: #6b7280;
  --bg-soft: #f9fafb;
  --border: #e5e7eb;
}
@page { size: A4; margin: 2.5cm 2cm; }
@page :first { margin: 0; } /* capa full bleed */
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; }
.page { page-break-before: always; }
.cover { /* full bleed, gradient bg, marca centralizada */ }
h1 { font-size: 32pt; color: var(--primary); ... }
h2 { font-size: 22pt; color: var(--accent); border-bottom: 2px solid var(--accent); padding-bottom: 8px; }
h3 { font-size: 16pt; color: var(--primary); }
.score-big { font-size: 96pt; color: var(--primary); font-weight: 700; }
.scorecard-table { ... }
.dimension-card { ... }
.before-after { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.competitor-grid { display: grid; grid-template-columns: repeat(2, 1fr); }
.roadmap-table th { background: var(--primary); color: white; }
blockquote.agent-citation { border-left: 4px solid var(--accent); padding-left: 16px; color: var(--muted); font-style: italic; }
.priority-alta { background: #fee2e2; color: #991b1b; padding: 2px 8px; border-radius: 4px; font-size: 9pt; font-weight: 600; }
.priority-media { background: #fef3c7; color: #92400e; ... }
.priority-baixa { background: #dbeafe; color: #1e40af; ... }
img.screenshot { max-width: 100%; border: 1px solid var(--border); border-radius: 4px; }
img.radar-chart { max-width: 600px; display: block; margin: 0 auto; }
```

### 4.4 `scripts/audit_roadmap_generator.py`

**Assinatura:**
```python
def generate(fixes: list[dict], rubric_weights: dict[str, int]) -> dict:
    """
    fixes: lista de fixes do scoring com dimension, score, fix.text, fix.priority
    Returns: {30_days: [...], 90_days: [...], 180_days: [...]}
    Cada item: {action, dimension, effort: S|M|L, impact: alto|medio|baixo, owner: string}
    """
```

**Heurística:**
- Priority alta + score baixo + dimensão high-weight (≥20%) → 30 dias
- Priority alta + score médio + dimensão medium-weight (10-15%) → 90 dias
- Priority média OU baixa → 180 dias
- Effort estimado por keywords no fix text (palavras como "reescrever", "criar", "redesign" → M ou L)
- Owner sugerido por dimensão (Conversão → Growth lead, Copy → Copywriter, SEO → SEO specialist, etc.)

**CLI mode:** Lê JSON de stdin, escreve JSON em stdout.

### 4.5 `scripts/audit_glossary.py`

**Conteúdo:** Dict estático com 30-40 termos técnicos usados nos relatórios. Cada entrada:
```python
GLOSSARY = {
    "CWV": "Core Web Vitals — métricas do Google que medem performance percebida (LCP, INP, CLS).",
    "schema markup": "Marcação estruturada (JSON-LD) que ajuda buscadores a entender conteúdo.",
    "hreflang": "Atributo HTML que sinaliza variantes de idioma de uma página pra Google.",
    "value proposition": "Promessa central que comunica por que escolher um produto vs alternativas.",
    ...
}
```

**Função:**
```python
def render_glossary_md(used_terms: set[str] | None = None) -> str:
    """Renders glossary section. If used_terms is given, includes only those (filtered)."""
```

### 4.6 `commands/auditoria-pro.md`

**Frontmatter:**
```yaml
---
description: Auditoria PREMIUM agency-grade de landing page. Despacha 7 agents + Playwright screenshots, gera radar chart, roadmap 30/90/180 dias, comparativo competitivo visual e PDF de 25-30 páginas pronto pra entregar pra cliente.
argument-hint: <url>
allowed-tools: Bash, WebFetch, Read, Write, Agent
---
```

**System prompt structure (~300 linhas):**

1. Validar input + detectar tipo (rejeitar se não landing — v6.8.0 escopo)
2. Criar diretório do run com sufixo `-pro`
3. **Em paralelo (single message):**
   - 7 Agent calls (mos-research, mos-seo, mos-copy, mos-funnel, mos-ads, mos-design, mos-brand). Prompts iguais ao v1 mas com instrução adicional: "Devolve output denso (1500-2000 palavras), incluindo: tabelas comparativas quando aplicável, diagramas ASCII quando útil, citações textuais do que viu no site, antes/depois de copy quando sugerir mudança"
   - Bash: `python audit_screenshot.py --url <url> --output-dir <run_dir>/screenshots`
4. Aguardar todos os outputs
5. Salvar cada output raw em `anexos/anexo_<agent>.md`
6. **Synthesis expandida (~150 linhas no command):**
   - Pra cada dimensão da rubric: prosa de 3-5 parágrafos consolidando os agents relevantes, sub-scores quando aplicável, antes/depois de copy quando agents sugeriram
   - Score final 0-100 + 3-5 evidências (não 1) + 1-3 fixes por dimensão
7. Bash: `python audit_scoring.py < scores.json` (mesma do v1)
8. Bash: `python audit_radar_chart.py --scores-json scoring_output.json --output charts/radar_scorecard.png`
9. Bash: `python audit_roadmap_generator.py < scores.json > roadmap.json`
10. Synthesis competitive section: usa output do mos-research pra montar tabela comparativa
11. Synthesis screenshots de competitors: tenta WebFetch dos sites competitor (até 3) ou indica seção visual omitida
12. Build RELATORIO.md com novo template (estrutura de 10 seções)
13. Bash: `python -c "from audit_premium_template import render; ... render(...)" > /tmp/render.html`
14. Bash: `python pdf_generator.py /tmp/render.html ${RUN_DIR}/RELATORIO.pdf [.auditoria-config.json]` (com novo flag `--from-html` ou detectar extensão)
15. Output final no chat: 5 linhas com paths + exec summary 5 frases

**Quality gates aplicados durante synthesis:**
- Sem `—` (travessão longo) → usar `:` ou `.` ou quebrar frase
- Sem palavra "brutal" → trocar por intenso/forte/pesado/impactante
- Sem CAPS em prosa → minúsculas
- Max 0-1 emoji
- PT-BR sempre acentuado
- Citação de fact (números, casos) tem que vir de output do agent ou WebSearch (não inventar)

### 4.7 `pdf_generator.py` extension (modify)

Adicionar flag `--from-html`:
```python
def generate(input_path, output_path, config_path=None, *, from_html: bool = False):
    if from_html or input_path.suffix == ".html":
        html = input_path.read_text()
    else:
        # current markdown → HTML pipeline
        ...
    HTML(string=html, base_url=...).write_pdf(...)
```

CLI: `python pdf_generator.py --from-html input.html output.pdf`

---

## Data flow

```
[1] User: /auditoria-pro <url>
       ↓
[2] Bash: audit_detector.py "<url>" → JSON (type=landing required)
       ↓
[3] Bash: mkdir -p workspace/auditorias/<run>-pro/{screenshots,charts,anexos}
       ↓
[4] Single message com PARALELO:
       - 7 Agent calls (research, seo, copy, funnel, ads, design, brand) com prompts denser (1500-2000 palavras)
       - Bash: audit_screenshot.py captura homepage + páginas internas
       ↓
[5] Coleta outputs + screenshot paths
       ↓
[6] Write: anexos/anexo_<agent>.md pra cada agent (raw output preservado)
       ↓
[7] Synthesis expandida (Claude no command): prosa por dimensão (3-5 parágrafos), 3-5 evidências, 1-3 fixes, antes/depois de copy. Output: scores.json (formato extendido vs v1)
       ↓
[8] Bash: audit_scoring.py < scores.json → scoring_output.json (com top wins/fixes)
       ↓
[9] Bash: audit_radar_chart.py → charts/radar_scorecard.png
       ↓
[10] Bash: audit_roadmap_generator.py < scores.json > roadmap.json
       ↓
[11] Synthesis competitive (Claude): mapeia 3 concorrentes do mos-research output, tenta WebFetch das homepages, build tabela comparativa
       ↓
[12] Build RELATORIO.md com new template (capa via HTML separado, 10 seções)
       ↓
[13] Bash: render via audit_premium_template.py → /tmp/<run>.html
       ↓
[14] Bash: pdf_generator.py --from-html /tmp/<run>.html → RELATORIO.pdf
       ↓
[15] Output: paths + exec summary 5 frases + custo total ($0.046 Apify se IG, $0 se só landing)
```

**Tempo estimado por run:**
- Agents em paralelo: ~3-5 min (7 agents, output denser)
- Playwright screenshots: ~30-60s
- Synthesis Claude: ~2-3 min (output mais longo)
- Scoring + radar + roadmap + template + PDF: ~30s
- **Total: ~6-9 min por auditoria-pro**

vs v1 que rodava em ~3-5 min. Aumento ~2x compatível com 5x output volume.

---

## Error handling

### Hard errors (aborta com mensagem clara)

| Falha | Resposta |
|---|---|
| Input vazio | Usage + exemplos + aborta |
| Type detected != landing | "Este command suporta apenas landing pages na v6.8.0. Para Instagram/Meta Ads/YouTube, use `/auditoria` standard." |
| Playwright não instalado | `pip install playwright && playwright install chromium` |
| matplotlib não instalado | `pip install matplotlib` |
| weasyprint não instalado | (igual v1) |
| `workspace/` não gravável | (igual v1) |

### Soft degradation (continua, sinaliza no relatório)

| Falha | Comportamento |
|---|---|
| Playwright timeout / página não carrega | Continua sem screenshot. Relatório mostra placeholder "Screenshot não disponível: <razão>". Mas dá pra usar bullet points descritivos do mos-design pra suprir |
| Páginas internas não encontradas | Captura só homepage. OK. |
| Competitor sites WebFetch falha | Pula seção "Análise Competitiva Visual", mas mantém tabela de comparativo (do mos-research) |
| Radar chart geração falha | Pula chart, scorecard fica só tabular. Sinaliza no relatório |
| Roadmap generator falha | Roadmap section fica como fallback simples (lista de fixes ordenados, sem timeline 30/90/180) |
| 1 agent falha | Continua com N-1, igual v1. Dimensões dependentes ficam parciais |
| 1 anexo não consegue ser salvo | Continua, sinaliza no `.audit-meta.json` |

---

## Testing

### Unit tests (rápidos)

| Test file | Cobertura | Coverage alvo |
|---|---|---|
| `test_audit_screenshot.py` | URL parsing, timeout handling, page navigation mocked. Real Playwright run em `@pytest.mark.smoke`. | ~70% (real run no smoke) |
| `test_audit_radar_chart.py` | Scores válidos geram PNG não-vazio, paleta aplicada (mock matplotlib if too slow), invalid scores raise | 100% |
| `test_audit_premium_template.py` | Render produz HTML válido, todas as 10 seções presentes, CSS variables aplicadas, screenshots embedded como `<img>` | 90% |
| `test_audit_roadmap_generator.py` | 30/90/180 buckets corretos por priority+score, effort estimation por keywords, owner mapping | 100% |
| `test_audit_glossary.py` | Render glossary, filtragem por used_terms, formato markdown válido | 100% |

### Integration test
| Test file | Cobertura |
|---|---|
| `test_auditoria_pro_smoke.py` (`@pytest.mark.smoke`) | Pipeline completo com mocked agent outputs + mocked Playwright. Detector → fake outputs → synthesis fake → scoring → radar → roadmap → template → PDF. Valida artefatos finais. |

### Tests existentes (cobertura automática)
- `test_commands_dispatch.py`: pega `/auditoria-pro` automaticamente
- `test_workspace_separation.py`: outputs em `workspace/auditorias/<run>-pro/`. Adicionar ao allowlist.
- `test_plugin_manifest.py`: count de commands aumenta pra 34
- `test_integration_mcp.py::TestCoberturaDeSscripts`: adicionar 5 novos scripts ao SCRIPTS_EXCLUIDOS

### Manual validation

3 cenários antes de release v6.8.0:
1. `/auditoria-pro https://stripe.com` (caso piloto). PDF deve sair com 25-30 páginas, todos os componentes presentes (capa, sumário, scorecard com radar, 7 dim sections com prosa real, comparativo, roadmap, anexos)
2. `/auditoria-pro https://example.com` (site simples). Validar graceful degradation se Playwright não consegue navegar páginas internas
3. `/auditoria-pro https://stripe.com` com `.auditoria-config.json` (white-label premium). Brand do user deve aparecer na capa, accent custom em todos os headings/charts/tabelas

Pass criteria: PDF gerado sem stack trace, 20+ páginas, contém radar chart, ≥5 screenshots, prosa real (não bullets), tabela competitiva, roadmap com timelines.

---

## File manifest

### Novos arquivos
- `commands/auditoria-pro.md` (~300 linhas)
- `scripts/audit_screenshot.py` (~250 linhas)
- `scripts/audit_radar_chart.py` (~150 linhas)
- `scripts/audit_premium_template.py` (~600 linhas inclui CSS)
- `scripts/audit_roadmap_generator.py` (~200 linhas)
- `scripts/audit_glossary.py` (~250 linhas, mostly dict)
- `scripts/tests/test_audit_screenshot.py` (~120 linhas)
- `scripts/tests/test_audit_radar_chart.py` (~100 linhas)
- `scripts/tests/test_audit_premium_template.py` (~150 linhas)
- `scripts/tests/test_audit_roadmap_generator.py` (~150 linhas)
- `scripts/tests/test_audit_glossary.py` (~80 linhas)
- `scripts/tests/test_auditoria_pro_smoke.py` (~200 linhas, marked `@pytest.mark.smoke`)
- `docs/AUDITORIA-PRO.md` (user-facing, ~150 linhas)

### Arquivos modificados
- `scripts/pdf_generator.py`: adicionar flag `--from-html` (~30 linhas adicionadas)
- `scripts/tests/test_pdf_generator.py`: testes pra `--from-html` (~50 linhas adicionadas)
- `requirements.txt`: + `matplotlib>=3.7`, `playwright>=1.40`
- `scripts/tests/test_integration_mcp.py`: adicionar 5 novos scripts a SCRIPTS_EXCLUIDOS
- `scripts/tests/test_workspace_separation.py`: allowlist commands/auditoria-pro.md
- `AGENTS.md`: count 33 → 34, mention `/auditoria-pro` na seção
- `CHANGELOG.md`: v6.8.0 entry com features novos
- `.claude-plugin/plugin.json`: bump 6.7.0 → 6.8.0
- `.claude-plugin/marketplace.json`: bump version

**Total estimado:** ~2.500 linhas novas + ~150 linhas modificadas.

---

## Open questions

### Confirmações pendentes (pode iterar durante implementação, não bloqueante)
- Capa: incluir foto do consultor/agência ou só logo? Default: só logo + texto.
- Glossário: 30 termos é suficiente ou queremos 50+? Default: 30, expandir conforme necessário.
- Radar chart: variante simples (1 polígono) ou comparativo (cliente vs benchmark setor)? Default: simples na v6.8.0, comparativo em v6.8.1+.
- Footer com paginação: incluir "Página X de Y"? Default: sim.

### V6.8.1+ candidatos (fora do scope desta release)
1. Apify para screenshots de concorrentes (Meta Ad Library + Instagram visuals)
2. Bounding boxes nos screenshots (overlay nas seções comentadas)
3. HTML interativo como output alternativo (radar clicável, sections expansíveis)
4. Versão mobile dos screenshots (viewport 375x812)
5. Roadmap exportável pra Trello/Linear/Notion via MCP
6. Outros 3 tipos com mesmo nível premium (instagram-pro, meta-ads-pro, youtube-pro)

---

## Implementation order (preview pra writing-plans)

1. Spec + dependências em `requirements.txt`
2. `audit_glossary.py` + tests (estático, isolado)
3. `audit_radar_chart.py` + tests (matplotlib isolado)
4. `audit_screenshot.py` + tests (Playwright isolado)
5. `audit_roadmap_generator.py` + tests (puro Python)
6. `audit_premium_template.py` + tests (HTML/CSS, depende dos 4 anteriores)
7. `pdf_generator.py` extension `--from-html` + tests
8. `commands/auditoria-pro.md` (depende dos 6 scripts; aqui o command bate com pipeline)
9. Smoke integration test
10. `docs/AUDITORIA-PRO.md`
11. Manual validation 3 cenários
12. AGENTS.md + CHANGELOG + bump v6.8.0

Ordem garante: dependências resolvidas, isolamento testável, command só entra quando scripts já passam tests.
