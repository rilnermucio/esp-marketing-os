# Baseline do eval de output do mos-copy

> Primeira execução: 2026-07-06, plugin v6.14.0 (pós-nivelamento das 5 ondas), mos-copy em opus. Esta é a régua contra a qual qualquer mudança futura no mos-copy (prompt, KB, gates, modelo) deve ser medida ANTES do merge. Método: OPERATING-MODEL (medir antes de refatorar).

## Método

1. **Geração**: 5 briefs fixos de `copy-output-cases.json` (todos os inputs de pre-flight preenchidos), gerados via dispatch headless real do mos-copy (`claude -p` + `--plugin-dir`, Agent tool). Outputs versionados em `baselines/copy/CO-00N.md`: são os alvos de comparação par-a-par das próximas rodadas.
2. **Camada determinística**: `python3 scripts/copy_output_eval.py score <output> --formato <f>` (usa `quality_gate.collect_checks`, mesma agregação do CLI).
3. **Camada julgada**: protocolo de `quality-anchors.md` (par-a-par, por critério, sem nota absoluta, 2 rodadas com ordem invertida, vitória só quando consistente). Prompt do julgador: `copy_output_eval.py pair`.
4. **Calibração do julgador** (pré-requisito): âncora negativa vs positiva, 2 ordens. Resultado: positiva venceu 6/6 critérios nas DUAS ordens, citando os vícios plantados. Julgador validado.

## Resultados da camada determinística

| Caso | Formato | Score | Palavras | Achados relevantes |
|------|---------|-------|----------|--------------------|
| CO-001 | headline | 50 | 821 | Travessão no título meta do documento (não na copy); resto é ruído de perfil (ver nota) |
| CO-002 | post | 58 | 321 | Travessão no título meta; "brutal" é FALSO POSITIVO (menção no self-report do agent, não uso) |
| CO-003 | email | 88 | 250 | Subject principal acima de 50 chars (87) |
| CO-004 | ad | 81 | 412 | Comprimento total alto pra anúncio (3 ângulos no mesmo arquivo explica) |
| CO-005 | sales | 58 | 238 | **Antítese negação→afirmação REAL no corpo da copy** ("não é a receita, é o...") |

**Nota de leitura dos scores**: o checker de formato pontua contra o perfil completo do tipo (ex: landing-page espera prova social/garantia/FAQ), então entregas parciais legítimas (set de headlines, dobra única) sofrem penalidade estrutural. Compare score de CO-00N sempre com o MESMO caso em rodadas futuras, nunca entre casos. As dimensões fortes pra comparação: Vícios de IA, Hook, Legibilidade, Acentuação.

## Resultado da camada julgada (CO-002 vs âncora positiva, mesmo formato)

Consistente nas duas ordens (zero flip por posição):

| Critério | Vencedor |
|----------|----------|
| hook | **mos-copy** |
| cta | **mos-copy** |
| fit | **mos-copy** |
| especificidade | âncora |
| prova | âncora |
| naturalidade | empate |
| **geral** | **mos-copy (2/2 rodadas)** |

Leitura: o output real do agent vence a âncora de referência no geral. As derrotas têm causa mapeada: o briefing do CO-002 não forneceu dado de prova e o agent corretamente NÃO inventou número (comportamento desejado do fact-check), pagando o preço no critério "prova". Rodadas futuras: quando o briefing fornecer prova (como CO-005 fornece), o critério mede uso; quando não fornecer, mede a honestidade.

Os outros 4 casos não foram julgados contra a âncora (formato diferente = ruído); a referência par-a-par deles são os próprios artefatos de `baselines/copy/`, comparados like-for-like na próxima rodada.

## Achados que viram ação

1. **Texto devolvido no chat não passa pelo hook** (F-GATE candidata): o `quality_gate_hook.py` dispara em Write/Edit; quando o agent devolve a copy como texto da resposta, a camada 2 não roda, e escaparam 2 travessões em títulos meta + 1 antítese em corpo de copy (CO-005). Mitigações candidatas (avaliar com esta baseline antes de mexer): instrução de self-check final com o padrão exato das regexes do hook, ou orientar commands de produção a escrever a peça via Write (o hook dispara).
2. **Falso positivo mention-vs-use no scorer**: o self-report do agent ("sem brutal") acusa a palavra. Refino v2 do `check_ai_tells` ou instrução pro agent não ecoar termos proibidos no self-report.
3. **Perfis de formato no checker**: score bruto mistura sinal e ruído por tipo; um perfil por formato (headline set, dobra, email) tornaria o número comparável entre casos. Backlog, não urgente (comparação like-for-like já funciona).

## Como rodar a próxima rodada (mudou algo no mos-copy? rode ANTES do merge)

```bash
# 1. Gere os 5 outputs candidatos com o agent modificado (mesmos briefs)
# 2. Camada determinística por caso:
python3 scripts/copy_output_eval.py score candidato-CO-002.md --formato post
# 3. Par-a-par contra a baseline (2 rodadas, ordem invertida na segunda):
python3 scripts/copy_output_eval.py pair --candidato candidato-CO-002.md \
  --referencia docs/ai-engineering/evals/baselines/copy/CO-002.md \
  --briefing <briefing do caso> [> prompt.txt; rodar num modelo juiz]
# 4. Aceite: candidato vence ou empata no geral em ≥4 dos 5 casos, consistente nas 2 ordens,
#    e a dimensão Vícios de IA não regride em nenhum. Senão, a mudança não entra.
```
