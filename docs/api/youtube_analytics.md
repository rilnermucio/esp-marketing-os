# youtube_analytics.py — YouTube Analytics API

Integração com YouTube Analytics API v2 e YouTube Data API v3 para análise de performance de canal. Autentica via Service Account (JWT), reutilizando as credenciais do Google Search Console quando disponíveis.

## Autenticação

```bash
# Opção 1: arquivo de Service Account dedicado para YouTube
export YT_CREDENTIALS_FILE=/caminho/para/service-account.json

# Opção 2: JSON inline
export YT_SERVICE_ACCOUNT_JSON='{"type":"service_account",...}'

# Opção 3: reutilizar credenciais do GSC (fallback automático)
export GSC_CREDENTIALS_FILE=/caminho/para/service-account.json
```

## Uso via CLI

```bash
# Estatísticas gerais do canal (últimos 30 dias)
python youtube_analytics.py channel

# Período customizado
python youtube_analytics.py channel --days 90

# Lista de vídeos com métricas
python youtube_analytics.py videos --days 30 --limit 20

# Top vídeos por views
python youtube_analytics.py top-videos --days 30 --limit 10

# Dados demográficos da audiência
python youtube_analytics.py demographics --days 30

# Fontes de tráfego
python youtube_analytics.py traffic-sources --days 30

# Relatório completo (todos os dados consolidados)
python youtube_analytics.py full-report --days 30

# Salvar relatório em arquivo JSON
python youtube_analytics.py full-report --days 30 --output relatorio.json

# Output JSON (machine-readable)
python youtube_analytics.py channel --json
```

### Subcomandos

| Subcomando | Descrição |
|------------|-----------|
| `channel` | Métricas gerais do canal (views, watch time, inscritos, etc.) |
| `videos` | Lista de vídeos com títulos e métricas enriquecidas |
| `top-videos` | Top vídeos por views no período |
| `demographics` | Distribuição por faixa etária e gênero |
| `traffic-sources` | De onde os espectadores chegam ao canal |
| `full-report` | Relatório completo com todos os dados |

### Argumentos comuns

| Argumento | Curto | Padrão | Descrição |
|-----------|-------|--------|-----------|
| `--days` | `-d` | `30` | Dias retroativos a analisar (1–365) |
| `--limit` | `-l` | `10` / `20` | Máximo de itens retornados |
| `--output` | `-o` | — | Arquivo de saída JSON |
| `--json` | — | `False` | Saída em JSON puro (sem formatação humana) |

## Exceções

### `YouTubeAnalyticsError`

Erro base da integração com as APIs do YouTube.

| Atributo | Tipo | Descrição |
|----------|------|-----------|
| `message` | `str` | Mensagem de erro |
| `status` | `Optional[int]` | Código HTTP (quando disponível) |

`str()` formata como `[HTTP 403] Quota excedida` quando `status` está presente.

### `YouTubeAuthError`

Subclasse de `YouTubeAnalyticsError`. Levantada para erros de credenciais, token inválido ou expirado, e campos ausentes no arquivo de Service Account.

## Funções

### `get_channel_stats(token, days, channel_id) -> Dict`

Retorna métricas gerais do canal para o período especificado.

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `token` | `str` | — | Access token OAuth 2.0 |
| `days` | `int` | `30` | Dias retroativos |
| `channel_id` | `str` | `"MINE"` | ID do canal (`"MINE"` = canal autenticado) |

**Retorno:** `Dict` com as chaves:

| Chave | Tipo | Descrição |
|-------|------|-----------|
| `periodo` | `str` | Intervalo analisado (`"YYYY-MM-DD a YYYY-MM-DD"`) |
| `views` | `int` | Total de visualizações |
| `watch_time_minutos` | `float` | Minutos assistidos |
| `duracao_media_seg` | `float` | Duração média por view (segundos) |
| `likes` | `int` | Total de likes |
| `comments` | `int` | Total de comentários |
| `shares` | `int` | Total de compartilhamentos |
| `subscribers_gained` | `int` | Inscritos ganhos |
| `subscribers_lost` | `int` | Inscritos perdidos |
| `net_subscribers` | `int` | Saldo de inscritos (`gained - lost`) |

Se não houver dados, retorna `{"periodo": ..., "dados": None, "mensagem": ...}`.

---

### `get_top_videos(token, days, limit, channel_id) -> List[Dict]`

Retorna os vídeos com melhor performance por views no período.

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `token` | `str` | — | Access token |
| `days` | `int` | `30` | Dias retroativos |
| `limit` | `int` | `10` | Máximo de vídeos (1–200) |
| `channel_id` | `str` | `"MINE"` | ID do canal |

**Retorno:** `List[Dict]`, cada item com:

| Chave | Tipo | Descrição |
|-------|------|-----------|
| `video_id` | `str` | ID do vídeo |
| `views` | `int` | Visualizações |
| `watch_time_minutos` | `float` | Minutos assistidos |
| `likes` | `int` | Likes |
| `comments` | `int` | Comentários |
| `shares` | `int` | Compartilhamentos |

Lista ordenada por `views` (maior primeiro). Retorna `[]` se não houver dados.

---

### `get_video_list(token, days, limit, channel_id) -> List[Dict]`

Retorna lista de vídeos enriquecida com títulos (via YouTube Data API) e taxa de engajamento calculada.

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `token` | `str` | — | Access token |
| `days` | `int` | `30` | Dias retroativos |
| `limit` | `int` | `20` | Máximo de vídeos |
| `channel_id` | `str` | `"MINE"` | ID do canal |

**Retorno:** `List[Dict]`, cada item com:

| Chave | Tipo | Descrição |
|-------|------|-----------|
| `video_id` | `str` | ID do vídeo |
| `titulo` | `str` | Título do vídeo (da Data API) |
| `views` | `int` | Visualizações |
| `watch_time_minutos` | `float` | Minutos assistidos |
| `likes` | `int` | Likes |
| `comments` | `int` | Comentários |
| `shares` | `int` | Compartilhamentos |
| `engagement_rate` | `float` | `(likes+comments+shares)/views × 100` |

Faz até `⌈limit/50⌉` chamadas à Data API para buscar títulos em lotes de 50. Se o título não for encontrado, usa `"Video {video_id}"` como fallback.

---

### `get_demographics(token, days, channel_id) -> Dict`

Retorna distribuição demográfica da audiência por faixa etária e gênero.

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `token` | `str` | — | Access token |
| `days` | `int` | `30` | Dias retroativos |
| `channel_id` | `str` | `"MINE"` | ID do canal |

**Retorno:** `Dict` com:

| Chave | Tipo | Descrição |
|-------|------|-----------|
| `periodo` | `str` | Intervalo analisado |
| `por_faixa_etaria` | `Dict[str, float]` | `{faixa: percentual}` agregado por faixa |
| `por_genero` | `Dict[str, float]` | `{genero: percentual}` agregado por gênero |

Faixas disponíveis: `age13-17`, `age18-24`, `age25-34`, `age35-44`, `age45-54`, `age55-64`, `age65-`.
Gêneros: `male`, `female`.

---

### `get_traffic_sources(token, days, channel_id) -> List[Dict]`

Retorna as fontes de tráfego do canal ordenadas por views.

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `token` | `str` | — | Access token |
| `days` | `int` | `30` | Dias retroativos |
| `channel_id` | `str` | `"MINE"` | ID do canal |

**Retorno:** `List[Dict]`, cada item com:

| Chave | Tipo | Descrição |
|-------|------|-----------|
| `source` | `str` | Tipo de fonte (`YT_SEARCH`, `SUGGESTED_VIDEOS`, `EXTERNAL`, etc.) |
| `views` | `int` | Views originárias desta fonte |
| `watch_time_minutos` | `float` | Minutos assistidos via esta fonte |
| `percentual_views` | `float` | Participação percentual no total de views |

Retorna `[]` se não houver dados.

---

### `get_credentials_and_token(scope) -> str`

Carrega credenciais do ambiente e retorna access token OAuth 2.0.

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `scope` | `str` | `YT_ANALYTICS_SCOPE` | Escopo OAuth solicitado |

**Retorno:** `str` — access token pronto para uso nos cabeçalhos `Authorization: Bearer {token}`.

**Exceções:**
- `YouTubeAuthError` — se as credenciais não estiverem configuradas ou forem inválidas
- `YouTubeAuthError` — se a biblioteca `cryptography` não estiver instalada

---

## Funções internas

| Função | Descrição |
|--------|-----------|
| `_load_credentials() -> Dict` | Carrega credenciais de variáveis de ambiente (JSON inline ou arquivo) |
| `_get_access_token(credentials, scope) -> str` | Gera JWT e troca por access token OAuth via Service Account |
| `_api_get(url, token, params) -> Dict` | GET autenticado com tratamento de erros HTTP |
| `_date_range(days) -> Tuple[str, str]` | Calcula `(start_date, end_date)` com delay de 2 dias (compensação do YouTube) |
| `_get_channel_id(token) -> str` | Retorna ID do canal autenticado via YouTube Data API |

## Constantes

| Constante | Tipo | Valor / Descrição |
|-----------|------|-------------------|
| `YT_ANALYTICS_BASE` | `str` | `"https://youtubeanalytics.googleapis.com/v2"` |
| `YT_DATA_BASE` | `str` | `"https://www.googleapis.com/youtube/v3"` |
| `OAUTH_TOKEN_URL` | `str` | `"https://oauth2.googleapis.com/token"` |
| `ENV_CREDENTIALS_FILE` | `str` | `"YT_CREDENTIALS_FILE"` |
| `ENV_CREDENTIALS_JSON` | `str` | `"YT_SERVICE_ACCOUNT_JSON"` |
| `ENV_CREDENTIALS_FILE_FALLBACK` | `str` | `"GSC_CREDENTIALS_FILE"` |
| `ENV_CREDENTIALS_JSON_FALLBACK` | `str` | `"GSC_SERVICE_ACCOUNT_JSON"` |
| `YT_ANALYTICS_SCOPE` | `str` | `"https://www.googleapis.com/auth/yt-analytics.readonly"` |
| `YT_DATA_SCOPE` | `str` | `"https://www.googleapis.com/auth/youtube.readonly"` |
| `METRICAS_CANAL` | `List[str]` | 9 métricas de nível de canal |
| `METRICAS_VIDEO` | `List[str]` | 10 métricas de nível de vídeo |

## Dependências

- **Stdlib apenas** — usa `urllib`, `json`, `base64`, `time`, `os`, `sys`, `datetime`, `argparse`
- **`cryptography`** — para assinar o JWT do Service Account (`pip install cryptography`)
- **`output_formatter`** — módulo interno para formatação de saída
- **`validators`** — módulo interno para validação de argumentos CLI
