# 01. W3C Design Tokens Spec, Companion

> Parte da stack de companions do `design-agent` (v4.0).
> Referência profunda sobre Design Tokens Community Group (DTCG) spec, operada sob a umbrella do W3C Community Group.

**Quando consultar:** ao desenhar ou evoluir arquitetura de tokens, ao integrar Style Dictionary ou Tokens Studio, ao decidir entre core, semantic e component, ao validar `tokens.json` existente.

**Pré-requisitos:** familiaridade com CSS, JSON, conceitos básicos de design system.

---

## Índice

1. O que é W3C Design Tokens
2. Anatomia de um token
3. Os 13 tipos oficiais
4. Referências e alias
5. Hierarquia de grupos
6. Arquitetura 3 camadas
7. Exemplo completo de `tokens.json`
8. Theming
9. Responsive tokens
10. Style Dictionary pipeline
11. Tokens Studio plugin (Figma)
12. Validation e linting
13. Versionamento de tokens
14. Integrações
15. Anti patterns
16. FAQ

---

## 1. O que é W3C Design Tokens

### 1.1. Origem e status

A especificação é produzida pelo **Design Tokens Community Group (DTCG)**, grupo comunitário operado sob a umbrella do W3C. A versão **2025.10** (publicada em 28 de outubro de 2025) é a primeira estável, encerrando anos de drafts e abrindo espaço para implementações em produção.

Pontos formais: não é W3C Standard em sentido estrito nem está no W3C Standards Track, opera sob o W3C Community Contributor License Agreement (CLA), referência canônica em `designtokens.org/tr/2025.10/format/`.

Neste documento, "DTCG spec" ou "spec 2025.10" são as abreviações usadas.

### 1.2. Objetivos

A spec resolve quatro problemas:

1. **Interoperabilidade entre ferramentas.** Figma, Tokens Studio, Style Dictionary, Theo, Terrazzo tinham formatos incompatíveis.
2. **Portabilidade entre plataformas.** Um arquivo gera CSS, Swift, Kotlin, Dart, XAML, JS sem perda semântica.
3. **Separação intenção vs valor.** Token carrega significado (cor de ação primária), não só o hex.
4. **Governança.** Design system passa a ter contrato de dados versionável e auditável.

### 1.3. Quem usa (adoção 2026)

Alguns sistemas públicos com adoção relevante:

- **Shopify Polaris** publica em `@shopify/polaris-tokens` (npm).
- **GitHub Primer** distribui via `@primer/primitives`, pipeline Style Dictionary.
- **IBM Carbon** em migração progressiva para DTCG.
- **Google Material 3** mantém tokens próprios mapeáveis para DTCG.
- **Microsoft Fluent 2** expõe tokens consumíveis por Style Dictionary.

Nem todos usam 100% da spec, muitos usam subset ou conversão no build. O que importa é que DTCG virou o denominador comum.

### 1.4. Ferramentas alinhadas

| Ferramenta | Papel | Suporta DTCG 2025.10 |
|------------|-------|-----------------------|
| Style Dictionary v4+ | Build multi plataforma | Sim |
| Tokens Studio (Figma) | Autoria visual, sync Git | Sim |
| Specify | Distribuição e sync | Sim |
| Terrazzo | Build e validação em monorepo | Sim |
| Cobalt UI | CLI de validação | Sim |

### 1.5. Relevância para Marketing OS

Conteúdo de marketing (landing, email, ads, posts) reutiliza a identidade visual do produto. Com tokens isolados em `tailwind.config.js`, cada peça vira retrabalho. Centralizando em `tokens.json` (DTCG): fonte de verdade única para CTA em ad/email/landing, consumo por workflows de IA (imagem, vídeo) com restrição automática de paleta, auditoria clara do que é core (imutável), semantic (trocável) e component (efêmero).

---

## 2. Anatomia de um token

### 2.1. Os quatro campos

Um token é objeto JSON com até quatro campos:

| Campo | Obrigatório | Descrição |
|-------|-------------|-----------|
| `$value` | Sim | Valor literal (hex, número, objeto composto, alias) |
| `$type` | Recomendado | Tipo semântico (seção 3). Pode ser herdado do grupo pai |
| `$description` | Não | Texto livre explicando intenção |
| `$extensions` | Não | Metadados específicos de ferramentas |

Qualquer chave sem `$value` vira **grupo** (seção 5).

### 2.2. Exemplo mínimo

```json
{ "color": { "brand": { "primary": {
  "$value": "#5B21B6", "$type": "color",
  "$description": "Cor de marca primária, usada em CTAs de alta prioridade." } } } }
```

### 2.3. `$value` com objeto (tipos compostos)

```json
{ "elevation": { "card": { "$type": "shadow", "$value": {
  "color": "#0000001A",
  "offsetX": { "value": 0, "unit": "px" },
  "offsetY": { "value": 2, "unit": "px" },
  "blur":    { "value": 8, "unit": "px" },
  "spread":  { "value": 0, "unit": "px" } } } } }
```

### 2.4. `$description` como intenção, não valor

Bom: "Cor neutra de fundo para superfícies de conteúdo principal em tema claro."
Ruim: "Um cinza claro, quase branco." (redundante com o hex).

### 2.5. `$extensions` (namespace reverso)

Reservado para ferramentas anexarem dados fora da spec. Regra: namespace reverso (estilo Java package) para evitar colisões. Ferramentas devem ignorar silenciosamente extensões desconhecidas.

```json
{ "color": { "brand": { "primary": {
  "$value": "#5B21B6", "$type": "color",
  "$extensions": {
    "org.acme.tokens":     { "owner": "brand-team", "reviewedAt": "2026-01-15" },
    "studio.tokens.figma": { "styleId": "S:12345" } } } } } }
```

### 2.6. Herança de `$type` via grupo

```json
{ "color": { "$type": "color", "brand": {
  "primary":   { "$value": "#5B21B6" },
  "secondary": { "$value": "#F59E0B" } } } }
```

Filhos herdam `$type: "color"`.

---

## 3. Os 13 tipos oficiais

A spec 2025.10 define 13 tipos. Dividimos em **básicos** (valor escalar ou string), **estruturais** (objetos simples) e **compostos** (combinações).

### 3.1. color

Cor em sRGB (hex, rgb, hsl) ou, a partir de 2025.10, color spaces modernos (P3, Rec2020, oklch, oklab) via objeto.

Formato string (legacy sRGB):
```json
{ "$type": "color", "$value": "#5B21B6" }
```

Formato objeto (recomendado em 2025.10+):
```json
{
  "$type": "color",
  "$value": { "colorSpace": "srgb", "components": [0.357, 0.129, 0.714], "alpha": 1 }
}
```

**Uso comum:** paleta de marca, neutras, status.

### 3.2. dimension

Quantidade em um eixo (largura, altura, raio, espaçamento). Unidades: `px`, `rem`.

```json
{ "$type": "dimension", "$value": { "value": 16, "unit": "px" } }
```

**Uso comum:** spacing scale, border radius, border width.

### 3.3. fontFamily

String única ou array (stack de fallback).

```json
{ "$type": "fontFamily", "$value": ["Inter", "system-ui", "sans-serif"] }
```

### 3.4. fontWeight

Numérico (100 a 1000) ou keyword (`thin`, `light`, `regular`, `medium`, `semi-bold`, `bold`, `extra-bold`, `black`).

```json
{ "$type": "fontWeight", "$value": 600 }
```

### 3.5. duration

Tempo (animações). Unidades: `ms` ou `s`.

```json
{ "$type": "duration", "$value": { "value": 200, "unit": "ms" } }
```

### 3.6. cubicBezier

Curva de easing. Array de 4 números (X em `[0,1]`, Y qualquer).

```json
{ "$type": "cubicBezier", "$value": [0.4, 0, 0.2, 1] }
```

### 3.7. number

Valor numérico puro (sem unidade). Útil para line height em múltiplos, opacidades, z index.

```json
{ "$type": "number", "$value": 1.5 }
```

### 3.8. strokeStyle

Keyword ou objeto com `dashArray` e `lineCap`. Keywords aceitas: `solid`, `dashed`, `dotted`, `double`, `groove`, `ridge`, `outset`, `inset`.

```json
{ "$type": "strokeStyle", "$value": "solid" }
```

```json
{ "$type": "strokeStyle", "$value": { "dashArray": [{ "value": 0.5, "unit": "rem" }, { "value": 0.25, "unit": "rem" }], "lineCap": "round" } }
```

### 3.9. shadow (composto)

Objeto único ou array (empilhamento).

```json
{ "$type": "shadow", "$value": { "color": "#00000033", "offsetX": { "value": 0, "unit": "px" }, "offsetY": { "value": 4, "unit": "px" }, "blur": { "value": 12, "unit": "px" }, "spread": { "value": 0, "unit": "px" }, "inset": false } }
```

### 3.10. border (composto)

Combinação de color, dimension e strokeStyle.

```json
{ "$type": "border", "$value": { "color": "{color.neutral.200}", "width": { "value": 1, "unit": "px" }, "style": "solid" } }
```

### 3.11. transition (composto)

Combinação de duration, delay e cubicBezier.

```json
{ "$type": "transition", "$value": { "duration": { "value": 200, "unit": "ms" }, "delay": { "value": 0, "unit": "ms" }, "timingFunction": [0.4, 0, 0.2, 1] } }
```

### 3.12. gradient (composto)

Array de stops. Cada stop tem `color` e `position`.

```json
{ "$type": "gradient", "$value": [{ "color": "#5B21B6", "position": 0 }, { "color": "#F59E0B", "position": 1 }] }
```

### 3.13. typography (composto)

Combina fontFamily, fontWeight, fontSize, letterSpacing, lineHeight.

```json
{ "$type": "typography", "$value": { "fontFamily": "{fontFamily.sans}", "fontSize": { "value": 1, "unit": "rem" }, "fontWeight": 400, "letterSpacing": { "value": 0, "unit": "em" }, "lineHeight": 1.5 } }
```

### 3.14. Tabela resumo

| Tipo | Categoria | Uso | `$value` |
|------|-----------|-----|----------|
| color | básico | paleta | string ou objeto |
| dimension | básico | spacing, radius | objeto |
| fontFamily | básico | font stack | string ou array |
| fontWeight | básico | peso | número ou keyword |
| duration | básico | animação | objeto |
| cubicBezier | básico | easing | array de 4 |
| number | básico | line height | número |
| strokeStyle | estrutural | borda | string ou objeto |
| shadow | composto | elevation | objeto ou array |
| border | composto | bordas | objeto |
| transition | composto | transições | objeto |
| gradient | composto | gradientes | array |
| typography | composto | texto | objeto |

---

## 4. Referências e alias

### 4.1. Sintaxe

Token referencia outro via `{path.to.token}`. Path usa `.` como separador.

```json
{
  "color": {
    "core": { "purple": { "600": { "$type": "color", "$value": "#5B21B6" } } },
    "brand": { "primary": { "$type": "color", "$value": "{color.core.purple.600}" } }
  }
}
```

`color.brand.primary` resolve para `#5B21B6`.

### 4.2. Alias em propriedades de composto

```json
{ "border": { "focus": { "$type": "border", "$value": {
  "color": "{color.brand.primary}",
  "width": "{dimension.border.2}",
  "style": "solid" } } } }
```

### 4.3. Resolução

Processo top down: parser busca target via path, resolve recursivamente até literal.

### 4.4. Ciclos proibidos

Parser conforme detecta e recusa:

```json
{ "a": { "$type": "color", "$value": "{b}" },
  "b": { "$type": "color", "$value": "{a}" } }
```

Deve falhar na validação com erro explícito.

### 4.5. Alias entre arquivos

A spec não prescreve. Ferramentas concatenam antes de resolver:

- **Style Dictionary**: junta todos os arquivos em objeto único.
- **Tokens Studio**: resolve dentro dos "sets" carregados.

Mantenha alias no mesmo bundle de build.

### 4.6. Quando usar alias

Use para expressar intenção dependente de primitiva:

- `color.brand.primary` => `{color.core.purple.600}` (troca de marca afeta só o alvo).
- `spacing.inset.md` => `{dimension.spacing.4}`.

Evite quando o valor é único e não compartilhado, ou quando a camada intermediária só adiciona ruído.

---

## 5. Hierarquia de grupos

### 5.1. Definição

Qualquer chave sem `$value` é **grupo**. Grupos aninham e repassam `$type`, `$description`, `$extensions` para filhos.

```json
{ "color": { "$type": "color", "$description": "Paleta de cores do sistema.",
  "neutral": { "100": { "$value": "#F5F5F5" }, "900": { "$value": "#171717" } },
  "brand":   { "primary": { "$value": "#5B21B6" } } } }
```

### 5.2. Convenção de nomes

Spec não prescreve, comunidade recomenda **kebab-case**. Também aceito (muito comum): camelCase.

Bom: `{ "font-family": { "sans-serif": { ... } } }` ou `{ "fontFamily": { "sans": { ... } } }`.

Evite:

- Acentos e não ASCII em chaves.
- Espaços.
- Começar com número puro (`600` direto, prefira `weight-600` ou agrupe).

### 5.3. Profundidade recomendada

Entre 3 e 5 níveis. Mais que isso indica over nesting (seção 15).

```
color.semantic.text.primary
^       ^        ^    ^
|       |        |    folha
|       |        categoria semântica
|       camada
categoria
```

### 5.4. Padrões comuns

| Padrão | Exemplo | Quando |
|--------|---------|--------|
| Category, scale | `color.neutral.100` | Core tokens |
| Category, intent | `color.intent.success` | Semantic tokens |
| Component, part, state | `button.background.hover` | Component tokens |
| Platform prefix | `ios.spacing.md` | Tokens específicos de plataforma |

### 5.5. Bom vs ruim

Bom:

```json
{ "spacing": { "$type": "dimension",
  "scale": { "1": { "$value": { "value": 4, "unit": "px" } }, "2": { "$value": { "value": 8, "unit": "px" } } },
  "inset": { "sm": { "$value": "{spacing.scale.2}" } } } }
```

Ruim:

```json
{ "Spacing_XS_small": { "$value": { "value": 4, "unit": "px" } },
  "SPACING-XL-very-big!": { "$value": { "value": 48, "unit": "px" } } }
```

Problemas: mistura de cases, separadores inconsistentes, sem grupo, caracteres especiais.

---

## 6. Arquitetura 3 camadas

Convenção comunitária dominante (a spec não impõe 3 camadas).

### 6.1. Core (Primitive, Global)

Valores literais, agnósticos de contexto. `color.core.purple.600 = #5B21B6`, `spacing.scale.4 = 16px`. Raramente muda, mudança é breaking.

### 6.2. Semantic (Alias, Intent)

Intenção, aliased a core. `color.semantic.action.primary => {color.core.purple.600}`. É onde theming acontece. Troca é segura para consumers (contrato permanece).

### 6.3. Component

Tokens específicos de componente, aliased a semantic. `button.primary.background.default => {color.semantic.action.primary}`. Alto número, vida curta.

### 6.4. Regra da chain

```
component => semantic => core
```

Nunca pule semantic, nem inverta a direção.

### 6.5. Quando cada camada

- **Só core**: protótipos, 1 produto. Não escala para theming.
- **Core + semantic**: produtos com 1 a 3 temas. O mais comum.
- **Core + semantic + component**: grandes, múltiplos times e plataformas.

### 6.6. Exemplo end to end

Botão primário que em light usa roxo 600, em dark usa roxo 400, em marca Acme Go usa laranja 500.

Core:
```json
{ "color": { "core": { "$type": "color",
  "purple": { "400": { "$value": "#A78BFA" }, "600": { "$value": "#5B21B6" } },
  "orange": { "500": { "$value": "#F97316" } } } } }
```

Semantic (light):
```json
{ "color": { "semantic": { "action": { "primary": { "$type": "color", "$value": "{color.core.purple.600}" } } } } }
```

Component:
```json
{ "button": { "primary": { "background": { "default": { "$type": "color", "$value": "{color.semantic.action.primary}" } } } } }
```

Para dark, só a semantic muda. Core e component ficam intactos.

---

## 7. Exemplo completo de `tokens.json`

Projeto fictício **Acme**, SaaS B2B. Aproximadamente 60 tokens folha (exemplo ilustrativo) cobrindo core, semantic e component.

```json
{
  "$description": "Acme Design Tokens, v1.0.0",
  "color": {
    "core": { "$type": "color",
      "neutral": { "0": { "$value": "#FFFFFF" }, "50": { "$value": "#FAFAFA" }, "100": { "$value": "#F5F5F5" }, "200": { "$value": "#E5E5E5" }, "400": { "$value": "#A3A3A3" }, "600": { "$value": "#525252" }, "900": { "$value": "#171717" } },
      "purple":  { "400": { "$value": "#A78BFA" }, "500": { "$value": "#8B5CF6" }, "600": { "$value": "#5B21B6" }, "700": { "$value": "#4C1D95" } },
      "green":   { "600": { "$value": "#059669" } },
      "red":     { "600": { "$value": "#DC2626" } },
      "amber":   { "500": { "$value": "#F59E0B" } }
    },
    "semantic": {
      "$type": "color",
      "text":    { "primary": { "$value": "{color.core.neutral.900}" }, "secondary": { "$value": "{color.core.neutral.600}" }, "disabled": { "$value": "{color.core.neutral.400}" }, "inverse": { "$value": "{color.core.neutral.0}" } },
      "surface": { "primary": { "$value": "{color.core.neutral.0}" },   "secondary": { "$value": "{color.core.neutral.50}" } },
      "action":  { "primary": { "$value": "{color.core.purple.600}" },  "primary-hover": { "$value": "{color.core.purple.700}" } },
      "status":  { "success": { "$value": "{color.core.green.600}" },   "warning": { "$value": "{color.core.amber.500}" }, "danger": { "$value": "{color.core.red.600}" } },
      "border":  { "default": { "$value": "{color.core.neutral.200}" }, "focus": { "$value": "{color.core.purple.500}" } }
    }
  },
  "dimension": {
    "spacing": { "$type": "dimension", "scale": { "0": { "$value": { "value": 0, "unit": "px" } }, "1": { "$value": { "value": 4, "unit": "px" } }, "2": { "$value": { "value": 8, "unit": "px" } }, "3": { "$value": { "value": 12, "unit": "px" } }, "4": { "$value": { "value": 16, "unit": "px" } }, "6": { "$value": { "value": 24, "unit": "px" } }, "8": { "$value": { "value": 32, "unit": "px" } } } },
    "radius":  { "$type": "dimension", "sm": { "$value": { "value": 4, "unit": "px" } }, "md": { "$value": { "value": 8, "unit": "px" } }, "lg": { "$value": { "value": 16, "unit": "px" } }, "full": { "$value": { "value": 9999, "unit": "px" } } }
  },
  "fontFamily": { "$type": "fontFamily",
    "sans": { "$value": ["Inter", "system-ui", "sans-serif"] },
    "mono": { "$value": ["JetBrains Mono", "ui-monospace", "monospace"] } },
  "fontWeight": { "$type": "fontWeight",
    "regular":  { "$value": 400 }, "medium": { "$value": 500 },
    "semibold": { "$value": 600 }, "bold":   { "$value": 700 } },
  "typography": { "$type": "typography",
    "heading-1": { "$value": { "fontFamily": "{fontFamily.sans}", "fontSize": { "value": 2.25, "unit": "rem" }, "fontWeight": "{fontWeight.bold}",    "lineHeight": 1.2, "letterSpacing": { "value": -0.02, "unit": "em" } } },
    "body-base": { "$value": { "fontFamily": "{fontFamily.sans}", "fontSize": { "value": 1,    "unit": "rem" }, "fontWeight": "{fontWeight.regular}", "lineHeight": 1.5, "letterSpacing": { "value": 0,     "unit": "em" } } }
  },
  "shadow": { "$type": "shadow",
    "sm": { "$value": { "color": "#0000001A", "offsetX": { "value": 0, "unit": "px" }, "offsetY": { "value": 1, "unit": "px" }, "blur": { "value": 2,  "unit": "px" }, "spread": { "value": 0, "unit": "px" } } },
    "md": { "$value": { "color": "#00000026", "offsetX": { "value": 0, "unit": "px" }, "offsetY": { "value": 4, "unit": "px" }, "blur": { "value": 12, "unit": "px" }, "spread": { "value": 0, "unit": "px" } } } },
  "motion": {
    "duration": { "$type": "duration",    "fast": { "$value": { "value": 150, "unit": "ms" } }, "base": { "$value": { "value": 250, "unit": "ms" } }, "slow": { "$value": { "value": 400, "unit": "ms" } } },
    "easing":   { "$type": "cubicBezier", "standard": { "$value": [0.4, 0, 0.2, 1] }, "decelerate": { "$value": [0, 0, 0.2, 1] }, "accelerate": { "$value": [0.4, 0, 1, 1] } }
  },
  "button": { "primary": {
    "background": {
      "default": { "$type": "color", "$value": "{color.semantic.action.primary}" },
      "hover":   { "$type": "color", "$value": "{color.semantic.action.primary-hover}" } },
    "foreground": { "default": { "$type": "color", "$value": "{color.semantic.text.inverse}" } },
    "padding": {
      "x": { "$type": "dimension", "$value": "{dimension.spacing.scale.4}" },
      "y": { "$type": "dimension", "$value": "{dimension.spacing.scale.2}" } },
    "radius": { "$type": "dimension", "$value": "{dimension.radius.md}" }
  } }
}
```

Distribuição: core (~28), semantic (~18), component (~12). Todos alias resolvem, sem ciclo.

---

## 8. Theming

### 8.1. Abordagem por arquivo

Cada tema é um arquivo que substitui a camada semantic. Core compartilhado.

```
tokens/
  core.json
  themes/ (light.json, dark.json, high-contrast.json)
  components/ (button.json)
```

**themes/light.json:**
```json
{ "color": { "semantic": { "$type": "color",
  "text":    { "primary": { "$value": "{color.core.neutral.900}" } },
  "surface": { "primary": { "$value": "{color.core.neutral.0}"   } },
  "action":  { "primary": { "$value": "{color.core.purple.600}"  } } } } }
```

**themes/dark.json:**
```json
{ "color": { "semantic": { "$type": "color",
  "text":    { "primary": { "$value": "{color.core.neutral.0}"   } },
  "surface": { "primary": { "$value": "{color.core.neutral.900}" } },
  "action":  { "primary": { "$value": "{color.core.purple.400}"  } } } } }
```

Build carrega `core + themes/<active> + components/*` e emite CSS com variáveis.

### 8.2. High contrast

Mesmo padrão, valores aumentados de contraste (ver companion `04-accessibility-wcag22.md`):

```json
{ "color": { "semantic": { "$type": "color",
  "text":    { "primary": { "$value": "#000000" } },
  "surface": { "primary": { "$value": "#FFFFFF" } },
  "border":  { "default": { "$value": "#000000" } } } } }
```

### 8.3. Multi brand

Adicione camada **brand** intermediária: `tokens/brands/acme.json`, `tokens/brands/acme-go.json`.

**brands/acme.json:**
```json
{ "color": { "brand": { "$type": "color",
  "primary":   { "$value": "{color.core.purple.600}" },
  "secondary": { "$value": "{color.core.amber.500}" } } } }
```

Semantic aponta para brand: `color.semantic.action.primary => {color.brand.primary}`. Ao trocar a marca no build, toda cadeia atualiza.

### 8.4. CSS vars em runtime

```css
:root, [data-theme="light"] {
  --color-semantic-text-primary: #171717;
  --color-semantic-surface-primary: #FFFFFF;
}
[data-theme="dark"] {
  --color-semantic-text-primary: #FFFFFF;
  --color-semantic-surface-primary: #171717;
}
```

```html
<html data-theme="dark">...</html>
```

Combine com `prefers-color-scheme` para detecção automática:

```css
@media (prefers-color-scheme: dark) {
  :root {
    --color-semantic-text-primary: #FFFFFF;
    --color-semantic-surface-primary: #171717;
  }
}
```

Data attribute dá precedência ao usuário sobre o sistema.

---

## 9. Responsive tokens

A spec 2025.10 não prescreve responsividade. Três abordagens comunitárias.

### 9.1. Tokens separados por breakpoint

```json
{
  "typography": {
    "heading-1": {
      "$type": "typography",
      "base": { "$value": { "fontFamily": "{fontFamily.sans}", "fontSize": { "value": 1.75, "unit": "rem" }, "lineHeight": 1.2 } },
      "md":   { "$value": { "fontFamily": "{fontFamily.sans}", "fontSize": { "value": 2.25, "unit": "rem" }, "lineHeight": 1.2 } },
      "lg":   { "$value": { "fontFamily": "{fontFamily.sans}", "fontSize": { "value": 3,    "unit": "rem" }, "lineHeight": 1.1 } }
    }
  }
}
```

Build emite CSS com media queries. Prós: declarativo. Contras: explosão de tokens.

### 9.2. Função responsive (clamp)

Token único com `clamp()`:

```json
{ "typography": { "heading-1": { "$type": "typography", "$value": { "fontFamily": "{fontFamily.sans}", "fontSize": { "value": "clamp(1.75rem, 3vw + 1rem, 3rem)" }, "lineHeight": 1.2 } } } }
```

`clamp()` não é formalmente suportado (unidades fora de `px`/`rem`). Use via `$extensions` ou override pós build.

### 9.3. Breakpoints como tokens

```json
{ "breakpoint": { "$type": "dimension",
  "sm": { "$value": { "value": 640,  "unit": "px" } },
  "md": { "$value": { "value": 768,  "unit": "px" } },
  "lg": { "$value": { "value": 1024, "unit": "px" } },
  "xl": { "$value": { "value": 1280, "unit": "px" } } } }
```

Breakpoints viram primitivas, media queries ficam no CSS gerado.

### 9.4. Recomendação prática

Combine: breakpoints como tokens (9.3), tokens por breakpoint para typography/spacing (9.1), `clamp()` via `$extensions` em casos específicos (9.2).

---

## 10. Style Dictionary pipeline

Ferramenta de build mais adotada. Versão 4.x suporta spec 2025.10 nativamente.

### 10.1. Instalação

```bash
npm install --save-dev style-dictionary
```

Requer Node.js 18+ em 2026.

### 10.2. Estrutura

```
my-design-system/
  tokens/
    core.json
    themes/ (light.json, dark.json)
    components/ (button.json)
  config.js
  build/
  package.json
```

### 10.3. Config básica

`config.js`:

```js
import StyleDictionary from 'style-dictionary';

const sd = new StyleDictionary({
  source: ['tokens/**/*.json'],
  platforms: {
    css:     { transformGroup: 'css',       buildPath: 'build/css/',     files: [{ destination: 'tokens.css',   format: 'css/variables',          options: { outputReferences: true } }] },
    ios:     { transformGroup: 'ios-swift', buildPath: 'build/ios/',     files: [{ destination: 'Tokens.swift', format: 'ios-swift/class.swift', className: 'Tokens' }] },
    android: { transformGroup: 'android',   buildPath: 'build/android/', files: [{ destination: 'tokens.xml',   format: 'android/resources' }] },
    js:      { transformGroup: 'js',        buildPath: 'build/js/',      files: [{ destination: 'tokens.js',    format: 'javascript/es6' }] }
  }
});

await sd.buildAllPlatforms();
```

### 10.4. Build

`package.json`:
```json
{ "scripts": { "build:tokens": "node config.js" } }
```

```bash
npm run build:tokens
```

### 10.5. Output CSS

```css
:root {
  --color-core-purple-600: #5B21B6;
  --color-semantic-action-primary: var(--color-core-purple-600);
  --button-primary-background-default: var(--color-semantic-action-primary);
  --dimension-spacing-scale-4: 16px;
}
```

`outputReferences: true` preserva cadeia de alias (cascata via `var()`). Permite trocar theme em runtime.

### 10.6. Output Flutter (custom format)

```js
sd.registerFormat({
  name: 'dart/tokens',
  format: ({ dictionary }) => {
    const lines = dictionary.allTokens.map(t => `  static const ${t.name.replace(/-/g, '_')} = "${t.value}";`);
    return `class Tokens {\n${lines.join('\n')}\n}`;
  }
});
```

### 10.7. Multi theme build

```js
const themes = ['light', 'dark', 'high-contrast'];
for (const theme of themes) {
  const sd = new StyleDictionary({
    source: ['tokens/core.json', `tokens/themes/${theme}.json`, 'tokens/components/**/*.json'],
    platforms: { css: { transformGroup: 'css', buildPath: 'build/css/',
      files: [{ destination: `${theme}.css`, format: 'css/variables',
        options: { selector: `[data-theme="${theme}"]`, outputReferences: true } }] } }
  });
  await sd.buildAllPlatforms();
}
```

Output: `light.css`, `dark.css`, `high-contrast.css`.

---

## 11. Tokens Studio plugin (Figma)

Plugin Figma mais adotado para autoria de tokens. Desde 2024 suporta export direto em DTCG.

### 11.1. Workflow

```
[Figma + Tokens Studio] --export JSON DTCG--> [Git branch] --PR+review--> [main] --CI--> [CSS, iOS, Android, JS] --> npm publish
```

### 11.2. Setup Figma

1. Instalar plugin "Tokens Studio for Figma".
2. Criar projeto, configurar provider de sync (GitHub, GitLab, Bitbucket, Azure DevOps).
3. Apontar para repo e path (`tokens/`).
4. Push inicial dos tokens existentes.

### 11.3. Estrutura de "sets"

Organização recomendada:

- `global` (core, sempre ativo)
- `theme/light`, `theme/dark` (semantic, ativável)
- `brand/acme` (ativável por brand)
- `components/button` (sempre ativo)

Temas combinam sets. "Acme Light" ativa: `global + theme/light + brand/acme + components/*`.

### 11.4. Push e pull

- **Push**: designer edita, "Push to Git" abre PR.
- **Pull**: designer traz mudanças de devs.

Boas práticas: não editar em paralelo (Figma vs editor), revisar PRs com CI passando, branch protection em `main`.

### 11.5. Aplicação

Designer seleciona frame, clica token no painel, valor aplica como fill. Troca de tema propaga globalmente.

### 11.6. Limitações

- Usa extensões proprietárias (`studio.tokens.*`).
- Alguns compostos (gradient multi stop) podem não viajar 100%.
- Sync falha em referências quebradas.

Contorno: rodar `cobalt validate` em CI.

---

## 12. Validation e linting

### 12.1. JSON Schema

Spec publica schema oficial. Valida: campos reservados, tipos consistentes, alias resolvíveis.

Uso via `ajv`:

```bash
npm install --save-dev ajv ajv-formats
```

```js
import Ajv from 'ajv';
import schema from './dtcg-schema.json' assert { type: 'json' };
import tokens from './tokens/core.json'  assert { type: 'json' };
const ajv = new Ajv({ allErrors: true });
const validate = ajv.compile(schema);
if (!validate(tokens)) { console.error(validate.errors); process.exit(1); }
```

### 12.2. Cobalt UI (CLI)

```bash
npm install --save-dev @cobalt-ui/cli
npx co check tokens/*.json
```

Valida, detecta ciclos, alias não resolvíveis, tipos inválidos.

### 12.3. TypeScript types gerados

Style Dictionary e Cobalt UI emitem `.d.ts` com nomes como union types:

```ts
export type TokenName =
  | 'color.core.purple.600'
  | 'color.semantic.action.primary'
  | 'dimension.spacing.scale.4';

export declare const tokens: Record<TokenName, string>;
```

Ganho: autocomplete, erro de build em token inexistente.

### 12.4. Regras customizadas

| Regra | Violação | Severidade |
|-------|----------|------------|
| Naming consistente | `Color.Brand_Primary` | Error |
| Profundidade máxima | 6+ níveis | Warning |
| Core não referencia outro | `core.foo => {core.bar}` | Error |
| Semantic deve referenciar core | `semantic.action.primary: "#ABC"` | Warning |
| Component deve referenciar semantic/core | `button.bg: "#ABC"` | Warning |
| Valor no range | `fontWeight: 1500` | Error |
| Contraste WCAG | `text.primary` vs `surface.primary` < 4.5:1 | Warning |

Ferramentas: `stylelint-design-tokens`, `@tokens-studio/token-linter`, scripts custom.

### 12.5. CI

```yaml
name: Validate Tokens
on: [pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npx co check tokens/**/*.json
      - run: npm run build:tokens
      - run: npm run test:tokens
```

---

## 13. Versionamento de tokens

Tokens são contrato público. Semver disciplina o que é breaking vs additive.

### 13.1. Semver aplicado

| Tipo | Quando | Exemplos |
|------|--------|----------|
| Major | Incompatível | Renomear ou remover token, trocar `$type`, mudar estrutura |
| Minor | Adição compatível | Novo token, novo tema, nova camada |
| Patch | Ajuste sem API | Valor de core mantendo nome, typo em `$description` |

### 13.2. Breaking changes comuns

- Remover `color.action.primary`.
- Renomear `button.background` para `button.bg`.
- Mudar `dimension.spacing.md` de `16px` para `20px` (muda visual).
- Trocar `$type` de um token.

### 13.3. Additive changes (minor)

- Adicionar `color.status.info`.
- Novo tema `theme/high-contrast`.
- Novo componente `card.*`.

### 13.4. Deprecation com migration

1. Marcar deprecated via `$extensions`:

```json
{ "button": { "background": {
  "$type": "color",
  "$value": "{color.semantic.action.primary}",
  "$description": "DEPRECATED, use button.primary.background.default.",
  "$extensions": { "org.acme.tokens": {
    "deprecated": true, "deprecatedSince": "1.4.0",
    "replacedBy": "button.primary.background.default", "removeIn": "2.0.0" } } } } }
```

2. Emitir warning no build quando consumers usam.
3. Publicar changelog com migration step.
4. Remover só no próximo major.

### 13.5. Changelog (Keep a Changelog)

```md
## [2.0.0] - 2026-07-15

### Removed
- `button.background` (deprecated desde 1.4.0).

### Added
- Novo tema `theme/high-contrast`.

## [1.5.0] - 2026-05-01

### Added
- Token `color.status.info`.
```

### 13.6. Distribuição

- npm: `@acme/tokens` (semver respeitado, consumers em `^1.0.0`).
- Git tag: `v1.5.0` (signed).
- CDN: URL immutable por versão.

---

## 14. Integrações

### 14.1. Comparativo

| Framework | Forma de consumo | Fonte | DTCG nativo |
|-----------|-------------------|-------|--------------|
| Tailwind CSS v4 | `@theme inline` + CSS vars | `tokens.css` gerado | Não (mapeamento) |
| shadcn/ui | CSS vars em `globals.css` | `tokens.css` | Não (convenção) |
| Material 3 | SDK + Figma Variables | `tokens.json` próprio | Parcial |
| Fluent 2 | `@fluentui/react-theme` | JSON proprietário | Parcial |
| Chakra UI v3 | `theme.ts` | Conversão JS | Não |
| Radix Themes | CSS vars | `tokens.css` | Não (convenção) |

### 14.2. Tailwind CSS v4

Tailwind v4 introduziu `@theme` para declarar tokens em CSS. Importe o `tokens.css` e mapeie:

```css
@import "tailwindcss";
@import "./tokens.css";

@theme inline {
  --color-brand-primary: var(--color-semantic-action-primary);
  --color-surface: var(--color-semantic-surface-primary);
  --spacing-4: var(--dimension-spacing-scale-4);
  --radius-md: var(--dimension-radius-md);
  --font-sans: var(--font-family-sans);
}
```

Classes geradas (`bg-brand-primary`, `p-4`, `rounded-md`) resolvem para seus tokens.

### 14.3. shadcn/ui

shadcn usa convenção própria (OKLCH a partir de shadcn v2), compatível via mapeamento:

```css
:root {
  --background:          var(--color-semantic-surface-primary);
  --foreground:          var(--color-semantic-text-primary);
  --primary:             var(--color-semantic-action-primary);
  --primary-foreground:  var(--color-semantic-text-inverse);
  --border:              var(--color-semantic-border-default);
  --radius:              var(--dimension-radius-md);
}
```

Ver companion `08-shadcn-integration.md`.

### 14.4. Material 3

Material 3 usa taxonomia própria. Mapeamento:

| Material 3 | DTCG equivalente |
|------------|-------------------|
| `md.sys.color.primary` | `color.semantic.action.primary` |
| `md.sys.color.on-primary` | `color.semantic.text.inverse` |
| `md.sys.color.surface` | `color.semantic.surface.primary` |
| `md.sys.color.on-surface` | `color.semantic.text.primary` |

Material Theme Builder exporta JSON convertível para DTCG via script.

### 14.5. Fluent 2

Fluent UI usa `tokens.ts` com naming `colorBrandBackground`. Similar a Material, mapeamento 1:1 semântico. Convert script trivial.

### 14.6. Qual escolher

- **Produto web novo**: DTCG + Style Dictionary + Tailwind v4 + shadcn. Máxima liberdade, mínimo vendor lock.
- **Android nativo**: Material 3 como fonte, exportar para DTCG para web marketing e iOS.
- **Windows enterprise**: Fluent 2 como fonte.
- **DS corporativo multi produto**: DTCG sempre canônico, adapters para cada alvo.

---

## 15. Anti patterns

### 15.1. Tokens arbitrários

Novos tokens entram no repo sem revisão, valores únicos usados em 1 lugar.

```json
{ "color": { "misc": { "login-button-bg-tuesday-special": { "$value": "#4A90E2" } } } }
```

Fix: revisar PRs. Novos core tokens exigem justificativa.

### 15.2. Nomeação inconsistente

```json
{ "Color": { "BrandPrimary": { "$value": "#5B21B6" } }, "color": { "brand-secondary": { "$value": "#F59E0B" } } }
```

Fix: escolher convenção no onboarding, linting bloqueia desvios.

### 15.3. Valores hard coded

```tsx
<div style={{ background: '#5B21B6', padding: '16px', borderRadius: '8px' }}>
```

Fix: usar classes de token.
```tsx
<div className="bg-brand-primary p-4 rounded-md">
```

Linting rules (`no-hardcoded-colors`, `no-hardcoded-spacing`) em ESLint/Stylelint.

### 15.4. Over nesting

```
color.palette.extended.tones.neutral.light.background.subtle.primary
```

Fix: máximo 5 níveis. Caminhos maiores indicam taxonomia errada.

### 15.5. Cor como string mágica

`<Button color="#5B21B6" />`. Fix: componente aceita apenas variantes nomeadas (`<Button variant="primary" />`).

### 15.6. Semantic sem alias

Ruim: `{ "color": { "semantic": { "action": { "primary": { "$type": "color", "$value": "#5B21B6" } } } } }`.

Fix: sempre alias para core: `{ ..., "$value": "{color.core.purple.600}" }`.

### 15.7. Component pulando semantic

Ruim: `{ "button": { "primary": { "background": { "$value": "{color.core.purple.600}" } } } }`.

Fix: component => semantic => core. `{ ..., "$value": "{color.semantic.action.primary}" }`.

### 15.8. Um token por tela

`login.page.background`, `signup.page.background`, `dashboard.page.background` com mesmo valor.

Fix: usar `color.semantic.surface.primary`.

### 15.9. Pleonasmo semântico

`color-color-primary`, `font-font-size-base`, `spacing-spacing-md`.

Fix: grupo pai já carrega categoria. `color.primary`, `font.size.base`.

### 15.10. Misturar intenção e valor

`color.purple-primary-cta-hover-lg-desktop`.

Fix: separar em camadas. Core descreve paleta, semantic descreve intenção, component descreve uso.

---

## 16. FAQ

### 16.1. Quando promover de core para semantic?

Quando um core passa a ter papel semântico reutilizado em múltiplos contextos. Regra: 3+ componentes usam o mesmo core para a mesma intenção, crie semantic e redirecione.

### 16.2. Devo ter um token por tela?

Não. Tela não é categoria semântica estável. Use semantic (`surface.primary`, `text.primary`). Token por tela só quando há requisito visual genuinamente único.

### 16.3. Como lidar com exceções one off?

Em ordem de preferência: (1) reutilizar token existente mesmo se não exato, (2) criar component token com alias para core mais próximo, documentando em `$description`, (3) valor literal inline (última opção), comentado como "exception".

### 16.4. Quando alias vs valor direto?

Core: valor direto (é primitiva). Semantic: sempre alias. Component: alias para semantic (preferencial) ou core (aceitável). Protótipos podem ter literais no component, devem virar alias antes de produção.

### 16.5. Posso ter tokens sem `$type`?

Tecnicamente sim (herança do grupo pai). Recomendação: sempre declarar no grupo raiz. Mais legível, evita ambiguidade.

### 16.6. Como versionar quando muitos tokens mudam de uma vez?

Agrupe em major release com: changelog detalhado, migration guide (script find and replace quando possível), codemod (jscodeshift, ts morph) se afeta código TS/JSX, dual emit (old + new) por 1 minor antes de remover.

### 16.7. Como garantir contraste em todos os temas?

CI roda teste de contraste em pares críticos. Thresholds: 4.5:1 body text, 3:1 large text e UI (WCAG 2.2 AA). Ferramentas: `polished`, `color2k`, `wcag-contrast`.

### 16.8. Tokens para dark mode precisam ser invertidos?

Não mecanicamente. Dark mode é design próprio. Na prática: `text.primary` neutral.900 vira neutral.0, `surface.primary` neutral.0 vira neutral.900, `action.primary` purple.600 vira purple.400 (mais claro para contraste).

### 16.9. Posso usar unicode em chaves?

Tecnicamente sim, mas não recomendado. Parsers, CLIs e editores tratam unicode de forma inconsistente. Use ASCII puro.

### 16.10. Quando `$extensions` vs criar fork?

Sempre `$extensions`. Forks fragmentam a comunidade. Use namespace reverso (`com.company.feature`), documente schema interno, ferramentas desconhecidas devem ignorar.

### 16.11. Como migrar tokens legados gradualmente?

Estratégia "strangler fig": (1) publicar novo pacote DTCG (`@acme/tokens-v2`), (2) build emite old e new lado a lado, (3) migrar consumers 1 a 1 (mais novo primeiro), (4) após N meses de uso zero, remover legado.

### 16.12. Tokens devem ficar no mesmo repo do produto?

Depende: 1 produto, monorepo OK. 2 a 5 produtos, repo separado em npm privado. Enterprise multi produto, repo separado com governança dedicada (ver `03-ds-governance.md`).

### 16.13. Posso usar YAML ao invés de JSON?

Spec define apenas JSON como formato normativo. Tokens Studio e algumas ferramentas aceitam YAML e convertem. Se adotar YAML, garanta que build emite JSON canônico.

### 16.14. Como responsive em composite types (typography)?

Variantes por breakpoint dentro do composite (ver seção 9.1). Build emite media queries.

### 16.15. DTCG vai virar W3C Recommendation?

Pode. Para virar Recommendation, teria que migrar para Working Group formal (processo longo: Candidate, Proposed, etc.). Status em abril 2026: ainda Community Group, com adoção em produção madura.

---

## Referências e próximos passos

- Spec oficial: `designtokens.org/tr/2025.10/format/`
- Site do grupo: `designtokens.org`
- Repo GitHub: `github.com/design-tokens/community-group`
- Blog: `w3.org/community/design-tokens/blog`
- Style Dictionary: `styledictionary.com`
- Tokens Studio docs: `tokens.studio/docs`

Companions relacionados:

- `02-atomic-design-playbook.md`: arquitetura de componentes (átomo a página).
- `03-ds-governance.md`: ciclo de vida, review, approval.
- `04-accessibility-wcag22.md`: contraste, focus, motion safe.
- `06-brand-system-blueprint.md`: marca como fonte dos tokens de maior nível.
- `08-shadcn-integration.md`: integração concreta com shadcn/ui.
- `09-handoff-to-code.md`: Figma => token => código.

---

Companion fechado. Quando DTCG publicar nova versão (2026.xx adiante), revisar este documento para refletir novos tipos e ajustes.