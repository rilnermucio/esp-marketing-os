# Golden sets de avaliação

Dados consumidos por testes determinísticos em `scripts/tests/`. Editar um arquivo aqui exige rodar o teste correspondente.

| Arquivo | Teste consumidor | Documentação |
|---|---|---|
| [routing-cases.json](routing-cases.json) | `scripts/tests/test_routing_evals.py` | [../ROUTING-EVALS.md](../ROUTING-EVALS.md) |

Formato dos routing cases: `id` (RT-NNN), `prompt` (briefing PT-BR literal), `expected_command` (nome do command sem barra, ou null), `expected_agents` (lista de `mos-*`), `dispatch` (`simples` | `paralelo` | `sequencial` | `nenhum`), `min_output_fields` (o que a resposta precisa conter), `detects` (IDs da FAILURE-TAXONOMY), `notes` (opcional).

Convenção do campo `dispatch` (calibrada pela camada viva em 2026-07-06, caso RT-021): rotula o modo dominante do **pipeline completo** do command. Paralelismo interno de uma fase não muda o rótulo; um pipeline de fases encadeadas é `sequencial` mesmo que uma fase dispare 2 agents em paralelo.
