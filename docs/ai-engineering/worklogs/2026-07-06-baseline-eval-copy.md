# Worklog: baseline do eval de output do mos-copy

- **Data**: 2026-07-06 (pós-release v6.14.0)
- **Motivação**: pergunta do mantenedor ("o mos-copy já é o melhor? precisa melhorar?"); resposta de engenharia: o prompt não é o gargalo, medição é. Sem baseline, qualquer mudança futura no agent é fé.
- **Executor**: mantenedor (Claude), sem delegação (design de eval é trabalho de especificação).

## O que nasceu

| Artefato | Papel |
|----------|-------|
| `evals/copy-output-cases.json` | 5 golden briefs (headline, post, email, ad, sales) com pre-flight completo |
| `scripts/copy_output_eval.py` | `score` (camada determinística via `quality_gate.collect_checks`) + `pair` (prompt do julgador par-a-par do protocolo quality-anchors) |
| `quality_gate.py::collect_checks` | Agregação extraída em função pura (CLI e eval usam a MESMA fonte, sem drift) |
| `scripts/tests/test_copy_output_evals.py` | 9 guards: IDs, briefings completos (pegou 4 briefings frouxos na primeira execução), determinismo do score, cap de AI-tells, montagem do prompt nas 2 ordens |
| `evals/baselines/copy/CO-00N.md` | Outputs reais do mos-copy v6.14.0 (opus, dispatch headless): alvos de comparação like-for-like |
| `evals/copy-output-baseline.md` | Números, julgamento, achados e critério de aceite pra próxima mudança |

## Resultados (resumo; detalhe no baseline doc)

- Calibração do julgador: âncora positiva 6/6 critérios nas duas ordens. Validado.
- Determinístico: CO-003 88, CO-004 81, CO-001/002/005 50-58 (ruído de perfil de formato documentado; comparação é sempre caso-a-caso entre rodadas).
- Par-a-par CO-002 vs âncora: **mos-copy vence no geral, consistente nas 2 ordens** (ganha hook/cta/fit, perde especificidade/prova, empata naturalidade).

## Achados (nenhum era visível sem o eval)

1. Output devolvido como TEXTO no chat não passa pelo `quality_gate_hook` (só Write/Edit disparam): escaparam 2 travessões em título meta e 1 antítese real em corpo de copy (CO-005). Mitigação candidata registrada no baseline doc; medir com a própria baseline antes de aplicar.
2. Falso positivo mention-vs-use: o self-report do agent ("sem brutal") acusa no scanner. Refino v2 do scorer em backlog.
3. O agent NÃO inventou prova quando o briefing não deu (perdeu o critério "prova" pra âncora por honestidade): comportamento correto do fact-check confirmado por eval.

## Rubricas (RUBRICS.md)

- R1 implementação: 3 (correção demonstrada por execução real; guards novos com casos negativo e positivo)
- R2 documentação: 4 (baseline doc + README de evals + este worklog no mesmo diff; artefatos versionados)
- R4 output: N/A (rodada de eval, não de produção)

## Follow-ups registrados

- [ ] Mitigar bypass do hook em output de chat (opções no baseline doc; decidir com dado da 2ª rodada)
- [ ] Refino mention-vs-use no `check_ai_tells`
- [ ] Perfis de formato no checker (baixa prioridade; like-for-like resolve hoje)
