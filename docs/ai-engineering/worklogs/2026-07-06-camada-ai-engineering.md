# 2026-07-06: Criação da camada de engenharia de IA

**Executor**: Claude Fable 5 via Claude Code (última rodada antes da virada de cobrança por uso: sessão deliberadamente usada pra construir alavancas, não operar manivelas; ver COST-CONTROL §2)
**Objetivo**: criar `docs/ai-engineering/` completa (modelo operacional, heurísticas, rubricas, taxonomia, estratégia de evals, golden set executável, gates, custo, release, handbook, ADRs, runbooks, worklogs) ANTES de qualquer refactor amplo, e registrar o veredito de arquitetura como ADR.
**Fora de escopo declarado**: executar o backlog P0-P3 da auditoria; release v6.9.0; refactor de agents; mudanças no pacote Codex.

## Arquivos lidos (relevantes pra decisão)
- Scout de estado: git log/status/tags, `.codex-plugin/plugin.json`, `scripts/build_codex_plugin.py` e `validate_codex_plugin.py` (headers), `.github/workflows/tests.yml`, wc -l de agents/SKILL/subagents
- Base de conhecimento da sessão: auditoria de 2026-06-12 (transcrição + memória do projeto), evitando re-auditar

## Arquivos alterados/criados
- `docs/ai-engineering/`: README, OPERATING-MODEL, IMPLEMENTATION-LOG, HEURISTICS, RUBRICS, FAILURE-TAXONOMY, EVALS-STRATEGY, ROUTING-EVALS, QUALITY-GATES, COST-CONTROL, RELEASE-CHECKLIST, MAINTAINER-HANDBOOK
- `docs/ai-engineering/adr/`: README, TEMPLATE, 0001 (arquitetura two-tier: veredito), 0002 (gates em 3 camadas com hook canônico)
- `docs/ai-engineering/evals/`: README + `routing-cases.json` (18 casos PT-BR)
- `docs/ai-engineering/runbooks/`: README + install-failure-debug
- `docs/ai-engineering/worklogs/`: este arquivo + backfill de 2026-06-12
- `scripts/tests/test_routing_evals.py` (novo): valida golden set contra commands/, agents/ e taxonomia
- `AGENTS.md`: seção-ponteiro pra camada

## Decisões (e alternativas rejeitadas)
- **Golden set em JSON, não YAML**: stdlib pura no teste, zero risco de dependência (yaml é opcional no repo por design)
- **IDs de taxonomia estáveis (F-CAT-NN) referenciados pelo golden set e validados por teste**: cria acoplamento verificável entre docs e evals (alternativa "docs soltos" rejeitada: doc sem consumo executável drifta)
- **Hook como fonte canônica dos gates (ADR-0002)** com redução gradual da duplicação; gerador automático adiado por H8.3
- **Consolidação de agents adiada com critério explícito (ADR-0001)**: remoção/fusão só com dado de uso; observação registrada pra ab-testing, growth, storytelling, audio
- **Camada viva dos routing evals é manual por enquanto**: medir roteamento real exige sessão; automatizar isso agora seria eval frágil (F-EVAL) e caro

## Evidências
- `test_routing_evals.py`: 92 passed em 0.05s na primeira execução (consistência golden set ↔ repo ↔ taxonomia)
- Suite completa + lint: ver seção Testes
- Números do ADR-0001 medidos na sessão (wc -l): Tier 1 = 4.411 linhas/18 agents; SKILL = 430; Tier 2 = 66.201 (800 a 6.529)
- Estado re-verificado antes de escrever (princípio 4): working tree limpo, Codex packaging presente, P0 da auditoria majoritariamente ainda aberto

## Testes
- Rodados: `pytest scripts/tests/test_routing_evals.py` (92 passed); suite completa `-m "not smoke"` + black/flake8 nos arquivos novos (resultado no fechamento da rodada)
- Não rodados e motivo: smoke (tokens/sessão); install real (sem release nesta rodada)

## Falhas da taxonomia tocadas
- Prevenidas: F-REG-01 (regras viram guard: golden set testado), F-EVAL-01/02 (estratégia anti-fragilidade codificada), F-REL-01..03 (checklist com verificação de ancestralidade), F-DOC-02/03 (carimbos e banners nos docs novos)
- Registradas como dívida: F-BLOAT-03 (plano no ADR-0002), F-ROUTE-03/04 (casos RT-013/RT-017 medem)

## Rubrica aplicada
- R1 Implementação: 4 (teste novo verde, escopo respeitado, guard acoplando docs↔dados)
- R2 Documentação: 4 (carimbos de data, links relativos, índice no README da pasta, drift-proofing por referência)
- R3 Roteamento: 3 (golden set criado; camada viva ainda não rodada em sessão real)
- R5 Compatibilidade: N/A (não tocou manifests/pacote) | R4 Output de marketing: N/A | R6 Release: N/A
- Veredito de merge: aprovado (≥3 em todas as aplicáveis)

## Custo aproximado
- 1 sessão de modelo de fronteira; ~22 arquivos criados/editados; leitura limitada a scout dirigido (sem re-auditoria). Tokens não expostos pela plataforma: "não medido". Racional de custo: sessão cara construindo o sistema que baixa o custo das próximas (COST-CONTROL §2).

## Riscos e follow-ups
- Docs canônicos novos podem driftar como os antigos: mitigação estrutural = golden set com teste, carimbos de data, tabela de sincronia no handbook; mitigação de processo = worklog obrigatório
- O resumo em ROUTING-EVALS.md duplica o JSON (aceito: legibilidade; o JSON vence e o teste protege o JSON)
- Camada viva do routing eval precisa da primeira execução real pra calibrar o gabarito

## Próximos passos
1. **P0 da auditoria (continua aberto)**: drift de clones (34/36→35 em README:3,137,154 e AGENTS:101; correção posterior na mesma data: o valor real é 34, ver worklog execucao-p0), fallback morto `commands/criar-post.md:54`, numpy no requirements.txt, "48 scripts"→50 no AGENTS.md, remover `narracao.aiff.txt` da raiz (trackeado!), revisar CONNECTORS.md
2. **Release v6.9.0** pelo RELEASE-CHECKLIST novo (CHANGELOG parado em v6.8.0 com 16+ commits acumulados)
3. **Onda P1 de paridade** começando por mos-email e mos-seo, medida pelas rubricas + matriz de paridade
4. **Primeira execução da camada viva** dos routing evals (5+ casos) e calibração do gabarito
5. **mos-offer** (ROADMAP Fase 3): maior gap de produto; RT-017 já espera por ele
