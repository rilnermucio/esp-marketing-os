# Heurísticas de engenharia do Marketing OS

> Canônico. Atualizado em 2026-07-06. Heurísticas destiladas de rodadas reais de manutenção; cada uma cita o precedente que a motivou quando existe.

## 1. Melhorar agents (Tier 1: `agents/mos-*.md`)

- **H1.1: mos-copy é o padrão de completude.** Antes de melhorar um agent, faça o diff de features contra ele: pre-flight, auto-iteração com scoring, red team condicionado a high-stakes, output schema com handoff JSON, protocolo de memory, gates bloqueantes, compliance auto-detection. Feature ausente é candidata; feature ausente E inútil pro domínio não entra (ver H7).
- **H1.2: toda capacidade citada precisa da tool correspondente.** Prompt que manda rodar `python3 scripts/x.py` exige `Bash` na tools list; gate de fact-check exige `WebSearch`. Precedente: instrução morta no mos-copy (jun/2026), hoje bloqueada por `validate_agents.py --strict`.
- **H1.3: memory: project entra quando o domínio aprende com o usuário.** Critério: existe pattern transferível entre sessões que o repo não captura? (subject lines vencedoras, keywords que rankearam, hooks com retenção). Se sim, memory + entrada no `init_agent_memory.py` + protocolo "o que salvar / o que NÃO salvar" no prompt. Se o output é determinístico do briefing, memory é ruído.
- **H1.4: red team é reativo, pre-flight é proativo; peça de alto custo de erro merece os dois.** Pre-flight barra geração sem insumo (research ausente); red team critica o que foi gerado. Agent com red team e sem pre-flight tem metade do ciclo.
- **H1.5: instrução condicional tem que ter condição alcançável.** "Se tiver acesso a X" onde X nunca é verdadeiro é pior que não ter a instrução: parece coberto e não está.

## 2. Melhorar knowledge bases (Tier 2: `subagents/*-agent.md`)

- **H2.1: profundidade vai no Tier 2, nunca no Tier 1.** O Tier 1 referencia PARTEs por nome; edição livre no Tier 2 não mexe no dispatch. Se um agent Tier 1 passar de ~400 linhas, algo está no andar errado.
- **H2.2: KB acima de ~1.500 linhas exige índice no topo.** O Tier 1 lê sob demanda; sem índice, "sob demanda" vira leitura integral (falha F-COST-01).
- **H2.3: seção datada exige snapshot guard.** Qualquer bloco com ferramentas, preços, tendências ou anos ganha preâmbulo "SNAPSHOT DATADO (mês/ano)" + instrução de confirmar via WebSearch antes de recomendar. Precedente: PARTE XVI do copy-agent envelheceu silenciosamente até jun/2026.
- **H2.4: princípios envelhecem bem, números envelhecem mal.** Ao escrever KB, separe: taxonomias e critérios de escolha (permanentes) de nomes de modelos, preços e stats (apêndice datado).
- **H2.5: Tier 1 que cita PARTE X do Tier 2 cria contrato.** Renomear/remover seção da KB exige grep pelos consumidores (falha F-REG-02).

## 3. Melhorar commands (`commands/*.md`)

- **H3.1: command de produção dispatcha; nunca produz inline.** Contrato travado por `test_commands_dispatch.py`. Utility genuíno entra em `UTILITY_COMMANDS` com justificativa em comentário.
- **H3.2: anatomia mínima**: frontmatter com `description` e `argument-hint` específicos; "Required inputs (ask if missing)" numerado; decision tree quando há mais de um caminho de dispatch; bloco de dispatch com prompt COMPLETO (inputs interpolados, entregável explícito, gates citados); "## Consolidação" com schema do output final; "Por que esse dispatch" de 3-5 linhas.
- **H3.3: o prompt de dispatch é uma API.** O subagent não vê a conversa; tudo que ele precisa vai no prompt (falha F-DISP-02). Teste mental: esse prompt funcionaria colado numa sessão limpa?
- **H3.4: paralelo por padrão, sequencial só com dependência real de dados.** Research → copy é sequencial (copy consome o research); email + subject lines é paralelo. Documentar a escolha no "Por que esse dispatch".
- **H3.5: referência temporal dentro de command é bug latente.** "Durante a migração", "quando X existir": remove ao encontrar (falha F-CMD-02; precedente vivo em `criar-post.md:54`).

## 4. Melhorar a skill orquestradora (`skills/marketing-os/SKILL.md`)

- **H4.1: a SKILL roteia, não executa.** Mapa de dispatch + regras de desempate + padrões de orquestração. Conteúdo de domínio que crescer ali deve descer pra um agent.
- **H4.2: toda ambiguidade recorrente de roteamento vira regra de desempate escrita** (ex: mos-brand vs mos-storytelling já tem; oferta high-ticket entre infoproduct/funnel/copy ainda não tem: gap conhecido, ver ADR-0001).
- **H4.3: mudou description de agent, mudou SKILL, mudou command? Rode os routing evals** (`pytest scripts/tests/test_routing_evals.py`) e revise a matriz em [ROUTING-EVALS.md](ROUTING-EVALS.md).

## 5. Reduzir contexto e tokens

- **H5.1: contexto é orçamento por camada.** Ordem de custo de carga: Tier 1 (sempre carregado quando a sessão abre) > SKILL (carrega ao invocar) > Tier 2/swipe-files/clones (sob demanda). Otimizações valem mais quanto mais alta a camada.
- **H5.2: leia a PARTE, não o arquivo.** Instrução no Tier 1 deve apontar seção específica da KB. "Leia a KB inteira" só se a tarefa realmente varre domínios.
- **H5.3: sumário no Tier 1 + profundidade no Tier 2 elimina o meio-termo.** Resumo de 30 linhas que duplica a KB é o pior dos mundos: gasta contexto e drifta (falha F-BLOAT-03).
- **H5.4: entregue top 2-3, gere 5-10.** Auto-iteração gera volume interno; o output final é curado. Volume no output é custo pro usuário e pro contexto da sessão-mãe.
- **H5.5: determinístico antes de modelo.** Se um script resolve (score de headline, lint de gates, contagem), rode o script. Ver [COST-CONTROL.md](COST-CONTROL.md).

## 6. Adicionar workflows novos

- **H6.1: workflow é padrão de orquestração documentado, não automação.** Ele descreve sequência de dispatch + por que a ordem importa. Automação stateful (fila, cron, retry) está fora do escopo do plugin (`docs/ROADMAP.md`).
- **H6.2: nasce na SKILL.md (seção Padrões de Orquestração); ganha arquivo em `workflows/` apenas se precisar de profundidade que não cabe lá.** Se ganhar arquivo, cross-link nos dois sentidos e no command que o usa (drift conhecido: 7 de 10 workflows hoje órfãos de cross-link).
- **H6.3: todo workflow declara: agents na ordem, o que passa de um pro outro (handoff), e critério de pronto.**

## 7. Decidir a forma: command, skill, agent, subagent-KB, hook ou script

| Se a necessidade é... | A forma certa é... | Porque... |
|---|---|---|
| Regra objetiva, bloqueante, universal (regex-detectável) | **Hook** (`scripts/hooks/`) | Roda no harness em todo Write/Edit, independe de obediência do modelo |
| Cálculo/validação determinística reutilizável | **Script** (`scripts/` + mos.py + teste) | Testável, barato, não gasta modelo |
| Expertise de domínio com contexto isolado e output schema | **Agent Tier 1** | Contexto próprio, tools próprias, memory própria |
| Profundidade de conhecimento do domínio | **Subagent-KB Tier 2** | Carregada sob demanda, evolui sem mexer no dispatch |
| Workflow empacotado com inputs conhecidos | **Command** | Porta de entrada explícita, dispatch pré-desenhado |
| Roteamento de briefing aberto entre domínios | **Skill orquestradora** | Já existe (SKILL.md); estenda o mapa, não crie outra |
| Sequência multi-agent recorrente | **Workflow (padrão documentado)** | Ver §6 |

Regras de desempate:

- **H7.1: se cabe em regex, é hook; se cabe em função pura, é script; modelo é o último recurso.**
- **H7.2: agent novo exige domínio que não é subconjunto de agent existente.** Teste: escreva a regra de desempate contra os vizinhos; se não conseguir, é seção de KB de um agent existente, não agent novo.
- **H7.3: command novo exige workflow com inputs estruturáveis e recorrência real.** Pedido raro roteia bem via SKILL/linguagem natural; não precisa de command.
- **H7.4: a mesma regra em 3+ arquivos exige fonte canônica + referência**, ou guard test que trave a sincronia (os quality gates hoje violam isso; plano no ADR-0002).

## 8. Evitar overengineering

- **H8.1: a régua de escopo do produto é `docs/ROADMAP.md`.** O plugin gera e valida; agendar, publicar em massa e mover dinheiro é papel de MCP/ferramenta externa. Feature que empurra pra ops/automação stateful: fora.
- **H8.2: não construa medição para o que nunca variou.** Guard test nasce de incidente real ou de risco com precedente na taxonomia, não de "seria bom validar".
- **H8.3: abstração na segunda repetição, não na primeira.** Um caso é caso; dois casos são padrão; três exigem fonte canônica (H7.4).
- **H8.4: feature de agent que nenhum briefing exercita é peso morto.** Antes de adicionar capability, aponte o routing eval ou caso de uso que a exercita.
- **H8.5: prefira frase sem número a número com guard, e número com guard a número solto.** Contagens em prosa são a maior fonte de drift do repo (falha F-DOC-01).
- **H8.6: se a "melhoria" não muda nenhuma rubrica de [RUBRICS.md](RUBRICS.md), questione se é melhoria.**
