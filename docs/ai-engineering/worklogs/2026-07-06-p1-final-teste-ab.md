# 2026-07-06: Onda P1 final (video/storytelling) + /criar-teste-ab

**Executor**: Claude Fable 5 via Claude Code
**Objetivo**: fechar a matriz de paridade (os dois últimos 4/10) e o último agent órfão de command.
**Fora de escopo declarado**: release (proposta ao usuário no fechamento); Fases 2 e 4 do ROADMAP.

## Arquivos alterados/criados

**P1 final (commit 99497bc)**: `agents/mos-video.md` (memory, pre-flight de VSL, auto-iteração de hooks/títulos com lint + timing, red team de retenção), `agents/mos-storytelling.md` (WebSearch + Bash + memory com story bank, pre-flight de matéria-prima real, auto-iteração multi-framework, red team de editor), `init_agent_memory.py` (15 agents), contagens com lista invertida "todos exceto" (menos superfície de drift).

**/criar-teste-ab (commit 48b9e32)**: command com decision tree de 3 caminhos, WebSearch no mos-ab-testing, RT-013 promovido no golden set, contagens 40/36, pacote Codex rebuildado.

## Decisões (e alternativas rejeitadas)

- **Pre-flight do storytelling é anti-fabricação, não anti-falta-de-research**: o risco nº 1 do domínio é inventar biografia/case "real". O pre-flight coleta fatos antes de narrar; o Gate 5 ganhou WebSearch pra verificar os públicos. Alternativa "só reforçar o gate em prosa" rejeitada: gate sem ferramenta era exatamente o estado anterior.
- **No /criar-teste-ab, quem desenha o experimento não escreve a variante**: sequencial ab-testing → copy/ads com contrato de "mude APENAS a dimensão especificada". Paralelo rejeitado: contamina o desenho (variante muda 3 coisas e invalida a leitura).
- **Listas de memory invertidas nos docs** ("todos exceto ai-tools, audio, growth, ab-testing"): com 15/19, listar os 15 é mais superfície de drift que listar os 4.

## Evidências

- `validate_agents.py --strict`: 19/19 clean (storytelling 190 linhas, video 199, ambos com 7 tools)
- Suite: 1999 passed, 2 skipped
- Camada viva RT-013: `command=criar-teste-ab | agents=mos-ab-testing | dispatch=simples`, acerto exato na mesma rodada da criação. Acumulado do dia: 7/7
- Matriz de paridade: zerada (nenhum agent abaixo do padrão em features estruturais; profundidade de KB segue variável por design, ver ADR-0001)

## Testes
- Rodados: suite completa 2x, strict 2x, camada viva 1 caso, rebuild + validate Codex
- Não rodados e motivo: smoke (tokens); install real (sem release nesta rodada)

## Falhas da taxonomia tocadas
- Corrigidas: F-ROUTE-03 (zerada: nenhum agent órfão de command), F-CLAIM-01 no storytelling (gate ganhou ferramenta)
- Prevenidas: F-DOC-01 (listas invertidas), F-EVAL (RT-013 validado vivo antes de declarar fechado)

## Rubrica aplicada
- R1: 4 | R2: 4 | R3: 4 (golden set + camada viva no mesmo diff) | R4/R6: N/A | R5: 3 (validates verdes; install na próxima release)
- Veredito de merge: aprovado

## Custo aproximado
- Fração de sessão de fronteira + 1 sessão headless (~20s). Não medido em tokens.

## Próximos passos
1. Release v6.11.0 (CHANGELOG Unreleased pronto; proposta feita ao usuário)
2. Fase 5 humana continua pendente (um install cobre v6.9.0/v6.10.0/v6.11.0)
3. ROADMAP Fase 2 (mídia real: /renderizar-imagem, /gerar-thumbnail, /produzir-reels) e Fase 4 (loop de métricas → memory via /aprender)
4. mos-community e mos-partnerships (Fase 3 restante) quando houver demanda
