---
description: Create a complete infoproduct (curso/membership/mentoria/ebook), research, structure, pricing, launch plan, sales materials. Dispatches workflow #7 (research → structure+launch+funnel → copy+email+ads).
argument-hint: "<type and topic, e.g., 'curso de IA pra empreendedores BR ticket R$ 1.997'>"
---

# /criar-infoproduto: Lançamento de Infoproduto Completo (Workflow #7)

Cria infoproduto + estratégia de lançamento conforme **workflow #7** em `skills/marketing-os/SKILL.md`.

## Required inputs (ask if missing)

1. **Formato** (obrigatório): curso online | membership | mentoria | ebook | comunidade paga | desafio
2. **Tópico** (obrigatório): o que ensina
3. **Avatar** (obrigatório): cargo, dor, faixa de renda
4. **Ticket alvo** (obrigatório): low (até R$ 297) | mid (R$ 297-1997) | high (R$ 1997+)
5. **Marca nova ou pivô?** (define se precisa mos-brand)
6. **Urgência de lançamento** (obrigatório): semana | mês | trimestre | sem prazo

## Dispatch, Fase 1 (paralelo, single message)

```
- Agent(subagent_type: "mos-research", prompt: "Validação de mercado para [formato] sobre [tópico]: tamanho do nicho BR, concorrentes ativos, ticket médio praticado, dores não atendidas, fontes de tráfego dominantes. Considere memory existente do cliente neste projeto. Retorne brief com 3-5 oportunidades de diferenciação.")

- Agent(subagent_type: "mos-brand", prompt: "Posicionamento e voz da marca/expert para [formato sobre tópico]. Definir arquétipo, tom, valores-chave, diferenciação competitiva. Considere memory existente do cliente neste projeto.")  # SÓ SE marca nova ou pivô

- Agent(subagent_type: "mos-infoproduct", prompt: "Estrutura completa do [formato]: módulos/aulas, formato de entrega, pricing strategy (por tier), bônus, garantia. Ticket alvo: [low/mid/high]. Aplicar princípios de andragogia/microlearning. Considere memory existente do cliente neste projeto.")
```

## Fase 2 (sequencial, depende dos outputs da Fase 1)

```
- Agent(subagent_type: "mos-launch", prompt: "Estratégia de lançamento (PLF / semente / relâmpago / perpétuo) baseada no produto: [colar resumo mos-infoproduct], avatar, urgência: [semana/mês/trimestre]. Definir cronograma e modelo. Considere memory existente do cliente neste projeto.")

- Agent(subagent_type: "mos-funnel", prompt: "Funil completo de lançamento: TOFU (CPL/anúncios) → MOFU (lead magnet/webinar/conteúdo) → BOFU (página de vendas/aplicação). Baseado em estratégia: [colar mos-launch]. Considere memory existente do cliente neste projeto.")
```

## Fase 3 (paralelo, depende da Fase 2)

```
- Agent(subagent_type: "mos-copy", prompt: "Página de vendas + headlines + CTAs alinhados com promessa do produto e estratégia de lançamento. Considere memory existente do cliente neste projeto.")

- Agent(subagent_type: "mos-email", prompt: "Sequência completa: pré-lançamento (lista) + abertura de carrinho + nutrição + última chamada + reengajamento. Cronograma alinhado com mos-launch.")

- Agent(subagent_type: "mos-ads", prompt: "Campanhas de tráfego pra cada fase do lançamento: pré (lista CPL) + durante (conversão) + retargeting de carrinho abandonado. Plataformas adequadas pro ticket [low/mid/high]. Considere memory existente do cliente neste projeto.")
```

## Fase 4: Quality Gates + Compliance + Próximos Passos

Aplicar gates globais do `skills/marketing-os/SKILL.md` (sem `—`, sem "brutal", PT-BR correto, máx 1-2 emojis) em todo conteúdo. Compliance regulatório por nicho (saúde/finanças/etc.). Sugerir teste A/B em headline + oferta + cronograma (mos-ab-testing) e setup de tracking (mos-analytics) pra métricas de lançamento.

## Consolidação

```markdown
## Infoproduto: [Nome]: [Formato]

### Validação de Mercado (mos-research)
[Tamanho + concorrentes + ticket + oportunidades]

### Marca/Posicionamento (mos-brand), se aplicável
[Arquétipo + voz + diferenciação]

### Estrutura do Produto (mos-infoproduct)
[Módulos + pricing + bônus + garantia]

### Estratégia de Lançamento (mos-launch)
[Modelo + cronograma + ticket]

### Funil de Lançamento (mos-funnel)
[TOFU + MOFU + BOFU + benchmarks]

### Materiais de Venda
**Sales Page (mos-copy):**
[Headlines + body + CTAs]

**Sequência de Email (mos-email):**
[Cronograma de emails por fase]

**Campanhas de Tráfego (mos-ads):**
[Estrutura de conta + criativos + budget]

### Próximos Passos
- A/B test em headline e oferta
- Setup de tracking (eventos pra GA4/Meta Pixel)
- Cronograma com datas específicas
```

## Por que esse encadeamento

Lançamento não é peça única, é orquestração de estratégia + estrutura + funil + execução. Pular Fase 1 (research) é o erro #1 de quem lança no escuro. Pular Fase 2 (escolha de modelo de lançamento) é o erro #2 de copiar PLF sem entender se cabe.
