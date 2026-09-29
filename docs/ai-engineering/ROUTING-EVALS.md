# Routing Evals: matriz de roteamento esperado

> Canônico. Atualizado em 2026-09-28. O gabarito vivo está em [evals/routing-cases.json](evals/routing-cases.json); este documento explica a matriz e o protocolo. A tabela abaixo é um resumo de leitura; **em divergência, o JSON vence**.

## O que a matriz cobre

Briefings de usuário em PT-BR, como chegam de verdade e sem jargão de sistema, e o roteamento esperado: command de entrada, agents dispatchados, modo de dispatch e campos mínimos do output. A matriz inclui linguagem natural, slash commands e seleção explícita por `@Marketing OS` no ChatGPT Work. Cada caso lista quais falhas da [FAILURE-TAXONOMY.md](FAILURE-TAXONOMY.md) ele detecta se o roteamento errar.

## Resumo dos casos (gabarito completo no JSON)

| ID | Briefing (resumo) | Command | Agents | Dispatch |
|---|---|---|---|---|
| RT-001 | post pro Instagram sobre tema X | `/criar-post` | research + social | paralelo |
| RT-002 | "o que é AIDA?" | nenhum (inline) | nenhum | nenhum |
| RT-003 | melhorar headline existente | `/otimizar-copy` | copy | simples |
| RT-004 | campanha completa de lançamento | `/campanha-lancamento` | research, launch, funnel, copy, email, ads | sequencial |
| RT-005 | artigo SEO | `/criar-artigo` | research → seo → copy | sequencial |
| RT-006 | anúncio Meta Ads | `/criar-anuncio` | research + ads | paralelo |
| RT-007 | roteiro de VSL | `/criar-video` | storytelling + copy + video | paralelo |
| RT-008 | sequência carrinho abandonado | `/criar-email` | email + copy | paralelo |
| RT-009 | análise de concorrente | `/analisar-concorrencia` | research + brand + copy | paralelo |
| RT-010 | landing page high-ticket | `/criar-landing-page` | funnel + copy + design (fase 1) | paralelo |
| RT-011 | datas comerciais do mês | `/datas-sazonais` (utility) | nenhum | nenhum |
| RT-012 | publicar no Notion | `/publicar-notion` (utility) | nenhum | nenhum |
| RT-013 | desenhar teste A/B | `/criar-teste-ab` | ab-testing | simples |
| RT-014 | narrar roteiro em áudio | `/narrar-roteiro` | audio | simples |
| RT-015 | "por que o engajamento caiu?" | nenhum (linguagem natural) | analytics | simples |
| RT-016 | carrossel 10 slides | `/criar-carrossel` | social + copy + design | paralelo |
| RT-017 | montar oferta high-ticket sem research | `/criar-oferta` | research → offer | sequencial |
| RT-018 | bio do Instagram | nenhum (linguagem natural) | social | simples |
| RT-019 | "quanto cobrar pela mentoria?" | nenhum (linguagem natural) | offer | simples |
| RT-020 | renderizar prompt em PNG | `/renderizar-imagem` | ai-tools | simples |
| RT-021 | thumbnail com texto | `/gerar-thumbnail` | video + ai-tools | sequencial (pipeline) |
| RT-022 | reels renderizado com legenda | `/produzir-reels` | video → audio (via `/narrar-roteiro`) | sequencial |
| RT-023 | aprender com métricas reais | `/aprender` | analytics | simples |
| RT-024 | responder comentários com haters | `/responder-comentarios` | community | simples |
| RT-025 | achar influencers skincare collab | `/prospectar-creators` | research → partnerships | sequencial |
| RT-026 | criar avatar completo para mentoria | `/criar-avatar` | research | simples |
| RT-027 | criar USP sem concorrentes mapeados | `/criar-usp` | research → brand | sequencial |
| RT-028 | `@Marketing OS` criar avatar completo | `/criar-avatar` | research | simples |
| RT-029 | `@Marketing OS` criar USP sem mapa competitivo | `/criar-usp` | research → brand | sequencial |
| RT-030 | `@Marketing OS` criar oferta com inputs validados | `/criar-oferta` | offer | simples |
| RT-031 | `@Marketing OS` explicar AIDA | nenhum (inline) | nenhum | nenhum |
| RT-032 | experimentos para app estagnado | nenhum (linguagem natural) | growth | simples |
| RT-033 | transformar consultoria em curso | `/criar-infoproduto` | research + infoproduct | paralelo |
| RT-034 | auditoria premium para entregar ao cliente | `/auditoria-pro` | funnel + copy + design (entre 7) | paralelo |
| RT-035 | sequência coordenada email, posts e ads | `/criar-sequencia` | email + social + ads | paralelo |
| RT-036 | configurar perfil de marca do projeto | `/configurar-marca` | brand | simples |
| RT-037 | responder reclamações do Reclame Aqui | `/responder-comentarios` (modo avaliações) | community | simples |
| RT-038 | live vira posts, cortes e newsletter | `/reaproveitar` | social → video + email | sequencial |
| RT-039 | dores e objeções literais de reviews | `/minerar-voc` | research | simples |

RT-013 e RT-017 eram gaps documentados e viraram validações das correções. RT-017 agora também trava a dependência de dados: oferta core ou high-ticket sem research usa `mos-research` antes de `mos-offer`; pedido pontual de precificação com contexto suficiente continua simples em RT-019. RT-026 guarda a interface explícita de avatar completo e sua rota natural para `mos-research`. RT-027 guarda a interface de USP e sua dependência de pesquisa quando o contexto competitivo ainda não foi mapeado. RT-028 a RT-031 preservam esses contratos no ChatGPT Work: o prefixo `@Marketing OS` seleciona o plugin, mas o briefing restante continua governando command, dependências e decisão inline. Correções de 2026-09-28: RT-001 esperava `mos-copy`, que o `/criar-post` nunca despacha; RT-018 mandava bio para `mos-copy`, contra o mapa do SKILL.md; RT-007 e RT-010 rotulavam como sequencial commands que disparam os agents em paralelo. RT-032 a RT-035 cobrem `mos-growth` e `mos-infoproduct` (antes sem caso) e duas desambiguações (`/auditoria-pro`, `/criar-sequencia`); ainda não rodaram na camada viva. Casos novos entram pelo protocolo da EVALS-STRATEGY §2.

## Validação em duas camadas

**Camada determinística (roda em CI):**

```bash
python -m pytest scripts/tests/test_routing_evals.py -q
```

Valida: IDs únicos e bem-formados, commands/agents citados existem no repo, coerência dispatch↔agents (dispatch "nenhum" implica zero agents; "simples" implica exatamente 1; paralelo/sequencial implicam 2+), campos mínimos presentes, e todo ID em `detects` definido na taxonomia. Isso trava o gabarito contra drift estrutural: renomear um command ou agent quebra o teste na hora. Desde 2026-09-28 também cruza o gabarito com o corpo do command: todo agent esperado precisa ser despachado pelo command esperado (`TestGoldenSetMatchesCommands`); alcance via outro command é declarado em `indirect_agents` e verificado. A execução real dos agents instalados (leitura de KB, gates) é medida pelo smoke de instalação, não por esta camada.

**Camada viva (manual, por amostragem):**

Periodicamente (a cada release ou mudança em SKILL.md/descriptions), rode 5+ casos do gabarito em sessão real: cole o `prompt` numa sessão limpa com o plugin carregado e compare o roteamento observado com o esperado. Registre no worklog: casos rodados, acertos, divergências. Divergência tem dois desfechos possíveis: bug de roteamento (corrigir SKILL/description) ou gabarito desatualizado (corrigir o JSON com justificativa).

## Campos mínimos do output (`min_output_fields`)

Cada caso declara o que a resposta final precisa conter (ex: post exige sugestão de enquete; artigo exige meta title/description; teste A/B exige hipótese se-X-então-Y-porque-Z e amostra mínima). Hoje servem de checklist pra camada viva; são o esqueleto da futura camada LLM-graded ([EVALS-STRATEGY.md](EVALS-STRATEGY.md) §4).

## Execuções da camada viva (log)

| Data | Método | Casos | Acerto | Divergências |
|---|---|---|---|---|
| 2026-07-06 | `claude -p "<briefing>" --plugin-dir <repo> --max-turns 2` de diretório limpo, com meta-instrução pedindo só a decisão de roteamento | RT-001, 002, 003, 015, 017, 019 | **6/6** | Nenhuma. RT-001 retornou o command com namespace (`marketing-os:criar-post`), mesma rota. RT-017/019 validaram o desempate do mos-offer no dia do lançamento dele |
| 2026-07-06 | Mesmo método | RT-013 (pós /criar-teste-ab) | **1/1** | Nenhuma. O command criado na mesma rodada roteou exato (`criar-teste-ab`, ab-testing, simples) |
| 2026-07-06 | Mesmo método | RT-021 (pós Fase 2) | **1/1 em rota** (command + agents exatos) | Dispatch veio `sequencial` vs `paralelo` do gabarito: divergência de CONVENÇÃO, não de rota. O gabarito rotulava o paralelismo interno da Fase 1; a leitura correta (e consistente com RT-022) é o pipeline inteiro. Gabarito calibrado + convenção documentada abaixo |
| 2026-07-06 | Mesmo método | RT-023, 024, 025 (pós Fases 3-4 delegadas ao Composer) | **3/3** | Nenhuma. Os 3 roteamentos criados por executor delegado rotearam exatos ao vivo (RT-025 listou o par de agents em ordem invertida, mesma rota sequencial). Acumulado do dia: 12/12 em rota |
| 2026-07-06 | `claude -p` SEM `--plugin-dir` (plugin INSTALADO do marketplace, v6.13.0) | RT-024 | **1/1** | Nenhuma. Valida o artefato distribuído de ponta a ponta (install → load → roteamento) e fecha a F-REL-03 das 5 releases do dia. Acumulado: 13/13 |
| 2026-07-06 | Mesmo método, pós-nivelamento das 5 ondas (branch feat/nivelamento-completo) | RT-013, 014, 015, 021, 023 | **5/5 em command** (4/5 exatos em todos os campos) | RT-021: command exato em 5/5 execuções, mas a lista DECLARADA de agents variou entre sessões (design+ai-tools na branch, ai-tools no controle em main pré-nivelamento, video+ai-tools no registro da manhã). Controle no main provou: instabilidade do próprio método além da fronteira do command, não regressão do nivelamento. Refinamento documentado abaixo |
| 2026-08-04 | `claude -p` com `--plugin-dir .`, schema JSON e instrução de decidir sem executar | RT-026 | **1/1** | Nenhuma. Retorno estruturado exato: `/criar-avatar`, `mos-research`, dispatch `simples` |

Limitação do método: mede a decisão de roteamento DECLARADA pelo orquestrador em modo headless, não o dispatch executado numa sessão interativa completa. Suficiente pra pegar F-ROUTE-02/04; um eval de dispatch executado fica como evolução futura.

Refinamento (2026-07-06, pós-controle do RT-021): quando o briefing roteia pra um COMMAND, o critério de acerto da camada viva é `expected_command`. O corpo do command define os agents e o modo de dispatch deterministicamente na execução real; a enumeração de agents que o orquestrador DECLARA em headless (sem carregar o corpo do command) é instável entre sessões e não deve ser tratada como gabarito. Pra casos sem command (`expected_command: null`), agents + dispatch continuam sendo o critério.

Consequência para RT-017: a execução viva de 2026-07-06 comprovou a escolha de
`/criar-oferta`. Ela não comprova o pipeline interno corrigido em 2026-08-04,
que permanece coberto deterministicamente pelo command e por
`test_offer_command.py` até nova execução interativa.

## Como estender

Protocolo em [EVALS-STRATEGY.md](EVALS-STRATEGY.md) §2. Resumo: motivo real → taxonomia primeiro se a falha for nova → caso no JSON → teste verde → atualizar o resumo aqui → worklog.
