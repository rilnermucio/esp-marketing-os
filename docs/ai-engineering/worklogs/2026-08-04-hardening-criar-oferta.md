# 2026-08-04: Hardening da arquitetura de oferta

**Executor**: Codex (GPT-5)
**Objetivo**: corrigir as lacunas verificadas em `/criar-oferta`: alinhar o roteamento high-ticket com pesquisa prévia, preservar o Dossiê de USP, tornar evidências e claims parte explícita da entrega, criar regressões dedicadas e eliminar o drift da skill legada.
**Fora de escopo declarado**: produzir uma oferta real sem briefing e evidências do cliente; revisar juridicamente todos os claims históricos da knowledge base; adicionar um novo agent; executar smoke tests com rede; publicar versão, commit, push, tag, release ou instalação limpa.

## Arquivos lidos (relevantes pra decisão)

- `docs/ai-engineering/OPERATING-MODEL.md`, `HEURISTICS.md`, `RUBRICS.md`, `EVALS-STRATEGY.md`, `ROUTING-EVALS.md`, `FAILURE-TAXONOMY.md` e `MAINTAINER-HANDBOOK.md`: processo obrigatório, rubricas, arquitetura e contrato do golden set.
- `commands/criar-oferta.md`, `agents/mos-offer.md` e `subagents/offer-agent.md`: interface pública, Tier 1 e knowledge base da Oferta.
- `commands/criar-usp.md`, `agents/mos-brand.md` e `subagents/brand-agent.md`: contrato produtor do Dossiê de USP que a Oferta precisa consumir sem reinterpretação silenciosa.
- `agents/mos-research.md` e `subagents/research-agent.md`: dependência de pesquisa em ofertas core e high-ticket sem contexto validado.
- `skills/marketing-os/SKILL.md`, `.agents/skills/source-command-marketing-os/SKILL.md` e `commands/mo.md`: roteamento canônico, compatibilidade legada e meta-orquestrador.
- `scripts/tests/test_commands_dispatch.py`, `test_routing_evals.py`, `test_repo_consistency.py`, `test_codex_distribution.py` e `test_workspace_separation.py`: contratos estáticos afetados.
- `scripts/build_codex_plugin.py` e `validate_codex_plugin.py`: geração e validação da distribuição Codex.

## Arquivos alterados/criados

- `scripts/tests/test_offer_command.py`: seis regressões para RT-017, handoff de USP, protocolo de evidências, adaptador legado, rota natural e meta-roteador.
- `commands/criar-oferta.md`: inputs de USP e pesquisa, sequência condicional, protocolo de evidências, claims aprovados e bloqueados, plano de validação e handoff verificável.
- `agents/mos-offer.md`: preflight do Dossiê de USP, preservação de IDs e limites, classes de evidência, schema de saída e quality gate adicional.
- `subagents/offer-agent.md`: contrato profundo para consumir USP, manter ledger `OE/OI/OH`, registrar claims e transformar hipóteses em plano de validação.
- `docs/ai-engineering/evals/routing-cases.json`: RT-017 corrigido para `mos-research` seguido de `mos-offer`, com campos mínimos de evidência, claims e handoff.
- `skills/marketing-os/SKILL.md` e `commands/mo.md`: rota natural e meta-rota explícitas para Oferta, com pesquisa condicional.
- `.agents/skills/source-command-marketing-os/SKILL.md`: conteúdo duplicado e desatualizado substituído por um adaptador fino para a skill canônica.
- `README.md`, `docs/ROADMAP.md`, `docs/VALIDATION-GUIDE.md`, `docs/ai-engineering/ROUTING-EVALS.md` e `HEURISTICS.md`: descoberta, estado da feature, teste manual e gabarito sincronizados.
- `plugins/marketing-os/`: pacote Codex regenerado a partir das fontes canônicas.
- `docs/ai-engineering/IMPLEMENTATION-LOG.md` e este worklog: índice e registro da rodada.

## Decisões (e alternativas rejeitadas)

- Corrigir RT-017 para dispatch sequencial `mos-research` seguido de `mos-offer`. Oferta core ou high-ticket sem pesquisa possui dependência real de avatar, alternativas, objeções e evidências; dispatch simples faria a etapa de Oferta trabalhar com suposições.
- Manter pesquisa condicional. Forçar `mos-research` em qualquer oferta repetiria trabalho quando o usuário já fornece pesquisa suficiente e rastreável.
- Consumir o Dossiê de USP como handoff versionado e preservar `primary_usp`, `reason_to_believe`, mecanismo, IDs de evidência, limites de claim e hipóteses abertas. Reescrever esses campos silenciosamente criaria duas fontes de verdade.
- Permitir Oferta sem Dossiê de USP, mas classificar promessa e mecanismo ainda não provados como hipótese e recomendar `/criar-usp` quando a ausência bloquear diferenciação confiável. Tornar USP obrigatória quebraria briefings simples e ofertas já maduras.
- Adotar IDs próprios `OE`, `OI` e `OH` para evidência confirmada, inferência e hipótese da Oferta, mantendo os IDs recebidos da USP. Reaproveitar IDs com novo significado destruiria a rastreabilidade entre etapas.
- Expor ledger de evidências, Claims Aprovados, Claims Bloqueados e plano de validação na saída. Fact-check apenas interno não impede que uma hipótese seja reutilizada depois como promessa factual.
- Substituir a skill legada por adaptador fino. Atualizar manualmente a antiga tabela de 18 agents manteria duas arquiteturas concorrentes e recriaria o drift na próxima mudança.
- Incluir `/criar-oferta` no meta-roteador `/mo`. Deixar a feature apenas no mapa canônico reduziria a descoberta por briefing aberto.
- Manter a arquitetura atual sem ADR novo. A correção aplica as decisões existentes de command, Tier 1, Tier 2, golden set e pacote gerado.

## Evidências

- Estado inicial: RT-017 esperava apenas `mos-offer`, enquanto o decision tree de `/criar-oferta` exigia pesquisa prévia para core e high-ticket sem research.
- Estado inicial: não existia `scripts/tests/test_offer_command.py`; a feature dependia apenas de testes genéricos de command e roteamento.
- Estado inicial: `/criar-oferta`, `mos-offer` e `offer-agent` não declaravam consumo do Dossiê de USP nem preservação dos IDs e limites de claim introduzidos por `/criar-usp`.
- Estado inicial: evidências eram tratadas no raciocínio interno, sem ledger, registro de claims aprovados e bloqueados ou plano de validação obrigatório na saída.
- Estado inicial: `.agents/skills/source-command-marketing-os/SKILL.md` duplicava a arquitetura antiga de 18 agents e não descobria Oferta, Avatar e USP; `commands/mo.md` também não expunha a rota de Oferta.
- TDD 1: a regressão de RT-017 falhou porque o caso retornava `['mos-offer']`; passou depois de registrar `['mos-research', 'mos-offer']` como dispatch sequencial.
- TDD 2: o teste de handoff falhou pela ausência de `Dossiê de USP`; passou depois da integração em command, Tier 1 e Tier 2.
- TDD 3: o teste de claims falhou pela ausência de `protocolo de evidências`; passou depois da inclusão do ledger, Claims Aprovados, Claims Bloqueados e plano de validação.
- TDD 4: o teste da skill legada falhou porque não havia delegação para `skills/marketing-os/SKILL.md`; passou depois da substituição pelo adaptador fino.
- TDD 5: o teste de roteamento natural falhou porque a skill canônica não possuía `Rota condicional: Oferta`; passou após a seção ser adicionada. O matcher foi ajustado apenas para aceitar quebra de linha Markdown, sem relaxar o contrato semântico.
- TDD 6: o teste do meta-roteador falhou porque `/mo` não continha `/criar-oferta`; passou após a rota explícita ser adicionada.
- Suite focada final: 502 testes passaram, cobrindo Oferta, dispatch, routing evals, consistência, distribuição Codex e separação de workspace.
- Suite estrita final: 2.177 testes passaram, 2 foram pulados e 23 smoke tests foram excluídos; cobertura total 70,83%.
- `validate_agents.py --strict`: 21/21 agents clean, zero warnings e zero falhas.
- Build Codex: pacote regenerado, `--check` sem drift e validator aprovado.
- `claude plugin validate .`: aprovado com o warning histórico de `category`, campo aceito e ignorado pelo Claude Code.
- Black, flake8, `git diff --check` e validação JSON: aprovados.

## Testes

- Rodados em ciclos vermelhos independentes: `python -m pytest scripts/tests/test_offer_command.py -q`, com falha observada antes de cada uma das seis correções de contrato descritas nas evidências.
- Rodados durante a implementação: `python -m pytest scripts/tests/test_offer_command.py scripts/tests/test_commands_dispatch.py scripts/tests/test_routing_evals.py scripts/tests/test_repo_consistency.py -q`: 496 passed no checkpoint anterior à sincronização do pacote.
- Rodados: `python -m pytest scripts/tests/test_offer_command.py scripts/tests/test_commands_dispatch.py scripts/tests/test_routing_evals.py scripts/tests/test_repo_consistency.py scripts/tests/test_codex_distribution.py scripts/tests/test_workspace_separation.py -q`: 502 passed.
- Rodados: `python -m pytest scripts/tests/ -q -m "not smoke" -W error::DeprecationWarning --cov=scripts --cov-report=term --cov-report=xml --cov-fail-under=70`: 2.177 passed, 2 skipped, 23 deselected, cobertura 70,83%.
- Rodados: `python scripts/validate_agents.py --strict`: 21/21 clean.
- Rodados: `black --check --diff scripts/*.py scripts/hooks/` e `flake8 scripts/`: aprovados.
- Rodados: `python scripts/build_codex_plugin.py`, `python scripts/build_codex_plugin.py --check` e `python scripts/validate_codex_plugin.py plugins/marketing-os`: aprovados.
- Rodados: `claude plugin validate .`: aprovado com warning conhecido de `category`.
- Rodados: `git diff --check` e `python -m json.tool docs/ai-engineering/evals/routing-cases.json`: aprovados.
- Não rodados e motivo: 23 smoke tests, pois exigem rede, credenciais ou sessão externa; nova execução viva de RT-017, pois esta rodada valida a arquitetura de forma determinística e não executa chamadas headless pagas; geração de uma oferta real, pois faltam briefing, Dossiê de USP e provas do cliente; instalação Claude/Codex em projeto limpo, pois não houve publicação de versão.

## Falhas da taxonomia tocadas

- F-ROUTE-02 e F-ROUTE-04: Oferta agora possui rota natural, meta-rota e golden case coerentes com o decision tree.
- F-DISP-01 e F-DISP-02: RT-017 usa sequência causal e transporta research, USP, evidências e limites entre etapas.
- F-CLAIM-01: claims recebem classe, ID, fonte ou origem, escopo, confiança, limite de uso e status aprovado ou bloqueado.
- F-DOC-01 e F-REG-01: documentação pública, skill legada e testes dedicados foram sincronizados com o contrato atual.
- F-CODEX-01 e F-CODEX-03: pacote Codex regenerado, validado e sem drift da fonte canônica.

## Rubrica aplicada

- R1 Implementação: 4. Seis contratos nasceram vermelhos, receberam correções mínimas e terminaram com a suite integral verde.
- R2 Documentação: 4. README, skill, meta-roteador, guia, roadmap, heurística, matriz e worklog foram sincronizados.
- R3 Roteamento: 3. RT-017, mapa natural, `/mo`, dispatch e testes determinísticos estão verdes; a nova composição interna ainda não foi repetida na camada viva.
- R4 Output de marketing: N/A. O contrato foi fortalecido, mas nenhuma oferta de cliente foi produzida e avaliada nesta rodada.
- R5 Compatibilidade Claude Code/Codex: 3. Manifest e pacote passam e não existe drift; instalação real em projeto limpo ficou fora desta rodada.
- R6 Release: N/A. Nenhuma release foi executada.
- Veredito: apto para revisão e merge junto das mudanças autorizadas anteriores; release ainda exige checklist próprio, teste vivo e instalação limpa.

## Custo aproximado

- Custo agregado da sessão Codex não foi exposto. Nenhuma chamada headless paga foi executada nesta rodada.

## Riscos e follow-ups

- O contrato e o roteamento estão verificados de forma estática. A qualidade de uma oferta completa precisa ser avaliada com briefing, pesquisa, Dossiê de USP e provas reais.
- A camada viva histórica de RT-017 comprovou a escolha do command, mas não a nova sequência interna nem o handoff enriquecido. Essa evidência precisa ser renovada antes do release.
- A knowledge base contém orientações históricas sobre claims e garantias que não receberam revisão jurídica nesta rodada. O novo registro reduz propagação acidental, mas não substitui validação legal no contexto do produto e do país.
- Uma instalação existente só receberá a correção depois de versão, release, atualização do plugin e abertura de uma nova sessão para evitar cache antigo.
- O worktree já continha mudanças autorizadas de hardening, Avatar e USP. Nenhum arquivo foi revertido, e esta rodada permanece sem commit ou push.

## Próximos passos

- Executar `/criar-oferta` com um produto real, Dossiê de Avatar, Dossiê de USP, research e inventário de provas.
- Rodar RT-017 na camada viva e avaliar o output com R4, incluindo rastreabilidade dos claims e utilidade do plano de validação.
- Depois da aprovação do diff combinado, preparar CHANGELOG, versão, commit e release pelo checklist canônico.
