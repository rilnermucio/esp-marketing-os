# 02. Atomic Design Playbook (2026)

> Parte da stack de companions do `design-agent` (v4.0).
> Referência aplicada de Atomic Design para sistemas de design em 2026, com camada de tokens explicitada na base.

**Quando consultar:** ao estruturar um DS do zero, ao decidir em qual nível um componente vive, ao desenhar variant systems (Figma + código), ao escrever guidelines de composição, ao diagnosticar DS com god-organisms ou abstrações prematuras.

**Pré-requisitos:** leitura prévia de `references/design/01-tokens-w3c-spec.md` (a camada 0 depende de tokens DTCG).

---

## Índice

1. Contexto histórico
2. Os 6 níveis
3. Decision tree, qual nível?
4. Atoms
5. Molecules
6. Organisms
7. Templates
8. Pages
9. Naming conventions por nível
10. Variant systems
11. Composition patterns
12. Anti patterns
13. Atomic Design + tokens
14. Migração entre níveis
15. 12 componentes end to end
16. FAQ

---

## 1. Contexto histórico

### 1.1. Brad Frost, 2013

Em 2013, Brad Frost cunhou **Atomic Design** em um post que virou livro em 2016 (`atomicdesign.bradfrost.com`). A metáfora: interfaces são sistemas compostos de partes que se combinam em estruturas cada vez mais complexas. A química foi o modelo pedagógico, átomos em moléculas, moléculas em organismos.

A proposta original tinha 5 níveis: **Atoms, Molecules, Organisms, Templates, Pages**. A ordem é estrita, um organism não pode ser átomo de outro organism sem virar molécula primeiro. Na prática, a fronteira molecule vs organism é a mais porosa.

### 1.2. Por que pegou

Antes, os termos dominantes eram genéricos: `components`, `widgets`, `modules`, `blocks`, `sections`. Não indicavam granularidade nem ordem de composição. Frost deu vocabulário compartilhado entre design e engenharia, reduzindo fricção em handoffs e documentação.

Entre 2015 e 2020 a metodologia virou default em DS corporativos: Shopify Polaris, IBM Carbon, Atlassian, SAP Fiori, Salesforce Lightning.

### 1.3. Críticas e evolução

A partir de 2019 surgiram críticas válidas:

1. Metáfora química tem limites (químicos não pensam em templates).
2. Hierarquia rígida trava composição (SearchField é molécula ou organismo?).
3. Naming verbose (`MoleculeSearchField` não agrega).
4. Falta de camada de primitivos não visuais (cores, espaçamentos escondidos nos átomos).

A resposta da comunidade, consolidada entre 2022 e 2025, foi **adicionar uma camada 0 de tokens** sob os átomos. Isso alinha Atomic Design com Design Tokens (DTCG, W3C) e torna a base auditável.

### 1.4. Estado em 2026

Times maduros usam Atomic Design como mapa mental, não dogma: 6 níveis (tokens + 5 originais), pastas por nível no Figma (`0-tokens/`, `1-atoms/`), sem prefixos `atom_` no código, combinando com padrões modernos (slots do Radix, compound components), tratando a fronteira molecule/organism como decisão pragmática.

---

## 2. Os 6 níveis

### 2.1. Camada 0, Tokens

Primitivos de design: cores, espaços, raios, tipografia, sombras, durações, easings, z-index. Entregues como `tokens.json` DTCG + tema claro/escuro, transformados em CSS vars, dicionário JS/TS, Figma variables. **Regra:** átomos e acima consomem tokens, nunca literais. Detalhe em `references/design/01-tokens-w3c-spec.md`, seções 3, 4 e 6.

### 2.2. Nível 1, Atoms

Componentes funcionais não decomponíveis. Podem ter múltiplos elementos HTML, mas representam uma unidade conceitual única. Critério: se você remove qualquer parte, deixa de ser o que é. Consomem apenas tokens. Exemplos: `Button`, `Input`, `Label`, `Icon`, `Link`, `Badge`, `Avatar`, `Checkbox`, `Radio`, `Switch`, `Spinner`, `Divider`.

### 2.3. Nível 2, Molecules

Combinações pequenas de átomos (2 a 5) com uma responsabilidade clara, reutilizáveis em múltiplos contextos. Consomem átomos + tokens. Expõem API de composição (slots, children). Exemplos: `SearchField`, `FormField`, `CardHeader`, `Alert`.

### 2.4. Nível 3, Organisms

Seções complexas de interface compostas por moléculas + átomos, com estado próprio ou contexto de domínio. Representam áreas navegáveis (header, sidebar, hero) ou blocos de negócio (product card, data table com filtros). Podem consumir hooks, contexts. Nível onde aparece acoplamento com domínio. Exemplos: `Header`, `Footer`, `Hero`, `ProductCard`, `DataTable`, `FormSection`, `Sidebar`, `NavigationMenu`.

### 2.5. Nível 4, Templates

Layouts estruturais de página, sem conteúdo real. Wireframes vivos que definem grid, posicionamento e slots para organismos. Usam React `children` ou slots nomeados. Exemplos: `DashboardTemplate`, `LandingTemplate`, `ArticleTemplate`, `CheckoutTemplate`, `AuthTemplate`.

### 2.6. Nível 5, Pages

Instâncias concretas de templates com dados reais. Fetchs, conteúdo específico, SEO, analytics. Geralmente no framework de rota (Next.js `page.tsx`, Remix `route.tsx`). Conhece domínio por completo.

### 2.7. Resumo visual

```
PAGE (instância com dados reais)
 └── TEMPLATE (layout estrutural)
      └── ORGANISM (seção complexa)
           └── MOLECULE (composição pequena)
                └── ATOM (unidade funcional)
                     └── TOKEN (primitivo visual)
```

| Nível | Consome | Conhece domínio? | Tem estado? | Canônico |
|-------|---------|------------------|-------------|----------|
| 0 Tokens | nada | Não | Não | `color.primary-500` |
| 1 Atoms | tokens | Não | Raro | `Button` |
| 2 Molecules | atoms + tokens | Pouco | Às vezes | `FormField` |
| 3 Organisms | molecules + atoms | Sim | Frequente | `DataTable` |
| 4 Templates | organisms + slots | Não | Não | `DashboardTemplate` |
| 5 Pages | template + dados | Sim | Sim | `/dashboard` |

---

## 3. Decision tree, qual nível?

Quando um componente novo nasce, responda em ordem:

```
1. É valor puro (cor, espaço, tipografia)?
   SIM -> TOKEN
2. Unidade funcional única, não decomponível conceitualmente?
   SIM -> ATOM
3. Composição de 2-5 átomos com responsabilidade clara, reutilizável?
   SIM -> MOLECULE
4. Seção grande de página, tem lógica local, conhece domínio?
   SIM -> ORGANISM
5. Layout estrutural sem dados reais, define posicionamento e slots?
   SIM -> TEMPLATE
6. Rota concreta com dados, fetchs, analytics?
   SIM -> PAGE
```

### 3.1. Casos de fronteira

- **`SearchField` (Input + Icon + Button):** molecule.
- **`SearchField` com dropdown de resultados, debounce, histórico:** organism (ganhou estado e lógica de domínio).
- **`Card`:** geralmente atom com 3 slots. Vira molecule quando compõe children obrigatórios.
- **`ProductCard` (Card + Image + Title + Price + CTA):** organism (conhece domínio produto).
- **`Modal`:** molecule. Estrutura genérica (overlay + container + close). Organism só quando ganha comportamento específico.
- **`Navigation`:** organism. Lista de Links + drawer mobile + contexto de rota ativa.

### 3.2. Heurística rápida

Nome começa com domínio (Product, Order, Customer) -> organism. Nome genérico em 50 linhas -> molecule. Substantivo puro (Button, Input) sem domínio -> atom.

---

## 4. Atoms

### 4.1. Princípios

1. Não decomponível conceitualmente.
2. Consome apenas tokens (nunca literais de cor ou espaço).
3. Zero domínio.
4. API pequena (3 a 8 props; acima de 10 merece revisão).
5. Acessível por padrão (roles ARIA, keyboard nav, focus visível).
6. Variants explícitos (tipo, tamanho, estado).

### 4.2. 12 exemplos

- **Button.** Ação primária. `<button>` por padrão, aceita `as` polimórfico para `<a>`. Variants: `variant` (primary, secondary, ghost, destructive), `size` (sm, md, lg), `state` (default, loading, disabled). Tokens: `color.bg.primary`, `color.text.on-primary`, `radius.md`, `spacing.3`, `typography.label.md`.
- **Input.** Campo de texto. Variants: `size`, `state` (default, error, success, disabled). Tokens: `color.bg.surface`, `color.border.default`, `color.border.focus`, `radius.md`, `spacing.3`.
- **Label.** Rótulo de campo. `<label htmlFor>`. Variants: `size`, `required` (bool).
- **Icon.** SVG. Wrapper sobre Lucide/Tabler/Phosphor. Variants: `name`, `size` (xs, sm, md, lg), `color`.
- **Link.** Navegação textual. `<a>` ou `<Link>` do router. Variants: `variant` (default, subtle, inverse), `external` (bool).
- **Badge.** Indicador curto (status, contagem, tag). Variants: `variant` (neutral, success, warning, danger, info), `size`.
- **Divider.** Linha separadora. Variants: `orientation` (horizontal, vertical), `spacing`.
- **Spinner.** Loading circular. Variants: `size`, `color`.
- **Avatar.** Foto circular com fallback. Variants: `size` (xs-xl), `shape` (circle, square).
- **Checkbox.** Seleção múltipla booleana. Variants: `size`, `state` (checked, unchecked, indeterminate).
- **Radio.** Seleção única em grupo. Variants: `size`. Container: `RadioGroup`.
- **Switch.** Toggle on/off. Variants: `size`, `state`.

### 4.3. Tabela rápida

| Atom | HTML | Variants chave |
|------|------|----------------|
| Button | button/a | variant, size, state |
| Input | input | size, state |
| Label | label | size, required |
| Icon | svg | name, size, color |
| Link | a | variant, external |
| Badge | span | variant, size |
| Divider | hr/div | orientation, spacing |
| Spinner | div | size, color |
| Avatar | img+fallback | size, shape |
| Checkbox | input | size, state |
| Radio | input | size |
| Switch | button | size, state |

---

## 5. Molecules

### 5.1. Princípios

1. Composição pequena (2 a 5 átomos).
2. Uma responsabilidade.
3. Contexto mínimo (aceita valor e callback, não conhece domínio).
4. API via slots (flexibilidade para organisms customizarem).
5. Reutilizável em 3+ contextos sem adaptação.

### 5.2. 10 exemplos

- **SearchField.** Input + Icon + Button (clear opcional). `<SearchField><SearchField.Icon/><SearchField.Input/><SearchField.Clear/></SearchField>`. Variants: `size`, `variant` (inline, expanded).
- **FormField.** Label + Input + HelperText + ErrorMessage.
  ```tsx
  <FormField name="email">
    <FormField.Label required>Email</FormField.Label>
    <FormField.Input type="email" />
    <FormField.Helper>Enviamos atualizações</FormField.Helper>
    <FormField.Error />
  </FormField>
  ```
- **CardHeader.** Avatar + Heading + Subtext + Menu de ações.
- **Alert.** Icon + Text + CloseButton. Variants: `severity` (info, success, warning, danger), `dismissible`.
- **Breadcrumb.** Lista de Links + Separators. `<Breadcrumb><Breadcrumb.Item href="/">Início</Breadcrumb.Item>...</Breadcrumb>`.
- **Pagination.** Buttons + PageInfo + PageSizeSelect. Variants: `variant` (simple, full, compact), `size`.
- **TagList.** Array de Badges removíveis. `<TagList tags={tags} onRemove={handleRemove} max={5} />`.
- **MenuItem.** Icon + Label + Shortcut + ChevronRight. Variants: `variant` (default, destructive), `disabled`.
- **Tooltip.** Wrapper com trigger + content, baseado em primitivos headless (Radix, Ark).
- **ToastContent.** Icon + Title + Description + Action + CloseButton. Renderizado dentro de um Toast organism.

### 5.3. Tabela rápida

| Molecule | Átomos que consome | Slots expostos |
|----------|--------------------|-----------------|
| SearchField | Input, Icon, Button | icon, input, clear |
| FormField | Label, Input, Text | label, input, helper, error |
| CardHeader | Avatar, Heading, Text, IconButton | avatar, title, subtitle, actions |
| Alert | Icon, Text, Button | icon, content, action, close |
| Breadcrumb | Link, Icon | item, separator |
| Pagination | Button, Text, Select | prev, pages, next, size |
| TagList | Badge | item, remove |
| MenuItem | Icon, Text, KeyboardKey | icon, label, shortcut, chevron |
| Tooltip | Text | trigger, content |
| ToastContent | Icon, Heading, Text, Button | icon, title, description, action, close |

---

## 6. Organisms

### 6.1. Princípios

1. Seção grande da página (navegação, hero, card de produto, tabela).
2. Estado local permitido (expansão, filtros, ordenação).
3. Pode conhecer domínio (`ProductCard` sabe de Product).
4. Composto por molecules + atoms (raro chamar outro organism dentro).
5. Contexto de rota e URL é comum (`NavigationMenu` lê `usePathname`).

### 6.2. 8 exemplos

- **Header.** Logo + NavigationMenu + SearchField + UserMenu. Variants: `variant` (marketing, app, minimal), `sticky`.
- **Footer.** Logo + LinkGroups + SocialLinks + Copyright. Variants: `variant`, `columns` (2, 3, 4).
- **Hero.** Heading + Subheading + CTA + Visual. Variants: `layout` (split, centered, full-bleed), `alignment` (left, center).
- **ProductCard.** Image + Badge + Title + Price + Rating + CTA. Variants: `layout` (grid, list), `size`.
- **DataTable.** Toolbar (Search, Filters, Columns, Export) + Header + Rows + Pagination. Variants: `density` (compact, comfortable, spacious), `selectable`.
- **FormSection.** Legend + Description + FormFields + SubmitActions. Variants: `layout` (vertical, horizontal, grid), `columns`.
- **Sidebar.** Logo + NavigationMenu + UserCard + CollapseButton. Variants: `variant` (expanded, collapsed, hidden), `position` (left, right).
- **NavigationMenu.** Lista de Links ou MenuItems, suporta submenus, badges, ativo por rota. Variants: `orientation`, `style` (pills, underline, plain).

### 6.3. Tabela rápida

| Organism | Molecules principais | Estado local típico |
|----------|---------------------|---------------------|
| Header | NavigationMenu, SearchField, UserMenu | Mobile drawer |
| Footer | LinkGroups | Nenhum |
| Hero | CTA group | Nenhum |
| ProductCard | CardHeader, Price | Wishlist toggle |
| DataTable | FilterBar, Pagination, Row | Sort, filter, selection, page |
| FormSection | FormField | Errors, submitting |
| Sidebar | NavigationMenu, UserCard | Expand/collapse |
| NavigationMenu | MenuItem | Active submenu |

---

## 7. Templates

### 7.1. Propósito

Templates capturam **estrutura de página** sem dados. Wireframes vivos. O organism vai no slot. O conteúdo vem da page.

### 7.2. Anatomia

Três responsabilidades: grid/layout (CSS grid ou flex), slots nomeados (props tipadas recebem JSX), responsividade (breakpoints, comportamento mobile).

### 7.3. Exemplo

```tsx
type DashboardTemplateProps = {
  sidebar: ReactNode;
  header: ReactNode;
  main: ReactNode;
  footer?: ReactNode;
};

export function DashboardTemplate({ sidebar, header, main, footer }: DashboardTemplateProps) {
  return (
    <div className="grid grid-cols-[240px_1fr] grid-rows-[auto_1fr_auto] min-h-screen">
      <aside className="row-span-3 border-r">{sidebar}</aside>
      <header className="col-start-2 border-b">{header}</header>
      <main className="col-start-2 overflow-y-auto">{main}</main>
      {footer && <footer className="col-start-2 border-t">{footer}</footer>}
    </div>
  );
}
```

### 7.4. Quando criar

Crie template quando **mais de 2 páginas compartilham o mesmo layout**. Para one-offs, monte direto na page.

### 7.5. Templates comuns

| Template | Slots | Casos de uso |
|----------|-------|--------------|
| DashboardTemplate | sidebar, header, main, footer | App interno, admin |
| LandingTemplate | nav, hero, sections[], footer | Marketing |
| ArticleTemplate | nav, breadcrumb, article, sidebar | Blog, docs |
| CheckoutTemplate | header, main, summary, footer | Fluxo de compra |
| AuthTemplate | logo, content, footer | Login, signup |

---

## 8. Pages

### 8.1. Definição e responsabilidades

Pages são rotas concretas com dados. É onde fetchs acontecem, SEO é aplicado, analytics dispara. Responsabilidades: data fetching (SSR, SSG, ISR, client), escolha do template, preenchimento de slots com organisms com dados reais, SEO (`<title>`, meta tags, OG, JSON LD), analytics (page view, events), error boundaries.

### 8.2. Exemplo, Next.js App Router

```tsx
// app/dashboard/page.tsx
import { DashboardTemplate } from '@/templates/DashboardTemplate';
import { Sidebar } from '@/organisms/Sidebar';
import { Header } from '@/organisms/Header';
import { MetricsGrid } from '@/organisms/MetricsGrid';
import { getDashboardData } from '@/lib/data';

export default async function DashboardPage() {
  const data = await getDashboardData();
  return (
    <DashboardTemplate
      sidebar={<Sidebar user={data.user} />}
      header={<Header user={data.user} />}
      main={<MetricsGrid metrics={data.metrics} />}
    />
  );
}
```

### 8.3. Quando parar de compor

A page é a última estação. Dela, nada sobe. Se sente vontade de reusar algo da page em outra, promova para organism ou template.

---

## 9. Naming conventions por nível

### 9.1. Regras gerais

1. PascalCase no código (`Button`, não `button`).
2. kebab-case em arquivos quando o stack usa; consistência com o repositório.
3. Sem prefixo de nível (`AtomButton` não; pasta já indica).
4. Plural só para containers (`RadioGroup`, `Tabs`, `Menu`).
5. Compound components via dot notation (`Card.Header`, `Tabs.List`).

### 9.2. Por nível

| Nível | Convenção | Exemplo |
|-------|-----------|---------|
| Token | dot notation semântica | `color.bg.primary-default` |
| Atom | PascalCase, substantivo simples | `Button`, `Input` |
| Molecule | PascalCase, substantivo composto | `FormField`, `SearchField` |
| Organism | PascalCase, função ou domínio | `ProductCard`, `Sidebar` |
| Template | PascalCase + `Template` | `DashboardTemplate` |
| Page | Definido pelo router | `page.tsx` |

### 9.3. Variantes de nome vs variants

Quando um componente tem múltiplas formas radicais (não só um prop), use sufixo: `Button` e `IconButton`, `Modal` e `Drawer`, `Select` e `Combobox`, `Tooltip` e `Popover`. Se são variações suaves de forma, use prop `variant`.

### 9.4. Props convention

| Prop | Tipo | Semântica |
|------|------|-----------|
| `variant` | union | Mudança visual principal |
| `size` | union | sm, md, lg, xl |
| `tone` | union | Semântica de cor |
| `state` | union | Estado controlado |
| `as` | ElementType | Polymorphic tag |
| `children` | ReactNode | Slot default |
| `className` | string | Escape hatch, use com moderação |

---

## 10. Variant systems

### 10.1. Figma variants

No Figma, variants são propriedades nomeadas de um componente. Cada combinação gera um estado visual. Para Button: `variant` (primary, secondary, ghost, destructive) × `size` (sm, md, lg) × `state` (default, hover, focus, active, disabled, loading) = 72 permutações. Nem todas precisam existir, mas o espaço está mapeado.

**Práticas:** use Variables para tokens; divida em Base + States; prefixe variants técnicas (`_dev_only`, `_deprecated`); nomeie sem símbolos (`/`, `\` quebram export); crie Stories mostrando todas combinações relevantes.

### 10.2. Code variants com CVA

Em 2026 o padrão dominante para variants em código é `class-variance-authority` (CVA).

```tsx
import { cva, type VariantProps } from 'class-variance-authority';

const buttonVariants = cva(
  'inline-flex items-center justify-center font-medium transition-colors focus-visible:outline-2',
  {
    variants: {
      variant: {
        primary: 'bg-primary text-on-primary hover:bg-primary-hover',
        secondary: 'bg-surface text-primary border border-primary hover:bg-primary/10',
        ghost: 'text-primary hover:bg-primary/10',
        destructive: 'bg-danger text-on-danger hover:bg-danger-hover',
      },
      size: {
        sm: 'h-8 px-3 text-sm rounded-md',
        md: 'h-10 px-4 text-md rounded-md',
        lg: 'h-12 px-6 text-lg rounded-lg',
      },
      state: {
        default: '', loading: 'cursor-wait opacity-80', disabled: 'cursor-not-allowed opacity-50',
      },
    },
    defaultVariants: { variant: 'primary', size: 'md', state: 'default' },
  }
);

type ButtonProps = VariantProps<typeof buttonVariants> & { children: ReactNode; onClick?: () => void };

export function Button({ variant, size, state, children, onClick }: ButtonProps) {
  return (
    <button
      className={buttonVariants({ variant, size, state })}
      disabled={state === 'disabled' || state === 'loading'}
      onClick={onClick}
    >
      {state === 'loading' ? <Spinner size={size} /> : children}
    </button>
  );
}
```

### 10.3. Sincronizando Figma e código

Mesmos nomes (`primary`, não `Primary Azul`). Mesma ordem (default primeiro). Documente mapeamento em README (tabela Figma variant -> código prop). Automatize quando possível (Tokens Studio + Style Dictionary -> classes Tailwind -> CVA consome).

### 10.4. Limites do Figma

Figma variants não têm lógica (não expressam "se loading, mostra Spinner"), explodem combinações (5 variants × 3 valores = 243 frames) e não capturam estado controlado. Solução: cobrir no Figma as combinações usadas + um spec de referência; deixar o resto para código + storybook.

---

## 11. Composition patterns

### 11.1. Visão geral

Em 2026 dominam quatro padrões: `children` simples, props + slots (polymorphic), compound components (dot notation), render props / headless.

### 11.2. children simples

```tsx
<Card>
  <h2>Título</h2>
  <p>Conteúdo</p>
</Card>
```

Quando usar: componente genérico que não estrutura seu conteúdo. Limite: se exige posições específicas, `children` sozinho não garante.

### 11.3. Props + slots

```tsx
<Card header={<h2>Título</h2>} actions={<Button>Ação</Button>}>
  <p>Conteúdo</p>
</Card>
```

Quando usar: 2 a 4 posições fixas sem aninhamento complexo. Limite: verboso com muitos slots.

### 11.4. Compound components

Padrão dominante em DS modernos (Radix UI, shadcn/ui, Ark UI).

```tsx
<Tabs defaultValue="overview">
  <Tabs.List>
    <Tabs.Trigger value="overview">Visão geral</Tabs.Trigger>
    <Tabs.Trigger value="details">Detalhes</Tabs.Trigger>
  </Tabs.List>
  <Tabs.Content value="overview">Conteúdo da visão geral</Tabs.Content>
  <Tabs.Content value="details">Conteúdo dos detalhes</Tabs.Content>
</Tabs>
```

Vantagens: semântica clara; context compartilhado (sincronizar Trigger e Content); extensível; tipagem forte. Quando usar: 3+ partes interdependentes com contexto (Tabs, Accordion, Menu, Dialog, Combobox).

Implementação resumida:

```tsx
const TabsContext = createContext(null);
const useTabsContext = () => { const ctx = useContext(TabsContext); if (!ctx) throw new Error('Tabs.*'); return ctx; };

export function Tabs({ defaultValue, children }) {
  const [value, setValue] = useState(defaultValue);
  return <TabsContext.Provider value={{ value, setValue }}>{children}</TabsContext.Provider>;
}
Tabs.List = ({ children }) => <div role="tablist">{children}</div>;
Tabs.Trigger = ({ value: v, children }) => {
  const { value, setValue } = useTabsContext();
  return <button role="tab" aria-selected={value === v} onClick={() => setValue(v)}>{children}</button>;
};
Tabs.Content = ({ value: v, children }) => {
  const { value } = useTabsContext();
  return value === v ? <div role="tabpanel">{children}</div> : null;
};
```


### 11.5. Render props / headless

Componente expõe estado e handlers, consumidor controla a UI. Quando usar: comportamento genérico (combobox, dnd, virtualização) onde a UI varia drasticamente. Bibliotecas: Downshift, TanStack Table, React Aria, Ark UI.

### 11.6. Escolhendo o padrão

| Cenário | Padrão |
|---------|--------|
| Container genérico | `children` |
| 2 a 4 slots fixos | props + slots |
| 5+ partes com contexto compartilhado | Compound |
| Comportamento reutilizável, UI variável | Render props / headless |

### 11.7. Slot polymorphic com `as`

```tsx
<Button as="a" href="/sobre">Sobre</Button>
<Button as={Link} href="/dashboard">Dashboard</Button>
```

---

## 12. Anti patterns

### 12.1. Over-abstraction prematura

**Sintoma:** criar `FormField` na story 3, antes de ter 5 formulários. **Problema:** API desenhada sem dados reais de uso. **Regra:** 3 usos reais antes de extrair. Copy-paste 2 vezes é ok; na terceira, abstraia.

### 12.2. God-organism

**Sintoma:** um `Header` com 40 props que serve marketing, app, admin, mobile, checkout. **Problema:** qualquer mudança cascateia. **Regra:** split por variant primário (`MarketingHeader`, `AppHeader`, `CheckoutHeader`).

### 12.3. Confusão de nível

**Sintoma:** `ProductCard` (organism) importado solto em landing pages, que não deveria depender de `Product` type. **Regra:** organism conhece domínio, átomo não. Respeite a fronteira.

### 12.4. Variants que viram propriedades

**Sintoma:** `<Button isPrimary isLarge isLoading>` em vez de `<Button variant="primary" size="lg" state="loading">`. **Problema:** combinações inválidas possíveis em tipos. **Regra:** variants são unions, não booleanos.

### 12.5. Tokens hardcoded em átomos

**Sintoma:** `className="bg-blue-600 text-white"` dentro de `<Button>`. **Problema:** troca de tema impossível. **Regra:** átomos consomem apenas tokens (`bg-primary`, `text-on-primary`).

### 12.6. Composição forçada

**Sintoma:** `<Card><Card.Header><Card.Title>X</Card.Title></Card.Header></Card>` quando `<Card title="X">` bastaria. **Regra:** compound components para partes interdependentes com contexto. Para 1 a 2 slots sem estado, props simples.

### 12.7. Naming leakage

**Sintoma:** `ProductCardV2_NEW_FINAL`, `ButtonLegacy`. **Problema:** migração incompleta. **Regra:** feature flags ou deprecation warnings; um componente, caminho de migração claro, remoção em N semanas.

### 12.8. Variants infinitos

**Sintoma:** `Button` com 8 variants, 5 sizes, 6 tones, 4 states = 960 combinações. **Regra 3×3:** máximo 3 variants × 3 sizes × 3 tones. Se precisa mais, split em múltiplos componentes.

### 12.9. Escape hatches abusados

**Sintoma:** 60% dos usos de `Button` passam `className` custom. **Regra:** se passa de 20%, revise a API; falta variant ou token.

### 12.10. Esquecer responsividade

**Sintoma:** componentes lindos em desktop, quebrados em mobile (60%+ do tráfego em 2026). **Regra:** mobile-first nos variants; `size="md"` vira `sm` em breakpoint baixo.

---

## 13. Atomic Design + tokens

### 13.1. A camada 0

Tokens alimentam átomos, átomos alimentam moléculas. A consistência visual de um DS inteiro é função de: tokens bem desenhados (semânticos, não só literais); átomos que consomem **apenas** tokens; moléculas que consomem átomos + tokens; organisms que montam moléculas, tokens só para layout local.

### 13.2. Mapa de dependências

```
tokens.json (DTCG)
    │  [build: Style Dictionary]
    ▼
CSS vars + tailwind.config + figma-variables
    │
    ▼
atoms/ -> usam color.bg.primary, spacing.3, radius.md
    │
    ▼
molecules/ -> usam <Label>, <Input>, <Text>, spacing.2
    │
    ▼
organisms/ -> usam <SearchField>, <NavigationMenu>, layout tokens
```

### 13.3. Troca de tema

Tema claro/escuro ou multi-brand funciona porque tokens são substituíveis por camada semântica.

```json
{ "color": { "bg": { "primary": { "$value": "{color.blue.500}", "$type": "color" } } } }
```

Em tema escuro, `color.blue.500` pode virar outro tom. Componentes não mudam, só o mapeamento semântico -> core. Detalhe em `01-tokens-w3c-spec.md`, seção 6.

### 13.4. Ciclo de atualização

1. Update em `tokens.json`. 2. `npm run tokens:build` gera CSS vars + dicionário JS. 3. Componentes consomem novo valor (sem rebuild). 4. Figma puxa via Tokens Studio sync. 5. Testes visuais (Chromatic, Percy) capturam diffs.

### 13.5. Regra de ouro

Se um componente usa um literal (cor, espaço, fonte) que não vem de token, é bug. Lint rules (stylelint, `eslint-plugin-tailwind`) podem bloquear no CI.

---

## 14. Migração entre níveis

### 14.1. Sinais para promover

**Molecule -> Organism:** ganhou estado local complexo (filters, sort, selection); consome contexts de domínio (`useUser`, `useCart`); precisou de lógica de fetch ou mutation; passou de 150 linhas. Exemplo: `<SearchField>` vira `<SearchDropdown>` quando ganha sugestões API, debounce, histórico.

**Organism -> Template:** raro. Só quando o organism vira layout de página completa com slots expostos.

### 14.2. Sinais para rebaixar

**Organism -> Molecule:** removeu contexto de domínio; virou puramente visual; passou a ser reutilizado em contextos não relacionados.

**Molecule -> Atom:** colapsou para 1 átomo wrapper; perdeu composição significativa. Exemplo: `<IconButton>` começa molecule, mas vira wrapper trivial do `Button` com `variant="icon"` e migra para atom.

### 14.3. Processo

1. Identifique sinais (code review, métricas de uso, feedback). 2. Proponha na RFC (motivação, impacto, plano). 3. Implemente em paralelo (novo convive com antigo por 1-2 sprints). 4. Migre consumidores (codemod quando possível, `jscodeshift`). 5. Remova antigo após 100% migrado.

### 14.4. Codemod exemplo

```js
// Migra <SearchField withDropdown> para <SearchDropdown>
module.exports = function transformer(file, api) {
  const j = api.jscodeshift;
  const root = j(file.source);
  root.findJSXElements('SearchField').forEach(path => {
    const hasDropdownProp = path.value.openingElement.attributes.some(
      attr => attr.name && attr.name.name === 'withDropdown'
    );
    if (hasDropdownProp) {
      path.value.openingElement.name.name = 'SearchDropdown';
      path.value.closingElement.name.name = 'SearchDropdown';
    }
  });
  return root.toSource();
};
```

### 14.5. Comunicação

Migrações quebram a pasta de origem. Comunicar: release notes; CHANGELOG semver (minor se caminho de migração limpo, major se breaking); banner no site do DS por 30 dias; `console.warn` com link para docs.

---

## 15. 12 componentes end to end

Para cada: Figma structure, code API, tokens usados, do/don't.

### 15.1. Button (atom)

**Figma:** variants `variant` (primary, secondary, ghost, destructive) × `size` (sm, md, lg) × `state` (default, hover, focus, disabled, loading). Children: `[Icon]?`, `Label`, `[Icon]?`, `[Spinner]?`.

```tsx
<Button variant="primary" size="md" onClick={handleClick}>Continuar</Button>
<Button variant="secondary" size="sm" leftIcon="arrow-left">Voltar</Button>
<Button variant="ghost" size="lg" state="loading">Processando</Button>
```

**Tokens:** `color.bg.primary`, `color.bg.primary-hover`, `color.text.on-primary`, `color.border.primary`, `radius.md`, `spacing.3`, `spacing.4`, `typography.label.md`.

**Do:** `variant="primary"` para ação principal (1 por tela); combine com ícone só quando agrega semântica; min-height 44px em mobile. **Don't:** 2 primary na mesma tela (ambiguidade); customizar `className` para cor (use variant); texto longo (>3 palavras, vire link).

### 15.2. Card (atom com slots)

**Figma:** variants `variant` (default, elevated, outlined) × `padding` (none, sm, md, lg). Slots: `header?`, `media?`, `body`, `footer?`.

```tsx
<Card variant="elevated" padding="md">
  <Card.Header>
    <Heading>Título</Heading>
    <Text tone="muted">Subtítulo</Text>
  </Card.Header>
  <Card.Body>Conteúdo principal.</Card.Body>
  <Card.Footer><Button variant="primary">Ação</Button></Card.Footer>
</Card>
```

**Tokens:** `color.bg.surface`, `color.bg.surface-elevated`, `color.border.subtle`, `shadow.sm`, `shadow.md`, `radius.lg`, `spacing.4`, `spacing.6`.

**Do:** compound components para estruturar; padding via token; limite altura em grid. **Don't:** aninhar cards; customizar radius por instância; usar card para containers genéricos.

### 15.3. Form (organism)

**Figma:** `Form` (container) > `FormSection` > `FormField` (molecule) > Label + Input + HelperText + ErrorMessage. `FormActions` com Button cancel + submit.

```tsx
<Form onSubmit={handleSubmit}>
  <FormSection legend="Dados pessoais" description="Preencha seus dados.">
    <FormField name="name">
      <FormField.Label required>Nome</FormField.Label>
      <FormField.Input /><FormField.Error />
    </FormField>
    <FormField name="email">
      <FormField.Label required>Email</FormField.Label>
      <FormField.Input type="email" />
      <FormField.Helper>Usamos para enviar atualizações.</FormField.Helper>
      <FormField.Error />
    </FormField>
  </FormSection>
  <FormActions>
    <Button variant="ghost" type="button" onClick={handleCancel}>Cancelar</Button>
    <Button variant="primary" type="submit">Salvar</Button>
  </FormActions>
</Form>
```

**Tokens:** `spacing.4`, `spacing.6`, `color.text.primary`, `color.text.muted`, `color.text.danger`, `typography.label.sm`, `typography.body.md`.

**Do:** FormSection para agrupar; mostrar `required` visualmente; desabilitar submit durante `submitting`. **Don't:** 1 coluna se muitos campos (use grid 2 col em desktop); esconder labels; misturar padrões de validação (realtime vs onSubmit).

### 15.4. Modal (molecule)

**Figma:** variants `size` (sm, md, lg, full) × `variant` (default, danger). Parts: Overlay + Container (Header com Title + CloseButton; Body; Footer com Actions).

```tsx
<Modal open={isOpen} onClose={setClose} size="md">
  <Modal.Header><Modal.Title>Confirmar exclusão</Modal.Title></Modal.Header>
  <Modal.Body>Essa ação não pode ser desfeita. Deseja continuar?</Modal.Body>
  <Modal.Footer>
    <Button variant="ghost" onClick={setClose}>Cancelar</Button>
    <Button variant="destructive" onClick={handleDelete}>Excluir</Button>
  </Modal.Footer>
</Modal>
```

**Tokens:** `color.bg.surface`, `color.bg.overlay`, `shadow.xl`, `radius.lg`, `spacing.6`, `spacing.8`.

**Do:** focar no primeiro elemento interativo; fechar com ESC e clique fora; body lock no background; `role="dialog"` com `aria-labelledby`. **Don't:** modal dentro de modal; formulário longo em modal (use drawer ou página); desabilitar fechamento sem razão forte.

### 15.5. Table (organism)

**Figma:** `DataTable` > Toolbar (SearchField + FilterButton + ExportMenu + ColumnSelector) + Table (Header com HeaderCell sortable, Body com Row selectable, cells) + Pagination.

```tsx
<DataTable
  data={orders}
  columns={[
    { key: 'id', label: 'Pedido', sortable: true },
    { key: 'customer', label: 'Cliente' },
    { key: 'total', label: 'Total', align: 'right', format: 'currency' },
    { key: 'status', label: 'Status', render: (v) => <Badge variant={statusColor(v)}>{v}</Badge> },
  ]}
  density="comfortable" selectable
  onRowClick={handleRowClick}
  pagination={{ pageSize: 25, total: 500 }}
  toolbar={{ search: true, filters: true, columns: true, export: true }}
/>
```

**Tokens:** `color.bg.surface`, `color.bg.row-hover`, `color.border.subtle`, `spacing.3` (comfortable), `spacing.2` (compact), `typography.body.sm`.

**Do:** cabeçalho sticky em tables longas; sort server-side em datasets grandes; keyboard nav (arrow, enter); empty state claro. **Don't:** renderizar tudo client-side com 10k+ linhas (virtualize); esconder colunas críticas em mobile (use cards); misturar densities na mesma tabela.

### 15.6. Nav (organism)

**Figma:** `NavigationMenu` variants `orientation` (horizontal, vertical) × `style` (pills, underline, plain) × `size` (sm, md, lg). Children: `MenuItem` x N (active if route matches), com Icon?, Label, Badge?, Submenu?.

**Code:**
```tsx
<NavigationMenu orientation="horizontal" style="underline" size="md">
  <NavigationMenu.Item href="/dashboard" icon="home">Dashboard</NavigationMenu.Item>
  <NavigationMenu.Item href="/orders" icon="package" badge={pendingOrders}>Pedidos</NavigationMenu.Item>
  <NavigationMenu.Item href="/customers" icon="users">Clientes</NavigationMenu.Item>
  <NavigationMenu.Item href="/reports" icon="chart">Relatórios
    <NavigationMenu.Submenu>
      <NavigationMenu.Item href="/reports/sales">Vendas</NavigationMenu.Item>
      <NavigationMenu.Item href="/reports/traffic">Tráfego</NavigationMenu.Item>
    </NavigationMenu.Submenu>
  </NavigationMenu.Item>
</NavigationMenu>
```

**Tokens:** `color.text.nav`, `color.text.nav-active`, `color.bg.nav-hover`, `spacing.3`, `spacing.4`, `typography.label.md`.

**Do:** rota ativa com `aria-current="page"`; keyboard nav (tab + arrows); skip link para acessibilidade.

**Don't:** cores custom para ativo; esconder navegação principal atrás de hover sem clique; submenus com mais de 2 níveis.

### 15.7. Hero (organism)

**Figma:** variants `layout` (split, centered, full-bleed) × `alignment` (left, center, right) × `theme` (light, dark). Parts: Content (Eyebrow?, Heading h1, Subheading, Actions 1-2 buttons, SocialProof?) + Visual.

**Code:**
```tsx
<Hero layout="split" alignment="left" theme="light">
  <Hero.Content>
    <Hero.Eyebrow>Novo</Hero.Eyebrow>
    <Hero.Heading>Automação de marketing sem código</Hero.Heading>
    <Hero.Subheading>Orquestre campanhas em múltiplos canais com IA.</Hero.Subheading>
    <Hero.Actions>
      <Button variant="primary" size="lg">Começar grátis</Button>
      <Button variant="ghost" size="lg">Ver demo</Button>
    </Hero.Actions>
    <Hero.SocialProof><Avatar.Group>...</Avatar.Group><Text>+5.000 times usam</Text></Hero.SocialProof>
  </Hero.Content>
  <Hero.Visual><img src="/dashboard.webp" alt="" /></Hero.Visual>
</Hero>
```

**Tokens:** `color.bg.hero`, `color.text.hero`, `spacing.16`, `spacing.24`, `typography.display.lg`, `typography.heading.md`.

**Do:** 1 CTA primária + 1 secundária (máximo); heading 6-12 palavras; visual com `loading="eager"` se above the fold.

**Don't:** 3+ CTAs (dispersão); gradientes muito saturados; vídeo autoplay com áudio.

### 15.8. Search (molecule)

**Figma:** variants `size` (sm, md, lg) × `variant` (inline, expanded). Parts: Icon (search) + Input + ClearButton? + SubmitButton? (se explícito).

**Code:**
```tsx
<SearchField
  size="md"
  variant="inline"
  placeholder="Buscar..."
  value={query}
  onChange={setQuery}
  onClear={() => setQuery('')}
/>

// Versão promovida a organism
<SearchDropdown
  items={results}
  isLoading={isLoading}
  onSelect={handleSelect}
  placeholder="Buscar..."
  recentSearches={recent}
/>
```

**Tokens:** `color.bg.input`, `color.border.default`, `color.border.focus`, `spacing.2`, `spacing.3`, `radius.md`, `radius.full`.

**Do:** debounce 200-300ms; empty state com ação clara; suportar ESC para limpar.

**Don't:** buscar com 0 caracteres; aceitar menos de 2 normalmente; perder foco após resultado aparecer.

### 15.9. Pagination (molecule)

**Figma:** variants `variant` (simple, full, compact) × `size` (sm, md). Parts: PrevButton + PageInfo (texto ou botões numerados) + NextButton + PageSizeSelect?.

**Code:**
```tsx
<Pagination
  currentPage={page} totalPages={totalPages} totalItems={totalItems}
  pageSize={pageSize} pageSizeOptions={[10, 25, 50, 100]}
  onPageChange={setPage} onPageSizeChange={setPageSize}
  variant="full" size="md"
/>
```

**Tokens:** `color.text.muted`, `color.bg.page-active`, `spacing.1`, `spacing.2`, `typography.body.sm`.

**Do:** desabilitar prev/next em extremos; mostrar total para contexto; keyboard nav (left/right).

**Don't:** mostrar todos os números se >20 páginas (use "..."); trocar page sem feedback de loading; usar em dataset pequeno (<25 itens).

### 15.10. Alert (molecule)

**Figma:** variants `severity` (info, success, warning, danger) × `variant` (soft, solid, outline) × `dismissible`. Parts: Icon + Content (Title?, Description) + Action? + CloseButton?.

**Code:**
```tsx
<Alert severity="warning" variant="soft" dismissible onDismiss={handleDismiss}>
  <Alert.Title>Sessão prestes a expirar</Alert.Title>
  <Alert.Description>Sua sessão expira em 5 minutos. Salve seu trabalho.</Alert.Description>
  <Alert.Action onClick={renewSession}>Renovar sessão</Alert.Action>
</Alert>
```

**Tokens:** `color.bg.info-soft`, `color.bg.success-soft`, `color.bg.warning-soft`, `color.bg.danger-soft`, correspondentes de texto, `spacing.3`, `spacing.4`, `radius.md`.

**Do:** icon apropriado por severity; mensagem acionável; `role="alert"` para danger, `role="status"` para info/success.

**Don't:** empilhar 5 alerts simultâneos; danger para validação inline (use inline error); alerts bloqueantes sem ação para sair.

### 15.11. Avatar (atom)

**Figma:** variants `size` (xs, sm, md, lg, xl, 2xl) × `shape` (circle, square) × `status` (none, online, offline, busy, away). Parts: Image + Fallback (initials) + StatusDot? + Ring?.

**Code:**
```tsx
<Avatar src="/user.jpg" alt="João Silva" fallback="JS" size="md" shape="circle" status="online" />

<Avatar.Group max={3}>
  <Avatar src="/a.jpg" alt="A" /><Avatar src="/b.jpg" alt="B" />
  <Avatar src="/c.jpg" alt="C" /><Avatar src="/d.jpg" alt="D" />
</Avatar.Group>
// Renderiza A, B, C + "+1"
```

**Tokens:** `color.bg.avatar-fallback`, `color.border.avatar-ring`, `color.bg.status-online`, `color.bg.status-busy`, `radius.full`, `radius.md`, `typography.label.xs` até `typography.label.lg`.

**Do:** sempre ter fallback; lazy load em grid; alt descritivo ("Foto de João Silva").

**Don't:** sem alt text; cores de ring que conflitam com DS; avatar como botão sem affordance visual.

### 15.12. Tabs (molecule)

**Figma:** variants `orientation` (horizontal, vertical) × `style` (underline, pills, enclosed) × `size` (sm, md, lg). Parts: TabsList > TabsTrigger (active, inactive, disabled) + TabsContent x N.

**Code:**
```tsx
<Tabs defaultValue="overview" orientation="horizontal" style="underline">
  <Tabs.List>
    <Tabs.Trigger value="overview">Visão geral</Tabs.Trigger>
    <Tabs.Trigger value="activity">Atividade</Tabs.Trigger>
    <Tabs.Trigger value="settings">Configurações</Tabs.Trigger>
    <Tabs.Trigger value="danger" tone="danger">Excluir conta</Tabs.Trigger>
  </Tabs.List>
  <Tabs.Content value="overview"><MetricsGrid metrics={metrics} /></Tabs.Content>
  <Tabs.Content value="activity"><ActivityFeed items={activities} /></Tabs.Content>
  <Tabs.Content value="settings"><SettingsForm /></Tabs.Content>
  <Tabs.Content value="danger"><DangerZone /></Tabs.Content>
</Tabs>
```

**Tokens:** `color.text.tab`, `color.text.tab-active`, `color.border.tab-active`, `spacing.4`, `spacing.6`, `typography.label.md`.

**Do:** roles `tablist`, `tab`, `tabpanel` com aria-controls; keyboard nav (arrows); lazy render de content; sync com URL via `?tab=overview` quando deep-linking importa.

**Don't:** tabs para conteúdo sequencial (use wizard); 7+ tabs (use dropdown ou sidebar); animar transição sem reduce-motion check.

---

## 16. FAQ

**16.1. Preciso seguir Atomic Design à risca?** Não. Use como mapa mental. Em 2026 times maduros adaptam: 6 níveis, nomenclatura pragmática, fronteira molecule/organism flexível.

**16.2. Onde vive Card?** Atom com slots, na maioria dos DS. Vira molecule quando compound components com children obrigatórios (`Card.Header`, `Card.Body`).

**16.3. E se um componente não cabe em nenhum nível?** Investigue: provavelmente mistura responsabilidades. Split em 2. Se persistir, pode ser template ou utility/provider que não é UI.

**16.4. Devo criar pasta por nível?** Sim, recomendado. Ou por domínio com nível como tag no arquivo. A primeira é mais explícita, a segunda escala melhor com muitos componentes.

**16.5. Como nomeio variantes?** Se pequenas (cor, tamanho), prop `variant`/`size`. Se estruturais (só ícone vs texto+ícone), componentes irmãos (`Button`, `IconButton`).

**16.6. Quando criar compound components?** Quando há 3+ partes interdependentes com contexto compartilhado (Tabs, Accordion, Menu, Dialog). Para 1-2 slots sem estado, props simples.

**16.7. Storybook é obrigatório?** Não obrigatório, mas recomendado para atoms e molecules. Para organisms e acima, muitos times usam Ladle (mais rápido) ou docs com exemplos.

**16.8. Como testo cada nível?** Tokens: snapshot de `tokens.json`. Atoms: unit tests (Vitest), testing-library. Molecules: unit + acessibilidade (axe). Organisms: integração (MSW). Templates: snapshot visual (Chromatic). Pages: E2E (Playwright).

**16.9. Adoção em time pequeno?** Time de 2-5 devs sem DS dedicado: camada 0 (tokens) + camadas 1-3 (atoms, molecules, organisms). Pule templates formais, componha inline nas pages.

**16.10. Quando Atomic Design não serve?** Apps one-off pequenos (<10 telas); prototipação rápida; sites estáticos simples. Para tudo acima, o mapa mental vale a disciplina.

**16.11. E tokens sem Atomic Design?** Funciona parcialmente. Tokens dão consistência visual, Atomic Design dá consistência estrutural. Os dois juntos são mais que soma das partes.

**16.12. Referências.** Brad Frost, `atomicdesign.bradfrost.com`. Nathan Curtis, série "Components, Patterns, and Subatomic Design" no Medium. Vitaly Friedman, Smashing Magazine. Radix UI primitives, Ark UI, shadcn/ui (implementações de referência). `references/design/01-tokens-w3c-spec.md` (camada 0).

---

**Fim do documento.**
