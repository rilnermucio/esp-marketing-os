---
description: Shortlist de creators com fit score e rascunhos de outreach. Dispatch sequencial mos-research → mos-partnerships; Gmail create_draft quando MCP disponível (nunca send).
argument-hint: "<nicho + o que a marca oferece/espera, ex: 'skincare, permuta + fee micro, reels 60s'>"
---

# /prospectar-creators: Prospectar Creators e Outreach (Dispatch-Based)

Descobre creators do nicho, valida fit e redige rascunhos de outreach orquestrando **sequencial** `mos-research` → `mos-partnerships`. **Nada é enviado automaticamente.**

## Required inputs (ask if missing)

1. **Nicho e ICP do creator** (obrigatório): tema, faixa de seguidores, região
2. **Oferta de parceria** (obrigatório): o que a marca oferece (permuta, fee, comissão) e o que espera (entregáveis, prazo)
3. **Critérios de fit** (opcional; agent propõe se faltar): ER mínimo, valores, exclusões
4. **Quantidade** (opcional, default 5-10): tamanho da shortlist
5. **Canal preferido** (opcional): Instagram, TikTok, YouTube

## Dispatch Decision Tree

```
Briefing recebido
  ├── Oferta de parceria indefinida?
  │     └── PARAR: pedir o que marca oferece e espera
  │
  ├── Sourcing/validação de audiência necessária?
  │     └── Dispatch SEQUENCIAL: mos-research → mos-partnerships
  │
  └── Lista de creators já fornecida pelo usuário?
        └── Dispatch SIMPLES: mos-partnerships (fit + outreach)
```

## Dispatch Sequencial (padrão)

```
Passo 1: Agent(subagent_type: "mos-research", prompt: "Research para prospectar creators de [nicho]. Objetivo: shortlist de parceria (não pesquisa genérica). Entregue: creators/concorrentes que já fazem publi no nicho, hashtags e perfis referência, faixas de audiência verificáveis, sinais de engajamento real vs inflado. Use WebSearch e, se APIFY_TOKEN disponível, apify_instagram/apify_tiktok. Não invente números; marque estimativas. Retorne research brief compacto pra partnerships.")

Passo 2: Agent(subagent_type: "mos-partnerships", prompt: "Monte shortlist e outreach. Nicho: [nicho]. Oferta da marca: [oferece + espera]. Critérios de fit: [critérios]. Research do passo anterior: [brief]. Quantidade: [N] creators. Para cada um: fit score 1-10 com justificativa verificável, modelo de parceria sugerido, 2-3 ângulos de primeira mensagem + follow-up. Red team win-win, audiência real, risco de marca. Se MCP Gmail disponível: create_draft por creator (NUNCA send). Senão: textos prontos. Modo: RASCUNHO ONLY. Aplicar quality gates.")
```

## Dispatch Simples (lista já fornecida)

```
Agent(subagent_type: "mos-partnerships", prompt: "Avalie fit e redija outreach para: [lista de @handles]. Oferta: [oferece + espera]. Entregue shortlist com fit score, modelos sugeridos e rascunhos (Gmail create_draft se MCP, senão texto). Nunca enviar. Aplicar quality gates.")
```

## Consolidação

Entregue ao usuário:

```markdown
## Prospectar Creators: [nicho]

### Oferta de parceria
[O que marca oferece / espera]

### Shortlist
| Creator | Fit | Modelo | Justificativa |
|---|---|---|---|

### Rascunhos de outreach
[Por creator: ângulos A/B/C + follow-up]

### Gmail
[create_draft executado para N creators | textos prontos para colar]

### Próximos passos
- Revisar e enviar manualmente
- Após resposta positiva: brief formal de collab (mos-partnerships PARTE VI)
- Registrar status na memory do mos-partnerships
```

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md` + gates do mos-partnerships:
- **Nunca send**: apenas rascunho ou `create_draft`
- Fit score com justificativa verificável por creator
- Sem números de audiência inventados (WebSearch/Apify ou marcar estimativa)
- Disclosure #publi previsto no modelo de parceria remunerada
- Sem `—`, sem "brutal", sem antítese negação→afirmação, acentos PT-BR

## Por que esse dispatch

Sourcing de mercado e fechamento de parceria são competências distintas. O `mos-research` valida audiência e referências do nicho com dados verificáveis; o `mos-partnerships` transforma isso em shortlist acionável com outreach win-win. Separar evita outreach genérico sem fit e evita research acadêmico sem próximo passo comercial.
