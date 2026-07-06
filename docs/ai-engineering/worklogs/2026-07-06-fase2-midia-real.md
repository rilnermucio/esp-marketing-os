# 2026-07-06: Fase 2 do ROADMAP (mídia real)

**Executor**: Claude Fable 5 via Claude Code
**Objetivo**: fechar o gap "só gera prompt": prompt → PNG, brief → thumbnail 16:9, roteiro → Reels legendado renderizado.
**Fora de escopo declarado**: publicação/upload nas plataformas (fora do escopo do plugin por decisão do ROADMAP); Fase 4 (loop de métricas).

## Arquivos alterados/criados

- `scripts/thumbnail_composer.py` (novo) + `scripts/tests/test_thumbnail_composer.py` (11 testes) + entrada `thumbnail compose` no mos.py + `Pillow>=10,<12` no requirements: overlay tipográfico determinístico 1280x720 (cover-resize, quebra por largura medida, autoajuste de fonte, stroke + faixa de contraste)
- `commands/renderizar-imagem.md`, `commands/gerar-thumbnail.md`, `commands/produzir-reels.md` (novos): padrão 2 fases do /narrar-roteiro (plugin prepara e valida via mos-*; skill do ambiente/execução local renderiza) com fallback honesto por degrau
- `docs/MEDIA-PIPELINE.md` (novo): dependências de ambiente, fallbacks e regras do pipeline
- Golden set RT-020/021/022 + resumo; allowlist do workspace +3; contagens 43/39; ROADMAP Fase 2 marcada entregue; CHANGELOG Unreleased

## Decisões (e alternativas rejeitadas)

- **Texto NUNCA no prompt de imagem**: gerador renderiza texto mal; o overlay é script determinístico (a razão de existir do thumbnail_composer). Alternativa "pedir o texto no prompt e torcer" rejeitada: é a falha padrão de thumbnail por IA.
- **Pipeline de Reels em degraus com fallback declarado**: cada degrau (roteiro → áudio → vídeo) entrega valor sozinho; sem HyperFrames no ambiente, o command entrega a composição pronta + o comando de render, nunca finge que renderizou.
- **Skills externas por detecção, não por dependência**: gpt-image-2/ai-image-generation/hyperframes são do ambiente do usuário; o plugin não as distribui (consistente com o padrão Apify e a política de delegação da SKILL).

## Evidências

- Suite: 2046 passed (composer 11/11 + contratos dos 3 commands parametrizados + 3 casos novos do golden set); strict 19/19; pacote Codex rebuildado e validado
- Smoke end-to-end real: `mos.py thumbnail compose` gerou PNG 1280x720 com texto acentuado
- Camada viva RT-021: **rota exata** (command + agents), com a primeira divergência instrutiva do gabarito: dispatch `sequencial` vs `paralelo`. Diagnóstico: o gabarito rotulava o paralelismo interno da Fase 1; a convenção correta (consistente com RT-022) é rotular o pipeline inteiro. **Gabarito calibrado + convenção documentada** no evals/README (é exatamente o papel da camada viva: o gabarito também é código e também tem bugs)

## Testes
- Rodados: suite completa, strict, lint (black/flake8) nos arquivos novos, smoke CLI real, camada viva 1 caso
- Não rodados e motivo: render real de Reels via HyperFrames (exige npx no fluxo completo; degraus 1-2 são cobertos por tts_runner já testado); smoke geral (tokens)

## Falhas da taxonomia tocadas
- Prevenidas: F-COST-01 (pipeline usa scripts determinísticos onde cabe), F-CODEX-03 (outputs em workspace/, allowlist justificada), F-REG (gate "declarar o degrau alcançado" contra reporte de mídia não renderizada)
- Calibradas: F-EVAL (convenção do campo dispatch documentada após divergência real)

## Rubrica aplicada
- R1: 4 (script com testes incluindo falso positivo do teste corrigido honestamente; smoke real) | R2: 4 | R3: 4 (golden set + camada viva + calibração no mesmo diff) | R5: 3 (validates verdes; install fica pra release) | R4/R6: N/A
- Veredito de merge: aprovado

## Custo aproximado
- Fração de sessão de fronteira + 1 sessão headless (~20s) + 1 render local de teste (PIL, ~0,5s). Não medido em tokens.

## Próximos passos
1. Release v6.12.0 (Unreleased pronto)
2. Fase 4 do ROADMAP: loop /aprender (métricas reais → memories, que agora existem em 15 agents e têm consumidores óbvios: CTR de thumbnail → mos-video, winners → swipe files)
3. Fase 3 restante (mos-community, mos-partnerships) quando houver demanda real
4. Fase 5 humana das releases do dia continua pendente (1 install cobre todas)
