# Baseline do eval de output: mos-social, mos-email e mos-ads

> Primeira execução: 2026-09-28, branch `fix/auditoria-set2026` (depois da ADR-0008), agents em sonnet. É a régua contra a qual qualquer mudança nesses três agents (prompt, KB, gates, modelo) deve ser medida antes do merge. Método: OPERATING-MODEL (medir antes de refatorar).

## Método

1. **Geração**: 9 briefs fixos de `agent-output-cases.json` (3 por agent), cada um com todos os campos do PRE-FLIGHT do agent, gerados por dispatch headless real: `claude -p --plugin-dir <repo>` num diretório vazio fora do repo, com as cópias instaladas do plugin desligadas. A peça é o retorno do Agent no stream-json, sem o envelope do runtime. Outputs versionados em `baselines/<perfil>/AO-00N.md`.
2. **Camada determinística**: `python3 scripts/copy_output_eval.py score <output> --profile <social|email|ads>`.
3. **Camada julgada**: protocolo de `quality-anchors.md` (par a par, por critério, 2 rodadas com ordem invertida). Critérios por perfil em `scripts/evals/output-profiles.json`; o perfil `social` foi criado nesta rodada.

## Resultados da camada determinística

| Caso | Perfil | Peça | Score | Palavras | Vícios de IA | Leitura |
|------|--------|------|-------|----------|--------------|---------|
| AO-001 | social | Carrossel Instagram (café) | 82 | 942 | 0 | Slides, legenda e enquete completos |
| AO-002 | social | Post LinkedIn com enquete | 90 | 843 | 0 | Texto e enquete dentro do limite pedido |
| AO-003 | social | Stories com caixa de perguntas (psicologia) | 85 | 1.481 | 0 | Sem promessa de cura, como pede a categoria |
| AO-004 | email | Boas-vindas, 3 emails | 85 | 1.625 | 0 | Subjects, preheaders e CTA por email |
| AO-005 | email | Reengajamento e limpeza de lista | 80 | 2.830 | 0 | Inclui a regra de limpeza pedida |
| AO-006 | email | Fim de teste grátis (SaaS) | 83 | 1.613 | 0 | Trata a objeção de migração |
| AO-007 | ads | Meta Ads, curso de Excel | 66 | 1.600 | 0 | Estrutura, orçamento e 3 criativos |
| AO-008 | ads | Google Ads de pesquisa, serviço local | 73 | 2.348 | 0 | Grupos, correspondências, negativas e 2 RSAs |
| AO-009 | ads | Meta Ads, clínica odontológica | 76 | 2.454 | 0 | Abre com alerta de compliance (ver abaixo) |

Nenhuma das 9 peças tem travessão ou vício de IA detectado. Scores de anúncio ficam mais baixos porque o checker de `anuncio` pontua uma peça curta, e a entrega aqui é campanha inteira (estrutura, orçamento e vários criativos): compare cada caso só com ele mesmo.

**Compliance em runtime (AO-009)**: o briefing pedia "avaliação gratuita" para uma clínica odontológica, o que o Código de Ética Odontológica veda (art. 20, IX, e art. 44, I). O `mos-ads` abriu a entrega com um alerta citando esses artigos, tirou a gratuidade e a condição comercial da peça, exigiu nome do dentista e CRO em todo criativo (art. 43; CFO-196, art. 4º), evitou "popular", sorteio e antes e depois, e recomendou validar com o CRO. É a leitura de `references/compliance-br.md` funcionando no agent instalado.

## Achado que virou correção

A primeira geração (antes da ADR-0008) revelou o laço de avisos no gate da resposta final: nos casos AO-005 e AO-007, o subagent entregou a peça completa, recebeu um bloqueio, corrigiu e depois foi reaberto 3 vezes por avisos em `additionalContext`, até a última mensagem virar "Peço desculpas...". O orquestrador recebeu a nota no lugar da peça e precisou retomar o agent. A mesma geração pegou "Não é X. São Y." passando pelo gate (AO-001). As duas falhas foram corrigidas antes desta baseline (F-COPY-01 e F-COPY-05), e as 9 peças foram regeradas com o gate novo.

## Como rodar a próxima rodada (mudou mos-social, mos-email ou mos-ads? rode antes do merge)

```bash
# 1. Gere os outputs candidatos com o agent modificado (mesmos briefs de agent-output-cases.json)
# 2. Camada determinística por caso:
python3 scripts/copy_output_eval.py score candidato-AO-004.md --profile email
# 3. Par a par contra a baseline (2 rodadas, ordem invertida na segunda),
#    com o briefing do caso salvo num arquivo:
python3 scripts/copy_output_eval.py pair --candidato candidato-AO-004.md \
  --referencia docs/ai-engineering/evals/baselines/email/AO-004.md \
  --profile email --briefing briefing-AO-004.txt
python3 scripts/copy_output_eval.py pair --candidato candidato-AO-004.md \
  --referencia docs/ai-engineering/evals/baselines/email/AO-004.md \
  --profile email --briefing briefing-AO-004.txt --inverter
# 4. Aceite: candidato vence ou empata no geral em pelo menos 2 dos 3 casos do agent,
#    consistente nas 2 ordens, e a dimensão de vícios de IA não regride em nenhum.
```

Compare o score de um caso sempre com o mesmo caso em rodadas futuras, nunca entre casos: o checker pontua contra o perfil completo do tipo, e entregas parciais legítimas perdem pontos estruturais.
