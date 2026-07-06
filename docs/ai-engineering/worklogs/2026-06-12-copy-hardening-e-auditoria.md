# 2026-06-12: Hardening de copy + auditoria geral (registro retroativo)

**Executor**: Claude Fable 5 via Claude Code
**Objetivo**: (1) fechar os 8 gaps da auditoria de copy (gate de antítese, Bash no mos-copy, /otimizar-copy, swipe-files vivos, snapshot guards, awareness level, drift de contagens, guard de instrução morta); (2) auditoria geral do plugin em 4 dimensões com verificação manual dos achados.
**Fora de escopo declarado**: refactor de outros agents; release; itens P2/P3 da auditoria.

> Nota: registro escrito em 2026-07-06, retroativamente, a partir da transcrição da sessão. Worklogs passam a ser escritos no fechamento da própria rodada a partir de agora.

## Arquivos lidos (relevantes pra decisão)
- `agents/mos-copy.md`, `subagents/copy-agent.md` (headers + seções alvo): base da auditoria de copy
- `scripts/hooks/quality_gate_hook.py`, `scripts/quality_gate.py`, `scripts/tests/test_quality_gate.py`: entender as camadas antes de estender
- `scripts/tests/test_commands_dispatch.py`: contratos que o command novo precisava passar
- `scripts/validate_agents.py`: onde ancorar o guard novo
- ROADMAP, SKILL.md, README, AGENTS.md: contagens e mapa de dispatch

## Arquivos alterados/criados
- `scripts/hooks/quality_gate_hook.py`: +2 HARD BLOCKs de antítese (com span anti-falso-positivo) +1 WARN (variante suave); IGNORECASE unificado
- `scripts/quality_gate.py`: check "Vícios de IA" novo; score capado em 60 quando viola regra obrigatória
- `scripts/tests/test_quality_gate_hook.py` (novo): o hook não tinha teste nenhum
- `scripts/tests/test_quality_gate.py`: classe TestCheckAITells
- `agents/mos-copy.md`: Bash na tools list; lint determinístico virou passo real; gate de antítese; awareness level no schema; protocolo de swipe file pessoal; drift "3510 linhas" removido
- `commands/otimizar-copy.md` (novo): diagnóstico + score + reescrita de copy existente
- `subagents/copy-agent.md`: trilhos do swipe-file vivo; snapshot guards (PARTE XVI e 6.2)
- `scripts/validate_agents.py`: guard "script referenciado sem Bash" (exceção: init_agent_memory.py, que é instrução pro usuário)
- README/AGENTS/SKILL/VALIDATION-GUIDE: contagens 38/34 e correções de drift
- `scripts/tests/test_workspace_separation.py`: allowlist +3 (referências a workspace/ por design)

## Decisões (e alternativas rejeitadas)
- Antítese como HARD BLOCK, não WARN: a regra do usuário é absoluta; regex com span que exclui pontuação interna pra evitar falso positivo entre cláusulas (alternativa "warn pra tudo" rejeitada por diluir a regra)
- Swipe file pessoal em `workspace/` (gitignored) em vez de append nos assets distribuídos: assets ficam no install dir do plugin pra usuários finais; escrever lá é errado por design
- Guard de Bash como warning que `--strict` transforma em bloqueio de CI (padrão do validator existente)

## Evidências
- Suite: 1885 passed, 2 skipped (após allowlist do workspace)
- `validate_agents.py --strict`: 18/18 clean
- Smokes end-to-end: hook bloqueou antítese com exit 2; CLI capou score em 60 com veredicto de revisão; guard flagrou agent sintético sem Bash
- Auditoria: 4 subagents Explore em paralelo + verificação manual; **6 claims refutados** (mos-email não tem protocolo de memory no body; hooks não dependem de Bash do agent; requirements não está quebrado, apify_client é módulo local e yaml tem fallback; seo-agent TEM índice; open(args.file) em CLI não é path traversal; /otimizar-copy tem required inputs)

## Testes
- Rodados: tier padrão completo + testes novos + 3 smokes manuais (outputs na transcrição)
- Não rodados e motivo: smoke tests (`-m smoke`) exigem sessão/tokens; install real não aplicável (sem release)

## Falhas da taxonomia tocadas
- Prevenidas: F-COPY-01 (antítese nas 3 camadas), F-BLOAT-02 (guard de instrução morta), F-DOC-01 (contagens), F-DOC-03 (snapshot guards), F-CMD-01 (command novo com dispatch)
- Identificadas e deixadas em backlog: F-ROUTE-03 (3 agents órfãos), F-CODEX-03 (narracao.aiff.txt na raiz), F-REL-02 (CHANGELOG parado)

## Rubrica aplicada
- Retroativo: rubricas não existiam na data. Auto-avaliação a posteriori: R1≈4 (guard + testes com falsos positivos cobertos), R2≈3 (contagens no mesmo diff; worklog só agora), R3≈3 (routing evals ainda não existiam).

## Custo aproximado
- Não medido em tokens (plataforma não expunha na sessão). Proxy: 1 sessão de fronteira, ~15 arquivos tocados, 4 subagents de auditoria.

## Riscos e follow-ups
- Regex de antítese pode gerar falso positivo não previsto em produção: mitigado por testes de casos limítrofes; ajustar COM teste se aparecer.

## Próximos passos (estado em 2026-06-12)
- P0: commit do trabalho (feito depois); drift de clones 34/35/36; fallback morto criar-post.md:54; numpy no requirements; narracao.aiff.txt; "48 scripts"
- P1: paridade dos agents fracos (email, seo, video, storytelling) vs padrão mos-copy
- P2: mos-offer; entry points pra growth/ab-testing; P3: release v6.9.0, docs archive, workflows cross-links
