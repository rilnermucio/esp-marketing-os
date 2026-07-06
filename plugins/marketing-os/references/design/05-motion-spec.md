# 05. Motion Spec Deep Reference (2026)

> Parte da stack de companions do `design-agent` (v4.0).
> Referência aplicada sobre motion em design systems: tokens de duração e easing, choreography, 12 princípios Disney aplicados a UI, reduced-motion, motion grammar, receitas por componente, micro-interactions, performance, comparação de ferramentas e anti-patterns.

**Quando consultar:** ao definir tokens de duração e easing para um design system, ao especificar motion de um componente (modal, toast, button), ao auditar performance de animações (stutter, jank), ao implementar `prefers-reduced-motion`, ao escolher ferramenta (CSS, Framer Motion, Lottie, Rive, GSAP), ao traduzir brand personality em motion, ou ao revisar anti-patterns em um produto existente.

**Pré-requisitos:** `references/design/01-tokens-w3c-spec.md` (tokens), `references/design/02-atomic-design-playbook.md` (composição) e `references/design/04-accessibility-wcag22.md` (motion tem implicações em WCAG 2.3.3).

---

## Índice

1. Por que motion importa
2. Motion tokens
3. Easing curves
4. Choreography
5. 12 princípios Disney aplicados a UI
6. Reduced motion
7. Motion grammar
8. Component-level recipes
9. Micro-interactions
10. Performance
11. Tools comparison
12. Decision tree qual tool
13. Motion in brand
14. Anti-patterns
15. Testing motion

---

## 1. Por que motion importa

Motion em produto digital não é decoração. É linguagem. Quatro funções concretas:

**Comunicação (feedback):** motion responde a ação do usuário e confirma que o sistema recebeu o input. Click em botão sem feedback visual faz o usuário clicar de novo. Scale de 2% em 100ms resolve: o botão acknowledgea, o usuário sabe que a ação foi registrada. Feedback motion preenche o gap entre input e resposta do servidor.

**Orientação (onde vem, onde vai):** quando um elemento aparece ou sai da tela, o movimento sinaliza origem e destino. Modal que cresce do botão clicado cria continuidade espacial. Page transitions com slide-in da direita indicam avançar, slide-in da esquerda indicam voltar.

**Continuidade (não quebra mental model):** elementos que aparecem instantaneamente quebram a expectativa de que o mundo é contínuo. Cérebro humano processa mudanças instantâneas como falhas. Motion de 150ms a 300ms preserva continuidade.

**Personalidade (brand expression):** motion carrega tom de voz. Marca que usa spring com bounce leve comunica energia. Marca que usa ease-out linear em durações curtas comunica precisão. Motion é brand asset, equivalente a paleta e tipografia.

**Acessibilidade (cognitive load):** motion bem projetado reduz cognitive load. Mal projetado adiciona load: distrai, causa mareio, força o usuário a parar. `prefers-reduced-motion` (seção 6) é resposta WCAG.

---

## 2. Motion tokens

Motion precisa de tokens pelo mesmo motivo que cor precisa: consistência, escala, temabilidade. Sem tokens, cada componente inventa durações e você acaba com modal de 450ms, toast de 275ms, button de 180ms sem justificativa.

### 2.1. Duration scale

| Token | Valor | Uso |
|-------|-------|-----|
| `duration.instant` | 100ms | Acknowledgement imediato (button press, checkbox toggle) |
| `duration.fast` | 150ms | Hover, tooltip show, small UI state changes |
| `duration.normal` | 250ms | Modal enter, toast pop, dropdown open |
| `duration.slow` | 400ms | Page transitions, dialog enter com conteúdo |
| `duration.slower` | 700ms | Hero animations, onboarding reveals |
| `duration.glacial` | 1200ms | Decorative only, hero loops, não interativo |

Derivados de Material Design, iOS HIG e IBM Carbon. Três regras: abaixo de 100ms imperceptível; acima de 500ms em UI vira lento; zona útil é 100ms a 400ms.

### 2.2. Easing library

| Token | Cubic-bezier | Uso |
|-------|-------------|-----|
| `easing.linear` | `linear` | Loops, progress, velocidade constante |
| `easing.standard` | `cubic-bezier(0.4, 0.0, 0.2, 1)` | Default, movimento de A para B |
| `easing.decelerate` | `cubic-bezier(0.0, 0.0, 0.2, 1)` | Entry: chega e desacelera (ease-out) |
| `easing.accelerate` | `cubic-bezier(0.4, 0.0, 1, 1)` | Exit: acelera ao sair (ease-in) |
| `easing.emphasized` | `cubic-bezier(0.2, 0.0, 0, 1)` | Transições importantes com overshoot sutil |

### 2.3. Tokens em CSS

```css
:root {
  --duration-instant: 100ms;
  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --duration-slow: 400ms;
  --duration-slower: 700ms;
  --easing-standard: cubic-bezier(0.4, 0, 0.2, 1);
  --easing-decelerate: cubic-bezier(0, 0, 0.2, 1);
  --easing-accelerate: cubic-bezier(0.4, 0, 1, 1);
}
```

Em JSON (Tokens Studio, Style Dictionary), motion vira categoria ao lado de color, typography, spacing, com `type: "duration"` e `type: "cubicBezier"`.

---

## 3. Easing curves

Easing é a função matemática que descreve aceleração ao longo do tempo. Entre linear (constante) e step (abrupto), infinitas curvas.

### 3.1. Três famílias

**Ease-out (decelerate):** começa rápido, termina devagar. Use para entrada. Motivo físico: objetos chegando desaceleram. Visualmente comunica "chegou".

**Ease-in (accelerate):** começa devagar, termina rápido. Use para saída. Motivo físico: objetos saindo aceleram. Visualmente comunica "foi embora".

**Ease-in-out (standard):** desacelera no início e fim, acelera no meio. Use para movimento contínuo entre dois estados (carro em estrada).

### 3.2. Material vs iOS

Google definiu `cubic-bezier(0.4, 0.0, 0.2, 1)` como padrão. 40% em aceleração, 60% em desaceleração. Bias para desaceleração parece mais natural em UI. Funciona em 100ms a 400ms.

Apple usa `cubic-bezier(0.25, 0.1, 0.25, 1)`, mais próximo de `ease-out` puro. Para spring em SwiftUI, `spring(response: 0.55, dampingFraction: 0.825)` é default. Resultado: iOS tende a ser mais gentil, menos punchy que Android.

### 3.3. Easing cheat sheet

| Situação | Easing |
|----------|--------|
| Elemento aparecendo | `ease-out` ou `decelerate` |
| Elemento desaparecendo | `ease-in` ou `accelerate` |
| Movendo entre posições | `ease-in-out` ou `standard` |
| Loop infinito (spinner) | `linear` |
| Confirmação com bounce | `spring` com damping 0.7 |

```css
.modal-enter {
  animation: modal-enter var(--duration-normal) var(--easing-decelerate);
}

.modal-exit {
  animation: modal-exit var(--duration-fast) var(--easing-accelerate);
}
```

---

## 4. Choreography

Choreography é a orquestração de múltiplas animações. Um modal não é uma animação: é backdrop, container, conteúdo interno.

### 4.1. Stagger (atraso sequencial)

Elementos aparecem um depois do outro com delay fixo. Usado em listas, cards, grids. Regra: 30ms a 80ms de delay. Menos vira simultâneo, mais vira lento.

```css
.card {
  animation: fade-in 300ms var(--easing-decelerate) backwards;
}

.card:nth-child(1) { animation-delay: 0ms; }
.card:nth-child(2) { animation-delay: 50ms; }
.card:nth-child(3) { animation-delay: 100ms; }
```

### 4.2. Parallel, sequential, orchestrated

**Parallel:** todas ao mesmo tempo. Use quando elementos são peers sem hierarquia.

**Sequential:** uma espera a anterior. Use quando há causalidade: backdrop, depois modal, depois conteúdo.

**Orchestrated:** combinação. Modal complexo: backdrop fade (0-150ms) + container scale (0-250ms) + header fade (100-300ms) + body stagger (150ms+) + footer (300-500ms). Total 500ms, mas feedback já aos 250ms.

### 4.3. Quando usar qual

| Situação | Choreography |
|----------|-------------|
| Lista de 3-10 items | Stagger |
| Dois elementos sem hierarquia | Parallel |
| Modal com backdrop | Sequential ou parallel |
| Onboarding hero | Orchestrated |
| Reorder de lista | Parallel |

---

## 5. 12 princípios Disney aplicados a UI

Johnston e Thomas publicaram em 1981. Escritos para cartoon, aplicáveis a UI.

1. **Squash and stretch:** deformação sutil (2-5%) em button press.
2. **Anticipation:** micro-movimento oposto antes de ação grande.
3. **Staging:** foco visual. Modal com backdrop escuro força o olho.
4. **Straight ahead vs pose to pose:** em UI, pose to pose domina (estado inicial e final).
5. **Follow through e overlapping:** partes continuam se movendo depois do objeto parar. Card escala, sombra expande com leve delay.
6. **Slow in e slow out (ease):** movimento sem ease parece mecânico.
7. **Arcs:** objetos na natureza se movem em arcos. Em UI, uso limitado.
8. **Secondary action:** suporta a principal. Card escala, sombra cresce junto.
9. **Timing:** duração comunica mood. Rápido é energético, lento é pesado.
10. **Exaggeration:** overshoot de 5-10% em ações de sucesso. Com moderação.
11. **Solid drawing:** volume e forma. Em UI, transições 3D (flip card). Uso raro.
12. **Appeal:** movimento precisa ser agradável. Subjetivo, testável via A/B.

---

## 6. Reduced motion

WCAG 2.3.3 (AAA) e `prefers-reduced-motion` respondem ao problema: motion pode causar nausea, enxaqueca, vertigo. Aproximadamente 35% da população adulta tem alguma sensibilidade (VeDA, 2022). Ativado em macOS (Accessibility → Display → Reduce Motion), iOS (Accessibility → Motion), Windows (Accessibility → Visual Effects) e Android (Accessibility → Remove animations).

### 6.1. Padrão errado

```css
/* Errado: quebra componentes que dependem de transition */
@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
}
```

Remove feedback essencial. Button sem press visual vira falha de usabilidade. Dropdown com max-height transition fica saltando.

### 6.2. Padrão correto

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

Durações viram praticamente instantâneo mas transitions funcionam. Iterations limitadas a 1.

### 6.3. Padrão ideal: substituir por crossfade

Para movimento essencial, substituir scale/rotate por opacity-only:

```css
.modal {
  animation: modal-enter var(--duration-normal) var(--easing-decelerate);
}

@keyframes modal-enter {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

@media (prefers-reduced-motion: reduce) {
  .modal {
    animation: modal-enter-reduced var(--duration-fast) linear;
  }

  @keyframes modal-enter-reduced {
    from { opacity: 0; }
    to { opacity: 1; }
  }
}
```

Transform scale removido (causa zoom que dispara vertigo). Opacity fade preservado.

### 6.4. Framer Motion

```jsx
import { useReducedMotion } from "framer-motion";

const shouldReduceMotion = useReducedMotion();

<motion.div
  animate={{ opacity: 1, scale: shouldReduceMotion ? 1 : 1.05 }}
  transition={{ duration: shouldReduceMotion ? 0 : 0.25 }}
/>
```

### 6.5. Checklist

- [ ] `prefers-reduced-motion: reduce` configurado em todas as animações
- [ ] Transforms scale e rotate removidos em reduced
- [ ] Opacity transitions preservadas
- [ ] Nenhum auto-play de video em reduced
- [ ] Parallax scroll desabilitado em reduced
- [ ] Testado com setting ativo em macOS e Windows

---

## 7. Motion grammar

Conjunto de padrões reutilizáveis que definem a linguagem do produto.

### 7.1. Entry e exit

```css
@keyframes enter {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

@keyframes exit {
  from { opacity: 1; transform: scale(1); }
  to { opacity: 0; transform: scale(0.95); }
}

.entry { animation: enter var(--duration-normal) var(--easing-decelerate); }
.exit { animation: exit var(--duration-fast) var(--easing-accelerate); }
```

Scale 0.95 é sutil. Scale 0.8 é agressivo, reservado para hero onboarding. Exit sempre mais rápido que entry.

### 7.2. Emphasis, loading, error

```css
@keyframes emphasis {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.03); }
}

@keyframes skeleton-pulse {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

@keyframes error-shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-4px); }
  75% { transform: translateX(4px); }
}

.error-shake {
  animation: error-shake 200ms var(--easing-standard) 2;
}
```

Duas iterações de 200ms (400ms total).

---

## 8. Component-level recipes

### 8.1. Modal enter

```css
.modal-container {
  animation: modal-enter var(--duration-normal) var(--easing-decelerate);
}

@keyframes modal-enter {
  from { opacity: 0; transform: scale(0.95) translateY(8px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}
```

```jsx
<motion.div
  initial={{ opacity: 0, scale: 0.95, y: 8 }}
  animate={{ opacity: 1, scale: 1, y: 0 }}
  exit={{ opacity: 0, scale: 0.95, y: 8 }}
  transition={{ duration: 0.25, ease: [0, 0, 0.2, 1] }}
/>
```

### 8.2. Toast, button press, page transition, skeleton

```css
@keyframes toast-enter {
  from { opacity: 0; transform: translateY(-16px); }
  to { opacity: 1; transform: translateY(0); }
}

.button {
  transition: transform var(--duration-instant) var(--easing-standard);
}
.button:active { transform: scale(0.98); }

.skeleton {
  background: linear-gradient(90deg,
    var(--color-surface-1) 25%,
    var(--color-surface-2) 50%,
    var(--color-surface-1) 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s var(--easing-standard) infinite;
}

@keyframes skeleton-shimmer {
  from { background-position: 200% 0; }
  to { background-position: -200% 0; }
}
```

```jsx
<motion.button whileTap={{ scale: 0.98 }} transition={{ duration: 0.1 }} />

<AnimatePresence mode="wait">
  <motion.div
    key={location.pathname}
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    exit={{ opacity: 0 }}
    transition={{ duration: 0.3 }}
  />
</AnimatePresence>
```

---

## 9. Micro-interactions

### 9.1. Hover, focus, active

```css
.card {
  transition:
    transform var(--duration-fast) var(--easing-standard),
    box-shadow var(--duration-fast) var(--easing-standard);
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.input:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}

.button:active { transform: scale(0.98); }
```

Focus não anima entrada (instantâneo para acessibilidade), mas pode animar o ring out em blur.

### 9.2. Success e error

```css
@keyframes success-bounce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.success {
  animation: success-bounce var(--duration-slow) var(--easing-standard);
}

.input.invalid {
  border-color: var(--color-danger);
  animation: error-shake 200ms var(--easing-standard) 2;
}
```

---

## 10. Performance

Meta: 60fps constante (16.6ms por frame), ou 120fps em devices compatíveis.

### 10.1. GPU-accelerated properties

| Prop | GPU? | Por quê? |
|------|------|----------|
| `transform` | YES | Compositor layer |
| `opacity` | YES | Compositor layer |
| `filter` | YES (limitado) | GPU em maior parte |
| `top`, `left`, `width`, `height`, `margin`, `padding` | NO | Causa layout |
| `background-color`, `box-shadow` | NO | Causa paint |

### 10.2. Animar errado vs certo

```css
/* Errado: causa layout em 60 frames/seg */
@keyframes slide {
  from { left: -100px; }
  to { left: 0; }
}

/* Certo: GPU-accelerated */
@keyframes slide {
  from { transform: translateX(-100px); }
  to { transform: translateX(0); }
}
```

### 10.3. will-change com moderação

Muitos `will-change` esgotam memória de GPU em mobile. Aplicar apenas antes da animação e remover depois.

```js
element.style.willChange = "transform";
element.addEventListener("animationend", () => {
  element.style.willChange = "auto";
});
```

`transform: translate3d(0, 0, 0)` é hack legado. Use `will-change` quando necessário.

### 10.4. Métricas target

| Métrica | Target | Aceitável |
|---------|--------|-----------|
| Frame rate | 60fps | >= 58fps |
| INP (Interaction to Next Paint) | < 100ms | < 200ms |
| Long Animation Frames | 0 | < 5 por sessão |

Chrome DevTools Performance: procurar `Recalculate Style` e `Layout` em vermelho.

---

## 11. Tools comparison

| Ferramenta | Strengths | Weaknesses | Quando usar |
|-----------|-----------|-----------|-------------|
| **CSS transitions/animations** | Nativo, cheap, acessível | Limitado a props CSS, difícil orquestrar | Micro-interactions, state changes simples |
| **Web Animations API** | JS-controlled, performático | Verbose, menos declarativo | Controle programático sem lib |
| **Framer Motion** | React declarativo, spring, variants | React-only, bundle +40kb | Apps React com motion complexo |
| **Lottie** | Designer workflow (AE → JSON) | JSON pesado | Ilustrações animadas, onboarding |
| **Rive** | State machines, interativo, binário pequeno | Curva de aprendizado | Personagens interativos |
| **GSAP** | Timeline-based, features avançadas | Bundle 50kb+ | Animações complexas não-React |

### 11.1. Exemplos

```jsx
// Framer Motion
<motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.25 }} />

// Lottie
import Lottie from "lottie-react";
<Lottie animationData={data} loop={false} />

// Rive
import { useRive } from "@rive-app/react-canvas";
const { RiveComponent } = useRive({ src: "char.riv", stateMachines: "State", autoplay: true });

// GSAP
gsap.to(".box", { x: 100, duration: 1, ease: "power2.inOut" });
```

### 11.2. Bundle size

CSS e Web Animations API: 0kb. Framer Motion: 40kb (15-20kb com tree-shaking). Lottie: 180-250kb. Rive: 200kb. GSAP core: 50kb. Começar com CSS. Subir a stack só quando CSS não resolve.

---

## 12. Decision tree qual tool

```
Precisa animar algo?
│
├── Simples (hover, fade, scale)?
│   YES → CSS transitions/animations
│
├── State-driven React (entrada/saída condicional)?
│   YES → Framer Motion
│
├── Ilustração vetorial complexa?
│   YES → Lottie
│
├── Personagem interativo com estados?
│   YES → Rive
│
├── Timeline complexo com scroll-trigger?
│   YES → GSAP
│
└── Controle programático sem lib?
    YES → Web Animations API
```

### 12.1. Exemplos práticos

| Caso | Ferramenta |
|------|-----------|
| Button hover color | CSS |
| Modal enter/exit em React | Framer Motion |
| Checkout success com confete | Lottie ou CSS + JS |
| Mascote que reage a input | Rive |
| Landing com parallax scroll | GSAP |
| Toast do topo | CSS ou Framer Motion |
| Skeleton shimmer | CSS |
| Page transition SPA | Framer Motion (AnimatePresence) |
| Infographic animado (AE export) | Lottie |

---

## 13. Motion in brand

Motion carrega personalidade. Três arquétipos.

### 13.1. Bouncy (playful, energético)

Exemplos: Duolingo, Mailchimp, Figma. Spring com damping baixo (0.6-0.7), overshoot visível. Durações 300-500ms. Scale exagerado (1.1-1.2). Bounce em sucesso.

```jsx
<motion.div
  animate={{ scale: 1 }}
  initial={{ scale: 0.5 }}
  transition={{ type: "spring", damping: 10, stiffness: 100 }}
/>
```

### 13.2. Elegante (precisão, calma)

Exemplos: Apple, Linear, Arc Browser. Ease-out puro ou cubic-bezier suave. Durações 150-250ms. Sem overshoot. Crossfades mais que scale.

```css
.transition { transition: all var(--duration-fast) cubic-bezier(0.25, 0.1, 0.25, 1); }
```

### 13.3. Minimalista (funcional)

Exemplos: Craft, Notion, enterprise. Motion apenas onde essencial. Durações 100-150ms. Sem ornamentação. Só opacity quando possível.

```css
.minimal { transition: opacity 100ms linear; }
```

### 13.4. Como escolher

Parte da brand guidelines. Fintech ou SaaS B2B → minimalista ou elegante. Consumer ou edtech → bouncy. Luxo ou design → elegante. Teste A/B com 10 pessoas da audiência target define o tom.

---

## 14. Anti-patterns

**Bouncy everything:** spring é tempero, não molho principal. Usar em confirmações de sucesso, não em hover de link.

**Distracting loops:** loop infinito em elemento não-essencial (logo pulsando, ícone girando sem motivo). Rouba atenção.

**Durações 1s+ em interações:** acima de 500ms em UI interativa é lento. Exceção: onboarding hero.

**Auto-play videos em entrada:** problema WCAG (2.2.2), performance, UX. Usar poster com play button.

**Simultaneous competing animations:** cinco elementos animando em posições diferentes. Olho não sabe onde olhar. Choreographar: um por vez, stagger, ou agrupar.

**Infinite subtle motion:** gradiente em loop no background, partículas flutuando. Acumula cognitive load. Usar apenas em heroes.

**Motion como único canal de informação:** elemento que só é visível por animar. Para quem tem reduced-motion, fica invisível. Motion é enhancement.

**Easing errado para direção:** elemento saindo com ease-out parece relutante. Elemento entrando com ease-in parece trombado. Direção importa.

**Motion que ignora scroll position:** animação dispara fora da viewport. Usar IntersectionObserver com `{ threshold: 0.3 }` para animar apenas quando entra na viewport.

**Reset de scroll em transition:** page transition que scrolla para topo quebra UX em listas. Preservar scroll position.

---

## 15. Testing motion

### 15.1. Screen recording

Gravar em 60fps. Assistir frame a frame. Procurar: saltos (frames pulados), easing inconsistente, pops (elemento aparece antes da animação), tearing (linha cortando).

### 15.2. Stutter detection

Chrome DevTools Performance. Meta 60fps. Procurar long frames (>16.6ms) em vermelho, FPS abaixo de 58, Layout/Paint durante animação. Em production, usar `PerformanceObserver` com `entryTypes: ["long-animation-frame"]` e alertar quando `entry.duration > 50ms`.

### 15.3. Reduced-motion QA

- [ ] Ativar `prefers-reduced-motion: reduce` no OS.
- [ ] Navegar pelo produto completo.
- [ ] Verificar que feedback de interação existe (button press, hover).
- [ ] Confirmar que nada essencial sumiu.
- [ ] Confirmar que nada está saltando (transition removida quebrou layout).

### 15.4. Device variation

Testar em iPhone SE 2020 (CPU lenta), iPhone 14+ (120Hz target), Pixel 6a (Android mid), Motorola G (low-end), Desktop Chrome i5, Safari M1. Usar Chrome DevTools throttling (4x slowdown) como proxy quando não tem device físico.

### 15.5. Interruption handling

Usuário clica, animação começa, clica em outro lugar antes de terminar. Opções:

- **Cancel:** animação para, próxima começa do zero. Pode parecer salto.
- **Reverse:** reverte suavemente. Elegante, mais complexo.
- **Complete then next:** espera terminar. Parece lento.

Framer Motion faz reverse por default:

```jsx
<motion.div
  animate={{ x: isOpen ? 100 : 0 }}
  transition={{ duration: 0.3 }}
/>
```

Mudança de `isOpen` no meio reverte suavemente.

### 15.6. Testing toolkit

Chrome DevTools Performance (profiling), `PerformanceObserver` API (monitoring prod), Lighthouse (INP), Puppeteer/Playwright (visual regression), Percy/Chromatic (snapshot em frames), Motion Tester (Chrome ext para preview).

### 15.7. Regression prevention

Storybook + Chromatic captura snapshots em keyframes específicos. Se animação muda sem querer, regression fail. Usar `play` function com delay para esperar midpoint (125ms em animação de 250ms) e comparar com baseline. PR é marked como visual change.

---

## Referências

- W3C CSS Animations Level 1: https://www.w3.org/TR/css-animations-1/
- W3C CSS Transitions: https://www.w3.org/TR/css-transitions-1/
- Web Animations API: https://www.w3.org/TR/web-animations-1/
- Material Design Motion: https://m3.material.io/styles/motion/
- Apple HIG Motion: https://developer.apple.com/design/human-interface-guidelines/motion
- IBM Carbon Motion: https://carbondesignsystem.com/guidelines/motion/overview/
- Framer Motion: https://www.framer.com/motion/
- Lottie: https://airbnb.io/lottie/
- Rive: https://rive.app/docs
- GSAP: https://gsap.com/docs/
- "The Illusion of Life" (Johnston, Thomas, 1981)
- WCAG 2.3.3 Animation from Interactions (AAA)
- Vestibular Disorders Association, 2022 report on motion sensitivity.

---

**Última revisão:** 2026-04-22 · **Owner:** design-agent (v4.0 companion stack) · **Status:** Ativo
