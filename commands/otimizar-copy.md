---
description: Diagnose, score and rewrite existing copy. Dispatches mos-copy com diagnóstico (PARTE XVIII), Copy Score System (PARTE XV) e reescritas com hipóteses A/B.
argument-hint: "<copy colada, path de arquivo, ou o que otimizar (ex: 'headline da minha landing')>"
---

# /otimizar-copy: Diagnóstico e Reescrita de Copy (Dispatch-Based)

Recebe copy existente (colada na conversa ou em arquivo), diagnostica por que ela não performa e entrega reescritas escoradas com hipóteses de teste. Orquestra via `Agent(subagent_type: "mos-copy")`. Não produz inline.

É o command pro trabalho de copy mais frequente do dia a dia: melhorar o que já existe, em vez de criar do zero.

## Required inputs (ask if missing)

1. **A copy** (obrigatório): texto colado, path de arquivo local, ou transcrição
2. **Formato/canal** (obrigatório): headline, post, anúncio, email, seção de landing, CTA, bio, etc.
3. **Objetivo da peça** (obrigatório): conversão, cliques, engajamento, lead, resposta
4. **Sintoma** (opcional, mas muda o diagnóstico): "CTR baixo", "abre mas não clica", "ninguém responde". Sem sintoma, o diagnóstico é estrutural
5. **Público + oferta** (opcional): contexto que aumenta a precisão da reescrita
6. **Métricas atuais** (opcional): baseline para calibrar hipóteses A/B

## Dispatch

Single message:

```
Agent(subagent_type: "mos-copy", prompt: "Otimize a copy existente abaixo. Formato: [formato]. Objetivo: [objetivo]. Sintoma reportado: [sintoma ou 'nenhum']. Público: [público se informado]. Oferta: [oferta se informada]. Métricas atuais: [baseline ou 'não informadas'].

COPY ORIGINAL:
[copy completa]

Processo obrigatório:
1. Leia PARTE XVIII do knowledge (Diagnóstico de Copy Fraca) e rode o diagnóstico: identifique os 3-5 problemas principais em ordem de impacto (hook, promessa, prova, estrutura, CTA, awareness mismatch)
2. Score a peça original com o Copy Score System (PARTE XV): Clareza, Persuasão, Ação, Relevância, Legibilidade
3. Identifique o nível de consciência real do público (PARTE I, 1.3) e diga se a copy original fala com o nível errado
4. Reescreva: 3-5 variações com hipóteses A/B distintas, cada uma atacando um problema diagnosticado diferente
5. Score cada variação com o mesmo sistema e rode o lint determinístico (scripts/quality_gate.py; headline_scorer.py se for headline)
6. Entregue top 2-3 com: score antes vs depois, o que mudou e por quê, hipótese de teste no formato 'se X então Y porque Z', métrica primária

Aplicar quality gates globais (sem travessão, sem 'brutal', sem antítese negação/afirmação, acentuação PT-BR, máx 1 emoji).")
```

**Escalações** (apenas se necessário):
- Peça de venda high-stakes (sales page, VSL, lançamento) sem research de público: dispatchar `Agent(subagent_type: "mos-research")` ANTES, porque o pre-flight do mos-copy exige research pra esse tipo de peça
- Sintoma é de funil, não de peça ("a página inteira converte mal"): redirecionar pra `/criar-landing-page` ou `Agent(subagent_type: "mos-funnel")`

## Consolidação

Após o agent retornar, entregue:

```markdown
## Otimização de Copy: [formato]

### Diagnóstico (por que a original não performa)
| # | Problema | Impacto | Evidência na peça |
|---|----------|---------|-------------------|
| 1 | [...] | Alto/Médio | "[trecho da copy original]" |

**Score original**: [N]/100 ([breakdown por critério])
**Nível de consciência**: a original fala com [X]; o público real está em [Y]

### Reescritas (top 2-3)

**Variação 1** ([hipótese em 1 linha])
[copy completa pronta pra publicar]
Score: [N]/100 | O que mudou: [...]

**Variação 2** ([hipótese])
[...]

### Plano de teste
| Variação | Hipótese (se X então Y porque Z) | Métrica primária | Amostra mínima |
|----------|----------------------------------|------------------|----------------|

### Próximos passos
- Testar a variação recomendada em [canal]
- Reportar o resultado: o winner entra no swipe file pessoal (workspace/swipe-files/aprovados.md)
- A/B com budget alto em paid media: delegar cálculo de amostra pra mos-ab-testing
```

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Sem `—`, sem "brutal", sem antítese negação→afirmação ("Não é X / É Y"), sem CAPS gratuito
- Acentuação PT-BR correta
- Fact-check via WebSearch para stat/case/citação adicionada na reescrita
- Limites de plataforma do formato (email subject 30-50 chars, X 280, Google Ads 30/90, etc.)

## Por que esse dispatch

Otimizar copy existente é o trabalho mais recorrente de copywriting e usa exatamente as partes mais profundas do `mos-copy`: PARTE XVIII (diagnóstico) e PARTE XV (scoring), que os commands de criação só acionam de forma indireta. Um único dispatch resolve porque diagnóstico, score e reescrita compartilham o mesmo contexto; separar em agents paralelos quebraria o vínculo entre o problema identificado e a solução proposta.
