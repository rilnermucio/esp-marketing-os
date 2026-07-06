# 07. Figma MCP Playbook, Companion

> Parte da stack de companions do `design-agent` (v4.0).
> Guia aplicado sobre o uso eficaz das skills Figma MCP (Model Context Protocol) disponíveis no Marketing OS.

**Quando consultar:** ao operar a integração Figma MCP, decidir qual skill invocar, estruturar prompts para writes no canvas, configurar Code Connect, implementar design Figma em código, publicar biblioteca de DS ou resolver falhas de invocação.

**Pré-requisitos:** `references/design/01-tokens-w3c-spec.md` (tokens que as skills consomem), `references/design/08-shadcn-radix-recipes.md` (padrões de código-alvo), `references/design/09-design-handoff-to-code.md` (processo handoff) e acesso ao Figma Dev Mode com plano que habilita MCP.

---

## Índice

1. O ecossistema Figma MCP 2026
2. Decision tree, qual skill usar
3. Ordem correta de build do DS
4. Prompt patterns que funcionam
5. Prompt patterns que falham
6. Setup inicial
7. Workflow 1, code para Figma library
8. Workflow 2, Figma design para production code
9. Workflow 3, page from code para Figma screen
10. Workflow 4, design system rules
11. Workflow 5, Code Connect
12. Common gotchas
13. Handoff designer para dev
14. Troubleshooting

---

## 1. O ecossistema Figma MCP 2026

### 1.1. O que é MCP em Figma

Model Context Protocol (MCP) é o padrão aberto criado pela Anthropic que permite que LLMs conversem com servidores externos via ferramentas tipadas. A Figma expõe um MCP server que dá acesso programático ao canvas, variables, styles, components e libraries de um arquivo aberto no Dev Mode.

Na prática, isso significa que um agente pode ler a estrutura do arquivo, criar nós, vincular tokens a propriedades, gerar variants e publicar bibliotecas sem que o humano precise clicar manualmente no app. O humano continua sendo o revisor final.

### 1.2. Skills disponíveis

O Marketing OS tem seis skills Figma MCP instaladas. Cada uma encapsula um conjunto de capacidades diferentes e tem seu próprio contrato de input e output.

| Skill | Direção | Resumo |
|-------|---------|--------|
| `figma:figma-use` | Prereq | Carrega a API do plugin para executar JavaScript no contexto do arquivo. Obrigatória antes de qualquer write. |
| `figma:figma-generate-library` | Código para Figma | Constrói ou atualiza DS no Figma a partir de codebase. Gera variables, components, theming. |
| `figma:figma-generate-design` | Código para Figma | Traduz uma página ou view existente em código para uma screen Figma completa. |
| `figma:figma-implement-design` | Figma para código | Traduz design Figma para código de produção com fidelidade 1:1. |
| `figma:figma-code-connect` | Bi-direcional | Cria e mantém arquivos `.figma.ts` que mapeiam components Figma para snippets de código. |
| `figma:figma-create-design-system-rules` | Meta | Gera rules customizadas de DS para o projeto, orientando o comportamento das outras skills. |

### 1.3. Quando usar vs UI tradicional do Figma

Use MCP quando:

- Está construindo ou atualizando DS em lote (dezenas de components ou variables).
- Precisa de reprodutibilidade ou versionamento via código.
- Tem codebase maduro e quer refletir DS no Figma sem trabalho manual.
- Está implementando telas Figma em React e quer fidelidade 1:1.
- Quer estabelecer Code Connect em escala.

Use UI tradicional do Figma quando:

- Está explorando ideias visuais em alta liberdade.
- O trabalho é de polimento estético que requer sensibilidade humana direta.
- O arquivo é pequeno e a curva de aprendizado da MCP não compensa.
- Falta integração com codebase.

---

## 2. Decision tree, qual skill usar

A pergunta que decide a skill correta vem do resultado desejado, não da ferramenta disponível.

```
Preciso construir DS do zero no Figma a partir do meu código?
  SIM -> figma:figma-generate-library (+ figma:figma-use como prereq)
  NAO -> segue

Preciso implementar design existente no Figma em React e produção?
  SIM -> figma:figma-implement-design
  NAO -> segue

Preciso criar um mock Figma baseado em uma página web que ja existe?
  SIM -> figma:figma-generate-design (+ figma:figma-use como prereq)
  NAO -> segue

Preciso conectar components Figma a snippets de código via Code Connect?
  SIM -> figma:figma-code-connect
  NAO -> segue

Preciso de rules customizadas para orientar as outras skills no meu projeto?
  SIM -> figma:figma-create-design-system-rules
  NAO -> segue

Preciso apenas executar JavaScript via API do Figma para operações de write?
  SIM -> figma:figma-use (obrigatoriamente antes de qualquer use_figma)
  NAO -> revisar premissas, talvez UI tradicional resolva
```

### 2.1. Tabela comparativa detalhada

| Skill | Input típico | Output típico | Duração estimada |
|-------|--------------|---------------|------------------|
| `figma-use` | Instrução curta explicando write desejado | Plugin API carregada na sessão | Instantâneo |
| `figma-generate-library` | `tokens.json` + diretório de components | Arquivo Figma com variables, components e variants | 30 a 90 min |
| `figma-generate-design` | URL de página web ou JSX + referência de DS | Screen Figma completa com tokens vinculados | 10 a 40 min |
| `figma-implement-design` | URL Figma (arquivo e node) | React component com fidelidade 1:1 | 5 a 30 min |
| `figma-code-connect` | Component path + Figma node URL | Arquivo `.figma.tsx` sincronizado | 2 a 10 min por component |
| `figma-create-design-system-rules` | Descrição do projeto + convenções | Arquivo `design-system-rules.md` customizado | 15 a 30 min |

---

## 3. Ordem correta de build do DS

Construir DS no Figma exige ordem. A camada anterior alimenta a próxima e inverter a ordem cria retrabalho.

### 3.1. Sequência canônica

1. **Variables.** Primitivas e semânticas. Cor, spacing, radius, duração de motion.
2. **Styles.** Text styles, effect styles (shadows, blurs), grid styles. Consomem variables.
3. **Components.** Button, Input, Card. Consomem variables e styles.
4. **Variants.** Estados (default, hover, disabled), tamanhos (sm, md, lg), intenções (primary, secondary, destructive).
5. **Libraries.** Publicação que torna os artefatos consumíveis em outros arquivos da organização.

### 3.2. Por que essa ordem

Se você cria Button antes das cor variables, os fills ficam hardcoded. Quando for trocar a paleta, será um achar-e-substituir manual em centenas de nós. Se você cria variants antes dos components base, os variants ficam desalinhados e a matriz de estados explode.

O fluxo variables primeiro é o mesmo padrão que o Style Dictionary usa em código e que o W3C Design Tokens Group recomenda na spec 2025.10 (ver `01-tokens-w3c-spec.md` §§ 6, 11).

### 3.3. Checkpoint entre camadas

Depois de cada camada, pare e valide antes de seguir.

- Após variables: confira se todas as referências semânticas têm valor primitivo mapeado.
- Após styles: aplique um style em um nó de teste e mude a variable para ver se propaga.
- Após components: crie instância e veja se override de variable respeita a intenção.
- Após variants: gere combinações extremas (primary large disabled) para checar visual.

---

## 4. Prompt patterns que funcionam

Prompts efetivos são específicos, referenciam artefatos existentes e definem o escopo com precisão.

### 4.1. Padrão 1, referenciar tokens existentes

**Bom:**

```
Invoke figma:figma-generate-library to build a Button component with
3 variants (primary, secondary, destructive) and 3 sizes (sm, md, lg).
Use existing color variables under collection "Brand/Intent" and
spacing variables under "Scale/Spacing". Radius token is "radius.md".
Text style is "Body/Medium".
```

Por que funciona: nomeia coleções, tokens e styles concretos. A skill resolve referências sem inventar.

### 4.2. Padrão 2, delimitar escopo com lista fechada

**Bom:**

```
Implement the Figma design at <FIGMA_URL>#node-id=123-456 as a React
component. Target file: src/components/Card.tsx. Use ONLY components
from @/components/ui (shadcn). Tailwind classes from tailwind.config.ts
tokens. No external dependencies.
```

Por que funciona: define alvo, import paths permitidos e proíbe invenções.

### 4.3. Padrão 3, especificar dimensões de variant

**Bom:**

```
Create variants for the Input component along 2 axes:
- state: default, focused, disabled, error
- size: sm (32px), md (40px), lg (48px)
Result is a 4x3 matrix (12 variants total).
Error state uses color.error.base as border and color.error.text for label.
```

Por que funciona: matriz explícita, tokens nomeados, contagem esperada.

### 4.4. Padrão 4, pedir diff antes de write

**Bom:**

```
Before writing anything, summarize in markdown:
1. What will be created (list of nodes)
2. What will be modified (list of existing nodes)
3. Variable bindings to be established
Then pause for my approval.
```

Por que funciona: dá controle antes de operação destrutiva no arquivo.

### 4.5. Padrão 5, citar arquivo de código como fonte de verdade

**Bom:**

```
Source of truth: design-tokens/tokens.json (W3C DTCG format).
Sync this into Figma as variables. Primitives go into "Core/Primitives"
collection. Semantic go into "Core/Semantic". Preserve alias references
with {group.name} syntax.
```

Por que funciona: ancora a skill em artefato existente, evita inferência.

---

## 5. Prompt patterns que falham

### 5.1. Antipadrão 1, pedido vago

**Ruim:**

```
Crie um DS no Figma para o meu projeto.
```

Por que falha: sem escopo, sem tokens, sem convenção. A skill tenta adivinhar e o resultado é genérico.

**Correção:** comece pela lista explícita de artefatos (variables, N components, quais variants) e cite fontes.

### 5.2. Antipadrão 2, assumir contexto

**Ruim:**

```
Aplique nosso DS padrão no Button.
```

Por que falha: "DS padrão" é referência externa que a skill não resolve. Ela não conhece seus arquivos sem que você nomeie.

**Correção:** cite caminho do repositório, URL do Figma, ou handle específico.

### 5.3. Antipadrão 3, variants sem dimensões

**Ruim:**

```
Crie todas as variants possíveis do Button.
```

Por que falha: "todas" é infinito. A skill pode gerar 6 ou 60 variants, nenhuma das duas é o que você quer.

**Correção:** use matriz N x M com valores nomeados (§4.3).

### 5.4. Antipadrão 4, pular o prereq

**Ruim:**

```
Use use_figma para criar o Button.
```

Por que falha: `use_figma` é tool, não skill. Sem invocar `figma-use` primeiro, a chamada falha com erro obscuro de contexto não carregado.

**Correção:** invoque `figma:figma-use` antes de qualquer `use_figma`. Essa ordem é obrigatória.

### 5.5. Antipadrão 5, pedir implementação sem DS alvo

**Ruim:**

```
Implement this Figma design as React.
```

Por que falha: sem especificar biblioteca UI, tokens, e paths, o agente pode importar shadcn numa base que usa MUI. Ou inventar tokens.

**Correção:** declare explicitamente a stack (ver §4.2).

---

## 6. Setup inicial

### 6.1. Pré-requisitos de conta

- Plano Figma com Dev Mode habilitado (Professional ou Organization).
- MCP server da Figma ativo (Settings > Experiments > MCP server).
- Node.js 18+ e package manager do projeto (npm, pnpm ou yarn).
- Figma CLI instalada, se for usar Code Connect.

### 6.2. Conexão MCP server ao Claude Code

O Marketing OS gerencia MCPs via `.mcp.json` na raiz do projeto. O Figma MCP é adicionado editando esse arquivo ou via `claude mcp add figma`:

```
claude mcp add figma
```

Após adição, o agente roda `gh auth status` equivalente para Figma e retorna `mcp: figma connected` quando tudo está verde.

### 6.3. Autenticação

Figma MCP autentica via personal access token ou OAuth app. Para uso individual, o token gerado em Figma Settings > Account > Personal access tokens resolve. Para equipe, configure OAuth no painel de admin.

O token deve ter escopos: `files:read`, `variables:write`, `components:write`, `code_connect:write`.

### 6.4. Validação pós setup

Rode um ping simples para confirmar que a skill está viva:

```
Invoke figma:figma-use with a read-only probe:
  list the top 5 nodes of the currently open Figma file
  and return their IDs, names, and types.
```

Se voltar JSON estruturado com IDs dos nós, está operacional. Se voltar erro ou timeout, verifique token e Dev Mode ativo.

---

## 7. Workflow 1, code para Figma library

### 7.1. Objetivo

Transformar um codebase com tokens e components em uma biblioteca Figma publicada, onde cada component do código tem equivalente vivo no canvas.

### 7.2. Inputs

- `design-tokens/tokens.json` no formato W3C DTCG.
- Diretório `src/components/ui/` com componentes shadcn ou equivalente.
- URL de um arquivo Figma vazio ou existente onde publicar a library.

### 7.3. Invocação

```
Load figma:figma-use and figma:figma-generate-library.

Context:
  - Tokens source: /design-tokens/tokens.json (DTCG)
  - Components source: /src/components/ui/
  - Target Figma file: https://figma.com/file/ABC123
  - Collection names:
      Primitives -> "Core/Primitives"
      Semantic   -> "Core/Semantic"
      Themes     -> "Theme/Light", "Theme/Dark"

Plan:
  1. Create variable collections
  2. Import token values, preserving DTCG $type and $value
  3. Create text styles from typography tokens
  4. Build components in order: Button, Input, Card, Badge
  5. For each component, create variants along axes defined in code
  6. Publish library when complete

Before any write, print the plan summary and wait for approval.
```

### 7.4. Output esperado

- Arquivo Figma com collections populadas.
- Text styles aplicados e vinculados a variables.
- Components matching component props do código.
- Relatório markdown listando o que foi criado, modificado e pulado.

### 7.5. Validação

Abra o arquivo no Figma, escolha um component, confira:

- Fill do component referencia variable, não valor raw.
- Variants têm nomes iguais aos props do React (ex. `variant=primary`, não `primary-v1`).
- Text styles aplicam Inter (ou a família definida) com size e line height tokenizados.

---

## 8. Workflow 2, Figma design para production code

### 8.1. Objetivo

Traduzir uma tela desenhada no Figma em componentes React prontos para merge, com fidelidade 1:1 e sem refatoração adicional.

### 8.2. Inputs

- URL completa do Figma apontando para o node específico (arquivo e node-id).
- Stack do projeto (React 18, Next.js 15, Tailwind 3, shadcn/ui).
- Path de destino no repositório.

### 8.3. Invocação

```
Invoke figma:figma-implement-design.

Source: https://figma.com/file/XYZ789?node-id=12-345
Target: src/app/pricing/page.tsx
Stack:
  - Next.js App Router
  - Tailwind CSS 3.4
  - shadcn/ui components (import from @/components/ui)
  - Tokens from tailwind.config.ts (colors.brand.*, spacing.*)

Constraints:
  - No inline styles
  - No new dependencies
  - Accessible (WCAG 2.2 AA, see companion 04)
  - Responsive (mobile-first, breakpoints sm/md/lg)

Produce:
  1. The .tsx file (single component)
  2. A diff view vs existing page.tsx if present
  3. List of missing tokens or components that need to be added first
```

### 8.4. Output esperado

- Arquivo `page.tsx` ou `Component.tsx` com estrutura JSX que espelha as hierarquias do Figma.
- Imports apenas do que está declarado no stack.
- Relatório de gaps: tokens faltando, components não existentes, decisões que o agente tomou.

### 8.5. Validação

Rode `pnpm dev`, abra no browser, compare lado a lado com o Figma. Ferramenta recomendada: Pixelparallel ou Perfect Pixel para overlay.

---

## 9. Workflow 3, page from code para Figma screen

### 9.1. Objetivo

Criar um mock Figma a partir de uma página existente em código, útil quando design foi feito direto em código e precisa ser documentado no Figma para handoff, marketing ou arquivamento.

### 9.2. Inputs

- URL da página em produção ou dev local.
- Identificação do DS Figma que deve ser usado (library e collection).

### 9.3. Invocação

```
Load figma:figma-use and figma:figma-generate-design.

Source: https://app.example.com/dashboard
Target file: https://figma.com/file/DEF456
Target page: "Screens/Dashboard v2"

Design system reference:
  - Library "Acme DS" (published)
  - Use existing components, do NOT create new ones
  - If a UI element has no equivalent, note it in the report

Generation mode:
  - Section by section (hero, stats, table, footer)
  - Each section gets a frame with auto-layout
  - Tokens from library applied to fills, strokes, text

After each section, pause and show preview URL.
```

### 9.4. Output esperado

- Nova page "Screens/Dashboard v2" com frames por seção.
- Components instanciados da library, sem detached.
- Report de componentes faltantes ou overrides necessários.

---

## 10. Workflow 4, design system rules

### 10.1. Objetivo

Gerar um arquivo `design-system-rules.md` customizado para o projeto, que outras skills consultam ao executar. Atua como constituição do DS.

### 10.2. Inputs

- Descrição do projeto (stack, objetivo, escala).
- Convenções de nomenclatura existentes.
- Restrições não negociáveis (acessibilidade, performance, brand).

### 10.3. Invocação

```
Invoke figma:figma-create-design-system-rules.

Project: Marketing OS
Stack: Next.js 15, React 19, Tailwind 4, shadcn/ui, Radix primitives
Scale: 50+ components, 3 brands (verticals), theming light/dark/high-contrast
Non-negotiables:
  - WCAG 2.2 AA minimum
  - Core Web Vitals green
  - No em-dash in UI copy
  - Portuguese accents preserved in all Pt-BR screens

Naming conventions:
  - Variables: kebab-case, semantic over primitive
  - Components: PascalCase matching React
  - Variants: prop=value (ex. size=md)

Output: references/design/project-design-system-rules.md
```

### 10.4. Uso posterior

As skills `figma-generate-library`, `figma-generate-design` e `figma-implement-design` leem este arquivo automaticamente quando presente e aplicam as rules. Isso reduz ambiguidade e aumenta consistência ao longo de múltiplas sessões.

---

## 11. Workflow 5, Code Connect

### 11.1. Objetivo

Criar mapeamento 1:1 entre um component Figma e seu equivalente em código, de modo que o Figma Dev Mode mostre o snippet correto quando um desenvolvedor inspeciona o component.

### 11.2. Setup inicial

```bash
cd /path/to/project
npx @figma/code-connect connect create
```

Isso gera um arquivo base. Em seguida, use a skill.

### 11.3. Invocação

```
Invoke figma:figma-code-connect.

Component: src/components/ui/Button.tsx
Figma node: https://figma.com/file/ABC?node-id=5-10

Map props:
  - variant (primary|secondary|destructive) -> Figma variant "Type"
  - size (sm|md|lg) -> Figma variant "Size"
  - disabled (bool) -> Figma variant "State" value "disabled"
  - children -> Figma text node "Label"

Output: src/components/ui/Button.figma.tsx
```

### 11.4. Sync contínuo

Após criar o mapping, publique:

```bash
npx @figma/code-connect publish
```

Agora o Figma Dev Mode mostra o snippet correto. Qualquer mudança no prop do React exige atualização no `.figma.tsx` correspondente. Essa manutenção é recorrente, reserve 15 a 30 min por mês.

---

## 12. Common gotchas

### 12.1. Variables ausentes quando o script assume que existem

**Sintoma:** Script falha em `setBoundVariable` porque a variable não existe na coleção alvo.

**Causa:** Ordem errada, ou variable foi renomeada sem atualizar as referências no script.

**Correção:** Execute um probe antes de cada bloco de writes, confirme que todas as variables citadas existem. Se ausente, crie antes de seguir.

### 12.2. Unit mismatch entre plataformas

**Sintoma:** Component no Figma tem 48px de altura, em código renderiza como 48dp (Android) ou 3rem (web) e visualmente difere.

**Causa:** Tokens no Figma estão em px mas código consome em rem ou dp sem conversão.

**Correção:** Defina unidade canônica na spec (ver `01-tokens-w3c-spec.md` §8.1). Em Figma, use px. Em código, use função de conversão `px -> rem` no build.

### 12.3. Variant explosion

**Sintoma:** Component com 5 variants de intent × 4 de size × 5 de state = 100 variants. Publicação lenta e busca no Figma demora.

**Causa:** Matriz sem curadoria, nem toda combinação é realista.

**Correção:** Defina combinações impossíveis como "inexistentes" (ex. intent=destructive + state=success). Limite variants reais a 20 a 30 por component. Use boolean toggles para estados que se combinam.

### 12.4. Timezone em publish automatizado

**Sintoma:** Publish agendado roda às 17h UTC mas o esperado era 17h local (14h UTC em São Paulo).

**Causa:** Scheduler MCP usa UTC por padrão.

**Correção:** Declare timezone explicitamente no job. Ver `references/design/03-ds-governance.md` (§ release cadence).

### 12.5. Token reference não resolvida

**Sintoma:** Fill do component fica cinza em vez da cor esperada.

**Causa:** Alias `{colors.brand.primary}` aponta para variable que foi movida ou renomeada.

**Correção:** No Figma, abra o inspector da variable, veja referência quebrada. Conserte no tokens.json e re-publique library. Script de lint (ver `01-tokens-w3c-spec.md` §12) pega esses erros antes do push.

---

## 13. Handoff designer para dev

A MCP reduz fricção mas não elimina a necessidade de comunicação. Checkpoints explícitos evitam que decisões implícitas virem bugs.

### 13.1. Specs obrigatórias no Figma

- **Component name.** Igual ao nome do React component.
- **Variant axes.** Mesmas dimensões e valores dos props.
- **Spacing.** Via auto-layout, nunca manual.
- **Tokens.** Todas as cores e medidas vinculadas a variables. Zero valores raw.
- **Estados.** Default, hover, focus, active, disabled, error, success. Nem todos os components têm todos os estados, mas a lista de estados suportados deve estar explícita.

### 13.2. Comentários no Figma

Use comentários para informação que não cabe no canvas:

- Regras condicionais (ex. "botão só aparece quando user tem role=admin").
- Comportamento em breakpoint (ex. "no mobile vira bottom sheet").
- Integração com backend (ex. "submit chama POST /api/leads").

### 13.3. Checkpoints antes do handoff

Antes de marcar uma screen como "ready for dev", rode este check:

1. Todos os elementos usam components da library, zero detached.
2. Todas as cores vêm de variables, zero fills raw.
3. Todos os texts usam text styles.
4. Auto-layout aplicado em frames que devem ser responsivos.
5. Constraints corretas em elementos fixos.
6. Comentários cobrem lógica condicional e comportamento.
7. Contraste validado (ver `04-accessibility-wcag22.md` §4).

### 13.4. Dev pede clarificação via MCP

Quando algo não está claro, dev pode usar a skill para perguntar estruturadamente:

```
figma:figma-use probe on node 12-345:
  Are all fills bound to variables? If not, list unbound ones.
  What is the auto-layout direction? padding values?
  Any comments on this node?
```

Resposta vem em JSON, o que acelera troubleshoot versus ida-e-volta humana.

---

## 14. Troubleshooting

### 14.1. Skill retorna erro `context not loaded`

**Hipótese:** esqueceu de invocar `figma:figma-use` antes.

**Fix:** carregue-a como primeira ação, depois chame a skill de write.

### 14.2. Write falha silenciosamente

**Hipótese:** token sem escopo `variables:write` ou `components:write`.

**Fix:** Regenere o token com escopos completos (ver §6.3) e reautentique reaplicando o token em `.mcp.json`.

### 14.3. Resultado visual não bate com código

**Hipóteses possíveis:**

- Unit mismatch (§12.2).
- Version skew entre library publicada e arquivo consumidor.
- Override local no arquivo que não vem da library.

**Fix:** confira version da library em File > Library. Atualize se necessário. Detect local overrides via Dev Mode inspector.

### 14.4. MCP server não responde

**Hipóteses:**

- Token expirado.
- Figma Dev Mode desativado no arquivo.
- Rate limit (muitos calls em janela curta).

**Fix:** rode o probe do §6.4. Se timeout, valide token. Se rate limit, espere 60s e retry. Se persistir, verifique status via `claude mcp list`.

### 14.5. Skill produz resultado ruim (genérico ou errado)

**Fallbacks em ordem:**

1. **Adicionar contexto.** Refaça o prompt com mais especificidade (ver §4).
2. **Dividir a task.** Component muito grande, quebre em subcomponents.
3. **Fallback manual.** Faça no UI do Figma os 2 a 3 components críticos, use MCP para o resto.
4. **Pedir verbose.** Peça para a skill explicar suas decisões antes de executar, revise, aprove.
5. **Escalar.** Se a skill falha repetidamente, é bug. Documente em `docs/qa/mcp-issues/` para análise.

### 14.6. Publish falha com erro de permissão

**Hipótese:** user não é admin da team, ou library está locked.

**Fix:** publish só funciona para editores da team. Para libraries críticas, defina owner e processos de release (ver `03-ds-governance.md`).

---

## Referências cruzadas

- `references/design/01-tokens-w3c-spec.md`, base de tokens que a `figma-generate-library` consome.
- `references/design/02-atomic-design-playbook.md`, estrutura atom-molecule-organism que guia ordem de creation.
- `references/design/03-ds-governance.md`, processos de release e RFC que alimentam MCP.
- `references/design/04-accessibility-wcag22.md`, critérios de contraste e navegação validados no output.
- `references/design/08-shadcn-radix-recipes.md`, patterns de código-alvo para `figma-implement-design`.
- `references/design/09-design-handoff-to-code.md`, processo humano complementar ao handoff automatizado.
