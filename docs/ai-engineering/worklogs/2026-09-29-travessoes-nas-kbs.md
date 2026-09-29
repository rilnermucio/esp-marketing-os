# 2026-09-29: Travessões fora dos exemplos das knowledge bases

**Executor**: Claude Opus 5.5 via Claude Code (desktop)
**Objetivo**: tirar os travessões das knowledge bases Tier 2 (`subagents/*.md`), pedido do usuário depois da rodada de implementação da auditoria.
**Fora de escopo declarado**: travessões em commands (45), workflows (19), references (1) e voice clones em `assets/` (975); epígrafes com antítese no topo das KBs; exemplo de advocacia que contradiz o Provimento OAB 205. Todos listados em "Próximos passos".

## Arquivos lidos (relevantes pra decisão)
- As 13 KBs com travessão, linha a linha, com contexto das linhas vizinhas nos casos de continuação.
- `scripts/tests/test_repo_consistency.py`: o guard da prosa isentava bloco de código e citação, onde estavam 236 dos 248 travessões.

## Arquivos alterados/criados
- 13 KBs em `subagents/`: 249 linhas trocadas, nenhuma outra linha mexida.
- `scripts/tests/test_repo_consistency.py`: `test_no_dash_in_kb_examples`.
- `docs/ai-engineering/FAILURE-TAXONOMY.md` (F-COPY-01) e `CHANGELOG.md`.

## Decisões (e alternativas rejeitadas)
- Regra por contexto, aplicada por script e revisada linha a linha: rótulo e descrição viram dois-pontos; com dois-pontos antes ou conectivo depois, vírgula; atribuição de citação e de livro vai para parênteses; assinatura de depoimento perde o travessão inicial; faixa numérica vira "a"; célula de tabela desenhada só com travessão vira hífen, para manter o alinhamento; texto depois do travessão que já tinha dois-pontos vai para parênteses.
- 20 linhas com decisão manual: blocos de copy com aposto quebrado em linhas, continuação de frase, lições com complemento, linha de identificação da advogada reordenada.
- Hífen com espaços como substituto foi rejeitado: repete o visual do travessão que a regra quer evitar.
- Guard mais rígido que o da prosa: nas KBs vale dentro de bloco de código e citação; só código inline e a linha que enuncia a regra ficam de fora.

## Evidências
- Antes: 248 travessões longos em 13 KBs (design-agent 111, copy-agent 56) e 2 travessões curtos como pontuação no funnel-agent. Depois: 0 e 0.
- `git diff --numstat subagents/`: 249 linhas adicionadas e 249 removidas.
- O guard novo reprova o estado antigo (13 falhas, uma por KB afetada) e aprova o novo (21 de 21).

## Testes
- Rodados: suíte estática completa, `black --check`, `flake8`, `validate_agents.py --strict`, `build_codex_plugin.py --check` e `validate_codex_plugin.py plugins/marketing-os`.
- Não rodados e motivo: smoke com modelo real, porque a mudança é só de pontuação em conteúdo lido sob demanda, sem mexer em hook, caminho, nome de agent ou manifest.

## Falhas da taxonomia tocadas
- F-COPY-01: exemplos com travessão ensinavam o padrão que o gate bloqueia na entrega.

## Rubrica aplicada
- Qualidade de copy: melhora (exemplos alinhados à regra global). Documentação: CHANGELOG e taxonomia atualizados. Veredito: merge sim.

## Custo aproximado
- Não medido em tokens; uma rodada curta, sem subagentes.

## Riscos e follow-ups
- Uma troca de pontuação pode ter mudado a ênfase de algum exemplo; a revisão linha a linha e o diff de 249 linhas reduzem esse risco.

## Próximos passos
- Commands (45) e workflows (19) ainda têm travessão em bloco de código e citação; o guard da prosa os isenta.
- Voice clones em `assets/` (975): parte é citação de autor real, então a troca pede critério próprio.
- Epígrafes no topo de 6 KBs usam a antítese proibida ("Growth não é um departamento. É uma mentalidade") e têm atribuição a conferir.
- O exemplo de anúncio de advocacia no copy-agent (PARTE XI) oferece avaliação "R$0" e cita honorários, o que o Provimento OAB 205 (art. 3º, I) veda.
