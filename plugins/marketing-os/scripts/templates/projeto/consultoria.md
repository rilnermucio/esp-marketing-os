---
name: {name}
slug: {slug}
type: consultoria
status: active
current_stage: discovery
default_approval: required
created_at: {created_at}
pipeline:
  - id: discovery
    agent: mos-research
    approval: required
  - id: diagnostico
    agent: mos-analytics
    approval: required
  - id: estrategia
    agent: mos-growth
    approval: required
  - id: deliverable
    agent: mos-copy
    approval: required
---

# Briefing: {name}

## Cliente
[Nome / setor]

## Problema apresentado
[Dor que o cliente trouxe]

## Escopo da consultoria
[O que está incluído]

## Prazo
- Início: {created_at}
- Entrega: [data]

## Notas adicionais
[Detalhes relevantes]
