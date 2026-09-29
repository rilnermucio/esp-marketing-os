# ADR-0007: Dispatch garantido pela plataforma em command de agent único (`context: fork`)

**Status**: aceito (piloto em `/gerar-imagem`)
**Data**: 2026-09-28
**Autor**: Claude Opus 5.5

## Contexto

Dos 51 commands, 47 despacham um especialista por instrução em texto: o corpo do command manda o modelo da sessão chamar `Agent(subagent_type: "marketing-os:mos-*")`. O dispatch depende de o orquestrador seguir a instrução e acertar o nome. As duas falhas já aconteceram: produção inline (F-ROUTE-01, 8 de 25 commands antes da v6.5) e nome curto recusado com "Agent type not found" (F-DIST-05, auditoria 2026-09-28). Os guards de `test_commands_dispatch.py` conferem o texto do command, não o comportamento em runtime.

A plataforma oferece outro caminho. Com `context: fork` e `agent: <plugin>:<agent>` no frontmatter, o corpo do command vira a tarefa do agent, executada em contexto isolado, sem o orquestrador decidir nada. A sonda de 2026-09-28 (Claude Code 2.1.283, `--plugin-dir`) confirmou o comportamento em arquivo de `commands/` e em skill: o `SubagentStop` chegou com `agent_type` qualificado. O limite também foi medido: o agent em fork não vê o histórico da conversa, só `$ARGUMENTS` e os arquivos do projeto.

## Decisão

Usar `context: fork` com `agent: marketing-os:mos-<agent>` e `background: false` em command que atende os quatro critérios:

1. Despacha um único agent.
2. Todo o input vem do pedido (`$ARGUMENTS`) e de arquivos do projeto, como `workspace/brand/perfil.md`.
3. Não tem aprovação humana entre etapas.
4. Não tem dispatch paralelo nem sequencial entre agents.

Regras para o corpo desse command:

- Ele é escrito como tarefa do agent, com `Pedido do usuário: $ARGUMENTS`, `## Tarefa`, `## Saída (...)` e quality gates. Instruções ao orquestrador ficam fora dele.
- Pedido incompleto devolve apenas as perguntas que faltam e para. O agent não supõe o que foi combinado antes, porque não vê a conversa.
- Ofertas de continuação ficam numa seção separada, que o orquestrador usa depois do retorno.

O piloto é `/gerar-imagem` (`mos-ai-tools`). Os próximos candidatos que atendem os critérios são `/renderizar-imagem` e `/narrar-roteiro`. A expansão depende de o piloto rodar em uso real sem regressão de qualidade nem reclamação de contexto perdido.

Contratos:

- `test_commands_dispatch.py::dispatched_agents()` conta o `agent:` do frontmatter como dispatch, então os guards de cobertura, agent existente e utility valem para os dois estilos.
- `test_plugin_runtime_paths.py::test_fork_commands_use_qualified_agent` exige o nome qualificado e `background: false`.
- `test_routing_evals.py` lê o fork ao casar o golden set com os commands.
- `build_codex_plugin.py` reescreve `marketing-os:mos-` para `mos-` no pacote universal. ChatGPT Work e Codex não têm subagent e executam o corpo como tarefa.
- Prova de runtime: `test_install_smoke.py::test_fork_command_runs_inside_declared_agent` roda `/marketing-os:gerar-imagem` num projeto vazio e confirma o `SubagentStop` de `marketing-os:mos-ai-tools` avaliado pelo gate.

## Alternativas consideradas

1. **Manter só o dispatch por texto**: rejeitada para commands que atendem os critérios. A plataforma dá uma garantia que a instrução em texto não dá, sem custo de manutenção.
2. **Converter os 47 commands de uma vez**: rejeitada. A regra 1 do OPERATING-MODEL pede medir antes de refatorar. O fork também perde o histórico da conversa, o que quebra commands que retomam turnos anteriores, e não cobre commands com vários agents ou aprovação no meio.
3. **Mover o piloto para `skills/` com `context: fork`**: rejeitada. Criaria uma segunda skill invocável pelo modelo, disputando o roteamento com a skill orquestradora `marketing-os`, sem ganho sobre o command, que já aceita `context: fork`.

## Consequências

Positivas: no piloto, o dispatch passa a ser garantido pela plataforma e não depende de o orquestrador seguir a instrução nem de acertar o nome. O agent recebe contexto limpo, e o gate de `SubagentStop` continua avaliando a resposta final.

Negativas (custo aceito): pedido que depende da conversa ("o prompt daquela imagem que discutimos") chega sem esse contexto. A mitigação é a regra de pedido incompleto, que devolve perguntas. Convivem dois estilos de command, documentados no AGENTS.md e cobertos pelos mesmos guards.

## Critério de revisão

Expandir para os candidatos quando o piloto tiver uso real sem regressão. Reverter se a plataforma mudar a semântica de `context: fork` em commands de plugin ou se a perda do histórico virar reclamação recorrente.
