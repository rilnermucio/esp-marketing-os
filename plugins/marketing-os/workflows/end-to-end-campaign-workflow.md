# End-to-End Campaign Workflow — Da Estratégia à Publicação

## Visão Geral

O End-to-End Campaign Workflow orquestra **todos os subagentes** do Marketing OS em uma cadeia completa: da definição de objetivo até a análise pós-campanha. É o workflow mais completo do sistema, ideal para campanhas de lançamento, promoções e conteúdo de alto impacto.

```
FLUXO COMPLETO:
Objetivo → Pesquisa → Estratégia → Copy → Design → Distribuição → Análise
```

| Fase | Agente(s) | Input | Output | Duração |
|------|-----------|-------|--------|---------|
| 1. Diagnóstico | Research Agent | Objetivo + contexto | Market brief | 20-30 min |
| 2. Estratégia | Copy Agent + Brand Agent | Market brief | Estratégia de campanha | 15-20 min |
| 3. Copy | Copy Agent + Storytelling Agent | Estratégia | Copy completo | 25-35 min |
| 4. Assets Visuais | Design Agent + AI Tools Agent | Copy | Design brief + prompts | 15-20 min |
| 5. Distribuição | Social Agent + Email Agent + Ads Agent | Tudo | Posts, emails, anúncios | 20-30 min |
| 6. Análise | Analytics Agent | Resultados | Performance report | 10-15 min |

**Duração total estimada:** 105-150 minutos para campanha completa

---

## Fase 1: Diagnóstico de Mercado (Research Agent)

### Ativar Research Agent

```
Ativação: Use o subagente Research Agent
Comando: "Preciso de um market brief para campanha de [objetivo]"
```

### Checklist de Diagnóstico

```
TAREFA: Market Brief
AGENTE: Research Agent

MERCADO:
[ ] Tamanho e segmentos do mercado-alvo
[ ] 3-5 concorrentes diretos com análise de posicionamento
[ ] Gaps e oportunidades não exploradas
[ ] Trends relevantes (Google Trends, redes sociais, notícias)

AUDIÊNCIA:
[ ] Avatar principal (demografia, psicografia, comportamento digital)
[ ] Dores e frustrações mais frequentes
[ ] Desejos e aspirações
[ ] Linguagem e vocabulário da audiência
[ ] Objeções mais comuns

PRODUTO/SERVIÇO:
[ ] Proposta de valor central
[ ] Diferenciadores competitivos
[ ] Provas e resultados existentes
[ ] Depoimentos e casos de sucesso disponíveis

ENTREGÁVEL: market-brief.md
```

### Template: Market Brief

```markdown
# Market Brief

**Campanha:** [Nome da campanha]
**Objetivo:** [O que a campanha deve alcançar]
**Data:** [Data de criação]

## Mercado
- **Tamanho estimado:** [Número de potenciais clientes]
- **Principais segmentos:** [Segmentos priorizados]
- **Tendência:** [Crescendo/estagnado/decrescendo]

## Análise Competitiva
| Concorrente | Posicionamento | Ponto Forte | Vulnerabilidade |
|------------|---------------|-------------|-----------------|
| [comp1]    |               |             |                 |

## Avatar Principal
- **Quem é:** [Descrição em 2-3 linhas]
- **Problema central:** [A dor principal]
- **Desejo central:** [O que realmente quer]
- **Objeção principal:** [Por que ainda não comprou]
- **Onde encontrá-lo:** [Plataformas, comunidades, canais]

## Oportunidade Identificada
[O que os concorrentes NÃO estão fazendo que você pode fazer]

## Recomendações para a Campanha
- **Tom sugerido:** [Emocional/racional/provocador/educativo]
- **Ângulo diferenciador:** [O que só você pode dizer]
- **Clone recomendado:** [Qual expert do sistema de clones usar]
- **Canal prioritário:** [Onde a campanha terá mais impacto]
```

---

## Fase 2: Estratégia de Campanha (Copy Agent + Brand Agent)

### Ativar Copy Agent

```
Ativação: Use o subagente Copy Agent
Input: Market Brief da Fase 1
Comando: "Com base neste market brief, crie a estratégia de campanha"
```

### Checklist de Estratégia

```
TAREFA: Estratégia de Campanha
AGENTES: Copy Agent + Brand Agent

POSICIONAMENTO:
[ ] Definir a mensagem central da campanha (1 frase)
[ ] Escolher o ângulo principal (medo/desejo/curiosidade/prova)
[ ] Selecionar o clone de voz para a campanha
[ ] Mapear o arco emocional da campanha

ESTRUTURA:
[ ] Definir os canais e formatos
[ ] Estabelecer sequência e timing (quando cada peça vai ao ar)
[ ] Definir a oferta central e as condições
[ ] Planejar o follow-up para não-convertidos

MÉTRICAS:
[ ] Definir KPI principal da campanha
[ ] Estabelecer metas numéricas
[ ] Definir ferramentas de rastreamento

ENTREGÁVEL: campaign-strategy.md
```

### Template: Estratégia de Campanha

```markdown
# Estratégia de Campanha

**Campanha:** [Nome]
**Período:** [Data início] até [Data fim]
**Objetivo:** [Meta principal com número]

## Mensagem Central
> "[A mensagem em uma frase que captura tudo]"

## Ângulo Principal
- **Tipo:** [Medo / Desejo / Curiosidade / Prova / Problema-Solução]
- **Gancho central:** [O gancho que abre todas as peças]
- **Clone de voz:** [Expert do sistema de clones]

## Canais e Sequência
| Dia | Canal | Formato | Objetivo |
|-----|-------|---------|----------|
| D-7 | Email | Aquecimento | Gerar antecipação |
| D-3 | Instagram | Post/Reels | Awareness |
| D-1 | Email | Lembrete | Urgência |
| D0  | Todos | Lançamento | Conversão |
| D+2 | Email | Follow-up | Recuperar indecisos |
| D+5 | Ads | Retargeting | Fechar não-convertidos |

## Oferta
- **Produto/serviço:** [Descrição]
- **Preço:** [Valor]
- **Bônus:** [Lista de bônus]
- **Garantia:** [Termos da garantia]
- **Urgência/Escassez:** [Prazo ou quantidade limitada]

## KPIs
| Métrica | Meta | Canal |
|---------|------|-------|
| [métrica1] | [meta] | [canal] |

## Budget
- **Paid traffic:** R$[valor]
- **Produção:** R$[valor]
- **Total:** R$[valor]
```

---

## Fase 3: Produção de Copy (Copy Agent + Storytelling Agent)

### Ativar Copy Agent

```
Ativação: Use o subagente Copy Agent
Input: Estratégia de Campanha da Fase 2
Comando: "Com base nesta estratégia, produza todas as peças de copy"
```

### Checklist de Copy por Canal

```
TAREFA: Copy Completo da Campanha
AGENTES: Copy Agent + Storytelling Agent

EMAIL (se a campanha usar email):
[ ] Email de aquecimento (1 semana antes)
[ ] Email de anúncio/lançamento
[ ] Email de follow-up (2 dias depois)
[ ] Email de urgência/fechamento (último dia)
[ ] Sequência de reativação (pós-campanha)

REDES SOCIAIS:
[ ] Caption para Instagram Feed (com variações A/B)
[ ] Caption para Stories (interativo)
[ ] Script para Reels/TikTok
[ ] Post para LinkedIn (se relevante)

ANÚNCIOS (se paid traffic):
[ ] Copy do anúncio (headline + texto + CTA)
[ ] 3 variantes de criativo para teste A/B
[ ] Retargeting específico para não-convertidos

LANDING PAGE:
[ ] Headline + subheadline
[ ] Copy do hero
[ ] Benefícios (bullet points)
[ ] Prova social
[ ] Oferta detalhada
[ ] FAQs
[ ] CTA(s)

ENTREGÁVEL: copy-completo.md
```

---

## Fase 4: Produção de Assets Visuais (Design Agent + AI Tools Agent)

### Ativar Design Agent

```
Ativação: Use o subagente Design Agent
Input: Copy completo da Fase 3
Comando: "Crie o design brief e prompts de IA para todos os assets"
```

### Checklist de Assets Visuais

```
TAREFA: Assets Visuais Completos
AGENTES: Design Agent + AI Tools Agent

IDENTIDADE VISUAL DA CAMPANHA:
[ ] Paleta de cores (baseada na identidade da marca)
[ ] Tipografia (heading, body, CTA)
[ ] Estilo visual (fotográfico/ilustrado/minimalista)
[ ] Tom emocional das imagens

ASSETS POR CANAL:
[ ] Instagram Feed: 1080x1080 (1-3 imagens/carrossel)
[ ] Instagram Stories: 1080x1920 (3-5 stories)
[ ] Instagram Reels: thumbnail + overlay de texto
[ ] LinkedIn: 1200x627 (se relevante)
[ ] Email: banner do email + imagens do corpo
[ ] Anúncios: variantes de criativo por formato
[ ] Landing page: hero image + imagens de suporte

PROMPTS DE IA (Midjourney, DALL-E, Flux):
[ ] Prompt para cada asset visual necessário
[ ] Especificação de estilo, iluminação, composição
[ ] Variações de prompt para testes

ENTREGÁVEL: design-brief.md + prompts.md
```

---

## Fase 5: Distribuição Multi-Canal (Social Agent + Email Agent + Ads Agent)

### Ativar Social Agent

```
Ativação: Use o subagente Social Agent (e Email Agent / Ads Agent conforme necessário)
Input: Copy + Design Assets das fases anteriores
Comando: "Prepare e schedule todos os posts conforme a estratégia de campanha"
```

### Checklist de Distribuição

```
TAREFA: Distribuição Multi-Canal
AGENTES: Social Agent + Email Agent + Ads Agent

SOCIAL MEDIA:
[ ] Posts agendados conforme calendário da estratégia
[ ] Hashtags otimizadas por plataforma e objetivo
[ ] Horários de pico considerados
[ ] Stories + feed sincronizados
[ ] Primeira resposta de comentários preparada (engage inicial)

EMAIL MARKETING:
[ ] Segmentação da lista definida
[ ] Sequência de automação configurada
[ ] Tracking de abertura e clique ativo
[ ] Preview nos principais clientes de email testado
[ ] Sender name e reply-to configurados

ANÚNCIOS PAGOS (se aplicável):
[ ] Campanha configurada na plataforma
[ ] Audiências definidas (fria + lookalike + retargeting)
[ ] Budget diário configurado
[ ] Pixel/conversão rastreando
[ ] Criativo aprovado pela plataforma

LANDING PAGE:
[ ] URL correta em todos os links
[ ] Formulário/checkout funcionando
[ ] Tracking de conversão ativo
[ ] Página testada em mobile

ENTREGÁVEL: distribution-checklist.md (com itens marcados)
```

---

## Fase 6: Análise e Aprendizado (Analytics Agent)

### Ativar Analytics Agent

```
Ativação: Use o subagente Analytics Agent
Input: Dados de performance pós-campanha
Comando: "Analise a performance da campanha e gere relatório com aprendizados"
```

### Checklist de Análise

```
TAREFA: Performance Report
AGENTE: Analytics Agent

MÉTRICAS POR CANAL:
[ ] Email: abertura, clique, conversão, receita
[ ] Redes sociais: alcance, engajamento, cliques, conversões
[ ] Ads: impressões, CTR, CPC, ROAS, CAC
[ ] Landing page: visitas, taxa de conversão, receita

ANÁLISE COMPARATIVA:
[ ] KPIs realizados vs. metas
[ ] Performance por variante A/B
[ ] Canal com maior ROI
[ ] Segmento com melhor resposta

APRENDIZADOS:
[ ] O que funcionou (top 3 insights positivos)
[ ] O que não funcionou (top 3 problemas)
[ ] Hipóteses para próxima campanha

ENTREGÁVEL: performance-report.md
```

### Template: Performance Report

```markdown
# Performance Report

**Campanha:** [Nome]
**Período:** [Data início] a [Data fim]
**Analista:** Analytics Agent

## Resumo Executivo

| KPI | Meta | Realizado | Delta |
|-----|------|-----------|-------|
| [kpi1] | [meta] | [real] | [%] |
| Receita total | R$[meta] | R$[real] | [%] |
| ROAS | [meta] | [real] | [%] |
| CAC | R$[meta] | R$[real] | [%] |

## Performance por Canal

### Email Marketing
| Métrica | Resultado | Benchmark |
|---------|-----------|-----------|
| Taxa de abertura | [%] | 25-35% |
| Taxa de clique | [%] | 3-8% |
| Taxa de conversão | [%] | 1-5% |
| Receita atribuída | R$[valor] | — |

### Redes Sociais
| Canal | Alcance | Engajamento | Conversões |
|-------|---------|-------------|------------|
| Instagram | | | |
| LinkedIn | | | |

### Anúncios Pagos
| Plataforma | Gasto | Receita | ROAS |
|------------|-------|---------|------|
| Meta Ads | R$[val] | R$[val] | [x] |
| Google Ads | R$[val] | R$[val] | [x] |

## Top Aprendizados

### O Que Funcionou
1. [Insight positivo + dado de suporte]
2. [Insight positivo + dado de suporte]
3. [Insight positivo + dado de suporte]

### O Que Não Funcionou
1. [Problema + hipótese de causa]
2. [Problema + hipótese de causa]

### Recomendações para Próxima Campanha
1. [Recomendação específica]
2. [Recomendação específica]
3. [Recomendação específica]
```

---

## Fluxo Visual Completo

```
┌──────────────────────────────────────────────────────────┐
│              END-TO-END CAMPAIGN WORKFLOW                 │
└──────────────────────────────────────────────────────────┘

         [OBJETIVO + BRIEFING DO USUÁRIO]
                        │
                        ▼
         ┌─────────────────────────────┐
         │  FASE 1: DIAGNÓSTICO        │
         │  Research Agent             │
         │  → market-brief.md          │
         └──────────────┬──────────────┘
                        │
                        ▼
         ┌─────────────────────────────┐
         │  FASE 2: ESTRATÉGIA         │
         │  Copy Agent + Brand Agent   │
         │  → campaign-strategy.md     │
         └──────────────┬──────────────┘
                        │
                        ▼
         ┌─────────────────────────────┐
         │  FASE 3: COPY               │
         │  Copy + Storytelling Agent  │
         │  → copy-completo.md         │
         └──────────────┬──────────────┘
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
  ┌──────────────────┐  ┌──────────────────────┐
  │  FASE 4: DESIGN  │  │  FASE 5: DISTRIBUIÇÃO │
  │  Design Agent +  │  │  Social + Email +      │
  │  AI Tools Agent  │  │  Ads Agent             │
  │  → design-brief  │  │  → distribuição ativa  │
  └────────┬─────────┘  └──────────┬────────────┘
           └──────────┬────────────┘
                      │ (paralelo)
                      ▼
         ┌─────────────────────────────┐
         │  FASE 6: ANÁLISE            │
         │  Analytics Agent            │
         │  → performance-report.md    │
         └──────────────┬──────────────┘
                        │
                        ▼
              [APRENDIZADOS → PRÓXIMA CAMPANHA]
```

---

## Modo Rápido (Quick Campaign)

Para campanhas simples ou urgentes, use o modo rápido (Fases 3 e 5 apenas):

```
QUICK CAMPAIGN (30-45 minutos):
1. Copy Agent → Criar copy para o canal principal
2. Social/Email/Ads Agent → Distribuir imediatamente

Use quando:
- Conteúdo recorrente (posts semanais)
- Urgência real (acontecimento do dia)
- Tema já pesquisado anteriormente
- Formato padronizado
```

---

## Integração com Scripts do Marketing OS

| Fase | Script Disponível | Uso |
|------|------------------|-----|
| Fase 1 | `scripts/seo_analyzer.py` | Análise de keywords |
| Fase 1 | `scripts/competitor_analyzer.py` | Análise de concorrentes |
| Fase 1 | `scripts/trend_tracker.py` | Trends em tempo real |
| Fase 3 | `scripts/hook_generator.py` | Geração de hooks |
| Fase 3 | `scripts/headline_scorer.py` | Score de headlines |
| Fase 3 | `scripts/caption_generator.py` | Geração de captions |
| Fase 3 | `scripts/hashtag_generator.py` | Hashtags por plataforma |
| Fase 3 | `scripts/content_repurposer.py` | Reutilização de conteúdo |
| Fase 3 | `scripts/ab_generator.py` | Variantes A/B |
| Fase 6 | `scripts/content_audit.py` | Auditoria pós-publicação |
| Fase 6 | `scripts/readability_checker.py` | Legibilidade do copy |

---

## Glossário de Arquivos do Workflow

| Arquivo | Fase | Descrição |
|---------|------|-----------|
| `market-brief.md` | 1 | Análise de mercado, audiência e oportunidade |
| `campaign-strategy.md` | 2 | Posicionamento, canais, oferta e KPIs |
| `copy-completo.md` | 3 | Todas as peças de copy da campanha |
| `design-brief.md` | 4 | Especificações visuais e prompts de IA |
| `prompts.md` | 4 | Prompts específicos para geração de imagens |
| `distribution-checklist.md` | 5 | Checklist de publicação por canal |
| `performance-report.md` | 6 | Análise de resultados e aprendizados |

---

## Recursos Relacionados

- [content-pipeline.md](content-pipeline.md) — Workflow simplificado para conteúdo orgânico
- [assets/checklists/quality-gate.md](../assets/checklists/quality-gate.md) — Quality gate pré-publicação
- [squads/marketing-os/data/clones/clone-manifest.yaml](../squads/marketing-os/data/clones/clone-manifest.yaml) — Sistema de clones para tom de voz
- `scripts/` — Scripts Python para análise e geração de conteúdo
