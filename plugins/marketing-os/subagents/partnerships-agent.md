# Partnerships Agent: Knowledge Base de Parcerias com Creators

> Tier 2 do `agents/mos-partnerships.md`. Descoberta, fit, outreach e brief de collab. Pesquisa de mercado genérica mora em `subagents/research-agent.md`; este arquivo cobre parceria acionável com creators.

## ÍNDICE

- PARTE I: Fundamentos (parceria vs anúncio em certos estágios)
- PARTE II: Sourcing de creators
- PARTE III: Fit e engajamento real vs inflado
- PARTE IV: Modelos de parceria BR
- PARTE V: Outreach e follow-up
- PARTE VI: Negociação e brief de collab
- PARTE VII: Métricas de parceria
- PARTE VIII: Anti-padrões
- PARTE IX: Referências cruzadas

---

# PARTE I: FUNDAMENTOS

## 1.1 Por que parceria > anúncio em certos estágios

| Estágio da marca | Parceria brilha quando... | Anúncio brilha quando... |
|---|---|---|
| Early / nicho | Creator traz confiança transferida | Precisa escala rápida com criativo testado |
| Lançamento | Buzz orgânico + prova social | Retargeting e conversão direta |
| Produto visual/experiencial | UGC autêntico | Catálogo e DPA |
| High-ticket | Autoridade do creator reduz objeção | Funil longo com múltiplos touchpoints |

Parceria não substitui ads: complementa. Creator traz credibilidade; ads trazem controle de escala e mensuração.

## 1.2 O que define uma boa parceria

- **Fit de audiência**: seguidores do creator ≈ público da marca
- **Fit de valores**: tom e temas alinhados
- **Win-win**: valor real pros dois lados
- **Entregáveis claros**: formato, prazo, direitos, disclosure
- **Mensuração**: link, cupom, UTM ou código rastreável

## 1.3 Princípio do rascunho (nunca send)

Outreach mal calibrado queima ponte com creator. O Marketing OS entrega rascunhos revisáveis (Gmail `create_draft` ou texto pronto). O humano envia porque negocia tom fino e conhece budget real.

---

# PARTE II: SOURCING DE CREATORS

## 2.1 Onde achar creators do nicho

| Canal | Uso | Limitação |
|---|---|---|
| Busca por hashtag do nicho | Descoberta orgânica | Trabalhoso, bom pra micro |
| Explore / FYP do tema | TikTok/Reels trends | Subjetivo |
| Listas de concorrentes | Quem já publiou no setor | Cuidado com exclusividade |
| Plataformas (Squid, Influency, etc.) | Escala, dados | Custo da plataforma |
| Apify (`apify_instagram.py`, `apify_tiktok.py`) | Dados estruturados | Requer APIFY_TOKEN |
| WebSearch | Artigos "top creators [nicho] BR" | Pode estar desatualizado |

## 2.2 Critérios de busca (montar antes da shortlist)

- Nicho e subnicho (ex: skincare → pele sensível, não só "beleza")
- Faixa de seguidores (nano 1-10k, micro 10-100k, mid 100k-500k, macro 500k+)
- ER mínimo aceitável (varia por plataforma; ver PARTE III)
- Região/idioma (PT-BR)
- Exclusões: concorrentes diretos, polêmicas, fake followers

## 2.3 Processo de sourcing em 4 passos

```
1. Definir ICP do creator (espelho do ICP da marca)
2. Coletar 20-30 candidatos (hashtag, Apify, manual)
3. Pré-filtrar por sinais de fit (bio, últimos 9 posts)
4. Aprofundar top 10 com dados de engajamento
```

Handoff do mos-research: quando `/prospectar-creators` roda sequencial, research valida audiência do nicho e concorrentes; partnerships fecha fit + outreach.

---

# PARTE III: FIT E ENGAJAMENTO REAL

## 3.1 Engajamento real vs inflado

| Sinal saudável | Sinal de alerta |
|---|---|
| Comentários variados, perguntas reais | "Nice post" repetido, emojis só |
| ER estável entre posts | Pico só em post patrocinado |
| Seguidores crescem gradualmente | Salto de 50k em uma semana |
| Views proporcionais a seguidores | 500k seguidores, 2k views |
| Audiência do mesmo país/idioma | % alto de perfis sem foto |

## 3.2 ER de referência (orientativo, não absoluto)

| Plataforma | Nano/micro saudável | Mid/macro saudável |
|---|---|---|
| Instagram | 3-8% | 1-3% |
| TikTok | 5-15% | 3-8% |
| YouTube | N/A (usar views/sub) | 2-5% engajamento em vídeo |

Sempre marcar fonte: Apify verificado, cálculo manual ou estimativa.

## 3.3 Fit Score (1-10)

| Dimensão | Peso | Pergunta |
|---|---|---|
| Alinhamento de nicho | 0-3 | O conteúdo do creator fala com meu público? |
| Engajamento autêntico | 0-3 | ER e comentários parecem reais? |
| Qualidade de audiência | 0-2 | Demografia e intenção batem? |
| Risco de marca | 0-2 (invertido) | Histórico polêmico, desalinhamento? |

Documentar justificativa por creator. Score sem evidência = inválido.

## 3.4 Red flags

- Posts só de sorteio e publi, zero conteúdo próprio
- Bio só email comercial sem identidade
- Engajamento comprado (picos em horários estranhos)
- Creator já publiou concorrente direto sem intervalo
- Valores incompatíveis (humor pesado vs marca family-friendly)

---

# PARTE IV: MODELOS DE PARCERIA BR

## 4.1 Permuta (barter)

**O que é**: produto/serviço em troca de conteúdo.

**Quando usar**: ticket baixo-médio, produto visual, estoque disponível, nano/micro creators.

**Prós**: baixo custo cash; UGC autêntico.

**Contras**: creator pode não priorizar; difícil escalar; valor tributário (atenção contábil).

**Exemplo**: marca de skincare envia kit; creator posta rotina de 60s.

## 4.2 Flat fee (cachê fixo)

**O que é**: pagamento único por entregáveis definidos.

**Quando usar**: mid/macro, campanhas com prazo, controle de mensagem.

**Faixa orientativa BR** (verificar via WebSearch/memory; varia muito):

- Nano: R$ 200-800 por post
- Micro: R$ 800-5.000
- Mid: R$ 5.000-25.000
- Macro: R$ 25.000+

Sempre marcar como estimativa até proposta formal.

## 4.3 Comissão / afiliado

**O que é**: % por venda via link/cupom do creator.

**Quando usar**: e-commerce, infoproduto, SaaS com margem; creator com audiência compradora.

**Prós**: paga por resultado; escala.

**Contras**: creator pode não promover sem base fixa; atribuição imperfeita.

**Estrutura típica**: 10-30% ou valor fixo por lead qualificado.

## 4.4 Embaixador (longo prazo)

**O que é**: relação recorrente (3-12 meses), múltiplos touchpoints.

**Quando usar**: marca estabelecida, produto de recompra, comunidade.

**Entregáveis**: X posts/mês, presença em eventos, primeiro acesso a lançamentos.

## 4.5 Co-criação

**O que é**: produto ou conteúdo desenvolvido junto (linha limitada, curso conjunto).

**Quando usar**: audiências sobrepostas, creator com expertise real.

**Prós**: buzz alto, diferenciação.

**Contras**: complexidade jurídica e operacional.

## 4.6 Matriz de decisão rápida

| Objetivo | Modelo preferido |
|---|---|
| Awareness rápido, budget baixo | Permuta + nano/micro |
| Lançamento com controle | Flat fee + mid |
| Venda direta | Afiliado + cupom |
| Marca de longo prazo | Embaixador |
| Diferenciação forte | Co-criação |

---

# PARTE V: OUTREACH E FOLLOW-UP

## 5.1 Framework de primeira mensagem (AIDA adaptado)

1. **Atenção**: referência específica ao conteúdo dele (post recente, série)
2. **Interesse**: por que a marca combina com a audiência dele
3. **Desejo**: o que ele ganha (não só "exposure")
4. **Ação**: pergunta fechada ou convite pra call curta

**Comprimento**: 80-120 palavras em email; DM ainda mais curta.

## 5.2 Exemplo PT-BR (email/DM)

> Oi, [Nome]! Vi seu reel sobre [tema específico] e curti como você explicou [detalhe]. Sou da [Marca] e a gente trabalha com [produto] pra [público].
>
> Tô montando uma collab com creators que falam de [nicho] e acho que faz sentido pra sua audiência: [benefício concreto, ex: kit + fee ou comissão X%].
>
> Faz sentido trocar uma ideia de 15 min essa semana?

## 5.3 Ângulos alternativos (auto-iteração)

- **Ângulo valor mútuo**: foco no benefício da audiência dele
- **Ângulo co-criação**: convite pra ideia conjunta
- **Ângulo resultado**: case de creator similar (com permissão)

## 5.4 Follow-up

- **Timing**: D+5 a D+7 úteis, uma vez
- **Tom**: leve, sem culpa ("sei que a caixa enche")
- **Não**: 3 follow-ups, mensagem idêntica, pressão

Exemplo follow-up:
> Oi, [Nome]! Passando pra ver se a proposta de collab com a [Marca] chegou a fazer sentido. Se não for o momento, sem problema. Abraço!

## 5.5 O que nunca fazer

- Mensagem genérica sem referência ao conteúdo
- "Temos uma oportunidade incrível" sem detalhe
- Pedir publi grátis como única contrapartida
- Enviar brief de 5 páginas na primeira mensagem
- Contatar pelo mesmo creator em 3 canais no mesmo dia

---

# PARTE VI: NEGOCIAÇÃO E BRIEF DE COLLAB

## 6.1 Entregáveis típicos

| Formato | Spec mínima |
|---|---|
| Reels/TikTok | 30-60s, roteiro aprovado, #publi na legenda |
| Stories | 3 frames, link sticker, menção @marca |
| Feed | 1 carrossel ou foto, copy aprovada |
| YouTube | Integração 60-90s ou vídeo dedicado |

## 6.2 Direitos de uso

Definir no brief:

- Uso orgânico só no perfil do creator vs repurposing em ads da marca
- Prazo (6 meses, 12 meses, perpetuidade)
- Whitelisting / Spark Ads (Meta, TikTok)
- Exclusividade de categoria (ex: 30 dias sem concorrente direto)

## 6.3 Disclosure obrigatório (CONAR)

Conteúdo remunerado ou permuta com contrapartida comercial:

- **#publi** ou **#publicidade** ou **#parceriaremunerada**
- Visível, não escondido no meio de 30 hashtags
- Stories: texto legível no frame

O agent inclui disclosure no brief; compliance final é do usuário.

## 6.4 Estrutura de brief de collab

```markdown
## Brief: [Marca] x [Creator]

### Objetivo da campanha
[awareness | conversão | lançamento]

### Mensagem-chave (1 frase)
[...]

### Entregáveis
- [formato, quantidade, prazo]

### Tom e restrições
- Fazer: [...]
- Evitar: [...]

### Produto / compensação
[permuta + fee | só fee | comissão X%]

### Disclosure
#publi obrigatório

### Aprovação
Roteiro aprovado em [X] dias antes da publicação

### Métricas de sucesso
[views, cliques, vendas cupom X]
```

---

# PARTE VII: MÉTRICAS DE PARCERIA

## 7.1 KPIs por objetivo

| Objetivo | Métrica primária | Secundária |
|---|---|---|
| Awareness | Alcance, impressões | Salvamentos, shares |
| Engajamento | ER no post patrocinado | Comentários qualitativos |
| Conversão | Vendas via cupom/UTM | CPA da parceria |
| UGC | Direitos adquiridos | Performance em ads whitelisted |

## 7.2 CPE (custo por engajamento)

```
CPE = Investimento total / (likes + comments + shares + saves)
```

Comparar CPE da parceria vs CPE de ad equivalente (benchmark interno).

## 7.3 Atribuição

- Cupom único por creator
- UTM: `?utm_source=creator&utm_medium=influencer&utm_campaign=[nome]`
- Link na bio temporário
- Planilha de vendas manual se não houver tracking automático

## 7.4 O que registrar na memory

- Creators contatados + status
- Faixas de fee que o nicho aceitou (verificadas)
- Formatos de collab com melhor ROI reportado

---

# PARTE VIII: ANTI-PADRÕES

1. **Só olhar seguidores**: ER e fit importam mais
2. **"Exposure" como pagamento**: creator profissional recusa
3. **Outreach em massa idêntico**: queima reputação da marca
4. **Enviar sem revisar** (viola produto do Marketing OS)
5. **Números inventados** de audiência ou fee
6. **Esquecer #publi**: risco CONAR e de credibilidade
7. **Parceria com creator polêmico** sem red team
8. **Confundir com pesquisa de mercado** (sem outreach acionável)

---

# PARTE IX: REFERÊNCIAS CRUZADAS

| Necessidade | Agent / recurso |
|---|---|
| Pesquisa de nicho e audiência (sem outreach) | mos-research |
| Copy do roteiro da publi | mos-copy |
| Criativo de ad com whitelisting | mos-ads |
| Tom de voz da marca no brief | mos-brand |
| Resposta a comentários pós-publi | mos-community |
| Métricas de campanha agregadas | mos-analytics |
| Scripts Apify | `scripts/apify_instagram.py`, `scripts/apify_tiktok.py` |

Fluxo típico do command `/prospectar-creators`: mos-research (sourcing/validação) → mos-partnerships (fit + drafts).
