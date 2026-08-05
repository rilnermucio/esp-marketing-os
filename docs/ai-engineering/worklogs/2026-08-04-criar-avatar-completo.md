# 2026-08-04: Criação de avatar como feature explícita

**Executor**: Codex (GPT-5)
**Objetivo**: transformar a capacidade dispersa de persona do Marketing OS em uma interface pública de avatar completo, com evidências, segmentação, anti-avatar, JTBD e handoff reutilizável pelos agents de execução.
**Fora de escopo declarado**: criar um avatar real de um negócio específico sem briefing e dados do cliente; adicionar um novo agent; conectar CRM ou ferramenta de entrevistas; commit, push, tag, release e instalação real em projeto limpo.

## Arquivos lidos (relevantes pra decisão)

- `docs/ai-engineering/OPERATING-MODEL.md`, `HEURISTICS.md`, `RUBRICS.md`, `EVALS-STRATEGY.md` e `ROUTING-EVALS.md`: processo, forma correta de command, rubricas e gabarito de roteamento.
- `scripts/tests/test_commands_dispatch.py`, `test_routing_evals.py`, `test_repo_consistency.py` e `test_workspace_separation.py`: contratos estáticos afetados pela nova interface.
- `agents/mos-research.md` e `subagents/research-agent.md`: ownership atual de Audience Research, JTBD, persona e validação de fontes.
- `assets/personas/persona-template.md` e `personas-por-nicho.md`: template anterior e banco distribuído de referências por nicho.
- `skills/marketing-os/SKILL.md`, `commands/mo.md`, `commands/criar-email.md` e `commands/criar-funil.md`: roteamento natural, meta-orquestração e anatomia de commands existentes.
- `README.md`, `AGENTS.md`, `docs/VALIDATION-GUIDE.md` e `docs/TROUBLESHOOTING.md`: superfícies públicas e contagens a sincronizar.
- `scripts/build_codex_plugin.py` e `validate_codex_plugin.py`: geração e validação da distribuição Codex.

## Arquivos alterados/criados

- `commands/criar-avatar.md`: nova interface com pre-flight, decision tree, dispatch simples auto-contido, schema de consolidação e quality gates.
- `scripts/tests/test_avatar_command.py`: guarda existência, dispatch exclusivo, contrato mínimo e reuso entre command, agent, template e skill.
- `assets/personas/persona-template.md`: contrato canônico com ledger, maturidade, segmentação, papéis de compra, avatar principal, segmentos secundários condicionais, anti-avatar, linguagem documentada, plano de validação e handoff JSON.
- `agents/mos-research.md`: triggers de avatar, buyer persona, ICP e anti-avatar; uso obrigatório do template e schema específico de Dossiê de Avatar.
- `subagents/research-agent.md`: protocolo profundo alinhado ao template, banco tratado como hipótese e prompt legado de persona ampliado.
- `skills/marketing-os/SKILL.md` e `commands/mo.md`: rota explícita para `/criar-avatar` em linguagem natural e no meta-orquestrador.
- `docs/ai-engineering/evals/routing-cases.json` e `ROUTING-EVALS.md`: RT-026 e evidência da execução viva.
- `README.md`, `AGENTS.md`, `docs/VALIDATION-GUIDE.md` e `docs/TROUBLESHOOTING.md`: descoberta da feature, contagens 43/47 e documentação de validação sincronizadas.
- `plugins/marketing-os/`: pacote Codex regenerado a partir das fontes canônicas.
- `docs/ai-engineering/IMPLEMENTATION-LOG.md` e este worklog: índice e registro da rodada.

## Decisões (e alternativas rejeitadas)

- Implementar um command sobre `mos-research`. Um agent novo duplicaria Audience Research, JTBD, WebSearch e triangulação já existentes, contrariando H7.2.
- Centralizar profundidade em `persona-template.md` e manter o Tier 1 como roteador do contrato. Copiar todo o schema para `mos-research` aumentaria contexto permanente e drift.
- Tratar personas pré-construídas como referências e hipóteses. Promovê-las automaticamente a fatos repetiria o principal risco apontado pelo usuário: completude aparente sem base verificável.
- Criar um único avatar principal e aceitar segmentos secundários apenas com diferença acionável comprovada. Gerar várias personas decorativas diluiria decisões de mídia, oferta e mensagem.
- Classificar maturidade como exploratória, validada ou operacional. Um dossiê feito só com fontes externas permanece útil, mas não recebe o mesmo grau de confiança de dados próprios e comportamento de compra.
- Usar handoff JSON com consumidores nomeados. Texto livre exigiria que cada agent reinterpretasse o avatar e criaria versões divergentes.
- Manter a arquitetura existente sem ADR novo. A mudança segue as regras já decididas para command, Tier 1, Tier 2 e pacote gerado.

## Evidências

- Estado inicial: 46 commands, nenhum arquivo `commands/criar-avatar.md` e schema genérico de Research Brief no `mos-research` para pedidos de persona.
- Teste primeiro: a primeira execução focada terminou com 5 falhas e 131 passes, cobrindo command ausente, contrato ausente e RT-026 apontando para rota inexistente.
- Depois da implementação: 404 testes focados de avatar, commands e roteamento passaram; com consistência do repo, 482 passaram.
- A primeira suite completa encontrou uma referência proibida a caminho pessoal em `subagents/research-agent.md`; o texto foi corrigido e os 6 testes de avatar + separação passaram antes da repetição integral.
- Suite final: 2.155 testes passaram, 2 foram pulados e 23 smoke tests foram excluídos; cobertura total 70,82%.
- Camada viva RT-026: retorno estruturado exato `{"command":"/criar-avatar","agents":["mos-research"],"dispatch":"simples"}` com o plugin local carregado.
- `validate_agents.py --strict`: 21/21 agents clean, zero warnings e zero falhas.
- Build Codex: pacote regenerado, `--check` sem drift, validator aprovado e presença de `/criar-avatar` confirmada no artefato.
- `claude plugin validate .`: aprovado com o warning conhecido de `category`.
- Black, flake8, `git diff --check` e validação JSON: aprovados.

## Testes

- Rodados: `python -m pytest scripts/tests/test_avatar_command.py scripts/tests/test_commands_dispatch.py scripts/tests/test_routing_evals.py scripts/tests/test_repo_consistency.py -q`: 482 passed.
- Rodados: `python -m pytest scripts/tests/ -q -m "not smoke" -W error::DeprecationWarning --cov=scripts --cov-report=term --cov-report=xml --cov-fail-under=70`: 2.155 passed, 2 skipped, 23 deselected, cobertura 70,82%.
- Rodados: `python scripts/validate_agents.py --strict`: 21/21 clean.
- Rodados: `black --check --diff scripts/*.py scripts/hooks/` e `flake8 scripts/`: aprovados.
- Rodados: `python scripts/build_codex_plugin.py`, `python scripts/build_codex_plugin.py --check` e `python scripts/validate_codex_plugin.py plugins/marketing-os`: aprovados.
- Rodados: `claude plugin validate .`: aprovado com warning conhecido de `category`.
- Rodados: camada viva RT-026 via `claude -p` com o plugin local: 1/1 exato.
- Não rodados e motivo: 23 smoke tests, pois exigem rede, credenciais ou sessão externa; geração de um dossiê real, pois faltam briefing e evidências de um cliente; instalação Claude/Codex em projeto limpo, pois esta rodada não publica uma versão.

## Falhas da taxonomia tocadas

- F-ROUTE-02: briefing de avatar agora possui command, triggers e golden case próprios.
- F-DISP-02: o prompt do command carrega todos os inputs, fontes, entregáveis e gates necessários para uma sessão isolada.
- F-CLAIM-01: afirmações de avatar passam por ledger, classificação, fonte, data, geografia e confiança.
- F-DOC-01: contagens e tabelas públicas foram sincronizadas com os 47 commands.
- F-REG-01: o contrato novo ganhou teste dedicado e RT-026.
- F-CODEX-01 e F-CODEX-03: pacote regenerado, validado e sem vazamento de caminho pessoal.

## Rubrica aplicada

- R1 Implementação: 4. A interface nasceu com teste vermelho, guard dedicado, regressão de separação detectada e suite integral verde.
- R2 Documentação: 4. README, AGENTS, SKILL, guia, troubleshooting, matriz e worklog foram sincronizados.
- R3 Roteamento: 4. Description, mapa, meta-orquestrador, RT-026, testes determinísticos e camada viva exata.
- R4 Output de marketing: N/A. O contrato foi implementado, mas nenhum avatar de cliente foi produzido nesta rodada.
- R5 Compatibilidade Claude Code/Codex: 3. Manifest e pacote passam; instalação real em projeto limpo ficou fora do escopo.
- R6 Release: N/A. Nenhuma release foi executada.
- Veredito: apto para revisão e merge; release ainda exige checklist próprio e instalação real.

## Custo aproximado

- Validação viva Claude reportou US$ 2,434008 em duas tentativas: a primeira encerrou antes do resultado pelo teto de US$ 0,20; a segunda retornou o gabarito. O custo agregado da sessão Codex não foi exposto.

## Riscos e follow-ups

- Um dossiê baseado somente em fontes externas recebe maturidade exploratória. A promoção para validado exige dados próprios; para operacional, comportamento e vendas.
- A ingestão de CRM, entrevistas e suporte continua manual pelo briefing ou por arquivos fornecidos pelo usuário.
- O schema está verificado de forma estática e o roteamento foi verificado ao vivo; a qualidade de um dossiê completo ainda precisa de avaliação com um caso real e fontes reais.
- O worktree já continha mudanças autorizadas da rodada anterior. Nenhum arquivo foi revertido, e este trabalho permanece sem commit ou push.

## Próximos passos

- Executar `/criar-avatar` com um produto real, dados próprios disponíveis e decisão de marketing definida.
- Revisar as hipóteses de maior impacto com entrevistas, CRM, vendas ou testes de mensagem e elevar a maturidade do dossiê conforme a evidência.
- Após aprovação do diff combinado, preparar CHANGELOG, versão, commit e release pelo checklist canônico.
