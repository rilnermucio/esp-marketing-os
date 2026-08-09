# 2026-08-08: Hardening após auditoria Grok

**Executor**: Codex (GPT-5.6), com auditoria passiva do Grok 4.5 via Paseo
**Objetivo**: verificar as recomendações externas no estado real do repositório e implementar somente os itens aprovados: paths de memory, robustez do validador universal, consistência de voice clones, higiene da taxonomia e cobertura de testes.
**Fora de escopo declarado**: commit, push, tag, release, publicação pública, alteração de branch protection, refactor amplo das knowledge bases, MCP para ChatGPT e instalação adicional na conta web.

## Arquivos lidos (relevantes pra decisão)

- `AGENTS.md`, `docs/ai-engineering/OPERATING-MODEL.md`, `docs/ai-engineering/HEURISTICS.md` e `docs/ai-engineering/MAINTAINER-HANDBOOK.md`: contratos de manutenção, evidência e distribuição.
- `commands/*.md`, `agents/mos-*.md`, `subagents/*-agent.md` e `scripts/init_agent_memory.py`: fonte canônica dos paths de memory e do inventário de clones.
- `scripts/validate_codex_plugin.py`, `scripts/build_codex_plugin.py` e testes de distribuição: comportamento do validador e sincronização do pacote universal.
- `docs/ai-engineering/FAILURE-TAXONOMY.md`, `RUBRICS.md` e `EVALS-STRATEGY.md`: classificação dos achados e critérios de aceite.
- `docs/ai-engineering/evals/routing-cases.json` e `ROUTING-EVALS.md`: contratos RT-028 e RT-031 para ChatGPT Work.
- `docs/ai-engineering/worklogs/2026-08-05-chatgpt-work-skills-only.md`: fronteira entre instalação local no app desktop e disponibilidade web.

## Arquivos alterados/criados

- `commands/batch.md`, `campanha-*.md` afetados e `publicar-anuncio.md`: paths legados `marketing-os-*` substituídos pelos diretórios canônicos `mos-*`.
- `scripts/tests/test_commands_dispatch.py`: guard que proíbe o prefixo legado de agent memory.
- `scripts/validate_codex_plugin.py`: descoberta do repo root pela presença de `.agents/plugins/marketplace.json`, aceitando raiz, fonte ou pacote gerado.
- `scripts/tests/test_codex_distribution.py`: cobertura dos novos pontos de entrada do validador.
- `docs/ai-engineering/OPERATING-MODEL.md`, `MAINTAINER-HANDBOOK.md`, `RUBRICS.md` e `runbooks/install-failure-debug.md`: receita canônica alinhada ao pacote gerado.
- `subagents/{ads,brand,copy,design,infoproduct-builder,launch,social}-agent.md`: inventário normalizado para 34 voice clones.
- `scripts/tests/test_repo_consistency.py`: contagem dinâmica de clones e paridade entre os 21 agents e a matriz de smoke.
- `scripts/tests/test_agents_smoke.py`: cenários adicionados para `mos-community`, `mos-offer` e `mos-partnerships`.
- `scripts/tests/test_auditoria_smoke.py`, `test_auditoria_pro_smoke.py` e `pytest.ini`: integrações offline determinísticas promovidas para a suíte padrão; marcador smoke reservado a runtime externo.
- `docs/ai-engineering/FAILURE-TAXONOMY.md`: F-CMD-02 e F-CODEX-03 atualizados como incidentes resolvidos.
- `plugins/marketing-os/`: pacote universal regenerado a partir da fonte canônica.
- `docs/ai-engineering/IMPLEMENTATION-LOG.md` e este worklog: índice e evidências da rodada.

## Decisões (e alternativas rejeitadas)

- Corrigir o drift de memory e adicionar guard. A divergência textual era confirmada; falha funcional total foi tratada como hipótese porque os Tier 1 já usam os paths corretos.
- Encontrar o repo root subindo a árvore até o marketplace. Restringir o CLI a um único CWD manteria a receita frágil para agentes e mantenedores.
- Comparar contagens de inventário com o filesystem. Um assert fixo em 34 voltaria a exigir manutenção manual quando um clone fosse adicionado.
- Limitar o detector de contagem a frases de inventário e disponibilidade. Números de exemplos, subconjuntos e combinações por fase não representam o total do catálogo.
- Manter os nomes históricos `test_auditoria*_smoke.py`. Remover o marcador altera a seleção do pytest sem produzir uma renomeação sem ganho funcional.
- Completar a matriz smoke com os 21 agents e travar a paridade por AST. Conferência manual da lista repetiria F-EVAL-02.
- Não enviar RT-031 como texto literal sem o plugin selecionado. A conta web não expôs o Marketing OS, então essa resposta seria um falso positivo do modelo geral.
- Manter versão e publicação intactas. A autorização cobriu implementação e validação local, sem commit ou release.

## Evidências

- Auditoria externa foi executada em modo somente leitura; cada recomendação da shortlist foi confrontada com grep, filesystem, testes e documentação canônica antes da aprovação.
- O grep final encontrou zero referências a `.claude/agent-memory/marketing-os-` em `commands/`.
- O filesystem contém 34 diretórios de clone conformes e a busca final encontrou zero alegações residuais de 35 clones em agents e subagents.
- `validate_codex_plugin.py` aprovou tanto `.` quanto `plugins/marketing-os`.
- A coleta do smoke de agents passou de 18 para 21 casos e cobre os 21 arquivos `agents/mos-*.md`.
- As quatro integrações offline de `/auditoria` e `/auditoria-pro` passaram na suíte padrão.
- Computer use nativo abriu o ChatGPT Work no Chrome e verificou a origem pessoal. A conta web mostrou zero habilidades instaladas e somente Magnific e Leadflow em plugins pessoais; Marketing OS permaneceu restrito à instalação local do app desktop.
- O computer use nativo recusou controlar `com.openai.codex` por segurança. RT-031 e RT-028 não foram enviados, preservando a classificação de execução viva como pendente.
- Nenhum commit, push, tag ou release foi criado.

## Testes

- Rodados: `python -m pytest scripts/tests/test_commands_dispatch.py -q`: 322 passed.
- Rodados: `python -m pytest scripts/tests/test_codex_distribution.py -q`: 8 passed.
- Rodados: testes focados de consistência e auditoria: 85 passed.
- Rodados: `python -m pytest scripts/tests/test_agents_smoke.py --collect-only -q`: 21 casos coletados.
- Rodados: `python -m pytest scripts/tests/ -q -m "not smoke" -W error::DeprecationWarning --cov=scripts --cov-report=term --cov-report=xml --cov-fail-under=70`: 2.261 passed, 2 skipped, 22 deselected, cobertura 70,88%.
- Rodados: `python scripts/validate_agents.py --strict`: 21/21 clean.
- Rodados: build, `build_codex_plugin.py --check` e validador universal nos dois pontos de entrada: aprovados.
- Rodados: `black --check --diff scripts/*.py scripts/hooks/`: 58 arquivos inalterados; `flake8 scripts/`: aprovado; `git diff --check`: aprovado.
- Rodados: `claude plugin validate .`: aprovado com o warning histórico de `category` no manifesto Claude.
- Não rodados e motivo: 22 smoke tests de runtime externo; RT-031 e RT-028 no app desktop, pois o computer use nativo bloqueia o próprio app Codex e a instalação local não aparece na conta web; CI remota, commit e release, fora da autorização.

## Falhas da taxonomia tocadas

- F-CMD-02: referências obsoletas foram diferenciadas de incidentes já encerrados.
- F-DOC-01: totais de clones agora seguem o filesystem por guard executável.
- F-EVAL-02: a matriz smoke falha se um agent novo não receber cenário.
- F-CODEX-01: validador universal aceita os pontos de entrada documentados e o pacote regenerado.
- F-CODEX-03: o incidente histórico deixou de aparecer como P0 aberto.
- F-ROUTE-02 e F-REL-03: execução viva no ChatGPT Work permanece pendente com causa observada.

## Rubrica aplicada

- R1 Implementação: 4. Cada drift corrigido recebeu teste focado ou guard dinâmico e a suíte integral está verde.
- R2 Documentação: 4. Receitas, taxonomia, pacote gerado e worklog ficaram sincronizados.
- R3 Roteamento: 3. Golden set e testes estáticos estão verdes; RT-031 e RT-028 continuam sem resposta viva observada.
- R4 Output de marketing: N/A. A rodada não produz peça de marketing.
- R5 Compatibilidade ChatGPT Work / Claude Code / Codex: 3. Manifests, pacote e validadores estão verdes; a instalação web diverge da instalação local desktop.
- R6 Release: N/A. Nenhuma ação de release foi autorizada.
- Veredito: implementação pronta para revisão local; release deve aguardar os dois casos vivos no app desktop.

## Custo aproximado

- Não medido. Paseo, Grok, Codex e computer use não expuseram custo monetário consolidado nesta rodada.

## Riscos e follow-ups

- O working tree ainda contém o WIP de ChatGPT Work iniciado em 2026-08-05 junto com esta rodada. Uma revisão de diff precisa separar intenção anterior de hardening novo antes de versionar.
- Marketing OS está instalado no marketplace pessoal local do app desktop, mas não aparece nas habilidades nem nos plugins pessoais da conta web observada.
- RT-031 e RT-028 ainda exigem uma conversa Work no app desktop. A resposta precisa ser registrada em `ROUTING-EVALS.md` antes de elevar R3 e R5 para 4.
- Os smoke tests dos 21 agents dependem de runtime Claude e podem continuar bloqueados pela política da organização.

## Próximos passos

- Abrir manualmente uma conversa Work nova no app desktop, selecionar Marketing OS e executar RT-031 seguido de RT-028.
- Registrar acerto ou divergência em `ROUTING-EVALS.md` e atualizar as notas R3/R5 deste worklog.
- Revisar o WIP completo e pedir autorização separada antes de commit, push, tag ou release.
