---
description: Voice clone personalizado a partir de amostras LOCAIS do usuario (posts, emails, artigos). Diferente de /criar-clone, nao pesquisa expert externo. Dispatcha mos-copy que roda scripts/voice_extractor.py e gera os 4 arquivos do clone.
argument-hint: "<slug-do-clone>"
---

# /criar-meu-clone: Voice Clone Pessoal (Dispatch + voice_extractor)

Cria clone de voz a partir das amostras reais de escrita do usuario. Resultado: 4 arquivos em `assets/clones/{slug}/` que o `mos-copy` consulta quando voce pedir copy "no meu estilo".

> **Diferenca de `/criar-clone`**: aquele pesquisa experts externos (Halbert, Ogilvy) via web. Este analisa SUAS amostras locais.

## Quando usar

- Voce tem marca/persona digital com voz distintiva
- Quer copy gerada pelo `mos-copy` que soa como voce, nao mistura generica
- Tem pelo menos 10-20 amostras reais ja publicadas/enviadas

## Required inputs (ask if missing)

1. **Slug** (obrigatorio): identificador kebab-case sem espacos. Use prefixo `_user-` pra distinguir de clones de experts.
   - Bom: `_user-rilner`, `me-rilner`, `_my-voice`
   - Evitar: `joao` (conflita com clones publicos)

2. **Samples** (obrigatorio): pelo menos 10 amostras de copy real sua. Aceita:
   - Caminhos de arquivo: `workspace/drafts/post1.md, workspace/drafts/post2.md`
   - Pasta inteira: `workspace/my-content/`
   - Texto colado direto na conversa
   - URLs publicas (Instagram, LinkedIn, blog)

3. **Contexto** (opcional, recomendado): uma frase explicando seu nicho/persona. Ex: "marketer BR focado em IA aplicada", "creator de financas pessoais com tom didatico".

## Pre-flight check (orquestrador inline)

Antes de dispatchar:

1. Diretorio `assets/clones/{slug}/` NAO existe (se existir, perguntar overwrite ou abortar)
2. `assets/clones/clone-manifest.yaml` existe
3. Pelo menos 10 amostras foram fornecidas. Se < 10, avisar que qualidade vai ser limitada e perguntar se quer prosseguir.

## Dispatch (mos-copy roda voice_extractor + gera arquivos)

```
Agent(subagent_type: "mos-copy", prompt: "Voice extraction de amostras LOCAIS do usuario (nao expert externo, nao usar WebSearch). Slug: {slug}. Contexto: [contexto fornecido].

PASSO 1, Coleta e limpeza:
- Carregar todas as amostras (Read pra arquivos, WebFetch pra URLs publicas, parsear texto colado)
- Para cada amostra: remover headers/metadata, manter apenas texto produzido pelo usuario, identificar tipo (post curto/longo, email, artigo, thread)
- Reportar inventario: 'Coletei N amostras: X posts, Y emails, Z artigos'

PASSO 2, Analise mecanica via script:
Rode via Bash: `python3 scripts/voice_extractor.py --input <pasta-ou-lista-de-arquivos> --output md --top-words 30 --top-ngrams 20`
O script entrega top-30 palavras distintivas (com freq + presence + score), top-20 n-grams, distribuicao % de tamanho de frase, padroes de pontuacao.

PASSO 3, Interpretacao qualitativa em cima do output do script:
- Vocabulario tipico: das 30 palavras, classificar como 'signature' (distintiva, raramente usada por outros), 'topical' (sobre o nicho) ou 'generica' (descartar). Manter 15-20 signature. Marcar palavras que o usuario NUNCA escreve (comparando com baseline mental de PT-BR comum).
- Cadencia e ritmo: identificar padrao dominante (frases curtas predominam / alternancia balanceada / frases longas e fluidas / variacao deliberada). Cruzar com pontuacao (dois-pontos = setup-payoff, parenteses = nuance, ? = pergunta retorica, ... = suspensivo).
- Estrutura narrativa por tipo de conteudo: como abre? como fecha? tem CTA? estrutura geral.
- Anti-padroes: cliches que aparecem em <5% das amostras (ou nunca), tons que o usuario rejeita implicitamente.
- Persona e posicionamento: nichos tratados, objecoes, prova social usada (numeros proprios? cases? dados externos?), tom (autoridade/parceiro/mentor/contrarian).

PASSO 4, Gerar os 4 arquivos em assets/clones/{slug}/ via Write:

profile.md, Identidade (slug, tipo: voice clone proprio nao expert externo, nicho primario detectado, posicionamento detectado), Contexto (do user), Sumario (2-3 paragrafos com base na analise), Tipos de conteudo dominantes, Audiencia detectada.

voice.md (PRIORIDADE, agent vai ler primeiro quando gerar copy estilo {slug}), Tom Geral, Vocabulario Tipico (palavras distintivas + vocabulario banido), Cadencia (distribuicao + padrao dominante), Estrutura Tipica (aberturas com 5 exemplos das amostras + fechamentos com 5 exemplos + CTAs caracteristicos), Anti-padroes (tabela 'Item | Por que nao usa'), Heuristicas de fidelidade (3-5 regras concretas pra clonar a voz).

frameworks.md, Frameworks proprietarios identificados nas amostras (se houver), Frameworks classicos detectados (AIDA / PAS / Hook-Story-Offer), Estruturas de conteudo dominantes por formato (template extraido).

examples.md, Exemplos diretos (5-10 das amostras originais com anotacao do que torna autenticamente 'voz dele'), Exemplos sinteticos (5-10 novos gerados imitando o estilo, com anotacao do que esta capturando), Comparacao 'antes vs depois' (copy generica reescrita no estilo {slug}).

REGRAS:
- Tudo em PT-BR
- Aplicar quality gates globais (sem '—', sem 'brutal', sem CAPS, sem aspas em falas, max 1-2 emojis)
- Cada um dos 4 arquivos com pelo menos 200 palavras
- Voice precisa ser distintivo: se vocabulario tipico tem so palavras genericas, sinalizar e pedir mais amostras
- Heuristicas de fidelidade devem ser concretas (regras acionaveis, nao 'seja autentico')

Considere memory existente do cliente neste projeto. Reportar ao final: total de amostras processadas, top 5 palavras distintivas extraidas, padrao de cadencia dominante."
)
```

`mos-copy` tem memory project, cita explicitamente.

## Phase pos-dispatch (orquestrador inline)

### Atualizar manifest

Adicionar entrada em `assets/clones/clone-manifest.yaml`:

```yaml
- slug: {slug}
  type: user-voice  # diferente de "expert" usado por /criar-clone
  created_at: {data}
  samples_count: {N}
  niches: [{detectados pelo agent}]
  notes: "Voice clone gerado a partir de amostras pessoais"
```

### Validacao

1. Verificar que os 4 arquivos foram criados em `assets/clones/{slug}/`
2. Rodar `python3 scripts/quality_gate.py assets/clones/{slug}/voice.md --type artigo` pra sanity check
3. Reportar ao usuario:
   - Total de amostras processadas
   - Top 5 palavras distintivas extraidas
   - Padrao de cadencia dominante
   - Qualquer flag (poucas amostras, vocabulario generico, baixa profundidade)

## Como ativar o clone depois

No `mos-copy` (ou qualquer chamada de copy), use:

- "crie copy de vendas no meu estilo (`{slug}`)"
- "escreva como eu escreveria"
- "estilo `{slug}`"

O agent vai automaticamente fazer Read em `assets/clones/{slug}/voice.md` antes de gerar (per protocolo PARTE XV-B em `subagents/copy-agent.md`).

## Iteracao

Voice clones podem ser **atualizados** com mais amostras:

```
/criar-meu-clone {slug} --update
```

(adicionar novas amostras ao clone existente, sem sobrescrever, o agent faz merge no voice.md/examples.md).

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Nao prosseguir com < 10 amostras (avisar e perguntar)
- Sinalizar amostras de baixa qualidade (texto < 50 caracteres, repetidos, off-topic)
- Voice extraido deve ser distintivo: vocabulario tipico generico = refazer com mais amostras
- Cada um dos 4 arquivos com > 200 palavras (caso contrario sem profundidade)
- Tudo em PT-BR com acentuacao correta (mesmo este command esta sem acentos por seguranca de encoding, o agent gera com acentuacao plena)

## Por que isso importa

Os 35 clones de experts em `assets/clones/` sao excelentes pra "copy estilo Halbert" ou "estilo Hormozi". Mas a sua marca tem voz propria que e a soma de todas as escolhas linguisticas suas ao longo do tempo. Sem este clone, o agent gera "uma mistura generica de mestres". Com este clone, o agent gera copy que soa como voce, nao como uma fusao plagiada.

`/criar-meu-clone` e o caso especial do sistema: nao despacha `mos-research` (nao vai a web), usa `voice_extractor.py` pra extrair padroes objetivos e `mos-copy` pra interpretar e materializar nos 4 arquivos.
