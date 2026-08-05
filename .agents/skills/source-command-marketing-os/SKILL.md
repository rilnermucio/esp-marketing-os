---
name: "source-command-marketing-os"
description: "Adaptador de compatibilidade para o Marketing OS. Use para produção e estratégia de marketing, incluindo conteúdo, copy, SEO, anúncios, email, vídeo, funis, lançamentos, oferta, USP, avatar, marca, pesquisa, design e testes. Triggers explícitos: /criar-oferta, /criar-usp e /criar-avatar."
---

# Marketing OS: adaptador do source command

Esta skill preserva compatibilidade com o source command migrado `marketing-os`.
A fonte canônica de agentes, roteamento, workflows, quality gates e commands é:

`skills/marketing-os/SKILL.md`

## Contrato de execução

1. Leia `skills/marketing-os/SKILL.md` integralmente antes de decidir a rota.
2. Trate o mapa de dispatch, os desempates e os workflows desse arquivo como
   fonte de verdade.
3. Quando o usuário invocar um command explícito, leia também
   `commands/<nome-do-command>.md` e siga seu decision tree e output schema.
4. Pedidos de produção passam pelos agents `mos-*` definidos pela skill
   canônica. Perguntas conceituais sobre marketing ou sobre o próprio sistema
   podem ser respondidas inline conforme o protocolo canônico.
5. Aplique os Quality Gates globais antes de entregar qualquer output.

## Entradas estratégicas recentes

- `/criar-avatar`: pesquisa e Dossiê de Avatar baseado em evidências.
- `/criar-usp`: proposta central, diferenciação, reason to believe e limites.
- `/criar-oferta`: promessa comercial, value stack, preço, garantia, urgência,
  evidências, validação e handoff.

Não replique aqui inventários, contagens ou tabelas de agentes. Essa informação
permanece exclusivamente na fonte canônica para evitar drift.
