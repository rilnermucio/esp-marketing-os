# 2026-09-28: Implementação da auditoria de runtime e produto

**Executor**: Claude Opus 5.5 via Claude Code (desktop), com 3 subagentes de pesquisa (compliance BR, GEO/AEO, plataformas BR)
**Objetivo**: implementar todo o relatório da auditoria de 2026-09-28 ([worklog](2026-09-28-auditoria-runtime-e-produto.md)): P0 de privacidade e runtime instalado, P1 e P2 de scripts, conteúdo, roteamento e processo, oportunidades estruturais O1 a O4 e de produto P-a a P-h.
**Fora de escopo declarado**: reescrever o histórico público para apagar os `.docx` (exige force-push e aprovação), remover o marketplace sincronizado na conta claude.ai (ação do usuário), push, tag e release com bump de versão (aguardam aprovação), espanhol LATAM (só com ADR).

## Arquivos lidos (relevantes pra decisão)
- `docs/ai-engineering/worklogs/2026-09-28-auditoria-runtime-e-produto.md`: backlog e ordem das rodadas.
- `scripts/hooks/quality_gate_hook.py`, `hooks/hooks.json`, frontmatter dos 21 agents: fiação real do gate.
- Documentação oficial do Claude Code e sonda própria (`scratchpad/hookprobe`, Claude Code 2.1.283): hooks de frontmatter ignorados em agent de plugin, `agent_type` qualificado, memória nativa, `${CLAUDE_PLUGIN_ROOT}` e `context: fork` em command.
- Texto integral das normas de publicidade (CFM 2.336/2023, Código CFO, CFO-196 e CFO-271, CFN 599, CFP, Provimento OAB 205, CONAR 2026) salvo pela pesquisa e conferido artigo por artigo.
- Documentação oficial de Google Search Central, Search Console, GA4, OpenAI, Anthropic, Perplexity, Bing, WhatsApp, Threads, YouTube e Amazon para os fatos de plataforma.

## Arquivos alterados/criados
26 commits na branch `fix/auditoria-set2026`. Principais:
- Privacidade: 3 `.docx` fora do índice; `test_workspace_separation.py` trava a classe.
- Runtime instalado: `${CLAUDE_PLUGIN_ROOT}` e dispatch `marketing-os:mos-*` em agents, commands e SKILL.md; gate em `hooks/hooks.json`; `marketing_agent()` no hook; memória em `marketing-os-mos-*` com migração; `test_install_smoke.py`; ADR-0005 e ADR-0006.
- Dispatch pela plataforma: `/gerar-imagem` com `context: fork`; ADR-0007.
- Scripts: `test_cli_contracts.py` (flags contra o argparse por AST), `workspace_paths.py`, `install_doctor.py`, `utm_builder.py`, `voc_extractor.py`, `compliance_check.py`, `check_platform_facts.py`; bugs de template em roteiros e legendas.
- Conteúdo: `references/platform-facts.md` (35 linhas, 25 fatos com fonte e data), `references/compliance-br.md`, PARTE XII do seo-agent (GEO e AEO), Kwai, WhatsApp, Threads, LinkedIn e marketplaces nas KBs de social, copy e ads.
- Roteamento: SKILL.md como fonte única (457 linhas), golden set RT-032 a RT-044, descriptions em PT-BR.
- Commands novos: `/configurar-marca`, `/reaproveitar`, `/minerar-voc`, `/checar-compliance`, `/coletar-prova` (53 commands, 49 com dispatch).
- Evals: perfil `social`, `agent-output-cases.json` (AO-001 a AO-009) e baselines em `evals/baselines/{social,email,ads}/`.
- Processo: CI em Python 3.9, validador universal, ADRs 0005 a 0007, FAILURE-TAXONOMY (F-DIST-01 a 07, F-EVAL-05 e atualizações), RELEASE-CHECKLIST, AGENTS.md, CHANGELOG, ROADMAP (Fase 5).

## Decisões (e alternativas rejeitadas)
- Na resposta final, só o bloqueio fala com o agent (ADR-0008): aviso em `additionalContext` reabria o subagent. Mostrar avisos ao usuário por `systemMessage` foi rejeitado por ora, porque o aviso de compliance é condicional e tem falso positivo fora da categoria.
- Gate no nível do plugin (`hooks/hooks.json`) em vez de frontmatter: a plataforma ignora hooks em agent de plugin (sonda). Manter no frontmatter "por garantia" foi rejeitado porque dá falsa sensação de cobertura.
- Nome qualificado no dispatch e reescrita para nome curto no pacote universal: o Claude Code exige `marketing-os:mos-*`; ChatGPT Work e Codex leem `agents/mos-*.md`.
- `context: fork` só em command de agent único, sem aprovação no meio e com input no pedido (ADR-0007). Converter os 47 de uma vez foi rejeitado: o fork não vê a conversa. A primeira versão da ADR citava `/renderizar-imagem` como candidato por engano (a renderização depende da ferramenta Skill, que o agent não tem); corrigido com nota na própria ADR.
- `quality_gate.py` carrega os padrões do hook: a cópia própria já tinha divergido ("brutalmente", travessão curto).
- Compliance como aviso com a norma citada, sem bloqueio: a mesma frase pode ser vedada para dentista e permitida para médico; o hook não sabe a categoria. Bloqueio foi rejeitado por falso positivo.
- `/checar-compliance` por dispatch em texto (sem fork): a peça costuma vir da conversa.
- Pesquisa por subagente com legenda CONFIRMADO/PROVÁVEL/NÃO USAR e conferência própria dos itens mais sensíveis antes de entrar na KB. Itens NÃO USAR ficaram fora (duração máxima do Kwai, limite de título da Shopee, percentuais demográficos do Kwai).

## Evidências
- Smoke antes da correção: 3 de 4 testes falharam (KB não encontrada fora do repo, gate descartando `marketing-os:mos-copy`, escrita não gateada). Depois: todos passam, inclusive bloqueio e correção de violação real e memória nativa.
- Fork: `test_fork_command_runs_inside_declared_agent` passou em 66 s; o `SubagentStop` chegou com `agent_type` `marketing-os:mos-ai-tools` e foi avaliado pelo gate.
- Baselines AO-005 e AO-007 (primeira geração): o transcript do subagent mostra a peça completa entregue, um bloqueio corrigido e depois 3 rodadas só de avisos em `additionalContext`, cada uma reabrindo o agent, até a última mensagem virar "Peço desculpas, ainda deixei a palavra em caixa alta". O orquestrador recebeu essa nota e retomou o agent para recuperar a entrega. Corrigido pela ADR-0008; as 9 baselines foram regeradas com o gate novo (brutos antigos preservados no scratchpad como evidência).
- Baseline AO-001 antes da correção do gate: a variação 2 continha "Não é falta de equipamento caro. São cinco ajustes simples." e passou. O regex só aceitava "é" na afirmação. Corrigido com teste que fixa o caso e outro que protege "São Paulo".
- Normas conferidas no texto integral: CFO art. 20, IX ("consultas e diagnósticos gratuitos ou sem compromisso"), art. 44, I e VII; CFO-271 art. 1º (brinde, premiação e sorteio seguem vedados); CFM art. 11, XII e XIII; CFP art. 20, a a h; CFN 599 arts. 56 a 58; Provimento 205 arts. 3º e 6º; CONAR Anexos B e C.
- Fatos de plataforma conferidos na fonte oficial: guia de IA generativa do Google (lista do que ignorar, atualizado em 10/07/2026), relatório e controle de IA do Search Console (31/08/2026), canal AI Assistant do GA4, robôs da OpenAI, Anthropic e Perplexity, FAQ rich result encerrado em 07/05/2026, thumbnail do YouTube em 3840x2160, Threads 500 caracteres mais anexo de 10.000, anúncios no Threads no Brasil (jan/2026), título da Amazon em 75 caracteres (27/07/2026).
- Suíte estática: 2262 testes no início da rodada; 2875 passando no fim, sem skips.
- Baselines do P-g (depois da ADR-0008): 9 peças completas, nenhuma com travessão ou vício de IA, scores de 66 a 90. No AO-005, um bloqueio e o reenvio da sequência inteira (16,8 mil caracteres); no AO-007, uma única parada. No AO-009, o `mos-ads` abriu a entrega com alerta citando o Código de Ética Odontológica (art. 20, IX, e art. 44, I) e tirou a "avaliação gratuita" pedida no briefing.

## Testes
- Rodados: `python -m pytest scripts/tests/ -q -m "not smoke"` verde em cada commit; `black --check scripts/*.py scripts/hooks/`, `flake8 scripts/`, `python scripts/validate_agents.py --strict`, `python scripts/build_codex_plugin.py --check`, `python scripts/validate_codex_plugin.py plugins/marketing-os`, `claude plugin validate .` (passa; aviso antigo sobre `category`).
- Smoke com modelo real (`MOS_SMOKE=1`): `test_install_smoke.py` 7 de 7 com o gate da ADR-0008 (192 s), inclusive o fork e a trava de no máximo 2 paradas por dispatch; `test_agents_smoke.py` 21 de 21 agents (19 min, Haiku).
- Não rodados e motivo: julgamento par a par das baselines novas (a baseline é a régua; a primeira comparação acontece na próxima mudança desses agents); teste real no ChatGPT Work e no Codex (RT-031 e RT-028 exigem conversa nova nesses clientes); `/plugin install` a partir do marketplace (depende de push e release).

## Falhas da taxonomia tocadas
- Corrigidas: F-DIST-01 a F-DIST-06, F-COPY-01 (antítese com "São"), F-COPY-04, F-COPY-05 (laço de avisos na resposta final), F-CLAIM-02, F-DOC-03, F-BLOAT-02, F-EVAL-05, F-CMD-03, F-ROUTE-02.
- Mitigada: F-ROUTE-01 (fork no piloto) e F-DIST-07 (install doctor; a remoção da cópia sincronizada é do usuário).
- Risco novo: F-DOC-03 para `compliance-br.md` (norma muda); mitigado pelo aviso de 90 dias no `mos.py facts check`.

## Rubrica aplicada
- Distribuição e runtime 4/4 (smoke real verde); roteamento 4/4 (golden set cruzado com os commands); qualidade de copy 3/4 (gate mais forte e baselines novas, julgamento par a par pendente); documentação 4/4 (contagens com guard, ADRs 0005 a 0008, CHANGELOG). Veredito: merge sim, após as decisões do usuário listadas em "Riscos".

## Custo aproximado
- Não medido em tokens. Smoke com Haiku remapeado (centavos); baselines do P-g com Sonnet (9 execuções de 2 a 8 minutos); 3 pesquisas em subagente de 20 a 35 minutos cada.

## Riscos e follow-ups
- Histórico público ainda contém os 3 `.docx`: reescrever exige force-push e decisão do usuário.
- O app desktop carrega a cópia sincronizada 6.1.5 do marketplace "Marketing-OS" da conta claude.ai; `mos.py install doctor` mostra o conflito, e a remoção é do usuário.
- Sem push, tag nem bump de versão: o release segue o RELEASE-CHECKLIST com aprovação.
- KBs ainda têm cerca de 240 travessões em exemplos (tarefa separada sugerida).
- `/checar-compliance` sinaliza risco e não substitui parecer jurídico; a referência precisa de revisão trimestral.

## Próximos passos
- Decidir sobre histórico, marketplace da conta e release.
- Rodar a primeira comparação par a par contra as baselines AO-001 a AO-009 quando mos-social, mos-email ou mos-ads mudarem.
- Avaliar `/minerar-voc` e `/narrar-roteiro` com `context: fork` (material em arquivo) depois de uso real do piloto. A auditoria sugeria piloto de 2 ou 3 commands; ficou em 1 porque o fork não vê a conversa e os outros candidatos mudam de UX. `/renderizar-imagem` não cabe: a renderização usa uma skill do ambiente pelo orquestrador.
- Limpar travessões dos exemplos das KBs, com guard.
