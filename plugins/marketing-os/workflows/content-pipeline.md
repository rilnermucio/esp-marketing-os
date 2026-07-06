# Content Pipeline — Workflow de Produção Integrado

## Visão Geral

O Content Pipeline é um workflow de produção de conteúdo que orquestra múltiplos subagentes em sequência para garantir qualidade e consistência em cada peça produzida.

| Fase | Agente | Input | Output | Tempo |
|------|--------|-------|--------|-------|
| 1. Pesquisa | Research Agent | Tema + nicho | Research Brief | 15-20 min |
| 2. Redação | Copy Agent + SEO Agent | Research Brief | Content Draft | 20-30 min |
| 3. Design | Design Agent + AI Tools Agent | Content Draft | Design Brief | 10-15 min |
| 4. Revisão | Analytics Agent | Tudo anterior | Quality Report | 10 min |

**Tempo total estimado:** 55-75 minutos por peça de conteúdo

**Quando usar:** Para conteúdo de alta qualidade que precisa de pesquisa, redação otimizada, direção visual e validação de qualidade antes de publicar.

---

## Fase 1: Pesquisa (Research Agent)

### Objetivo
Levantar dados, tendências, concorrência e insights que fundamentem o conteúdo.

### Checklist

```
TAREFA: Research Brief
AGENTE: Research Agent

- [ ] Definir tema principal e ângulo
- [ ] Pesquisar palavras-chave relevantes (volume, dificuldade)
- [ ] Analisar 3-5 conteúdos concorrentes sobre o tema
- [ ] Identificar gaps de conteúdo (o que ninguém está falando)
- [ ] Levantar dados e estatísticas recentes
- [ ] Mapear perguntas da audiência (Google, Reddit, Quora)
- [ ] Identificar trends relacionados ao tema

ENTREGÁVEL: research-brief.md
```

### Template do Research Brief

```markdown
## Research Brief

**Tema:** [Tema principal]
**Ângulo:** [Perspectiva única]
**Data:** [Data da pesquisa]

### Palavras-chave
| Keyword | Volume | Dificuldade | Intenção |
|---------|--------|-------------|----------|
| [kw1] | [vol] | [diff] | [intent] |

### Dados e Estatísticas
- [Dado 1 — fonte]
- [Dado 2 — fonte]
- [Dado 3 — fonte]

### Análise de Concorrência
| Concorrente | Ângulo | Pontos Fortes | Gaps |
|------------|--------|---------------|------|
| [conc1] | [ângulo] | [fortes] | [gaps] |

### Perguntas da Audiência
1. [Pergunta mais buscada]
2. [Pergunta relevante]
3. [Pergunta de oportunidade]

### Trends Relacionados
- [Trend 1 — contexto]
- [Trend 2 — contexto]

### Recomendações para o Conteúdo
- **Hook sugerido:** [Hook baseado na pesquisa]
- **Ângulo diferenciador:** [O que só você pode dizer]
- **Dados para incluir:** [Estatísticas de impacto]
- **CTA recomendado:** [CTA baseado na intenção]
```

---

## Fase 2: Redação (Copy Agent + SEO Agent)

### Objetivo
Criar o conteúdo com base no Research Brief, otimizado para engajamento e SEO.

### Checklist

```
TAREFA: Content Draft
AGENTES: Copy Agent + SEO Agent

- [ ] Ler Research Brief completo
- [ ] Definir framework de copy (AIDA, PAS, BAB)
- [ ] Criar 3 opções de hook
- [ ] Escrever body copy seguindo o framework
- [ ] Inserir dados/estatísticas do Research Brief
- [ ] Otimizar para SEO (se artigo/blog)
  - [ ] Keyword no título e H2s
  - [ ] Meta description
  - [ ] Internal/external links sugeridos
- [ ] Criar CTA forte e contextual
- [ ] Gerar variações A/B do hook e CTA
- [ ] Adaptar tom ao nicho e plataforma

ENTREGÁVEL: content-draft.md
```

### Regras de Redação

| Princípio | Aplicação |
|-----------|-----------|
| Benefícios > Features | Sempre liderar com o resultado, não o recurso |
| Específico > Genérico | Números, dados, exemplos concretos |
| Você > Nós | Falar diretamente com o leitor |
| Ativo > Passivo | Verbos de ação, frases diretas |
| Curto > Longo | Parágrafos de 1-3 linhas, frases de até 20 palavras |

### Verificações de SEO

- [ ] Keyword density entre 1-2%
- [ ] Keyword no primeiro parágrafo
- [ ] H2s com variações da keyword
- [ ] Meta description com keyword + CTA
- [ ] Alt text para imagens sugerido
- [ ] URL slug otimizado
- [ ] Contagem de palavras adequada ao formato

---

## Fase 3: Design (Design Agent + AI Tools Agent)

### Objetivo
Criar a direção visual e prompts de IA para complementar o conteúdo.

### Checklist

```
TAREFA: Design Brief
AGENTES: Design Agent + AI Tools Agent

- [ ] Definir paleta de cores (baseada no nicho/marca)
- [ ] Sugerir tipografia (heading + body)
- [ ] Criar layout/composição recomendada
- [ ] Gerar prompts de imagem IA (Midjourney, DALL-E, Flux)
- [ ] Definir estilo visual (fotográfico, ilustrado, minimalista)
- [ ] Especificar dimensões por plataforma
- [ ] Criar mockup conceitual (descrição textual)

ENTREGÁVEL: design-brief.md
```

### Especificações por Plataforma

| Plataforma | Formato | Dimensões | Aspectos |
|------------|---------|-----------|----------|
| Instagram Feed | Quadrado | 1080x1080 | Texto grande, contraste alto |
| Instagram Stories | Vertical | 1080x1920 | Zona segura central |
| Instagram Reels | Vertical | 1080x1920 | Thumbnail atrativo |
| LinkedIn | Horizontal | 1200x627 | Profissional, clean |
| Twitter/X | Horizontal | 1600x900 | Impactante, simples |
| YouTube Thumbnail | Horizontal | 1280x720 | Face + texto grande |
| Blog/SEO | Horizontal | 1200x630 | OG image, shareável |
| TikTok | Vertical | 1080x1920 | Nativo, autêntico |

---

## Fase 4: Revisão (Analytics Agent)

### Objetivo
Validar a qualidade do conteúdo antes da publicação.

### Checklist

```
TAREFA: Quality Report
AGENTE: Analytics Agent

- [ ] Verificar acentuação (português)
- [ ] Avaliar força do hook (score 1-10)
- [ ] Verificar presença e clareza do CTA
- [ ] Conferir adequação ao formato da plataforma
- [ ] Validar limites de caracteres
- [ ] Checar hashtags (quantidade e relevância)
- [ ] Medir readability score
- [ ] Verificar consistência com brand voice
- [ ] Confirmar dados/estatísticas citados
- [ ] Avaliar potencial de engajamento (score 1-10)

ENTREGÁVEL: quality-report.md
```

### Template do Quality Report

```markdown
## Quality Report

**Conteúdo:** [Título/descrição]
**Data:** [Data da revisão]

### Scores

| Critério | Score | Status |
|----------|-------|--------|
| Força do hook | [X]/10 | [Pass/Fail] |
| Clareza do CTA | [X]/10 | [Pass/Fail] |
| Adequação à plataforma | [X]/10 | [Pass/Fail] |
| SEO optimization | [X]/10 | [Pass/Fail] |
| Readability | [X]/10 | [Pass/Fail] |
| Brand voice consistency | [X]/10 | [Pass/Fail] |
| Fact-check | [X]/10 | [Pass/Fail] |
| Potencial de engajamento | [X]/10 | [Pass/Fail] |

**Score geral:** [X]/100
**Veredicto:** [Aprovado / Revisão necessária / Reprovado]

### Problemas Encontrados
1. [Problema — sugestão de correção]
2. [Problema — sugestão de correção]

### Sugestões de Melhoria
1. [Sugestão para aumentar engajamento]
2. [Sugestão para melhorar conversão]

### Aprovação
- [ ] Conteúdo aprovado para publicação
- [ ] Revisões necessárias (ver problemas acima)
```

---

## Fluxo Completo

```
                    ┌─────────────┐
                    │   BRIEFING   │
                    │  (Usuário)   │
                    └──────┬──────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   FASE 1: PESQUISA     │
              │   Research Agent       │
              │   → research-brief.md  │
              └────────────┬───────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   FASE 2: REDAÇÃO      │
              │   Copy + SEO Agent     │
              │   → content-draft.md   │
              └────────────┬───────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   FASE 3: DESIGN       │
              │   Design + AI Tools    │
              │   → design-brief.md    │
              └────────────┬───────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   FASE 4: REVISÃO      │
              │   Analytics Agent      │
              │   → quality-report.md  │
              └────────────┬───────────┘
                           │
                    ┌──────┴──────┐
                    │  APROVADO?  │
                    └──────┬──────┘
                     Sim ↙   ↘ Não
                   ┌────┐  ┌──────────┐
                   │PUBL│  │ REVISÃO  │
                   │ICAR│  │ (volta   │
                   └────┘  │  Fase 2) │
                           └──────────┘
```

---

## Métricas de Produtividade

| Métrica | Meta | Como Medir |
|---------|------|------------|
| Tempo por peça | < 75 min | Cronômetro por fase |
| Taxa de aprovação | > 80% | Quality Reports aprovados / total |
| Score médio de qualidade | > 75/100 | Média dos Quality Reports |
| Peças por dia | 3-5 | Contagem diária |
| Retrabalho | < 20% | Peças que voltam para revisão |

---

## Dicas para Máxima Eficiência

1. **Pesquisa em lote:** Faça Research Briefs para 5-10 temas de uma vez
2. **Templates prontos:** Use templates por formato para acelerar a redação
3. **Clone de voz:** Ative um clone para manter consistência de tom
4. **Batch de design:** Agrupe direção visual para peças similares
5. **Revisão simplificada:** Para conteúdo recorrente, use checklist reduzido

---

## Ferramentas Recomendadas

| Categoria | Ferramenta | Uso |
|-----------|-----------|-----|
| Pesquisa | WebSearch / Exa | Dados em tempo real |
| SEO | `scripts/seo_analyzer.py` | Análise on-page |
| Headlines | `scripts/headline_scorer.py` | Score de headlines |
| Readability | `scripts/readability_checker.py` | Legibilidade |
| Hashtags | `scripts/hashtag_generator.py` | Geração de hashtags |
| Hooks | `scripts/hook_generator.py` | Hooks virais |
| Calendário | `scripts/content_calendar.py` | Planejamento |

---

## Recursos Relacionados

- `workflows/batch-production-workflow.md` — Produção em lote (volume)
- `assets/checklists/pre-publicacao.md` — Checklist pré-publicação
- `references/strategy.md` — Estratégia geral de marketing
- `references/social-media.md` — Guia por plataforma
- `references/blog-seo.md` — Guia de SEO para blog
