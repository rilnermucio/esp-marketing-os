---
description: Workflow de projetos com pipeline declarativo, dispatch sequencial dos mos-* e approval gates entre stages. Subcomandos novo|list|status|avancar|aprovar|rejeitar.
argument-hint: "<subcomando> [args] (ex: novo \"Lançamento X\" --tipo lancamento)"
---

# /projeto: Gestão de projetos com workflow estruturado

Gerencia projetos de marketing como pipeline declarativo, com handoffs entre subagents `mos-*` e approval gates entre stages. Cada projeto vive em `workspace/projects/<slug>/` (gitignored).

## Subcomandos

- `/projeto novo "<nome>" --tipo {lancamento|perpetuo|consultoria|mentoria}`: cria projeto novo a partir do template
- `/projeto list`: lista todos os projetos com status atual
- `/projeto status <slug>`: mostra detalhe (pipeline, stage atual, último run)
- `/projeto avancar <slug>`: despacha o agente do stage atual e salva output como pending_approval
- `/projeto aprovar <slug>`: aprova último run e avança pra próximo stage
- `/projeto rejeitar <slug> "<feedback>"`: rejeita último run; próxima execução roda novamente com o feedback

## Como cada subcomando se comporta

### novo / list / status / aprovar / rejeitar, determinísticos

Roda direto via Bash, sem dispatch:

```
Bash("python scripts/project_manager.py <subcomando> [args]")
```

Mostra a saída do script direto pro usuário (já vem human-readable).

### avancar, orquestrador real

Esse subcomando NÃO é determinístico. Despacha um subagent. Fluxo:

1. **Lê estado:** `Bash("python scripts/project_manager.py status <slug>")` retorna pipeline, stage atual, agente daquele stage.
2. **Cria run pendente + folder:** `Bash("python scripts/project_manager.py avancar <slug>")` registra `run_NNN` em `runs.jsonl` com `status: pending` e cria `<NN>-<stage_id>/` automaticamente. O output do comando inclui o `folder` relativo.
3. **Monta contexto:** lê `workspace/projects/<slug>/project.md` (briefing) + outputs anteriores das pastas `<NN>-<stage>/` se existirem. Se a iteração for >1, lê o feedback de `decisions.md` e adiciona ao prompt.
4. **Despacha agente** com instrução explícita de output completo:

```
Agent(subagent_type: "mos-<x>", prompt: """
<briefing + outputs anteriores + feedback se houver>

INSTRUÇÃO DE OUTPUT (obrigatório):
Devolva o output COMPLETO verbatim na sua resposta. NÃO sumarize.
NÃO ofusque. O conteúdo do seu response será salvo direto em arquivo
e usado pelo próximo stage do pipeline. Sumário no final é opcional,
mas o output detalhado vem PRIMEIRO e completo.
""")
```

5. **Salva output:** o resultado da resposta vai pra `workspace/projects/<slug>/<NN>-<stage_id>/draft-vN.md` (NN é a posição do stage no pipeline; N é o número da iteração).
6. **Completa o run:** `Bash("python scripts/project_manager.py completar <slug> --output <NN>-<stage_id>/draft-vN.md")`. Esse comando atualiza o run pra `status: pending_approval`, adiciona `completed_at` e `output`. Se o stage tem `approval: skip`, **auto-aprova e avança**; senão pausa pra revisão humana.
7. **Mostra ao usuário:** preview do output + instrução "use `/projeto aprovar <slug>` ou `/projeto rejeitar <slug> \"motivo\"`" (a menos que tenha sido auto-aprovado).

Importante:
- Se `approval: skip` no stage atual, `completar` já avança automaticamente, não precisa chamar `aprovar` manualmente.
- Se já for o último stage do pipeline, ao aprovar marca o projeto como `status: completed`.
- Se houver iteração com feedback de rejeição anterior, incluir o feedback explicitamente no prompt do novo run.
- Quality Gates globais (ver `skills/marketing-os/SKILL.md`) se aplicam ao output do agente antes de salvar.

## Exemplo de uso completo

```
> /projeto novo "Lançamento Curso IA" --tipo lancamento
Projeto criado em workspace/projects/lancamento-curso-ia.
Stage atual: research. Pipeline: research → estrategia → funil → copy → design → ads.

> /projeto avancar lancamento-curso-ia
[mos-research roda automaticamente, despacha pesquisa de mercado]
Output salvo em 01-research/draft-v1.md.
Stage tem approval: skip, avancei automaticamente.
Próximo stage: estrategia (mos-launch).

> /projeto avancar lancamento-curso-ia
[mos-launch roda]
Output em 02-estrategia/draft-v1.md.
Use /projeto aprovar ou /projeto rejeitar.

> /projeto rejeitar lancamento-curso-ia "muito agressivo, suaviza tom"
Rejeitado. Feedback registrado em decisions.md.

> /projeto avancar lancamento-curso-ia
[mos-launch roda novamente, prompt agora inclui o feedback]
Output em 02-estrategia/draft-v2.md (iteration: 2).
```

## Quando NÃO usar /projeto

- **Tarefa one-shot rápida** (1 post, 1 email, 1 artigo): use `/criar-*` direto.
- **Pergunta conceitual:** responda inline sem criar projeto.
- **Campanha completa em paralelo sem precisar de approval:** use `/campanha-*` direto.

`/projeto` é pra quando você quer rastreabilidade entre stages, controle de aprovação e capacidade de retomar dias depois.

## Estrutura de arquivos por projeto

```
workspace/projects/<slug>/
├── project.md           # frontmatter (state machine) + briefing
├── runs.jsonl           # log append-only de execuções
├── decisions.md         # histórico de aprovações/rejeições
├── 01-<stage>/draft-v1.md
├── 02-<stage>/draft-v1.md
└── ...
```

## Templates de pipeline default (Fase 1)

Os pipelines são fixos por tipo no MVP. Para customizar, edite o `pipeline:` no frontmatter do `project.md` antes de rodar `/projeto avancar`.

| Tipo | Pipeline default |
|------|-----------------|
| `lancamento` | research → estrategia → funil → copy → design → ads |
| `perpetuo` | research → funil → copy → ads → analytics |
| `consultoria` | discovery → diagnostico → estrategia → deliverable |
| `mentoria` | planejamento → conteudo → comunidade → feedback |

## Limitações conhecidas (Fase 2 vai resolver)

- Pipeline 100% sequencial, sem paralelismo (ex: copy + design simultâneos)
- Approval só `required` ou `skip`: sem `auto_approve` com log
- Output e approval são o mesmo gate, sem distinção entre "aprovado pra avançar" e "publicado"
- Sem integração de publish (ex: postar no Notion automaticamente após aprovar)

Fase 2 entra se uso real mostrar dor.
