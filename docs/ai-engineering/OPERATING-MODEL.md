# Operating Model: como um agente de IA trabalha neste repo

> Canônico. Atualizado em 2026-07-06. Se este documento conflitar com um pedido explícito do usuário, o pedido vence; registre a exceção no worklog.

## Princípios (em ordem de precedência)

1. **Medir antes de mudar.** Refatoração ampla só depois de existir rubrica/eval que detecte melhora ou piora. Se a régua não existe, criá-la é a primeira entrega da rodada.
2. **Menor fatia útil.** Uma rodada = um tema. Fix pontual não vira refactor; feature não carrega reorganização de pasta junto.
3. **Guard-rail antes de convenção.** Toda regra que já quebrou uma vez vira teste ou validador, não parágrafo de doc. Exemplos vivos: `scripts/tests/test_commands_dispatch.py` (command sem dispatch), `scripts/validate_agents.py` (frontmatter, refs de knowledge, script referenciado sem Bash).
4. **Verificar claims com os próprios olhos.** Output de subagente, auditoria ou doc antiga é hipótese, não fato. Precedente real: na auditoria de 2026-06, 6 claims de subagentes auditores caíram em fact-check manual (detalhes em `worklogs/2026-06-12-copy-hardening-e-auditoria.md`).
5. **Documentação faz parte do diff.** Contagens, tabelas e docs afetados são atualizados no mesmo commit da mudança, nunca "depois".

## Ordem de leitura por tipo de tarefa

| Tarefa | Ler antes (nesta ordem) |
|---|---|
| Qualquer sessão | `AGENTS.md` (raiz) → este arquivo |
| Criar/alterar agent Tier 1 ou KB Tier 2 | [HEURISTICS.md](HEURISTICS.md) §1-2 → [MAINTAINER-HANDBOOK.md](MAINTAINER-HANDBOOK.md) §agents → agent de referência (`agents/mos-copy.md`) |
| Criar/alterar command | [HEURISTICS.md](HEURISTICS.md) §3 → `scripts/tests/test_commands_dispatch.py` (contratos) → command de referência (`commands/criar-email.md`) |
| Alterar quality gates | [QUALITY-GATES.md](QUALITY-GATES.md) inteiro |
| Diagnosticar bug | [FAILURE-TAXONOMY.md](FAILURE-TAXONOMY.md) → [runbooks/](runbooks/) |
| Release | [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md) inteiro, sem pular passo |
| Mudança de arquitetura | [adr/](adr/) existentes → [RUBRICS.md](RUBRICS.md) → escrever ADR novo antes do código |
| Roteamento/descriptions | [ROUTING-EVALS.md](ROUTING-EVALS.md) + rodar `pytest scripts/tests/test_routing_evals.py` |

## Ciclo de trabalho de uma rodada

```
1. SCOUT      git log/status, estado real dos arquivos que o pedido toca.
              Nunca confiar em memória de sessão anterior sem re-verificar.
2. ESCOPO     Declarar o que entra e o que fica fora. Backlog vivo está em
              worklogs/ (seção "Próximos passos" da última rodada).
3. AUDITAR?   Ver critérios abaixo. Se sim, auditoria vem antes e vira artefato.
4. IMPLEMENTAR Menor fatia útil. Teste novo nasce junto do comportamento novo.
5. VALIDAR    python -m pytest scripts/tests/ -m "not smoke" -q
              python scripts/validate_agents.py --strict
              python scripts/validate_codex_plugin.py   (se tocou distribuição)
6. DOCUMENTAR Contagens, tabelas, docs afetados no mesmo diff.
7. REGISTRAR  Worklog da rodada + ADR se houve decisão estrutural.
```

## Quando auditar antes de implementar

Audite primeiro (e entregue a auditoria como artefato) quando **qualquer um** valer:

- A mudança toca 3+ subsistemas (agents, commands, scripts, docs, manifests).
- O pedido usa palavras como "melhorar", "otimizar", "refatorar" sem alvo específico.
- Existe suspeita de drift entre docs e realidade (contagens, versões, features).
- A última auditoria tem mais de 60 dias ou não cobre a área.

Implemente direto quando: o alvo é específico, o raio de mudança é conhecido, e existe teste cobrindo a área (ou o fix é o teste).

## Quando pedir aprovação humana vs prosseguir

**Pare e pergunte** antes de:

- Ação destrutiva sobre conteúdo que você não criou: `git rm`, sobrescrever arquivo com conteúdo divergente do descrito, force-push, retag, delete de branch.
- Publicação externa: push, criação de tag/release, publish em marketplace, post em qualquer serviço externo.
- Mudança de escopo: o pedido era X e a solução correta parece ser Y estrutural.
- Trade-off de produto sem resposta no repo (ex: "esse agent novo entra no escopo?"; a régua de escopo mora em `docs/ROADMAP.md`, seção "Princípio de escopo").

**Prossiga sem bloquear** quando: a ação é reversível, está dentro do escopo pedido, e a decisão tem default óbvio no repo (siga o padrão existente e registre no worklog). Ficar perguntando "posso?" para ações reversíveis dentro do escopo é falha de processo, não prudência.

## Como limitar escopo (anti-derrapagem)

- Declare no início do worklog: objetivo em 1 frase + lista "fora de escopo".
- Descobriu problema fora do escopo? Registre em "Próximos passos" do worklog e siga. Não conserte no mesmo diff, exceto typo trivial na linha que você já está editando.
- Commits temáticos: `feat(...)`, `fix(...)`, `docs(...)`, `test(...)` separados. O histórico deste repo segue esse padrão; mantenha.
- Se a rodada passar de ~10 arquivos modificados fora do tema declarado, pare e reavalie o escopo.

## Como registrar decisões

| Tipo de decisão | Onde | Exemplo real |
|---|---|---|
| Estrutural / difícil de reverter | [adr/](adr/) | Manter arquitetura two-tier ([ADR-0001](adr/0001-arquitetura-two-tier.md)) |
| Regra de qualidade nova | [QUALITY-GATES.md](QUALITY-GATES.md) + teste | Gate de antítese (2026-06) |
| Escopo de produto (entra/não entra) | `docs/ROADMAP.md` | Scheduler fica fora do plugin |
| Aprendizado operacional de uma rodada | worklog da rodada | Claims de auditores refutados |
| Gotcha de plataforma | `AGENTS.md` (tabela de gotchas) | plugin.json precisa estar em `.claude-plugin/` |

## Anti-padrões de processo (todos já aconteceram)

| Anti-padrão | Incidente real | Prevenção |
|---|---|---|
| Confiar em claim de subagente sem verificar | Auditoria jun/2026: "requirements quebrado", "seo-agent sem índice" e mais 4 claims falsos | Fact-check manual de todo achado grave antes de reportar/agir |
| Corrigir contagem sem criar guard | Contagens de commands divergiram 4x (25/32/34/37 simultâneos em docs) | Preferir frase sem número; quando número for necessário, guard test |
| Tag apontando pra commit fora do main | Releases v6.7/v6.8 exigiram reset + force-push + retag | Checklist de release, passo "verificar ancestralidade da tag" |
| Instrução morta em prompt | mos-copy mandava rodar script sem ter Bash na tools list | `validate_agents.py` agora bloqueia em `--strict`; rode sempre |
| Refatorar sem régua | (evitado até aqui; este documento existe pra continuar assim) | Princípio 1 |
