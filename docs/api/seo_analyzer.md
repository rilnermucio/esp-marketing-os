# seo_analyzer.py — Analisador de conteúdo para otimização SEO

O `seo_analyzer.py` analisa arquivos de texto ou Markdown e gera um relatório de otimização SEO com métricas de legibilidade, estrutura de headings, links, densidade de keyword e score geral de 0 a 100. O resultado é exibido no terminal e também impresso como JSON para integração com outros scripts.

## Uso via CLI

```bash
# Analisar arquivo sem keyword específica
python scripts/seo_analyzer.py artigo.md

# Analisar com keyword principal
python scripts/seo_analyzer.py artigo.md "marketing digital"

# Analisar arquivo .txt
python scripts/seo_analyzer.py conteudo.txt "produtividade"
```

## Argumentos

| Argumento | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `arquivo` | `str` (posicional) | Sim | — | Caminho para o arquivo `.md` ou `.txt` a analisar |
| `keyword` | `str` (posicional) | Não | `None` | Keyword principal a analisar (máx. 100 caracteres) |

## Funções

### `analyze_content(content: str, keyword: Optional[str]) -> Dict`

Analisa o conteúdo textual e retorna um dicionário completo com métricas, estrutura, análise de keyword, recomendações e score SEO. Internamente chama `calculate_seo_score()`.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `content` | `str` | Texto completo do conteúdo a analisar |
| `keyword` | `Optional[str]` | Keyword principal (pode ser `None`) |

**Retorno:** `Dict` com chaves:

| Chave | Tipo | Descrição |
|-------|------|-----------|
| `metrics` | `Dict` | Métricas de conteúdo (ver tabela abaixo) |
| `structure` | `Dict` | Estrutura de headings e links |
| `keyword_analysis` | `Optional[Dict]` | Análise de keyword (ou `None` se não informada) |
| `recommendations` | `List[str]` | Lista de recomendações textuais |
| `seo_score` | `int` | Score SEO de 0 a 100 |

**Estrutura de `metrics`:**

| Chave | Tipo | Descrição |
|-------|------|-----------|
| `word_count` | `int` | Total de palavras |
| `sentence_count` | `int` | Total de sentenças |
| `paragraph_count` | `int` | Total de parágrafos |
| `avg_sentence_length` | `float` | Média de palavras por sentença |
| `avg_word_length` | `float` | Média de caracteres por palavra |
| `readability_score` | `float` | Score de legibilidade simplificado (0–100) |

**Estrutura de `structure`:**

| Chave | Tipo | Descrição |
|-------|------|-----------|
| `headers` | `Dict[str, int]` | Contagem de H1, H2 e H3 |
| `internal_links` | `int` | Links internos (padrão `[texto](/caminho)`) |
| `external_links` | `int` | Links externos (padrão `[texto](https://...)`) |

**Estrutura de `keyword_analysis`:**

| Chave | Tipo | Descrição |
|-------|------|-----------|
| `keyword` | `str` | Keyword informada |
| `count` | `int` | Número de ocorrências |
| `density` | `float` | Densidade percentual (%) |
| `in_first_100_words` | `bool` | Se a keyword aparece nas primeiras 100 palavras |
| `in_h1` | `bool` | Se a keyword aparece em algum H1 |
| `in_h2` | `bool` | Se a keyword aparece em algum H2 |
| `ideal_density_range` | `str` | Faixa ideal (`"1-2%"`) |
| `status` | `str` | `"good"` se density 1–2%, `"adjust"` caso contrário |

---

### `calculate_seo_score(word_count, headers, keyword_analysis, external_links) -> int`

Calcula o score SEO de 0 a 100 distribuindo pontos entre quatro critérios: volume de palavras (até 30 pts), estrutura de headings (até 20 pts), análise de keyword (até 30 pts) e links externos (até 20 pts).

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `word_count` | `int` | Total de palavras do conteúdo |
| `headers` | `Dict[str, int]` | Contagem de headings por nível |
| `keyword_analysis` | `Optional[Dict]` | Resultado da análise de keyword (pode ser `None`) |
| `external_links` | `int` | Número de links externos encontrados |

**Retorno:** `int` — Score SEO de 0 a 100.

**Critérios de pontuação:**

| Critério | Pontos máximos | Regra |
|----------|----------------|-------|
| Volume de palavras | 30 | 5 pts (<500), 15 pts (500–999), 25 pts (1000–1499), 30 pts (≥1500) |
| H1 único | 10 | 10 pts se exatamente 1 H1 |
| H2 suficiente | 10 | 10 pts se ≥ 2 H2s |
| Keyword no H1 | 10 | 10 pts se keyword em H1 |
| Keyword nas primeiras 100 palavras | 10 | 10 pts se presente |
| Densidade de keyword ideal | 10 | 10 pts se density 1–2% |
| Links externos | 20 | 10 pts (≥ 1 link), 20 pts (≥ 2 links) |

## Constantes

| Constante | Tipo | Descrição |
|-----------|------|-----------|
| `USO` | `str` | String de ajuda exibida quando o script é chamado sem argumentos |
