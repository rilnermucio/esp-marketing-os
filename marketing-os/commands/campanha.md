# /campanha — Presets de Campanha por Objetivo

## Descrição

O comando `/campanha` ativa o preset adequado ao objetivo da campanha, carregando automaticamente a estratégia, os subagentes, o clone de voz e os templates ideais para cada tipo de ação.

## Uso

```
/campanha [tipo]

Tipos disponíveis:
  lancamento     → Campanha de lançamento de produto/serviço
  prospeccao     → Geração de leads e novos clientes
  retencao       → Retenção e reativação de clientes existentes
  autoridade     → Construção de autoridade e marca pessoal
  growth         → Growth hacking e experimentos de crescimento
  black-friday   → Campanha de datas especiais e promoções
```

---

## Preset 1: /campanha lancamento

**Objetivo:** Lançar um novo produto, serviço, curso ou oferta com máximo impacto.

### Configuração Automática

```yaml
tipo: lancamento
clone_primario: brunson
clone_alternativo: suby
agentes_ativos:
  - Research Agent (análise de mercado e concorrência)
  - Copy Agent (copy de lançamento — PLF ou Webinar)
  - Storytelling Agent (narrativa da jornada do produto)
  - Social Agent (sequência de posts de aquecimento)
  - Email Agent (sequência de lançamento — 7 emails)
  - Ads Agent (anúncios de remarketing e conversão)
  - Design Agent (assets visuais da campanha)
  - Analytics Agent (setup de tracking e KPIs)
sequencia_default:
  semana_-2: "Conteúdo de aquecimento (problema)"
  semana_-1: "Conteúdo de value (solução parcial)"
  dia_-3: "Abertura do carrinho / anúncio do produto"
  dia_-1: "Urgência e prova social"
  dia_0: "Lançamento oficial"
  dia_+2: "Depoimentos e follow-up"
  dia_+5: "Fechamento / última chance"
frameworks:
  - PLF (Product Launch Formula) de Jeff Walker
  - Seed-and-Launch de Russell Brunson
  - Value Stack de Alex Hormozi
```

### Checklist de Lançamento

```
PRÉ-LANÇAMENTO (2 semanas antes):
[ ] Pesquisa de mercado e validação de oferta (Research Agent)
[ ] Definição do avatar e posicionamento (Copy Agent)
[ ] Criação do produto/oferta core completa
[ ] Landing page de captura de leads/lista de espera
[ ] Sequência de email de aquecimento (7 dias)
[ ] Conteúdo de aquecimento para redes sociais (5-7 posts)
[ ] Assets visuais e identidade da campanha (Design Agent)
[ ] Setup de tracking (pixel, UTMs, metas de conversão)

LANÇAMENTO (dia D):
[ ] Email de abertura do carrinho
[ ] Posts em todas as plataformas ativas
[ ] Anúncios pagos ativados (se no plano)
[ ] Stories com contagem regressiva
[ ] Monitoramento de métricas em tempo real

PÓS-LANÇAMENTO:
[ ] Sequência de follow-up (3-5 emails)
[ ] Retargeting para não-convertidos
[ ] Email de fechamento do carrinho
[ ] Análise de performance (Analytics Agent)
[ ] Documentação de aprendizados
```

### KPIs de Lançamento

| KPI | Benchmark | Como Medir |
|-----|-----------|------------|
| Taxa de conversão da lista | 3-7% | Compras / leads na lista |
| ROAS de anúncios | > 3x | Receita / Gasto em ads |
| Taxa de abertura de emails | > 35% | Emails abertos / enviados |
| Taxa de clique nos emails | > 5% | Cliques / abertos |

---

## Preset 2: /campanha prospeccao

**Objetivo:** Gerar leads qualificados e novos clientes de forma consistente e previsível.

### Configuração Automática

```yaml
tipo: prospeccao
clone_primario: suby
clone_alternativo: kennedy
agentes_ativos:
  - Research Agent (perfil de avatar e canais)
  - Copy Agent (copy de lead magnet e landing page)
  - Ads Agent (campanhas de tráfego pago)
  - Email Agent (sequência de nutrição — 10 emails)
  - Social Agent (conteúdo de topo de funil)
  - Analytics Agent (rastreamento de CAC e funil)
sequencia_default:
  semana_1: "Lançar lead magnet + landing page"
  semana_2: "Ativar tráfego pago e conteúdo orgânico"
  semana_3: "Otimizar com base em dados iniciais"
  mensal: "Revisão de CAC e ajuste de criativo"
frameworks:
  - Método HDIC de Sabri Suby (Horde-Direct-Convert)
  - Pirâmide de Consciência (3% → 97%)
  - Os 3 Pilares de Jay Abraham
```

### Estrutura de Funil de Prospecção

```
TOPO DE FUNIL (Awareness):
  → Conteúdo orgânico: problemas do avatar
  → Anúncios: audiência fria (interesse + lookalike)
  → Objetivo: tráfego para lead magnet

MEIO DE FUNIL (Interesse):
  → Lead magnet de alto valor (PDF, mini-curso, webinar)
  → Sequência de email de nutrição (7-10 dias)
  → Retargeting para visitantes do site
  → Objetivo: qualificação e aquecimento

FUNDO DE FUNIL (Decisão):
  → Oferta direta para leads quentes
  → Testemunhos e casos de sucesso
  → Garantia e remoção de objeções
  → Objetivo: conversão em cliente
```

### Checklist de Prospecção

```
SETUP INICIAL:
[ ] Definir avatar detalhado (Research Agent)
[ ] Criar lead magnet de alto valor (Copy Agent)
[ ] Construir landing page de captura (Copy + Design Agent)
[ ] Configurar sequência de nutrição por email (Email Agent)
[ ] Definir orçamento e canais de tráfego pago

OPERAÇÃO SEMANAL:
[ ] Publicar 3-5 posts de topo de funil
[ ] Monitorar CPL e otimizar criativos
[ ] Revisar métricas da sequência de email
[ ] Testar nova variante de landing page (A/B)

ANÁLISE MENSAL:
[ ] CAC vs LTV: está sustentável?
[ ] Qual canal tem menor CPL?
[ ] Qual email da sequência tem mais conversão?
[ ] Próximo teste A/B prioritário
```

### KPIs de Prospecção

| KPI | Meta | Canal |
|-----|------|-------|
| CPL (Custo por Lead) | < R$15-50 (varia por nicho) | Ads |
| Taxa de opt-in | > 35% | Landing page |
| Taxa de abertura nutrição | > 30% | Email |
| CAC (Custo de Aquisição) | < LTV/3 | Todos |

---

## Preset 3: /campanha retencao

**Objetivo:** Aumentar o LTV, reativar clientes inativos e reduzir churn.

### Configuração Automática

```yaml
tipo: retencao
clone_primario: abraham
clone_alternativo: leila-hormozi
agentes_ativos:
  - Research Agent (análise de clientes inativos e churn)
  - Copy Agent (copy de reativação e upsell)
  - Email Agent (sequências de reativação e onboarding)
  - Social Agent (conteúdo para clientes existentes)
  - Analytics Agent (análise de LTV e churn)
sequencia_default:
  imediato: "Campanha de reativação (clientes 90+ dias inativos)"
  mensal: "Sequência de upsell para clientes ativos"
  trimestral: "Campanha de indicação e referral"
frameworks:
  - Os 3 Pilares de Abraham (Pilar 2 e 3)
  - LTV Maximization
  - Reactivation Sequence de Dan Kennedy
```

### Segmentação de Clientes para Retenção

```
SEGMENTO 1 — CLIENTES INATIVOS (> 90 dias):
  Campanha: Reativação com oferta exclusiva
  Tom: Reconexão genuína (estilo Abraham)
  Sequência: 5 emails em 14 dias
  Oferta: Desconto de retorno ou bônus especial

SEGMENTO 2 — CLIENTES ATIVOS (última compra < 90 dias):
  Campanha: Upsell e cross-sell
  Tom: Confiante, baseado em resultados (estilo Hormozi)
  Sequência: Email + social
  Oferta: Produto complementar ou upgrade

SEGMENTO 3 — CLIENTES VIP (top 20% em valor):
  Campanha: Programa de fidelidade e indicação
  Tom: Exclusivo e personalizado
  Sequência: Email personalizado + ligação (se high-ticket)
  Oferta: Benefícios exclusivos + programa de referral

SEGMENTO 4 — EM RISCO DE CHURN (queda de engajamento):
  Campanha: Engajamento de emergência
  Tom: Direto, perguntando o problema
  Sequência: 3 emails rápidos
  Oferta: Suporte personalizado ou sessão gratuita
```

### Checklist de Retenção

```
SETUP (uma vez):
[ ] Segmentar base de clientes por recência e valor
[ ] Criar sequência de onboarding (novos clientes)
[ ] Criar sequência de reativação (inativos)
[ ] Criar sequência de upsell (clientes ativos)
[ ] Definir critérios de "cliente em risco"

OPERAÇÃO MENSAL:
[ ] Exportar lista de clientes inativos do mês
[ ] Rodar campanha de reativação
[ ] Identificar oportunidades de upsell
[ ] Analisar taxa de churn

KPIs:
[ ] LTV médio aumentando?
[ ] Taxa de reativação > 10%?
[ ] Taxa de upsell > 15%?
[ ] Churn abaixo da meta?
```

---

## Preset 4: /campanha autoridade

**Objetivo:** Construir autoridade, credibilidade e presença de marca no nicho.

### Configuração Automática

```yaml
tipo: autoridade
clone_primario: ogilvy
clone_alternativo: abdaal
agentes_ativos:
  - Research Agent (análise de temas de autoridade no nicho)
  - Copy Agent (artigos, posts de posicionamento)
  - SEO Agent (conteúdo otimizado para busca)
  - Social Agent (calendário editorial de autoridade)
  - Storytelling Agent (narrativas de credibilidade)
  - Brand Agent (consistência de identidade)
  - Audio Agent (podcast ou conteúdo em áudio)
sequencia_default:
  semanal: "2-3 posts de valor profundo"
  quinzenal: "1 artigo longo (SEO)"
  mensal: "1 caso de estudo ou entrevista"
frameworks:
  - Content Marketing de David Ogilvy
  - Evidence-Based Content de Ali Abdaal
  - Preeminência de Jay Abraham
```

### Pilares de Conteúdo de Autoridade

```
PILAR 1 — EDUCAÇÃO (40% do conteúdo):
  O quê: Ensina algo específico e útil
  Tom: Expert que democratiza conhecimento
  Formato: Carrossel, artigo, vídeo tutorial
  Objetivo: Ser referência no assunto

PILAR 2 — PERSPECTIVA (30% do conteúdo):
  O quê: Opinião baseada em dados sobre tendências
  Tom: Analítico e corajoso (não segue o rebanho)
  Formato: Post de texto, LinkedIn, thread
  Objetivo: Diferenciação e personalidade

PILAR 3 — PROVA (20% do conteúdo):
  O quê: Casos de sucesso, resultados, bastidores
  Tom: Transparente e específico
  Formato: Depoimento, estudo de caso, antes/depois
  Objetivo: Credibilidade e conversão

PILAR 4 — HUMANIZAÇÃO (10% do conteúdo):
  O quê: Falhas, jornada, curiosidades pessoais
  Tom: Vulnerável e acessível
  Formato: Stories, vídeo informal
  Objetivo: Conexão e retenção
```

---

## Preset 5: /campanha growth

**Objetivo:** Experimentação acelerada para crescimento não-linear.

### Configuração Automática

```yaml
tipo: growth
clone_primario: ellis
clone_alternativo: chen
agentes_ativos:
  - Research Agent (análise de dados e oportunidades)
  - AB Testing Agent (design e análise de experimentos)
  - Analytics Agent (tracking e análise de dados)
  - Copy Agent (variantes de copy para testes)
  - Growth Agent (estratégias de growth hacking)
sequencia_default:
  semanal: "1 experimento lançado, 1 analisado"
  mensal: "Review de todos experimentos + next batch"
frameworks:
  - ICE Score (Sean Ellis)
  - Growth Loop
  - Viral Coefficient
  - AARRR Metrics (Pirate Metrics)
```

### Framework de Experimentos de Growth

```
ETAPA 1 — HIPÓTESE (segunda-feira):
  "Se [mudança], então [métrica] vai [melhorar] porque [razão]"
  ICE Score: Impacto × Confiança × Facilidade

ETAPA 2 — DESIGN (terça-feira):
  - Definir variante A (controle) e variante B
  - Calcular tamanho mínimo de amostra
  - Configurar rastreamento
  - Definir critério de parada

ETAPA 3 — EXECUÇÃO (quarta a sexta):
  - Lançar experimento
  - Não analisar antes do tempo definido
  - Documentar qualquer variável externa

ETAPA 4 — ANÁLISE (segunda-feira seguinte):
  - Calcular significância estatística
  - Analisar segmentos
  - Decisão: implementar / iterar / descartar

ETAPA 5 — DOCUMENTAÇÃO (sempre):
  - Registrar no log de experimentos
  - Aprendizados mesmo em casos negativos
  - Próxima hipótese baseada no aprendizado
```

---

## Preset 6: /campanha black-friday

**Objetivo:** Maximizar receita em datas especiais (Black Friday, datas comemorativas).

### Configuração Automática

```yaml
tipo: black-friday
clone_primario: hormozi
clone_alternativo: suby
agentes_ativos:
  - Copy Agent (copy de alta urgência e valor)
  - Email Agent (sequência intensiva 7 dias)
  - Ads Agent (campanhas de conversão agressivas)
  - Social Agent (contagem regressiva + promoção)
  - Analytics Agent (monitoramento em tempo real)
cronograma:
  dia_-7: "Teaser e lista VIP"
  dia_-3: "Anúncio oficial da promoção"
  dia_-1: "Último aviso"
  dia_0: "Abertura — Black Friday"
  dia_+1: "Cyber Monday (se aplicável)"
  dia_+2: "Última chance"
frameworks:
  - Value Stack de Hormozi
  - Urgência Real (não artificial)
  - Scarcity Marketing
```

### Checklist Black Friday

```
3 SEMANAS ANTES:
[ ] Definir a oferta (produto + bônus + desconto)
[ ] Calcular o valor stack para justificar o preço
[ ] Criar lista de espera VIP
[ ] Preparar todo o copy da campanha
[ ] Design dos assets da campanha

1 SEMANA ANTES:
[ ] Configurar anúncios (não ativar ainda)
[ ] Testar página de vendas/checkout
[ ] Agendar posts e emails
[ ] Briefing da equipe (se tiver)

NO DIA:
[ ] Ativar anúncios às 00h01
[ ] Enviar email de abertura
[ ] Postar em todas as plataformas
[ ] Monitorar métricas de hora em hora

KPIs:
[ ] Receita vs. meta
[ ] ROAS > 4x (Black Friday tem melhor ROAS)
[ ] Taxa de conversão vs. campanha normal
```

---

## Como Usar os Presets

### Ativação Rápida

Para ativar um preset, simplesmente especifique o tipo:

```
/campanha lancamento
→ Carrega todos os agentes, clone e checklist de lançamento

/campanha prospeccao
→ Carrega foco em geração de leads e funil de entrada

/campanha retencao
→ Carrega foco em LTV, reativação e upsell
```

### Customização

Cada preset pode ser customizado com parâmetros adicionais:

```
/campanha lancamento --produto="Curso de Copy" --preco=997 --clone=hormozi
/campanha prospeccao --canal=instagram --budget=500 --nicho=empreendedorismo
/campanha retencao --segmento=inativos-90dias --desconto=20%
```

### Combinação com Clone System

Cada preset tem um clone recomendado, mas você pode substituir:

```
/campanha autoridade --clone=garyvee
→ Usa tom de Gary Vee em vez de Ogilvy

/campanha lancamento --clone=kennedy
→ Usa abordagem de marketing direto de Kennedy
```

---

## Recursos Relacionados

- [workflows/end-to-end-campaign-workflow.md](../workflows/end-to-end-campaign-workflow.md) — Workflow completo de campanha
- [workflows/content-pipeline.md](../workflows/content-pipeline.md) — Pipeline de produção de conteúdo
- [squads/marketing-os/data/clones/clone-manifest.yaml](../../squads/marketing-os/data/clones/clone-manifest.yaml) — Sistema de clones
- [subagents/ab-testing-agent.md](../subagents/ab-testing-agent.md) — Testes A/B para campanhas
- [scripts/ab_generator.py](../scripts/ab_generator.py) — Geração automática de variantes
