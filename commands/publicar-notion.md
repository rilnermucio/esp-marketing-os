---
description: Publish editorial calendars, content plans, or generated content directly to your Notion workspace via Notion MCP. Routes to creation commands first when content does not yet exist.
argument-hint: "<what to publish, e.g., 'editorial calendar for March' or 'content plan for product launch'>"
---

# /publicar-notion: Publicar no Notion

Utility de publicação. Quando o conteúdo já existe, publica direto via Notion MCP. Quando precisa gerar antes, dispatcha o command de criação adequado e só publica depois.

## Required inputs (ask if missing)

1. **Tipo de conteúdo** (obrigatório): calendário editorial, plano de conteúdo, brief de campanha, post único, documentação de projeto
2. **Status do conteúdo** (obrigatório): já gerado (colar/referenciar) ou precisa ser criado
3. **Destino no Notion** (opcional): página, database, ou área específica do workspace
4. **Formato** (opcional): página, linha de database, database com template

## Decision Tree

```
Conteúdo já existe?
  ├── SIM → Publica direto via Notion MCP (Fase 2)
  │
  └── NÃO → Dispatch para command de criação primeiro (Fase 1), depois publica (Fase 2)
            ├── "calendário editorial" → /criar-calendario
            ├── "plano de conteúdo / campanha" → /campanha
            ├── "posts em lote pra encher database" → /batch
            └── "post único" → /criar-post
```

## Fase 1 (opcional): Geração de conteúdo

Se o input pede algo que ainda não foi gerado, **antes** de tocar no Notion MCP, roteie:

- "publica calendário pra março" sem calendário pronto → executar `/criar-calendario` primeiro com o briefing extraído
- "publica plano de campanha de lançamento" sem plano → executar `/campanha lancamento` (ou preset adequado)
- "publica 10 posts no database" sem posts → executar `/batch 10 posts <tema>`
- "publica este post" com copy colada → pular Fase 1

Após geração, **consolide o output** e siga pra Fase 2.

## Fase 2: Publicação via Notion MCP

Sequência de tools:

```
1. notion-search           → procura database/página de destino existente
2. notion-create-database  → cria database se não existir (apenas para calendário/plano novo)
3. notion-create-pages     → adiciona entries (post a post, ou página única)
```

### Schemas por tipo

**Calendário editorial → database** com colunas:
- Date (date), Platform (select), Content Type (select), Status (select: Draft/Review/Approved/Published), Topic (text), Copy (rich text), Hashtags (text), Notes (text)

**Plano de conteúdo → página estruturada** com: campaign overview, content pillars, channel strategy, timeline, KPIs

**Brief de campanha → página** com: objectives, target audience, messaging framework, channel breakdown, budget, timeline

**Post único → linha de database existente** com: copy, hashtags, visual direction, status, platform

## Output

```markdown
## Publicação Notion

Tipo: [calendário | plano | brief | post]
Destino: [URL ou nome da database/página]
Status: [Publicado | Erro]

### Resumo do que foi publicado
[N entries adicionadas / página criada / database criada]

### Links
- [URL direta da página ou database]

### Próximos passos
1. Revisar no Notion e ajustar status
2. Atribuir responsáveis
3. Atualizar conforme progresso
```

## Quality Gates (antes de publicar)

Aplicar gates globais do `skills/marketing-os/SKILL.md` no conteúdo **antes** de mandar pro Notion:
- Sem `—`, sem "brutal", sem CAPS gratuito
- Sem aspas em roteiros/falas
- Máximo 1-2 emojis
- Acentuação PT-BR correta
- Fatos verificados

Conteúdo que não passa nos gates **não vai pro Notion**: refaça primeiro.

## Follow-up ao usuário

"Quer que eu:
1. Adicione mais entries na mesma database?
2. Crie uma view alternativa (calendar, board, timeline)?
3. Gere mais conteúdo pra popular o calendário?
4. Configure templates de páginas pra o database?"

## Por que decision tree

Sem checagem de "conteúdo existe?", o usuário acaba pedindo `/publicar-notion` esperando que o Notion crie o conteúdo. Isso falha. Roteando pra `/criar-calendario` ou `/batch` primeiro garante que entra conteúdo de qualidade na database, não placeholder.
