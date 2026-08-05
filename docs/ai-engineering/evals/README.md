# Golden sets de avaliação

Dados consumidos por testes determinísticos em `scripts/tests/`. Editar um arquivo aqui exige rodar o teste correspondente.

| Arquivo | Teste consumidor | Documentação |
|---|---|---|
| [routing-cases.json](routing-cases.json) | `scripts/tests/test_routing_evals.py` | [../ROUTING-EVALS.md](../ROUTING-EVALS.md) |
| [copy-output-cases.json](copy-output-cases.json) | `scripts/tests/test_copy_output_evals.py` | [copy-output-baseline.md](copy-output-baseline.md) |
| [baselines/copy/](baselines/copy/) | (artefatos de referência par-a-par; comparados via `scripts/copy_output_eval.py pair`) | [copy-output-baseline.md](copy-output-baseline.md) |
| [`scripts/evals/output-profiles.json`](../../../scripts/evals/output-profiles.json) | `scripts/tests/test_copy_output_evals.py` | [quality-anchors.md](quality-anchors.md) |

O arquivo de perfis fica sob `scripts/evals/` para entrar no pacote Codex. Ele define agent, tipo do quality gate e conjunto de critérios para copy, e-mail, anúncios, oferta, funil, SEO e vídeo. A CLI mantém os aliases legados de `--formato` e também aceita `--profile`.

Formato dos routing cases: `id` (RT-NNN), `prompt` (briefing PT-BR literal), `expected_command` (nome do command sem barra, ou null), `expected_agents` (lista de `mos-*`), `dispatch` (`simples` | `paralelo` | `sequencial` | `nenhum`), `min_output_fields` (o que a resposta precisa conter), `detects` (IDs da FAILURE-TAXONOMY), `notes` (opcional).

Convenção do campo `dispatch` (calibrada pela camada viva em 2026-07-06, caso RT-021): rotula o modo dominante do **pipeline completo** do command. Paralelismo interno de uma fase não muda o rótulo; um pipeline de fases encadeadas é `sequencial` mesmo que uma fase dispare 2 agents em paralelo.
