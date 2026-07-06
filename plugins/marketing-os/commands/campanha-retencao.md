---
description: Preset de retenção. Dispatcha mos-research + mos-analytics em paralelo, depois mos-email + mos-copy + mos-social. Foco em LTV, reativação de inativos e redução de churn. Clone primário abraham.
argument-hint: "<base/contexto> [--segmento=inativos-90dias|vip|risco|todos] [--desconto=...] [--clone=abraham|leila-hormozi]"
---

# /campanha-retencao: Preset de Retenção

**Objetivo:** Aumentar LTV, reativar clientes inativos, reduzir churn.
**Clone primário:** `abraham` · **Clone alternativo:** `leila-hormozi`

## Required inputs (ask if missing)

1. **Base de clientes** (obrigatório): tamanho, segmentos disponíveis, dados de recência
2. **Segmento foco** (recomendado): inativos-90dias, vip, em-risco, ou todos
3. **Customizações opcionais:** `--desconto=<%>`, `--clone=<override>`

## Dispatch

**Fase 1 (paralelo, entender LTV/churn antes de agir):**

```
- Agent(subagent_type: "mos-research", prompt: "Análise da base atual: segmentação por recência/valor, identificação de clientes inativos (>90d), perfil de churn (motivos), ticket médio histórico. Considere memory do cliente.")

- Agent(subagent_type: "mos-analytics", prompt: "Métricas de retenção: LTV médio, taxa de churn mensal, segmento VIP (top 20%), padrões de queda de engajamento. Setup de alertas de risco.")
```

**Fase 2 (paralelo, depende dos segmentos da Fase 1):**

```
- Agent(subagent_type: "mos-email", prompt: "Sequências por segmento clone=abraham:
  - Inativos 90+d: 5 emails em 14d (reconexão genuína + oferta de retorno)
  - Ativos < 90d: upsell/cross-sell (estilo Hormozi confiante)
  - VIP top 20%: programa de fidelidade + indicação personalizada
  - Em risco de churn: 3 emails rápidos perguntando o problema + suporte personalizado
  Considere memory.")

- Agent(subagent_type: "mos-copy", prompt: "Copy de reativação e upsell clone=abraham: headlines que evocam reconexão (não desconto barato), CTAs de retorno, emails de programa de indicação.")

- Agent(subagent_type: "mos-social", prompt: "Conteúdo pra clientes existentes: bastidores, novidades, casos de uso avançados. Reforça valor pra quem já comprou. Quality gates + enquete.")
```

## Segmentação

```
SEGMENTO 1, INATIVOS (>90d): Reativação com oferta exclusiva. Tom Abraham. 5 emails / 14d.
SEGMENTO 2, ATIVOS (<90d): Upsell/cross-sell. Tom Hormozi. Email + social.
SEGMENTO 3, VIP (top 20%): Programa de fidelidade. Tom exclusivo. Email + ligação se high-ticket.
SEGMENTO 4, RISCO DE CHURN: Engajamento de emergência. 3 emails rápidos + suporte personalizado.
```

## Frameworks

- Os 3 Pilares, Abraham (Pilar 2 e 3)
- LTV Maximization
- Reactivation Sequence, Dan Kennedy

### Checklist

```
SETUP (uma vez):
[ ] Segmentar base por recência e valor (Fase 1)
[ ] Sequência de onboarding (novos clientes)
[ ] Sequência de reativação (inativos) (Fase 2: mos-email)
[ ] Sequência de upsell (ativos) (Fase 2: mos-email)
[ ] Critérios de "cliente em risco" definidos (Fase 1: mos-analytics)

OPERAÇÃO MENSAL:
[ ] Lista de inativos do mês exportada
[ ] Campanha de reativação rodada
[ ] Oportunidades de upsell identificadas
[ ] Taxa de churn analisada
```

### KPIs

| KPI | Meta | Como Medir |
|-----|------|------------|
| LTV médio | Crescente mês a mês | Receita total / clientes únicos |
| Reativação | > 10% | Compras de inativos / inativos contatados |
| Upsell | > 15% | Clientes que aceitam upsell / clientes contatados |
| Churn | Abaixo da meta | Cancelamentos / base ativa |

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Sem `—`, sem "brutal", sem CAPS gratuito
- Acentuação PT-BR correta
- Compliance regulatório se nicho saúde/finanças/suplementos
- Enquete obrigatória em conteúdo social

## Memory note

Os agents `mos-copy`, `mos-email`, `mos-social` têm memory project em `.claude/agent-memory/marketing-os-<agent>/`. Sempre mencione no prompt que considere memory existente do cliente para respeitar histórico de comunicação com cada segmento.
