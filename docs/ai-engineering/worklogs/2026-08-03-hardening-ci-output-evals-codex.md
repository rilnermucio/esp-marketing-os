# 2026-08-03: Hardening de CI, output, evals e pacote Codex

**Executor**: Codex (GPT-5)
**Objetivo**: executar as prioridades da auditoria do projeto: restaurar o contrato da CI e da release, eliminar drift do pacote Codex, validar a resposta final dos agents e ampliar os evals além de copy.
**Fora de escopo declarado**: commit, push, tag, release, alteração remota de branch protection, instalação real em projeto limpo e criação de baselines positivos para os domínios recém-cobertos.

## Arquivos lidos (relevantes pra decisão)

- `docs/ai-engineering/OPERATING-MODEL.md`: processo obrigatório para rodada não-trivial.
- `.github/workflows/tests.yml` e `.github/workflows/release.yml`: contratos reais de CI e publicação.
- `requirements.txt` e `scripts/project_manager.py`: origem do `ModuleNotFoundError: yaml` em ambiente limpo.
- `scripts/build_codex_plugin.py` e `scripts/validate_codex_plugin.py`: superfície gerada e validação da distribuição Codex.
- `scripts/hooks/quality_gate_hook.py`, `hooks/hooks.json` e documentação oficial de hooks do Claude Code: eventos, campos e comportamento bloqueante.
- `scripts/copy_output_eval.py`, `docs/ai-engineering/evals/quality-anchors.md` e `docs/ai-engineering/EVALS-STRATEGY.md`: contrato anterior limitado a copy e consolidação manual.
- `README.md`, `CONTRIBUTING.md`, `docs/ROADMAP.md` e `docs/ai-engineering/MAINTAINER-HANDBOOK.md`: drifts documentais encontrados na auditoria.

## Arquivos alterados/criados

- `.github/workflows/tests.yml`: corrige o input `files` do Codecov.
- `.github/workflows/release.yml`: adiciona job de verificação e impede publicação antes de suite, cobertura, lint, agents e pacote Codex verdes.
- `requirements.txt`: declara PyYAML como dependência de runtime e alinha a versão documentada do Python à CI.
- `scripts/audit_config.py`: usa o identificador registrado do metaschema Draft 7.
- `scripts/hooks/quality_gate_hook.py` e `hooks/hooks.json`: adicionam núcleo puro compartilhado e gate `SubagentStop` para a resposta final dos `mos-*`.
- `scripts/copy_output_eval.py` e `scripts/evals/output-profiles.json`: adicionam perfis por domínio, score genérico, prompt por perfil e consolidação das duas ordens A/B.
- `scripts/tests/test_audit_config.py`, `test_ci_contract.py`, `test_codex_distribution.py`, `test_copy_output_evals.py`, `test_quality_gate_hook.py` e `test_repo_consistency.py`: guardam os contratos corrigidos.
- `plugins/marketing-os/`: pacote Codex regenerado a partir das fontes, incluindo os perfis de eval.
- `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `docs/ROADMAP.md`, `docs/ai-engineering/QUALITY-GATES.md`, `EVALS-STRATEGY.md`, `FAILURE-TAXONOMY.md`, `MAINTAINER-HANDBOOK.md` e docs de eval: sincronizam comportamento, setup e estado entregue.
- `docs/ai-engineering/adr/0003-gate-na-fronteira-de-output.md`: registra a nova fronteira de qualidade e suas limitações.

## Decisões (e alternativas rejeitadas)

- Repetir a verificação no workflow de release e torná-la dependência do job de publicação. Confiar apenas no workflow de testes permitiu uma release verde para o mesmo commit cuja CI falhou.
- Manter um único detector puro para eventos de escrita e resposta final. Duplicar regexes em cada agent aumentaria drift e F-BLOAT-03.
- Limitar o retry de `SubagentStop` a uma tentativa por `stop_hook_active`. Bloqueio indefinido criaria risco de loop.
- Manter a chamada ao julgador fora da suite e automatizar as partes determinísticas: perfis, prompt, validação de schema A/B e consolidação. Chamar modelo em todo teste traria rede, custo e flakiness.
- Colocar `output-profiles.json` em `scripts/evals/` para que o runner funcione também dentro do pacote Codex. Manter o arquivo apenas em `docs/` quebraria a distribuição gerada.
- Preservar o warning de `category` no validator Claude. O campo atende o gotcha histórico do Desktop e sua remoção exige instalação real antes de ser considerada segura.

## Evidências

- Workflow remoto da `main` falhou no commit auditado com `ModuleNotFoundError: No module named 'yaml'`; o workflow de release do mesmo commit concluiu com sucesso. Essa divergência motivou o gate de release.
- Baseline local antes da rodada: 2.116 testes passaram, 2 foram pulados, 23 foram excluídos; o comando exato da CI falhou com 68,29% para threshold de 70%.
- Resultado final: 2.139 testes passaram, 2 foram pulados, 23 smoke tests foram excluídos; cobertura total 70,83%.
- A suite final rodou com `DeprecationWarning` promovido a erro e terminou sem warnings.
- `validate_agents.py --strict`: 21 agents clean, zero warnings e zero falhas.
- Build Codex: pacote gerado, `--check` sem drift e validator aprovado; smoke do pacote executa `copy_output_eval.py profiles` e encontra `mos-video`.
- `claude plugin validate .`: aprovado, com um warning conhecido sobre `category`.
- API remota informou que `main` não possui branch protection no snapshot desta rodada.

## Testes

- Rodados: `python -m pytest scripts/tests/ -q -m "not smoke" -W error::DeprecationWarning --cov=scripts --cov-report=term --cov-report=xml --cov-fail-under=70`: 2.139 passed, 2 skipped, 23 deselected, cobertura 70,83%.
- Rodados: `python scripts/validate_agents.py --strict`: 21/21 clean.
- Rodados: `python scripts/build_codex_plugin.py && python scripts/build_codex_plugin.py --check && python scripts/validate_codex_plugin.py plugins/marketing-os`: todos aprovados.
- Rodados: `claude plugin validate .`: aprovado com warning conhecido de `category`.
- Rodados: `black --check --diff scripts/*.py scripts/hooks/` e `flake8 scripts/`: aprovados.
- Não rodados e motivo: 23 smoke tests, pois exigem sessão, rede ou credenciais externas; instalação real Claude/Codex e execução do hook dentro de sessão interativa, pois esta rodada não publica nem altera o plugin instalado; CI remota, pois não houve push.

## Falhas da taxonomia tocadas

- F-COPY-04: resposta final entregue em chat sem passar pelo gate.
- F-EVAL-04: viés de posição A/B no julgamento par a par.
- F-CODEX-01 e F-CODEX-03: pacote inválido, com drift ou superfície incompleta.
- F-MAN-01: compatibilidade dos manifests preservada e revalidada.
- F-DOC-01: cobertura, setup, roadmap, árvore e contagens sincronizados.
- F-REG-01: achados da auditoria convertidos em testes de contrato.

## Rubrica aplicada

- R1 Implementação: 4. Mudanças guiadas por testes negativos/positivos, interfaces puras e suite completa acima do gate.
- R2 Documentação: 4. Docs canônicas, ADR, taxonomia, roadmap e worklog atualizados no mesmo diff.
- R3 Roteamento: N/A. SKILL, descriptions e commands não tiveram contrato de dispatch alterado.
- R4 Output de marketing: N/A. A rodada alterou infraestrutura de qualidade, sem produzir peça publicável.
- R5 Compatibilidade Claude Code/Codex: 3. Validators e pacote passam; instalação real e adapter automático Codex para resposta final permanecem pendentes.
- R6 Release: N/A. Nenhuma release foi executada.
- Veredito: apto para revisão e merge; release requer os passos externos pendentes.

## Custo aproximado

- Não medido: a sessão local não expôs custo agregado confiável de tokens ou tempo de execução do modelo.

## Riscos e follow-ups

- A cobertura tem margem de 0,83 ponto percentual sobre o threshold. Código novo sem teste pode derrubar a CI rapidamente.
- `main` permanece sem branch protection; o workflow de release reduz risco de artefato ruim, mas não controla merge direto.
- O gate `SubagentStop` foi validado por contrato, CLI e documentação oficial, porém ainda precisa de execução em uma instalação Claude limpa.
- Codex continua sem adapter automático de resposta final; prompt e CLI são as camadas disponíveis nesse runtime.
- O warning de `category` continua intencional até teste real no Desktop.
- E-mail, anúncios, oferta, funil, SEO e vídeo têm critérios versionados, porém faltam âncoras positivas calibradas.

## Próximos passos

- Revisar o diff e, após aprovação, preparar versão, CHANGELOG, commit e push.
- Após push, confirmar os workflows `tests` e `release` em GitHub e configurar branch protection com os checks obrigatórios.
- Testar instalação Claude e Codex em projeto limpo, incluindo uma resposta `mos-copy` bloqueada e corrigida pelo `SubagentStop`.
- Criar e calibrar baselines positivos por domínio antes de usar os novos perfis como gate de release.
