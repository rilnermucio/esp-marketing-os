---
description: Voice clone personalizado a partir de amostras LOCAIS do usuário (posts, emails, artigos). Diferente de /criar-clone, não pesquisa expert externo. Salva o clone no projeto do usuário, em workspace/clones/.
argument-hint: "<slug-do-clone>"
---

# /criar-meu-clone: Voice Clone Pessoal (Dispatch + voice_extractor)

Cria um clone de voz a partir das amostras reais de escrita do usuário. Resultado: 4 arquivos em `workspace/clones/{slug}/`, **no projeto do usuário**, que o `mos-copy` consulta quando você pedir copy "no meu estilo".

> **Diferença de `/criar-clone`**: aquele pesquisa experts externos (Halbert, Ogilvy) via web. Este analisa SUAS amostras locais.

> **Por que `workspace/clones/` e não a pasta do plugin**: a pasta do plugin é substituída a cada atualização e é compartilhada por todos os seus projetos. O clone pessoal é dado seu e fica no projeto.

## Quando usar

- Você tem marca ou persona digital com voz distintiva
- Quer copy gerada pelo `mos-copy` que soe como você, não como uma mistura genérica
- Tem pelo menos 10 a 20 amostras reais já publicadas ou enviadas

## Inputs obrigatórios (pergunte se faltar)

1. **Slug** (obrigatório): identificador kebab-case sem espaços. Use prefixo `me-` para distinguir dos clones de experts.
   - Bom: `me-rilner`, `me-marca-x`
   - Evitar: `joao` (conflita com clones públicos)

2. **Amostras** (obrigatório): pelo menos 10 amostras de copy real sua. Aceita:
   - Caminhos de arquivo: `workspace/drafts/post1.md, workspace/drafts/post2.md`
   - Pasta inteira: `workspace/my-content/`
   - Texto colado direto na conversa
   - URLs públicas (Instagram, LinkedIn, blog)

3. **Contexto** (opcional, recomendado): uma frase explicando seu nicho ou persona. Ex: "marketer BR focado em IA aplicada", "creator de finanças pessoais com tom didático".

## Pre-flight (orquestrador inline)

Antes de despachar:

1. O diretório `workspace/clones/{slug}/` do projeto NÃO existe (se existir, pergunte se é para sobrescrever ou abortar; com `--update`, siga para a iteração).
2. Pelo menos 10 amostras foram fornecidas. Se houver menos de 10, avise que a qualidade vai ser limitada e pergunte se quer prosseguir.

## Dispatch (mos-copy roda voice_extractor e gera os arquivos)

```
Agent(subagent_type: "marketing-os:mos-copy", prompt: "Voice extraction de amostras LOCAIS do usuário (não é expert externo; não usar WebSearch). Slug: {slug}. Contexto: [contexto fornecido].

PASSO 1, coleta e limpeza:
- Carregar todas as amostras (Read para arquivos, WebFetch para URLs públicas, parsear texto colado)
- Para cada amostra: remover headers e metadata, manter apenas texto produzido pelo usuário, identificar o tipo (post curto ou longo, email, artigo, thread)
- Reportar inventário: 'Coletei N amostras: X posts, Y emails, Z artigos'

PASSO 2, análise mecânica via script:
Rode via Bash: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/voice_extractor.py" --input <pasta-ou-lista-de-arquivos> --output md --top-words 30 --top-ngrams 20`
O script entrega as 30 palavras mais distintivas (com frequência, presença e score), os 20 n-grams principais, a distribuição de tamanho de frase e os padrões de pontuação.

PASSO 3, interpretação qualitativa em cima do output do script:
- Vocabulário típico: classificar as 30 palavras como 'signature' (distintiva), 'topical' (sobre o nicho) ou 'genérica' (descartar). Manter 15 a 20 signature. Marcar palavras que o usuário NUNCA escreve.
- Cadência e ritmo: identificar o padrão dominante (frases curtas, alternância balanceada, frases longas e fluidas, variação deliberada). Cruzar com a pontuação (dois-pontos = setup-payoff, parênteses = nuance, ? = pergunta retórica, ... = suspensão).
- Estrutura narrativa por tipo de conteúdo: como abre, como fecha, se tem CTA, estrutura geral.
- Anti-padrões: clichês que aparecem em menos de 5% das amostras (ou nunca) e tons que o usuário rejeita implicitamente.
- Persona e posicionamento: nichos, objeções, prova social usada (números próprios, cases, dados externos) e tom (autoridade, parceiro, mentor, contrarian).

PASSO 4, gerar os 4 arquivos em workspace/clones/{slug}/ (no diretório do projeto) via Write:

profile.md: identidade (slug, tipo: voice clone próprio, nicho primário detectado, posicionamento detectado), contexto do usuário, sumário (2 a 3 parágrafos), tipos de conteúdo dominantes, audiência detectada.

voice.md (PRIORIDADE, lido primeiro quando o usuário pedir copy no estilo {slug}): tom geral, vocabulário típico (palavras distintivas e vocabulário banido), cadência (distribuição e padrão dominante), estrutura típica (5 aberturas e 5 fechamentos tirados das amostras, CTAs característicos), anti-padrões (tabela 'Item | Por que não usa'), heurísticas de fidelidade (3 a 5 regras concretas).

frameworks.md: frameworks próprios identificados nas amostras (se houver), frameworks clássicos detectados (AIDA, PAS, Hook-Story-Offer), estruturas dominantes por formato.

examples.md: exemplos diretos (5 a 10 das amostras, com anotação do que torna a voz autêntica), exemplos sintéticos (5 a 10 novos no estilo, com anotação) e comparação 'antes vs depois' (copy genérica reescrita no estilo {slug}).

REGRAS:
- Tudo em PT-BR com acentuação correta
- Aplicar os quality gates globais (sem travessão, sem 'brutal', sem CAPS, sem aspas em falas, no máximo 1 ou 2 emojis)
- Cada um dos 4 arquivos com pelo menos 200 palavras
- A voz precisa ser distintiva: se o vocabulário típico só tiver palavras genéricas, sinalize e peça mais amostras
- Heurísticas de fidelidade concretas (regras acionáveis, nada de 'seja autêntico')

Considere a memory existente do cliente neste projeto. Reportar ao final: total de amostras processadas, 5 palavras mais distintivas e padrão de cadência dominante."
)
```

`mos-copy` tem memory de projeto e sabe procurar clones pessoais em `workspace/clones/`.

## Saída (pós-dispatch, orquestrador inline)

### Validação

1. Verificar que os 4 arquivos foram criados em `workspace/clones/{slug}/`
2. Rodar `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/quality_gate.py" workspace/clones/{slug}/voice.md --type artigo` como checagem de sanidade
3. Se existir `workspace/brand/perfil.md` (criado por `/configurar-marca`), registrar o slug no campo de clone de voz do perfil
4. Reportar ao usuário:
   - Total de amostras processadas
   - 5 palavras mais distintivas
   - Padrão de cadência dominante
   - Qualquer alerta (poucas amostras, vocabulário genérico, pouca profundidade)

## Como ativar o clone depois

No `mos-copy` (ou em qualquer pedido de copy), use:

- "crie copy de vendas no meu estilo (`{slug}`)"
- "escreva como eu escreveria"
- "estilo `{slug}`"

O agent procura `workspace/clones/{slug}/voice.md` no projeto antes de gerar. Clones de experts continuam na pasta do plugin.

## Iteração

Voice clones podem ser **atualizados** com mais amostras:

```
/criar-meu-clone {slug} --update
```

Adicione novas amostras ao clone existente sem sobrescrever; o agent faz o merge em `voice.md` e `examples.md`.

## Quality gates (antes de entregar)

Aplicar os gates globais do SKILL.md do Marketing OS:
- Não prosseguir com menos de 10 amostras (avisar e perguntar)
- Sinalizar amostras de baixa qualidade (texto com menos de 50 caracteres, repetido, fora do tema)
- A voz extraída deve ser distintiva: vocabulário genérico significa refazer com mais amostras
- Cada um dos 4 arquivos com mais de 200 palavras
- Tudo em PT-BR com acentuação correta

## Por que isso importa

Os clones de experts que vêm com o plugin são excelentes para "copy estilo Halbert" ou "estilo Hormozi". Mas a sua marca tem voz própria, que é a soma das suas escolhas linguísticas ao longo do tempo. Sem este clone, o agent gera uma mistura genérica de mestres. Com ele, o agent gera copy que soa como você.

`/criar-meu-clone` é o caso especial do sistema: não despacha `mos-research` (não vai à web), usa `voice_extractor.py` para extrair padrões objetivos e o `mos-copy` para interpretar e materializar os 4 arquivos.
