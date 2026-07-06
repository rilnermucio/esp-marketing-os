---
description: Create complete podcast episode scripts (solo, interview, co-hosted, storytelling, panel) with intros, segments, show notes and promo content. Dispatches mos-audio simples ou mos-research → mos-audio sequencial para entrevistas.
argument-hint: "<format and topic, e.g., 'interview about productivity' or 'solo episode on marketing trends'>"
---

# /criar-podcast: Roteiro de Podcast (Dispatch-Based)

Cria roteiro completo de episódio orquestrando subagent(s) especializados via `Agent(subagent_type: "mos-*")`. Não produz inline.

## Required inputs (ask if missing)

1. **Formato** (obrigatório): solo, interview, co-hosted, storytelling ou panel
2. **Tópico** (obrigatório): assunto principal do episódio
3. **Duração** (opcional): 15, 30, 45 ou 60+ minutos (default 30)
4. **Guest info** (obrigatório se interview): nome, credenciais, contexto, áreas de expertise, pontos polêmicos
5. **Audiência** (opcional): perfil de quem ouve o show
6. **Show name** (opcional): para intros/outros personalizados
7. **Tom** (opcional): educativo, conversacional, entertainer, profissional

## Dispatch Decision Tree

```
Briefing recebido
  ├── Solo / co-hosted / storytelling / panel?
  │     └── Dispatch SIMPLES: mos-audio
  │
  ├── Interview com guest específico?
  │     └── Dispatch SEQUENCIAL:
  │         1. mos-research (research do guest + tópico)
  │         2. mos-audio (script com perguntas baseadas no research)
  │
  └── Episódio recorrente (série) com formato já definido?
        └── Dispatch SIMPLES: mos-audio (com referência ao formato da série)
```

`mos-audio` não tem memory persistente, passe todos os inputs no prompt.

## Dispatch Simples (solo, co-hosted, storytelling, panel)

```
Agent(subagent_type: "mos-audio", prompt: "Roteiro completo de episódio [solo | co-hosted | storytelling | panel] sobre [tópico]. Show: [show name]. Duração-alvo: [N] minutos. Audiência: [audiência]. Tom: [tom]. Entregue: estrutura por timestamps (intro com hook + show intro + episode setup, segments com talking points e takeaways, ad breaks se aplicável, outro com summary + CTA + tease + sign-off), 3 opções de título de episódio, 3 social media clips (timestamp + hook), show notes completas (descrição SEO, key takeaways, timestamps, resources mencionados, CTA), copy promocional (Instagram caption + email teaser + Twitter thread). Aplicar quality gates globais (sem travessão, sem 'brutal', sem aspas em falas — escreva direto, PT-BR correto).")
```

## Dispatch Sequencial (interview)

### Passo 1, Research do guest

```
Agent(subagent_type: "mos-research", prompt: "Research profundo sobre guest [nome do guest] para entrevista de podcast sobre [tópico]. Considere memory existente do projeto. Entregue: bio e credenciais verificadas, trajetória profissional (origem, momentos-chave, pivôs), trabalhos/produtos atuais, principais ideias e teses defendidas, histórias e cases que o guest costuma contar, posições polêmicas ou contrarian, gaps no que ele já abordou em outras entrevistas (ângulos novos), 3-5 stats/estudos relevantes do tópico, conexão com a audiência [audiência]. Fact-check tudo (CONFIRMADO/PROVÁVEL/NÃO USAR).")

→ Aguarde research brief antes do passo 2.
```

### Passo 2, Script da entrevista

```
Agent(subagent_type: "mos-audio", prompt: "Roteiro completo de entrevista para podcast sobre [tópico]. Show: [show name]. Duração-alvo: [N] minutos. Guest: [nome]. Use este research como base [colar research brief do passo 1]. Entregue: estrutura por timestamps (pre-interview com hook + show intro + apresentação do guest + setup, opening questions 5-10min com background/journey, core questions 20-40min com 3-5 deep-dives + follow-ups + storytelling prompts + perguntas contrarian baseadas em pontos polêmicos do research, rapid-fire 5-10min, closing questions com best advice + recursos + onde encontrar guest, outro com thanks + insights + CTA), 3 opções de título de episódio, 3 social media clips (timestamp + hook + quote), show notes completas (descrição SEO, key takeaways, timestamps, resources do guest, CONNECT WITH GUEST com handles, sponsors), copy promocional (caption Instagram + email teaser + Twitter thread). Aplicar quality gates globais (sem travessão, sem 'brutal', sem aspas em falas — escreva direto, PT-BR correto).")
```

## Consolidação

Após os agents retornarem, entregue:

```markdown
## Podcast: [Show]: Episódio: [Título]

Formato: [solo | interview | co-hosted | storytelling | panel] | Duração-alvo: [N] min | Tópico: [tópico]

### Guest Brief (se interview, de mos-research)
- Bio + credenciais verificadas: [...]
- Trajetória + momentos-chave: [...]
- Teses principais e posições contrarian: [...]
- Gaps em entrevistas anteriores (ângulos novos): [...]
- Stats e estudos relevantes (CONFIRMADO/PROVÁVEL): [...]

### Episode Overview
- Goal: [o que o ouvinte deve aprender/sentir/fazer]
- Audiência: [...]

### Pre-Production Notes
[Equipamento + guest prep + facts a verificar]

### Script (timestamps)

#### Intro [0:00 - X:XX]
[Hook + show intro + episode setup, sem aspas, falas escritas direto]

#### Segment 1 / Opening Questions [X:XX - X:XX]
[Talking points / perguntas com follow-ups]

#### Segment 2 / Core Questions [X:XX - X:XX]
[Deep-dives + perguntas contrarian baseadas em research]

#### [Ad Break, se aplicável]
[Roteiro do ad-read]

#### Segment 3 / Rapid-Fire [X:XX - X:XX]
[...]

#### Closing / Outro [X:XX - X:XX]
[Summary + CTA + tease + sign-off]

### Episode Title Options (3)
1. [...]
2. [...]
3. [...]

### Social Media Clips (3)
- Clip 1: timestamp [X:XX - X:XX]: hook: [...]
- Clip 2: timestamp [X:XX - X:XX]: hook: [...]
- Clip 3: timestamp [X:XX - X:XX]: hook: [...]

### Show Notes
- Descrição SEO (150-300 palavras): [...]
- Key takeaways (5): [...]
- Timestamps: [...]
- Resources mencionados: [...]
- Connect with guest (se interview): [...]
- Sponsors: [...]

### Promo Copy
- Instagram caption: [...]
- Email teaser: [...]
- Twitter thread (3-5 tweets): [...]

### Próximos passos
- Roteiros de ad-read pra sponsors
- Série de episódios derivada deste tópico
- Versão YouTube/vídeo do episódio
```

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Sem `—`, sem "brutal", sem CAPS gratuito
- **Sem aspas em falas/roteiros** (escrever direto)
- Acentuação PT-BR correta
- Fact-check via WebSearch para todo claim/stat/citação atribuída ao guest (CONFIRMADO/PROVÁVEL/NÃO USAR)
- Compliance regulatório se nicho saúde/finanças/suplementos
- Show notes com SEO (keyword do tópico no título e primeiros 150 chars)

## Por que esse dispatch

Solo/co-hosted/storytelling/panel: `mos-audio` tem knowledge profunda de estrutura de episódio, hook formulas, transições, ad-reads, show notes. Sozinho entrega tudo. Interview é diferente: a qualidade da entrevista mora nas perguntas, e perguntas boas exigem research real do guest (gaps, polêmicas, ângulos novos). Por isso o `mos-research` vai antes, não em paralelo, porque o `mos-audio` precisa do output dele pra construir o questionário.
