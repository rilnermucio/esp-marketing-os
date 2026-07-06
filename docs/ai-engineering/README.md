# Engenharia de IA do Marketing OS

> Camada de processo que torna a evolução do plugin **acumulativa, auditável e segura**.
> Criada em 2026-07-06. Mantenedor: humano ou agente de IA atuando como mantenedor sênior.

## Propósito

O Marketing OS é mantido majoritariamente por agentes de IA sob supervisão humana. Sem processo, cada sessão de IA recomeça do zero, repete erros já cometidos e produz melhorias que ninguém consegue medir. Esta pasta resolve isso: ela é o contrato de trabalho entre quem mantém (humano ou modelo) e o repositório.

Regra de ouro, na ordem: **medir antes de refatorar**. Nenhuma refatoração ampla acontece sem que exista rubrica, eval ou guard test capaz de dizer se ela melhorou ou piorou o sistema.

## Como usar esta pasta

**Se você é um agente de IA** começando uma sessão de manutenção:

1. Leia `AGENTS.md` na raiz (arquitetura, comandos, gotchas). Ele aponta pra cá.
2. Leia [OPERATING-MODEL.md](OPERATING-MODEL.md): define como trabalhar, quando auditar, quando pedir aprovação, como registrar.
3. Consulte o arquivo específico da sua tarefa (tabela abaixo).
4. Ao terminar qualquer rodada não-trivial: crie um worklog em [worklogs/](worklogs/) usando o template de [IMPLEMENTATION-LOG.md](IMPLEMENTATION-LOG.md).

**Se você é humano**: use as rubricas pra revisar PRs de agentes, os worklogs pra auditar o que foi feito, e os ADRs pra entender por que a arquitetura é como é.

## Arquivos canônicos

| Arquivo | Papel | Quando consultar |
|---|---|---|
| [OPERATING-MODEL.md](OPERATING-MODEL.md) | **Canônico.** Modelo de trabalho do mantenedor | Início de toda sessão |
| [HEURISTICS.md](HEURISTICS.md) | **Canônico.** Heurísticas de design e decisão | Antes de criar/alterar agent, command, skill, hook ou script |
| [RUBRICS.md](RUBRICS.md) | **Canônico.** Rubricas 0-4 + threshold de merge | Antes de dar algo por pronto |
| [FAILURE-TAXONOMY.md](FAILURE-TAXONOMY.md) | **Canônico.** Taxonomia de falhas com IDs | Ao diagnosticar bug, escrever eval ou post-mortem |
| [EVALS-STRATEGY.md](EVALS-STRATEGY.md) | **Canônico.** Estratégia de avaliação | Ao adicionar teste/eval novo |
| [ROUTING-EVALS.md](ROUTING-EVALS.md) | **Canônico.** Matriz de roteamento esperado | Ao mexer em SKILL.md, descriptions de agents ou commands |
| [QUALITY-GATES.md](QUALITY-GATES.md) | **Canônico.** As 3 camadas de gates de qualidade | Ao alterar regras de output |
| [COST-CONTROL.md](COST-CONTROL.md) | **Canônico.** Política de custo, contexto e modelo | Ao escolher model, escopo ou volume de output |
| [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md) | **Canônico.** Checklists Claude Code + Codex | Em toda release |
| [MAINTAINER-HANDBOOK.md](MAINTAINER-HANDBOOK.md) | **Canônico.** Receitas operacionais (como adicionar X) | Ao executar tarefa recorrente |
| [IMPLEMENTATION-LOG.md](IMPLEMENTATION-LOG.md) | Template + índice de worklogs | Ao fechar uma rodada |
| [adr/](adr/) | Registro de decisões de arquitetura | Decisões estruturais ou difíceis de reverter |
| [evals/](evals/) | Dados de eval (golden sets) | Consumidos por testes em `scripts/tests/` |
| [runbooks/](runbooks/) | Procedimentos de diagnóstico | Quando algo quebra |
| [worklogs/](worklogs/) | Registro histórico de rodadas | Leitura de contexto; escrita ao fechar rodada |

## Relação com o resto do repo

- `AGENTS.md` (raiz) é o mapa do repositório; esta pasta é o **processo** de quem o mantém. Em conflito, `AGENTS.md` vence sobre fatos do repo; esta pasta vence sobre método de trabalho.
- Os guard tests em `scripts/tests/` são a materialização executável desta camada. Eval sem teste é aspiração; regra sem guard é pedido.
- `docs/` (pai) documenta o produto pro usuário final. Esta pasta documenta a engenharia pra quem mantém.
