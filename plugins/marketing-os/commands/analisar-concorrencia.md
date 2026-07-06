---
description: Analyze competitors extracting positioning, content strategy, audience insights, gaps and SWOT. Dispatches mos-research + mos-brand in parallel, with optional mos-copy handoff for replicable hooks/CTAs.
argument-hint: "<competitors or niche, e.g., '@competitor1 @competitor2' or 'fitness coaching niche'>"
---

# /analisar-concorrencia: Análise Competitiva (Dispatch paralelo)

Análise multi-dimensional de concorrentes despachando subagents em paralelo. Não produz análise inline.

## Required inputs (ask if missing)

1. **Concorrentes** (obrigatório): 2-5 contas/marcas específicas OU nicho a pesquisar
2. **Plataformas** (opcional): Instagram, LinkedIn, TikTok, YouTube (default: todas onde os concorrentes atuam)
3. **Profundidade** (opcional): quick overview, standard, comprehensive (default: standard)
4. **Focus areas** (opcional): content, engagement, positioning, audience, all (default: all)
5. **Sua marca** (opcional, recomendado): contexto da sua marca para benchmarking lado a lado
6. **Output bonus** (opcional): se quer hooks/CTAs replicáveis prontos para reuso (dispara handoff pra `mos-copy`)

## Dispatch (paralelo, single message)

Em **um único message**, dispare os 2 agents-base em paralelo:

```
- Agent(subagent_type: "mos-research", prompt: "Análise competitiva de [lista de concorrentes ou nicho] em [plataformas]. Profundidade: [profundidade]. Para cada concorrente: overview (followers, post freq, engajamento médio), métricas (engagement rate, comment ratio, save rate, share rate, growth rate), top performing content (3-5 posts/vídeos com hipótese de por que funcionou), audience analysis (perfis nos comentários, dores, perguntas, sentimento), content pillars e formatos dominantes. Considere memory existente do cliente neste projeto.")

- Agent(subagent_type: "mos-brand", prompt: "Análise de positioning de [lista de concorrentes]: UVP, arquétipo, voz/tom, identidade visual, sinais de credibilidade, faixa de preço/posicionamento, diferenciação aparente. Compare com a marca do user [contexto da marca, se fornecido]. Entregue framework SWOT por concorrente + matriz comparativa lado a lado. Considere memory existente do cliente neste projeto.")
```

### Handoff opcional (sequencial, depois das duas calls acima)

Se o user pediu hooks/CTAs replicáveis:

```
Passo 3 (depois de receber mos-research + mos-brand):
Agent(subagent_type: "mos-copy", prompt: "A partir do output [colar trechos relevantes de mos-research sobre top posts + mos-brand sobre voz dos concorrentes], extraia padrões de copy replicáveis: 5-10 hooks com variações adaptadas pra marca do user, 5-10 CTAs catalogados por intenção, 3-5 estruturas de copy comuns. Inclua nota de o-que-replicar / o-que-evitar / oportunidade de diferenciação. Aplique quality gates globais. Considere memory existente do cliente neste projeto.")
```

## Consolidação

Após os agents retornarem:

```markdown
## Análise Competitiva: [nicho ou lista]

Concorrentes analisados: [N] | Plataformas: [lista] | Data: [data]

### Resumo Executivo
- Top 3 insights: [bullet 1, 2, 3]
- Maior oportunidade identificada: [descrição]
- Recomendação principal: [ação prioritária]

### Concorrente 1: [@handle]
**Overview:** seguidores [N], freq [N/sem], engagement rate [X%]
**Positioning:** [2-3 frases]
**Content strategy:** pilares + formatos + horários
**O que funciona:** [3-5 pontos]
**Gaps/fraquezas:** [3-5 pontos]
**Top posts:** [3 com métricas]

### Concorrente 2-N
[Mesma estrutura]

### Comparativo lado a lado
| Métrica | Comp 1 | Comp 2 | Comp 3 | Sua marca | Benchmark nicho |
|---------|--------|--------|--------|-----------|-----------------|
| Followers | ... | ... | ... | ... | ... |
| Engagement rate | ... | ... | ... | ... | ... |
| Post freq | ... | ... | ... | ... | ... |

### SWOT por concorrente (de mos-brand)
[Tabela ou bloco por concorrente]

### Gaps de mercado e oportunidades
- Conteúdos que ninguém faz: [lista com nível de oportunidade]
- Ângulos de positioning não ocupados: [lista]
- Necessidades da audiência não atendidas: [lista]

### Diferenciação sugerida (de mos-brand)
[Como sua marca pode ocupar território único]

### Hooks e CTAs replicáveis (de mos-copy, se Fase 3 rodou)
- Hooks que funcionam no nicho (com adaptação pra sua marca)
- CTAs catalogados por intenção
- O-que-replicar / o-que-evitar / oportunidade de diferenciação

### Plano de ação (priorizado)
| Prioridade | Ação | Timeline | Impacto esperado |
|------------|------|----------|------------------|
| Alta | ... | ... | ... |
```

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Sem `—`, sem "brutal", sem CAPS gratuito, sem aspas em falas
- Acentuação PT-BR correta
- Métricas citadas devem ser verificáveis (CONFIRMADO via fonte primária ou PROVÁVEL com indicação)
- Não inventar números, quando o agent não conseguir extrair, marcar "não disponível" ou "estimativa"
- Compliance regulatório se nicho saúde/finanças/suplementos (analisar concorrentes não escapa do disclaimer pro user)

## Follow-up

Pergunte se quer:
1. Deep dive em concorrente específico
2. Plano de diferenciação detalhado a partir dos gaps
3. Calendário editorial pra ocupar gaps identificados
4. Benchmark periódico (rodar análise mensal/trimestral)

## Por que esse dispatch composto

Análise competitiva sem `mos-research` = sem dados de performance, vira opinião. Sem `mos-brand` = só métrica, sem entender posicionamento e por que cada concorrente atrai quem atrai. `mos-copy` no handoff opcional fecha o ciclo: análise vira biblioteca de hooks/CTAs adaptados, não relatório engavetado.
