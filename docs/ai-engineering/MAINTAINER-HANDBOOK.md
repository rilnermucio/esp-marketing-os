# Manual do mantenedor

> Canônico. Atualizado em 2026-07-06. Receitas passo a passo pras tarefas recorrentes. Cada receita termina na mesma linha: validar + atualizar contagens + registrar. Público: humano ou agente de IA.

## Pontos de sincronia (decorar isto evita 80% do drift)

Quando algo muda, estes lugares carregam contagens ou listas que precisam acompanhar:

| Mudança | Sincronizar em |
|---|---|
| Command novo/removido | `README.md` (linha 3, seção "Slash commands" + tabela, seção "Estrutura"), `AGENTS.md` (§"O que é" + §dispatch), `SKILL.md` (§"Slash commands rápidos" + tabela), `test_commands_dispatch.py` (`UTILITY_COMMANDS` se utility) |
| Agent novo/removido | os mesmos 3 docs (contagem "18") + `SKILL.md` mapa de dispatch + routing evals |
| Memory num agent | `init_agent_memory.py`, contagem de memory nos 3 docs, tabela de agents do README |
| Clone novo | `assets/clones/clone-manifest.yaml`, PARTE XV-B do `copy-agent.md` (inventário), contagem de clones nos docs |
| Regra de gate | ver [QUALITY-GATES.md](QUALITY-GATES.md) §atualização (hook → testes → CLI → tabelas derivadas) |

Heurística permanente: prefira reescrever a frase sem o número (H8.5).

## Como adicionar um agent Tier 1

1. Justifique contra **H7.2** (domínio não é subconjunto de agent existente) e escreva a regra de desempate contra os vizinhos. Se for decisão estrutural, ADR antes.
2. Crie `agents/mos-<nome>.md`. Requisitos:
   - `name` idêntico ao filename (validator trava).
   - `description` com triggers concretos em PT-BR (palavras que o usuário digita).
   - `tools` coerentes com o prompt (H1.2): fact-check exige WebSearch; rodar scripts exige Bash.
   - `model` por capacidade (ver [COST-CONTROL.md](COST-CONTROL.md) §2): opus só pra raciocínio pesado.
   - `hooks` PreToolUse com `${CLAUDE_PLUGIN_ROOT}/scripts/hooks/quality_gate_hook.py` (path relativo quebra fora do dev local: gotcha documentado).
   - Corpo: use `agents/mos-copy.md` como referência de estrutura (protocolo, gates, output schema, anti-padrões).
3. `memory: project`? Só se passa no critério H1.3. Se sim: bloco de memory no prompt (o que salvar / o que NÃO salvar), entrada no `scripts/init_agent_memory.py`, contagens.
4. Crie a KB `subagents/<nome>-agent.md` com índice no topo (H2.2) e snapshot guards em seções datadas (H2.3). O Tier 1 referencia PARTEs específicas.
5. Adicione ao mapa de dispatch da `SKILL.md` (+ regra de desempate).
6. Adicione ≥1 caso ao golden set de roteamento que exercite o agent.
7. Valide: `python scripts/validate_agents.py --strict` + suite + contagens (tabela acima).

## Como adicionar um command

1. Justifique contra **H7.3** (workflow recorrente com inputs estruturáveis).
2. Crie `commands/<nome>.md` com a anatomia mínima de **H3.2** (frontmatter, required inputs, decision tree se houver ramos, dispatch com prompt auto-contido, `## Consolidação`, referência a quality gates, "Por que esse dispatch").
3. Contratos automáticos que ele precisa passar (`test_commands_dispatch.py`): frontmatter com description; ≥1 `Agent(subagent_type: "mos-*")` com agent existente; marcador de consolidação; referência a quality gates. Utility genuíno: adicionar a `UTILITY_COMMANDS` com comentário.
4. Golden set: caso novo ou atualização de caso existente (ex: RT-013 espera `/criar-teste-ab` um dia).
5. Contagens nos 3 docs (tabela de sincronia) + tabela de categorias.
6. Suite completa.

## Como adicionar um workflow

Seguir **H6**: nasce como padrão na `SKILL.md`; só ganha arquivo em `workflows/` se precisar de profundidade. Com arquivo: cross-link SKILL ↔ arquivo ↔ command que o usa.

## Como atualizar um voice clone

1. Os 4 arquivos do clone em `assets/clones/<nome>/`: `profile.md`, `frameworks.md`, `voice.md` (o que o mos-copy lê primeiro), `examples.md`.
2. Registrar/atualizar em `assets/clones/clone-manifest.yaml` (specialty, best_for, niches).
3. Clone novo: inventário na PARTE XV-B do `copy-agent.md` + contagem de clones nos docs.
4. Manter `assets/clones/design/` fora da conta de voice clones (é o DNA visual do mos-design, exceção documentada).

## Como atualizar um quality gate

Receita completa em [QUALITY-GATES.md](QUALITY-GATES.md) §"Como atualizar sem quebrar". Resumo da ordem: hook → testes (positivos E negativos) → CLI → tabelas derivadas → suite.

## Como rodar testes

| O quê | Comando |
|---|---|
| Tier padrão (rápido, sem rede) | `python -m pytest scripts/tests/ -m "not smoke" -q` |
| Um arquivo/caso | `python -m pytest scripts/tests/test_x.py -v` / `::TestClasse::test_caso` |
| Smoke (exige tokens/sessão) | `python -m pytest scripts/tests/ -m smoke -v` |
| Validação de agents | `python scripts/validate_agents.py --strict` |
| Manifests Claude | `claude plugin validate .` |
| Pacote Codex | `python scripts/build_codex_plugin.py && python scripts/validate_codex_plugin.py` |
| Lint (CI bloqueia) | `black --check scripts/ && flake8 scripts/` |
| Routing evals | `python -m pytest scripts/tests/test_routing_evals.py -q` |

## Como diagnosticar falhas

| Sintoma | Primeiro passo |
|---|---|
| Install do plugin falha sem mensagem | [runbooks/install-failure-debug.md](runbooks/install-failure-debug.md) |
| `test_pdf_generator::test_cli_basic` falhou na suite cheia | Re-rodar isolado; flaky conhecido sob carga (F-EVAL-03) |
| Hook bloqueou escrita inesperadamente | Ver regex e `SKIP_PATH_PATTERNS` em `quality_gate_hook.py`; se falso positivo legítimo, ajustar regex COM teste do caso ([QUALITY-GATES.md](QUALITY-GATES.md)) |
| Briefing roteou pro agent errado | Comparar com o golden set; corrigir description/SKILL ou atualizar gabarito ([ROUTING-EVALS.md](ROUTING-EVALS.md) §camada viva) |
| Suspeita de drift docs↔realidade | Rodar a varredura da Fase 0 do [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md); se recorrente, auditoria completa (OPERATING-MODEL §quando auditar) |
| Validator acusa "script referenciado sem Bash" | Ou adicione Bash à tools list ou remova a instrução morta (F-BLOAT-02) |
| Bug novo sem categoria | Classificar em [FAILURE-TAXONOMY.md](FAILURE-TAXONOMY.md); se não couber, criar ID novo lá ANTES do fix |

## Ao terminar qualquer receita

1. Suite + validators verdes.
2. Contagens sincronizadas (tabela do topo).
3. Worklog da rodada ([IMPLEMENTATION-LOG.md](IMPLEMENTATION-LOG.md)).
4. Rubricas aplicáveis ≥ 3 ([RUBRICS.md](RUBRICS.md)).
