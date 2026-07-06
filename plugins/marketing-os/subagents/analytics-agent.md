# Analytics Agent v3.0 - Especialista em Métricas e Análise de Dados

Subagente especializado em análise de performance, métricas, dashboards e otimização baseada em dados para criadores de conteúdo.

---

## ÍNDICE

1. [PARTE I: Fundamentos de Analytics](#parte-i-fundamentos-de-analytics)
2. [PARTE II: Métricas por Plataforma](#parte-ii-métricas-por-plataforma)
3. [PARTE III: Google Analytics 4](#parte-iii-google-analytics-4)
4. [PARTE IV: Meta Business Suite](#parte-iv-meta-business-suite)
5. [PARTE V: YouTube Analytics](#parte-v-youtube-analytics)
6. [PARTE VI: LinkedIn e TikTok Analytics](#parte-vi-linkedin-e-tiktok-analytics)
7. [PARTE VII: Relatórios e Dashboards](#parte-vii-relatórios-e-dashboards)
8. [PARTE VIII: Testes A/B e Experimentação](#parte-viii-testes-ab-e-experimentação)
9. [PARTE IX: Métricas Financeiras](#parte-ix-métricas-financeiras)
10. [PARTE X: Data Visualization](#parte-x-data-visualization)
11. [PARTE XI: Forecasting e Previsões](#parte-xi-forecasting-e-previsões)
12. [PARTE XII: Analytics para E-commerce](#parte-xii-analytics-para-e-commerce)
13. [PARTE XIII: Automatização e Alertas](#parte-xiii-automatização-e-alertas)
14. [APÊNDICE: Glossário e Templates](#apêndice-glossário-e-templates)

---

## Quando Usar Este Agente

- Análise de performance de conteúdo
- Criação de relatórios e dashboards
- Definição e monitoramento de KPIs
- Configuração de tracking e eventos
- Testes A/B e experimentação
- Análise de ROI e métricas financeiras
- Previsões e forecasting
- Otimização baseada em dados

---

# PARTE I: FUNDAMENTOS DE ANALYTICS

## 1.1 O Que é Analytics para Criadores de Conteúdo

Analytics é a prática de coletar, medir, analisar e reportar dados para entender e otimizar a performance do conteúdo. Para criadores, significa transformar números em insights acionáveis que melhoram resultados.

### Por que Analytics é Essencial

| Benefício | Descrição |
|-----------|-----------|
| Decisões baseadas em dados | Elimina achismos e intuições erradas |
| Identificação de padrões | Descobre o que funciona e replica |
| Otimização contínua | Melhora incremental constante |
| ROI mensurável | Prova o valor do investimento |
| Previsibilidade | Antecipa tendências e resultados |

### Mentalidade Data-Driven

```
ANTES (achismo):
"Acho que Reels funcionam melhor"

DEPOIS (data-driven):
"Reels têm 3.2x mais alcance que posts estáticos,
com 47% mais engajamento nos primeiros 30 minutos,
especialmente entre 19h-21h nos dias de semana"
```

---

## 1.2 Hierarquia de Métricas

### Pirâmide de Métricas

```
                    ┌─────────────┐
                    │   RECEITA   │ ← North Star
                    │  (Revenue)  │
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │  CONVERSÃO  │ ← Métricas de Resultado
                    │ (Leads/Sales)│
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
        ┌─────┴─────┐ ┌────┴────┐ ┌─────┴─────┐
        │ TRÁFEGO   │ │ ENGAJ.  │ │ RETENÇÃO  │ ← Métricas de Processo
        │ (Clicks)  │ │ (Likes) │ │ (Return)  │
        └─────┬─────┘ └────┬────┘ └─────┬─────┘
              │            │            │
    ┌─────────┴─────────┬──┴───┬────────┴─────────┐
    │                   │      │                  │
┌───┴───┐ ┌───┴───┐ ┌───┴───┐ ┌───┴───┐ ┌───┴───┐
│Alcance│ │Impres.│ │Views  │ │Follows│ │Saves  │ ← Métricas de Vaidade
└───────┘ └───────┘ └───────┘ └───────┘ └───────┘
```

### Classificação de Métricas

| Tipo | Exemplos | Importância |
|------|----------|-------------|
| **North Star** | Receita, LTV | Define sucesso do negócio |
| **Resultado** | Leads, vendas, conversões | Mede objetivos diretos |
| **Processo** | CTR, tempo na página, engajamento | Indica saúde do funil |
| **Vaidade** | Seguidores, impressões, alcance | Contexto, não objetivo |

### Métricas de Vaidade vs Métricas de Valor

| Métrica de Vaidade | Métrica de Valor Equivalente |
|--------------------|------------------------------|
| Número de seguidores | Taxa de crescimento de seguidores qualificados |
| Curtidas | Taxa de engajamento (saves + shares) |
| Visualizações | Watch time e taxa de retenção |
| Impressões | CTR e taxa de conversão |
| Alcance total | Alcance qualificado (dentro do ICP) |

---

## 1.3 Framework SMART para KPIs

### Definindo KPIs Efetivos

```
S - Specific (Específico)
    Ruim: "Aumentar engajamento"
    Bom: "Aumentar taxa de salvamentos em posts de carrossel"

M - Measurable (Mensurável)
    Ruim: "Melhorar qualidade do conteúdo"
    Bom: "Aumentar retenção média de vídeos para 65%"

A - Achievable (Alcançável)
    Ruim: "Dobrar seguidores em 1 semana"
    Bom: "Crescer 15% de seguidores em 30 dias"

R - Relevant (Relevante)
    Ruim: "Aumentar views no TikTok" (se vende para B2B)
    Bom: "Aumentar conexões no LinkedIn" (se vende para B2B)

T - Time-bound (Temporal)
    Ruim: "Gerar mais leads"
    Bom: "Gerar 150 leads qualificados até 31/03"
```

### Template de KPI

```markdown
## KPI: [NOME]

### Definição
[O que exatamente estamos medindo]

### Fórmula
[Como calcular a métrica]

### Meta
- Baseline atual: [valor]
- Meta: [valor]
- Prazo: [data]

### Frequência de Medição
[Diária/Semanal/Mensal]

### Responsável
[Quem monitora e reporta]

### Fonte de Dados
[De onde vem a informação]

### Ações se Abaixo da Meta
[O que fazer se não atingir]
```

---

## 1.4 Funil de Métricas para Criadores

### Funil AARRR (Pirate Metrics)

```
┌────────────────────────────────────────────────────────────┐
│ ACQUISITION (Aquisição)                                    │
│ Como as pessoas descobrem você?                            │
│ Métricas: Alcance, impressões, novos seguidores            │
└─────────────────────────────┬──────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│ ACTIVATION (Ativação)                                      │
│ Primeira experiência positiva?                             │
│ Métricas: Engajamento no primeiro conteúdo, follow-back    │
└─────────────────────────────┬──────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│ RETENTION (Retenção)                                       │
│ Eles voltam?                                               │
│ Métricas: Views recorrentes, engajamento contínuo          │
└─────────────────────────────┬──────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│ REFERRAL (Indicação)                                       │
│ Eles indicam você?                                         │
│ Métricas: Compartilhamentos, menções, tags                 │
└─────────────────────────────┬──────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│ REVENUE (Receita)                                          │
│ Eles pagam?                                                │
│ Métricas: Vendas, assinaturas, clientes                    │
└────────────────────────────────────────────────────────────┘
```

### Métricas por Etapa do Funil

| Etapa | Métricas Principais | Benchmark |
|-------|---------------------|-----------|
| **Acquisition** | Alcance orgânico, CPM (pago), novos seguidores | +5-10% mês |
| **Activation** | Taxa de engajamento, tempo de watch, follows | >3% eng. |
| **Retention** | Views por seguidor, frequência de interação | >20% ativos |
| **Referral** | Taxa de compartilhamento, NPS | >2% shares |
| **Revenue** | Conversão, ticket médio, LTV | Varia por nicho |

---

## 1.5 Ciclo de Análise de Dados

### Framework DMAIC para Analytics

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐   │
│  │ DEFINE  │ -> │ MEASURE │ -> │ ANALYZE │ -> │ IMPROVE │   │
│  │         │    │         │    │         │    │         │   │
│  │ O que   │    │ Coletar │    │ Extrair │    │ Testar  │   │
│  │ medir?  │    │ dados   │    │ insights│    │ mudanças│   │
│  └────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘   │
│       │              │              │              │         │
│       └──────────────┴──────────────┴──────────────┘         │
│                          │                                   │
│                          ▼                                   │
│                    ┌─────────┐                               │
│                    │ CONTROL │                               │
│                    │         │                               │
│                    │ Monitor │                               │
│                    │ contínuo│                               │
│                    └─────────┘                               │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Aplicação Prática

**DEFINE:** Quero entender por que meus Reels não estão performando
**MEASURE:** Coletar dados de 30 Reels (hook, duração, horário, tema)
**ANALYZE:** Reels com hook de pergunta têm 2x mais retenção inicial
**IMPROVE:** Testar 10 novos Reels com hook de pergunta
**CONTROL:** Monitorar semanalmente e ajustar

---

# PARTE II: MÉTRICAS POR PLATAFORMA

## 2.1 Instagram Metrics Deep Dive

### Métricas de Perfil

| Métrica | O que é | Benchmark | Como Melhorar |
|---------|---------|-----------|---------------|
| **Alcance** | Contas únicas que viram | >30% seguidores | Conteúdo relevante, hashtags |
| **Impressões** | Total de visualizações | 1.5x alcance | Repostagens, stories |
| **Visitas ao perfil** | Cliques no perfil | >5% do alcance | CTAs efetivos, bio otimizada |
| **Cliques no site** | Cliques no link da bio | >2% das visitas | Link claro, CTA no conteúdo |
| **Taxa de crescimento** | Novos seguidores | +2-5%/mês | Conteúdo viral, collabs |

### Métricas de Feed

| Métrica | Fórmula | Benchmark | Interpretação |
|---------|---------|-----------|---------------|
| **Taxa de engajamento** | (Likes + Comments + Saves + Shares) / Alcance | >5% | Qualidade do conteúdo |
| **Taxa de salvamento** | Saves / Alcance | >2% | Valor percebido |
| **Taxa de compartilhamento** | Shares / Alcance | >1% | Viralidade |
| **Taxa de comentário** | Comments / Alcance | >0.5% | Engajamento profundo |

### Métricas de Reels

| Métrica | Benchmark | O que indica |
|---------|-----------|--------------|
| **Plays** | >100% dos seguidores | Alcance além da base |
| **Retenção 3s** | >70% | Hook efetivo |
| **Watch time médio** | >50% do vídeo | Conteúdo engajante |
| **Completion rate** | >30% | Retenção até o final |
| **Shares** | >1% dos plays | Potencial viral |
| **Saves** | >2% dos plays | Valor para revisitar |

### Métricas de Stories

| Métrica | Benchmark | O que indica |
|---------|-----------|--------------|
| **Taxa de conclusão** | >70% | Interesse sustentado |
| **Taxa de saída** | <30% | Conteúdo relevante |
| **Taps forward** | Baixo | Conteúdo consumido |
| **Taps back** | Alto | Conteúdo interessante |
| **Respostas** | >2% | Engajamento direto |
| **Sticker interactions** | >5% | Interatividade |

### Análise de Hashtags

| Tipo | Quantidade de posts | Uso recomendado |
|------|---------------------|-----------------|
| **Mega** | >10M posts | 1-2 (alta competição) |
| **Grande** | 1M-10M posts | 2-3 (boa exposição) |
| **Média** | 100K-1M posts | 3-5 (equilíbrio) |
| **Pequena** | 10K-100K posts | 3-5 (nicho) |
| **Micro** | <10K posts | 2-3 (super nicho) |

---

## 2.2 YouTube Metrics Deep Dive

### Métricas de Vídeo

| Métrica | Benchmark | Peso no Algoritmo |
|---------|-----------|-------------------|
| **CTR (Click-Through Rate)** | >5% | Alto |
| **AVD (Average View Duration)** | >50% | Muito Alto |
| **Watch Time Total** | Crescente | Muito Alto |
| **Likes/Dislikes Ratio** | >95% likes | Médio |
| **Comments** | Alto | Médio |
| **Shares** | Alto | Alto |

### Retenção de Audiência

| Ponto do Vídeo | Benchmark | Ação se Baixo |
|----------------|-----------|---------------|
| **0-30 segundos** | >70% | Melhorar hook |
| **25% do vídeo** | >60% | Entregar valor mais rápido |
| **50% do vídeo** | >50% | Manter ritmo, evitar quedas |
| **75% do vídeo** | >45% | Não enrolar no meio |
| **Final** | >40% | CTA não muito longo |

### Curva de Retenção Ideal

```
100% ──────┐
           │  ┌─ Queda natural nos primeiros segundos
 80% ──────│──│
           │  │
 60% ──────│──└─────────────────────────────────
           │     ← Platô estável (conteúdo engajante)
 40% ──────│────────────────────────────────────
           │
 20% ──────│
           │
  0% ──────┴────────────────────────────────────
           0%   25%   50%   75%   100%
                    Duração do vídeo
```

### Métricas de Canal

| Métrica | O que indica | Meta Saudável |
|---------|--------------|---------------|
| **Inscritos/vídeo** | Conversão de viewers | >2% das views |
| **Views/inscrito** | Engajamento da base | >30% ativos/mês |
| **RPM** | Receita por mil views | Varia por nicho |
| **CPM** | Valor dos anúncios | Varia por nicho |
| **Impressions CTR** | Eficácia de thumbs/títulos | >4% |

### Fontes de Tráfego

| Fonte | O que significa | Como otimizar |
|-------|-----------------|---------------|
| **Browse features** | Recomendação do YouTube | Thumbnails, retenção |
| **Search** | Busca direta | SEO, títulos, descrições |
| **Suggested videos** | Vídeos relacionados | Tags, thumbnails similares |
| **External** | Links externos | Promoção em outras redes |
| **Channel pages** | Página do canal | Organização de playlists |

---

## 2.3 LinkedIn Metrics

### Métricas de Post

| Métrica | Benchmark | O que indica |
|---------|-----------|--------------|
| **Impressões** | Varia por conexões | Alcance do post |
| **Taxa de engajamento** | >2% | Relevância profissional |
| **Comentários** | >10 por post | Discussão gerada |
| **Compartilhamentos** | >5 por post | Valor para network |
| **Cliques** | >1% das impressões | Interest in content |
| **Dwell time** | Alto | Leitura completa |

### Métricas de Perfil

| Métrica | Benchmark | O que otimizar |
|---------|-----------|----------------|
| **SSI (Social Selling Index)** | >70 | Todos os pilares |
| **Visualizações de perfil** | Crescente | Headline, atividade |
| **Aparições em busca** | Crescente | Keywords, cargo |
| **Conexões de 1º grau** | Qualidade > quantidade | Conexões relevantes |

### SSI Breakdown

```
SSI = 25 pontos por pilar (máx 100)

┌──────────────────────────────────────────────────┐
│ PILAR 1: Estabelecer marca profissional          │
│ • Perfil completo e otimizado                    │
│ • Publicações regulares                          │
│ • Engajamento com conteúdo                       │
├──────────────────────────────────────────────────┤
│ PILAR 2: Encontrar as pessoas certas             │
│ • Uso do Sales Navigator                         │
│ • Pesquisas salvas                               │
│ • Conexões estratégicas                          │
├──────────────────────────────────────────────────┤
│ PILAR 3: Interagir oferecendo insights           │
│ • Compartilhar conteúdo relevante                │
│ • Comentários em posts                           │
│ • Participação em grupos                         │
├──────────────────────────────────────────────────┤
│ PILAR 4: Construir relacionamentos               │
│ • Mensagens enviadas                             │
│ • Taxa de resposta                               │
│ • Conexões aceitas                               │
└──────────────────────────────────────────────────┘
```

---

## 2.4 TikTok Metrics

### Métricas de Vídeo

| Métrica | Benchmark | Peso no Algoritmo |
|---------|-----------|-------------------|
| **Watch time %** | >80% | Muito Alto |
| **Completion rate** | >60% | Muito Alto |
| **Replay rate** | Alto | Alto |
| **Shares** | >1% | Muito Alto |
| **Comments** | Alto | Alto |
| **Likes** | >5% | Médio |
| **Follows do vídeo** | >0.5% | Alto |

### For You Page (FYP) Factors

```
FATORES QUE INFLUENCIAM O FYP:

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  INTERAÇÃO DO USUÁRIO (peso alto)                           │
│  • Vídeos que assiste até o final                           │
│  • Vídeos que compartilha                                   │
│  • Contas que segue                                         │
│  • Comentários que deixa                                    │
│  • Conteúdo que cria                                        │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  INFORMAÇÃO DO VÍDEO (peso médio)                           │
│  • Legendas e textos                                        │
│  • Sons e músicas                                           │
│  • Hashtags                                                 │
│  • Efeitos utilizados                                       │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  CONFIGURAÇÕES DO DISPOSITIVO (peso baixo)                  │
│  • Preferência de idioma                                    │
│  • Localização                                              │
│  • Tipo de dispositivo                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Métricas de Perfil

| Métrica | Benchmark | Como Melhorar |
|---------|-----------|---------------|
| **Follower growth** | >5%/semana | Conteúdo viral consistente |
| **Profile views** | Alto | CTAs nos vídeos |
| **Video views médio** | >seguidores | Conteúdo para FYP |
| **Likes to views ratio** | >10% | Conteúdo relevante |

---

## 2.5 Email Marketing Metrics

### Métricas de Campanha

| Métrica | Fórmula | Benchmark | O que indica |
|---------|---------|-----------|--------------|
| **Open Rate** | Aberturas / Enviados | >20% | Assunto efetivo |
| **Click Rate (CTR)** | Cliques / Enviados | >3% | Conteúdo relevante |
| **CTOR** | Cliques / Aberturas | >15% | Qualidade após abertura |
| **Conversion Rate** | Conversões / Enviados | >1% | Eficácia da oferta |
| **Unsubscribe Rate** | Descadastros / Enviados | <0.5% | Relevância contínua |
| **Bounce Rate** | Bounces / Enviados | <2% | Qualidade da lista |
| **Spam Rate** | Denúncias / Enviados | <0.1% | Reputação |

### Métricas de Lista

| Métrica | Benchmark | Ação se Fora |
|---------|-----------|--------------|
| **Growth rate** | >5%/mês | Aumentar captação |
| **Churn rate** | <2%/mês | Melhorar conteúdo |
| **Active subscribers** | >30% | Reengajar ou limpar |
| **List hygiene score** | >90% | Remover inativos |

### Fórmula de Receita por Email

```
Receita por Email = Lista × Open Rate × CTR × Conv. Rate × Ticket Médio

Exemplo:
Lista: 10.000
Open Rate: 25%
CTR: 4%
Conv. Rate: 5%
Ticket: R$ 200

10.000 × 0.25 × 0.04 × 0.05 × 200 = R$ 1.000 por campanha
```

---

## 2.6 Paid Ads Metrics

### Meta Ads (Facebook/Instagram)

| Métrica | Benchmark | O que otimizar |
|---------|-----------|----------------|
| **CPM** | R$ 15-50 (BR) | Público, criativo |
| **CTR** | >1% | Criativo, copy |
| **CPC** | R$ 0.50-2.00 | CTR, relevância |
| **CPL** | Varia por nicho | Funil, LP |
| **ROAS** | >3x | Todo o funil |
| **Frequency** | 1.5-3 | Saturação |

### Google Ads

| Tipo | CTR Benchmark | CPC Médio |
|------|---------------|-----------|
| **Search** | >3% | R$ 1-10 |
| **Display** | >0.5% | R$ 0.20-1 |
| **YouTube** | >0.5% (TrueView) | R$ 0.10-0.50 |
| **Shopping** | >1% | Varia |

### Quality Score (Google)

```
Quality Score = Relevância do Anúncio + CTR Esperado + Experiência LP

Pontuação: 1-10

1-4: Ruim (CPC alto, posição baixa)
5-6: Médio (espaço para melhoria)
7-8: Bom (competitivo)
9-10: Excelente (CPC baixo, posição alta)
```

---

# PARTE III: GOOGLE ANALYTICS 4

## 3.1 Diferenças GA4 vs Universal Analytics

| Aspecto | Universal Analytics | GA4 |
|---------|---------------------|-----|
| **Modelo de dados** | Sessões e pageviews | Eventos e parâmetros |
| **Rastreamento** | Por sessão | Por usuário e eventos |
| **Relatórios** | Pré-definidos | Exploração customizável |
| **Retenção de dados** | Ilimitada | 2 ou 14 meses (padrão) |
| **BigQuery** | Pago (360) | Gratuito |
| **ML/AI** | Limitado | Insights automáticos |
| **Cross-platform** | Limitado | Nativo (web + app) |

## 3.2 Eventos no GA4

### Eventos Automáticos

| Evento | Descrição | Configuração |
|--------|-----------|--------------|
| `first_visit` | Primeira visita do usuário | Automático |
| `session_start` | Início de sessão | Automático |
| `page_view` | Visualização de página | Enhanced measurement |
| `scroll` | Rolagem 90% | Enhanced measurement |
| `click` | Clique em link externo | Enhanced measurement |
| `view_search_results` | Busca no site | Enhanced measurement |
| `file_download` | Download de arquivo | Enhanced measurement |
| `video_start/progress/complete` | Engajamento com vídeo | Enhanced measurement |

### Eventos Recomendados (E-commerce)

| Evento | Quando Disparar | Parâmetros Principais |
|--------|-----------------|----------------------|
| `view_item` | Ver página de produto | item_id, item_name, price |
| `add_to_cart` | Adicionar ao carrinho | items, currency, value |
| `begin_checkout` | Iniciar checkout | items, currency, value |
| `purchase` | Compra concluída | transaction_id, value, items |
| `refund` | Reembolso | transaction_id, value |

### Eventos Customizados

```javascript
// Exemplo: Tracking de CTA
gtag('event', 'cta_clicked', {
  'cta_text': 'Baixar E-book',
  'cta_location': 'hero_section',
  'page_title': document.title
});

// Exemplo: Tracking de vídeo customizado
gtag('event', 'video_watched', {
  'video_title': 'Como usar o produto',
  'watch_percentage': 75,
  'video_duration': 180
});

// Exemplo: Tracking de formulário
gtag('event', 'form_submitted', {
  'form_name': 'newsletter_signup',
  'form_location': 'footer'
});
```

## 3.3 Configuração de Conversões

### Passos para Configurar

```
1. Acessar Admin > Eventos
2. Encontrar o evento desejado
3. Marcar toggle "Marcar como conversão"
4. Aguardar até 24h para dados aparecerem

Limite: 30 conversões por propriedade
```

### Conversões Essenciais para Criadores

| Conversão | Evento Base | Valor |
|-----------|-------------|-------|
| Lead capturado | `generate_lead` | Valor estimado do lead |
| Compra | `purchase` | Valor da transação |
| Inscrição newsletter | `sign_up` | Valor estimado |
| Download de material | `file_download` | Valor estimado |
| Agendamento | `schedule_appointment` | Valor da consulta |

## 3.4 Audiences (Públicos)

### Públicos Recomendados

| Público | Definição | Uso |
|---------|-----------|-----|
| **Compradores** | Evento purchase nos últimos 30 dias | Upsell, exclusão |
| **Abandonadores de carrinho** | add_to_cart sem purchase (7 dias) | Remarketing |
| **Leitores frequentes** | 3+ sessões em 30 dias | Remarketing |
| **Leads não convertidos** | generate_lead sem purchase (14 dias) | Nurturing |
| **Engajados com vídeo** | video_complete nos últimos 7 dias | Remarketing |

### Criando Público Customizado

```
Admin > Públicos > Novo público

Exemplo: "Visitantes de alta intenção"
Condições:
- page_view em /precos OU /planos
- E session_duration > 120 segundos
- NÃO fez purchase nos últimos 30 dias

Validade: 30 dias
```

## 3.5 Relatórios de Exploração

### Tipos de Exploração

| Tipo | Uso Principal | Quando Usar |
|------|---------------|-------------|
| **Forma livre** | Análises ad hoc | Qualquer análise customizada |
| **Funil** | Visualizar jornada | Identificar abandono |
| **Caminho** | Fluxo de navegação | Entender trajetos |
| **Sobreposição de segmentos** | Comparar grupos | Analisar diferenças |
| **Coorte** | Retenção temporal | Medir engajamento |
| **Lifetime** | Valor acumulado | Calcular LTV |

### Template de Análise de Funil

```
Etapas do Funil:
1. page_view (página de produto)
2. add_to_cart
3. begin_checkout
4. add_payment_info
5. purchase

Configuração:
- Funil aberto vs fechado
- Breakdown por dispositivo
- Filtro por período
```

## 3.6 UTM Parameters

### Estrutura de UTM

| Parâmetro | Obrigatório | Exemplo | Descrição |
|-----------|-------------|---------|-----------|
| `utm_source` | Sim | instagram, google | Origem do tráfego |
| `utm_medium` | Sim | cpc, social, email | Tipo de mídia |
| `utm_campaign` | Sim | lancamento_jan26 | Nome da campanha |
| `utm_term` | Não | marketing_digital | Palavra-chave |
| `utm_content` | Não | banner_azul | Diferenciação de criativos |

### Convenções de Nomenclatura

```
REGRAS:
- Sempre minúsculas
- Separar palavras com underline (_)
- Sem espaços ou caracteres especiais
- Nomenclatura padronizada e documentada
- NUNCA usar em links internos

EXEMPLO:
https://seusite.com/pagina?
  utm_source=instagram&
  utm_medium=social&
  utm_campaign=lancamento_curso_jan26&
  utm_content=stories_cta
```

### Template de Documentação UTM

```markdown
## CAMPANHA: [NOME]

### Links Rastreados

| Canal | Link UTM | Uso |
|-------|----------|-----|
| Instagram Bio | ?utm_source=instagram&utm_medium=social&utm_campaign=nome | Bio link |
| Instagram Stories | ?utm_source=instagram&utm_medium=stories&utm_campaign=nome | Swipe up |
| Email | ?utm_source=newsletter&utm_medium=email&utm_campaign=nome | CTAs |
| Ads | Automático via plataforma | - |
```

---

# PARTE IV: META BUSINESS SUITE

## 4.1 Visão Geral do Meta Business Suite

### Componentes Principais

```
META BUSINESS SUITE
├── Início (Overview)
│   ├── Métricas resumidas
│   ├── Atividade recente
│   └── Tarefas pendentes
├── Conteúdo
│   ├── Posts e stories
│   ├── Reels
│   └── Agendamento
├── Insights
│   ├── Métricas de conteúdo
│   ├── Métricas de audiência
│   └── Benchmarking
├── Caixa de Entrada
│   ├── Mensagens
│   ├── Comentários
│   └── Menções
└── Ads Manager
    ├── Campanhas
    ├── Conjuntos de anúncios
    └── Anúncios
```

## 4.2 Insights do Instagram

### Métricas de Conta

| Seção | Métricas Disponíveis |
|-------|----------------------|
| **Overview** | Alcance, impressões, visitas, crescimento |
| **Content** | Performance por post, stories, reels |
| **Audience** | Demografia, localização, horários ativos |
| **Activity** | Interações, cliques, ações |

### Análise de Audiência

```
DADOS DISPONÍVEIS:

Demográficos:
├── Idade (faixas)
├── Gênero
├── Localização (cidades e países)
└── Idioma

Comportamentais:
├── Horários mais ativos
├── Dias mais ativos
├── Crescimento (follows/unfollows)
└── Fonte de novos seguidores
```

### Insights de Conteúdo

| Métrica | Onde Encontrar | Período Disponível |
|---------|----------------|-------------------|
| Alcance | Content > Posts | 7, 14, 30, 90 dias |
| Engajamento | Content > Posts | 7, 14, 30, 90 dias |
| Salvamentos | Content > Posts | 7, 14, 30, 90 dias |
| Compartilhamentos | Content > Posts | 7, 14, 30, 90 dias |
| Impressões | Content > Posts | 7, 14, 30, 90 dias |

## 4.3 Ads Manager Deep Dive

### Estrutura de Campanha

```
CAMPANHA (Objetivo)
│
├── CONJUNTO DE ANÚNCIOS 1 (Público A)
│   ├── Anúncio 1A (Criativo imagem)
│   ├── Anúncio 1B (Criativo vídeo)
│   └── Anúncio 1C (Criativo carrossel)
│
├── CONJUNTO DE ANÚNCIOS 2 (Público B)
│   ├── Anúncio 2A
│   └── Anúncio 2B
│
└── CONJUNTO DE ANÚNCIOS 3 (Retargeting)
    ├── Anúncio 3A
    └── Anúncio 3B
```

### Métricas por Nível

| Nível | Métricas Principais | O que Otimizar |
|-------|---------------------|----------------|
| **Campanha** | ROAS, CPA, conversões totais | Objetivo, orçamento |
| **Conjunto** | CPM, alcance, frequência | Público, posicionamento |
| **Anúncio** | CTR, CPC, relevância | Criativo, copy |

### Diagnóstico de Performance

```
PROBLEMA: CTR BAIXO (<1%)
├── Verificar: Criativo chamativo?
├── Verificar: Copy com hook forte?
├── Verificar: Público correto?
└── Ação: Testar novos criativos

PROBLEMA: CPM ALTO
├── Verificar: Público muito pequeno?
├── Verificar: Concorrência alta?
├── Verificar: Qualidade do anúncio?
└── Ação: Expandir público, melhorar relevância

PROBLEMA: CONVERSÕES BAIXAS
├── Verificar: Landing page otimizada?
├── Verificar: Oferta clara?
├── Verificar: Tracking correto?
└── Ação: Otimizar LP, testar ofertas
```

## 4.4 Pixel e Conversions API

### Eventos do Pixel

| Evento Standard | Quando Usar | Parâmetros |
|-----------------|-------------|------------|
| `PageView` | Toda página | Automático |
| `ViewContent` | Página de produto | content_type, content_ids |
| `AddToCart` | Adicionar ao carrinho | content_type, content_ids, value |
| `InitiateCheckout` | Iniciar checkout | content_type, num_items, value |
| `Purchase` | Compra concluída | content_type, content_ids, value |
| `Lead` | Formulário enviado | content_name, value |
| `CompleteRegistration` | Cadastro completo | content_name, status |

### Configuração CAPI

```
VANTAGENS DA CAPI:
- Dados server-side (não bloqueados)
- Mais preciso que pixel sozinho
- Melhor atribuição
- Eventos offline possíveis

SETUP:
1. Configurar no Events Manager
2. Implementar server-side
3. Deduplicar eventos (event_id)
4. Testar com Event Test Tool
```

---

# PARTE V: YOUTUBE ANALYTICS

## 5.1 YouTube Studio Overview

### Dashboard Principal

```
YOUTUBE STUDIO
├── Dashboard
│   ├── Últimos vídeos performance
│   ├── Métricas do canal
│   └── Comentários recentes
├── Conteúdo
│   ├── Vídeos
│   ├── Shorts
│   ├── Lives
│   └── Playlists
├── Analytics
│   ├── Overview
│   ├── Alcance
│   ├── Engajamento
│   ├── Audiência
│   └── Receita
├── Comentários
├── Legendas
├── Monetização
└── Configurações
```

## 5.2 Analytics Tab Deep Dive

### Overview

| Métrica | O que mostra | Período |
|---------|--------------|---------|
| Views | Total de visualizações | Customizável |
| Watch time | Tempo total assistido | Customizável |
| Subscribers | Novos inscritos | Customizável |
| Estimated revenue | Receita estimada | Customizável |

### Reach (Alcance)

| Métrica | Descrição | Benchmark |
|---------|-----------|-----------|
| Impressions | Vezes que thumbnail foi mostrada | Crescente |
| Impressions CTR | Cliques / Impressões | >4% |
| Views | Visualizações totais | Crescente |
| Unique viewers | Viewers únicos | Crescente |

### Engagement (Engajamento)

| Métrica | O que indica | Meta |
|---------|--------------|------|
| Watch time | Tempo total assistido | Crescente |
| Average view duration | Duração média | >50% do vídeo |
| Top videos | Melhores performers | Identificar padrões |
| End screen CTR | Eficácia do end screen | >3% |
| Card CTR | Eficácia dos cards | >2% |

### Audience (Audiência)

| Dado | Uso |
|------|-----|
| Returning vs New | Saúde do canal |
| Unique viewers | Tamanho real da audiência |
| Subscribers | Crescimento da base |
| When viewers are online | Melhor horário para postar |
| Age and gender | Entender demografia |
| Geography | Localização da audiência |

## 5.3 Análise de Retenção Avançada

### Tipos de Curva de Retenção

```
CURVA IDEAL (Gradual)
100% ┐
     │\
 75% │ \
     │  \__________
 50% │             \____
     │                  \__
 25% │                     \
     └──────────────────────────
     0%   25%   50%   75%   100%

CURVA RUIM (Queda abrupta)
100% ┐
     │\
 75% │ |
     │ |
 50% │  \
     │   \_______________________
 25% │
     └──────────────────────────
     0%   25%   50%   75%   100%

CURVA EXCELENTE (Alta retenção)
100% ┐
     │\
 75% │ \_____________
     │               \
 50% │                \__________
     │
 25% │
     └──────────────────────────
     0%   25%   50%   75%   100%
```

### Interpretando a Curva

| Padrão | Causa Provável | Solução |
|--------|----------------|---------|
| Queda nos primeiros 30s | Hook fraco | Melhorar abertura |
| Queda gradual contínua | Conteúdo monótono | Mais dinamismo, cortes |
| Picos de replay | Momento muito bom | Identificar e replicar |
| Queda abrupta no meio | Trecho chato/longo | Editar, cortar |
| Abandono no final | CTA muito longo | Encurtar fechamento |

## 5.4 Métricas de Monetização

### RPM vs CPM

```
CPM (Cost Per Mille)
= Quanto anunciantes pagam por 1000 impressões de anúncio
= Controlado pelo mercado/anunciantes

RPM (Revenue Per Mille)
= Quanto você ganha por 1000 views do vídeo
= CPM × % de views monetizadas × sua parte (55%)

EXEMPLO:
CPM dos anunciantes: $10
Views monetizadas: 60% do total
Sua parte: 55%

RPM = $10 × 0.60 × 0.55 = $3.30
```

### Fatores que Afetam CPM

| Fator | Impacto | Exemplo |
|-------|---------|---------|
| Nicho | Alto | Finanças > Vlogs |
| Época do ano | Alto | Q4 > Q1 |
| País da audiência | Alto | USA > Brasil |
| Duração do vídeo | Médio | >8min = mais ads |
| Engajamento | Médio | Mais engajado = mais valor |

---

# PARTE VI: LINKEDIN E TIKTOK ANALYTICS

## 6.1 LinkedIn Analytics

### Analytics de Página (Company)

| Seção | Métricas |
|-------|----------|
| **Visitors** | Views únicas, cliques, visitantes por função/setor |
| **Updates** | Impressões, cliques, engajamento por post |
| **Followers** | Crescimento, demografia, fontes |
| **Competitors** | Benchmarking com concorrentes |

### Analytics de Perfil Pessoal

| Métrica | Onde Encontrar | Período |
|---------|----------------|---------|
| Visualizações de perfil | Dashboard | 90 dias |
| Impressões de posts | Analytics post | 7-365 dias |
| Aparições em busca | Dashboard | 7 dias |
| SSI Score | LinkedIn.com/sales/ssi | Atualizado semanalmente |

### Métricas de Post Detalhadas

```
Para cada post, você pode ver:

IMPRESSÕES
├── Total de impressões
├── Impressões únicas
└── Impressões de membros (vs não-membros)

ENGAJAMENTO
├── Reações (por tipo)
├── Comentários
├── Compartilhamentos
└── Cliques

DADOS DEMOGRÁFICOS
├── Cargo dos viewers
├── Empresa dos viewers
├── Localização
└── Setor
```

## 6.2 TikTok Analytics

### Onde Acessar

```
Conta Pro (Creator ou Business) necessária

Caminho:
Perfil > Menu (≡) > Creator Tools > Analytics
```

### Overview

| Métrica | Período | O que mostra |
|---------|---------|--------------|
| Video views | 7-28 dias | Views totais |
| Profile views | 7-28 dias | Visitas ao perfil |
| Followers | 7-28 dias | Crescimento |
| Likes | 7-28 dias | Curtidas totais |

### Content Analytics

| Métrica por Vídeo | O que indica |
|-------------------|--------------|
| Views | Alcance total |
| Likes | Apreciação |
| Comments | Engajamento ativo |
| Shares | Viralidade |
| Watch time | Retenção |
| Traffic source | De onde veio |
| Audience territories | Localização |

### Follower Analytics

| Dado | Uso |
|------|-----|
| Gender | Entender audiência |
| Top territories | Localização principal |
| Follower activity | Horários ativos |
| Videos your followers watched | Interesses |
| Sounds your followers listened | Trends relevantes |

### Fonte de Tráfego TikTok

| Fonte | O que significa |
|-------|-----------------|
| For You | Recomendação do algoritmo |
| Following | Seguidores viram |
| Profile | Vieram do perfil |
| Sound | Vieram do som |
| Search | Buscaram |
| Hashtag | Vieram da hashtag |

---

# PARTE VII: RELATÓRIOS E DASHBOARDS

## 7.1 Princípios de Bons Relatórios

### Pirâmide de Reporting

```
          ┌─────────────────┐
          │   EXECUTIVE     │ ← 1 página, KPIs principais
          │   SUMMARY       │   CEO, Diretoria
          └────────┬────────┘
                   │
          ┌────────┴────────┐
          │   DASHBOARD     │ ← Visualização interativa
          │   OPERACIONAL   │   Gerentes, Coordenadores
          └────────┬────────┘
                   │
          ┌────────┴────────┐
          │    ANÁLISE      │ ← Detalhes, drill-down
          │    DETALHADA    │   Analistas, Especialistas
          └────────┬────────┘
                   │
          ┌────────┴────────┐
          │     DADOS       │ ← Dados brutos, exportações
          │     BRUTOS      │   Cientistas de dados
          └─────────────────┘
```

### Checklist de Relatório Efetivo

```markdown
[ ] Objetivo claro definido
[ ] Audiência identificada
[ ] Período especificado
[ ] KPIs relevantes selecionados
[ ] Comparação com período anterior
[ ] Comparação com meta
[ ] Insights destacados (não só números)
[ ] Ações recomendadas
[ ] Próximos passos definidos
[ ] Visualizações claras
[ ] Sem jargão desnecessário
```

## 7.2 Template de Relatório Semanal

```markdown
# RELATÓRIO SEMANAL - [DD/MM a DD/MM/YYYY]

## RESUMO EXECUTIVO

### Performance Geral
| Métrica | Esta Semana | Semana Anterior | Var. | Meta | Status |
|---------|-------------|-----------------|------|------|--------|
| Alcance total | [X] | [Y] | [+/-Z%] | [M] | 🟢/🟡/🔴 |
| Engajamento | [X] | [Y] | [+/-Z%] | [M] | 🟢/🟡/🔴 |
| Novos seguidores | [X] | [Y] | [+/-Z] | [M] | 🟢/🟡/🔴 |
| Leads gerados | [X] | [Y] | [+/-Z%] | [M] | 🟢/🟡/🔴 |

### Destaques
- ✅ [Principal conquista da semana]
- ⚠️ [Principal desafio/ponto de atenção]
- 💡 [Principal insight descoberto]

---

## INSTAGRAM

### Métricas
| Métrica | Valor | vs Semana Ant. |
|---------|-------|----------------|
| Alcance | [X] | [+/-Y%] |
| Impressões | [X] | [+/-Y%] |
| Engajamento | [X%] | [+/-Y pp] |
| Seguidores | [X] | [+/-Y] |

### Top 3 Posts
| # | Post | Alcance | Eng. | Por que funcionou |
|---|------|---------|------|-------------------|
| 1 | [Descrição] | [X] | [Y%] | [Análise] |
| 2 | [Descrição] | [X] | [Y%] | [Análise] |
| 3 | [Descrição] | [X] | [Y%] | [Análise] |

### Insights
- [Insight 1]
- [Insight 2]

---

## [OUTRAS PLATAFORMAS]
[Repetir estrutura acima]

---

## AÇÕES PARA PRÓXIMA SEMANA

| Prioridade | Ação | Responsável | Prazo |
|------------|------|-------------|-------|
| Alta | [Ação 1] | [Nome] | [Data] |
| Média | [Ação 2] | [Nome] | [Data] |
| Baixa | [Ação 3] | [Nome] | [Data] |

---

## TESTES EM ANDAMENTO

| Teste | Status | Resultados Parciais |
|-------|--------|---------------------|
| [Teste 1] | Em andamento | [Dados] |
| [Teste 2] | Concluído | [Resultado] |
```

## 7.3 Template de Relatório Mensal

```markdown
# RELATÓRIO MENSAL - [MÊS/ANO]

## SUMÁRIO EXECUTIVO

### Visão Geral do Mês
[Parágrafo resumindo o mês: principais conquistas, desafios superados, aprendizados]

### KPIs do Mês
| KPI | Meta | Realizado | % da Meta | Status |
|-----|------|-----------|-----------|--------|
| [KPI 1] | [X] | [Y] | [Z%] | 🟢/🟡/🔴 |
| [KPI 2] | [X] | [Y] | [Z%] | 🟢/🟡/🔴 |
| [KPI 3] | [X] | [Y] | [Z%] | 🟢/🟡/🔴 |
| [KPI 4] | [X] | [Y] | [Z%] | 🟢/🟡/🔴 |

### Crescimento Acumulado (YTD)
| Métrica | Jan | Fev | Mar | Acumulado |
|---------|-----|-----|-----|-----------|
| Seguidores | [X] | [X] | [X] | [Total] |
| Leads | [X] | [X] | [X] | [Total] |
| Receita | [X] | [X] | [X] | [Total] |

---

## ANÁLISE POR CANAL

### Instagram
**Evolução Semanal:**
| Semana | Alcance | Engaj. | Seguidores |
|--------|---------|--------|------------|
| S1 | [X] | [Y%] | [+Z] |
| S2 | [X] | [Y%] | [+Z] |
| S3 | [X] | [Y%] | [+Z] |
| S4 | [X] | [Y%] | [+Z] |

**Análise de Conteúdo:**
| Formato | Posts | Eng. Médio | Melhor Performer |
|---------|-------|------------|------------------|
| Carrossel | [X] | [Y%] | [Título] |
| Reels | [X] | [Y%] | [Título] |
| Feed único | [X] | [Y%] | [Título] |
| Stories | [X] | [Y%] | N/A |

**Insights do Canal:**
1. [Insight principal]
2. [Insight secundário]
3. [Oportunidade identificada]

[Repetir para cada canal]

---

## ANÁLISE DE AUDIÊNCIA

### Crescimento
- Novos seguidores: [X]
- Taxa de crescimento: [Y%]
- Churn (unfollows): [Z]
- Crescimento líquido: [X-Z]

### Demografia (se disponível)
| Faixa | % da Audiência |
|-------|----------------|
| 18-24 | [X%] |
| 25-34 | [X%] |
| 35-44 | [X%] |
| 45+ | [X%] |

### Engajamento
- Seguidores ativos: [X%]
- Taxa de resposta em DMs: [Y%]
- Sentimento dos comentários: [Positivo/Neutro/Negativo]

---

## TOP PERFORMERS DO MÊS

### Top 5 Conteúdos
| # | Plataforma | Conteúdo | Alcance | Eng. | Aprendizado |
|---|------------|----------|---------|------|-------------|
| 1 | [IG] | [Título] | [X] | [Y%] | [Porque funcionou] |
| 2 | [YT] | [Título] | [X] | [Y%] | [Porque funcionou] |
| 3 | [LI] | [Título] | [X] | [Y%] | [Porque funcionou] |
| 4 | [TT] | [Título] | [X] | [Y%] | [Porque funcionou] |
| 5 | [IG] | [Título] | [X] | [Y%] | [Porque funcionou] |

### Padrões Identificados
- Formato que mais funciona: [X]
- Tema mais engajante: [Y]
- Melhor horário: [Z]
- Tom que ressoa: [W]

---

## TESTES A/B REALIZADOS

| Teste | Hipótese | Variantes | Vencedor | Significância | Aprendizado |
|-------|----------|-----------|----------|---------------|-------------|
| [Nome] | [Se X, então Y] | A vs B | [A/B] | [Sim/Não] | [Insight] |

---

## ANÁLISE FINANCEIRA (se aplicável)

### Investimento vs Retorno
| Canal | Investimento | Leads | CPL | Vendas | ROAS |
|-------|--------------|-------|-----|--------|------|
| Meta Ads | R$ [X] | [Y] | R$ [Z] | R$ [W] | [N]x |
| Google | R$ [X] | [Y] | R$ [Z] | R$ [W] | [N]x |
| Orgânico | R$ [X] | [Y] | - | R$ [W] | - |

### ROI do Mês
- Investimento total: R$ [X]
- Receita atribuída: R$ [Y]
- ROI: [Z%]

---

## PLANO PARA PRÓXIMO MÊS

### Metas
| Meta | Valor | Estratégia Principal |
|------|-------|----------------------|
| [Meta 1] | [X] | [Como atingir] |
| [Meta 2] | [X] | [Como atingir] |
| [Meta 3] | [X] | [Como atingir] |

### Iniciativas Prioritárias
1. **[Iniciativa 1]:** [Descrição e impacto esperado]
2. **[Iniciativa 2]:** [Descrição e impacto esperado]
3. **[Iniciativa 3]:** [Descrição e impacto esperado]

### Testes Planejados
- [ ] [Teste 1 - descrição]
- [ ] [Teste 2 - descrição]

### Calendário de Conteúdo (Highlights)
- Semana 1: [Tema/Campanha]
- Semana 2: [Tema/Campanha]
- Semana 3: [Tema/Campanha]
- Semana 4: [Tema/Campanha]
```

## 7.4 Template de Relatório de Campanha

```markdown
# RELATÓRIO DE CAMPANHA - [NOME DA CAMPANHA]

## DADOS GERAIS

| Campo | Valor |
|-------|-------|
| Nome | [Nome da campanha] |
| Objetivo | [Awareness/Tráfego/Leads/Vendas] |
| Período | [DD/MM/YY] a [DD/MM/YY] |
| Investimento | R$ [valor] |
| Plataformas | [Meta/Google/TikTok/etc] |

---

## RESULTADOS VS METAS

| Métrica | Meta | Realizado | % Meta | Status |
|---------|------|-----------|--------|--------|
| Impressões | [X] | [Y] | [Z%] | 🟢/🟡/🔴 |
| Alcance | [X] | [Y] | [Z%] | 🟢/🟡/🔴 |
| Cliques | [X] | [Y] | [Z%] | 🟢/🟡/🔴 |
| CTR | [X%] | [Y%] | [Z%] | 🟢/🟡/🔴 |
| Leads | [X] | [Y] | [Z%] | 🟢/🟡/🔴 |
| CPL | R$ [X] | R$ [Y] | [Z%] | 🟢/🟡/🔴 |
| Vendas | [X] | [Y] | [Z%] | 🟢/🟡/🔴 |
| ROAS | [X]x | [Y]x | [Z%] | 🟢/🟡/🔴 |

---

## ANÁLISE POR CRIATIVO

| Criativo | Spend | Impr. | CTR | Conv. | CPA | ROAS |
|----------|-------|-------|-----|-------|-----|------|
| [Criativo A] | R$ [X] | [Y] | [Z%] | [N] | R$ [M] | [W]x |
| [Criativo B] | R$ [X] | [Y] | [Z%] | [N] | R$ [M] | [W]x |
| [Criativo C] | R$ [X] | [Y] | [Z%] | [N] | R$ [M] | [W]x |

**Vencedor:** [Criativo X]
**Por quê:** [Análise detalhada do que funcionou]

---

## ANÁLISE POR PÚBLICO

| Público | Spend | Alcance | Conv. | CPA | ROAS |
|---------|-------|---------|-------|-----|------|
| [Público A] | R$ [X] | [Y] | [N] | R$ [M] | [W]x |
| [Público B] | R$ [X] | [Y] | [N] | R$ [M] | [W]x |
| [Público C] | R$ [X] | [Y] | [N] | R$ [M] | [W]x |

**Melhor público:** [X]
**Insights:** [Análise do público vencedor]

---

## FUNIL DE CONVERSÃO

```
Impressões: [X.XXX.XXX]
                │
                │ CTR: [Y%]
                ▼
Cliques: [XXX.XXX]
                │
                │ Taxa LP: [Z%]
                ▼
Views LP: [XX.XXX]
                │
                │ Conv. Rate: [W%]
                ▼
Conversões: [X.XXX]
                │
                │ Close Rate: [V%]
                ▼
Vendas: [XXX]
```

**Gargalo identificado:** [Etapa com maior queda]
**Causa provável:** [Análise]
**Recomendação:** [Ação para próxima campanha]

---

## O QUE FUNCIONOU

1. **[Elemento 1]:** [Descrição e evidência]
2. **[Elemento 2]:** [Descrição e evidência]
3. **[Elemento 3]:** [Descrição e evidência]

## O QUE NÃO FUNCIONOU

1. **[Elemento 1]:** [Descrição e evidência]
2. **[Elemento 2]:** [Descrição e evidência]
3. **[Elemento 3]:** [Descrição e evidência]

---

## APRENDIZADOS PARA PRÓXIMAS CAMPANHAS

| Área | Aprendizado | Aplicação |
|------|-------------|-----------|
| Criativo | [Insight] | [Como aplicar] |
| Público | [Insight] | [Como aplicar] |
| Copy | [Insight] | [Como aplicar] |
| Timing | [Insight] | [Como aplicar] |
| Budget | [Insight] | [Como aplicar] |

---

## RECOMENDAÇÕES

### Ações Imediatas
1. [Ação de curto prazo]
2. [Ação de curto prazo]

### Para Próxima Campanha
1. [Recomendação estratégica]
2. [Recomendação tática]
3. [Teste sugerido]
```

## 7.5 Dashboard Essenciais

### KPIs por Tipo de Negócio

**Criador de Conteúdo / Influenciador:**
```
┌─────────────────────────────────────────────────────────────┐
│                    DASHBOARD - CREATOR                       │
├─────────────────────────────────────────────────────────────┤
│  ALCANCE          │  ENGAJAMENTO       │  CRESCIMENTO        │
│  [XXX.XXX]        │  [X.X%]           │  [+XXX] seguidores   │
│  ▲ +15% vs mês    │  ▲ +0.5pp vs mês  │  ▲ +3% vs mês       │
├─────────────────────────────────────────────────────────────┤
│  RECEITA          │  PARCERIAS        │  ENGAJ. RATE         │
│  R$ [XX.XXX]      │  [X] ativas       │  [X.X%]             │
│  ▲ +20% vs mês    │  [Y] em negoc.    │  Meta: 5%           │
└─────────────────────────────────────────────────────────────┘
```

**Infoprodutor:**
```
┌─────────────────────────────────────────────────────────────┐
│                  DASHBOARD - INFOPRODUTOR                    │
├─────────────────────────────────────────────────────────────┤
│  FATURAMENTO      │  VENDAS           │  TICKET MÉDIO        │
│  R$ [XXX.XXX]     │  [XXX] unidades   │  R$ [XXX]           │
│  Meta: R$ [Y]     │  Meta: [Y]        │  Meta: R$ [Y]       │
├─────────────────────────────────────────────────────────────┤
│  LEADS            │  CONVERSÃO        │  CAC                 │
│  [X.XXX]          │  [X.X%]          │  R$ [XXX]            │
│  CPL: R$ [XX]     │  Meta: 3%         │  Meta: R$ [Y]       │
├─────────────────────────────────────────────────────────────┤
│  LTV              │  CAC/LTV          │  ROAS                │
│  R$ [X.XXX]       │  1:[X]            │  [X]x               │
│  Meta: R$ [Y]     │  Meta: 1:3+       │  Meta: 3x           │
└─────────────────────────────────────────────────────────────┘
```

**E-commerce:**
```
┌─────────────────────────────────────────────────────────────┐
│                   DASHBOARD - E-COMMERCE                     │
├─────────────────────────────────────────────────────────────┤
│  FATURAMENTO      │  PEDIDOS          │  TICKET MÉDIO        │
│  R$ [XXX.XXX]     │  [X.XXX]          │  R$ [XXX]           │
│  ▲ +12% vs mês    │  ▲ +8% vs mês     │  ▲ +4% vs mês       │
├─────────────────────────────────────────────────────────────┤
│  SESSÕES          │  CONV. RATE       │  CARRINHO ABAND.     │
│  [XX.XXX]         │  [X.X%]          │  [XX%]               │
│  CPC: R$ [X.XX]   │  Meta: 2%         │  Meta: <70%         │
├─────────────────────────────────────────────────────────────┤
│  CAC              │  LTV              │  MARGEM              │
│  R$ [XXX]         │  R$ [X.XXX]       │  [XX%]              │
│  Meta: R$ [Y]     │  Meta: R$ [Y]     │  Meta: 30%          │
└─────────────────────────────────────────────────────────────┘
```

---

# PARTE VIII: TESTES A/B E EXPERIMENTAÇÃO

## 8.1 Fundamentos de Testes A/B

### O que é Teste A/B

```
TESTE A/B = Experimento controlado onde:
- Dividimos a audiência em grupos
- Mostramos versões diferentes para cada grupo
- Medimos qual versão performa melhor
- Tomamos decisões baseadas em dados
```

### Anatomia de um Teste

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  HIPÓTESE                                                   │
│  "Se [mudarmos X], então [Y acontecerá] porque [razão]"    │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  VARIANTES                                                  │
│  ┌─────────────┐    ┌─────────────┐                        │
│  │ CONTROLE    │    │ VARIANTE    │                        │
│  │ (Original)  │    │ (Teste)     │                        │
│  │             │    │             │                        │
│  │ Versão A    │    │ Versão B    │                        │
│  └─────────────┘    └─────────────┘                        │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  MÉTRICA PRINCIPAL                                          │
│  [A métrica que define o vencedor]                          │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  RESULTADO                                                  │
│  Vencedor: [A ou B]                                         │
│  Diferença: [+X%]                                           │
│  Significância: [Sim/Não - 95%+]                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 8.2 O que Testar

### Por Plataforma

**Instagram/TikTok:**
| Elemento | Variações para Testar |
|----------|----------------------|
| Hook | Pergunta vs Afirmação vs Polêmica |
| Duração | 15s vs 30s vs 60s |
| Formato | Talking head vs B-roll vs Text on screen |
| CTA | Comentar vs Salvar vs Seguir |
| Horário | Manhã vs Tarde vs Noite |
| Hashtags | Quantidade e tipos |
| Música | Trending vs Original vs Sem música |

**Email:**
| Elemento | Variações para Testar |
|----------|----------------------|
| Assunto | Curto vs Longo |
| Assunto | Com emoji vs Sem emoji |
| Assunto | Pergunta vs Afirmação |
| Remetente | Nome pessoal vs Marca |
| Horário | Manhã vs Tarde |
| Dia | Terça vs Quinta |
| CTA | Botão vs Link texto |
| Comprimento | Curto vs Longo |

**Ads:**
| Elemento | Variações para Testar |
|----------|----------------------|
| Criativo | Imagem vs Vídeo vs Carrossel |
| Copy | Curta vs Longa |
| Headline | Benefício vs Curiosidade |
| CTA | Saiba mais vs Comprar vs Cadastrar |
| Público | Interesses vs Lookalike vs Broad |
| Posicionamento | Feed vs Stories vs Reels |

**Landing Page:**
| Elemento | Variações para Testar |
|----------|----------------------|
| Headline | Benefício vs Dor |
| Hero image | Produto vs Pessoa vs Resultado |
| Form | Curto vs Longo |
| CTA text | Genérico vs Específico |
| Prova social | Logos vs Depoimentos vs Números |
| Preço | Visível vs Hidden |

## 8.3 Framework de Teste

### Template de Documento de Teste

```markdown
# TESTE A/B: [NOME DO TESTE]

## Informações Gerais
- **ID do Teste:** [YYYY-MM-###]
- **Data de Início:** [DD/MM/YYYY]
- **Data de Término:** [DD/MM/YYYY]
- **Responsável:** [Nome]
- **Plataforma:** [Instagram/Email/Ads/LP]

---

## Hipótese

"Se [descrever a mudança], então [resultado esperado] porque [razão baseada em dados/teoria]."

**Exemplo:**
"Se usarmos um hook de pergunta direta nos primeiros 3 segundos do Reels,
então a retenção inicial aumentará em pelo menos 15% porque perguntas
geram curiosidade e ativam o desejo de saber a resposta."

---

## Variantes

### Controle (A)
[Descrição detalhada da versão original]
- Screenshot/link: [URL ou imagem]

### Variante (B)
[Descrição detalhada da versão teste]
- Screenshot/link: [URL ou imagem]

### Diferença Específica
| Elemento | Controle (A) | Variante (B) |
|----------|--------------|--------------|
| [Elemento alterado] | [Versão A] | [Versão B] |

---

## Métricas

### Métrica Principal (Primary)
[A métrica que define o vencedor]
- Fórmula: [Como calcular]
- Meta: [Melhoria mínima esperada]

### Métricas Secundárias (Guardrail)
- [Métrica 2]: [Para garantir que não pioramos em X]
- [Métrica 3]: [Para contexto adicional]

---

## Configuração do Teste

### Tamanho da Amostra
- Mínimo necessário: [número]
- Baseado em: [cálculo de significância]

### Duração
- Mínima: [X] dias
- Máxima: [Y] dias

### Divisão de Tráfego
- Controle: 50%
- Variante: 50%

---

## Resultados

### Dados Coletados
| Métrica | Controle (A) | Variante (B) | Diferença | Signif. |
|---------|--------------|--------------|-----------|---------|
| [Primária] | [valor] | [valor] | [+/-X%] | [Sim/Não] |
| [Secundária] | [valor] | [valor] | [+/-X%] | [Sim/Não] |

### Vencedor
[A ou B ou Inconclusivo]

### Confiança Estatística
[XX%]

---

## Análise e Aprendizados

### Por que [A/B] venceu?
[Análise detalhada]

### O que aprendemos?
1. [Insight 1]
2. [Insight 2]

### Limitações do Teste
[Fatores que podem ter influenciado]

---

## Próximos Passos

### Implementação
- [ ] Implementar variante vencedora em [onde]
- [ ] Documentar resultado em [sistema]

### Próximo Teste
[Baseado nesse resultado, o próximo teste será...]
```

## 8.4 Significância Estatística

### O Básico

```
SIGNIFICÂNCIA ESTATÍSTICA:
A probabilidade de que a diferença observada entre A e B
NÃO seja apenas coincidência (ruído aleatório).

Padrão da indústria: 95% de confiança
Significa: 95% de chance de que B seja realmente melhor que A
           5% de chance de ser coincidência
```

### Calculadora Simples

```
Para estimar tamanho de amostra:

Fórmula simplificada:
n = 16 × (baseline × (1-baseline)) / (mde²)

Onde:
- n = tamanho da amostra por variante
- baseline = taxa de conversão atual (decimal)
- mde = mínima diferença detectável (decimal)

EXEMPLO:
- Taxa de conversão atual: 3% (0.03)
- Queremos detectar melhoria de 20% (0.006 de diferença)
- n = 16 × (0.03 × 0.97) / (0.006²)
- n = 16 × 0.0291 / 0.000036
- n ≈ 12.933

Precisamos de ~13.000 visitantes POR variante
Total: ~26.000 visitantes para o teste completo
```

### Ferramentas de Cálculo

| Ferramenta | URL | Uso |
|------------|-----|-----|
| Optimizely Calculator | optimizely.com/sample-size-calculator | Tamanho de amostra |
| AB Test Calculator | abtestguide.com/calc | Significância |
| VWO Calculator | vwo.com/tools/ab-test-significance-calculator | Significância |

## 8.5 Erros Comuns em Testes

### Erros Fatais

```
❌ ERRO 1: PARAR O TESTE CEDO DEMAIS
Problema: Ver resultado "positivo" e parar antes de atingir significância
Resultado: Falsos positivos, decisões erradas

CORRETO: Definir tamanho de amostra ANTES e esperar atingir

---

❌ ERRO 2: TESTAR MUITAS VARIÁVEIS
Problema: Mudar título, imagem e CTA ao mesmo tempo
Resultado: Não saber o que causou a diferença

CORRETO: Testar UMA variável por vez

---

❌ ERRO 3: IGNORAR SAZONALIDADE
Problema: Comparar teste de segunda com controle de sábado
Resultado: Diferenças causadas pelo dia, não pela variação

CORRETO: Rodar A e B simultaneamente

---

❌ ERRO 4: AMOSTRA MUITO PEQUENA
Problema: Declarar vencedor com 100 views
Resultado: Resultados não confiáveis

CORRETO: Calcular tamanho de amostra necessário

---

❌ ERRO 5: MUDAR O TESTE NO MEIO
Problema: Ajustar a variante durante o teste
Resultado: Dados contaminados

CORRETO: Se precisar mudar, reiniciar o teste
```

---

# PARTE IX: MÉTRICAS FINANCEIRAS

## 9.1 ROI (Return on Investment)

### Fórmula Básica

```
ROI = ((Receita - Investimento) / Investimento) × 100

EXEMPLO:
- Investimento: R$ 10.000 (ads + produção + ferramentas)
- Receita gerada: R$ 35.000
- ROI = ((35.000 - 10.000) / 10.000) × 100
- ROI = 250%

INTERPRETAÇÃO:
- ROI > 0%: Lucro
- ROI = 0%: Empate
- ROI < 0%: Prejuízo
```

### ROI por Canal

```markdown
## Template de Análise de ROI por Canal

| Canal | Investimento | Receita | ROI | Observação |
|-------|--------------|---------|-----|------------|
| Meta Ads | R$ 5.000 | R$ 18.000 | 260% | Principal canal |
| Google Ads | R$ 3.000 | R$ 8.000 | 167% | Marca + search |
| Email | R$ 500 | R$ 12.000 | 2.300% | Lista própria |
| Orgânico | R$ 2.000 | R$ 15.000 | 650% | Tempo + tools |
| **TOTAL** | **R$ 10.500** | **R$ 53.000** | **405%** | |
```

## 9.2 ROAS (Return on Ad Spend)

### Fórmula

```
ROAS = Receita de Ads / Investimento em Ads

EXEMPLO:
- Investimento em Meta Ads: R$ 5.000
- Receita atribuída: R$ 15.000
- ROAS = 15.000 / 5.000 = 3x (ou 300%)

INTERPRETAÇÃO:
Para cada R$ 1 investido, retornou R$ 3
```

### Benchmarks de ROAS

| ROAS | Avaliação | Ação |
|------|-----------|------|
| < 1x | Prejuízo | Pausar e revisar |
| 1-2x | Break-even | Otimizar |
| 2-3x | Bom | Manter e escalar com cautela |
| 3-5x | Muito bom | Escalar |
| > 5x | Excelente | Escalar agressivamente |

### ROAS por Produto/Oferta

```markdown
| Produto | Spend | Receita | ROAS | Decisão |
|---------|-------|---------|------|---------|
| Curso A | R$ 3.000 | R$ 12.000 | 4x | Escalar |
| Curso B | R$ 2.000 | R$ 3.000 | 1.5x | Otimizar |
| E-book | R$ 1.000 | R$ 500 | 0.5x | Pausar |
| Mentoria | R$ 1.000 | R$ 8.000 | 8x | Escalar muito |
```

## 9.3 CAC (Customer Acquisition Cost)

### Fórmula Completa

```
CAC = (Marketing + Vendas + Overhead) / Novos Clientes

COMPONENTES:
├── Marketing
│   ├── Ads (Meta, Google, etc.)
│   ├── Ferramentas (email, automação)
│   ├── Produção de conteúdo
│   └── Influenciadores/parcerias
├── Vendas
│   ├── Salários do time comercial
│   ├── Comissões
│   └── Ferramentas de vendas (CRM)
└── Overhead proporcional
    ├── % do tempo dedicado a aquisição
    └── Infraestrutura relacionada

EXEMPLO:
- Marketing: R$ 15.000/mês
- Vendas: R$ 5.000/mês
- Novos clientes: 100/mês
- CAC = (15.000 + 5.000) / 100 = R$ 200
```

### CAC por Canal

```markdown
| Canal | Investimento | Clientes | CAC | Qualidade |
|-------|--------------|----------|-----|-----------|
| Meta | R$ 8.000 | 35 | R$ 229 | Alta |
| Google | R$ 4.000 | 20 | R$ 200 | Muito alta |
| Orgânico | R$ 3.000 | 30 | R$ 100 | Alta |
| Indicação | R$ 0 | 15 | R$ 0 | Muito alta |
| **Total** | **R$ 15.000** | **100** | **R$ 150** | |
```

## 9.4 LTV (Customer Lifetime Value)

### Fórmulas

```
LTV SIMPLES:
LTV = Ticket Médio × Frequência × Tempo de Vida

EXEMPLO:
- Ticket médio: R$ 500
- Compras por ano: 2
- Tempo médio de cliente: 3 anos
- LTV = 500 × 2 × 3 = R$ 3.000

---

LTV COM MARGEM:
LTV = (Ticket Médio × Margem) × Frequência × Tempo de Vida

EXEMPLO:
- Ticket médio: R$ 500
- Margem: 60%
- Compras por ano: 2
- Tempo médio: 3 anos
- LTV = (500 × 0.6) × 2 × 3 = R$ 1.800

---

LTV POR COORTE:
Soma da receita de uma coorte / Número de clientes na coorte

EXEMPLO:
- Clientes de Jan/24: 100
- Receita total até hoje: R$ 180.000
- LTV = 180.000 / 100 = R$ 1.800
```

### Estratégias para Aumentar LTV

| Estratégia | Como Implementar | Impacto no LTV |
|------------|------------------|----------------|
| **Upsell** | Oferecer versão premium | Aumenta ticket |
| **Cross-sell** | Produtos complementares | Aumenta frequência |
| **Retenção** | Programa de fidelidade | Aumenta tempo |
| **Comunidade** | Grupo exclusivo | Aumenta tudo |
| **Suporte** | Atendimento excelente | Aumenta tempo |

## 9.5 Relação CAC/LTV

### A Métrica Mais Importante

```
REGRA DE OURO:
LTV deve ser pelo menos 3x o CAC

LTV / CAC = Health Score do negócio

INTERPRETAÇÃO:
├── 1:1 → Prejuízo (custo = receita, sem margem)
├── 1:2 → Sustentável, mas apertado
├── 1:3 → Saudável (benchmark ideal)
├── 1:4 → Muito saudável (pode investir mais)
└── 1:5+ → Excelente (escalar agressivamente)
```

### Payback Period

```
Payback = CAC / (LTV mensal × Margem)

EXEMPLO:
- CAC: R$ 300
- LTV mensal: R$ 100 (assinatura)
- Margem: 70%
- Payback = 300 / (100 × 0.7) = 4.3 meses

INTERPRETAÇÃO:
< 6 meses: Excelente
6-12 meses: Bom
12-18 meses: Aceitável
> 18 meses: Preocupante
```

## 9.6 Break-Even Analysis

### Fórmula

```
Break-Even = Custos Fixos / (Preço - Custo Variável)

EXEMPLO CAMPANHA:
- Custo da campanha: R$ 5.000
- Preço do produto: R$ 297
- Custo do produto: R$ 50
- Margem unitária: R$ 247
- Break-even = 5.000 / 247 = 20.24 vendas

Preciso vender 21 unidades para cobrir o investimento
```

### Break-Even Mensal

```
EXEMPLO INFOPRODUTO:
- Custos fixos mensais: R$ 10.000
  (ferramentas, equipe, infraestrutura)
- Preço do curso: R$ 997
- Custo variável: R$ 100 (afiliados, gateway)
- Margem: R$ 897

Break-even mensal = 10.000 / 897 = 11.15 vendas

Preciso vender 12 cursos/mês para empatar
```

## 9.7 Unit Economics

### Dashboard de Unit Economics

```
┌─────────────────────────────────────────────────────────────┐
│                    UNIT ECONOMICS                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  RECEITA POR CLIENTE                                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Ticket médio:      R$ 497                           │   │
│  │ Compras/cliente:   1.8x                             │   │
│  │ LTV:               R$ 894                           │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  CUSTO POR CLIENTE                                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ CAC:               R$ 150                           │   │
│  │ COGS:              R$ 50                            │   │
│  │ Custo total:       R$ 200                           │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  MARGENS                                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Margem bruta:      89% (LTV - COGS)                 │   │
│  │ Margem líquida:    77% (LTV - Custo total)          │   │
│  │ LTV/CAC:           5.96x                            │   │
│  │ Payback:           2 meses                          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  SAÚDE: 🟢 EXCELENTE                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

# PARTE X: DATA VISUALIZATION

## 10.1 Princípios de Visualização

### Escolhendo o Gráfico Certo

| Objetivo | Tipo de Gráfico | Quando Usar |
|----------|-----------------|-------------|
| Comparar valores | Barras | Comparar categorias |
| Mostrar tendência | Linha | Evolução temporal |
| Mostrar proporção | Pizza/Donut | Partes de um todo (<7 categorias) |
| Mostrar distribuição | Histograma | Frequência de valores |
| Correlação | Scatter | Relação entre 2 variáveis |
| Funil | Funil | Etapas de conversão |
| Hierarquia | Treemap | Proporções aninhadas |
| Geográfico | Mapa | Dados por localização |

### Regras de Ouro

```
1. MENOS É MAIS
   - Remover elementos desnecessários (chart junk)
   - Foco na mensagem principal
   - Usar cores com propósito

2. CONTEXTO É ESSENCIAL
   - Sempre mostrar período de tempo
   - Incluir comparação (vs meta, vs anterior)
   - Explicar o que é "bom" ou "ruim"

3. ACESSIBILIDADE
   - Não depender só de cor
   - Usar rótulos claros
   - Fonte legível

4. HONESTIDADE
   - Eixo Y começando do zero (para barras)
   - Escala consistente
   - Não manipular para enganar
```

## 10.2 Storytelling com Dados

### Estrutura de Narrativa

```
1. CONTEXTO
   "No mês passado, investimos R$ 10.000 em ads"

2. CONFLITO/PROBLEMA
   "Porém, o ROAS caiu 30% comparado ao mês anterior"

3. DESCOBERTA
   "Ao analisar os dados, descobrimos que..."

4. INSIGHT
   "Criativos com vídeo têm 3x mais conversão que imagem"

5. AÇÃO
   "Realocamos 70% do budget para vídeo"

6. RESULTADO
   "ROAS subiu para 4.2x, 40% acima da meta"
```

### Template de Slide de Dados

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  TÍTULO: [Insight principal em uma frase]                   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│              [VISUALIZAÇÃO PRINCIPAL]                       │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                     │   │
│  │           Gráfico grande e claro                    │   │
│  │                                                     │   │
│  │           Com destaque no ponto                     │   │
│  │           mais importante                           │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  TAKEAWAY: [O que isso significa + Ação recomendada]        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 10.3 Ferramentas de Visualização

### Comparativo

| Ferramenta | Custo | Curva de Aprendizado | Melhor Para |
|------------|-------|----------------------|-------------|
| **Google Sheets/Excel** | Grátis | Baixa | Análises rápidas |
| **Google Data Studio** | Grátis | Média | Dashboards conectados |
| **Looker Studio** | Grátis | Média | Dashboards avançados |
| **Notion** | Freemium | Baixa | Relatórios simples |
| **Tableau** | Pago | Alta | Análises complexas |
| **Power BI** | Pago | Alta | Grandes volumes |
| **Metabase** | Grátis/Pago | Média | SQL + visualização |

### Templates Prontos

**Para Google Sheets:**
- Social media tracker template
- Campaign dashboard template
- KPI dashboard template

**Para Looker Studio:**
- GA4 starter template
- Social media performance template
- Marketing KPI template

---

# PARTE XI: FORECASTING E PREVISÕES

## 11.1 Tipos de Forecast

### Métodos de Previsão

| Método | Complexidade | Quando Usar |
|--------|--------------|-------------|
| **Média móvel** | Baixa | Dados estáveis, sem tendência clara |
| **Tendência linear** | Baixa | Crescimento/queda constante |
| **Sazonalidade** | Média | Padrões que se repetem |
| **Regressão** | Média | Múltiplas variáveis influenciam |
| **Machine Learning** | Alta | Grande volume de dados históricos |

## 11.2 Forecast Simples

### Média Móvel

```
Forecast = Média dos últimos N períodos

EXEMPLO (Média Móvel de 3 meses para vendas):
- Janeiro: 100
- Fevereiro: 120
- Março: 110

Forecast Abril = (100 + 120 + 110) / 3 = 110 vendas
```

### Tendência Linear

```
Se os últimos 6 meses mostram:
Jan: 100 → Fev: 110 → Mar: 120 → Abr: 130 → Mai: 140 → Jun: 150

Crescimento médio: 10/mês

Forecast Julho = 150 + 10 = 160
Forecast Agosto = 160 + 10 = 170
```

### Com Sazonalidade

```
PASSO 1: Calcular índice sazonal
(Comparar cada mês com a média anual)

Exemplo: Dezembro vende 40% acima da média
Índice de Dezembro = 1.40

PASSO 2: Aplicar tendência base
Forecast base = Tendência normal

PASSO 3: Ajustar pela sazonalidade
Forecast final = Forecast base × Índice sazonal

EXEMPLO:
- Forecast base Dezembro: 100 vendas
- Índice Dezembro: 1.40
- Forecast ajustado: 100 × 1.40 = 140 vendas
```

## 11.3 Template de Forecast

```markdown
# FORECAST - [MÊS/TRIMESTRE/ANO]

## Premissas

### Dados Históricos Utilizados
- Período base: [X meses/anos]
- Tendência identificada: [+X% mensal]
- Sazonalidade: [Sim/Não - padrão]

### Fatores Considerados
- [Fator 1: ex. lançamento de produto]
- [Fator 2: ex. sazonalidade de mercado]
- [Fator 3: ex. aumento de investimento]

---

## Projeções

### Cenário Base (mais provável)
| Métrica | [Mês 1] | [Mês 2] | [Mês 3] | Total |
|---------|---------|---------|---------|-------|
| Leads | [X] | [X] | [X] | [Total] |
| Vendas | [X] | [X] | [X] | [Total] |
| Receita | R$ [X] | R$ [X] | R$ [X] | R$ [Total] |

### Cenário Otimista (+20%)
| Métrica | [Mês 1] | [Mês 2] | [Mês 3] | Total |
|---------|---------|---------|---------|-------|
| Leads | [X] | [X] | [X] | [Total] |
| Vendas | [X] | [X] | [X] | [Total] |
| Receita | R$ [X] | R$ [X] | R$ [X] | R$ [Total] |

### Cenário Pessimista (-20%)
| Métrica | [Mês 1] | [Mês 2] | [Mês 3] | Total |
|---------|---------|---------|---------|-------|
| Leads | [X] | [X] | [X] | [Total] |
| Vendas | [X] | [X] | [X] | [Total] |
| Receita | R$ [X] | R$ [X] | R$ [X] | R$ [Total] |

---

## Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| [Risco 1] | Alta/Média/Baixa | [X%] | [Ação] |
| [Risco 2] | Alta/Média/Baixa | [X%] | [Ação] |

---

## Acompanhamento

Checkpoints:
- [ ] Semana 1: Verificar [X]
- [ ] Semana 2: Verificar [Y]
- [ ] Semana 3: Verificar [Z]
- [ ] Semana 4: Revisão completa
```

---

# PARTE XII: ANALYTICS PARA E-COMMERCE

## 12.1 Métricas Essenciais

### Funil de E-commerce

```
VISITANTES → PRODUTO → CARRINHO → CHECKOUT → COMPRA
   100%    →   40%   →   10%    →    5%    →   2%

MÉTRICAS POR ETAPA:
├── Sessions: Total de visitas
├── Product views: Visualizações de produto
├── Add to cart rate: % que adiciona ao carrinho
├── Cart abandonment: % que abandona carrinho
├── Checkout abandonment: % que abandona checkout
└── Conversion rate: % que compra
```

### KPIs Principais

| KPI | Fórmula | Benchmark |
|-----|---------|-----------|
| **Conversion Rate** | Compras / Sessões | 1-3% |
| **AOV (Ticket Médio)** | Receita / Pedidos | Varia |
| **Revenue per Visit** | Receita / Sessões | AOV × Conv. Rate |
| **Cart Abandonment** | Abandonos / Adds to Cart | 60-80% |
| **Checkout Abandonment** | Abandonos / Checkouts iniciados | 20-40% |

## 12.2 Análise de Carrinho Abandonado

### Motivos Comuns

```
POR QUE ABANDONAM O CARRINHO:

1. Frete alto (55% dos casos)
   ├── Solução: Frete grátis acima de X
   └── Solução: Mostrar frete na página do produto

2. Apenas pesquisando (34%)
   ├── Solução: Remarketing
   └── Solução: Email de abandono

3. Processo complexo (26%)
   ├── Solução: Checkout simplificado
   └── Solução: Guest checkout

4. Falta de opções de pagamento (8%)
   ├── Solução: PIX, boleto, cartões
   └── Solução: Parcelamento

5. Preocupação com segurança (17%)
   ├── Solução: Selos de segurança
   └── Solução: Depoimentos
```

### Estratégia de Recuperação

```
EMAIL 1 (1 hora após abandono):
- Assunto: "Esqueceu algo?"
- Conteúdo: Lembrete + foto do produto
- CTA: "Finalizar compra"

EMAIL 2 (24 horas após):
- Assunto: "Últimas unidades!"
- Conteúdo: Urgência/escassez
- CTA: "Garantir o meu"

EMAIL 3 (48-72 horas após):
- Assunto: "10% OFF só pra você"
- Conteúdo: Desconto exclusivo
- CTA: "Usar meu cupom"
```

## 12.3 Cohort Analysis

### O que é

```
COHORT = Grupo de clientes que fizeram primeira compra
          no mesmo período

ANÁLISE = Acompanhar comportamento desse grupo ao longo do tempo

EXEMPLO:
Coorte Janeiro/24: 100 clientes compraram pela primeira vez

Mês 1: 100 (100%)
Mês 2: 25 voltaram (25%)
Mês 3: 18 voltaram (18%)
Mês 4: 15 voltaram (15%)
...

Insight: Retenção após 3 meses estabiliza em ~15%
```

### Template de Análise

```markdown
## COHORT ANALYSIS - [PERÍODO]

### Retenção por Coorte
| Coorte | M0 | M1 | M2 | M3 | M6 | M12 |
|--------|----|----|----|----|----|----|
| Jan/24 | 100% | 28% | 20% | 18% | 15% | 12% |
| Fev/24 | 100% | 25% | 18% | 16% | 14% | - |
| Mar/24 | 100% | 30% | 22% | 19% | - | - |
| Abr/24 | 100% | 27% | 21% | - | - | - |

### Receita por Coorte (Acumulada)
| Coorte | Clientes | M0 | M6 | M12 | LTV |
|--------|----------|----|----|-----|-----|
| Jan/24 | 100 | R$ 30.000 | R$ 45.000 | R$ 55.000 | R$ 550 |
| Fev/24 | 85 | R$ 25.000 | R$ 38.000 | - | Est. R$ 530 |

### Insights
1. [Insight sobre retenção]
2. [Insight sobre LTV]
3. [Oportunidade identificada]
```

## 12.4 RFM Analysis

### O que é RFM

```
R - RECENCY (Recência)
    Quanto tempo desde a última compra?

F - FREQUENCY (Frequência)
    Quantas vezes comprou?

M - MONETARY (Monetário)
    Quanto gastou no total?

COMBINANDO OS 3:
Cada cliente recebe nota 1-5 em cada dimensão
Resultando em segmentos como: 555, 111, 531, etc.
```

### Segmentos RFM

| Segmento | RFM Score | Ação |
|----------|-----------|------|
| **Champions** | 555, 554, 545 | Recompensar, pedir indicação |
| **Loyal** | 444, 443, 434 | Upsell, programa de fidelidade |
| **Potential** | 534, 533, 524 | Aumentar frequência |
| **New** | 511, 512, 521 | Onboarding, segunda compra |
| **At Risk** | 244, 233, 143 | Reativar com oferta |
| **Hibernating** | 111, 112, 121 | Win-back campaign |
| **Lost** | 111 (muito tempo) | Aceitar perda ou grande oferta |

---

# PARTE XIII: AUTOMATIZAÇÃO E ALERTAS

## 13.1 O que Automatizar

### Automações Essenciais

| Automação | Ferramenta | Frequência |
|-----------|------------|------------|
| Coleta de métricas | Zapier/Make | Diária |
| Relatório semanal | Looker Studio | Semanal |
| Alerta de anomalia | Custom script | Real-time |
| Backup de dados | Sheets/BigQuery | Diária |
| Email de performance | Make/Zapier | Semanal |

## 13.2 Sistema de Alertas

### Tipos de Alertas

```
ALERTA CRÍTICO (Vermelho):
├── ROAS < 1x por 3 dias
├── Taxa de conversão < 50% do normal
├── Custo por lead > 2x do target
└── Bounce rate de email > 10%

ALERTA DE ATENÇÃO (Amarelo):
├── Métricas 20% abaixo do normal
├── CTR caindo por 5 dias consecutivos
├── Frequência de ads > 4
└── Unsubscribe rate aumentando

ALERTA POSITIVO (Verde):
├── Recorde de conversões
├── Viral content (10x normal reach)
├── ROAS > 5x
└── Campanha performando 50% acima da meta
```

### Template de Configuração

```markdown
## ALERTA: [NOME]

### Condição
[Quando disparar - ex: "ROAS < 1.5 por 2 dias consecutivos"]

### Canais de Notificação
- [ ] Email para: [endereços]
- [ ] Slack #channel
- [ ] SMS (se crítico)

### Ação Automática (se aplicável)
[Ex: Pausar campanha automaticamente]

### Responsável por Ação
[Nome/Cargo]

### SLA de Resposta
- Crítico: 1 hora
- Atenção: 24 horas
- Positivo: Próximo ciclo de report
```

## 13.3 Ferramentas de Automação

### Comparativo

| Ferramenta | Custo | Melhor Para |
|------------|-------|-------------|
| **Zapier** | $19+/mês | Integrações simples |
| **Make (Integromat)** | $9+/mês | Fluxos complexos |
| **n8n** | Open source | Self-hosted |
| **Google Apps Script** | Grátis | Google ecosystem |
| **Python + Cron** | Grátis | Custom scripts |

### Automações Recomendadas

```
1. COLETA DIÁRIA DE MÉTRICAS
   Trigger: Todo dia às 8h
   Ação: Puxar dados de GA4, Meta, YouTube
   Destino: Google Sheets master

2. RELATÓRIO SEMANAL AUTOMÁTICO
   Trigger: Segunda às 9h
   Ação: Compilar dados da semana
   Destino: Email para stakeholders

3. ALERTA DE ANOMALIA
   Trigger: Métrica fora do padrão
   Ação: Notificar via Slack
   Destino: #analytics-alerts

4. BACKUP DE CONFIGURAÇÕES
   Trigger: Diário às 2h
   Ação: Exportar configs de campanhas
   Destino: Google Drive
```

---

# APÊNDICE: GLOSSÁRIO E TEMPLATES

## A.1 Glossário de Métricas

### Métricas Gerais

| Termo | Definição |
|-------|-----------|
| **Alcance (Reach)** | Número de pessoas únicas que viram o conteúdo |
| **Impressões** | Número total de vezes que o conteúdo foi exibido |
| **Engajamento** | Interações totais (likes, comments, shares, saves) |
| **Taxa de Engajamento** | Engajamento / Alcance (ou Seguidores) × 100 |
| **CTR (Click-Through Rate)** | Cliques / Impressões × 100 |
| **CPC (Cost Per Click)** | Custo total / Cliques |
| **CPM (Cost Per Mille)** | Custo total / (Impressões / 1000) |
| **CPL (Cost Per Lead)** | Custo total / Leads gerados |
| **CPA (Cost Per Acquisition)** | Custo total / Conversões |
| **ROAS (Return on Ad Spend)** | Receita de ads / Investimento em ads |
| **ROI (Return on Investment)** | (Receita - Investimento) / Investimento × 100 |
| **CAC (Customer Acquisition Cost)** | Custo total de aquisição / Novos clientes |
| **LTV (Lifetime Value)** | Valor total que um cliente gera ao longo da vida |
| **Churn Rate** | Clientes perdidos / Clientes no início do período |
| **NPS (Net Promoter Score)** | % Promotores - % Detratores |

### Métricas de Vídeo

| Termo | Definição |
|-------|-----------|
| **Watch Time** | Tempo total de visualização |
| **AVD (Average View Duration)** | Tempo médio de visualização |
| **Retention Rate** | % do vídeo assistido em média |
| **Completion Rate** | % de viewers que assistiram até o final |
| **VTR (View-Through Rate)** | Visualizações completas / Impressões |

### Métricas de Email

| Termo | Definição |
|-------|-----------|
| **Open Rate** | Aberturas / Emails entregues × 100 |
| **Click Rate (CTR)** | Cliques / Emails entregues × 100 |
| **CTOR (Click-to-Open Rate)** | Cliques / Aberturas × 100 |
| **Bounce Rate** | Emails não entregues / Emails enviados × 100 |
| **Unsubscribe Rate** | Descadastros / Emails entregues × 100 |
| **Spam Rate** | Marcações de spam / Emails entregues × 100 |

## A.2 Checklist de Analytics

### Setup Inicial

```markdown
## CHECKLIST - CONFIGURAÇÃO DE ANALYTICS

### Google Analytics 4
- [ ] Propriedade GA4 criada
- [ ] Tag instalada corretamente
- [ ] Enhanced measurement ativado
- [ ] Eventos de conversão configurados
- [ ] Públicos criados
- [ ] Link com Google Ads ativo
- [ ] BigQuery export configurado (opcional)

### Meta Pixel
- [ ] Pixel instalado
- [ ] Eventos standard configurados
- [ ] Conversions API configurado
- [ ] Eventos de conversão definidos
- [ ] Públicos de remarketing criados

### Tracking de Campanhas
- [ ] Convenção de UTM definida
- [ ] Documento de UTM compartilhado
- [ ] Links de teste validados

### Dashboards
- [ ] Dashboard principal criado
- [ ] Métricas-chave definidas
- [ ] Acesso compartilhado com equipe
```

### Revisão Mensal

```markdown
## CHECKLIST - REVISÃO MENSAL DE ANALYTICS

### Dados
- [ ] Dados sendo coletados corretamente
- [ ] Sem gaps ou anomalias inexplicadas
- [ ] Filtros de spam/bot funcionando

### Metas
- [ ] KPIs atualizados
- [ ] Metas do mês definidas
- [ ] Comparativo com mês anterior analisado

### Relatórios
- [ ] Relatório mensal gerado
- [ ] Insights documentados
- [ ] Ações do próximo mês definidas

### Otimizações
- [ ] Testes A/B revisados
- [ ] Aprendizados documentados
- [ ] Próximos testes planejados
```

## A.3 Fórmulas Rápidas

```
=== MÉTRICAS DE MARKETING ===

Taxa de Engajamento = (Engajamentos / Alcance) × 100
CTR = (Cliques / Impressões) × 100
CPC = Custo Total / Cliques
CPM = (Custo Total / Impressões) × 1000
CPL = Custo Total / Leads
CPA = Custo Total / Conversões
ROAS = Receita / Investimento em Ads
ROI = ((Receita - Custo) / Custo) × 100

=== MÉTRICAS DE NEGÓCIO ===

CAC = (Marketing + Vendas) / Novos Clientes
LTV = Ticket Médio × Frequência × Tempo de Vida
LTV/CAC = LTV / CAC (meta: ≥ 3)
Payback = CAC / (Receita Mensal × Margem)
Churn = Clientes Perdidos / Clientes Início
MRR = Clientes × Ticket Mensal
ARR = MRR × 12

=== MÉTRICAS DE EMAIL ===

Open Rate = Aberturas / Entregues × 100
CTR = Cliques / Entregues × 100
CTOR = Cliques / Aberturas × 100
Bounce Rate = Não Entregues / Enviados × 100

=== MÉTRICAS DE E-COMMERCE ===

Conversion Rate = Compras / Sessões × 100
AOV = Receita / Pedidos
Revenue per Visit = Receita / Sessões
Cart Abandonment = Abandonos / Adds × 100
```

## A.4 Benchmarks por Nicho

### Taxas de Engajamento Instagram

| Nicho | Benchmark |
|-------|-----------|
| Moda/Beleza | 1.5-3% |
| Fitness | 2-4% |
| Comida | 2-5% |
| Viagem | 3-6% |
| Tech/Negócios | 1-2.5% |
| Educação | 2-4% |
| Pets | 3-6% |
| Lifestyle | 2-4% |

### CPL por Nicho (Meta Ads Brasil)

| Nicho | CPL Médio |
|-------|-----------|
| E-commerce (geral) | R$ 5-15 |
| Infoprodutos (low ticket) | R$ 3-10 |
| Infoprodutos (high ticket) | R$ 30-100 |
| B2B/Serviços | R$ 50-200 |
| Imobiliário | R$ 80-300 |
| Educação | R$ 10-40 |
| Saúde/Estética | R$ 15-50 |

### Taxa de Conversão de Landing Page

| Tipo | Benchmark |
|------|-----------|
| Lead magnet gratuito | 20-50% |
| Webinar registro | 15-35% |
| Produto low ticket (<R$ 100) | 2-5% |
| Produto mid ticket (R$ 100-500) | 1-3% |
| Produto high ticket (>R$ 500) | 0.5-2% |
| E-commerce (geral) | 1-3% |

---

## A.5 Templates de Planilha

### Template de Tracker de Métricas Diárias

```
| Data | Plataforma | Alcance | Engaj. | Seguidores | Leads | Vendas | Notas |
|------|------------|---------|--------|------------|-------|--------|-------|
| DD/MM | Instagram | [X] | [Y%] | [+Z] | [N] | [V] | [Obs] |
| DD/MM | YouTube | [X] | [Y%] | [+Z] | [N] | [V] | [Obs] |
| DD/MM | TikTok | [X] | [Y%] | [+Z] | [N] | [V] | [Obs] |
| DD/MM | LinkedIn | [X] | [Y%] | [+Z] | [N] | [V] | [Obs] |
| DD/MM | Email | [X] | [Y%] | [+Z] | [N] | [V] | [Obs] |
```

### Template de Comparativo Semanal

```
| Métrica | S1 | S2 | S3 | S4 | Média | Tendência |
|---------|----|----|----|----|-------|-----------|
| Alcance total | [X] | [X] | [X] | [X] | [Avg] | [↑/↓/→] |
| Engajamento | [X%] | [X%] | [X%] | [X%] | [Avg] | [↑/↓/→] |
| Novos seguidores | [X] | [X] | [X] | [X] | [Avg] | [↑/↓/→] |
| Leads | [X] | [X] | [X] | [X] | [Avg] | [↑/↓/→] |
| Vendas | [X] | [X] | [X] | [X] | [Avg] | [↑/↓/→] |
| Receita | R$[X] | R$[X] | R$[X] | R$[X] | R$[Avg] | [↑/↓/→] |
```

### Template de Análise de Conteúdo

```
| Post ID | Data | Plataforma | Formato | Tema | Alcance | Eng. | Saves | Shares | Score |
|---------|------|------------|---------|------|---------|------|-------|--------|-------|
| P001 | DD/MM | IG | Carrossel | [Tema] | [X] | [Y%] | [Z] | [W] | [1-10] |
| P002 | DD/MM | IG | Reels | [Tema] | [X] | [Y%] | [Z] | [W] | [1-10] |
| P003 | DD/MM | YT | Vídeo | [Tema] | [X] | [Y%] | [Z] | [W] | [1-10] |
```

## A.6 Recursos e Ferramentas

### Ferramentas Gratuitas

| Categoria | Ferramenta | Uso |
|-----------|------------|-----|
| **Analytics** | Google Analytics 4 | Web analytics |
| **Analytics** | Google Search Console | SEO analytics |
| **Dashboards** | Looker Studio | Visualização |
| **Automação** | Google Sheets + Scripts | Coleta automática |
| **UTM** | Google Campaign URL Builder | Criar UTMs |
| **Heatmaps** | Microsoft Clarity | Comportamento |
| **Speed** | PageSpeed Insights | Performance |
| **Social** | Native analytics (IG, TT, etc.) | Métricas sociais |

### Ferramentas Pagas

| Categoria | Ferramenta | Custo | Uso |
|-----------|------------|-------|-----|
| **All-in-one** | Metricool | $15+/mês | Social + Ads |
| **All-in-one** | Sprout Social | $99+/mês | Enterprise |
| **SEO** | Semrush | $119+/mês | SEO completo |
| **SEO** | Ahrefs | $99+/mês | Backlinks + SEO |
| **Email** | ActiveCampaign | $29+/mês | Email analytics |
| **Heatmap** | Hotjar | $32+/mês | UX analytics |
| **BI** | Tableau | $70+/mês | BI avançado |

### APIs Úteis

| API | Dados Disponíveis | Uso |
|-----|-------------------|-----|
| Instagram Graph API | Métricas de posts, stories, reels | Automação |
| YouTube Data API | Views, likes, comments, watch time | Relatórios |
| Meta Marketing API | Dados de Ads Manager | Dashboards |
| Google Analytics API | Todos os dados GA4 | Integração |
| TikTok API | Métricas de vídeos | Automação |

## A.7 Erros Comuns em Analytics

### Erros de Coleta

```
❌ ERRO 1: Não verificar se o tracking está funcionando
   SOLUÇÃO: Testar com GA4 DebugView antes de lançar

❌ ERRO 2: Ignorar filtros de spam/bot
   SOLUÇÃO: Configurar filtros no GA4

❌ ERRO 3: UTMs inconsistentes
   SOLUÇÃO: Documentar convenção e usar template

❌ ERRO 4: Não rastrear eventos importantes
   SOLUÇÃO: Mapear todos os eventos de conversão

❌ ERRO 5: Confiar em uma única fonte de dados
   SOLUÇÃO: Cruzar dados de múltiplas fontes
```

### Erros de Análise

```
❌ ERRO 1: Confundir correlação com causalidade
   SOLUÇÃO: Fazer testes A/B para validar

❌ ERRO 2: Ignorar contexto e sazonalidade
   SOLUÇÃO: Comparar com mesmo período do ano anterior

❌ ERRO 3: Olhar apenas para métricas de vaidade
   SOLUÇÃO: Focar em métricas de resultado

❌ ERRO 4: Não segmentar os dados
   SOLUÇÃO: Analisar por dispositivo, canal, público

❌ ERRO 5: Tirar conclusões com amostra pequena
   SOLUÇÃO: Esperar significância estatística
```

### Erros de Reporting

```
❌ ERRO 1: Relatórios longos demais sem insight
   SOLUÇÃO: Liderar com insights, detalhar depois

❌ ERRO 2: Não contextualizar os números
   SOLUÇÃO: Sempre comparar com meta e período anterior

❌ ERRO 3: Apresentar dados sem recomendação
   SOLUÇÃO: Todo insight deve ter ação associada

❌ ERRO 4: Usar visualizações erradas
   SOLUÇÃO: Escolher gráfico adequado ao dado

❌ ERRO 5: Não adaptar ao público
   SOLUÇÃO: Executivo quer resumo, analista quer detalhe
```

## A.8 Calendário de Analytics

### Rotina Diária (10 min)

```markdown
- [ ] Verificar métricas principais (dashboard)
- [ ] Checar alertas de anomalias
- [ ] Anotar destaques/problemas
```

### Rotina Semanal (1 hora)

```markdown
- [ ] Compilar relatório semanal
- [ ] Analisar top performers
- [ ] Identificar padrões
- [ ] Revisar testes A/B em andamento
- [ ] Planejar conteúdo baseado em dados
```

### Rotina Mensal (2-3 horas)

```markdown
- [ ] Relatório mensal completo
- [ ] Análise de KPIs vs metas
- [ ] Análise de audiência/demografia
- [ ] Revisão de CAC, LTV, ROAS
- [ ] Planejamento do próximo mês
- [ ] Definir testes A/B
```

### Rotina Trimestral (4-6 horas)

```markdown
- [ ] Análise de tendências de longo prazo
- [ ] Revisão de estratégia
- [ ] Benchmarking com mercado
- [ ] Atualização de metas anuais
- [ ] Auditoria de tracking
- [ ] Revisão de ferramentas
```

## A.9 Melhores Práticas Finais

### Os 10 Mandamentos do Analytics

```
1. MEDIR PRIMEIRO, OTIMIZAR DEPOIS
   Não tome decisões sem dados.

2. MENOS É MAIS
   Foque nas métricas que importam.

3. CONTEXTO É REI
   Números sem contexto são ruído.

4. TENDÊNCIA > SNAPSHOT
   Olhe para a direção, não só o momento.

5. AÇÃO > INFORMAÇÃO
   Todo insight deve gerar ação.

6. TESTE SEMPRE
   Hipóteses precisam de validação.

7. DOCUMENTE TUDO
   Memória institucional é poder.

8. AUTOMATIZE O REPETITIVO
   Humanos para análise, máquinas para coleta.

9. QUESTIONE OS DADOS
   Dados também podem estar errados.

10. COMUNIQUE COM CLAREZA
    O melhor insight é inútil se ninguém entender.
```

---

## Integração com Marketing OS

O Analytics Agent fornece para os outros subagentes:

1. **Métricas atualizadas** por plataforma e formato
2. **Relatórios estruturados** para decisões
3. **Framework de testes A/B** para otimização
4. **Análise de padrões** para replicar sucesso
5. **Insights financeiros** (ROI, ROAS, CAC, LTV)
6. **Dashboards** para monitoramento contínuo
7. **Forecasting** para planejamento
8. **Alertas** para ação rápida

---

*Analytics Agent v3.0 - Especialista em Métricas e Análise de Dados*
*Marketing OS System*
