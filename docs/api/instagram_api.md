# instagram_api.py — Meta Graph API (Instagram Business)

Integração com a Meta Graph API v18.0 para gerenciar contas Instagram Business.
Sem dependências externas — usa apenas a biblioteca padrão Python (`urllib`).

## Autenticação

Defina a variável de ambiente antes de usar:

```bash
export INSTAGRAM_ACCESS_TOKEN='EAAxxxxx...'
```

O token deve ser um **Long-Lived Access Token** com as permissões:
- `instagram_basic`
- `instagram_content_publish`
- `instagram_manage_insights`
- `pages_read_engagement`

## Uso via CLI

```bash
# Insights da conta
python instagram_api.py insights <account_id>
python instagram_api.py insights <account_id> --period week --since 2026-01-01 --until 2026-01-31

# Informações da conta
python instagram_api.py account <account_id>

# Dados demográficos da audiência
python instagram_api.py audience <account_id>

# Posts recentes
python instagram_api.py posts <account_id>
python instagram_api.py posts <account_id> --limit 25

# Publicar foto
python instagram_api.py publish-photo <account_id> <image_url> "<caption>"

# Publicar carrossel (2-10 imagens)
python instagram_api.py publish-carousel <account_id> "<caption>" <url1> <url2> [url3...]
```

## Exceções

### `InstagramAPIError`
Erro genérico retornado pela API. Contém `.code` (int) e `.subcode` (int opcional).

### `InstagramAuthError`
Subclasse de `InstagramAPIError`. Levantada quando o token é inválido (códigos 190, 102, 104).

---

## Funções

### `get_account_insights(account_id, token, metrics, period, since, until) -> Dict`

Retorna insights da conta Instagram Business.

**Parâmetros:**
| Nome | Tipo | Padrão | Descrição |
|------|------|--------|-----------|
| `account_id` | `str` | — | ID da conta Instagram Business |
| `token` | `str` | — | Long-Lived Access Token |
| `metrics` | `list[str] \| None` | `METRICAS_CONTA` | Lista de métricas |
| `period` | `str` | `"day"` | Granularidade: `day`, `week`, `days_28`, `month`, `lifetime` |
| `since` | `str \| None` | `None` | Data de início (YYYY-MM-DD ou Unix timestamp) |
| `until` | `str \| None` | `None` | Data de fim |

**Métricas disponíveis (`METRICAS_CONTA`):**
`impressions`, `reach`, `profile_views`, `website_clicks`, `follower_count`

```python
from instagram_api import get_account_insights

insights = get_account_insights(
    account_id="17841400008460056",
    token=os.environ["INSTAGRAM_ACCESS_TOKEN"],
    period="week",
)
```

---

### `get_insights(media_id, token, metrics) -> Dict`

Retorna insights de um post/mídia específico.

**Parâmetros:**
| Nome | Tipo | Padrão | Descrição |
|------|------|--------|-----------|
| `media_id` | `str` | — | ID do post ou mídia |
| `token` | `str` | — | Access token |
| `metrics` | `list[str] \| None` | `METRICAS_POST` | Lista de métricas |

**Métricas disponíveis (`METRICAS_POST`):**
`impressions`, `reach`, `engagement`, `saved`, `video_views`, `likes`, `comments`, `shares`

---

### `get_audience_demographics(account_id, token) -> Dict`

Retorna dados demográficos da audiência (faixa etária, gênero, cidade, país, locale).
Usa período `lifetime` automaticamente.

---

### `get_recent_posts(account_id, token, limit) -> Dict`

Retorna posts recentes da conta com campos:
`id`, `caption`, `media_type`, `media_url`, `thumbnail_url`, `timestamp`, `like_count`, `comments_count`, `permalink`

**Parâmetros:**
| Nome | Tipo | Padrão | Descrição |
|------|------|--------|-----------|
| `limit` | `int` | `10` | Número de posts (1–100) |

---

### `publish_photo(account_id, token, image_url, caption) -> Dict`

Publica uma foto no Instagram Business (fluxo de 2 etapas: container → publish).

**Parâmetros:**
| Nome | Tipo | Descrição |
|------|------|-----------|
| `image_url` | `str` | URL pública HTTPS da imagem (JPEG/PNG) |
| `caption` | `str` | Legenda do post (máx. 2200 caracteres) |

**Retorna:** `{"id": "...", "creation_id": "..."}`

**Levanta:** `InstagramAPIError` se o container não for criado.

```python
result = publish_photo(
    account_id="17841400008460056",
    token=token,
    image_url="https://example.com/imagem.jpg",
    caption="Meu post de marketing digital",
)
print(f"Post publicado: {result['id']}")
```

---

### `publish_carousel(account_id, token, caption, image_urls) -> Dict`

Publica um carrossel com 2–10 imagens (fluxo de 3 etapas).

**Parâmetros:**
| Nome | Tipo | Descrição |
|------|------|-----------|
| `caption` | `str` | Legenda do carrossel |
| `image_urls` | `list[str]` | Lista de URLs (2–10 imagens) |

**Retorna:** `{"id": "...", "creation_id": "...", "children_ids": [...]}`

**Levanta:** `ValidationError` se `len(image_urls) < 2` ou `> 10`.

---

### `get_token() -> str`

Lê o token de `INSTAGRAM_ACCESS_TOKEN`. Encerra com código 1 se não definido.

---

## Constantes

| Constante | Descrição |
|-----------|-----------|
| `GRAPH_API_BASE` | `https://graph.facebook.com/v18.0` |
| `ENV_TOKEN` | `"INSTAGRAM_ACCESS_TOKEN"` |
| `METRICAS_POST` | Lista de 8 métricas de post |
| `METRICAS_CONTA` | Lista de 5 métricas de conta |
| `PERIODOS_VALIDOS` | `{"day", "week", "days_28", "month", "lifetime"}` |
