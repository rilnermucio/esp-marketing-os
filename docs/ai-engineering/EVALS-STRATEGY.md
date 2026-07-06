# Estratégia de evals

> Canônico. Atualizado em 2026-07-06. Como o Marketing OS mede a si mesmo, em ordem de preferência: determinístico > estrutural > LLM-graded > humano. Cada camada só entra quando a anterior não alcança.

## Pirâmide de avaliação

```
4. HUMANO          voz de marca final, decisões de escopo, aprovação de release
3. LLM-GRADED      qualidade de output vs rubrica (futuro controlado; ver §4)
2. GOLDEN SETS     roteamento e contratos esperados, validados por teste
1. DETERMINÍSTICO  suite pytest (~1.900 testes), validadores, hooks, lint
```

A base já existe e é a maior força do repo: `scripts/tests/` roda em segundos, sem modelo, sem rede (`-m "not smoke"`). Toda regra nova tenta primeiro morar aqui.

## 1. O que DEVE ser code-graded (determinístico)

| Alvo | Mecanismo atual |
|---|---|
| Estrutura de commands (frontmatter, dispatch, consolidação, gates) | `test_commands_dispatch.py` |
| Frontmatter e sanidade de agents (tools, refs de KB, script sem Bash) | `validate_agents.py --strict` (CI bloqueia) |
| Vícios de IA em copy (travessão, "brutal", antítese) | `quality_gate_hook.py` (bloqueio) + `quality_gate.py` (score) + testes de ambos |
| Acentuação PT-BR, hook, CTA, limites de formato | `quality_gate.py` checks |
| Manifests Claude | `test_plugin_manifest.py` + `claude plugin validate .` |
| Pacote Codex | `validate_codex_plugin.py` |
| Separação workspace/plugin | `test_workspace_separation.py` (com allowlist justificada) |
| Golden set de roteamento (consistência interna) | `test_routing_evals.py` (novo, 2026-07) |

Regra: se a propriedade é expressável como regex, glob, contagem, schema ou existência de arquivo, ela é code-graded. Sem exceção por conveniência.

## 2. Golden sets

Dados em [evals/](evals/), consumidos por testes. Hoje: [routing-cases.json](evals/routing-cases.json) (matriz briefing → roteamento esperado, ver [ROUTING-EVALS.md](ROUTING-EVALS.md)).

O teste valida o que dá pra validar sem modelo: casos bem-formados, commands/agents citados existem, IDs de falha existem na taxonomia, coerência dispatch↔agents. O acerto de roteamento em sessão real usa o mesmo arquivo como gabarito de revisão manual (protocolo em ROUTING-EVALS.md §validação viva).

### Como adicionar um golden case

1. Motivo real: um briefing roteou errado, ou uma área nova precisa de cobertura. Caso inventado sem falha plausível associada é peso morto (H8.2).
2. Adicione o caso em `routing-cases.json` com `detects` apontando IDs da [FAILURE-TAXONOMY.md](FAILURE-TAXONOMY.md). Falha nova? Primeiro a taxonomia, depois o caso.
3. Rode `python -m pytest scripts/tests/test_routing_evals.py -q`.
4. Registre no worklog da rodada o que motivou o caso.

## 3. Anti-fragilidade (regras pra evals que não apodrecem)

1. **Presença e range, nunca valor exato de score.** `assert 0 <= score <= 100`, não `assert score == 83`. Precedente positivo: toda a suite do quality_gate.
2. **Glob + parametrize.** Coleções de arquivos são descobertas, não listadas: arquivo novo entra na cobertura automaticamente (padrão de `test_commands_dispatch.py`). Eval com lista hardcoded de arquivos é F-EVAL-02.
3. **Asserte classe/ID, não texto de mensagem.** Mensagens mudam por estilo; IDs de taxonomia e nomes de check são estáveis.
4. **Fixture pequena e local.** O caso de teste carrega seu próprio insumo mínimo; nada de depender de arquivo grande do repo que pode mudar por outro motivo.
5. **Rede/token = smoke.** Teste que precisa de APIFY_TOKEN, browser ou API externa leva marker `smoke` e fica fora do tier padrão.
6. **Flaky conhecido é registrado, não silenciado.** `test_pdf_generator::test_cli_basic` flaca sob carga da suite e passa isolado: re-rode isolado antes de debugar (F-EVAL-03).
7. **Falso positivo tem teste também.** Todo detector (regex de gate) nasce com casos que NÃO devem disparar (precedente: `test_quality_gate_hook.py` cobre antíteses reais e frases legítimas parecidas).

## 4. LLM-graded (futuro, com guarda-corpo)

Candidatos, em ordem de valor:

1. **Qualidade de copy vs rubrica R4 + Copy Score System**: amostra de outputs dos agents scoreada por modelo com rubrica fixa e exemplos âncora.
2. **Fidelidade de voice clone**: Voice Match Scoring (PARTE XV-B do copy-agent) aplicado a par (amostra original, output do clone).
3. **Adaptação BR** (F-PTBR-02): julgar se o texto soa nativo ou traduzido.

Regras quando implementar: julgamento **par-a-par ou contra âncora**, nunca nota absoluta isolada; rubrica e âncoras versionadas neste diretório; modelo julgador barato (ver [COST-CONTROL.md](COST-CONTROL.md)); disagreement com humano medido antes de confiar. Até lá, esses aspectos são human-reviewed.

## 5. Human-reviewed (permanente)

- Voz de marca final de peças publicáveis.
- Decisões de escopo de produto (ROADMAP).
- Aprovação de release (checklist tem passos humanos: install real, marketplace).
- Amostragem periódica dos golden sets: o gabarito também envelhece.

## 6. Métricas por dimensão

| Dimensão | Métrica | Fonte |
|---|---|---|
| Roteamento | % de acerto na revisão viva do golden set | ROUTING-EVALS §validação viva |
| Qualidade de output | Score médio `quality_gate.py` em amostra + violações de hook por rodada | CLI + logs de hook |
| Documentação | Achados de drift por auditoria (tendência deve cair) | Worklogs de auditoria |
| Compatibilidade | validates Claude + Codex verdes em CI | CI |
| Custo/contexto | Linhas por camada (Tier 1 total, SKILL, KB média) + notas de custo nos worklogs | ADR-0001 baseline + worklogs |
