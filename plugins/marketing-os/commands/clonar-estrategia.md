---
description: Analyze a competitor/expert and reverse-engineer their content strategy adapted for your brand. Dispatches workflow #10 (mos-research + mos-brand → mos-copy with voice clone extraction).
argument-hint: "<profile or brand, e.g., '@hormozi Instagram strategy' or 'concorrente.com content analysis'>"
---

# /clonar-estrategia: Análise + Clone de Estratégia (Workflow #10)

Engenharia reversa de estratégia de concorrente/expert conforme **workflow #10** em `skills/marketing-os/SKILL.md`.

## Required inputs (ask if missing)

1. **Alvo** (obrigatório): @profile ou URL do concorrente/expert
2. **Sua marca/contexto** (obrigatório): pra adaptar o que for replicável
3. **Foco da análise** (obrigatório): conteúdo orgânico | ads | funil de vendas | posicionamento | copy
4. **Profundidade** (obrigatório): rápida (visão geral) | profunda (frameworks específicos)

## Dispatch, Fase 1 (paralelo, single message)

```
- Agent(subagent_type: "mos-research", prompt: "Mapeamento completo de [alvo]: produtos vendidos + ticket, posicionamento (Schwartz nível, big idea), fontes de tráfego ativas, conteúdo orgânico (frequência/formatos/temas), ads ativos (Meta/Google ad library), depoimentos públicos, autoridade construída. WebSearch + análise de perfis públicos. Considere memory existente do cliente neste projeto.")

- Agent(subagent_type: "mos-brand", prompt: "Extrair positioning, arquétipo, voz/tom de [alvo] a partir de samples reais (posts, lives, ads). Gerar brand spec replicável: arquétipo principal, sub-arquétipos, voz, tom, valores comunicados, vocabulário recorrente. Comparar com [sua marca] e identificar gaps/oportunidades. Considere memory existente do cliente neste projeto.")
```

## Fase 2 (sequencial, depende dos outputs da Fase 1)

```
- Agent(subagent_type: "mos-copy", prompt: "Voice clone de [alvo]: extrair padrões de copy a partir do mapeamento da Fase 1: estruturas de headline, padrões de CTA, vocabulário distintivo, ritmo de frase, gatilhos emocionais usados, framework de prova social. SE [alvo] é copywriter conhecido (Halbert, Hopkins, Sugarman, etc.), referenciar perfil em assets/clones/. Gerar 3-5 samples adaptados pra [sua marca/avatar/produto]. Considere memory existente do cliente neste projeto.")
```

## Fase 3: Brief Consolidado de Estratégia Clonada

Saída final:

```markdown
## Análise Reversa: [Alvo]

### Mapeamento (mos-research)
**Produtos:** [lista + ticket]
**Posicionamento:** [Schwartz nível X, big idea, mecanismo único]
**Tráfego:** [orgânico %, ads %, parcerias %, etc.]
**Conteúdo:** [frequência/formatos/temas dominantes]
**Ads ativos:** [exemplos da ad library]
**Autoridade:** [como construiu, credenciais, depoimentos, mídia]

### Brand Spec Extraído (mos-brand)
**Arquétipo:** [principal + sub-arquétipos]
**Voz:** [adjetivos descritivos]
**Tom:** [como soa em prática]
**Valores comunicados:** [lista]
**Vocabulário:** [palavras-chave distintivas]

### Padrões de Copy (mos-copy + voice clone)
**Headlines:** [estruturas recorrentes]
**CTAs:** [padrões + verbos]
**Hooks:** [tipos usados]
**Framework de prova social:** [como apresenta cases/depoimentos]

### Samples adaptados pra [sua marca]
[3-5 peças no estilo extraído mas com sua voz/produto]

## Checklist: o que replicar / evitar / diferenciar

**Replicar (compatível com sua marca):**
- [item]
- [item]

**Evitar (não cabe pra você):**
- [item]
- [item]

**Diferenciar (oportunidades onde [alvo] é fraco):**
- [item]
- [item]
```

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Sem `—`, sem "brutal", sem CAPS gratuito
- Acentuação PT-BR correta
- Não usar nada que viole IP do concorrente (ideias e frameworks são ok; copy literal não)
- Compliance regulatório por nicho
- Verificar fatos citados via WebSearch (CONFIRMADO/PROVÁVEL)
- Adaptar pra avatar/produto da marca atual, não copiar cego

## Por que essa orquestração

Clone sem `mos-research` é cópia rasa (só pega headlines visíveis). Sem `mos-brand` é só pegar peças (sem entender o posicionamento que faz funcionar). Sem `mos-copy` é análise sem aplicação prática. Os 3 juntos = engenharia reversa que vira playbook acionável.

## Related commands

- `/analisar-concorrencia`: análise mais focada em conteúdo/SEO
- `/analisar-video`: análise focada em 1 vídeo específico
- `/criar-clone`: cria clone de copywriter externo (Halbert, Hopkins, etc.) via web research
- `/criar-meu-clone`: clone da SUA voz via amostras locais
