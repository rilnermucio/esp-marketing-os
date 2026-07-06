# 2026-07-06: Onda P1 (email/seo) + mos-offer + primeira camada viva

**Executor**: Claude Fable 5 via Claude Code
**Objetivo**: (1) nivelar mos-email e mos-seo ao padrão de paridade; (2) criar o 19º agent `mos-offer` com command e desempate; (3) primeira execução real dos routing evals medindo o estado final.
**Fora de escopo declarado**: release (fica pra quando o usuário quiser cortar v6.10.0); demais agents da matriz de paridade; `/criar-teste-ab`.

## Ordem executada (e por quê)

P1 → mos-offer → camada viva. A camada viva mede o estado final: RT-017 existia no golden set justamente pra testar o desempate que o mos-offer criaria.

## Arquivos alterados/criados (por frente)

**P1 (commit 5fc1741)**: `agents/mos-email.md` (Bash, memory, pre-flight de sequência high-stakes, auto-iteração de 8-12 subjects com lint, red team de deliverability), `agents/mos-seo.md` (memory, pre-flight de money page exigindo keyword research, auto-iteração de title/meta, red team "SEO do concorrente na posição 1"), `init_agent_memory.py` + contagens (12 memory).

**mos-offer (commit 7eeba62)**: `agents/mos-offer.md` (191 linhas, opus, paridade completa de nascença), `subagents/offer-agent.md` (KB com índice: equação de valor, Grand Slam, stack/bônus, garantias com CDC art. 49, precificação BR, escassez ética, Offer Score, por modelo, exemplos PT-BR, anti-padrões), `commands/criar-oferta.md`, desempate na SKILL, RT-017 atualizado + RT-019 novo, contagens 19/39/13 em README/AGENTS/SKILL/manifests, ROADMAP Fase 3 marcado entregue, guard `EXPECTED_AGENT_COUNT` atualizado conscientemente, pacote Codex rebuildado.

**Camada viva**: log em ROUTING-EVALS.md; nenhum arquivo de produto precisou de correção (6/6).

## Decisões (e alternativas rejeitadas)

- **KB do offer com ~380 linhas densas, não 3-5k**: v1 completa com índice supera volume; cresce com uso (H2.2, H8.3). A aplicação do stack em copy ficou em referência cruzada pra PARTE II-C do copy-agent, sem duplicar (H7.4).
- **mos-offer com `model: opus`**: precificação/garantia são trade-offs de raciocínio pesado, consistente com o critério do commit e46eeca.
- **Guard de contagem de agents renomeado** de `test_agents_count_is_eighteen` pra `test_agents_count_matches_expected` com constante comentada: o guard continua forçando reconhecimento consciente sem precisar renomear a função a cada agent.
- **Camada viva via headless `claude -p --plugin-dir` de diretório limpo**: evita duplo carregamento com o plugin instalado no projeto (v6.8.0 em scope project) e roda a decisão de roteamento real. Meta-instrução limita à declaração da rota (limitação documentada).

## Evidências

- `validate_agents.py --strict`: 19/19 clean (mos-offer com 2 knowledge refs válidas)
- Suite: 1992 passed, 2 skipped (inclui o guard novo de contagem e os 2 casos novos do golden set)
- O guard `test_agents_count_is_eighteen` QUEBROU quando o 19º agent entrou, como desenhado, e foi atualizado conscientemente (não silenciado)
- Camada viva 6/6: RT-002 (inline), RT-001 (criar-post, social+copy paralelo), RT-003 (otimizar-copy), RT-015 (analytics via linguagem natural), RT-017 (criar-oferta), RT-019 (offer via linguagem natural). ~18-30s por caso, modelo default da instalação
- Pacote Codex rebuildado e validado com os 19 agents

## Testes
- Rodados: suite completa 2x (P1 e offer), validate_agents --strict 2x, claude plugin validate, validate_codex_plugin, camada viva com 6 sessões headless reais
- Não rodados e motivo: smoke (tokens); install real (sem release nesta rodada)

## Falhas da taxonomia tocadas
- Corrigidas: F-ROUTE-03 parcial (offer nasce com command; ab-testing segue órfão), F-ROUTE-04 (desempate de oferta criado E validado ao vivo)
- Prevenidas: F-BLOAT-02 (tools coerentes desde o frontmatter), F-DOC-01 (contagens no mesmo diff, guard consciente), F-CODEX-01 (pacote rebuildado no mesmo commit)

## Rubrica aplicada
- R1 Implementação: 4 (guard quebrou e foi atualizado como desenhado; testes verdes; escopo por commit)
- R2 Documentação: 4 (tabela de sincronia do handbook coberta integralmente; ROADMAP atualizado)
- R3 Roteamento: 4 (golden set atualizado no mesmo diff + camada viva executada com 6/6)
- R4 Output de marketing: N/A | R5 Compatibilidade: 3 (validates verdes; install real fica pra release) | R6: N/A
- Veredito de merge: aprovado

## Custo aproximado
- 1 sessão de fronteira + 6 sessões headless curtas (~18-30s cada, modelo default). Tokens não expostos: "não medido".

## Riscos e follow-ups
- mos-offer novo em produção: primeiras ofertas reais devem alimentar a memory (take rate/refund) pra calibrar as referências da PARTE IV/V
- Camada viva mede decisão declarada, não dispatch executado (documentado); considerar eval de dispatch executado no futuro
- Push pendente de aprovação do usuário (3 commits locais)

## Próximos passos
1. Push + release v6.10.0 quando o usuário aprovar (CHANGELOG Unreleased já preparado)
2. Onda P1 seguinte: mos-video e mos-storytelling (os 4/10 da matriz)
3. `/criar-teste-ab` pra fechar o último órfão (RT-013)
4. Fase 2 do ROADMAP (mídia real) e Fase 4 (loop de métricas → memory)
