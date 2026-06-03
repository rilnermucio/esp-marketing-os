---
description: Create a design brief with specs, palettes, typography, and component requirements. Dispatches mos-design simples ou mos-design + mos-brand (+ opcional mos-ai-tools) em paralelo para identidade completa.
argument-hint: "<project type, e.g., 'Instagram carousel template' or 'landing page design for SaaS'>"
---

# /criar-brief-design: Brief de Design (Dispatch-Based)

Cria brief de design completo orquestrando subagent(s) especializados via `Agent(subagent_type: "mos-*")`. Não produz inline.

## Required inputs (ask if missing)

1. **Project type** (obrigatório): social media template, landing page, carousel, ad creative, brand identity, presentation, email template
2. **Brand context** (obrigatório): nome, indústria, cores/fontes existentes (se houver), mood
3. **Purpose** (obrigatório): o que o design precisa gerar (conversão, awareness, branding, retenção)
4. **Audiência** (opcional): quem vai ver
5. **Plataformas** (opcional): onde será usado (Instagram, web, print, etc.)
6. **Style preference** (opcional): minimalista, bold, corporativo, playful, premium, tech, organic
7. **References** (opcional): inspiração, concorrentes, mood references
8. **AI image prompts?** (opcional): se sim, ativa dispatch adicional do `mos-ai-tools`

## Dispatch Decision Tree

```
Briefing recebido
  ├── Brief de 1 peça única (ad creative, social template, email template, etc.)
  │   COM identidade de marca já definida?
  │     └── Dispatch SIMPLES: mos-design
  │
  ├── Brief envolve identidade de marca completa (brand identity, novo cliente,
  │   sem brand book, ou redesign de marca)?
  │     └── Dispatch PARALELO: mos-design + mos-brand
  │         (mos-brand cuida de paleta + tipografia + tom + identidade;
  │          mos-design cuida de specs técnicas + layout + componentes)
  │
  └── Usuário pediu prompts pra IA gerar visuais (Midjourney/Flux/Ideogram)?
        └── ADICIONAR EM PARALELO: mos-ai-tools
            (junto com mos-design, ou junto com mos-design + mos-brand)
```

`mos-design` tem `memory: project`. `mos-brand` também tem `memory: project`. Explicite "considere memory existente do cliente" em ambos os prompts. `mos-ai-tools` não tem memory, passe tudo no prompt.

## Dispatch Simples (1 peça, identidade existente)

```
Agent(subagent_type: "mos-design", prompt: "Brief de design completo para [project type]. Brand: [brand context]. Purpose: [purpose]. Audiência: [audiência]. Plataformas: [plataformas]. Style: [style]. Considere memory existente do cliente neste projeto. Entregue: visual direction (style + mood + 3-5 adjetivos descritivos + references), color palette completa (primary, secondary, accent, neutral, background, surface — 6 cores com hex e usage), typography (heading + body + accent fonts com weights e scale), layout principles (grid + spacing unit + border radius + shadows), component specs detalhadas (dimensões, layout, elementos, estados), dimensions table por plataforma com formatos e DPI, design checklist (cores, tipografia, espaçamento, mobile, contraste WCAG AA, exports). Aplicar quality gates globais (sem travessão, sem 'brutal', PT-BR correto).")
```

## Dispatch Paralelo (identidade completa, single message)

```
- Agent(subagent_type: "mos-brand", prompt: "Identidade de marca para [brand name] em [indústria]. Audiência: [audiência]. Purpose: [purpose]. Style preference: [style]. Considere memory existente do cliente neste projeto. Entregue: arquétipo de marca, posicionamento, manifesto, tom de voz (3-5 atributos + do/don't), paleta de cores justificada por psicologia + nicho (primary, secondary, accent, neutral — com hex e racional), tipografia recomendada (heading + body + accent com personalidade da fonte), brand voice examples (3 exemplos curtos de copy no tom da marca), aplicação em diferentes contextos. Aplicar quality gates globais.")

- Agent(subagent_type: "mos-design", prompt: "Brief de design técnico para [project type]. Brand: [brand context]. Purpose: [purpose]. Plataformas: [plataformas]. Considere memory existente do cliente neste projeto. Aguarde paleta + tipografia do mos-brand e construa em cima delas. Entregue: layout principles (grid + spacing + border radius + shadows), component specs detalhadas (dimensões, layout, elementos, estados), dimensions table por plataforma com formatos e DPI, hierarquia visual, mobile responsive specs, design checklist (acessibilidade WCAG AA, exports). Aplicar quality gates globais.")
```

## Adicional (paralelo, se usuário pediu prompts de IA)

```
- Agent(subagent_type: "mos-ai-tools", prompt: "Prompts otimizados para gerar visuais com IA (Midjourney + Flux + Ideogram + DALL-E) para [project type]. Brand context: [brand context]. Style: [style]. Mood: [mood — pegar de mos-brand se houver]. Audiência: [audiência]. Entregue: 3-5 prompts por uso principal (hero image, supporting visual, background pattern, social asset, etc.), com aspect ratio e parâmetros específicos por ferramenta (--ar, --style, etc.), variações de tom/composição, prompt para variações A/B. Não use cenas com pessoas reais identificáveis sem aviso. Aplicar quality gates globais.")
```

## Consolidação

Após os agents retornarem, entregue:

```markdown
## Design Brief: [Project Type]

Brand: [...] | Purpose: [...] | Plataformas: [...] | Style: [...]

### Visual Direction
- Style: [...]
- Mood: [3-5 adjetivos]
- References: [...]
- Arquétipo de marca (se mos-brand): [...]
- Tom de voz (se mos-brand): [...]

### Color Palette (de mos-brand quando houver, senão mos-design)
| Role | Swatch | Hex | Usage |
|------|--------|-----|-------|
| Primary | ■ | #[...] | [...] |
| Secondary | ■ | #[...] | [...] |
| Accent | ■ | #[...] | [...] |
| Neutral | ■ | #[...] | [...] |
| Background | ■ | #[...] | [...] |
| Surface | ■ | #[...] | [...] |

Racional da paleta (se mos-brand): [psicologia + nicho]

### Typography
- Heading: [Font]: [Weight] (personalidade: ...)
- Body: [Font]: [Weight]
- Accent: [Font]: [Weight] (se aplicável)
- Scale: H1/H2/H3/Body/Small/Caption (size px / line-height)

### Layout & Spacing (de mos-design)
- Grid: [12 cols | 8 cols | free]
- Spacing unit: [base px]: multiples
- Border radius: [...]
- Shadows: [...]

### Component Specs (de mos-design)
**Component 1: [Name]**
- Dimensões: [W x H]
- Layout: [...]
- Elementos: [...]
- Estados: default, hover, active, disabled

[Repetir por componente]

### Dimensions Table
| Asset | Width | Height | Format | DPI |
|-------|-------|--------|--------|-----|
| [...] | [...] | [...] | PNG/JPG/SVG | 72/300 |

### Brand Voice Examples (se mos-brand)
1. [Exemplo de copy 1]
2. [Exemplo de copy 2]
3. [Exemplo de copy 3]

### AI Image Prompts (se mos-ai-tools)
**Prompt 1, [Uso]:**
"[Prompt detalhado para Midjourney/Flux/Ideogram, com aspect ratio e parâmetros]"

[Repetir por uso]

### Design Checklist
- [ ] Cores aplicadas conforme palette
- [ ] Tipografia consistente em todos os componentes
- [ ] Espaçamento seguindo grid
- [ ] Mobile responsive verificado
- [ ] Contraste WCAG AA validado
- [ ] Assets exportados nos formatos corretos
- [ ] Marca/logo posicionados corretamente

### Próximos passos
- Conectar brief ao Figma via MCP
- Gerar copy que acompanha o design
- Adaptar brief pra plataformas adicionais
- Especificação de component library completa
```

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Sem `—`, sem "brutal", sem CAPS gratuito
- Acentuação PT-BR correta
- Contraste WCAG AA validado em qualquer combinação cor+texto
- Hex codes corretos (6 dígitos, sem #ABC abreviado)
- Dimensões em pixels com unidades explícitas
- Compliance regulatório se nicho saúde/finanças/suplementos (claims visuais)
- Prompts de IA não devem gerar pessoas reais identificáveis sem aviso

## Por que esse dispatch

1 peça com identidade existente: `mos-design` resolve sozinho (knowledge profunda de specs por plataforma, layout principles, component patterns). Identidade completa: `mos-brand` define a alma (paleta com racional, tipografia com personalidade, arquétipo, tom) e `mos-design` constrói o esqueleto técnico em cima, paralelizam porque são camadas independentes (mos-brand não precisa de specs técnicas, mos-design pode trabalhar layout/grid sem cor final). `mos-ai-tools` adicional só quando pedido explicitamente, porque prompts de IA têm escopo próprio e não dependem de specs nem de identidade pra começar.
