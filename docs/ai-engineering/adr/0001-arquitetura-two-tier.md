# ADR-0001: Arquitetura two-tier com skill orquestradora

**Status**: aceito
**Data**: 2026-07-06
**Autor**: Claude Fable 5 (mantenedor sênior), a partir da auditoria de 2026-06-12 e medições de 2026-07-06

## Contexto

O pedido "verifique se a arquitetura foi feita da melhor forma e se os agents/subagents são todos necessários" exige um veredito registrado, com números. Estado medido em 2026-07-06:

| Camada | Medida |
|---|---|
| Tier 1 (`agents/mos-*.md`, 18 arquivos) | 4.411 linhas somadas (~245/agent; maior: mos-copy com 399) |
| Skill orquestradora (`SKILL.md`) | 430 linhas |
| Tier 2 (`subagents/*-agent.md`, 18 KBs) | 66.201 linhas somadas (mín: ab-testing 800; máx: ads 6.529) |
| Commands | 38 (34 com dispatch) |
| Guard tests | ~1.900 no tier padrão |

## Decisão

**Manter a arquitetura em 4 formas: Tier 1 enxuto + Tier 2 sob demanda + skill orquestradora + camada determinística (hooks/scripts/guards). Não consolidar nem expandir agents sem um ciclo de medição de uso.**

O racional central é custo de contexto com profundidade preservada: o conhecimento total (66k linhas) é ~15x o que se carrega por sessão (4,4k). Carregar tudo sempre seria proibitivo; não ter o conhecimento nivelaria o output por baixo. O design atual paga o mínimo fixo e compra profundidade só quando o briefing exige. Além do custo: KBs evoluem sem tocar dispatch (edição livre no Tier 2), dispatch paralelo isola contextos, e tools/memory/model são calibráveis por domínio.

## Veredito sobre os 18 agents ("são todos necessários?")

**Núcleo confirmado (13)**: copy, social, video, email, ads, seo, research, funnel, launch, infoproduct, design, brand, analytics. Domínio claro, exposição por commands, regras de desempate existentes ou triviais.

**Zona de observação (5)**, com hipótese registrada e critério de decisão:

| Agent | Sinal | Hipótese | Decidir quando |
|---|---|---|---|
| mos-ab-testing | KB de 800 linhas (a menor), 1 command, fronteira difusa com growth/analytics | Fundir com mos-growth num agent de experimentação OU ganhar `/criar-teste-ab` | Após 1 ciclo de medição de uso (camada viva dos routing evals + memória de dispatches) |
| mos-growth | 1 command, sobreposição parcial com analytics/funnel | Mesmo destino do ab-testing (fusão os tornaria coesos) | Idem |
| mos-storytelling | Tier 1 mais fraco da matriz de paridade (sem WebSearch com gate de fatos; sem memory) | Reforçar primeiro (P1 da auditoria); julgar necessidade só depois de nivelado | Após onda P1 |
| mos-audio | Menos diferenciado de video; sem WebSearch/Bash | Manter (ganhou `/narrar-roteiro` em jun/2026, tem tração); documentar fronteira audio×video na SKILL | Reavaliar se ficar 2 ciclos sem uso |
| mos-ai-tools | Fronteira com design exige atenção | Manter: a divisão "design dirige, ai-tools prompta" é regra de desempate válida | Estável |

**Gap na direção oposta**: existe demanda sem dono (oferta/monetização, caso RT-017 do golden set). `mos-offer` está previsto no ROADMAP Fase 3 e é prioridade maior que qualquer consolidação.

**Regra desta decisão**: remoção ou fusão de agent é mudança irreversível pra usuários (briefings roteados, memórias por projeto). Só acontece com dado de uso, nunca por estética de arquitetura. O plano histórico de expandir para 32 agents (`docs/archive/SUBAGENTS-EXPANSION-PLAN.md`) permanece rejeitado: o overhead de roteamento e desempate cresce combinatoriamente e já há 3 agents subexpostos com 18.

## Alternativas consideradas

1. **Agent monolítico com KB única**: rejeitado. 66k linhas não cabem em contexto; domínios se contaminam; paralelismo desaparece.
2. **Só skill + KBs (sem agents nativos)**: rejeitado. Perde isolamento de contexto por dispatch, tools por domínio, `memory: project` por domínio e hooks por agent.
3. **Granularidade maior (32 agents)**: rejeitado (acima).
4. **Mover conhecimento pra RAG/embedding externo**: rejeitado por ora. Adiciona infraestrutura e dependência externa a um plugin que hoje é Python+Markdown puro e roda offline; o mecanismo Read-sob-demanda com índices cumpre o papel num custo aceitável. Critério de revisão abaixo.

## Duplicações identificadas (dívida registrada, não resolvida aqui)

1. **Quality gates repetidos em ~20 arquivos** (agents, SKILL, AGENTS.md, commands): tratado no [ADR-0002](0002-defesa-em-tres-camadas.md) com plano de redução gradual.
2. **Workflows × padrões da SKILL desalinhados** (numeração e cross-links; 7 de 10 arquivos órfãos): plano em HEURISTICS H6.2.
3. **Sumários de Tier 1 que espelham a KB** (risco H5.3): monitorar no review; teto informal de 400 linhas por agent Tier 1.

## Consequências

Positivas: custo fixo de sessão baixo e estável; evolução de conhecimento desacoplada; qualidade calibrável por domínio; a matriz de paridade (auditoria jun/2026) dá um caminho claro de nivelamento.

Negativas (custo aceito): sincronia Tier1↔PARTEs da KB é manual (F-REG-02, candidato a guard futuro); contagens vivem em 3 docs (mitigado por H8.5 e pela tabela de sincronia do MAINTAINER-HANDBOOK); a fronteira entre agents vizinhos exige regras de desempate escritas e casos no golden set.

## Critério de revisão

Reabrir este ADR se: (a) um ciclo de medição mostrar 2+ agents com uso ~zero e sem porta de entrada planejada; (b) o mecanismo de plugins ganhar forma nativa de knowledge loading que torne o Read-sob-demanda obsoleto; (c) o Tier 1 somado passar de ~6.000 linhas (inflação estrutural); ou (d) a distribuição Codex exigir forma diferente de empacotar conhecimento.
