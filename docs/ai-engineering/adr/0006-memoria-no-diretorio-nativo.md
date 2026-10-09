# ADR-0006: Memória dos agents no diretório nativo de agent de plugin

**Status**: aceito
**Data**: 2026-09-28
**Autor**: Claude Opus 5.5

## Contexto

Com `memory: project` no frontmatter, o Claude Code dá a cada subagent um diretório de memória e injeta no system prompt as primeiras 200 linhas ou 25 KB do `MEMORY.md` dali. Para agent de plugin, o diretório é `.claude/agent-memory/<plugin>-<agent>/`. A sonda de 2026-09-28 (Claude Code 2.1.283, `--plugin-dir`) mostrou o agent citando e criando `.claude/agent-memory/hookprobe-probe-writer/`.

Na v6.5.0 o plugin padronizou o contrário: `.claude/agent-memory/mos-<agent>/`, chamado de "path canônico" (`docs/VALIDATION-GUIDE.md`), e um guard em `test_commands_dispatch.py` passou a proibir o prefixo `marketing-os-`. A premissa era que os agents rodavam como locais. Instalado como plugin, o resultado era duas memórias por agent: a plataforma injetava `marketing-os-mos-*` (que o plugin nunca escrevia) e o bootstrap, o `memory_writer.py`, o `/aprender` e as instruções dos 21 agents usavam `mos-*` (que a plataforma não injeta). O loop de aprendizado da Fase 4 alimentava o diretório errado.

## Decisão

Adotar o diretório nativo `.claude/agent-memory/marketing-os-mos-<agent>/` como canônico em todo o plugin:

1. `scripts/init_agent_memory.py` expõe `memory_dir_name()` (`<plugin>-<agent>`, aceita nome curto ou qualificado), cria os diretórios nativos e migra o legado.
2. Migração sem perda: só o legado existe, então ele é renomeado; os dois existem, então o `MEMORY.md` antigo é anexado ao nativo sob `## Migrado de ...` e a pasta antiga vira `mos-<agent>.migrado`. Nada é apagado.
3. `scripts/memory_writer.py` grava no diretório nativo, aceita `marketing-os:mos-*` e migra o legado na primeira escrita, sem exigir novo bootstrap.
4. Agents, commands, SKILL.md, KBs e docs citam o caminho nativo. O guard de commands foi invertido: agora proíbe o caminho `mos-*`.
5. Prova de runtime: `test_install_smoke.py::test_bootstrap_memory_is_the_native_memory` roda o bootstrap num projeto vazio, grava um marcador e confirma que o agent real o recebe na memória injetada.

## Alternativas consideradas

1. **Manter `mos-*` e remover `memory: project` do frontmatter**: rejeitada. Perde a injeção automática, que entrega a memória sem chamada de ferramenta, e mantém uma convenção própria contra a da plataforma.
2. **Manter os dois diretórios e sincronizar**: rejeitada. Duplica estado e cria conflito de escrita sem ganho.
3. **Migrar apagando o legado**: rejeitada. Memória é dado do usuário; o custo de uma pasta `.migrado` é desprezível.

## Consequências

Positivas: a memória gravada pelo `/aprender` e pelo `memory_writer` chega ao agent sem leitura explícita; um só diretório por agent; migração automática.

Negativas (custo aceito): instalações locais fora do plugin (agent em `.claude/agents/` com nome curto) usariam `mos-*` pela regra da plataforma; esse modo não é distribuído e fica sem suporte. Projetos com memória antiga ganham uma pasta `.migrado` após a migração.

## Critério de revisão

Reabrir se a plataforma mudar a regra de nome do diretório de memória de agent de plugin ou se o plugin passar a ser distribuído também como agents locais.
