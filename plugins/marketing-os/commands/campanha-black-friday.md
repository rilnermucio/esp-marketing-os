---
description: Preset de Black Friday e datas comemorativas. Dispatcha mos-launch sequencial, depois mos-copy + mos-email + mos-ads + mos-social em paralelo, fechando com mos-analytics em tempo real. Clone primário hormozi.
argument-hint: "<produto> [--desconto=...] [--clone=hormozi|suby] [--canal=...] [--data=black-friday|cyber-monday|...]"
---

# /campanha-black-friday: Preset de Black Friday e Datas Especiais

**Objetivo:** Maximizar receita em datas especiais (Black Friday, Cyber Monday, datas comemorativas).
**Clone primário:** `hormozi` · **Clone alternativo:** `suby`

## Required inputs (ask if missing)

1. **Produto/oferta** (obrigatório)
2. **Desconto e bônus** (obrigatório): composição da oferta de BF
3. **Data alvo** (obrigatório): Black Friday, Cyber Monday, etc.
4. **Customizações opcionais:** `--clone=<override>`, `--canal=<canal>`, `--budget=<valor>`

## Dispatch

**Fase 1 (sequencial, estratégia precisa vir primeiro):**

```
- Agent(subagent_type: "mos-launch", prompt: "Estratégia Black Friday pra [produto]: composição da oferta (desconto + bônus + urgência real), value stack que justifica o preço, cronograma D-7 → D+2, lista VIP pra warm-up. Frameworks: Hormozi value stack + scarcity real (não artificial).")
```

**Fase 2 (paralelo, depende da estratégia):**

```
- Agent(subagent_type: "mos-copy", prompt: "Copy clone=hormozi de alta urgência pra Black Friday: headlines de oferta, página de vendas atualizada com timer, CTAs agressivos mas honestos, FAQ de objeções de fim de ano. Quality gates + compliance.")

- Agent(subagent_type: "mos-email", prompt: "Sequência intensiva 7 dias:
  - Dia -7: teaser + abertura da lista VIP
  - Dia -3: anúncio oficial da promoção
  - Dia -1: último aviso
  - Dia 0: abertura, Black Friday (manhã + tarde + noite)
  - Dia +1: Cyber Monday (se aplicável)
  - Dia +2: última chance (manhã + 6h antes do fim)
  Considere memory de campanhas BF anteriores.")

- Agent(subagent_type: "mos-ads", prompt: "Campanhas agressivas de conversão pra BF: budget escalonado D-7 → D+2, bid strategy ROAS, criativos com timer + desconto destacado, retargeting de carrinho abandonado. ROAS alvo > 4x.")

- Agent(subagent_type: "mos-social", prompt: "Posts e stories de contagem regressiva + promoção: D-7 teaser, D-3 oficial, D-1 urgência, D0 abertura, D+1 social proof de quem comprou, D+2 última chance. Quality gates + enquete.")
```

**Fase 3 (paralelo durante a campanha):**

```
- Agent(subagent_type: "mos-analytics", prompt: "Monitoramento em tempo real durante BF: receita/hora vs meta, ROAS por canal, conversão do checkout, alertas de queda. Dashboard de plantão.")
```

## Cronograma

| Dia | Ação |
|-----|------|
| D-7 | Teaser + lista VIP |
| D-3 | Anúncio oficial da promoção |
| D-1 | Último aviso |
| D 0 | Abertura, Black Friday |
| D+1 | Cyber Monday (se aplicável) |
| D+2 | Última chance |

## Frameworks

- Value Stack, Alex Hormozi
- Urgência Real (não artificial)
- Scarcity Marketing

### Checklist Black Friday

```
3 SEMANAS ANTES:
[ ] Oferta definida (produto + bônus + desconto) (Fase 1: mos-launch)
[ ] Value stack calculado pra justificar preço (Fase 1)
[ ] Lista VIP de espera criada
[ ] Copy completa preparada (Fase 2: mos-copy)
[ ] Design dos assets (mos-design opcional)

1 SEMANA ANTES:
[ ] Anúncios configurados (Fase 2: mos-ads), não ativar ainda
[ ] Página de vendas e checkout testados
[ ] Posts e emails agendados
[ ] Briefing da equipe

NO DIA:
[ ] Anúncios ativados às 00h01
[ ] Email de abertura enviado
[ ] Posts em todas as plataformas
[ ] Monitoramento por hora (Fase 3: mos-analytics)
```

### KPIs

| KPI | Meta | Como Medir |
|-----|------|------------|
| Receita vs meta | 100%+ | Vendas BF / meta definida |
| ROAS | > 4x (BF tem melhor ROAS) | Receita / gasto em ads |
| Conversão vs normal | 2-3x maior | Taxa BF / taxa baseline |
| Carrinho abandonado recuperado | > 15% | Recuperações / abandonos |

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Sem `—`, sem "brutal", sem CAPS gratuito
- Acentuação PT-BR correta
- Urgência REAL (estoque limitado, prazo verdadeiro), nunca falsa
- Compliance regulatório, especialmente em saúde/finanças
- Disclaimer "Resultados não garantidos" em qualquer promessa quantitativa
- Enquete obrigatória em conteúdo social

## Memory note

Os agents `mos-copy`, `mos-email`, `mos-ads`, `mos-social`, `mos-launch` têm memory project em `.claude/agent-memory/marketing-os-<agent>/`. Sempre mencione no prompt que considere memory de campanhas BF anteriores para evitar reciclar ângulos saturados e para escalar o que já performou bem.
