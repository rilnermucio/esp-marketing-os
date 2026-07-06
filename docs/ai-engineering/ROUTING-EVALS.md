# Routing Evals: matriz de roteamento esperado

> Canônico. Atualizado em 2026-07-06. O gabarito vivo está em [evals/routing-cases.json](evals/routing-cases.json); este documento explica a matriz e o protocolo. A tabela abaixo é um resumo de leitura; **em divergência, o JSON vence**.

## O que a matriz cobre

Briefings de usuário em PT-BR (como chegam de verdade, sem jargão de sistema) e o roteamento esperado: command de entrada, agents dispatchados, modo de dispatch e campos mínimos do output. Cada caso lista quais falhas da [FAILURE-TAXONOMY.md](FAILURE-TAXONOMY.md) ele detecta se o roteamento errar.

## Resumo dos casos (gabarito completo no JSON)

| ID | Briefing (resumo) | Command | Agents | Dispatch |
|---|---|---|---|---|
| RT-001 | post pro Instagram sobre tema X | `/criar-post` | social + copy | paralelo |
| RT-002 | "o que é AIDA?" | nenhum (inline) | nenhum | nenhum |
| RT-003 | melhorar headline existente | `/otimizar-copy` | copy | simples |
| RT-004 | campanha completa de lançamento | `/campanha-lancamento` | research, launch, funnel, copy, email, ads | sequencial |
| RT-005 | artigo SEO | `/criar-artigo` | research → seo → copy | sequencial |
| RT-006 | anúncio Meta Ads | `/criar-anuncio` | research + ads | paralelo |
| RT-007 | roteiro de VSL | `/criar-video` | storytelling → copy → video | sequencial |
| RT-008 | sequência carrinho abandonado | `/criar-email` | email + copy | paralelo |
| RT-009 | análise de concorrente | `/analisar-concorrencia` | research + brand + copy | paralelo |
| RT-010 | landing page high-ticket | `/criar-landing-page` | funnel → copy → design | sequencial |
| RT-011 | datas comerciais do mês | `/datas-sazonais` (utility) | nenhum | nenhum |
| RT-012 | publicar no Notion | `/publicar-notion` (utility) | nenhum | nenhum |
| RT-013 | desenhar teste A/B | nenhum (gap: sem command) | ab-testing | simples |
| RT-014 | narrar roteiro em áudio | `/narrar-roteiro` | audio | simples |
| RT-015 | "por que o engajamento caiu?" | nenhum (linguagem natural) | analytics | simples |
| RT-016 | carrossel 10 slides | `/criar-carrossel` | social + copy + design | paralelo |
| RT-017 | montar oferta high-ticket | nenhum (ambiguidade conhecida) | infoproduct + copy | paralelo |
| RT-018 | bio do Instagram | nenhum (linguagem natural) | copy | simples |

Casos RT-013 e RT-017 documentam gaps reais (agent órfão de command; ambiguidade sem regra de desempate). Eles existem pra medir se as futuras correções resolveram: quando `/criar-teste-ab` ou `mos-offer` existirem, atualize o gabarito no mesmo diff (e este resumo).

## Validação em duas camadas

**Camada determinística (roda em CI):**

```bash
python -m pytest scripts/tests/test_routing_evals.py -q
```

Valida: IDs únicos e bem-formados, commands/agents citados existem no repo, coerência dispatch↔agents (dispatch "nenhum" implica zero agents; "simples" implica exatamente 1; paralelo/sequencial implicam 2+), campos mínimos presentes, e todo ID em `detects` definido na taxonomia. Isso trava o gabarito contra drift estrutural: renomear um command ou agent quebra o teste na hora.

**Camada viva (manual, por amostragem):**

Periodicamente (a cada release ou mudança em SKILL.md/descriptions), rode 5+ casos do gabarito em sessão real: cole o `prompt` numa sessão limpa com o plugin carregado e compare o roteamento observado com o esperado. Registre no worklog: casos rodados, acertos, divergências. Divergência tem dois desfechos possíveis: bug de roteamento (corrigir SKILL/description) ou gabarito desatualizado (corrigir o JSON com justificativa).

## Campos mínimos do output (`min_output_fields`)

Cada caso declara o que a resposta final precisa conter (ex: post exige sugestão de enquete; artigo exige meta title/description; teste A/B exige hipótese se-X-então-Y-porque-Z e amostra mínima). Hoje servem de checklist pra camada viva; são o esqueleto da futura camada LLM-graded ([EVALS-STRATEGY.md](EVALS-STRATEGY.md) §4).

## Como estender

Protocolo em [EVALS-STRATEGY.md](EVALS-STRATEGY.md) §2. Resumo: motivo real → taxonomia primeiro se a falha for nova → caso no JSON → teste verde → atualizar o resumo aqui → worklog.
