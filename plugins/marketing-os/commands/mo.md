---
description: "Porta de entrada para qualquer briefing em linguagem natural: escolhe o command ou especialista certo e diz qual rota tomou. Use quando não souber qual command usar ou o pedido misturar várias entregas."
argument-hint: "<briefing aberto, ex: 'preciso de conteúdo pro lançamento de um curso de Python'>"
---

# /mo: Meta-Orquestrador (briefing aberto, sem precisar saber o command)

Atalho universal para quando o usuário sabe **o que precisa** mas não sabe **qual `/criar-X` usar**. Recebe briefing em linguagem natural, identifica o caso, e:

1. Dispatcha o(s) agent(s) mos-* certo(s), OU
2. Sugere o command especializado equivalente (`/criar-post`, `/campanha`, etc.), OU
3. Pergunta clarificações ANTES de dispatchar quando o briefing é ambíguo demais.

Não duplica lógica do `skills/marketing-os/SKILL.md`: usa o Mapa de Dispatch oficial daquele arquivo como fonte de verdade.

## Quando usar este command

- Você não sabe qual `/criar-X` cabe ("preciso de conteúdo pro lançamento", `/criar-post`? `/campanha`? `/criar-infoproduto`?)
- Briefing toca em mais de uma área ("artigo + post promo + email")
- Você só quer descrever o problema e deixar o sistema decidir o melhor workflow
- Quer descobrir quais workflows existem antes de comprometer com um command específico

Para briefings claros e únicos (`"cria um post Instagram sobre X"`), invoque `/criar-post` direto, vai direto ao ponto sem a camada de roteamento.

## Protocolo de execução (você, o orquestrador)

### Passo 1: Ler o briefing

O usuário forneceu texto livre. Identifique:

- **Tipo de entregável** (peça única? campanha? análise?)
- **Plataforma/canal** (Instagram, email, landing page, ads, etc.)
- **Estágio de funil** (TOFU / MOFU / BOFU)
- **Sinais de complexidade** (uma peça vs sequência vs lançamento completo)

### Passo 2: Decidir a rota

Use a tabela abaixo. Para casos não cobertos, consulte o **Mapa de Dispatch** em `skills/marketing-os/SKILL.md` (seção "Mapa de Dispatch"), fonte canônica.

#### Fonte única de roteamento: o SKILL.md

Este command não mantém tabela própria. Leia, nesta ordem, as seções de `skills/marketing-os/SKILL.md`:

1. **"Slash commands: qual usar para cada necessidade"**: escolha o command. É a tabela canônica e cobre todos os commands.
2. **"Mapa de Dispatch"**, com as rotas condicionais e os desempates: use quando nenhum command encaixar e escolha o agent.
3. **"Workflows compostos"** (5 a 10): páginas, webinar, lançamento, carrossel, VSL e clone de estratégia.

Briefing puramente conceitual ("o que é AIDA?", "qual a diferença entre TOFU e BOFU?"): responda inline, sem dispatch.

Divergência entre um mapa próprio aqui e o SKILL.md foi o achado #13 da auditoria de 2026-09-28 (21 commands ausentes, gatilhos mapeados para rotas diferentes). Se o SKILL.md não cobre um caso, corrija o SKILL.md.

### Passo 3: Decision tree (qual modo de resposta)

```
Briefing recebido
  |
  +-- Briefing 100% claro + cabe num único command?
  |     -> Modo "sugerir command": diga ao usuário qual /criar-X equivale,
  |        ofereça rodar agora ou apenas indicar o atalho
  |
  +-- Briefing claro + não tem command específico mas mapeia 1 agent direto?
  |     -> Modo "dispatch direto": Agent(subagent_type: "mos-X", prompt: ...)
  |
  +-- Briefing amplo / multi-canal / lançamento / campanha?
  |     -> Modo "workflow": rotear pra /campanha <preset> ou pro workflow
  |        composto certo (#5 página BOFU, #6 webinar, #7 infoproduto,
  |        #8 carrossel, #9 VSL, #10 análise concorrente, ver SKILL.md)
  |
  +-- Briefing ambíguo (faltam dados-chave: nicho, avatar, ticket, plataforma)?
        -> Modo "clarificar": faça as 5 perguntas-chave do SKILL.md
           (numerada na mesma resposta), aguarde resposta, depois roteie
```

### Passo 4: Modo "sugerir command" (caso comum, baixa fricção)

Quando você identifica um command específico que cabe, responda assim:

```
Pelo briefing, isso é um caso de **/criar-post** (post Instagram sobre [tema]).

Quer que eu:
A. Rode /criar-post agora com esses dados
B. Só indique o command pra você invocar diretamente

Se preferir A, dispatcho o mos-social com o briefing pronto. Se faltar algo
(nicho, avatar, tom), eu pergunto antes.
```

Espere a escolha do usuário. Não dispatche sem confirmação quando o command equivalente existe, o usuário pode preferir aprender o atalho.

### Passo 5: Modo "dispatch direto" (sem command equivalente OR usuário pediu pra rodar)

Use o template do command equivalente como referência (eles estão em `commands/`), e dispatche o agent. Exemplo:

```
Agent(subagent_type: "mos-X", prompt: "[contexto extraído do briefing]. Considere memory existente do cliente neste projeto. Aplique quality gates globais (sem travessão, sem 'brutal', PT-BR correto, máx 1-2 emojis). Entregue: [schema do agent].")
```

### Passo 6: Modo "clarificar" (briefing ambíguo)

Pergunte exatamente as **5 perguntas-chave** do SKILL.md (numeradas na mesma resposta):

1. **Nicho**: qual área? (saúde, finanças, tech, educação, etc.)
2. **Avatar**: quem é o público? (cargo/profissão, faixa de renda, dor principal)
3. **Ticket**: preço do produto? (gratuito, low/mid/high-ticket)
4. **Plataforma**: onde vai publicar? (Instagram, LinkedIn, email, página web, etc.)
5. **Urgência**: publicar hoje, semana, planejamento futuro?

Pule as que já vieram explícitas no briefing OU já estão em memory do cliente (`.claude/agent-memory/marketing-os-mos-*/`). NÃO chute respostas.

## Quality Gates (sempre, antes de qualquer entrega)

Se você dispatcha qualquer agent ou consolida output, aplique a seção "Quality Gates Globais" do SKILL.md (travessão, "brutal", antítese, CAPS, emojis, acentuação, fact-check, enquete em social e compliance regulatório por conselho).

## Exemplos resolvidos

### Exemplo 1: briefing claro com command equivalente

```
Usuário: /mo preciso de um post no Instagram sobre produtividade pra devs

Você responde:
Isso cabe direto em **/criar-post**. Quer que eu rode agora ou prefere
invocar o command direto?

Se rodar agora, dispatcho mos-social com:
- Plataforma: Instagram
- Tema: produtividade pra devs
- Goal: engagement (default, me corrige se for tráfego/conversão)
- Tom: técnico-prático

Confirma?
```

### Exemplo 2: briefing genérico complexo (campanha)

```
Usuário: /mo vou lançar um curso de Python pra iniciantes em 30 dias,
preciso de tudo

Você responde:
Isso é caso clássico de lançamento, recomendo **/campanha-lancamento**
(preset que dispatcha mos-research + mos-launch + mos-funnel em paralelo,
depois copy + storytelling + social + email, depois ads + design + analytics).

Antes de rodar, preciso confirmar:
1. Avatar, devs juniores? estudantes? profissionais migrando de área?
2. Ticket, quanto custa o curso? (define modelo de lançamento)
3. Lista existente? Tamanho? (define se é PLF / semente / relâmpago)
4. Plataforma principal de aquecimento, Instagram, YouTube, email?
5. Budget pra ads, tem? quanto?

Com isso, rodo /campanha-lancamento "Curso Python iniciantes"
--preco=[X] --clone=[brunson|hormozi conforme estilo]
```

### Exemplo 3: briefing que mapeia 1 agent direto

```
Usuário: /mo quero 5 headlines pra uma sales letter de cripto

Você responde:
Vou dispatchar mos-copy direto.

[Agent(subagent_type: "mos-copy", prompt: "5 headlines pra sales letter
no nicho cripto. Considere compliance CVM (rentabilidade passada não
garante futura, sem promessa de retorno, risco explícito). Quality gates
globais. Entregue 5 variações com ângulos diferentes: problem-aware,
big idea, mecanismo único, social proof, urgência.")]
```

### Exemplo 4: briefing ambíguo

```
Usuário: /mo preciso melhorar meu marketing

Você responde (modo clarificar):
Briefing amplo demais pra rotear bem. Antes de chutar, me ajuda com:

1. **Nicho**: qual área? (saúde, finanças, tech, educação, etc.)
2. **Avatar**: quem é o público alvo?
3. **Ticket**: qual o preço do produto/serviço principal?
4. **Plataforma**: onde já está ativo / quer estar?
5. **Urgência**: peça pontual ou planejamento mensal/lançamento?

Pode responder em texto corrido, eu extraio. Com isso eu roteio pro
workflow certo (post, sequência, campanha completa, etc.).
```

### Exemplo 5: pergunta conceitual (responder inline)

```
Usuário: /mo qual a diferença entre TOFU e BOFU?

Você responde inline (sem dispatch):
TOFU (Top of Funnel) é topo de funil: conteúdo de descoberta pra audiência
fria que ainda não sabe que tem o problema. BOFU (Bottom of Funnel) é fundo:
copy de conversão pra leads quentes prontos pra comprar (página de vendas,
oferta direta, email de fechamento). MOFU é o meio (nutrição, lead magnet,
educação que conecta dor a solução). No SKILL.md, /criar-funil cobre os 3
estágios; /criar-landing-page foca BOFU.
```

## Por que existe esse command

Há dezenas de commands específicos. Pra usuários novos é fricção descobrir o certo. Pra casos ambíguos ("conteúdo pro lançamento", qual command?) o sistema fica engessado. `/mo` resolve com:

- **Single entry point**: 1 command que aceita qualquer briefing de marketing
- **Discoverability**: usuário não precisa decorar nomes de commands
- **Sem duplicação**: usa SKILL.md como fonte canônica do roteamento
- **Não force dispatch**: prefere sugerir command equivalente quando existe (ensina o usuário o atalho), só dispatcha quando ele confirma OU não há command direto

## Output

Sua resposta sempre cai em UM dos 4 formatos abaixo. Escolha conforme o decision tree do Passo 3 e mantenha o output curto:

### Formato A: Sugerir command (briefing claro + tem command equivalente)

```markdown
## Roteamento

Cabe em **/criar-X** (ou **/campanha <preset>**).

Briefing extraído:
- [campo 1]: [valor]
- [campo 2]: [valor]
- ...

Quer que eu:
A. Rode /criar-X agora com esses dados
B. Só indique o command pra você invocar diretamente (atalho aprendido)

Se faltar [campo opcional], pergunto antes de rodar.
```

### Formato B: Dispatch direto (sem command equivalente OU usuário pediu pra rodar)

Após Agent(...) retornar, consolide:

```markdown
## Entrega

Agent dispatchado: mos-X
Briefing: [resumo de 1 linha]

[output do agent, formatado conforme schema do agent]

### Quality gates aplicados
- [x] Sem travessão / "brutal" / CAPS / aspas em fala
- [x] PT-BR acentuado
- [x] Fact-check: [CONFIRMADO | PROVÁVEL | N/A]
- [x] Compliance: [aplicado X | N/A]
- [x] Enquete: [incluída | N/A não é social]

### Próximos passos
1. [ação 1]
2. [ação 2]
```

### Formato C: Workflow (briefing amplo / multi-canal / lançamento)

```markdown
## Roteamento

Briefing exige workflow composto. Recomendo **/campanha <preset>** OU
**workflow #N** (ver skills/marketing-os/SKILL.md).

Plano:
- Fase 1 (paralelo): [agents]
- Fase 2 (sequencial/paralelo): [agents]
- Fase 3 (consolidação): [output]

Antes de rodar, confirme:
1. [pergunta 1 das 5-chave que faltou]
2. [pergunta 2]
...
```

### Formato D: Clarificar (briefing ambíguo)

```markdown
## Antes de rotear, preciso de:

1. **Nicho**: qual área?
2. **Avatar**: quem é o público?
3. **Ticket**: preço do produto?
4. **Plataforma**: onde vai publicar?
5. **Urgência**: pontual / mensal / lançamento?

Pode responder em texto corrido. Pulo as que já vieram no briefing inicial.
```

## Observações

- **Nunca duplique** lógica de Mapa de Dispatch aqui, sempre referencie `skills/marketing-os/SKILL.md`
- **Prefira sugerir command** sobre dispatchar direto quando o command existe (efeito colateral positivo: usuário aprende o atalho)
- **Clarifique antes de dispatchar** quando faltam dados-chave (5 perguntas), nunca chute
- **Para campanhas/lançamentos**, sempre roteie pra `/campanha <preset>` (presets já têm cronograma, KPIs, checklist)
- **Quality gates globais** se aplicam mesmo aqui: você é o último filtro antes da entrega
