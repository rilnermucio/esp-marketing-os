---
description: "Calendário comercial brasileiro: datas comerciais e culturais do ano com a antecedência ideal de campanha. Use quando perguntarem quais datas aproveitar ou quando começar a campanha de uma data."
argument-hint: "(sem args: próximos 90 dias) | --ano AAAA | --from YYYY-MM-DD --to YYYY-MM-DD"
---

# /datas-sazonais: Calendário Sazonal Comercial BR

Utilitário de dados. Mostra as efemérides comerciais e culturais brasileiras de uma janela, com a antecedência ideal pra começar a campanha e os nichos que mais aproveitam cada data. **Não despacha agents diretamente** (é fonte de dados, igual ao `/campanha` índice).

## Como usar

Roda o script determinístico `${CLAUDE_PLUGIN_ROOT}/scripts/seasonal_calendar_br.py` (sem necessidade de token):

```bash
# Próximos 90 dias (padrão)
python "${CLAUDE_PLUGIN_ROOT}/scripts/seasonal_calendar_br.py"
# ou via CLI unificado
python "${CLAUDE_PLUGIN_ROOT}/scripts/mos.py" seasonal list

# Ano inteiro
python "${CLAUDE_PLUGIN_ROOT}/scripts/seasonal_calendar_br.py" --ano 2026

# Janela específica
python "${CLAUDE_PLUGIN_ROOT}/scripts/seasonal_calendar_br.py" --from 2026-10-01 --to 2026-12-31

# JSON estruturado (pra alimentar outro passo)
python "${CLAUDE_PLUGIN_ROOT}/scripts/seasonal_calendar_br.py" --ano 2026 --json
```

## O que apresentar ao usuário

1. Liste as datas da janela pedida (data, nome, tipo, dias de antecedência ideal, nichos fortes).
2. Para cada data relevante ao nicho do usuário, **sugira o próximo passo** sem executar:
   - Black Friday / Cyber Monday → `/campanha-black-friday`
   - Datas de presente (Mães, Pais, Namorados, Natal, Crianças) → `/criar-calendario` ou `/campanha-lancamento` com o tema da data
   - Qualquer data → `/criar-post`, `/criar-carrossel` ou `/criar-anuncio` com o gancho sazonal
3. Respeite a antecedência: se a data já está dentro da janela de `dias_antecedencia_ideal`, marque como "começar agora".

## Cobertura

Datas fixas (Consumidor, Namorados, Cliente, Crianças, Natal, Ano Novo), por regra (Mães, Pais, Black Friday, Cyber Monday, Solteiro 11.11) e móveis via Computus (Carnaval, Páscoa, Sexta-feira Santa, Corpus Christi). Computadas pra qualquer ano, sem manutenção anual.
