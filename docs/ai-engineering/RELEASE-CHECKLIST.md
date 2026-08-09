# Release Checklist (ChatGPT Work + Claude Code + Codex)

> Canônico. Atualizado em 2026-08-05. Executar item a item, registrando evidência por item no worklog da release. Pular passo é F-REL. Incidentes que moldaram este checklist: installs quebrados v6.1.0→v6.1.6 (manifests), tags v6.7/v6.8 apontando pra commit fora do main e divergências entre metadados aceitos localmente e pela listagem pública universal.

## Fase 0: pré-condições

- [ ] Working tree limpo (`git status`) e branch main atualizada.
- [ ] Suite verde: `python -m pytest scripts/tests/ -m "not smoke" -q`
  - Se `test_pdf_generator::test_cli_basic` falhar na suite cheia, re-rode isolado antes de investigar (flaky conhecido, F-EVAL-03).
- [ ] `python scripts/validate_agents.py --strict` limpo (CI também roda, mas valide local).
- [ ] Varredura rápida de drift: contagens em README/AGENTS/SKILL batem com `ls commands/*.md | wc -l`, nº de agents, nº de clones. Divergência: corrigir ANTES do bump (F-DOC-01).

## Fase 1: conteúdo da release

- [ ] `git log --oneline <última-tag>..HEAD` revisado por inteiro.
- [ ] `CHANGELOG.md` ganha a seção da versão nova cobrindo TODO o range, agrupado Added/Changed/Fixed (F-REL-02). Data no formato do arquivo.
- [ ] Decidir versão por semver: breaking em estrutura de dispatch/manifests = major; agent/command/feature novo = minor; correção = patch.

## Fase 2: manifests, listagem universal e versão

- [ ] `.claude-plugin/plugin.json` → `version`
- [ ] `.claude-plugin/marketplace.json` → `version` top-level E `plugins[0].version` (2 pontos no mesmo arquivo)
- [ ] `.codex-plugin/plugin.json` → base igual à nova versão + sufixo `+codex.YYYYMMDD` do dia (F-CODEX-02)
- [ ] Conformidade com a tabela de gotchas do `AGENTS.md` re-verificada se QUALQUER campo além de version mudou: author como object, category singular, source `./`, sem field `skills`, description/version top-level no marketplace (F-MAN-01)
- [ ] Metadados universais revalidados: `shortDescription` ≤ 30, categoria pública aceita, 1 a 3 starter prompts e ausência de `apps`/`mcpServers` no pacote skills-only.
- [ ] `skills/marketing-os/SKILL.md` usa somente frontmatter portátil e `skills/marketing-os/agents/openai.yaml` mantém invocação implícita sem product gating.
- [ ] `claude plugin validate .` verde

## Fase 3: pacote universal ChatGPT Work e Codex

- [ ] `python scripts/build_codex_plugin.py` gera o pacote sem erro
- [ ] `python scripts/validate_codex_plugin.py plugins/marketing-os` verde (F-CODEX-01)
- [ ] Inspeção anti-vazamento do pacote gerado: nada de `workspace/`, `.claude/agent-memory/`, arquivos pessoais soltos (áudio, drafts) (F-CODEX-03). Conferir contra `COPY_DIRS`/`COPY_FILES` do build script.
- [ ] Se houver cópia para marketplace pessoal: `test ! -L <destino>` passa, `realpath <destino>` difere de `pwd -P` e o destino é uma pasta física fora do repo. `rsync --delete` fica proibido sem esse preflight (F-CODEX-04).

## Fase 4: commit, tag e push

- [ ] Commit de release no main: `release: vX.Y.Z` (inclui manifests + CHANGELOG + qualquer fix de drift da Fase 0).
- [ ] **Verificação de ancestralidade antes de taggear** (lição v6.7/v6.8, F-REL-01):
  ```bash
  git tag -a vX.Y.Z -m "vX.Y.Z"
  git merge-base --is-ancestor vX.Y.Z main && echo "OK: tag alcançável do main" || echo "PARE: tag fora do main"
  ```
- [ ] Anotar rollback antes do push: `git push` é publicação; reversão de tag publicada exige delete remoto + retag (procedimento no histórico da v6.7/v6.8, ver memória do projeto).
- [ ] `git push && git push --tags`

## Fase 5: teste real de install (validate é necessário, não suficiente)

- [ ] **ChatGPT Work**: instalar a origem repo-scoped no ChatGPT Desktop, abrir conversa Work nova, confirmar `@Marketing OS` e rodar pelo menos um caso `RT-028` a `RT-031`.
- [ ] **Claude Code**: em projeto limpo, `/plugin install marketing-os@mos-marketplace`; abrir sessão; rodar 1 command de produção (ex: `/criar-post`) e 1 briefing em linguagem natural do golden set ([ROUTING-EVALS.md](ROUTING-EVALS.md), camada viva) (F-REL-03).
- [ ] **Codex**: `codex plugin marketplace add rilnermucio/esp-marketing-os --ref vX.Y.Z` + install; abrir e verificar que os especialistas respondem.
- [ ] Install falhou sem mensagem clara? [runbooks/install-failure-debug.md](runbooks/install-failure-debug.md).

## Fase 6: pós-release

- [ ] Docs que citam versão explícita atualizados (badge do README acompanha automaticamente? conferir).
- [ ] Worklog da release criado (template do [IMPLEMENTATION-LOG.md](IMPLEMENTATION-LOG.md)) com evidência por fase.
- [ ] Rubrica R6 preenchida; release só sai com tudo ≥ 3.
