---
description: Preset de lançamento. Dispatcha mos-research + mos-launch + mos-funnel em paralelo, depois mos-copy + mos-storytelling + mos-social + mos-email, fechando com mos-ads + mos-design + mos-analytics. Clone primário brunson.
argument-hint: "<produto> [--preco=...] [--clone=brunson|suby|hormozi] [--canal=...] [--budget=...] [--nicho=...]"
---

# /campanha-lancamento: Preset de Lançamento

**Objetivo:** Lançar produto, serviço, curso ou oferta com máximo impacto.
**Clone primário:** `brunson` · **Clone alternativo:** `suby`

## Required inputs (ask if missing)

1. **Produto/oferta** (obrigatório)
2. **Audiência/avatar** (obrigatório)
3. **Ticket/preço** (obrigatório)
4. **Customizações opcionais:** `--clone=<override>`, `--canal=<canal>`, `--budget=<valor>`, `--nicho=<nicho>`

## Dispatch

**Fase 1 (paralelo, single message):**

```
- Agent(subagent_type: "mos-research", prompt: "Validação pré-lançamento de [produto] pra [avatar/nicho]: tamanho do nicho, concorrência ativa, ticket médio praticado, dores não atendidas, ângulos de oferta com tração. Considere memory existente.")

- Agent(subagent_type: "mos-launch", prompt: "Estratégia de lançamento pra [produto], ticket [preço]: escolher modelo (PLF / semente / relâmpago / perpétuo) baseado em nicho [nicho] e tamanho da lista. Definir cronograma -2sem → +5dias, pitch timing, gatilhos de escassez.")

- Agent(subagent_type: "mos-funnel", prompt: "Funil de lançamento pra [produto]: TOFU (aquecimento orgânico + ads) → MOFU (lead magnet/CPL/webinar) → BOFU (carta de vendas + carrinho). Pontos de queda esperados e contramedidas.")
```

**Fase 2 (paralelo, depende da estratégia da Fase 1):**

```
- Agent(subagent_type: "mos-copy", prompt: "Copy de lançamento clone=brunson: headline da página, big idea, mecanismo único, anti-avatar, stack value, garantia, FAQ. Usando posicionamento da Fase 1: [colar].")

- Agent(subagent_type: "mos-storytelling", prompt: "Narrativa da jornada do produto: arco do criador → problema dor → descoberta → solução. Hero's journey aplicado ao pitch de lançamento.")

- Agent(subagent_type: "mos-social", prompt: "Sequência de posts de aquecimento (5-7 posts): semana -2 problema, semana -1 solução parcial, dia 0 abertura. Plataforma [Instagram/LinkedIn/etc]. Aplicar quality gates + enquete.")

- Agent(subagent_type: "mos-email", prompt: "Sequência completa de lançamento: 5 emails de pré-aquecimento + email abertura carrinho + 3 emails de urgência/prova/fechamento + email pós-fechamento. Considere memory do cliente.")
```

**Fase 3 (sequencial, depende da copy/criativo da Fase 2):**

```
- Agent(subagent_type: "mos-ads", prompt: "Campanhas de tráfego pra cada fase do lançamento: pré (lista quente), durante (conversão), retargeting pós. Budget [valor]. Audiências quentes/frias/lookalikes.")

- Agent(subagent_type: "mos-design", prompt: "Assets visuais da campanha: identidade do lançamento, paleta, capa do produto, mockups, criativos de ads, banners de página. Coerência com brand existente.")

- Agent(subagent_type: "mos-analytics", prompt: "Setup de tracking: pixels, UTMs, eventos de conversão (lead, view-content, add-to-cart, purchase), KPIs do lançamento, dashboard de monitoramento.")
```

## Cronograma default

- **Semana -2:** Aquecimento (problema)
- **Semana -1:** Conteúdo de valor (solução parcial)
- **Dia -3:** Abertura do carrinho / anúncio do produto
- **Dia -1:** Urgência e prova social
- **Dia 0:** Lançamento oficial
- **Dia +2:** Depoimentos e follow-up
- **Dia +5:** Fechamento / última chance

## Frameworks aplicados

- PLF (Product Launch Formula), Jeff Walker
- Seed-and-Launch, Russell Brunson
- Value Stack, Alex Hormozi

### Checklist de Lançamento

```
PRÉ-LANÇAMENTO (2 semanas antes):
[ ] Pesquisa de mercado e validação de oferta (Fase 1: mos-research)
[ ] Definição de avatar e posicionamento (Fase 1)
[ ] Produto/oferta core completa
[ ] Landing page de captura de leads / lista de espera
[ ] Sequência de email de aquecimento (Fase 2: mos-email)
[ ] Conteúdo de aquecimento social (Fase 2: mos-social)
[ ] Assets visuais e identidade (Fase 3: mos-design)
[ ] Setup de tracking, pixel, UTMs, conversões (Fase 3: mos-analytics)

LANÇAMENTO (dia D):
[ ] Email de abertura
[ ] Posts em todas as plataformas ativas
[ ] Anúncios pagos ativados
[ ] Stories com contagem regressiva
[ ] Monitoramento em tempo real (mos-analytics)

PÓS-LANÇAMENTO:
[ ] Sequência de follow-up
[ ] Retargeting para não-convertidos
[ ] Email de fechamento
[ ] Análise de performance (mos-analytics)
[ ] Documentação de aprendizados
```

### KPIs

| KPI | Benchmark | Como Medir |
|-----|-----------|------------|
| Conversão da lista | 3-7% | Compras / leads na lista |
| ROAS de ads | > 3x | Receita / Gasto em ads |
| Open rate emails | > 35% | Abertos / enviados |
| CTR emails | > 5% | Cliques / abertos |

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Sem `—`, sem "brutal", sem CAPS gratuito
- Acentuação PT-BR correta
- Compliance regulatório se nicho saúde/finanças/suplementos

## Memory note

Os agents `mos-copy`, `mos-email`, `mos-ads`, `mos-social`, `mos-funnel`, `mos-launch` têm memory project em `.claude/agent-memory/marketing-os-<agent>/`. Sempre mencione no prompt que considere memory existente do cliente para evitar repetir hooks usados, manter consistência com campanhas passadas e respeitar restrições de compliance previamente registradas.
