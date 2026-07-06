# Worklog: nivelamento completo dos 21 agents + 21 KBs (5 ondas)

- **Data**: 2026-07-06/07
- **Executores**: Onda B pelo mantenedor (Claude); ondas A, C, D, E delegadas ao Cursor Composer (composer-2.5-fast) com briefs fechados; revisão frontier entre todas
- **Origem**: auditoria completa pós-v6.13.0 (backlog em memória do projeto, vereditos de remoção: nenhuma estrutural)

## O que mudou por onda

| Onda | Commit | Conteúdo |
|------|--------|----------|
| A | 8729e74 | Mecânica: 34 clones (5 agents), contagens de linhas de KB removidas de 13 agents (H8.5), ÍNDICE em brand/email/funnel/launch KBs, 34 snapshot guards + 1 aviso de fact-check em 8 KBs, lógica invertida do mos-design corrigida, 6 linhas de delegação (offer/community/research) |
| A-fix | c767ff0 | Correção da revisão: 4 "35 clones" em subagents (escopo do brief era estreito demais), header "Brand book primeiro" no design |
| B | 2469cbf | Paridade de domínio: PRE-FLIGHT + auto-iteração nos 13 agents faltantes; red team em growth/ab-testing/analytics/ai-tools/funnel; Régua ICE Canônica (eram 3 réguas contraditórias, uma delas com fórmula × e exemplos calculados por média); memory 21/21 (+ab-testing, ai-tools, audio, growth); audio ganha WebSearch+Bash (capability morta destravada); Bash em ai-tools/funnel/community; analytics ganha consciência do pipeline /aprender; sync init_agent_memory/AGENTS.md/README/SKILL.md |
| C | 9068f3e | memory_writer.py nos protocolos dos 21 (categorias mapeadas por item, exceção story bank do storytelling em edição direta); swipe files pessoais de ads (ads-aprovados.md) e offer (ofertas-aprovadas.md) com leitura no protocolo + append no resultado; allowlist do workspace |
| D | 0572177 | Dedup conservador de KBs (−26 linhas líquidas, +78/−102 brutas): email teoria→email-agent canônico (funnel −39), vieses→copy-agent PARTE I, compliance em cross-ref sem remoção (redundância local é proteção), template DADOS DO VÍDEO 5x→1+refs, snapshot guard nos Mestres do social |
| E | 3a46e1d | Gate 1 comprimido nos 21 agents (ADR-0002: hook é canônico); itens específicos de domínio preservados (spam triggers do email, siglas do ads, sem-aspas-em-falas de video/audio/storytelling) |

## Decisões de design registradas

1. **Régua ICE**: produto puro I×C×E (1-1000) com faixas 300+/150-299/100-149/<100, canônica na KB do ab-testing. Growth e ab-testing citam por referência; âncoras de pontuação por dimensão continuam na KB do growth.
2. **Red team seletivo**: só onde o custo do erro é alto (estatística, budget, arquitetura). Audio ficou sem red team; a auto-iteração de cold opens cobre o risco principal (H: red team em tudo vira cerimônia).
3. **Bash adicionado a 4 agents** (ai-tools, funnel, community, audio) como pré-requisito do memory_writer; sem isso a Onda C criaria instrução não executável.
4. **Dedup conservador**: na dúvida, referência cruzada em vez de corte. Compliance NUNCA cortado (gate de segurança local mantido).

## Falhas evitadas/encontradas

- Brief da Onda A restringiu "35 clones" a agents/ e as KBs ficaram de fora: o executor sinalizou o desvio no relatório em vez de improvisar, e a correção voltou pra ele (diretiva correção-volta-pro-executor). F-PROC: escopo de grep no brief deve cobrir o repo, não o diretório do sintoma.
- A citação Wharton estava em ai-tools-agent.md, não em copy-agent como a auditoria anotara; o executor confirmou a realidade antes de aplicar (comportamento correto de verificação de claim).
- Terceira régua ICE (KB, fórmula × com exemplos ÷) só apareceu na leitura da seção durante a execução; auditoria via matriz não pegou porque o threshold era plausível isoladamente. Lição: contradições numéricas exigem ler a SEÇÃO, não só o grep do número.

## Validação de fechamento

- Suite 2107 passed + validate_agents --strict 21/21 após CADA onda (execução independente do revisor, não só a do executor).
- Camada viva na integração final: RT-013/014/015/021/023 com 5/5 em command (4/5 exatos em todos os campos); a divergência do RT-021 foi provada instabilidade do método via controle no main pré-nivelamento (refinamento de critério documentado em ROUTING-EVALS.md: caso com command é pontuado por expected_command).
- black no CI scope; zero travessão em prosa nova de todas as ondas (grep no diff por onda).
