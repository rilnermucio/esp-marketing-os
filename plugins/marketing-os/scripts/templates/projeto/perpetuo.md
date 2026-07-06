---
name: {name}
slug: {slug}
type: perpetuo
status: active
current_stage: research
default_approval: required
created_at: {created_at}
pipeline:
  - id: research
    agent: mos-research
    approval: skip
  - id: funil
    agent: mos-funnel
    approval: required
  - id: copy
    agent: mos-copy
    approval: required
  - id: ads
    agent: mos-ads
    approval: required
  - id: analytics
    agent: mos-analytics
    approval: skip
---

# Briefing: {name}

## Produto/Oferta perpétua
[Descrever a oferta evergreen]

## Avatar
[Cliente ideal]

## Ticket
[Preço]

## Canais de tráfego
[Meta Ads / Google Ads / Orgânico]

## Notas adicionais
[Detalhes relevantes]
