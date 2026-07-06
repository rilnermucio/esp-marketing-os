"""Premium HTML/CSS template renderer for /auditoria-pro PDF reports.

Renders 10 sections: cover, executive summary, methodology, visual scorecard,
per-dimension analysis (7), competitive comparison, roadmap, appendix, glossary,
next steps. CSS embedded for weasyprint compatibility.

Visual identity: deep ink blue #0a2540 + warm orange #ff6b35.
"""

from __future__ import annotations

from html import escape

_DEFAULT_CONFIG = {
    "brand_name": "marketing-os",
    "primary_color": "#0a2540",
    "accent_color": "#ff6b35",
    "footer_text": "Auditoria Pro · marketing-os",
    "logo_path": None,
}


# NOTE: CSS uses {primary} and {accent} as .format() placeholders.
# CSS counter() functions are escaped as {{counter(page)}} / {{counter(pages)}}
# so .format() doesn't treat them as Python placeholders.
_CSS = """
:root {{
  --primary: {primary};
  --accent: {accent};
  --text: #1a1a1a;
  --muted: #6b7280;
  --bg-soft: #f9fafb;
  --border: #e5e7eb;
  --success: #16a34a;
  --warning: #f59e0b;
  --danger: #dc2626;
}}
@page {{ size: A4; margin: 2.5cm 2cm; @bottom-right {{ content: "Página " counter(page) " de " counter(pages); font-size: 9pt; color: var(--muted); }} }}
@page :first {{ margin: 0; @bottom-right {{ content: ""; }} }}
* {{ box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; color: var(--text); line-height: 1.55; font-size: 11pt; margin: 0; }}
.page {{ page-break-before: always; padding: 0; }}
.page:first-of-type {{ page-break-before: auto; }}
.cover {{ width: 100%; height: 297mm; background: linear-gradient(135deg, var(--primary) 0%, #1a3a5c 100%); color: white; padding: 60mm 30mm; display: flex; flex-direction: column; justify-content: space-between; }}
.cover-brand {{ font-size: 14pt; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; opacity: 0.85; }}
.cover-title {{ font-size: 48pt; font-weight: 700; line-height: 1.1; margin-top: 40pt; }}
.cover-client {{ font-size: 24pt; font-weight: 400; margin-top: 12pt; opacity: 0.9; }}
.cover-meta {{ display: flex; flex-direction: column; gap: 6pt; font-size: 11pt; opacity: 0.8; margin-top: 60pt; }}
.cover-confidential {{ display: inline-block; background: var(--accent); color: white; padding: 4pt 12pt; border-radius: 4pt; font-size: 10pt; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; align-self: flex-end; }}
h1 {{ font-size: 28pt; color: var(--primary); font-weight: 700; margin: 0 0 16pt 0; line-height: 1.2; }}
h2 {{ font-size: 20pt; color: var(--accent); font-weight: 600; border-bottom: 2px solid var(--accent); padding-bottom: 8pt; margin: 28pt 0 12pt 0; }}
h3 {{ font-size: 14pt; color: var(--primary); font-weight: 600; margin: 18pt 0 8pt 0; }}
h4 {{ font-size: 11pt; color: var(--primary); font-weight: 600; margin: 12pt 0 4pt 0; text-transform: uppercase; letter-spacing: 0.5px; }}
p {{ margin: 0 0 10pt 0; text-align: justify; }}
.score-big {{ font-size: 96pt; color: var(--primary); font-weight: 700; line-height: 1; text-align: center; margin: 20pt 0; }}
.score-label {{ text-align: center; font-size: 13pt; color: var(--muted); text-transform: uppercase; letter-spacing: 2px; margin-top: -10pt; }}
.exec-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24pt; margin-top: 24pt; }}
.exec-card {{ background: var(--bg-soft); border-left: 4px solid var(--accent); padding: 16pt; border-radius: 4pt; }}
.exec-card.strength {{ border-left-color: var(--success); }}
table {{ width: 100%; border-collapse: collapse; margin: 12pt 0; font-size: 10pt; }}
table thead {{ background: var(--primary); color: white; }}
table th, table td {{ padding: 8pt 10pt; text-align: left; border-bottom: 1px solid var(--border); }}
table tbody tr:nth-child(even) {{ background: var(--bg-soft); }}
.scorecard-status {{ padding: 2pt 8pt; border-radius: 3pt; font-size: 9pt; font-weight: 600; }}
.status-forte {{ background: #dcfce7; color: #166534; }}
.status-ok {{ background: #fef3c7; color: #92400e; }}
.status-atencao {{ background: #fee2e2; color: #991b1b; }}
.priority-alta {{ background: #fee2e2; color: #991b1b; padding: 2pt 8pt; border-radius: 3pt; font-size: 9pt; font-weight: 600; }}
.priority-media {{ background: #fef3c7; color: #92400e; padding: 2pt 8pt; border-radius: 3pt; font-size: 9pt; font-weight: 600; }}
.priority-baixa {{ background: #dbeafe; color: #1e40af; padding: 2pt 8pt; border-radius: 3pt; font-size: 9pt; font-weight: 600; }}
.dimension-section {{ page-break-inside: avoid; margin-bottom: 24pt; }}
.dimension-header {{ display: flex; justify-content: space-between; align-items: baseline; border-bottom: 1px solid var(--border); padding-bottom: 8pt; }}
.dimension-score-pill {{ font-size: 24pt; color: var(--primary); font-weight: 700; }}
.dimension-prose {{ margin: 12pt 0; }}
.evidences-list {{ background: var(--bg-soft); padding: 12pt 16pt; border-radius: 4pt; margin: 12pt 0; }}
.evidences-list ul {{ margin: 6pt 0; padding-left: 20pt; }}
.before-after {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16pt; margin: 12pt 0; }}
.before-after-card {{ padding: 12pt; border-radius: 4pt; }}
.before-card {{ background: #fee2e2; border-left: 3pt solid var(--danger); }}
.after-card {{ background: #dcfce7; border-left: 3pt solid var(--success); }}
.before-after-label {{ font-size: 9pt; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; margin-bottom: 4pt; }}
blockquote.agent-citation {{ border-left: 3pt solid var(--accent); padding: 8pt 16pt; margin: 12pt 0; color: var(--muted); font-style: italic; background: var(--bg-soft); }}
img.screenshot {{ max-width: 100%; border: 1px solid var(--border); border-radius: 4pt; margin: 12pt 0; }}
img.radar-chart {{ max-width: 600px; display: block; margin: 16pt auto; }}
.competitive-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 16pt; margin: 16pt 0; }}
.competitor-card {{ background: var(--bg-soft); padding: 16pt; border-radius: 4pt; }}
.roadmap-bucket {{ margin: 16pt 0; }}
.roadmap-bucket-header {{ display: flex; align-items: center; gap: 12pt; margin-bottom: 8pt; }}
.roadmap-bucket-title {{ font-size: 13pt; color: var(--primary); font-weight: 700; }}
.roadmap-bucket-pill {{ padding: 2pt 12pt; background: var(--accent); color: white; border-radius: 99pt; font-size: 9pt; font-weight: 600; }}
.appendix-agent {{ page-break-inside: avoid; margin: 20pt 0; padding: 16pt; background: var(--bg-soft); border-radius: 4pt; }}
.appendix-agent-header {{ font-size: 13pt; font-weight: 700; color: var(--primary); margin-bottom: 12pt; }}
.glossary dt {{ font-weight: 700; color: var(--primary); margin-top: 8pt; }}
.glossary dd {{ margin: 0 0 12pt 0; padding-left: 0; color: var(--text); }}
.next-steps-box {{ background: var(--primary); color: white; padding: 24pt; border-radius: 4pt; margin: 16pt 0; }}
.next-steps-box h2 {{ color: white; border-bottom-color: rgba(255,255,255,0.3); }}
.muted {{ color: var(--muted); font-size: 10pt; }}
.divider {{ height: 1px; background: var(--border); margin: 20pt 0; }}
"""


def _render_cover(data: dict, config: dict | None) -> str:
    cfg = {**_DEFAULT_CONFIG, **(config or {})}
    brand = escape(cfg["brand_name"])
    client = escape(data["client_name"])
    url = escape(data["client_url"])
    audit_type = escape(data["audit_type"])
    ts = escape(data["timestamp"])
    return f"""
    <section class="cover">
      <div>
        <div class="cover-brand">{brand}</div>
        <h1 class="cover-title" style="color: white;">Auditoria Pro</h1>
        <div class="cover-client">{client}</div>
        <div class="cover-meta">
          <div>URL: {url}</div>
          <div>Tipo: {audit_type}</div>
          <div>Data: {ts}</div>
        </div>
      </div>
      <div class="cover-confidential">Confidencial</div>
    </section>
    """


def _render_executive_summary(data: dict) -> str:
    score = data["overall_score"]
    summary = escape(data["exec_summary"])
    partial_label = " (parcial)" if data.get("partial") else ""
    return f"""
    <section class="page">
      <h1>Sumário Executivo</h1>
      <div class="score-big">{score}</div>
      <div class="score-label">Score Geral{escape(partial_label)} · 0 a 100</div>
      <div class="divider"></div>
      <p>{summary}</p>
    </section>
    """


def _render_methodology() -> str:
    return """
    <section class="page">
      <h1>Metodologia</h1>
      <p>Esta auditoria foi conduzida via dispatch paralelo de 7 agents especializados (research, SEO, copy, funnel, ads, design, brand) que analisaram a landing page usando WebFetch e conhecimento público setorizado. As respostas foram sintetizadas via rubric ponderada de 7 dimensões.</p>
      <h2>Dimensões avaliadas</h2>
      <table>
        <thead><tr><th>Dimensão</th><th>Peso</th><th>Foco</th></tr></thead>
        <tbody>
          <tr><td>Conversão (CTA, friction, funil)</td><td>25%</td><td>Caminho até a ação principal, atrito, lead magnets</td></tr>
          <tr><td>Copy (headline, value prop)</td><td>20%</td><td>Clareza, persuasão, especificidade</td></tr>
          <tr><td>SEO (technical + content)</td><td>15%</td><td>Title, meta, schema, performance, mobile</td></tr>
          <tr><td>Trust signals</td><td>10%</td><td>Prova social, garantias, autoridade</td></tr>
          <tr><td>Design (hierarquia visual)</td><td>10%</td><td>Hierarquia, tipografia, acessibilidade</td></tr>
          <tr><td>Brand (consistência, voice)</td><td>10%</td><td>Voice, identidade, persona</td></tr>
          <tr><td>Diferenciação competitiva</td><td>10%</td><td>Posicionamento vs alternativas</td></tr>
        </tbody>
      </table>
      <h2>Frameworks aplicados</h2>
      <p>Análise de copy via 4Us (Útil, Urgente, Único, Específico), princípios de Cialdini para trust signals, hierarquia visual via Gestalt, scoring de fricção segundo Sugarman.</p>
      <h2>Limitações declaradas</h2>
      <p>A análise considerou exclusivamente conteúdo público acessível via WebFetch e WebSearch. Dados internos (analytics, funil real, ROI de campanhas) não estão refletidos.</p>
    </section>
    """


def _render_visual_scorecard(data: dict, charts: dict) -> str:
    radar_path = charts.get("radar")
    radar_html = (
        f'<img class="radar-chart" src="file://{radar_path}" alt="Radar de scores" />'
        if radar_path
        else ""
    )

    rows = []
    for dim, info in data["dimensions"].items():
        score = info["score"]
        weight = info["weight"]
        if score is None:
            status = "N/D"
            cls = "scorecard-status"
            score_str = "N/D"
        elif score >= 80:
            status = "Forte"
            cls = "scorecard-status status-forte"
            score_str = str(score)
        elif score >= 60:
            status = "OK"
            cls = "scorecard-status status-ok"
            score_str = str(score)
        else:
            status = "Atenção"
            cls = "scorecard-status status-atencao"
            score_str = str(score)
        rows.append(
            f"<tr><td>{escape(dim)}</td><td>{weight}%</td><td>{score_str}</td><td><span class='{cls}'>{status}</span></td></tr>"
        )

    return f"""
    <section class="page">
      <h1>Diagnóstico Visual</h1>
      {radar_html}
      <h2>Scorecard</h2>
      <table>
        <thead><tr><th>Dimensão</th><th>Peso</th><th>Score</th><th>Status</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </section>
    """


def _render_dimension_section(name: str, data: dict, screenshot: str | None) -> str:
    score = data.get("score", "N/D")
    weight = data.get("weight", 0)
    prose = escape(data.get("prose", ""))
    evidences = data.get("evidences", [])
    fixes = data.get("fixes", [])
    before_after = data.get("before_after", [])
    citation = data.get("agent_citation", "")

    evid_html = (
        "<ul>" + "".join(f"<li>{escape(e)}</li>" for e in evidences) + "</ul>"
        if evidences
        else ""
    )
    fixes_html = ""
    for fix in fixes:
        prio = fix.get("priority", "baixa")
        fixes_html += f'<p><span class="priority-{prio}">{prio.upper()}</span> {escape(fix["text"])}</p>'

    ba_html = ""
    if before_after:
        ba_html = "<h4>Antes vs Depois (Copy sugerido)</h4><div class='before-after'>"
        for ba in before_after:
            ba_html += f"""
            <div class="before-after-card before-card">
              <div class="before-after-label">Antes</div>
              <div>{escape(ba['before'])}</div>
            </div>
            <div class="before-after-card after-card">
              <div class="before-after-label">Depois</div>
              <div>{escape(ba['after'])}</div>
            </div>
            """
        ba_html += "</div>"

    citation_html = (
        f'<blockquote class="agent-citation">{escape(citation)}</blockquote>'
        if citation
        else ""
    )
    screenshot_html = (
        f'<img class="screenshot" src="file://{screenshot}" alt="Screenshot" />'
        if screenshot
        else ""
    )

    return f"""
    <section class="dimension-section">
      <div class="dimension-header">
        <h2 style="border:none; margin:0;">{escape(name)}</h2>
        <div class="dimension-score-pill">{score}<span style="font-size:14pt; color:var(--muted);"> / 100 · peso {weight}%</span></div>
      </div>
      <div class="dimension-prose"><p>{prose}</p></div>
      {screenshot_html}
      <h4>Evidências observadas</h4>
      <div class="evidences-list">{evid_html}</div>
      {ba_html}
      <h4>Fix priorizado</h4>
      {fixes_html}
      {citation_html}
    </section>
    """


def _render_competitive(data: dict) -> str:
    competitive = data.get("competitive", {})
    competitors = competitive.get("competitors", [])
    table = competitive.get("table_md", "")
    cards = "".join(
        f'<div class="competitor-card"><h3>{escape(c["name"])}</h3><p>{escape(c.get("differentiation", ""))}</p></div>'
        for c in competitors
    )
    return f"""
    <section class="page">
      <h1>Análise Competitiva</h1>
      <p>Posicionamento da auditoria em relação aos principais concorrentes diretos identificados durante o research.</p>
      <div class="competitive-grid">{cards}</div>
      <h2>Tabela comparativa</h2>
      <div>{table}</div>
    </section>
    """


def _render_roadmap(roadmap: dict) -> str:
    def render_bucket(title: str, pill: str, items: list) -> str:
        if not items:
            return f"<div class='roadmap-bucket'><div class='roadmap-bucket-header'><div class='roadmap-bucket-title'>{title}</div><div class='roadmap-bucket-pill'>{pill}</div></div><p class='muted'>Sem itens críticos.</p></div>"
        rows = "".join(
            f"<tr><td>{escape(item['action'])}</td><td>{escape(item['dimension'])}</td><td>{item['effort']}</td><td>{item['impact']}</td><td>{escape(item['owner'])}</td></tr>"
            for item in items
        )
        return f"""
        <div class="roadmap-bucket">
          <div class="roadmap-bucket-header">
            <div class="roadmap-bucket-title">{title}</div>
            <div class="roadmap-bucket-pill">{pill}</div>
          </div>
          <table>
            <thead><tr><th>Ação</th><th>Dimensão</th><th>Esforço</th><th>Impacto</th><th>Owner sugerido</th></tr></thead>
            <tbody>{rows}</tbody>
          </table>
        </div>
        """

    return f"""
    <section class="page">
      <h1>Roadmap de Implementação</h1>
      <p>Sequenciamento dos fixes identificados, organizados por horizonte de execução. Esforço S/M/L (small/medium/large) e impacto estimado.</p>
      {render_bucket("Quick wins", "30 dias", roadmap.get("30_days", []))}
      {render_bucket("Impacto estruturante", "90 dias", roadmap.get("90_days", []))}
      {render_bucket("Transformações de fundo", "180 dias", roadmap.get("180_days", []))}
    </section>
    """


def _render_appendix(data: dict) -> str:
    appendix = data.get("appendix", {})
    sections = []
    for agent, raw in appendix.items():
        sections.append(f"""
        <details class="appendix-agent">
          <summary class="appendix-agent-header">Output completo: mos-{escape(agent)}</summary>
          <pre style="white-space: pre-wrap; font-size: 9pt;">{escape(raw)}</pre>
        </details>
        """)
    return f"""
    <section class="page">
      <h1>Apêndice Técnico</h1>
      <p>Outputs completos dos 7 agents. Use como referência pra desenvolvedores e especialistas.</p>
      {''.join(sections)}
    </section>
    """


def _render_glossary(used_terms: set | None = None) -> str:
    from audit_glossary import render_glossary_md

    md = render_glossary_md(used_terms)
    if not md:
        return ""

    # Convert simple markdown to HTML manually (preserving structure)
    lines = md.split("\n")
    html_parts = ["<section class='page'>", "<h1>Glossário</h1>"]
    in_dl = False
    for line in lines:
        if line.startswith("##"):
            continue  # already have h1
        if line.startswith("**") and "." in line:
            term, _, definition = line.partition(".** ")
            term = term.lstrip("*").rstrip("*")
            if not in_dl:
                html_parts.append("<dl class='glossary'>")
                in_dl = True
            html_parts.append(f"<dt>{escape(term)}</dt><dd>{escape(definition)}</dd>")
    if in_dl:
        html_parts.append("</dl>")
    html_parts.append("</section>")
    return "\n".join(html_parts)


def _render_next_steps(config: dict | None) -> str:
    cfg = {**_DEFAULT_CONFIG, **(config or {})}
    return f"""
    <section class="page">
      <h1>Próximos Passos</h1>
      <div class="next-steps-box">
        <h2 style="margin-top:0;">Como avançar</h2>
        <p>Esta auditoria identifica oportunidades específicas. A implementação dos fixes priorizados costuma gerar lift mensurável em 30-90 dias quando executada com disciplina.</p>
        <h3 style="color:white; margin-top:20pt;">Recomendamos</h3>
        <ol>
          <li><strong>Sessão de apresentação:</strong> revisar os achados com o time responsável e priorizar conjuntamente.</li>
          <li><strong>Sprint de quick wins:</strong> atacar primeiro os itens de 30 dias, validar lift via analytics.</li>
          <li><strong>Acompanhamento:</strong> auditoria de followup após 90 dias pra medir progresso e recalibrar.</li>
        </ol>
        <p style="margin-top: 20pt;"><strong>Contato.</strong> {escape(cfg['brand_name'])}</p>
      </div>
    </section>
    """


def render(
    report_data: dict,
    screenshots: dict,
    charts: dict,
    config: dict | None,
) -> str:
    """Render full HTML for premium PDF."""
    cfg = {**_DEFAULT_CONFIG, **(config or {})}

    css = _CSS.format(primary=cfg["primary_color"], accent=cfg["accent_color"])

    sections = []
    sections.append(_render_cover(report_data, config))
    sections.append(_render_executive_summary(report_data))
    sections.append(_render_methodology())
    sections.append(_render_visual_scorecard(report_data, charts))

    dim_screenshots = screenshots.get("dimensions", {})
    dim_html_parts = ["<section class='page'>", "<h1>Análise por Dimensão</h1>"]
    for dim_name, dim_data in report_data["dimensions"].items():
        dim_html_parts.append(
            _render_dimension_section(dim_name, dim_data, dim_screenshots.get(dim_name))
        )
    dim_html_parts.append("</section>")
    sections.append("\n".join(dim_html_parts))

    sections.append(_render_competitive(report_data))
    sections.append(_render_roadmap(report_data.get("roadmap", {})))
    sections.append(_render_appendix(report_data))
    sections.append(_render_glossary(report_data.get("used_terms")))
    sections.append(_render_next_steps(config))

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Auditoria Pro · {escape(report_data.get('client_name', ''))}</title>
<style>{css}</style>
</head>
<body>
{''.join(sections)}
</body>
</html>"""
