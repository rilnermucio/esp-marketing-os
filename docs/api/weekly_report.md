# weekly_report.py — Gerador automático de relatório semanal de performance

O `weekly_report.py` coleta e agrega métricas de conteúdo, SEO e email marketing para gerar um relatório semanal completo em formato Markdown. O script aceita dados via arquivo JSON ou opera com um template vazio, e salva o relatório em `output/reports/`.

## Uso via CLI

```bash
# Relatório da semana atual (template vazio)
python scripts/weekly_report.py

# Semana específica no formato ISO
python scripts/weekly_report.py --week 2026-W07

# Com dados de entrada em JSON
python scripts/weekly_report.py --input dados.json

# Salvar em caminho específico
python scripts/weekly_report.py --output relatorio.md

# Semana específica + dados + imprimir no terminal
python scripts/weekly_report.py --week 2026-W06 --input dados.json --print

# Combinação completa
python scripts/weekly_report.py --week 2026-W06 --input dados.json --output output/reports/semana-06.md --print
```

## Argumentos

| Argumento | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `--week`, `-w` | `str` | Não | Semana atual | Semana no formato ISO `YYYY-Www` (ex: `2026-W07`) |
| `--input`, `-i` | `str` | Não | `None` | Caminho para arquivo JSON com dados da semana |
| `--output`, `-o` | `str` | Não | `output/reports/semana-YYYY-Www.md` | Caminho do arquivo de saída |
| `--format`, `-f` | `str` | Não | `markdown` | Formato de saída (atualmente apenas `markdown`) |
| `--print`, `-p` | flag | Não | `False` | Imprimir relatório no terminal além de salvar |

### Estrutura do JSON de entrada (`--input`)

```json
{
  "week": "2026-W07",
  "content": [
    {
      "titulo": "string",
      "plataforma": "string",
      "formato": "string",
      "alcance": 0,
      "engajamentos": 0,
      "cliques": 0,
      "saves": 0,
      "shares": 0,
      "data": "2026-02-16"
    }
  ],
  "seo": [
    {
      "url": "string",
      "titulo": "string",
      "posicao_media": 0.0,
      "impressoes": 0,
      "cliques": 0,
      "ctr": 0.0
    }
  ],
  "email": {
    "enviados": 0,
    "taxa_abertura": 0.0,
    "taxa_clique": 0.0,
    "taxa_conversao": 0.0,
    "taxa_descadastro": 0.0
  },
  "meta_geral": {}
}
```

## Funções

### `get_current_week() -> str`

Retorna a semana atual no formato ISO `YYYY-Www`.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| — | — | Sem parâmetros |

**Retorno:** `str` — Ex: `"2026-W07"`

---

### `get_week_dates(week_str: str) -> tuple`

Retorna as datas de início (segunda-feira) e fim (domingo) de uma semana ISO.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `week_str` | `str` | Semana no formato `YYYY-Www` |

**Retorno:** `tuple[datetime, datetime]` — `(data_inicio, data_fim)`

**Exceção:** `ValueError` se o formato for inválido.

---

### `parse_week_number(week_str: str) -> int`

Extrai o número da semana de uma string no formato `YYYY-Www`.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `week_str` | `str` | Semana no formato `YYYY-Www` |

**Retorno:** `int` — Número da semana (1–52)

---

### `collect_content_metrics(content_list: List[Dict]) -> Dict`

Coleta e agrega métricas de uma lista de conteúdos publicados. Calcula alcance total, engajamento total, taxa de engajamento média, e classifica os top/bottom 3 conteúdos por engajamento relativo.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `content_list` | `List[Dict]` | Lista de dicionários com dados de cada conteúdo publicado |

**Retorno:** `Dict` com chaves:

| Chave | Tipo | Descrição |
|-------|------|-----------|
| `total_pecas` | `int` | Total de peças na lista |
| `alcance_total` | `int` | Soma de todos os alcances |
| `engajamento_total` | `int` | Soma de todos os engajamentos |
| `taxa_engajamento_media` | `float` | Média das taxas individuais (%) |
| `top_conteudos` | `List[Dict]` | Top 3 por engajamento relativo |
| `bottom_conteudos` | `List[Dict]` | Bottom 3 por engajamento relativo |
| `por_plataforma` | `Dict` | Agregação por plataforma |
| `por_formato` | `Dict` | Contagem por formato |

---

### `collect_seo_metrics(urls: List[Dict]) -> Dict`

Coleta e agrega métricas de SEO para uma lista de URLs. Identifica quick wins (posições 4–15 com CTR baixo) e lista as top páginas por cliques.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `urls` | `List[Dict]` | Lista de URLs com métricas do Google Search Console |

**Retorno:** `Dict` com chaves:

| Chave | Tipo | Descrição |
|-------|------|-----------|
| `total_urls` | `int` | Total de URLs analisadas |
| `impressoes_total` | `int` | Soma de impressões |
| `cliques_total` | `int` | Soma de cliques orgânicos |
| `ctr_medio` | `float` | CTR médio (%) |
| `posicao_media_geral` | `float` | Posição média geral |
| `quick_wins` | `List[Dict]` | Até 5 páginas com maior potencial de melhoria de CTR |
| `top_paginas` | `List[Dict]` | Top 5 páginas por cliques |

---

### `generate_next_week_recommendations(content_metrics, seo_metrics, email_metrics) -> List[str]`

Gera uma lista de recomendações textuais para a próxima semana com base nas métricas da semana atual.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `content_metrics` | `Dict` | Saída de `collect_content_metrics()` |
| `seo_metrics` | `Dict` | Saída de `collect_seo_metrics()` |
| `email_metrics` | `Optional[Dict]` | Dicionário com métricas de email (pode ser `None`) |

**Retorno:** `List[str]` — Lista de recomendações em linguagem natural.

---

### `generate_suggested_calendar(week_str: str, platforms: List[str]) -> List[Dict]`

Gera uma sugestão de calendário editorial para a semana seguinte à `week_str`.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `week_str` | `str` | Semana de referência no formato `YYYY-Www` |
| `platforms` | `List[str]` | Lista de plataformas (ex: `["instagram", "linkedin"]`) |

**Retorno:** `List[Dict]` — Lista de entradas de calendário com `data`, `dia_semana`, `plataforma`, `tema` e `formato_sugerido`.

---

### `generate_weekly_report(week_data: Dict) -> str`

Gera o relatório semanal completo em formato Markdown, combinando métricas de conteúdo, SEO e email com recomendações e calendário sugerido.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `week_data` | `Dict` | Dicionário com chaves `week`, `content`, `seo`, `email`, `meta_geral` |

**Retorno:** `str` — Relatório completo em Markdown.

---

### `export_report(report: str, output_path: Optional[str], fmt: str) -> str`

Exporta o relatório para um arquivo no disco. Cria o diretório de saída se não existir.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `report` | `str` | Conteúdo do relatório em Markdown |
| `output_path` | `Optional[str]` | Caminho de destino (usa padrão se `None`) |
| `fmt` | `str` | Formato de saída (atualmente ignorado, sempre escreve texto) |

**Retorno:** `str` — Caminho absoluto do arquivo salvo.

---

### `load_week_data(json_path: str) -> Dict`

Carrega os dados da semana de um arquivo JSON.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `json_path` | `str` | Caminho para o arquivo `.json` |

**Retorno:** `Dict` — Dados da semana deserializados.

## Constantes

| Constante | Tipo | Descrição |
|-----------|------|-----------|
| `BASE_DIR` | `str` | Diretório raiz do projeto (dois níveis acima do script) |
| `OUTPUT_DIR` | `str` | Diretório padrão de saída: `{BASE_DIR}/output/reports` |
| `BENCHMARKS` | `Dict` | Benchmarks de referência por plataforma (Instagram, LinkedIn, Email, Blog, YouTube) |
| `CONTENT_THEMES_BY_DAY` | `Dict` | Temas e formatos sugeridos por dia da semana (0=Segunda … 6=Domingo) |
