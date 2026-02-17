# content_calendar.py — Gerador de calendário editorial multiplataforma

O `content_calendar.py` gera um calendário editorial estruturado para múltiplas plataformas de redes sociais, cobrindo um período configurável de semanas. Para cada dia da semana, o script sugere tema, ideias de conteúdo, formatos recomendados e melhores horários de publicação. O resultado é exibido no terminal e salvo em um arquivo JSON.

## Uso via CLI

```bash
# Calendário de 4 semanas para Instagram (padrão)
python scripts/content_calendar.py 2026-02-17

# Especificar número de semanas
python scripts/content_calendar.py 2026-02-17 8

# Múltiplas plataformas
python scripts/content_calendar.py 2026-02-17 4 instagram linkedin

# Todas as plataformas suportadas
python scripts/content_calendar.py 2026-02-17 2 instagram linkedin twitter tiktok facebook
```

## Argumentos

| Argumento | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `data_inicio` | `str` (posicional) | Sim | — | Data de início no formato `YYYY-MM-DD` |
| `semanas` | `int` (posicional) | Não | `4` | Número de semanas a gerar (1–52) |
| `plataformas` | `str...` (posicionais) | Não | `["instagram"]` | Uma ou mais plataformas: `instagram`, `linkedin`, `twitter`, `tiktok`, `facebook` |

## Funções

### `generate_calendar(start_date, weeks, platforms, nicho) -> Dict`

Gera o calendário editorial completo iterando por todas as semanas e dias, associando temas, ideias, formatos e horários de publicação recomendados para cada plataforma.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `start_date` | `str` | Data de início no formato `YYYY-MM-DD` |
| `weeks` | `int` | Número de semanas a gerar (padrão: `4`) |
| `platforms` | `Optional[List[str]]` | Lista de plataformas (padrão: `["instagram"]`) |
| `nicho` | `str` | Nicho do criador de conteúdo (padrão: `"geral"`, informativo apenas) |

**Retorno:** `Dict` com chaves:

| Chave | Tipo | Descrição |
|-------|------|-----------|
| `calendar` | `List[Dict]` | Lista de semanas, cada uma com `week`, `start_date`, `end_date` e `days` |
| `summary` | `Dict` | Resumo: total de semanas, plataformas, nicho, datas de início e fim |
| `recommendations` | `Dict` | 5 recomendações gerais de operação (batch creation, scheduling, etc.) |
| `content_pillars` | `List[Dict]` | 4 pilares de conteúdo com percentual e exemplos |

**Estrutura de cada item em `calendar[n].days`:**

| Chave | Tipo | Descrição |
|-------|------|-----------|
| `date` | `str` | Data no formato `YYYY-MM-DD` |
| `day_of_week` | `str` | Nome do dia em inglês com inicial maiúscula |
| `theme` | `str` | Tema editorial do dia |
| `platforms` | `Dict` | Por plataforma: `suggested_times`, `content_ideas`, `formats`, `frequency` |

## Constantes

| Constante | Tipo | Descrição |
|-----------|------|-----------|
| `CONTENT_THEMES` | `Dict[str, Dict]` | Temas, ideias e formatos para cada dia da semana (`monday` … `sunday`). Cada entrada contém `theme` (str), `ideas` (List[str]) e `formats` (List[str]) |
| `BEST_TIMES` | `Dict[str, Dict]` | Melhores horários de publicação por plataforma, separados em `weekday` e `weekend`. Plataformas: `instagram`, `linkedin`, `twitter`, `tiktok`, `facebook` |
| `FREQUENCY` | `Dict[str, Dict]` | Frequência recomendada de publicação por plataforma e tipo de conteúdo (ex: `instagram.feed = "3-5/semana"`) |
| `USO` | `str` | String de ajuda exibida quando o script é chamado sem argumentos |
