---
description: Gera um voice clone personalizado a partir de amostras reais da sua escrita (posts, emails, artigos). Diferente de /criar-clone que pesquisa um expert externo, este captura a SUA voz pra que o Marketing OS gere copy que soa como voce.
argument-hint: "<slug-do-clone>"
---

# Criar Meu Clone (Voice Clone Personalizado)

Cria um clone de voz a partir das suas proprias amostras de escrita. O resultado: 4 arquivos (`profile.md`, `voice.md`, `frameworks.md`, `examples.md`) em `assets/clones/{slug}/` que o `mos-copy` agent vai consultar quando voce pedir copy "no meu estilo".

> **Diferenca de `/criar-clone`**: aquele pesquisa experts externos (Halbert, Ogilvy) via web. Este analisa SUAS amostras locais para capturar SUA voz autentica.

## Quando usar

- Voce tem uma marca/persona digital com voz distintiva
- Quer que copy gerada pelo `mos-copy` soe como voce, nao como mistura generica
- Tem pelo menos 10-20 amostras reais de copy publicada/enviada

## Inputs

1. **Slug** (obrigatorio) — identificador curto sem espacos. Use prefixo `_user-` ou seu @ pra distinguir de clones de experts:
   - Bom: `_user-rilner`, `me-rilner`, `_my-voice`
   - Evitar: `joao` (conflita com clones de pessoas famosas)

2. **Samples** (obrigatorio) — pelo menos 10 amostras de copy real sua. Aceita:
   - Caminhos de arquivo: `workspace/drafts/post1.md, workspace/drafts/post2.md`
   - Pasta inteira: `workspace/my-content/`
   - Texto colado direto na conversa
   - URLs publicas (Instagram, LinkedIn, blog) — agent vai usar WebFetch

3. **Contexto** (opcional, recomendado) — uma frase explicando seu nicho/persona:
   - "marketer BR focado em IA aplicada"
   - "creator de finanças pessoais com tom didatico"
   - "consultor B2B SaaS, voz tecnica mas acessivel"

## Pre-Flight Check

Antes de comecar, verificar:

1. Diretorio `assets/clones/{slug}/` NAO existe (se existir, perguntar overwrite ou abortar)
2. `assets/clones/clone-manifest.yaml` existe
3. Pelo menos 10 amostras foram fornecidas (se < 10, avisar usuario que qualidade vai ser limitada)

## Workflow de Execucao

### Fase 1: Coleta e Limpeza das Amostras

1. Carregar todas as amostras (Read para arquivos, WebFetch para URLs, parse direto pra texto colado)
2. Para cada amostra, normalizar:
   - Remover headers/metadata se houver
   - Manter apenas o texto produzido pelo usuario (nao replies/comentarios)
   - Identificar tipo: post curto, post longo, email, artigo, thread
3. Reportar inventario: "Coletei N amostras: X posts, Y emails, Z artigos"

### Fase 2: Analise de Padroes

**Use `scripts/voice_extractor.py` para a parte mecanica** (frequencia, distribuicao, n-grams, pontuacao). Em seguida, faca interpretacao qualitativa em cima dos dados.

```bash
python3 scripts/voice_extractor.py \
  --input <pasta-de-samples-ou-arquivos> \
  --output md \
  --top-words 30 \
  --top-ngrams 20
```

O script gera um relatorio com dados objetivos. Sua tarefa: interpretar.

#### A) Vocabulario Tipico (a partir do output do script)

- O script ja te entrega "Top 30 palavras distintivas" com freq + presence + score
- Sua tarefa: ler a lista e classificar cada palavra como "signature" (distintiva, raramente usada por outros), "topical" (sobre o nicho), ou "generica" (descartar)
- Mantenha as 15-20 palavras de signature
- Marcar palavras que o usuario NUNCA escreve (com base em comparacao com baseline mental de PT-BR comum)

#### B) Cadencia e Ritmo (a partir do output do script)

- O script entrega distribuicao % de tamanho de frase
- Identifique o padrao dominante:
  - "Frases curtas predominam" (>50% < 8 palavras)
  - "Alternancia balanceada" (mix em todos buckets)
  - "Frases longas e fluidas" (>40% > 15 palavras)
  - "Variacao deliberada" (alta dispersao com pico em 1-palavra ocasional)
- Cruze com o output de pontuacao: muitos dois-pontos = uso de "setup-payoff", muitos parenteses = nuance lateral, muitos `?` = perguntas retoricas, muitos `...` = tom suspensivo

#### C) Estrutura Narrativa

Para cada tipo de conteudo, identificar o pattern do usuario:
- **Posts curtos**: como abre? como fecha? tem CTA?
- **Posts longos**: estrutura geral (gancho -> contexto -> argumento -> CTA?)
- **Emails**: subject line patterns, opening lines, closing patterns
- **Threads/carrosseis**: numero medio de itens, formato de cada item

#### D) Anti-padroes (o que o usuario NAO faz)

- Lista de cliches que aparecem em <5% das amostras (ou nunca)
- Tons que o usuario rejeita implicitamente
- Estruturas que ele nao usa

#### E) Persona e Posicionamento

- Que assunto ele trata mais? (nichos)
- Que objeções ele endereca?
- Que prova social ele usa? (numeros proprios, casos de clientes, dados externos)
- Como ele se posiciona? (autoridade, parceiro, mentor, contrarian)

### Fase 3: Geracao dos 4 Arquivos

Crie `assets/clones/{slug}/` com os 4 arquivos:

#### profile.md

```markdown
# {Nome do usuario} - Profile

## Identidade
- **Slug**: {slug}
- **Tipo**: voice clone proprio (nao expert externo)
- **Nicho primario**: {detectado}
- **Posicionamento**: {detectado}

## Contexto
{contexto fornecido pelo usuario}

## Sumario
{2-3 paragrafos descrevendo a voz/persona com base na analise}

## Tipos de conteudo dominantes
{lista detectada: posts, emails, artigos, etc.}

## Audiencia
{persona detectada se possivel}
```

#### voice.md (LER PRIMEIRO quando agent gerar copy estilo {slug})

```markdown
# {Nome} - Guia de Voz

## Tom Geral
{descricao em 1-2 paragrafos}

## Vocabulario Tipico

**Palavras/frases distintivas:**
{20-30 termos com freq alta + singularidade alta}

**Vocabulario banido (raro/nunca):**
{lista do que ele evita}

## Cadencia
{distribuicao de tamanho de frase + padrao dominante}

## Estrutura Tipica

### Aberturas
{patterns de como ele abre + 5 exemplos das amostras}

### Fechamentos
{patterns + 5 exemplos}

### CTAs caracteristicos
{como ele pede acao, se pede}

## Anti-padroes (NAO faca)

| Item | Por que ele nao usa |
|------|---------------------|
| ... | ... |

## Heuristicas de fidelidade

Para gerar copy fiel a {slug}:
1. {regra concreta 1}
2. {regra concreta 2}
3. {regra concreta 3}
```

#### frameworks.md

```markdown
# {Nome} - Frameworks

## Frameworks proprietarios identificados
{frameworks que aparecem nas amostras, se houver}

## Frameworks classicos que ele usa
{ex: AIDA, PAS, Hook-Story-Offer detectados}

## Estruturas de conteudo dominantes

### Para posts curtos
{template extraido das amostras}

### Para posts longos
{template extraido}

### Para emails
{template extraido}
```

#### examples.md

```markdown
# {Nome} - Exemplos Aplicados

## Exemplos diretos (das amostras)
{5-10 exemplos das amostras originais com anotacao do que torna autenticamente "voz dele"}

## Exemplos sinteticos (gerados respeitando o estilo)
{5-10 exemplos novos, gerados pelo agent imitando o estilo, com anotacao do que esta capturando}

## Comparacao "antes vs depois"
{exemplo: copy generica reescrita no estilo {slug}}
```

### Fase 4: Atualizar Manifest

Adicionar entrada em `assets/clones/clone-manifest.yaml`:

```yaml
- slug: {slug}
  type: user-voice  # diferente de "expert" usado por /criar-clone
  created_at: {data}
  samples_count: {N}
  niches: [{detectados}]
  notes: "Voice clone gerado a partir de amostras pessoais"
```

### Fase 5: Validacao

1. Verificar que os 4 arquivos foram criados
2. Rodar `python3 scripts/quality_gate.py {slug}/voice.md --type artigo` para sanity check
3. Reportar ao usuario:
   - Total de amostras processadas
   - Top 5 palavras distintivas extraidas
   - Padrao de cadencia dominante
   - Como ativar: 'gerar copy no estilo `{slug}`' ou 'meu estilo'

## Como ativar o clone depois

No `mos-copy` agent (ou em qualquer chamada de copy), use:

- "crie copy de vendas no meu estilo (`{slug}`)"
- "escreva como eu escreveria"
- "estilo `{slug}`"

O agent vai automaticamente fazer Read em `assets/clones/{slug}/voice.md` antes de gerar (per protocolo PARTE XV-B em `subagents/copy-agent.md`).

## Quality Gates

- Nao prosseguir com < 10 amostras
- Sinalizar amostras de baixa qualidade (texto < 50 caracteres, repetidos, off-topic)
- Voice extraido deve ser distintivo: se o vocabulario tipico tem so palavras genericas, refazer com mais amostras
- Cada um dos 4 arquivos deve ter > 200 palavras (caso contrario nao tem profundidade suficiente)

## Iteracao

Voice clones podem ser **atualizados** com mais amostras ao longo do tempo:

```
/criar-meu-clone {slug} --update
```

(adicionar novas amostras ao clone existente, sem sobrescrever)

## Por que isso importa

Os 35 clones de experts sao excelentes para "copy estilo Halbert" ou "estilo Hormozi". Mas sua marca tem voz propria que e a soma de todas as suas escolhas linguisticas ao longo do tempo. Sem este clone, o agent gera "uma mistura generica de mestres". Com este clone, o agent gera copy que soa como voce, nao como uma fusao plagiada.
