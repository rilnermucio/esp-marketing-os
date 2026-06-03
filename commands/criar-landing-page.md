---
description: Create a complete landing page (BOFU), hero, benefits, social proof, offer, CTA. Dispatches mos-funnel + mos-copy + mos-design in parallel (workflow #5), with optional handoff to frontend-design for HTML/CSS build.
argument-hint: "<product/offer and avatar, e.g., 'mentoria médica high-ticket pra Dr. Victor'>"
---

# /criar-landing-page: Landing Page BOFU (Workflow #5)

Cria página de aplicação / landing page / página de vendas conforme **workflow #5** em `skills/marketing-os/SKILL.md`.

**REGRA CRÍTICA:** marketing-os reivindica esse território. NÃO delegue direto a `frontend-design` sem antes orquestrar a camada estratégica.

## Required inputs (ask if missing)

1. **Produto/Oferta** (obrigatório): nome, ticket, formato (curso/mentoria/serviço)
2. **Avatar** (obrigatório): cargo, faixa de renda, dor principal
3. **Tipo de página** (obrigatório): aplicação (formulário + call) | vendas direta (checkout) | captura (lead magnet)
4. **Nicho** (obrigatório): saúde, finanças, tech, etc., define disclaimers regulatórios
5. **Copy fornecida** (opcional): se houver PDF/DOCX existente, anexar pra revisão
6. **Buildar HTML/CSS?** (opcional): sim = handoff a `frontend-design` na Fase 2; não = só specs

## Dispatch, Fase 1 (paralelo, single message)

```
- Agent(subagent_type: "mos-funnel", prompt: "Estruturar página BOFU para [produto/avatar/ticket]: CTA placement, escassez, anti-avatar, FAQ, prova social, stack value, hierarquia de seções. Tipo: [aplicação/vendas/captura]. Considere memory existente do cliente neste projeto.")

- Agent(subagent_type: "mos-copy", prompt: "[Se copy fornecida: revisar/melhorar: colar conteúdo do PDF]. [Senão: gerar copy do zero pra produto X, avatar Y]. Considere memory existente do cliente neste projeto. Aplicar quality gates globais. Sugerir variações de headline/CTA.")

- Agent(subagent_type: "mos-design", prompt: "Direção visual para página BOFU em [nicho]: paleta (premium/médica/tech/etc.), tipografia, hierarquia visual, mood, exemplos de referência. Ticket: [low/mid/high]. Tom: profissional/acolhedor/etc. Considere memory existente do cliente neste projeto.")
```

## Fase 2 (sequencial, depende dos outputs da Fase 1)

Consolidar os 3 outputs num **brief único**:

```markdown
## Brief Consolidado: Landing Page [Produto]

### Estrutura (mos-funnel)
[Hierarquia de seções + CTA placement + anti-avatar + FAQ]

### Copy (mos-copy)
[Headlines + body + CTAs + variações A/B + disclaimers regulatórios]

### Design Spec (mos-design)
[Paleta + tipografia + hierarquia + mood + componentes-chave]
```

**Decisão:**
- SE user pediu HTML/CSS de fato → delegar à skill `frontend-design` (plugin oficial Anthropic) com o brief consolidado como input
- SE user pediu só specs → entregar o brief e parar aqui

## Fase 3: Quality Gates + Compliance

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Sem `—`, sem "brutal", PT-BR correto, sem placeholders publicados
- Gates de substância: promessas com backup, garantia clara, sem linguagem absoluta
- Compliance regulatório (auto-aplicado por nicho):
  - Saúde: CRM visível + "resultados variam" + sem "cura"
  - Finanças: "rentabilidade passada não garante futura"
  - Suplementos: "auxilia/contribui" (sem prometer cura)

## Sugestões opcionais (perguntar ao user no fim)

- Setup de teste A/B em headline + CTA (mos-ab-testing)
- Tracking de eventos pra GA4/Meta Pixel (mos-analytics)
- Sequência de email pós-formulário (mos-email)

## Por que essa ordem importa

- Sem `mos-funnel`: estrutura sai genérica sem padrões BOFU (escassez, anti-avatar, stack value)
- Sem `mos-copy`: copy não passa pelos quality gates, oportunidade de melhoria perdida
- Sem `mos-design`: visual sai com cara de template genérico, não de nicho premium
- `frontend-design` é excelente em build técnico, mas não conhece padrões de conversão, é executor da Fase 2, não decisor da Fase 1
