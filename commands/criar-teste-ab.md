---
description: Design a statistically sound A/B test (hypothesis, sample size, duration, stop criteria). Dispatches mos-ab-testing; sequencial com mos-copy/mos-ads quando as variantes ainda não existem.
argument-hint: "<o que testar + canal + volume, ex: 'CTA da landing, ~800 visitas/dia, baseline 2,1%'>"
---

# /criar-teste-ab: Design de Experimento A/B (Dispatch-Based)

Desenha um teste A/B estatisticamente honesto (hipótese formal, amostra mínima, duração, critério de parada) orquestrando `Agent(subagent_type: "mos-ab-testing")`. Não produz inline. Quando as variantes ainda não existem, a criação delas é etapa sequencial com o agent de domínio.

## Required inputs (ask if missing)

1. **O que testar** (obrigatório): elemento + peça (headline da landing, CTA do email, criativo do anúncio, preço/oferta, thumbnail)
2. **Canal** (obrigatório): landing page, email, Meta/Google Ads, Instagram orgânico, etc.
3. **Métrica primária** (obrigatório): CR, CTR, open rate, CPA, take rate
4. **Volume disponível** (obrigatório pra amostra): tráfego/dia, tamanho da lista ou budget diário
5. **Baseline atual** (opcional, melhora o cálculo): taxa atual da métrica primária
6. **Variantes já existem?** (define o caminho de dispatch abaixo)

## Dispatch Decision Tree

```
Briefing recebido
  ├── Variantes JÁ existem (usuário traz A e B)?
  │     └── Dispatch SIMPLES: mos-ab-testing
  │         (formaliza hipótese, calcula amostra/duração, define parada)
  │
  ├── Variantes NÃO existem?
  │     └── Dispatch SEQUENCIAL: mos-ab-testing (hipótese + dimensão a
  │         variar) → mos-copy (escreve as variantes conforme a hipótese)
  │         [criativo de anúncio pago: mos-ads no lugar de mos-copy]
  │
  └── Teste de preço/oferta?
        └── SEQUENCIAL: mos-offer (desenha as duas arquiteturas) →
            mos-ab-testing (experimento)
```

## Dispatch Simples (variantes existentes)

```
Agent(subagent_type: "mos-ab-testing", prompt: "Desenhe o teste A/B. Elemento: [elemento] em [peça/canal]. Métrica primária: [métrica]. Volume disponível: [tráfego/lista/budget por dia]. Baseline: [taxa atual ou 'desconhecida']. Variante A (controle): [A]. Variante B: [B]. Entregue: hipótese formal (se X então Y porque Z), tamanho mínimo de amostra por variante com as premissas explícitas (baseline, efeito mínimo detectável, poder, significância), duração estimada com o volume dado, critério de parada (sem peeking; quando parar por sucesso, fracasso ou inconclusivo), plano de leitura do resultado e riscos (sazonalidade, contaminação de audiência, novelty effect). Se benchmarks de plataforma forem citados, validar via WebSearch. Aplicar quality gates globais."
)
```

## Dispatch Sequencial (variantes a criar)

```
Passo 1: Agent(subagent_type: "mos-ab-testing", prompt: "Defina a hipótese de maior alavancagem pra testar [elemento] em [peça/canal] com métrica [métrica] e baseline [X]. Use priorização ICE se houver mais de uma dimensão candidata. Entregue: hipótese formal, dimensão única a variar (uma variável por teste), especificação do que a variante B precisa mudar, e o desenho do experimento (amostra, duração, parada) condicionado ao volume [volume].")

Passo 2: Agent(subagent_type: "mos-copy", prompt: "Escreva a variante B para o teste A/B. Controle (A): [peça atual]. Hipótese do experimento: [hipótese do passo 1]. Mude APENAS a dimensão especificada: [dimensão]. Entregue a variante B pronta pra publicar + confirmação de que nada além da dimensão testada mudou. Aplicar quality gates globais.")
```

Criativo de anúncio pago: substituir o passo 2 por `Agent(subagent_type: "mos-ads")` com o mesmo contrato. Teste de preço/oferta: `Agent(subagent_type: "mos-offer")` desenha as duas arquiteturas antes do desenho do experimento.

## Consolidação

Entregue ao usuário:

```markdown
## Teste A/B: [elemento] em [canal]

### Hipótese
Se [mudança X], então [métrica Y melhora em Z%], porque [mecanismo].

### Variantes
| | Conteúdo | O que muda |
|---|---|---|
| A (controle) | [...] | base |
| B | [...] | apenas [dimensão testada] |

### Desenho estatístico
- Amostra mínima por variante: [N] (premissas: baseline [X]%, MDE [Y]%, poder 80%, significância 95%)
- Duração estimada: [dias] com o volume atual
- Critério de parada: [regra explícita; sem espiar resultado antes da amostra]

### Plano de leitura
- Se B vence: [ação + registrar winner na memory do agent de domínio]
- Se inconclusivo: [ação: rodar mais tempo até teto de X dias ou descartar]
- Riscos: [sazonalidade, contaminação, novelty effect quando aplicável]

### Próximos passos
- Implementar as variantes em [ferramenta do canal]
- Reportar o resultado: winner alimenta o swipe file pessoal e a memory
```

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Uma variável por teste (mudou mais de uma dimensão = refazer o desenho)
- Amostra calculada ANTES de rodar; teste sem amostra mínima declarada não sai
- Benchmark de plataforma citado passa por fact-check via WebSearch
- Sem `—`, sem "brutal", sem antítese negação→afirmação, acentos PT-BR

## Por que esse dispatch

Desenho de experimento e criação de variante são competências distintas que se contaminam quando feitas juntas: quem escreve a variante tende a mudar três coisas ao mesmo tempo e invalidar a leitura. O `mos-ab-testing` fixa a hipótese e a dimensão única primeiro; o agent de domínio (copy/ads/offer) cria dentro dessa restrição; e o desenho estatístico impede o erro mais caro de teste A/B em budget alto, que é declarar vencedor sem amostra.
