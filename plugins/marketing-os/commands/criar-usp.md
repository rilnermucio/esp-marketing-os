---
description: "Cria USP e proposta de valor com evidências, diferenciação competitiva e reason to believe. Use quando pedirem USP, diferencial, proposta de valor ou posicionamento da oferta."
argument-hint: "<produto ou oferta> <público> [categoria ou mercado] [geografia]"
---

# /criar-usp: Proposta Única de Venda Baseada em Evidências

Cria a proposta central que explica para quem a oferta serve, qual progresso entrega, por que merece preferência e quais provas sustentam essa escolha. O resultado prioriza uma USP principal e registra claramente os pontos ainda exploratórios.

## Required inputs (ask if missing)

1. **Produto, serviço ou oferta** (obrigatório): o que será vendido, formato, ticket ou faixa de preço e entrega principal.
2. **Público e Job To Be Done** (obrigatório): quem compra, situação que dispara a busca e progresso desejado. Um Dossiê de Avatar pode ser usado como fonte.
3. **Categoria e mercado** (obrigatório): como o cliente enquadra a solução, geografia e contexto B2B ou B2C.
4. **Decisão atendida** (obrigatório): posicionamento da oferta, hero de página, pitch, anúncio, lançamento ou alinhamento interno.
5. **Alternativas e concorrentes** (opcional): 2 a 5 opções que o cliente compara, incluindo fazer sozinho, adiar ou manter a solução atual.
6. **Mecanismo ou diferencial real** (opcional): capacidade, processo, ativo, modelo ou experiência que muda o resultado para o cliente.
7. **Provas disponíveis** (opcional): dados próprios, demonstrações, cases verificáveis, certificações, tecnologia, propriedade intelectual, processo ou histórico operacional.
8. **Research existente** (opcional): avatar, entrevistas, reviews, análise competitiva, tickets de suporte ou links.

Se faltarem produto, público ou decisão, faça no máximo 3 perguntas objetivas antes do dispatch. A ausência de concorrentes, diferencial ou provas aciona pesquisa e mantém candidatos não comprovados como hipótese.

## Distinção do entregável

- **USP**: uma proposta central de venda para uma oferta ou produto específico.
- **UVP**: arquitetura mais ampla de valor da marca ou portfólio.
- **Posicionamento**: lugar que a marca pretende ocupar em relação às alternativas.
- **Tagline ou slogan**: expressão verbal curta criada depois que a proposta foi validada.

Quando o pedido vier como UVP corporativa, entregue a UVP principal e derive a USP da oferta prioritária. O command continua usando o mesmo contrato de evidência e validação.

## Dispatch Decision Tree

```text
Briefing recebido
  ├── Público/JTBD validado + alternativas mapeadas + diferencial/prova disponível?
  │     └── Dispatch SIMPLES: mos-brand
  │
  ├── Faltam evidências de público, categoria, alternativas ou claims concorrentes?
  │     └── Dispatch SEQUENCIAL: mos-research → mos-brand
  │
  └── USP já aprovada e o pedido é apenas adaptação para uma peça?
        └── Encaminhar depois para mos-copy, preservando a USP como input
```

## Dispatch Simples

```text
Agent(subagent_type: "mos-brand", prompt: "Crie um Dossiê de USP completo para [produto, serviço ou oferta]. Público e Job To Be Done: [público, situação, progresso funcional, emocional e social]. Categoria, mercado e geografia: [categoria/contexto]. Decisão atendida: [uso da USP]. Ticket: [faixa]. Alternativas e concorrentes: [lista]. Mecanismo ou diferencial real: [descrição]. Provas e reason to believe disponíveis: [dados, cases, demonstrações, ativos ou nenhuma]. Research existente: [resumo ou nenhum]. Considere a memory existente do cliente neste projeto, se estiver ativa. Leia a seção 3.3 Unique Value Proposition de subagents/brand-agent.md e siga seu Contrato Canônico do Dossiê de USP. Gere candidatos internamente, pontue clareza, relevância, especificidade, diferenciação, credibilidade, defensabilidade e sustentabilidade; entregue os 3 melhores e recomende 1. Para toda afirmação material, registre fonte, data, escopo, classe EVIDÊNCIA CONFIRMADA, INFERÊNCIA ou HIPÓTESE e confiança. Inclua categoria e contexto competitivo, Job To Be Done, alternativas, matriz de diferenciação, USP principal, reason to believe, mecanismo ou diferencial, provas, limites da promessa, adaptações, plano de validação e Handoff Context para mos-offer, mos-copy, mos-ads e mos-funnel. Não invente exclusividade, prova, claim de concorrente ou resultado. Aplique os Quality Gates globais do Marketing OS.")
```

## Dispatch Sequencial

### Passo 1: pesquisa de público e contexto competitivo

```text
Agent(subagent_type: "mos-research", prompt: "Pesquise o contexto necessário para criar uma USP de [produto, serviço ou oferta] para [público suspeito], em [categoria, mercado e geografia]. Decisão atendida: [uso]. Dados existentes: [research, entrevistas, links ou nenhum]. Entregue um Research Brief compacto com: público e Job To Be Done; linguagem espontânea do cliente; alternativas diretas, indiretas, fazer sozinho, adiar e manter o status quo; 3 a 5 concorrentes; claims e propostas de valor atuais dos concorrentes; atributos comuns da categoria; gaps percebidos; critérios de decisão; sinais de prova; riscos regulatórios; fontes com URL e data. Separe EVIDÊNCIA CONFIRMADA, INFERÊNCIA e HIPÓTESE. Não formule a USP final. Considere a memory existente do cliente neste projeto, se estiver ativa.")
```

### Passo 2: formulação e seleção da USP

Depois do retorno do `mos-research`, passe o brief completo ao `mos-brand`:

```text
Agent(subagent_type: "mos-brand", prompt: "Crie o Dossiê de USP de [produto, serviço ou oferta] usando o Research Brief abaixo como evidência de entrada. Público e Job To Be Done: [público]. Categoria e decisão atendida: [contexto]. Mecanismo, diferencial e provas próprias fornecidos pelo cliente: [dados ou nenhum]. RESEARCH BRIEF: [colar integralmente o output do mos-research]. Leia a seção 3.3 Unique Value Proposition de subagents/brand-agent.md e siga seu Contrato Canônico do Dossiê de USP. Preserve os IDs, fontes, datas e classificações do research. Gere candidatos internamente, entregue os 3 melhores com Score de USP e recomende 1. Inclua categoria e contexto competitivo, matriz de candidatos, USP principal, reason to believe, mecanismo ou diferencial, provas, limites da promessa, adaptações, plano de validação e Handoff Context para mos-offer, mos-copy, mos-ads e mos-funnel. Qualquer exclusividade ou resultado sem suporte permanece HIPÓTESE. Aplique os Quality Gates globais do Marketing OS.")
```

## Consolidação

> **Precedência**: o conteúdo mínimo é o do Dossiê de USP definido no contrato canônico do `mos-brand` (seção 3.3 de `subagents/brand-agent.md`). O schema abaixo define a ordem de apresentação da entrega consolidada, sem descartar campo obrigatório do contrato.

Entregue o resultado final neste schema:

````markdown
# Dossiê de USP: [Produto ou Oferta]

## 1. Metadata e escopo
- Data: [YYYY-MM-DD]
- Tipo: [USP de oferta | UVP de marca + USP derivada]
- Mercado e geografia: [...]
- Contexto: [B2B | B2C]
- Decisão atendida: [...]
- Maturidade: [exploratória | validada | operacional]
- Limitações: [...]

## 2. Resumo executivo
- Público prioritário: [...]
- Job central: [...]
- Categoria: [...]
- Diferencial com maior suporte: [...]
- USP recomendada: [...]
- Maior hipótese pendente: [...]

## 3. Protocolo de evidências
| ID | Afirmação | Classe | Confiança | Fonte e data | Implicação |
|---|---|---|---|---|---|
| E01 | [...] | EVIDÊNCIA CONFIRMADA | alta | [...] | [...] |
| I01 | [...] | INFERÊNCIA | média | deriva de E01 + E02 | [...] |
| H01 | [...] | HIPÓTESE | baixa | validação pendente | [...] |

## 4. Categoria e contexto competitivo
- Público e situação de compra: [...] [ID]
- Job To Be Done: [...] [ID]
- Categoria percebida pelo cliente: [...] [ID]
- Alternativas diretas e indiretas: [...] [IDs]
- Status quo, fazer sozinho ou adiar: [...] [IDs]
- Critérios de decisão: [...] [IDs]
- Claims comuns da categoria: [...] [IDs]
- Espaços de diferenciação: [...] [IDs]

## 5. Inventário de diferenciação
| Capacidade, ativo ou mecanismo | Consequência para o cliente | Prova | Facilidade de cópia | Status |
|---|---|---|---|---|
| [...] | [...] | [IDs] | [baixa/média/alta] | [confirmado/inferido/hipótese] |

## 6. Matriz de candidatos
| Candidato de USP | Clareza | Relevância | Especificidade | Diferenciação | Credibilidade | Defensabilidade | Sustentabilidade | Total | Justificativa | Decisão |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| [...] | [1-5] | [1-5] | [1-5] | [1-5] | [1-5] | [1-5] | [1-5] | [20-100] | [racional por critério] | [recomendada/reserva/descartada] |

## 7. USP principal
- **Frase central:** [...]
- **Versão expandida:** Para [público] que [situação/JTBD], [oferta] é [categoria] que [benefício prioritário], por meio de [mecanismo ou diferencial], sustentado por [reason to believe], em contraste com [alternativa].
- **Reason to believe:** [...] [IDs]
- **Mecanismo ou diferencial:** [...] [IDs]
- **Provas necessárias:** [...]
- **Limites da promessa:** [...]
- **Claims proibidos ou ainda não verificados:** [...]

## 8. Candidatos alternativos

### Candidato 2
- Frase: [...]
- Vantagem: [...]
- Risco: [...]
- Quando testar: [...]

### Candidato 3
[Mesmo schema]

## 9. Adaptações da USP aprovada
- Hero de página: [...]
- Pitch de 30 segundos: [...]
- Headline de anúncio: [...]
- Bio ou descrição curta: [...]
- Brief interno de uma frase: [...]

## 10. Plano de validação
| Hipótese | Método | Público/amostra | Métrica ou sinal | Critério de decisão | Prioridade |
|---|---|---|---|---|---|
| H01 | [entrevista/teste dos 5 segundos/A-B/demonstração] | [...] | [...] | [...] | alta |

## 11. Handoff Context
```json
{
  "usp_version": "1.0",
  "maturity": "exploratoria | validada | operacional",
  "product_or_offer": "...",
  "primary_audience": "...",
  "job_to_be_done": "...",
  "category": "...",
  "primary_usp": "...",
  "reason_to_believe": ["..."],
  "mechanism_or_differentiator": "...",
  "alternatives": ["..."],
  "evidence_ids": ["E01"],
  "claim_limits": ["..."],
  "open_hypotheses": ["H01"],
  "handoffs": {
    "mos-offer": ["promessa", "mecanismo", "prova", "limites"],
    "mos-copy": ["USP aprovada", "RTB", "linguagem", "claims permitidos"],
    "mos-ads": ["público", "ângulo", "prova", "alternativas"],
    "mos-funnel": ["categoria", "consciência", "objeção", "prova necessária"]
  }
}
```

## 12. Fontes
1. [Título, organização ou autor, URL, publicação, acesso e escopo]
````

## Salvar no projeto

Depois de entregar, salve o dossiê em `workspace/brand/usp.md`, no projeto do usuário, para os outros especialistas usarem como contexto. Se o arquivo já existir, preserve a versão anterior com a data no nome. Se `workspace/brand/perfil.md` existir (criado por `/configurar-marca`), atualize a seção Negócio (diferencial) com um resumo de 2 ou 3 linhas.

## Quality Gates (antes de entregar)

- Uma USP principal domina o documento; os outros candidatos ficam como alternativas de teste.
- A frase identifica público, progresso relevante e motivo concreto de preferência.
- Exclusividade exige prova. Na ausência dela, use linguagem específica sem superlativo absoluto.
- O reason to believe aponta para evidência verificável ou permanece hipótese.
- O mecanismo representa uma diferença operacional real, não apenas um nome novo para processo comum.
- Claims de concorrentes incluem fonte e data; diferenças desatualizadas recebem alerta.
- A promessa respeita os limites de evidência, entrega e compliance do nicho.
- Clareza, relevância, especificidade, diferenciação, credibilidade, defensabilidade e sustentabilidade recebem justificativa, além da nota.
- Lista de benefícios, slogan, missão e tagline permanecem entregáveis auxiliares; a USP comunica uma proposta central.
- Aplicar os Quality Gates globais de `skills/marketing-os/SKILL.md`.

## Por que esse dispatch

O `mos-brand` é dono de posicionamento, diferenciação e UVP, portanto formula e seleciona a USP. O `mos-research` entra quando faltam público validado, alternativas ou claims competitivos; seu output precisa existir antes da formulação, justificando o dispatch sequencial. Oferta, copy, ads e funil consomem a USP aprovada por handoff, preservando uma única fonte de verdade.
