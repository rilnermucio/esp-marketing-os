---
name: {name}
slug: {slug}
type: mentoria
status: active
current_stage: planejamento
default_approval: required
created_at: {created_at}
pipeline:
  - id: planejamento
    agent: mos-infoproduct
    approval: required
  - id: conteudo
    agent: mos-copy
    approval: required
  - id: comunidade
    agent: mos-social
    approval: required
  - id: feedback
    agent: mos-analytics
    approval: skip
---

# Briefing: {name}

## Cohort/Turma
[Nome da turma, número de alunos]

## Tema central
[Sobre o que é a mentoria]

## Duração
- Início: {created_at}
- Fim: [data]
- Frequência: [semanal / quinzenal]

## Promessa de transformação
[O que o aluno sai sabendo/conseguindo]

## Notas adicionais
[Detalhes relevantes]
