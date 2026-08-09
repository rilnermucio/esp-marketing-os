# 2026-08-05: Compatibilidade skills-only com ChatGPT Work

**Executor**: Codex (GPT-5)
**Objetivo**: aplicar as recomendações para disponibilizar o Marketing OS no ChatGPT Work, preservando o mesmo contrato de Avatar, USP, Oferta e os demais especialistas; atualizar e verificar a instalação local.
**Fora de escopo declarado**: criar ou hospedar servidor MCP; adicionar autenticação ou estado remoto; publicar no diretório público; criar release, tag, commit, push ou PR; alterar a distribuição Claude; declarar como aprovado um teste de conversa Work que não foi observado.

## Arquivos lidos (relevantes pra decisão)

- `AGENTS.md` e `docs/ai-engineering/OPERATING-MODEL.md`: arquitetura, gates e processo obrigatório desta rodada.
- `skills/marketing-os/SKILL.md`, `skills/marketing-os/agents/openai.yaml` e `.codex-plugin/plugin.json`: contrato atual da skill e superfície universal.
- `scripts/build_codex_plugin.py`, `scripts/validate_codex_plugin.py` e testes de distribuição: build, validação e lacunas de cobertura.
- `docs/ai-engineering/ROUTING-EVALS.md`, `evals/routing-cases.json`, `RUBRICS.md`, `RELEASE-CHECKLIST.md` e ADRs: gabarito, aceitação e decisões estruturais.
- Skills `plugin-creator`, `chatgpt-apps`, `openai-docs` e `computer-use`, incluindo suas referências exigidas: formato portátil, fronteira MCP, documentação oficial e verificação do aplicativo real.
- Documentação oficial OpenAI de plugins, skills-only, marketplaces locais, uso no ChatGPT Work, submissão e erros de listagem: fonte da compatibilidade e dos limites públicos.
- Histórico JSONL desta tarefa: prova do estado Git limpo antes da rodada e reconstrução da sequência do incidente local.

## Arquivos alterados/criados

- `.codex-plugin/plugin.json`: apresentação universal para ChatGPT Work e Codex, categoria pública válida, descrição curta dentro do limite e starters de Avatar, USP e Oferta.
- `.agents/plugins/marketplace.json`: categoria `Business & Operations`.
- `skills/marketing-os/SKILL.md`: modo ChatGPT Work, semântica de `@Marketing OS`, roteamento por linguagem natural e fallback sem multi-agent ou shell.
- `skills/marketing-os/agents/openai.yaml`: descrição curta, prompt inicial e invocação implícita portátil.
- `scripts/validate_codex_plugin.py`: guards de listagem pública, pacote skills-only, frontmatter, `agents/openai.yaml`, marketplace e prompts.
- `scripts/build_codex_plugin.py`: linguagem universal no build.
- `scripts/tests/test_chatgpt_distribution.py`: contratos de manifesto, marketplace, skill, metadados OpenAI, documentação e preflight de symlink.
- `scripts/tests/test_codex_distribution.py`: regressões para metadados públicos e metadados de skill não portáveis.
- `docs/ai-engineering/evals/routing-cases.json` e `ROUTING-EVALS.md`: RT-028 a RT-031 para Avatar, USP, Oferta e pergunta conceitual com `@Marketing OS`.
- `docs/ai-engineering/adr/0004-chatgpt-work-skills-only.md` e índice de ADRs: decisão estrutural de reutilizar o pacote skills-only.
- `docs/ai-engineering/FAILURE-TAXONOMY.md`: F-CODEX-04 para atualização local que segue link simbólico.
- `docs/ai-engineering/RUBRICS.md` e `RELEASE-CHECKLIST.md`: ChatGPT Work incluído na aceitação e preflight seguro incluído na distribuição local.
- `README.md`, `AGENTS.md` e `CHANGELOG.md`: instalação, uso, arquitetura, regras universais e seção Unreleased.
- `plugins/marketing-os/`: pacote universal regenerado a partir da fonte.
- `docs/ai-engineering/IMPLEMENTATION-LOG.md` e este arquivo: índice e registro da rodada.

## Decisões (e alternativas rejeitadas)

- Manter um único pacote universal skills-only. O Marketing OS entrega conhecimento, instruções e scripts locais; um MCP acrescentaria hospedagem, autenticação e política de dados sem resolver uma necessidade atual.
- Tratar `@Marketing OS` como prefixo de seleção. O texto restante continua governando o command, o agent e a decisão entre dispatch e resposta inline.
- Preservar Tier 1/Tier 2 nos três hosts. ChatGPT Work e Codex leem somente os especialistas necessários e consolidam no agente principal quando multi-agent não estiver disponível.
- Omitir `policy.products`. A documentação oficial admite o campo opcional, mas o validador portátil instalado o rejeita; a ausência mantém descoberta universal e passa nos dois contratos atuais.
- Usar `Business & Operations`. `Marketing` não pertence à lista pública aceita pelo diretório universal.
- Manter a versão de fonte `6.15.0+codex.20260805`. A rodada não publica release; somente a cópia local recebe cachebuster temporal.
- Substituir a origem pessoal simbólica por uma pasta física, preservando o link antigo como backup. A instalação oficial 6.15.0 foi removida localmente para evitar duas skills com o mesmo nome; pode ser reinstalada pelo marketplace oficial.
- Registrar F-CODEX-04 e exigir preflight com `test ! -L` e `realpath`. A correção local isolada não protegeria a próxima atualização.

## Evidências

- A documentação oficial confirma que plugins somente com skills são aceitos no ChatGPT Work e no Codex, e que o ChatGPT Desktop lê marketplaces repo-scoped e pessoais.
- A ficha real do ChatGPT Desktop exibiu `Marketing OS`, descrição `Marketing completo em PT-BR`, uma skill habilitada, categoria `Business & Operations`, três starters corretos e versão local final `6.15.0+codex.20260805043747`.
- `codex plugin list` mostrou `marketing-os@plugins-cli` instalado e habilitado; a entrada oficial de mesmo nome ficou `not installed`.
- O cache final contém as instruções de ChatGPT Work, `@Marketing OS`, `/criar-avatar`, `/criar-usp` e `/criar-oferta`.
- O destino `/Users/rilner/plugins/marketing-os` terminou como pasta física. O link anterior foi preservado em `/Users/rilner/plugins/marketing-os.repo-link-backup-20260805`.
- O update final passou pelo preflight: destino não simbólico, diretório existente e `realpath` diferente de `pwd -P`; a cópia foi feita sem `--delete`.
- Antes desta rodada, `git status --short` estava vazio no histórico da própria tarefa.
- Durante a primeira atualização, `/Users/rilner/plugins/marketing-os` era um link para a raiz do repositório. `rsync --delete` seguiu esse link e removeu `.git`, `.github`, `.agents`, `docs`, `scripts/tests` e outros arquivos não distribuídos. Esse é o incidente F-CODEX-04.
- A recuperação salvou o conteúdo sobrevivente em `/private/tmp/mos-recovery.d13tLU`, clonou `origin/main`, sobrepôs a base sem exclusões e reaplicou o snapshot distribuível do cache. Arquivos de engenharia desta rodada foram reconstruídos e o pacote foi regenerado.
- Depois da recuperação, o Git mostrou somente os arquivos intencionais desta rodada; `git diff --check`, build, validadores e a suíte integral passaram.
- O estado Git limpo anterior comprova ausência de mudanças versionadas ou não versionadas conhecidas. Arquivos ignorados pelo Git não podem ser auditados retroativamente; o histórico não registra conteúdo pessoal conhecido nesse destino e não havia snapshot local do Time Machine.

## Testes

- Rodados: `python -m pytest scripts/tests/ -q -m "not smoke" -W error::DeprecationWarning --cov=scripts --cov-report=term --cov-report=xml --cov-fail-under=70`: 2.205 passed, 2 skipped, 23 deselected, cobertura 70,82%.
- Rodados: testes focados de ChatGPT, Codex e roteamento: 169 passed.
- Rodados: `python scripts/validate_agents.py --strict`: 21/21 clean, sem warnings.
- Rodados: `black --check --diff scripts/*.py scripts/hooks/`: 58 arquivos inalterados.
- Rodados: `flake8 scripts/`: aprovado.
- Rodados: `claude plugin validate .`: aprovado com o warning histórico de `category` no manifesto Claude.
- Rodados: build, `build_codex_plugin.py --check`, validador canônico, validador portátil e quick validator da skill: aprovados.
- Rodados: JSON dos manifests e do golden set, YAML de `agents/openai.yaml` e `git diff --check`: aprovados.
- Rodados: descoberta visual no ChatGPT Desktop e releitura da versão final instalada: aprovadas.
- Não rodados e motivo: 23 smoke tests exigem rede, credenciais ou serviços externos; submissão pública não foi autorizada; uma resposta dentro de conversa Work nova não foi observada porque `Testar agora` e o starter permaneceram na ficha enquanto esta tarefa estava ativa.

## Falhas da taxonomia tocadas

- F-ROUTE-02 e F-ROUTE-04: o prefixo ChatGPT e os domínios Avatar, USP e Oferta entraram no golden set.
- F-DISP-02: RT-028 a RT-030 preservam dependências e inputs mínimos.
- F-CLAIM-01: Avatar, USP e Oferta continuam separando evidência, inferência e hipótese.
- F-COST-02: RT-031 garante que pergunta conceitual permaneça inline.
- F-MAN-01: metadados públicos e portabilidade passaram em validadores independentes.
- F-CODEX-01, F-CODEX-02 e F-CODEX-03: estrutura, versão e separação do pacote foram verificadas.
- F-CODEX-04: incidente local recuperado e convertido em preflight documentado com teste.
- F-REL-03: descoberta no cliente real foi comprovada; execução em conversa Work continua explicitamente parcial.

## Rubrica aplicada

- R1 Implementação: 4. Contratos de host, fallback e metadados têm guards executáveis e suíte integral verde.
- R2 Documentação: 4. README, AGENTS, changelog, ADR, taxonomia, checklist, rubrica e worklog refletem a decisão e o incidente.
- R3 Roteamento: 3. Golden set determinístico cobre ChatGPT Work; execução viva em conversa separada ainda precisa ser observada.
- R4 Output de marketing: N/A. A rodada altera distribuição, não produz peça de cliente.
- R5 Compatibilidade ChatGPT Work, Claude Code e Codex: 3. Pacote, instalação e ficha real estão comprovados; resposta de conversa Work ficou pendente.
- R6 Release: N/A. Nenhuma release, tag, publicação ou push foi executado.
- Veredito: pronto para revisão e uso local, com publicação pública e conversa Work viva fora do escopo comprovado.

## Custo aproximado

- Não medido. Os validadores e o aplicativo não expuseram custo monetário desta rodada.

## Riscos e follow-ups

- A ficha do plugin está funcional e habilitada, mas o botão de teste não saiu da página durante esta tarefa. Uma conversa Work nova deve ser exercitada depois que a tarefa atual terminar.
- A instalação é pessoal e local. Disponibilidade no ChatGPT Work pela web para outros usuários exige compartilhamento ou submissão pública.
- MCP continua adiado. Ele passa a fazer sentido se o produto precisar de estado remoto, conectores autenticados, UI própria ou telemetria centralizada.
- O backup simbólico preservado ainda aponta para o repositório. Ele não participa do marketplace; deve ser removido somente depois de confirmação explícita do usuário.
- O Git não consegue provar a existência anterior de arquivos ignorados. Novas atualizações locais devem usar o preflight F-CODEX-04 antes de qualquer sincronização.

## Próximos passos

- Abrir uma conversa Work nova após encerrar esta tarefa e rodar RT-031, seguido de um caso de produção como RT-028.
- Se a execução viva passar, registrar o resultado em `ROUTING-EVALS.md` e elevar R3/R5 para 4.
- Quando o usuário quiser distribuição externa, executar o checklist de release e o fluxo oficial de compartilhamento ou submissão pública.
- Reavaliar ADR-0004 somente quando existir uma necessidade concreta de MCP.
