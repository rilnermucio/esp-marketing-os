# 04. Accessibility WCAG 2.2 Deep Reference (2026)

> Parte da stack de companions do `design-agent` (v4.0).
> Referência aplicada sobre WCAG 2.2: princípios POUR, nove success criteria novos, checklists por componente, keyboard contracts, ARIA patterns, testing toolkit e automação em CI.

**Quando consultar:** ao definir nível de conformância (A, AA ou AAA), ao implementar componente que precisa passar em audit, ao configurar pipeline de testes automatizados, ao revisar focus indicators, ao desenhar autenticação sem cognitive test, ao decidir target size, ou ao diagnosticar issues reportados por usuários de screen reader.

**Pré-requisitos:** leitura prévia de `references/design/01-tokens-w3c-spec.md` (tokens e contraste) e `references/design/02-atomic-design-playbook.md` (composição). Acessibilidade é camada transversal.

---

## Índice

1. WCAG 2.2 o que mudou vs 2.1
2. Princípios POUR
3. Níveis A, AA, AAA
4. Contraste completo
5. Focus indicators (2.4.11, 2.4.12, 2.4.13)
6. Target size (2.5.8)
7. Dragging movements (2.5.7)
8. Consistent help (3.2.6)
9. Redundant entry (3.3.7)
10. Accessible authentication (3.3.8, 3.3.9)
11. Checklist Button
12. Checklist Input e Form
13. Checklist Modal e Dialog
14. Checklist Table e DataGrid
15. Checklist Navigation e Menu
16. Checklist Toast e Notification
17. ARIA patterns essenciais
18. Keyboard navigation
19. Screen reader behavior
20. Cognitive a11y
21. Motor a11y
22. Testing toolkit
23. Automated testing in CI
24. Top 20 common failures e fixes
25. Role-based checklists

---

## 1. WCAG 2.2 o que mudou vs 2.1

WCAG 2.2 foi publicada pelo W3C em outubro de 2023 como Recommendation. Adiciona nove success criteria sobre WCAG 2.1 e remove um (4.1.1 Parsing, declarado obsoleto porque parsing tolerante dos browsers tornou a regra redundante). Critérios existentes de 2.0 e 2.1 permanecem. Não há mudança em POUR nem nos níveis.

### 1.1. Os nove novos success criteria

| Nível | Código | Nome | Foco |
|-------|--------|------|------|
| A | 2.5.7 | Dragging Movements | Alternativa single-pointer para drag |
| A | 3.3.8 | Accessible Authentication (Minimum) | Sem cognitive test obrigatório |
| AA | 2.4.11 | Focus Not Obscured (Minimum) | Item focado nunca totalmente escondido |
| AA | 2.5.8 | Target Size (Minimum) | Alvos táteis com 24x24 CSS pixels |
| AA | 3.2.6 | Consistent Help | Mecanismo de ajuda em posição consistente |
| AA | 3.3.7 | Redundant Entry | Não pedir duas vezes a mesma informação |
| AAA | 2.4.12 | Focus Not Obscured (Enhanced) | Item focado nunca parcialmente escondido |
| AAA | 2.4.13 | Focus Appearance | Focus ring com tamanho e contraste mínimos |
| AAA | 3.3.9 | Accessible Authentication (Enhanced) | Autenticação sem digitação obrigatória |

Dois critérios AAA (apesar do nome "enhanced" em alguns): `2.4.12` e `3.3.9`. O `2.4.13` subiu para AAA na versão final.

### 1.2. Migração 2.1 para 2.2

Para produto já em 2.1 AA, passar para 2.2 AA significa implementar quatro novos AA (2.4.11, 2.5.8, 3.2.6, 3.3.7) e dois novos A (2.5.7, 3.3.8). Tipicamente envolve: revisar drag-and-drop, adicionar target size mínimo em ícones, mover help link para posição consistente, evitar re-digitar email em fluxos multi-step, oferecer login sem captcha obrigatório.

---

## 2. Princípios POUR

Todos os critérios são filhos de um dos quatro princípios.

**Perceivable.** Informação precisa ser percebível. Cobre alt em imagens, legendas em vídeos, ordem de leitura, contraste, redimensionamento sem quebra. Falha típica: ícone-only button sem aria-label, logo o SR anuncia só "button".

**Operable.** Componentes precisam ser operáveis. Cobre keyboard accessibility, tempo suficiente, evitar flash, skip links, modalidades de input diversas. Falha típica: carrossel que só avança com swipe e não tem botões.

**Understandable.** UI precisa ser compreensível. Cobre legibilidade (lang declarado), previsibilidade, ajuda na entrada (labels, mensagens acionáveis, prevenção de erros). Falha típica: formulário que submete ao perder foco.

**Robust.** Conteúdo robusto o suficiente para assistive tech. Cobre markup válido, name-role-value corretos, status messages em live regions. Falha típica: custom dropdown com `<div>` sem `role="combobox"`.

### 2.1. POUR aplicado à decisão

Antes de considerar um componente pronto: Perceivable (estado em múltiplas modalidades), Operable (sem mouse), Understandable (labels e comportamentos previsíveis), Robust (semântica correta para assistive tech). Qualquer "não" é trabalho pendente.

---

## 3. Níveis A, AA, AAA

WCAG define três níveis cumulativos. AA inclui A, AAA inclui tudo.

**Nível A** cobre barreiras fundamentais (30 critérios em 2.2). Exemplos: conteúdo não textual sem alternativa (1.1.1), teclado inacessível (2.1.1), idioma não declarado (3.1.1). Sozinho é considerado piso inadequado pela comunidade.

**Nível AA** é o alvo comercial (64 critérios totais). Exigido por ADA (EUA, via interpretação judicial), EN 301 549 (UE), AODA (Ontario), LBI no Brasil via Decreto 9.522/2018. Inclui contraste 4.5:1, focus visible, headings estruturados, labels, consistent navigation.

**Nível AAA** é ideal, raramente alcançado em sites completos (87 critérios totais). W3C diz que "não é recomendado exigir AAA para sites inteiros porque alguns critérios são incompatíveis com certos conteúdos". Inclui contraste 7:1, sign language, sem timing, leitura nível 8ª série.

### 3.1. Escolha por contexto

| Contexto | Nível |
|----------|-------|
| Governo federal/estadual | 2.2 AA (legal) |
| SaaS B2B | 2.2 AA (enterprise exige) |
| E-commerce | 2.2 AA (risco ADA) |
| Educação infantil | 2.2 AA + seleção AAA |
| Serviço público crítico | 2.2 AA + AAA onde aplicável |
| Produto interno | 2.2 AA (colegas podem ter deficiência) |

---

## 4. Contraste completo

Contraste é razão de luminância entre frente e fundo, calculada por `(L1 + 0.05) / (L2 + 0.05)`.

### 4.1. Requisitos

| Elemento | AA | AAA | Observação |
|----------|----|----|------------|
| Texto normal | 4.5:1 | 7:1 | Até 18px regular ou 14px bold |
| Texto large | 3:1 | 4.5:1 | 24px regular ou 18.66px bold |
| UI components | 3:1 | n/a | Borda de input, toggle, focus ring |
| Non-text essential | 3:1 | n/a | Ícones informativos, gráficos |
| Texto desabilitado | Exempt | Exempt | Estados inativos |
| Logo | Exempt | Exempt | Isento |

### 4.2. Large text

Large text equivale a 18 pt ou 14 pt bold. Em CSS, aproximadamente 24px regular ou 18.66px bold. Num sistema com body 16px, só h3 para cima tipicamente atinge large.

### 4.3. UI components e non-text

SC 1.4.11 (AA) exige 3:1 para elementos que comunicam estado ou boundary: borda de input vs fundo, checkbox unchecked, toggle off vs on, progress bar, divisor funcional.

### 4.4. Ferramentas

WebAIM Contrast Checker (web), Chrome DevTools (inline), Stark e Able (Figma), axe DevTools, Color Oracle (simulação daltonismo).

### 4.5. Esquecidos frequentes

Placeholder cinza #AAA sobre branco dá 2.3:1 e falha. Regra: placeholder é texto, precisa 4.5:1 se comunica info essencial.

Link hover state: se muda só cor e novo tom não bate 4.5:1, falha. Manter contraste ou adicionar underline.

Badge sobre foto: forçar fundo opaco ou overlay para garantir contraste em imagens variadas.

---

## 5. Focus indicators

WCAG 2.2 endereça focus de forma cirúrgica em três critérios novos, além do 2.4.7 (Focus Visible, AA) que já existia.

### 5.1. 2.4.11 Focus Not Obscured (Minimum), AA

Elemento focado via teclado não pode estar totalmente coberto por conteúdo da página (sticky header, cookie banner, chat widget).

Fix via CSS para sticky header:

```css
html {
  scroll-padding-top: 80px;
}
*:focus-visible {
  scroll-margin-top: 80px;
}
```

### 5.2. 2.4.12 Focus Not Obscured (Enhanced), AAA

Nenhuma parte do elemento focado pode estar obscurecida. Se qualquer pixel do focus ring fica atrás do header, falha. Aplicável a produtos críticos ou quando AAA é alvo.

### 5.3. 2.4.13 Focus Appearance, AAA

Três métricas:

1. Área mínima: perímetro com espessura >= 2px ou área equivalente.
2. Contraste indicador: razão >= 3:1 focado vs não-focado.
3. Contraste vs adjacente: 3:1 entre indicador e fundo.

Implementação:

```css
button:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
  border-radius: 4px;
}
```

Evitar: `outline: none` sem substituto, focus ring 1px (falha área), ring cinza claro (falha contraste).

### 5.4. Focus management em SPAs

Em SPAs, ao trocar de rota o foco fica onde estava, o que confunde SR users. Padrão correto: mover foco para o `h1` da nova view.

```javascript
const main = document.querySelector('main h1');
if (main) {
  main.setAttribute('tabindex', '-1');
  main.focus();
}
```

Em modais, foco vai para dentro ao abrir e retorna ao trigger ao fechar. Detalhe na seção 13.

---

## 6. Target size

SC 2.5.8 (AA) exige targets interativos com pelo menos 24x24 CSS pixels.

### 6.1. O que conta

Qualquer elemento acionável: button, link, checkbox, radio, slider thumb, icon button, tab, close button, nav item.

### 6.2. Como medir

Bounding box do target, não só o ícone. Botão com ícone 16x16 em container 32x32 com padding passa, porque o clickable area é 32x32.

### 6.3. Exceções

1. Spacing: distância >= 24px entre centros de targets adjacentes.
2. Equivalent: existe outro target com mesma função e tamanho adequado.
3. Inline: link dentro de parágrafo está isento.
4. User agent default: tamanho determinado pelo browser sem CSS custom.
5. Essential: tamanho é essencial (pin em mapa marcando ponto exato).

### 6.4. Casos comuns

Ícone X em modal de 16x16 frequentemente falha. Aumentar container para 40x40 (recomendado). Checkbox custom 16x16 ganha padding invisível no label para 24x24 efetivo. Links em cells de tabela são inline, isentos.

### 6.5. Recomendação

Mirar 40x40 (iOS HIG e Material 3) em vez do mínimo legal. Users com tremor, dedos grandes e mobile beneficiam.

```css
.icon-button {
  width: 40px;
  height: 40px;
  padding: 8px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
```

---

## 7. Dragging movements

SC 2.5.7 (AA) exige que funcionalidades com drag tenham alternativa single-pointer.

### 7.1. Onde aparece

Kanban, sliders, file upload drag-and-drop, reordenação de lista, mapas (pan), image crop.

### 7.2. Alternativas

1. Botões stepper (em slider: `-/+` com incremento fixo).
2. Menu de ações (em Kanban: menu "Mover para...").
3. Input numérico (slider com campo editável).
4. Botão explícito "Enviar arquivo" além da drop zone.
5. Setas do teclado em slider.

### 7.3. Exceção

Dragging é essencial e não há alternativa viável: desenho livre, assinatura. Nesses casos, critério não-aplicável.

### 7.4. Kanban acessível

```html
<div role="group" aria-label="Card Revisar PR 42">
  <h3>Revisar PR 42</h3>
  <button aria-label="Mover card" aria-haspopup="menu" aria-expanded="false">
    Mover
  </button>
  <ul role="menu" hidden>
    <li role="menuitem"><button>Para To Do</button></li>
    <li role="menuitem"><button>Para In Progress</button></li>
    <li role="menuitem"><button>Para Done</button></li>
  </ul>
</div>
```

Drag continua para mouse users, menu funciona para keyboard e SR.

---

## 8. Consistent help

SC 3.2.6 (AA) exige que mecanismos de ajuda apareçam em ordem consistente entre páginas.

Cobertura: contato humano (phone, email), contato por mensagem (form, chat), self-help (FAQ, busca), automatizado (chatbot, IVR).

Regra: se "Ajuda" fica no canto inferior direito em uma página, fica lá em todas. Exceção: mudanças iniciadas pelo user (fechar widget) são aceitas.

Implementação: colocar componentes de help em layout compartilhado (root layout em Next.js ou Remix) garante consistência automaticamente.

---

## 9. Redundant entry

SC 3.3.7 (AA) exige que informação inserida na mesma sessão não seja re-pedida.

### 9.1. Cenários

Checkout pedindo endereço em step 2 e de novo em step 4 falha. Cadastro com endereço de entrega e cobrança pede checkbox "mesmo que entrega".

### 9.2. Soluções

1. Auto-fill a partir de state/sessão.
2. Checkbox "usar mesma informação".
3. Dropdown com valores já inseridos.
4. Copy button entre campos.

### 9.3. Exceção essencial

Confirmação de senha no cadastro é essencial (evita typo). Revalidação em ação de alto risco (deletar conta) é essencial.

### 9.4. React

```jsx
const [sameAsShipping, setSameAsShipping] = useState(false);

<label>
  <input
    type="checkbox"
    checked={sameAsShipping}
    onChange={(e) => {
      setSameAsShipping(e.target.checked);
      if (e.target.checked) setBilling(shipping);
    }}
  />
  Usar mesmo endereco de entrega
</label>
```

---

## 10. Accessible authentication

Dois critérios: 3.3.8 (Minimum, AA) e 3.3.9 (Enhanced, AAA).

### 10.1. 3.3.8 Minimum, AA

Autenticação não pode depender de cognitive function test. Proibidos: memorizar sequência (pattern lock), transcrever caracteres de imagem (CAPTCHA clássico), cálculo, puzzle.

Aceitáveis:

- Paste de password (não bloquear colar)
- Password manager integration (autofill)
- Magic link via email
- Biometria (Face ID, Touch ID)
- Copy-paste de OTP

### 10.2. 3.3.9 Enhanced, AAA

Nenhum cognitive test em nenhum ponto, mesmo com alternativa. Na prática: passkeys/WebAuthn ou federated login sem steps extras.

### 10.3. CAPTCHA

CAPTCHA tradicional viola 3.3.8 quando é único mecanismo. Alternativas: reCAPTCHA v3 invisible (score-based), audio CAPTCHA como alternativa, hCaptcha Privacy Pass, passkeys.

### 10.4. Magic link

User digita email, servidor envia link único, user clica, logado. Sem password ou captcha. Atende 3.3.8 e 3.3.9 naturalmente.

---

## 11. Checklist Button

### 11.1. Markup base

```html
<button type="button" aria-label="Fechar modal">
  <svg aria-hidden="true" focusable="false"><!-- X --></svg>
</button>
```

### 11.2. Regras

- `<button>`, nunca `<div onClick>`.
- `type="button"` em forms, exceto submit explícito.
- `aria-label` obrigatório em icon-only.
- `aria-hidden="true"` e `focusable="false"` em SVG interno.
- Estado disabled via prop `disabled`, não via styling.
- Loading com `aria-busy="true"` e live region para anunciar.

### 11.3. Keyboard

Tab foca, Enter/Space aciona. Focus visible atende 2.4.11, idealmente 2.4.13.

### 11.4. Target size

Mínimo 24x24, recomendado 40x40.

### 11.5. Screen reader

NVDA/VoiceOver anunciam "Fechar modal, botão". Toggle adiciona `aria-expanded`, menu trigger adiciona `aria-haspopup`.

### 11.6. Estados

Loading:

```html
<button aria-busy="true" disabled>
  <span aria-hidden="true">Salvando...</span>
  <span class="sr-only">Salvando, aguarde</span>
</button>
```

Toggle com `aria-pressed`:

```html
<button aria-pressed="false" onClick={toggle}>Curtir</button>
```

`aria-pressed` é para toggle buttons; `aria-expanded` é para disclosure.

---

## 12. Checklist Input e Form

### 12.1. Markup

```html
<div class="field">
  <label for="email">Email</label>
  <input
    id="email"
    type="email"
    name="email"
    autocomplete="email"
    required
    aria-describedby="email-hint email-error"
    aria-invalid="false"
  >
  <p id="email-hint" class="hint">Usaremos para enviar confirmacao.</p>
  <p id="email-error" role="alert" hidden>Email invalido.</p>
</div>
```

### 12.2. Regras

- Label explícito via `for`/`id`. Placeholder não substitui label.
- `autocomplete` adequado (valores do HTML spec).
- `aria-describedby` aponta para hint e erro.
- `aria-invalid="true"` em validação falha.
- Erro em `role="alert"` para ser anunciado automaticamente.
- `required` usa atributo nativo.

### 12.3. Keyboard

Tab foca, Esc em combobox fecha lista, Enter submete form por default.

### 12.4. Validação

Validar ao submeter (não a cada keystroke). Mover foco para primeiro erro.

```javascript
form.addEventListener('submit', (e) => {
  e.preventDefault();
  const firstError = form.querySelector('[aria-invalid="true"]');
  if (firstError) firstError.focus();
});
```

### 12.5. SR expectations

Ao focar input com erro: "Email, email invalido, invalido, campo obrigatorio". SR anuncia label, valor, invalid e required.

---

## 13. Checklist Modal e Dialog

### 13.1. Markup

```html
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  aria-describedby="dialog-desc"
>
  <h2 id="dialog-title">Confirmar exclusao</h2>
  <p id="dialog-desc">Esta acao nao pode ser desfeita.</p>
  <button type="button">Cancelar</button>
  <button type="button">Confirmar</button>
</div>
```

### 13.2. Focus management

Ao abrir: salvar trigger, mover foco para primeiro focável (ou h2 com `tabindex="-1"`), trap Tab dentro.

Ao fechar: retornar foco para trigger salvo.

```javascript
const trigger = document.activeElement;
openDialog();
dialog.querySelector('button')?.focus();

// Ao fechar
closeDialog();
trigger?.focus();
```

### 13.3. Keyboard

Esc fecha (crítico), Tab circula dentro, Enter confirma.

### 13.4. Screen reader

Ao abrir anuncia: "Confirmar exclusao, dialogo, esta acao nao pode ser desfeita, botao Cancelar". `aria-labelledby` garante título, `aria-describedby` dá contexto, `aria-modal="true"` bloqueia conteúdo de fora.

### 13.5. Conteúdo de fora

Recomendado aplicar `inert` no conteúdo de fora. Impede tab escapar.

```html
<main inert>...</main>
<div role="dialog" aria-modal="true">...</div>
```

### 13.6. Alert dialog

Confirmações destrutivas usam `role="alertdialog"` em vez de `dialog`.

---

## 14. Checklist Table e DataGrid

### 14.1. Table simples

```html
<table>
  <caption>Pedidos do mes</caption>
  <thead>
    <tr>
      <th scope="col">ID</th>
      <th scope="col">Cliente</th>
      <th scope="col">Valor</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">001</th>
      <td>Ana Silva</td>
      <td>R$ 1.200</td>
    </tr>
  </tbody>
</table>
```

### 14.2. Regras

- `<caption>` descreve a tabela.
- `<th scope="col">` em cabeçalhos de coluna.
- `<th scope="row">` na primeira célula de cada linha quando faz sentido.
- Não usar table para layout.

### 14.3. Sorting

```html
<th scope="col" aria-sort="ascending">
  <button type="button">Cliente</button>
</th>
```

Valores `aria-sort`: `ascending`, `descending`, `none`, `other`.

### 14.4. DataGrid

Para grids com editing, seleção múltipla, resize, usar `role="grid"` com padrão ARIA APG: `row`, `gridcell`, `columnheader`, `rowheader`. Navegação por setas entre cells. Tab foca grid, setas movem dentro.

```html
<table role="grid" aria-label="Usuarios">
  <tr role="row">
    <th role="columnheader">Nome</th>
    <th role="columnheader">Email</th>
  </tr>
  <tr role="row">
    <td role="gridcell" tabindex="0">Ana</td>
    <td role="gridcell" tabindex="-1">ana@ex.com</td>
  </tr>
</table>
```

### 14.5. SR em table

NVDA anuncia ao entrar em cell: "Cliente, Ana Silva, linha 1, coluna 2". JAWS tem modo de tabela com feedback dimensional.

---

## 15. Checklist Navigation e Menu

### 15.1. Landmarks

```html
<header>
  <a href="#main" class="skip-link">Pular para conteudo</a>
</header>
<nav aria-label="Principal">
  <ul>
    <li><a href="/" aria-current="page">Home</a></li>
    <li><a href="/sobre">Sobre</a></li>
  </ul>
</nav>
<main id="main">...</main>
```

### 15.2. Regras

- `<nav>` para navegação principal.
- `aria-label` distingue múltiplas navs ("Principal", "Rodape", "Breadcrumb").
- `aria-current="page"` marca item ativo.
- Skip link permite pular navegação.

### 15.3. Skip link

```css
.skip-link { position: absolute; left: -9999px; }
.skip-link:focus { position: static; left: auto; }
```

Invisível até receber foco. Primeiro Tab revela.

### 15.4. Menu disclosure

```html
<button aria-expanded="false" aria-controls="nav-menu">Menu</button>
<ul id="nav-menu" hidden>
  <li><a href="/">Home</a></li>
</ul>
```

### 15.5. Menu real (role="menu")

Distinção chave: link em "menu" não é `role="menu"`. `role="menu"` é para ações (contexto, dropdown de operações). Nav primária usa `<nav>` com links.

```html
<button aria-haspopup="menu" aria-expanded="false">Mais</button>
<ul role="menu" hidden>
  <li role="menuitem"><button>Editar</button></li>
  <li role="menuitem"><button>Excluir</button></li>
</ul>
```

Setas cima/baixo navegam, Esc fecha, Enter/Space aciona.

### 15.6. Breadcrumb

```html
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/blog">Blog</a></li>
    <li><span aria-current="page">Artigo</span></li>
  </ol>
</nav>
```

---

## 16. Checklist Toast e Notification

### 16.1. Informativo

```html
<div role="status" aria-live="polite" aria-atomic="true">
  Pedido salvo com sucesso.
</div>
```

### 16.2. Erro

```html
<div role="alert" aria-live="assertive" aria-atomic="true">
  Erro ao salvar. Tente novamente.
</div>
```

### 16.3. Regras

- `role="status"` para informativos.
- `role="alert"` para erros.
- `aria-live="polite"` anuncia quando SR terminar.
- `aria-live="assertive"` interrompe (usar com moderação).
- `aria-atomic="true"` lê container inteiro.

### 16.4. Dismissibility

Botão de fechar focável e >= 24x24. Autodismiss dispara SC 2.2.1 (Timing Adjustable): permitir pausar ou estender.

### 16.5. Múltiplos toasts

Container estático com `aria-live` e injetar children dinamicamente. Criar/destruir container impede anúncio.

```html
<div id="toast-region" aria-live="polite" aria-atomic="false">
  <!-- toasts injetados -->
</div>
```

### 16.6. SR behavior

Polite: SR termina frase, depois anuncia "Pedido salvo". Assertive: interrompe imediatamente.

---

## 17. ARIA patterns essenciais

"No ARIA is better than bad ARIA".

### 17.1. Primeira regra

Se há HTML nativo que faz o necessário, use-o. `<button>` em vez de `<div role="button">`. `<nav>` em vez de `<div role="navigation">`. ARIA é para widgets que HTML nativo não cobre.

### 17.2. Live regions

| Value | Quando |
|-------|--------|
| `off` | Default, sem anúncio |
| `polite` | Status informativo |
| `assertive` | Erros críticos |

Complementos: `aria-atomic="true"` (lê tudo), `aria-relevant` (controla trigger).

### 17.3. aria-describedby vs aria-labelledby

`aria-labelledby` substitui accessible name. `aria-describedby` adiciona descrição complementar (lida depois).

```html
<button aria-labelledby="btn-label" aria-describedby="btn-hint">
  <span id="btn-label">Salvar</span>
</button>
<span id="btn-hint">Atalho Cmd+S</span>
```

### 17.4. aria-expanded, aria-controls, aria-owns

- `aria-expanded="true|false"` em disclosure triggers.
- `aria-controls="id"` aponta para elemento controlado.
- `aria-owns="id"` estabelece relação parent-child lógica.

### 17.5. Landmarks

| Tag | Role implícito |
|-----|---------------|
| `<header>` | banner |
| `<nav>` | navigation |
| `<main>` | main |
| `<aside>` | complementary |
| `<footer>` | contentinfo |
| `<section aria-label>` | region |
| `<form aria-label>` | form |

SRs permitem navegação por landmarks (tecla D em NVDA).

### 17.6. aria-current

Valores: `page`, `step`, `location`, `date`, `time`, `true`.

### 17.7. Roles que estendem semântica

Usar quando nativo não cobre: `tablist/tab/tabpanel`, `combobox/listbox/option`, `tree/treeitem`, `grid/row/gridcell`, `menu/menuitem`, `tooltip`. Cada role vem com keyboard contract. Referência: ARIA Authoring Practices Guide em w3.org/WAI/ARIA/apg.

---

## 18. Keyboard navigation

Todo fluxo operável apenas com teclado.

### 18.1. Tab order

- `tabindex="0"` inclui na ordem natural.
- `tabindex="-1"` remove (permite focus programático).
- `tabindex` positivo é antipadrão.

Ordem DOM coincide com ordem visual. CSS `order` em flex/grid que inverte confunde.

### 18.2. Teclas por padrão

**Tabs.** Tab foca tablist, setas esquerda/direita navegam, Enter/Space aciona (manual activation), Home/End primeira/última.

**Menu.** Setas cima/baixo navegam, Enter/Space aciona, Esc fecha, letra faz type-ahead.

**Combobox.** Setas navegam listbox, Enter seleciona, Esc fecha listbox, Esc novamente limpa input.

**Grid.** Setas movem cell a cell, Ctrl+Home primeira, Ctrl+End última, Page Up/Down scrolla, Enter/F2 edit mode.

**Slider.** Setas step, Shift+Setas step grande, Home/End min/max.

**Dialog.** Esc fecha, Tab circula.

### 18.3. Convenção APG

Cada widget tem documentação oficial em w3.org/WAI/ARIA/apg/patterns. Consultar antes de inventar.

### 18.4. Teste manual

Desconectar mouse, executar fluxo completo só com teclado, validar que cada elemento interativo é alcançável e focado com indicador visível, Esc funciona em modais, Enter/Space aciona buttons.

---

## 19. Screen reader behavior

Testar em múltiplos SRs é ideal, em pelo menos um é mínimo.

### 19.1. NVDA (Windows)

Gratuito, open source, referência em testing. Hotkeys: Insert+F7 (lista), H próximo heading, D próximo landmark, F próximo form field, T próxima tabela, B próximo botão. Modos browse vs focus.

### 19.2. JAWS (Windows)

Comercial, padrão corporativo e governo EUA. Similar ao NVDA. Tabela com Ctrl+Alt+setas anuncia dimensional ("linha 3, coluna 2, Ana Silva").

### 19.3. VoiceOver (macOS/iOS)

Nativo Apple. Cmd+F5 (macOS) ou 3 toques botão lateral (iOS). VO modifier é Ctrl+Option no macOS. Rotor (VO+U) navega por tipo. Mobile: swipe direita/esquerda entre elementos, duplo toque aciona.

### 19.4. TalkBack (Android)

Nativo Google. Gestos similares ao VoiceOver iOS. Leitura por páginas move em blocos maiores.

### 19.5. Diferenças

| Feature | NVDA | JAWS | VoiceOver | TalkBack |
|---------|------|------|-----------|----------|
| Describedby | Settings | Sim | Sim | Variável |
| Autocomplete | Parcial | Sim | Sim | Sim |
| Landmarks list | Sim | Sim | Sim (rotor) | Sim |
| Browse/focus | Sim | Sim | Virtual cursor | N/A (mobile) |
| Table dimensional | Sim | Melhor | Sim | Limitado |

### 19.6. Testing pragmático

- Todo PR crítico: NVDA + Chrome.
- Release: NVDA + Chrome, VoiceOver + Safari, VoiceOver iOS + Safari.
- Enterprise: JAWS + Edge quando possível.

Não precisa ser SR user fluente. Saber comandos básicos cobre 80% dos problemas.

---

## 20. Cognitive a11y

Cognição (memória, atenção, processamento) é eixo central.

### 20.1. Plain language

SC 3.1.5 (AAA) sugere nível lower secondary (8ª série). Frases curtas, vocabulário comum, evitar jargão. Ferramentas: Hemingway Editor, Flesch-Kincaid (Word), Rewordify. Em português, Flesch-Kincaid adaptado.

### 20.2. Consistency

SC 3.2.3 (AA): mesma navegação em mesma ordem em todas páginas. SC 3.2.4 (AA): mesmo componente identificado da mesma forma. Se botão é "Excluir" em uma tela, é "Excluir" em todas, não "Deletar" em outras.

### 20.3. Error prevention

SC 3.3.4 (AA) para dados legais, financeiros ou irreversíveis: reversibilidade (undo), checagem (validação antes de confirmar), confirmação (revisão antes de submeter). Exemplo: checkout com resumo antes de cobrar; deleção de conta com confirmação textual.

### 20.4. Predictability

SC 3.2.1 (A): mudança de contexto não acontece ao receber foco. SC 3.2.2 (A): mudança de contexto não acontece ao alterar valor (exceto avisado). Antipadrão: dropdown que submete form ao selecionar.

### 20.5. Recovery

SC 3.3.1 (A) identificar erros. SC 3.3.3 (AA) sugestão de correção. Ruim: "Invalid input". Bom: "Email invalido. Use formato nome@exemplo.com".

### 20.6. Cognitive load

Recomendações: chunks (agrupar campos relacionados), progress indicators em fluxos longos, auto-save em forms longos, voltar sem perder dados, tooltips inline para conceitos complexos.

---

## 21. Motor a11y

Usuários com limitação motora usam switch devices, head pointers, eye tracking, voice control, keyboard, mouse com precisão reduzida.

### 21.1. Click targets

Seção 6. Mínimo 24x24, recomendado 40x40.

### 21.2. Drag alternatives

Seção 7. Sempre oferecer single-pointer.

### 21.3. Time-critical

SC 2.2.1 (A) e 2.2.3 (AAA): timeout permite turn off, adjust (10x), extend (warning + extensão). Exceção: leilões em tempo real.

### 21.4. Pointer gestures

SC 2.5.1 (A): funcionalidade que depende de gesto multi-point (pinch, swipe multi-dedo) precisa alternativa single-point. Mapa com pinch zoom precisa botões +/-.

### 21.5. Pointer cancellation

SC 2.5.2 (A): ações críticas disparam em pointer up, não pointer down. Permite cancelar arrastando fora antes de soltar. Usar `onClick` em vez de `onMouseDown` para ações destrutivas.

### 21.6. Voice control

SC 2.5.3 (A) Label in Name: accessible name começa com texto visível. Se botão mostra "Salvar" mas `aria-label` é "Confirmar", voice control falha ao dizer "click Salvar".

Ruim: `<button aria-label="Confirmar acao">Salvar</button>`.
Bom: `<button aria-label="Salvar documento">Salvar</button>`.

### 21.7. Switch devices

Switch users acionam um ou dois botões simulando Tab e Enter. Tudo que funciona com teclado funciona com switch. Otimizações: ações frequentes no topo da tab order, landmarks para pular rápido, evitar menus multinível.

---

## 22. Testing toolkit

### 22.1. axe-core

Engine open source da Deque. Integra Puppeteer, Playwright, Cypress, Jest. Padrão-ouro de automação.

```javascript
const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

test('home sem violacoes', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag22aa'])
    .analyze();
  expect(results.violations).toEqual([]);
});
```

Detecta: contraste, label ausente, role inválido, heading order, duplicate IDs.

### 22.2. Lighthouse

Built-in Chrome DevTools. Audit Accessibility gera score 0-100. Cobre ~30% dos critérios (o automatizável). Smoke test, não validação completa.

```bash
lighthouse https://exemplo.com --only-categories=accessibility --output=html
```

### 22.3. pa11y, WAVE, Color Oracle

**pa11y.** CLI focado em a11y, bom para CI sem browser UI.

```bash
npm install -g pa11y
pa11y https://exemplo.com --standard WCAG2AA
```

**WAVE.** Extensão WebAIM visualiza violações inline. Bom para manual review.

**Color Oracle.** Simula daltonismo (protanopia, deuteranopia, tritanopia, achromatopsia). Valida que cor não é único meio de comunicação.

### 22.6. Screen reader manual

Abrir Chrome, ativar NVDA (Ctrl+Alt+N), tabular pela página, Insert+F7 para listar elementos, validar que anúncios fazem sentido.

### 22.7. Keyboard-only

Desplugar mouse, usar Tab/Shift+Tab/Enter/Space/Esc/Setas, cumprir fluxos core. Travar em algum ponto é issue.

---

## 23. Automated testing in CI

Integrar a11y no pipeline detecta regressões.

### 23.1. GitHub Actions

`.github/workflows/a11y.yml`:

```yaml
name: Accessibility
on:
  pull_request:
    branches: [main]
jobs:
  a11y:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npx playwright install --with-deps chromium
      - run: npm run test:a11y
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: a11y-report
          path: a11y-results/
```

### 23.2. Test script

`tests/a11y.spec.js`:

```javascript
const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;
const fs = require('fs');

const pages = ['/', '/produtos', '/contato', '/login'];

for (const path of pages) {
  test(`a11y ${path}`, async ({ page }) => {
    await page.goto(`http://localhost:3000${path}`);
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag22aa'])
      .analyze();
    fs.writeFileSync(
      `a11y-results/${path.replace(/\//g, '_')}.json`,
      JSON.stringify(results, null, 2)
    );
    expect(results.violations).toEqual([]);
  });
}
```

### 23.3. Severity gate

Falhar build só em critical/serious, warning em minor/moderate:

```javascript
const criticalViolations = results.violations.filter(
  (v) => v.impact === 'critical' || v.impact === 'serious'
);
expect(criticalViolations).toEqual([]);
```

### 23.4. Regression tracking e coverage

Salvar snapshot de violations (use `@axe-core/cli` com diff mode). Count sobe em PR alerta. Automação detecta ~30-40% dos issues, 60-70% exigem manual (keyboard, SR, cognitive). Balancear com auditoria trimestral.

---

## 24. Top 20 common failures e fixes

1. **Alt text ausente.** `<img src>` sem alt ou `alt="image"`. Fix: alt descritivo ou `alt=""` se decorativo.
2. **Placeholder contraste.** #CCC em branco (1.6:1). Fix: >= #767676 (4.54:1).
3. **Div clicável sem role.** `<div onClick>`. Fix: usar `<button>`.
4. **Label ausente.** Input só com placeholder. Fix: `<label for><input id>`.
5. **Focus removido.** `outline: none` sem substituto. Fix: `:focus-visible { outline: 2px solid var(--focus); }`.
6. **Heading order.** h1 seguido de h3. Fix: ordem sequencial.
7. **Link sem texto.** `<a href><img></a>` sem alt. Fix: alt ou `aria-label`.
8. **Botão ícone sem label.** `<button><svg></svg></button>`. Fix: `aria-label`.
9. **Table de layout.** Usar table para layout. Fix: CSS Grid/Flex.
10. **Modal sem focus trap.** Tab escapa. Fix: implementar trap (focus-trap lib).
11. **Modal sem aria-modal.** `<div class="modal">`. Fix: `role="dialog" aria-modal="true" aria-labelledby`.
12. **Skip link ausente.** SR/keyboard tabula nav toda vez. Fix: `<a href="#main">Pular</a>`.
13. **Language não declarada.** `<html>` sem `lang`. Fix: `lang="pt-BR"`.
14. **Autocomplete ausente.** Email sem `autocomplete="email"`. Fix: adicionar.
15. **Erro não associado.** Mensagem abaixo sem `aria-describedby`. Fix: `aria-describedby="erro-id"`.
16. **Dropdown com role errado.** Nav com `role="menu"`. Fix: `<nav>` com links.
17. **Live region dinâmica.** Container só criado quando há toast. Fix: container permanente com `aria-live`.
18. **Loading sem anúncio.** Spinner visual, SR não sabe. Fix: `aria-busy="true"` + `sr-only`.
19. **Icon sem contraste.** Ícone informativo 2:1. Fix: 3:1 mínimo (SC 1.4.11).
20. **Target pequeno.** Ícone 16x16. Fix: container 40x40 com padding.

---

## 25. Role-based checklists

### 25.1. Designer (Figma)

Cores com contraste AA desde o início (Stark), focus ring em token de cor, targets >= 40x40, estados disabled/hover/focus/active em cada componente, hierarquia de headings marcada, `aria-label` em ícones-only anotado, validação em modo color-blind, skip link no layout, mensagens de erro acionáveis, prototypes validam keyboard flow.

### 25.2. Developer

HTML semântico nativo, ARIA só quando nativo não basta, todo input com label, todo button com texto ou `aria-label`, focus management em modais e SPAs, skip link funcional, language declarado, axe-core em dev, keyboard-only cada PR, NVDA smoke test em release, live regions para status, contraste validado em tokens.

### 25.3. QA

axe-core em todas páginas, Lighthouse audit, keyboard-only em fluxos críticos, NVDA em uma jornada, zoom 200% (SC 1.4.4), text-spacing aumentado (SC 1.4.12), dark mode, VoiceOver iOS ou TalkBack mobile, autoplay com pause, timeouts com opção de estender, consistent help e navigation validados.

### 25.4. Content writer

Nível 8ª série (Flesch), frases curtas e voz ativa, jargão explicado, alt text descritivo, transcrições e legendas, headings em ordem, links descritivos (não "clique aqui"), siglas expandidas na primeira ocorrência, erros acionáveis, labels curtos, CTAs com verbo de ação, tone consistente.

### 25.5. Product manager

Nível de conformância definido (AA recomendado), a11y em definition of done, budget para auditoria externa anual, recrutar users com deficiência, priorizar bugs por impact, a11y score como métrica, training para o time, compliance legal por região, VPAT em releases enterprise, acesso a ferramentas (Stark, axe Pro, JAWS).

### 25.6. DevOps

axe-core em cada PR, blockar merge em violations critical, artifacts de report disponíveis, métricas históricas, alertar regressão, Lighthouse CI em preview builds.

---

## Referências oficiais

- W3C, Web Content Accessibility Guidelines (WCAG) 2.2, Recommendation de 5 de outubro de 2023, w3.org/TR/WCAG22
- W3C, What's New in WCAG 2.2, w3.org/WAI/standards-guidelines/wcag/new-in-22
- W3C, ARIA Authoring Practices Guide (APG), w3.org/WAI/ARIA/apg
- Deque, axe-core rules, dequeuniversity.com/rules/axe
- WebAIM, Contrast Checker, webaim.org/resources/contrastchecker
- U.S. Section 508, section508.gov
- EN 301 549 (UE), etsi.org
- Brasil, Lei Brasileira de Inclusão 13.146/2015 e eMAG, governo.planejamento.gov.br/emag
