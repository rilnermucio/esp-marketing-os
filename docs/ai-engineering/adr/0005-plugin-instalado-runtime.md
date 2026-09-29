# ADR-0005: Plugin instalado: recursos pela raiz do plugin, dispatch qualificado e gates no nível do plugin

**Status**: aceito
**Data**: 2026-09-28
**Autor**: Claude Opus 5.5

## Contexto

Toda a validação do plugin rodava com a sessão dentro do próprio repo: a suíte estática, os smoke tests (`cwd=project_root`) e os testes manuais do mantenedor. Numa instalação real a sessão roda no projeto do usuário e o plugin fica num cache versionado. A auditoria de 2026-09-28 mediu o que muda nesse cenário, com doc oficial do Claude Code e uma sonda empírica (`claude -p --plugin-dir`, sessão fora do repo, Claude Code 2.1.283):

1. Caminho relativo a `subagents/`, `scripts/`, `assets/` e `references/` não resolve. O agent respondeu NOT-FOUND para a própria KB depois de 10 tentativas. Havia 291 referências assim em 36 arquivos.
2. `${CLAUDE_PLUGIN_ROOT}` é substituído no corpo de agents, commands e skills de plugin; com ele, a KB foi lida na primeira tentativa.
3. Agent de plugin recebe nome qualificado (`marketing-os:mos-copy`). O nome curto no dispatch falha com "Agent type 'mos-growth' not found".
4. A plataforma ignora `hooks`, `mcpServers` e `permissionMode` no frontmatter de agent de plugin. O gate de escrita declarado nos 21 agents nunca rodou instalado.
5. O `SubagentStop` de `hooks/hooks.json` dispara, mas o hook descartava todo `agent_type` que não começasse com `mos-`. O gate da resposta final também nunca rodou.
6. Stderr com exit 0 vai só para o log de debug. Os avisos de clichê e compliance nunca chegaram ao modelo.
7. Três scripts gravavam estado do usuário dentro da pasta do plugin, que é trocada a cada update.

O smoke de instalação criado nesta rodada (`scripts/tests/test_install_smoke.py`) reproduziu 1, 4 e 5 no plugin real antes de qualquer correção.

## Decisão

Tratar o plugin instalado como o alvo de todas as superfícies de runtime:

1. **Recursos do plugin via `${CLAUDE_PLUGIN_ROOT}`** em agents, commands e SKILL.md. Comandos de terminal levam o caminho entre aspas. Cada agent declara que as pastas citadas dentro das KBs (arquivos lidos sem substituição) ficam na raiz do plugin. Guard: `test_plugin_runtime_paths.py`.
2. **Dispatch com nome qualificado** `marketing-os:mos-*`. Guard no mesmo arquivo.
3. **Quality gate registrado no nível do plugin**: `hooks/hooks.json` declara `PreToolUse` (`Write|Edit|MultiEdit`) e `SubagentStop`. O bloco `hooks:` sai do frontmatter dos agents (ignorado em plugin; em instalação local o placeholder vazio faria o launcher falhar fechado). Guard: `test_agents_do_not_declare_frontmatter_hooks`.
4. **Escopo por agent**: `marketing_agent()` aceita `marketing-os:mos-*` e o nome curto de instalação local, e recusa agents de outros plugins. Escrita da sessão principal do usuário nunca passa pelo gate.
5. **Canal de saída**: bloqueio em exit 2 com motivo em stderr; avisos em JSON `hookSpecificOutput.additionalContext`; correção esgotada libera com `systemMessage` para o usuário e contexto para o agent que consolida.
6. **Exclusões de caminho** por extensão (código e config), pelo segmento `.claude/` e pela raiz de uma cópia do Marketing OS (exceto `workspace/`). Diretórios como `docs/` deixam de ser ignorados por substring.
7. **Estado do usuário** em `workspace/` do diretório da sessão (`scripts/workspace_paths.py`, override `MOS_WORKSPACE`). Guard: `test_workspace_paths.py`.
8. **Pacote universal**: `build_codex_plugin.py` desfaz 1 e 2 (`adapt_for_universal`), porque ChatGPT Work e Codex resolvem caminhos pela pasta da skill e não têm subagent nativo.
9. **Régua obrigatória**: mudança em hooks, caminhos, nomes de agent, memória ou manifests roda o smoke de instalação (`MOS_SMOKE=1`) antes do merge e no checklist de release.

## Alternativas consideradas

1. **Só uma linha declarando a raiz, sem prefixar cada caminho**: rejeitada. Comandos de terminal falham quando o modelo esquece de aplicar a base, e não há como escrever um guard determinístico para "o modelo lembrou".
2. **Copiar as KBs para o projeto do usuário num bootstrap**: rejeitada. Duplica cerca de 70 mil linhas por projeto e desatualiza a cada update do plugin.
3. **Manter os hooks no frontmatter e documentar a instalação local**: rejeitada. A plataforma ignora o campo em plugin, que é o único canal de distribuição.
4. **Gate em toda escrita da sessão**: rejeitada. Bloquearia trabalho do usuário que não tem relação com o Marketing OS.
5. **Resolver o nome do agent só pelo matcher do hooks.json**: o matcher `mos-.*` continua como primeiro filtro, mas a decisão fica em Python, onde é testável com payload real.

## Consequências

Positivas: KBs, scripts, clones e gates passam a funcionar na instalação real, com medição antes e depois pelo smoke; payloads reais viram fixtures (`scripts/tests/fixtures/hook_payloads/`); a classe inteira tem guard.

Negativas (custo aceito): os prompts ficam mais longos, porque o caminho absoluto é substituído em cada referência; o texto dos prompts agora depende do build para o pacote universal; os avisos passam a chegar ao modelo e podem provocar reescritas extras (monitorar ruído).

Relação com ADRs anteriores: mantém as decisões da ADR-0002 (hook como fonte canônica, três camadas) e da ADR-0003 (núcleo puro, `SubagentStop`, uma tentativa de correção) e corrige a fiação que elas assumiam.

## Critério de revisão

Reabrir se a plataforma passar a resolver nome curto de agent de plugin, honrar `hooks` no frontmatter de agent de plugin ou se ChatGPT Work e Codex passarem a substituir `${CLAUDE_PLUGIN_ROOT}`.
