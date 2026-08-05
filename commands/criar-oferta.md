---
description: Architect a complete offer (value stack, pricing, guarantee, bonuses, urgency). Dispatches mos-offer, com escalação pra mos-research (validação) e handoff pra mos-copy (página).
argument-hint: "<produto/serviço + público + ticket pretendido, ex: 'mentoria de tráfego pago, gestores, ~R$5k'>"
---

# /criar-oferta: Arquitetura de Oferta (Dispatch-Based)

Desenha a oferta em si (promessa, stack, preço, garantia, condições, motivo pra agir) orquestrando `Agent(subagent_type: "mos-offer")`. Não produz inline. A copy da página que vende a oferta é etapa seguinte (`mos-copy`).

## Required inputs (ask if missing)

1. **Produto/serviço** (obrigatório): o que é entregue (se o produto ainda não existe, rotear antes pra `/criar-infoproduto`)
2. **Público** (obrigatório): quem compra + nível de consciência se souber
3. **Modelo** (obrigatório): high-ticket/mentoria, curso, serviço, SaaS, e-commerce
4. **Ticket pretendido** (opcional): faixa de preço alvo ou "me recomenda"
5. **Posição no funil** (opcional, default core): core, tripwire, upsell, downsell
6. **Dados atuais** (opcional, valioso): preço atual, taxa de conversão, refund, objeções ouvidas em call
7. **Dossiê de USP** (opcional, recomendado): Handoff Context aprovado pelo `mos-brand`, com versão, maturidade, USP principal, reason to believe, mecanismo, provas e limites da promessa
8. **Research de público e mercado** (opcional): Dossiê de Avatar, entrevistas, alternativas, capacidade de pagamento e objeções

## Contrato de Handoff da USP

Quando houver Dossiê de USP, passe seu Handoff Context integralmente ao
`mos-offer`. Preserve estes campos como fonte estratégica da oferta:

```json
{
  "usp_version": "...",
  "maturity": "exploratoria | validada | operacional",
  "primary_usp": "...",
  "reason_to_believe": ["..."],
  "mechanism_or_differentiator": "...",
  "evidence_ids": ["E01"],
  "claim_limits": ["..."],
  "open_hypotheses": ["H01"]
}
```

O `mos-offer` pode adaptar a expressão da promessa ao modelo comercial, desde
que preserve o sentido, as provas e os limites da USP aprovada. Qualquer mudança
material vira proposta de nova versão e precisa de aprovação explícita.

## Protocolo de Evidências

Toda afirmação material da oferta recebe ID, classe, confiança, fonte, data e
escopo:

- **EVIDÊNCIA CONFIRMADA**: dado, documento, demonstração ou fonte verificável
  que sustenta diretamente a afirmação.
- **INFERÊNCIA**: conclusão derivada de evidências identificadas, com racional
  explícito.
- **HIPÓTESE**: suposição ainda pendente de teste.

Preserve IDs recebidos da USP. Use `OE01`, `OI01` e `OH01` para evidências,
inferências e hipóteses específicas da arquitetura da oferta. Preços de
concorrentes, comparáveis de valor, capacidade, urgência, garantia e promessa
precisam aparecer no ledger. O resultado separa claims aprovados de claims
bloqueados e transforma toda hipótese central em item do plano de validação.

## Dispatch Decision Tree

```
Briefing recebido
  ├── Oferta core/high-ticket SEM research de público no briefing?
  │     └── Dispatch SEQUENCIAL: mos-research (dores, capacidade de
  │         pagamento, alternativas) → mos-offer
  │
  ├── Oferta com research/dados fornecidos?
  │     └── Dispatch SIMPLES: mos-offer
  │
  └── Pedido inclui a página/copy de venda junto?
        └── SEQUENCIAL: mos-offer → mos-copy (o handoff JSON do offer
            alimenta o value stack da copy; ver workflow de páginas na SKILL)
```

## Dispatch Simples

```
Agent(subagent_type: "mos-offer", prompt: "Arquitete a oferta. Produto: [produto]. Público: [público + consciência]. Modelo: [modelo]. Ticket alvo: [faixa ou 'recomendar']. Posição no funil: [posição]. Dados atuais: [dados ou 'nenhum']. Research disponível: [resumo integral ou 'nenhum']. Dossiê de USP e Handoff Context: [JSON integral ou 'nenhum']. Se houver Dossiê de USP, preserve usp_version, maturity, primary_usp, reason_to_believe, mechanism_or_differentiator, evidence_ids, claim_limits e open_hypotheses; qualquer mudança material vira proposta de nova versão. Considere memory existente do cliente neste projeto. Entregue no Output Schema do agent: promessa central, value stack com justificativa de valor por item, preço + ancoragem + parcelamento BR, garantia com termos e sustentabilidade, motivo real para agir, mapa objeção→elemento, top 2 arquiteturas com Offer Score e red team critique. Inclua Protocolo de Evidências com EVIDÊNCIA CONFIRMADA, INFERÊNCIA e HIPÓTESE, fonte e data, confiança e escopo; Claims Aprovados; Claims Bloqueados; Plano de Validação; e Handoff Context com os IDs preservados. Aplicar quality gates (urgência real, garantia sustentável, valor justificado, fact-check de comparáveis).")
```

## Escalações

- **Sem research em oferta core**: `Agent(subagent_type: "mos-research", prompt: "Research pra arquitetura de oferta: dores prioritárias de [público], faixa de investimento que esse público já pratica, alternativas/concorrentes com preços, objeções típicas. Retorne research brief compacto.")` ANTES do mos-offer (o pre-flight dele exige)
- **Produto indefinido**: redirecionar pra `/criar-infoproduto` (curriculum primeiro, oferta depois)
- **Página de venda da oferta**: após o offer, dispatch `mos-copy` com o Handoff Context JSON como insumo

## Consolidação

Entregue ao usuário:

```markdown
## Oferta: [nome]

### Fundação estratégica
- USP de origem: [primary_usp ou hipótese proposta]
- Versão e maturidade: [usp_version + maturity]
- Reason to believe: [itens com evidence_ids]
- Mecanismo ou diferencial: [mechanism_or_differentiator]
- Limites da promessa: [claim_limits]
- Hipóteses abertas: [open_hypotheses]

### Protocolo de Evidências
| ID | Afirmação | Classe | Confiança | Fonte e data | Escopo | Uso na oferta |
|---|---|---|---|---|---|---|
| OE01 | [...] | EVIDÊNCIA CONFIRMADA | alta | [...] | [...] | [...] |
| OI01 | [...] | INFERÊNCIA | média | deriva de [IDs] | [...] | [...] |
| OH01 | [...] | HIPÓTESE | baixa | validação pendente | [...] | [...] |

### Claims Aprovados
- [claim permitido + IDs de suporte + limites]

### Claims Bloqueados
- [claim sem suporte ou fora dos limites + motivo]

### A oferta em 1 parágrafo
[Promessa + stack resumido + preço + garantia + deadline]

### Value Stack
[Tabela do agent: componente, o que resolve, valor percebido, justificativa]
Valor total: R$ X | Preço: R$ Y | Ratio X:Y

### Preço, condições e garantia
[Preço + ancoragem + parcelamento | tipo de garantia + termos + nota CDC]

### Motivo para agir agora
[Mecanismo + por que é real]

### Arquitetura alternativa (top 2)
[Trade-offs e Offer Score de cada]

### Red Team (o que um comprador cético atacaria)
[3 fraquezas + resposta recomendada]

### Plano de Validação
| Hipótese | Método | Amostra ou fonte | Métrica ou sinal | Critério de decisão | Prioridade |
|---|---|---|---|---|---|
| OH01 | [...] | [...] | [...] | [...] | alta |

### Handoff Context
[JSON do mos-offer com USP de origem, evidence_ids, claims aprovados, claims bloqueados, hipóteses e plano de validação]

### Próximos passos
- Copy da página de vendas com esse stack (mos-copy / workflow #5 da SKILL)
- Posicionamento no funil (mos-funnel) e mecânica de lançamento (mos-launch)
- Registrar resultado real (take rate/refund) pra memory do mos-offer aprender
```

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md` + os específicos do mos-offer:
- Urgência/escassez com justificativa verificável (fabricada = refazer)
- Garantia sustentável (refund × conversão calculado)
- Valor percebido com comparável real por item do stack
- Fact-check via WebSearch para preços de concorrentes e claims de mercado
- Ledger com fonte e data para toda afirmação material da oferta
- Claims aprovados respeitam os limites da USP e os IDs de evidência
- Claims bloqueados permanecem fora de copy, ads e páginas
- Plano de validação cobre toda hipótese central
- Sem `—`, sem "brutal", sem antítese negação→afirmação, acentos PT-BR

## Por que esse dispatch

Oferta é a maior alavanca do marketing e vem ANTES da copy: stack fraco com copy forte converte pior que o contrário. O `mos-offer` isola essa engenharia (valor, preço, risco) com red team obrigatório porque erro aqui é caro e estrutural. Research vem antes quando falta insumo (pre-flight do agent barra oferta em vácuo), e a copy vem depois consumindo o handoff JSON, nunca em paralelo: a página depende do stack fechado.
