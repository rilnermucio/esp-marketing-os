# meta_ads_api.py — Meta Ads API

Integração com a API de Marketing do Meta (Facebook/Instagram Ads) v18.0.
Sem dependências externas — usa apenas `urllib` da biblioteca padrão Python.

## Autenticação

```bash
export META_ACCESS_TOKEN='EAAxxxxx...'
export META_AD_ACCOUNT_ID='act_123456789'
```

O token deve ter as permissões:
- `ads_read` — para leitura de campanhas e insights
- `ads_management` — para criar/pausar/reativar campanhas e anúncios

## Uso via CLI

```bash
# Listar campanhas
python meta_ads_api.py campaigns
python meta_ads_api.py campaigns --status ACTIVE --limit 10 --json

# Insights de uma campanha
python meta_ads_api.py campaign-insights 120200000123456
python meta_ads_api.py campaign-insights 120200000123456 --days 14

# Performance de anúncios da conta
python meta_ads_api.py ad-performance --days 7 --level ad
python meta_ads_api.py ad-performance --days 30 --level campaign --json

# Criar campanha (status inicial: PAUSED)
python meta_ads_api.py create-campaign "Campanha Leads Q1" LEADS 5000
python meta_ads_api.py create-campaign "Campanha Vendas" SALES 10000 --status ACTIVE

# Pausar anúncio
python meta_ads_api.py pause-ad 120200000987654

# Reativar anúncio
python meta_ads_api.py resume-ad 120200000987654

# Usar conta específica (sobrescreve variável de ambiente)
python meta_ads_api.py --account act_999888777 campaigns
```

## Exceções

### `MetaAdsError`
Erro genérico da API. Contém `.code` e `.subcode`.

### `MetaAdsAuthError`
Subclasse de `MetaAdsError`. Levantada para códigos de erro 190, 102, 104 (token), 200, 10 (permissões).

---

## Funções

### `get_campaigns(ad_account_id, token, status, limit) -> List[Dict]`

Retorna campanhas da conta de anúncios.

**Parâmetros:**
| Nome | Tipo | Padrão | Descrição |
|------|------|--------|-----------|
| `ad_account_id` | `str` | — | ID da conta (ex: `act_123456789`) |
| `token` | `str` | — | Access token |
| `status` | `str \| None` | `None` | Filtrar por: `ACTIVE`, `PAUSED`, `DELETED`, `ARCHIVED` |
| `limit` | `int` | `25` | Número máximo de campanhas (1–100) |

**Retorna:** Lista com campos `id`, `name`, `status`, `objective`, `daily_budget`, `lifetime_budget`, `start_time`, `stop_time`, `created_time`.

---

### `get_campaign_insights(campaign_id, token, days, metrics) -> Dict`

Retorna insights de uma campanha para o período especificado.

**Parâmetros:**
| Nome | Tipo | Padrão | Descrição |
|------|------|--------|-----------|
| `campaign_id` | `str` | — | ID da campanha |
| `days` | `int` | `30` | Período de análise em dias |
| `metrics` | `list[str] \| None` | Métricas principais | Lista de métricas |

**Métricas padrão:** `impressions`, `clicks`, `ctr`, `cpc`, `spend`, `reach`, `frequency`

**Retorna:**
```python
{
    "campaign_id": "120200000123456",
    "periodo": "2026-01-18 a 2026-02-17",
    "dados": {"impressions": "15000", "clicks": "450", "ctr": "3.0", "spend": "125.50", ...}
}
```

---

### `get_ad_performance(ad_account_id, token, days, level) -> List[Dict]`

Retorna performance de anúncios/conjuntos/campanhas da conta.

**Parâmetros:**
| Nome | Tipo | Padrão | Descrição |
|------|------|--------|-----------|
| `days` | `int` | `7` | Período de análise |
| `level` | `str` | `"ad"` | Nível: `"ad"`, `"adset"`, `"campaign"`, `"account"` |

**Retorna:** Lista com `campaign_name`, `adset_name`, `ad_name`, `impressions`, `clicks`, `ctr`, `cpc`, `cpm`, `spend`, `reach`, `frequency`, `actions`, `cost_per_action_type`.

---

### `create_campaign(ad_account_id, token, name, objective, daily_budget, status) -> Dict`

Cria uma nova campanha de anúncios.

**Parâmetros:**
| Nome | Tipo | Padrão | Descrição |
|------|------|--------|-----------|
| `name` | `str` | — | Nome da campanha |
| `objective` | `str` | — | Objetivo (ver lista abaixo) |
| `daily_budget` | `float` | — | Orçamento diário em **centavos** (5000 = R$50,00) |
| `status` | `str` | `"PAUSED"` | Status inicial: `"ACTIVE"` ou `"PAUSED"` |

**Objetivos válidos (`OBJETIVOS_CAMPANHA`):**

| Valor | Descrição |
|-------|-----------|
| `AWARENESS` | Reconhecimento de marca |
| `TRAFFIC` | Tráfego |
| `ENGAGEMENT` | Engajamento |
| `LEADS` | Geração de leads |
| `APP_PROMOTION` | Promoção de app |
| `SALES` | Vendas |
| `OUTCOME_AWARENESS` | Reconhecimento (novo) |
| `OUTCOME_TRAFFIC` | Tráfego (novo) |
| `OUTCOME_ENGAGEMENT` | Engajamento (novo) |
| `OUTCOME_LEADS` | Leads (novo) |
| `OUTCOME_APP_PROMOTION` | App (novo) |
| `OUTCOME_SALES` | Vendas (novo) |

**Retorna:** `{"id": "...", "name": "...", "objective": "...", "daily_budget": ..., "status": "..."}`

**Levanta:** `MetaAdsError` se o ID não for retornado.

---

### `pause_ad(ad_id, token) -> Dict`

Pausa um anúncio ativo.

**Retorna:** `{"id": "...", "status": "PAUSED", "success": True}`

---

### `resume_ad(ad_id, token) -> Dict`

Reativa um anúncio pausado.

**Retorna:** `{"id": "...", "status": "ACTIVE", "success": True}`

---

### `get_token() -> str`

Lê o token de `META_ACCESS_TOKEN`. Encerra com código 1 se não definido.

---

### `get_ad_account_id(cli_value) -> str`

Retorna o ID da conta de anúncios do argumento CLI ou de `META_AD_ACCOUNT_ID`.
Adiciona automaticamente o prefixo `act_` se ausente.

---

## Constantes

| Constante | Valor |
|-----------|-------|
| `GRAPH_API_BASE` | `https://graph.facebook.com/v18.0` |
| `ENV_TOKEN` | `"META_ACCESS_TOKEN"` |
| `ENV_AD_ACCOUNT` | `"META_AD_ACCOUNT_ID"` |
| `STATUS_VALIDOS` | `{"ACTIVE", "PAUSED", "DELETED", "ARCHIVED"}` |
