---
name: {name}
slug: {slug}
type: lancamento
status: active
current_stage: research
default_approval: required
created_at: {created_at}
pipeline:
  - id: research
    agent: mos-research
    approval: skip
  - id: estrategia
    agent: mos-launch
    approval: required
  - id: funil
    agent: mos-funnel
    approval: required
  - id: copy
    agent: mos-copy
    approval: required
  - id: design
    agent: mos-design
    approval: required
  - id: ads
    agent: mos-ads
    approval: required
---

# Briefing: {name}

## Produto/Oferta
[Descrever o produto]

## Avatar
[Quem é o cliente ideal]

## Ticket
[Preço]

## Cronograma
- Início: {created_at}
- Carrinho abre: [data]
- Carrinho fecha: [data]

## Notas adicionais
[Detalhes relevantes]
