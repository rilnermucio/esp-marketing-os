# gsc_analyzer.py — Google Search Console Analyzer

Integração com a API do Google Search Console para análise de performance SEO.
Autenticação via **Service Account** — sem dependências externas além de `cryptography` para assinar o JWT.

## Instalação

```bash
pip install cryptography
```

## Autenticação

### Opção 1 — Arquivo de credenciais

```bash
export GSC_CREDENTIALS_FILE='/caminho/para/service-account.json'
```

### Opção 2 — JSON inline

```bash
export GSC_SERVICE_ACCOUNT_JSON='{"type":"service_account","project_id":...}'
```

O arquivo de credenciais deve ser um **Service Account** do Google Cloud com a API do Search Console ativada e o site verificado no GSC.

## Uso via CLI

```bash
# Principais queries de busca
python gsc_analyzer.py queries https://example.com
python gsc_analyzer.py queries https://example.com --days 60 --limit 200 --json

# Páginas com melhor performance
python gsc_analyzer.py top-pages https://example.com --days 30 --limit 50

# Oportunidades de CTR (impressões altas, CTR baixo)
python gsc_analyzer.py ctr-opportunities https://example.com
python gsc_analyzer.py ctr-opportunities https://example.com --min-impressions 200 --max-ctr 2.0

# Variações de posição entre dois períodos
python gsc_analyzer.py position-changes https://example.com --days 30 --compare 30

# Relatório completo (salvo em JSON)
python gsc_analyzer.py full-report https://example.com --days 30 --output relatorio.json
```

**Nota:** O GSC tem delay de ~3 dias nos dados. O período é calculado automaticamente com esse offset.

## Exceções

### `GSCError`
Erro genérico da API. Contém `.status` (HTTP status code).

### `GSCAuthError`
Subclasse de `GSCError`. Levantada para erros de autenticação (HTTP 401) ou credenciais inválidas.

---

## Funções

### `get_search_queries(site_url, token, days, limit) -> List[Dict]`

Retorna as principais queries de busca orgânica ordenadas por cliques.

**Parâmetros:**
| Nome | Tipo | Padrão | Descrição |
|------|------|--------|-----------|
| `site_url` | `str` | — | URL do site (`https://example.com` ou `sc-domain:example.com`) |
| `token` | `str` | — | Access token OAuth 2.0 |
| `days` | `int` | `30` | Dias retroativos |
| `limit` | `int` | `100` | Número máximo de queries |

**Retorna:** Lista de dicionários com:
```python
{
    "query": "marketing digital",
    "clicks": 100,
    "impressions": 1000,
    "ctr": 10.0,       # em percentual (%)
    "position": 8.5,
}
```

---

### `get_top_pages(site_url, token, days, limit) -> List[Dict]`

Retorna as páginas com melhor performance orgânica.

**Retorna:** Lista com campos `page`, `clicks`, `impressions`, `ctr`, `position`.

---

### `get_ctr_opportunities(site_url, token, days, min_impressions, max_ctr, max_position) -> List[Dict]`

Identifica queries com alto volume de impressões mas CTR abaixo do limiar — oportunidades de otimização.

**Parâmetros:**
| Nome | Tipo | Padrão | Descrição |
|------|------|--------|-----------|
| `min_impressions` | `int` | `100` | Mínimo de impressões para considerar |
| `max_ctr` | `float` | `3.0` | CTR máximo (%) para classificar como oportunidade |
| `max_position` | `float` | `20.0` | Posição máxima para considerar |

**Retorna:** Lista ordenada por impressões (maior primeiro), com campo adicional `ctr_potencial` (estimativa de cliques com CTR de 5%).

---

### `get_position_changes(site_url, token, days, compare_days, limit) -> Dict`

Compara posições médias entre dois períodos para identificar variações.

**Retorna:**
```python
{
    "periodo_atual": "últimos 30 dias",
    "periodo_anterior": "30-60 dias atrás",
    "subiram": [{"query": "...", "position_atual": 3.0, "position_anterior": 10.0, "variacao": 7.0}],
    "desceram": [...],
    "novos": [{"query": "...", "position": 8.5}],
    "resumo": {"total_subiram": 5, "total_desceram": 3, "total_novos": 12},
}
```

---

### `get_credentials_and_token() -> str`

Carrega credenciais (`_load_credentials()`) e retorna um access token OAuth 2.0 válido.

**Levanta:** `GSCAuthError` se as credenciais não estiverem configuradas ou forem inválidas.

---

### `_load_credentials() -> Dict`

Carrega credenciais da variável de ambiente `GSC_SERVICE_ACCOUNT_JSON` (JSON inline) ou `GSC_CREDENTIALS_FILE` (caminho para arquivo).

---

### `_get_access_token(credentials) -> str`

Gera e troca um JWT RS256 por um access token OAuth 2.0 da Google.
**Requer** a biblioteca `cryptography` instalada.

---

## Constantes

| Constante | Valor |
|-----------|-------|
| `GSC_API_BASE` | `https://searchconsole.googleapis.com/webmasters/v3` |
| `ENV_CREDENTIALS_FILE` | `"GSC_CREDENTIALS_FILE"` |
| `ENV_CREDENTIALS_JSON` | `"GSC_SERVICE_ACCOUNT_JSON"` |
| `MAX_ROWS` | `25000` |
| `DEFAULT_ROWS` | `1000` |
| `DIMENSOES_VALIDAS` | `{"query", "page", "country", "device", "searchAppearance", "date"}` |
