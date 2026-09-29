---
description: Cria um dossiê completo do cliente ideal com pesquisa, evidências, JTBD, anti-avatar e handoff para execução de marketing.
argument-hint: "<produto ou oferta> <nicho> [B2B|B2C] [mercado ou região]"
---

# /criar-avatar: Dossiê de Avatar Baseado em Evidências

Cria o avatar de cliente que servirá como fonte de verdade para copy, anúncios, oferta, funil e conteúdo. A execução pesquisa e sintetiza; não preenche lacunas com estereótipos.

## Required inputs (ask if missing)

1. **Produto ou oferta** (obrigatório): o que será vendido, formato, ticket ou faixa de preço e transformação prometida.
2. **Mercado e geografia** (obrigatório): nicho, país, região ou idioma relevante.
3. **Contexto de compra** (obrigatório): B2B ou B2C; quem usa, quem compra e quem influencia, se já souber.
4. **Decisão que o avatar alimentará** (obrigatório): copy, campanha, oferta, funil, conteúdo, posicionamento ou validação.
5. **Evidências próprias disponíveis** (opcional): entrevistas, CRM, tickets de suporte, reviews, métricas, gravações de vendas, pesquisas e base de clientes.
6. **Público ou segmentos suspeitos** (opcional): hipóteses iniciais que precisam ser verificadas.
7. **Profundidade** (opcional): rápida, padrão ou profunda. Default: padrão.

Se faltarem produto/oferta, mercado/geografia ou decisão, faça no máximo 3 perguntas objetivas antes do dispatch. Dados demográficos desconhecidos não bloqueiam: devem permanecer como hipótese ou ser omitidos quando não afetam a compra.

## Dispatch Decision Tree

```text
Briefing recebido
  ├── Há dados próprios do cliente?
  │     └── Usar como evidência primária e triangular com fontes externas
  ├── Contexto B2B?
  │     └── Incluir ICP, usuário, comprador econômico, influenciadores e comitê
  ├── Contexto B2C?
  │     └── Incluir pessoa compradora, contexto doméstico e influenciadores
  └── Segmentos ainda incertos?
        └── Comparar candidatos e escolher o principal pela força das evidências
```

Todos os caminhos usam dispatch simples para `mos-research`. Os ramos alteram o conteúdo do dossiê, sem trocar o especialista.

## Dispatch Simples

```text
Agent(subagent_type: "marketing-os:mos-research", prompt: "Crie um Dossiê de Avatar completo para [produto ou oferta], no mercado [nicho e geografia], contexto [B2B ou B2C], para orientar a decisão [decisão]. Ticket ou faixa de preço: [ticket]. Transformação prometida: [transformação]. Evidências próprias fornecidas: [dados, links ou nenhuma]. Segmentos suspeitos: [lista ou nenhum]. Profundidade: [rápida, padrão ou profunda]. Considere a memory existente do cliente neste projeto, se estiver ativa. Leia a seção Audience Research Profundo de ${CLAUDE_PLUGIN_ROOT}/subagents/research-agent.md, consulte ${CLAUDE_PLUGIN_ROOT}/assets/personas/personas-por-nicho.md apenas como banco de hipóteses e siga integralmente o contrato canônico de ${CLAUDE_PLUGIN_ROOT}/assets/personas/persona-template.md. Use WebSearch para evidências externas atuais e priorize fontes primárias, dados próprios, reviews, fóruns e linguagem espontânea do público. Para toda afirmação material, registre fonte, data, escopo geográfico, classificação EVIDÊNCIA CONFIRMADA, INFERÊNCIA ou HIPÓTESE e confiança alta, média ou baixa. Entregue: ledger de evidências; segmentação e priorização; um avatar principal; segmentos secundários somente quando houver diferença comprovada de job, jornada ou decisão; anti-avatar; Jobs To Be Done funcional, emocional e social; nível de consciência; dores, desejos, alternativas atuais, objeções, critérios, gatilhos e jornada de compra; canais, formatos e linguagem real; diferenças B2B ou B2C; plano de validação; recomendações acionáveis; Handoff Context em JSON para mos-copy, mos-ads, mos-offer, mos-funnel e mos-social. Declare limitações. Não invente demografia, citações, comportamento, renda ou disposição a pagar. Aplique os Quality Gates globais do Marketing OS.")
```

## Consolidação

Entregue o resultado final neste schema, removendo blocos realmente inaplicáveis e explicando a remoção:

````markdown
# Dossiê de Avatar: [Produto ou Oferta]

## 1. Metadata e escopo
- Data da pesquisa: [YYYY-MM-DD]
- Mercado e geografia: [...]
- Contexto: [B2B | B2C]
- Decisão atendida: [...]
- Profundidade: [rápida | padrão | profunda]
- Maturidade: [exploratório | validado | operacional]
- Limitações: [...]

## 2. Resumo executivo
- Segmento prioritário: [...]
- Job central: [...]
- Problema mais urgente: [...]
- Motivo para agir agora: [...]
- Maior risco de erro no avatar: [...]

## 3. Protocolo de evidências
| ID | Afirmação | Classe | Confiança | Fonte e data | Implicação |
|---|---|---|---|---|---|
| E01 | [...] | EVIDÊNCIA CONFIRMADA | alta | [...] | [...] |
| I01 | [...] | INFERÊNCIA | média | deriva de E01 + E02 | [...] |
| H01 | [...] | HIPÓTESE | baixa | validação pendente | [...] |

## 4. Segmentação e priorização
| Segmento candidato | Job distinto | Fit com a oferta | Urgência | Capacidade de compra | Acessibilidade | Força das evidências | Decisão |
|---|---|---:|---:|---:|---:|---:|---|
| [...] | [...] | [...] | [...] | [...] | [...] | [...] | principal, secundário ou descartado |

## 5. Avatar principal
[Acrescente `[E##]`, `[I##]` ou `[H##]` a cada afirmação material.]

### Identificação funcional e contexto
### Perfil profissional ou doméstico relevante
### Valores, crenças e identidade
### Jobs To Be Done
### Dores e consequências
### Desejos e critérios de sucesso
### Alternativas atuais e histórico de tentativas
### Objeções, medos e riscos percebidos
### Critérios e processo de decisão
### Gatilhos e momento de necessidade
### Nível de consciência
### Jornada de compra
### Canais, formatos e comportamento de pesquisa
### Linguagem real

## 6. Contexto B2B ou B2C
- Usuário: [...]
- Comprador econômico: [...]
- Influenciadores e bloqueadores: [...]
- Comitê ou contexto familiar: [...]
- Ciclo e restrições da decisão: [...]

## 7. Segmentos secundários
[Incluir apenas segmentos sustentados por evidências e explicar o que muda no job, na mensagem ou na jornada. Caso contrário: nenhum segmento secundário validado.]

## 8. Anti-avatar
- Critérios objetivos de exclusão: [...]
- Sinais de desqualificação: [...]
- Motivo do baixo fit: [...]
- Alternativa mais adequada: [...]

## 9. Implicações para marketing
- Promessa e ângulos permitidos: [...]
- Mensagens a evitar: [...]
- Provas necessárias: [...]
- Canais e formatos prioritários: [...]
- Perguntas e temas de conteúdo: [...]

## 10. Plano de validação
| Hipótese | Método | Amostra ou fonte | Sinal de confirmação | Prioridade |
|---|---|---|---|---|
| H01 | [...] | [...] | [...] | alta |

## 11. Handoff Context
```json
{
  "avatar_version": "1.0",
  "primary_segment": "...",
  "secondary_segments": [],
  "anti_avatar": ["..."],
  "jobs_to_be_done": {
    "functional": ["..."],
    "emotional": ["..."],
    "social": ["..."]
  },
  "awareness_level": "...",
  "top_pains": ["..."],
  "top_desires": ["..."],
  "objections": ["..."],
  "purchase_triggers": ["..."],
  "decision_criteria": ["..."],
  "real_language": [
    {"excerpt": "...", "source_id": "E01"}
  ],
  "evidence_ids": ["E01"],
  "open_hypotheses": ["H01"],
  "handoffs": {
    "mos-copy": ["promessa", "dor", "desejo", "objeção", "linguagem"],
    "mos-ads": ["segmento", "gatilho", "canal", "ângulo"],
    "mos-offer": ["job", "alternativa", "critério", "risco percebido"],
    "mos-funnel": ["consciência", "jornada", "fricção", "prova"],
    "mos-social": ["tema", "pergunta", "formato", "vocabulário"]
  }
}
```

## 12. Fontes
1. [Título, organização ou autor, URL, publicação, acesso e contexto geográfico]
````

## Quality Gates (antes de entregar)

- Toda afirmação material aponta para um ID do ledger ou está rotulada como hipótese.
- Evidência confirmada usa dado próprio confiável ou triangulação de fontes independentes.
- Inferências explicam de quais evidências derivam.
- Hipóteses entram no plano de validação e nunca viram fato por repetição.
- Citações de linguagem real preservam sentido, têm fonte e são curtas.
- Dados antigos, globais ou de outra região recebem alerta de aplicabilidade.
- Demografia só entra quando influencia aquisição, uso ou compra.
- Segmentos secundários exigem diferença acionável; nomes decorativos são removidos.
- O anti-avatar usa critérios de fit e elegibilidade, sem caricaturas ou discriminação.
- Aplicar os Quality Gates globais de `${CLAUDE_PLUGIN_ROOT}/skills/marketing-os/SKILL.md`.

## Por que esse dispatch

Avatar é um problema de pesquisa e síntese. O `mos-research` já possui WebSearch, triangulação, Audience Research e JTBD, então um dispatch simples preserva uma única cadeia de evidências. O handoff estruturado permite que os agents de execução consumam o mesmo diagnóstico depois, sem refazer o avatar ou introduzir versões conflitantes.
