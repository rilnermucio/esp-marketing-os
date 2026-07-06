# Implementation Log

> Template e índice dos registros de rodada. Cada rodada de implementação não-trivial gera um arquivo em [worklogs/](worklogs/) com o nome `YYYY-MM-DD-slug.md`. Este arquivo define o formato e indexa as rodadas.

## O que conta como "rodada não-trivial"

Qualquer sessão que altere comportamento, estrutura ou documentação canônica. Fica dispensado: typo fix isolado, bump de versão puramente mecânico já coberto pelo checklist de release.

## Template (copiar para worklogs/YYYY-MM-DD-slug.md)

```markdown
# YYYY-MM-DD: <título da rodada>

**Executor**: <modelo ou humano, ex: Claude Fable 5 via Claude Code>
**Objetivo**: <1-2 frases; o que o usuário pediu ou o problema atacado>
**Fora de escopo declarado**: <o que foi deliberadamente deixado de fora>

## Arquivos lidos (relevantes pra decisão)
- <path>: <por quê>

## Arquivos alterados/criados
- <path>: <o que mudou, 1 linha>

## Decisões (e alternativas rejeitadas)
- <decisão>: <por quê; alternativa considerada e motivo da rejeição>

## Evidências
- <output de teste, número medido, incidente verificado; nada de "deve funcionar">

## Testes
- Rodados: <comando + resultado resumido, ex: "pytest -m 'not smoke': 1885 passed">
- Não rodados e motivo: <ex: smoke tests exigem sessão Claude Code interativa>

## Falhas da taxonomia tocadas
- <IDs de FAILURE-TAXONOMY.md que esta rodada previne, corrige ou introduz risco>

## Rubrica aplicada
- <notas 0-4 por dimensão aplicável de RUBRICS.md + veredito merge sim/não>

## Custo aproximado
- <quando disponível: tokens/tempo/modelo; senão "não medido" e por quê>

## Riscos e follow-ups
- <o que pode quebrar depois; o que foi adiado>

## Próximos passos
- <backlog acionável que a próxima rodada deve considerar>
```

## Campos obrigatórios

Todos os campos do template. "Evidências" exige dado verificado (output real de comando, número contado, arquivo lido); afirmação sem verificação não é evidência. "Testes não rodados e motivo" existe pra impedir omissão silenciosa: não rodou, declara.

## Índice de rodadas

| Data | Rodada | Worklog |
|---|---|---|
| 2026-06-12 | Hardening de copy + auditoria geral (retroativo) | [2026-06-12-copy-hardening-e-auditoria.md](worklogs/2026-06-12-copy-hardening-e-auditoria.md) |
| 2026-07-06 | Criação da camada de engenharia de IA | [2026-07-06-camada-ai-engineering.md](worklogs/2026-07-06-camada-ai-engineering.md) |
| 2026-07-06 | Execução do P0 da auditoria | [2026-07-06-execucao-p0.md](worklogs/2026-07-06-execucao-p0.md) |
