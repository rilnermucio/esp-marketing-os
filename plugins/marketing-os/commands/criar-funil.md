---
description: Create a complete sales funnel strategy (TOFU/MOFU/BOFU) with content plan, email sequences, conversion optimization. Dispatches mos-funnel (with mos-research and mos-copy when needed).
argument-hint: "<funnel type and goal, e.g., 'lead generation funnel for SaaS' or 'course launch funnel'>"
---

# /criar-funil: Funil de Vendas

Cria estratégia completa de funil orquestrando subagents conforme `skills/marketing-os/SKILL.md`.

## Required inputs (ask if missing)

1. **Tipo de funil** (obrigatório): lead funnel | webinar funnel | tripwire | evergreen | launch funnel | high-ticket application
2. **Produto/Oferta** (obrigatório): nome, ticket, formato
3. **Avatar** (obrigatório): cargo, dor, faixa de renda
4. **Tráfego de origem** (obrigatório): orgânico, ads pagos, referência, etc.
5. **Cliente novo ou existente?** (define se precisa de mos-research)

## Dispatch, decisão por contexto

### Caso A: Cliente conhecido + funil tradicional

**Dispatch simples:**
```
- Agent(subagent_type: "mos-funnel", prompt: "Mapear funil [tipo] para [produto/avatar/ticket]: stages TOFU/MOFU/BOFU, conteúdo por estágio, taxas benchmark, pontos de queda, otimizações. Tráfego: [origem]. Considere memory existente do cliente neste projeto.")
```

### Caso B: Cliente novo OU nicho não validado

**Dispatch paralelo (single message):**
```
- Agent(subagent_type: "mos-research", prompt: "Validar [nicho/avatar]: tamanho do mercado, concorrentes ativos, ticket médio praticado, dores não atendidas, fontes de tráfego comuns. Considere memory existente do cliente neste projeto. Retorne research brief.")

- Agent(subagent_type: "mos-funnel", prompt: "Mapear funil [tipo]: stages, conteúdo por estágio, taxas benchmark, usar research brief da pesquisa paralela. Considere memory existente do cliente neste projeto.")
```

### Caso C: Funil de webinar

→ Use `/criar-webinar` (workflow #6 dedicado)

### Caso D: Funil de lançamento de infoproduto

→ Use `/criar-infoproduto` (workflow #7 dedicado, mais completo)

## Consolidação

```markdown
## Funil [Tipo]: [Produto]

### Estrutura
- TOFU: [conteúdo de topo, fontes de tráfego]
- MOFU: [lead magnet, nutrição]
- BOFU: [oferta, CTA, escassez]

### Sequência de Emails por Estágio
[Quantos emails em cada fase + objetivo]

### Pontos de Queda Esperados
[Onde os leads costumam abandonar + remediação]

### Métricas-chave
[CPL, taxa de conversão por etapa, LTV alvo]

### Próximos Passos
- Setup de tracking (mos-analytics)
- Copy específica de cada peça (mos-copy)
- Sequência de emails detalhada (mos-email)
- Tráfego pago se aplicável (mos-ads)
```

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Sem `—`, sem "brutal", sem CAPS gratuito
- Acentuação PT-BR correta
- Compliance regulatório por nicho (saúde/finanças/suplementos)

## Por que esse dispatch

Funil é um framework estratégico que `mos-funnel` cobre profundamente. Para clientes novos, `mos-research` valida assumptions ANTES de mapear o funil, evita projetar funil sobre premissas erradas. Os outros agents (copy, email, ads, analytics) são executores das peças individuais, chame em comandos dedicados depois.
