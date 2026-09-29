# ADR-0008: Na resposta final, só o bloqueio fala com o agent

**Status**: aceito
**Data**: 2026-09-28
**Autor**: Claude Opus 5.5

## Contexto

O gate avalia a resposta final dos agents no `SubagentStop` (ADR-0003 e ADR-0005). Violação dura bloqueia com exit 2; avisos (CAPS, clichês, compliance) saíam com exit 0 e `additionalContext`. As baselines AO-005 e AO-007 do eval de output (2026-09-28) mostraram o efeito no runtime:

1. O agent entregou a peça completa.
2. O bloqueio pediu "reescreva e tente novamente", e o agent reenviou a peça corrigida.
3. Na parada seguinte, só havia avisos. O `additionalContext` foi entregue ao subagent, que continuou e respondeu com uma nota curta ("Ajuste feito: troquei o placeholder...").
4. A nota repetia o termo avisado, o aviso voltou e o ciclo se repetiu mais duas vezes, até "Peço desculpas, ainda deixei a palavra em caixa alta".

Só a última mensagem do subagent volta a quem o chamou. O orquestrador recebeu a nota de desculpas no lugar da campanha e precisou retomar o agent para recuperar a entrega. Aviso não tinha o limite de uma tentativa que o bloqueio tem, então virava laço.

## Decisão

Na resposta final (`Stop` e `SubagentStop`):

1. Só o bloqueio fala com o agent. A mensagem de bloqueio pede a entrega completa já corrigida, do início ao fim, e proíbe responder só com o trecho alterado, desculpas ou explicação. Avisos e compliance viajam dentro do bloqueio, quando ele existe.
2. Avisos sem violação dura não geram saída: exit 0, sem `additionalContext`. Ficam no log (`MOS_HOOK_LOG`).
3. Violação que sobra depois da única tentativa de correção vai para o usuário por `systemMessage`, sem reabrir o agent.

Nas escritas (`PreToolUse`), nada muda: avisos seguem como `additionalContext`, porque a ferramenta prossegue e o agent não é reaberto.

Guards: `test_quality_gate_hook.py::TestRender` (bloqueio pede entrega completa, aviso sozinho fica em silêncio, retry esgotado usa só `systemMessage`) e `test_install_smoke.py::test_final_answer_gate_evaluates_namespaced_agent` (no máximo 2 paradas por dispatch).

## Alternativas consideradas

1. **Manter avisos como additionalContext e limitar por contador**: rejeitada. Mesmo uma rodada extra troca a entrega por uma nota curta, e o hook não tem estado entre paradas além de `stop_hook_active`.
2. **Mostrar os avisos ao usuário por systemMessage**: rejeitada por ora. Avisos de compliance são condicionais ("se a peça é de dentista...") e têm falso positivo fora da categoria; na tela do usuário virariam ruído. Os avisos continuam chegando ao agent nas escritas e nos bloqueios.
3. **Bloquear também por aviso**: rejeitada. Aviso existe justamente porque há uso legítimo.

## Consequências

Positivas: a entrega que chega ao orquestrador é a peça completa; o gate não gera laço; custo e latência caem.

Negativas (custo aceito): na resposta final sem violação dura, o agent não vê avisos de CAPS, clichê ou compliance. A mitigação é o gate de escrita, a instrução de compliance nos 21 agents e os quality gates que o orquestrador aplica antes de entregar.

## Critério de revisão

Reabrir se a plataforma passar a oferecer um canal de exit 0 na resposta final que chegue ao agent sem reabri-lo, ou se o log mostrar violação recorrente que só aparecia como aviso.
