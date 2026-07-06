# Taxonomia de falhas do Marketing OS

> Canônico. Atualizado em 2026-07-06. Todo bug, eval e post-mortem referencia estas falhas por ID. Formato do ID: `F-<CATEGORIA>-<NN>`. Os IDs são estáveis: nunca renumere; deprecie com nota e crie novo.
>
> "Exemplo real" cita incidente deste repositório quando existe; "hipotético" marca risco com precedente externo. Detecção aponta o mecanismo executável quando há.

## F-ROUTE: Roteamento

| ID | Falha | Exemplo real / risco | Detecção | Prevenção |
|---|---|---|---|---|
| F-ROUTE-01 | Produção de marketing executada inline em vez de dispatch | Pré-v6.5: 8 de 25 commands produziam inline | `test_commands_dispatch.py`; matriz de routing evals | Protocolo de dispatch no AGENTS.md; H3.1 |
| F-ROUTE-02 | Briefing roteado pro command/agent errado | Hipotético (medido pelo golden set) | [evals/routing-cases.json](evals/routing-cases.json) + revisão manual | Triggers concretos nas descriptions; mapa da SKILL |
| F-ROUTE-03 | Agent sem porta de entrada (órfão de exposição) | Auditoria jun/2026: mos-growth, mos-ab-testing, mos-infoproduct com 1 command cada | Mapa de cobertura command→agent (auditoria) | R3 "Exposição"; decisão de produto por agent |
| F-ROUTE-04 | Ambiguidade de domínio sem regra de desempate | Oferta high-ticket cai em infoproduct, funnel ou copy sem regra escrita | Casos RT-017 do golden set | H4.2: ambiguidade recorrente vira regra na SKILL |

## F-DISP: Dispatch

| ID | Falha | Exemplo real / risco | Detecção | Prevenção |
|---|---|---|---|---|
| F-DISP-01 | Sequencial onde cabia paralelo (latência) ou paralelo com dependência real (output inconsistente) | Hipotético; regra existe desde v6.5 | Revisão contra H3.4 | "Por que esse dispatch" obrigatório no command |
| F-DISP-02 | Prompt de dispatch sem inputs mínimos; subagent recebe briefing vazio | Hipotético (medido pelos campos mínimos do golden set) | Routing evals: `min_output_fields` | H3.3: prompt de dispatch é API auto-contida |
| F-DISP-03 | Dispatch pra agent inexistente | Risco em rename de agent | `test_commands_dispatch.py::test_dispatched_agents_exist` | Guard já ativo |

## F-COPY: Qualidade de copy

| ID | Falha | Exemplo real / risco | Detecção | Prevenção |
|---|---|---|---|---|
| F-COPY-01 | AI-tells: travessão, "brutal", antítese negação→afirmação, clichês | Recorrente até jun/2026 (motivou o gate de antítese em 3 camadas) | `quality_gate_hook.py` (HARD BLOCK) + `quality_gate.py` (score capado em 60) | [QUALITY-GATES.md](QUALITY-GATES.md) |
| F-COPY-02 | Hook fraco, CTA fraco, promessa sem prova | Medido, não bloqueado | `quality_gate.py` (checks de hook/CTA) + Copy Score System | Auto-iteração com scoring (H1.1) |
| F-COPY-03 | Estouro de limite de plataforma (chars, formato) | Hipotético | `quality_gate.py --type` + Gate 4 do mos-copy | Tabela de limites no agent |

## F-PTBR: Língua

| ID | Falha | Exemplo real / risco | Detecção | Prevenção |
|---|---|---|---|---|
| F-PTBR-01 | Texto sem acentuação correta | Recorrente em outputs de modelos menores | `quality_gate.py::check_accents` (MUST_ACCENT_WORDS) | Gate 3 dos agents; hook |
| F-PTBR-02 | Framework gringo traduzido literalmente sem adaptação BR | Hipotético | Revisão humana (LLM-graded futuro) | Anti-padrão declarado nos agents |

## F-CLAIM: Claims sem fonte

| ID | Falha | Exemplo real / risco | Detecção | Prevenção |
|---|---|---|---|---|
| F-CLAIM-01 | Estatística/citação/case publicado sem verificação | Números "direcionais" na PARTE XVI do copy-agent exigiram aviso de fact-check | Gate 2 (fact-check via WebSearch, classificação CONFIRMADO/PROVÁVEL/NÃO USAR) | WebSearch na tools list de quem tem o gate |
| F-CLAIM-02 | Disclaimer regulatório ausente (CVM/ANVISA/CONAR/afiliado) | Coberto desde a criação do hook | `quality_gate_hook.py` (COMPLIANCE WARN) + compliance auto-detection do mos-copy | Tabela de triggers→disclaimers |

## F-BLOAT: Inchaço de agent

| ID | Falha | Exemplo real / risco | Detecção | Prevenção |
|---|---|---|---|---|
| F-BLOAT-01 | Knowledge profunda subindo pro Tier 1 | Contido: Tier 1 médio ~245 linhas (2026-07) | `validate_agents.py` reporta `lines`; revisão | H2.1; convenção nº1 do AGENTS.md |
| F-BLOAT-02 | Instrução morta (capacidade citada sem tool correspondente) | mos-copy mandava rodar quality_gate.py sem Bash (jun/2026) | `validate_agents.py --strict` (guard de script-ref sem Bash) | H1.2 |
| F-BLOAT-03 | Mesma regra duplicada em N arquivos sem fonte canônica | Quality gates repetidos em ~20 arquivos (agents, commands, SKILL, AGENTS) | Auditoria; ainda sem guard | H7.4; plano no [ADR-0002](adr/0002-defesa-em-tres-camadas.md) |

## F-CMD: Drift de commands

| ID | Falha | Exemplo real / risco | Detecção | Prevenção |
|---|---|---|---|---|
| F-CMD-01 | Command de produção sem dispatch e sem declarar utility | Motivou o guard em v6.5 | `test_commands_dispatch.py::test_no_unexpected_non_dispatch_commands` | Guard ativo |
| F-CMD-02 | Referência temporal/stale dentro de command | `criar-post.md:54` ainda cita "durante migração" (aberto, P0) | Auditoria; grep por "ainda não existir", "durante a migração" | H3.5 |
| F-CMD-03 | Contagem de commands divergente entre docs | 25/32/34/37 simultâneos até jun/2026 | Auditoria; guards de consistência | H8.5 |

## F-MAN: Manifests

| ID | Falha | Exemplo real / risco | Detecção | Prevenção |
|---|---|---|---|---|
| F-MAN-01 | Violação dos gotchas de manifest (localização, author string, category plural, source bare, field skills) | v6.1.0 a v6.1.6: cada item quebrou install em produção | `claude plugin validate .` + tabela de gotchas | Tabela no AGENTS.md; teste real de install |
| F-MAN-02 | Versão dessincronizada entre plugin.json e marketplace.json | Risco em todo bump | `test_plugin_manifest.py`; checklist de release | Bump nos 3 pontos no mesmo commit |

## F-CODEX: Pacote Codex

| ID | Falha | Exemplo real / risco | Detecção | Prevenção |
|---|---|---|---|---|
| F-CODEX-01 | Pacote com estrutura inválida | Risco desde 2026-07 (distribuição nova) | `python scripts/validate_codex_plugin.py` | Rodar no CI e no checklist de release |
| F-CODEX-02 | Versão base dessincronizada ou sufixo `+codex.YYYYMMDD` esquecido | Risco em release | validate_codex (semver) + checklist | R5 "Versões" |
| F-CODEX-03 | Conteúdo pessoal vazando pro pacote (workspace/, memory, áudio de teste) | `narracao.aiff.txt` trackeado na raiz (aberto, P0) | Inspeção do output de `build_codex_plugin.py` | Lista COPY_DIRS/COPY_FILES explícita; nunca copiar raiz inteira |

## F-REL: Release

| ID | Falha | Exemplo real / risco | Detecção | Prevenção |
|---|---|---|---|---|
| F-REL-01 | Tag apontando pra commit fora do main | v6.7 e v6.8: recovery via reset + force-push + retag | `git merge-base --is-ancestor <tag> main` | Passo obrigatório do checklist |
| F-REL-02 | CHANGELOG não cobre o range da release | 15+ commits sem entrada entre v6.8.0 e jul/2026 | `git log <última-tag>..HEAD` vs CHANGELOG | Checklist |
| F-REL-03 | Release publicada sem teste real de install | Motivou a regra "validate é necessário mas não suficiente" (v6.1.x) | Install em projeto limpo | Checklist |

## F-DOC: Documentação desatualizada

| ID | Falha | Exemplo real / risco | Detecção | Prevenção |
|---|---|---|---|---|
| F-DOC-01 | Contagem drifted em prosa | Clones citados como 34/35/36 em lugares diferentes até jul/2026 (real: 34; o "35" veio de off-by-one da própria auditoria, pego pelo guard `test_repo_consistency`); scripts 48/50/52 em 30 dias | Guard `test_readme_counts_match_filesystem`; grep numérico | H8.5: frase sem número > número com guard > número solto |
| F-DOC-02 | Doc histórica sem banner tratada como atual | VALIDATION-RESULTS-v6.5.0.md; SUBAGENTS-EXPANSION-PLAN.md | Auditoria de docs | Banner "histórico" no topo ou mover pra archive/ |
| F-DOC-03 | Seção datada sem snapshot guard | PARTE XVI do copy-agent (corrigido jun/2026) | Grep por anos/meses em KBs | H2.3 |

## F-EVAL: Evals frágeis

| ID | Falha | Exemplo real / risco | Detecção | Prevenção |
|---|---|---|---|---|
| F-EVAL-01 | Assert de valor exato onde range/presença basta | Risco padrão; suite atual usa ranges (`0 <= score <= 100`) | Revisão de PR de teste | [EVALS-STRATEGY.md](EVALS-STRATEGY.md) §anti-fragilidade |
| F-EVAL-02 | Eval não parametrizado: arquivo novo escapa da cobertura | Evitado por design em `test_commands_dispatch.py` (glob + parametrize) | Revisão | Padrão glob+parametrize pra qualquer coleção de arquivos |
| F-EVAL-03 | Flaky tratado como quebrado (ou ignorado como flaky sem registro) | `test_pdf_generator::test_cli_basic` flaca sob carga, passa isolado | Re-rodar isolado antes de debugar | Registro do flake conhecido (memória + este doc) |

## F-COST: Custo e contexto

| ID | Falha | Exemplo real / risco | Detecção | Prevenção |
|---|---|---|---|---|
| F-COST-01 | Ler KB inteira (800 a 6.529 linhas) pra tarefa pontual | Risco permanente; KBs sem índice agravam | Revisão de transcript | H2.2 (índices) + H5.2 (ler a PARTE) |
| F-COST-02 | Processo pesado em peça trivial (red team em microcopy) | Anti-pattern documentado no mos-copy | Revisão | Trigger de red team condicionado a high-stakes |
| F-COST-03 | Modelo errado pro trabalho (opus em tarefa mecânica; modelo leve em raciocínio pesado) | Commit e46eeca calibrou opus pros agents de raciocínio pesado | Revisão do frontmatter `model:` | [COST-CONTROL.md](COST-CONTROL.md) |
| F-COST-04 | Output inflado (10 variações entregues, tabela redundante, eco do briefing) | Risco permanente | Revisão | H5.4 |

## F-REG: Regressão silenciosa

| ID | Falha | Exemplo real / risco | Detecção | Prevenção |
|---|---|---|---|---|
| F-REG-01 | Mudança em área sem guard passa despercebida | SKILL.md ficou com "32 commands" por várias versões | Auditorias periódicas | Converter achado recorrente em guard (princípio 3) |
| F-REG-02 | Edição no Tier 2 quebra contrato de PARTE citada pelo Tier 1 | Risco em toda reorganização de KB | Grep por consumidores antes de renomear | H2.5; candidato a guard futuro |
