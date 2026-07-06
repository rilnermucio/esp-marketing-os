---
description: Capture screenshots of landing pages, social profiles, or competitor sites via Playwright MCP. Optionally dispatches mos-research or mos-design for analysis after capture.
argument-hint: "<URL to capture, e.g., 'https://competitor.com' or 'Instagram profile @username'>"
---

# /capturar-tela: Captura de Tela

Utility de captura via Playwright MCP. Operação principal é a captura visual. Análise pós-captura é dispatch opcional baseado na intenção do usuário.

## Required inputs (ask if missing)

1. **URL** (obrigatório): página a capturar
2. **Tipo de captura** (opcional): full page, above the fold, seção específica, mobile view, multiple viewports
3. **Device** (opcional): Desktop (1920x1080), Tablet (768x1024), Mobile (375x812)
4. **Propósito** (opcional): análise, referência, auditoria competitiva, inspiração de design

## Tipos de captura

- **Full Page**: página inteira de cima a baixo, com scroll
- **Above the Fold**: só o que aparece sem scroll (hero + CTA principal)
- **Mobile View**: como aparece em iPhone 14 (375x812)
- **Multiple Viewports**: mesma página em desktop + tablet + mobile pra análise responsiva

## Workflow

```
1. browser_navigate            → carrega URL
2. browser_resize              → seta viewport (se device específico)
3. wait 3s ou elemento âncora  → garante carregamento
4. browser_take_screenshot     → captura
5. browser_snapshot (opcional) → árvore de acessibilidade pra análise textual
6. browser_evaluate (opcional) → extrai dados específicos da página
```

## MCP tools usados

| Tool | Propósito |
|------|-----------|
| `browser_navigate` | Carrega URL |
| `browser_resize` | Seta viewport |
| `browser_take_screenshot` | Captura visual |
| `browser_snapshot` | Árvore de acessibilidade |
| `browser_evaluate` | Extrai dados específicos |

## Dispatch opcional pós-captura (analyze intent)

Se o usuário pediu **análise** junto com a captura, despache **após** a captura concluída:

```
Intenção do usuário                          → Dispatch
─────────────────────────────────────────────────────────────────────
"analise este hero / above-the-fold"         → Agent(subagent_type: "mos-research", prompt: "Análise UX/conversão do above-the-fold capturado: positioning, headline clarity, hierarquia, CTA visibility, prova social, fricções óbvias. Screenshot/snapshot anexo: [referência].")

"avalia o design / paleta / tipografia"      → Agent(subagent_type: "mos-design", prompt: "Análise visual da página capturada: paleta, tipografia, hierarquia, mood, cohesion, comparação com benchmarks de [nicho]. Screenshot anexo: [referência].")

"extrai estratégia / clona padrões"          → roteia pra /clonar-estrategia (mencionar)

"compara com concorrentes"                   → roteia pra /analisar-concorrencia (mencionar)

(sem pedido de análise, só captura)         → Pular dispatch, entregar screenshot puro
```

## Output

```markdown
## Captura de Tela

URL: [URL]
Viewport: [dimensions]
Device: [Desktop | Tablet | Mobile]
Capturado em: [data/hora]

### Screenshot
[imagem]

### Análise da página (se dispatch rodou)
**Tipo:** [Landing page | Blog | Social profile | E-commerce]

**Above the fold:**
- [ ] Headline visível e clara
- [ ] CTA visível
- [ ] Value proposition clara
- [ ] Hierarquia visual eficaz

**Observações** (de mos-research ou mos-design):
[Output do agent dispatchado]

### Insights competitivos (se for análise de concorrente)
| Elemento | Abordagem deles | Oportunidade |
|----------|-----------------|--------------|
| Headline | [...] | [...] |
| CTA | [...] | [...] |
| Prova social | [...] | [...] |
| Design | [...] | [...] |
```

## Quality Gates (na análise, se dispatch rodou)

Aplicar gates globais do `skills/marketing-os/SKILL.md` em qualquer texto de análise:
- Sem `—`, sem "brutal", sem CAPS gratuito
- Acentuação PT-BR correta
- Máximo 1-2 emojis

## Follow-up ao usuário

"Quer que eu:
1. Capture a versão mobile da mesma página?
2. Compare com outro concorrente?
3. Crie landing page inspirada nesse design? (roteia pra /criar-landing-page)
4. Analise os elementos de conversão em profundidade? (dispatch mos-research)"
