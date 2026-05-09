# Apify Integration (opcional)

Scraping estruturado de SERP do Google, Instagram, TikTok, YouTube e Meta Ad Library via [Apify Actors](https://apify.com/store), consumido pelos agents `mos-seo`, `mos-research`, `mos-ads` e `mos-video`. **Totalmente opt-in** — sem token configurado, o plugin se comporta exatamente como antes.

## Por que existe

Casos onde `WebSearch`/`WebFetch` não bastam:

- **SERP estruturado pra SEO**: top 10 com snippets, People Also Ask e related searches em JSON.
- **Concorrente externo no Instagram, TikTok e YouTube**: posts/vídeos + métricas agregadas + top hashtags de perfil público sem precisar de login.
- **Anúncios ATIVOS de concorrente (Meta Ad Library)**: criativo, copy, plataformas, datas. Único jeito programático de ver criativos rotando agora — alternativa é screenshot manual.

Pra qualquer outra coisa (pesquisa rasa, fact-check, conteúdo em página única), `WebSearch` continua sendo o caminho — mais rápido, sem custo e sem dependência externa.

## Setup (3 passos)

1. **Crie conta no Apify**: https://console.apify.com/sign-up (free tier dá ~$5 USD de crédito mensal — cobre semanas de teste leve).
2. **Pegue o token**: Settings → Integrations → API token → copiar.
3. **Exporte no shell** (ou no `~/.zshrc` / `.env` local):
   ```bash
   export APIFY_TOKEN="apify_api_xxx..."
   ```

Pronto. Rode um `--dry-run` em qualquer script pra confirmar setup:

```bash
python scripts/apify_serp.py --query "infoproduto bofu" --dry-run
python scripts/apify_instagram.py --handle @concorrente --dry-run
python scripts/apify_meta_ads.py --query "hotmart" --dry-run
python scripts/apify_tiktok.py --handle @concorrente --dry-run
python scripts/apify_youtube.py --channel @mrbeast --dry-run
```

## Uso direto

```bash
# SERP do Google (default 10 resultados, BR + pt-BR)
python scripts/apify_serp.py --query "infoproduto bofu"

# Instagram profile (default 30 posts)
python scripts/apify_instagram.py --handle @concorrente

# Meta Ad Library — anúncios ATIVOS por keyword/marca
python scripts/apify_meta_ads.py --query "hotmart" --country BR --max-ads 30

# TikTok profile (default 30 vídeos)
python scripts/apify_tiktok.py --handle @usuario

# YouTube channel (default 20 vídeos)
python scripts/apify_youtube.py --channel @mrbeast

# Via CLI unificado (mos.py)
python scripts/mos.py apify serp "infoproduto bofu" --max-results 10
python scripts/mos.py apify instagram @concorrente --max-posts 30
python scripts/mos.py apify meta-ads --query "hotmart" --country BR
python scripts/mos.py apify tiktok --handle @concorrente
python scripts/mos.py apify youtube --channel @mrbeast
```

Output (idêntico em todos os scripts):
- **stdout**: Markdown summary (consumível direto pelos agents)
- **arquivo**: JSON completo em `workspace/research/apify/<timestamp>-<slug>.json` (gitignored)
- **stderr**: caminho do arquivo salvo + mensagens de erro

## Custo estimado

Baseado em pricing público dos Actors em maio/2026. **Heurística** — preço real pode variar.

| Operação | Default | Custo aproximado |
|---|---|---|
| SERP (1 query, 10 resultados) | 10 | $0.050 |
| SERP (cap) | 100 | $0.500 |
| Instagram (30 posts) | 30 | $0.069 |
| Instagram (cap) | 100 | $0.230 |
| Meta Ad Library (30 ads) | 30 | $0.045 |
| Meta Ad Library (cap) | 100 | $0.150 |
| TikTok (30 vídeos) | 30 | $0.060 |
| TikTok (cap) | 100 | $0.200 |
| YouTube (20 vídeos) | 20 | $0.100 |
| YouTube (cap) | 100 | $0.500 |

**Hard caps por script** evitam engano de digitar 10000. Sempre rode `--dry-run` antes de execuções com `--max-*` alto.

## Como os agents usam

### `mos-seo`
SERP enriquecido pra keyword research, intent matching, content gap. Invoca `apify_serp.py` se `APIFY_TOKEN` existe.

### `mos-research`
Análise competitiva profunda em qualquer plataforma. Pode invocar **todos** os scripts conforme briefing — Instagram/TikTok/YouTube pra perfil de concorrente, Meta Ad Library pra ver criativos ativos, SERP pra contexto. O Research Brief consolida.

### `mos-ads`
Inteligência competitiva de criativo via Meta Ad Library: copy, CTA, plataforma, duração de campanha. Bate em `/criar-anuncio` e `/clonar-estrategia`.

### `mos-video`
Reverse-engineer de top creators no YouTube e TikTok pra extrair patterns de hooks, retenção, formato. Encaixa em `/analisar-video` e `/criar-video`.

## Graceful degrade

Sem `APIFY_TOKEN`, os scripts saem com **exit 0** e mensagem em stderr. Os agents capturam isso e seguem com WebSearch. Não há erro, não há crash — só ausência da ferramenta opcional.

Erros reais (401 invalid token, 429 rate limit, timeout) saem com **exit 2** e mensagem clara em stderr. O agent decide retry, fallback ou alertar o usuário.

## FAQ

**O token Apify fica exposto no plugin?**
Não. Cada usuário define o seu `APIFY_TOKEN` localmente. O plugin nunca embute credencial. Outputs vão pra `workspace/` que é gitignored.

**Funciona offline / sem internet?**
Não. Os Actors rodam na nuvem do Apify.

**Por que não usar a API do TikTok/YouTube direto?**
- TikTok não tem API pública pra perfis de terceiros
- YouTube tem API mas com quota agressiva e exige projeto Google Cloud
- Meta Ad Library tem API mas exige autenticação por desenvolvedor approved

Apify centraliza tudo num único token, sem setup por plataforma.

**Twitter/X?**
Não incluímos. Os Actors disponíveis no Apify ou exigem rental mensal (~$25/mês fixos), ou cobram por compute time mesmo retornando demo data — perda de crédito sem retorno. Pra tweets pontuais, use `WebSearch` (Google indexa X). Se Twitter virar prioridade, dá pra adicionar editando `apify_client.py` + criando novo `apify_twitter.py`.

**LinkedIn?**
Não incluímos no plugin. Apify oferece scrapers, mas viola ToS do LinkedIn agressivamente — risco de banimento + ação legal. Pular.

**Como vejo o que foi salvo até agora?**
```bash
ls -lah workspace/research/apify/
```

**Como deleto resultados antigos?**
```bash
# Remove tudo mais antigo que 30 dias
find workspace/research/apify/ -name "*.json" -mtime +30 -delete
```

**Quero usar um Actor diferente do que vem no plugin**
Os Actor IDs são constantes no topo de cada script (`SERP_ACTOR_ID`, `INSTAGRAM_ACTOR_ID`, etc.). Edite e adicione entrada em `_COST_RATES` em `apify_client.py` se quiser custo estimado.

## Opt-out completo

Se decidir desinstalar:

1. Remova `APIFY_TOKEN` do shell.
2. Opcional: delete `workspace/research/apify/` (são só JSONs locais, gitignored).
3. Os scripts Python ficam, mas inertes — agents voltam ao comportamento original (WebSearch).

Não há banco de dados, não há config persistente, não há lock-in.

## Arquitetura

```
scripts/
├── apify_client.py        # auth + run-sync + erro + custo (sem CLI próprio)
├── apify_serp.py          # apify/google-search-scraper + CLI
├── apify_instagram.py     # apify/instagram-scraper + CLI
├── apify_meta_ads.py      # curious_coder/facebook-ads-library-scraper + CLI
├── apify_tiktok.py        # clockworks/free-tiktok-scraper + CLI (FREE)
└── apify_youtube.py       # streamers/youtube-scraper + CLI

scripts/tests/
├── test_apify_client.py     # 31 tests
├── test_apify_serp.py       # 25 tests
├── test_apify_instagram.py  # 29 tests
├── test_apify_meta_ads.py   # 24 tests
├── test_apify_tiktok.py     # 25 tests
└── test_apify_youtube.py    # 23 tests
```

`apify_client.py` usa `urllib.request` da stdlib — zero dependência nova. Mock dos testes via `monkeypatch.setattr` (consistente com `test_notion_api.py`, `test_meta_ads_api.py`).

## Mapeamento Actor → script → agent

| Actor | Script | Agent principal | Use case |
|---|---|---|---|
| `apify/google-search-scraper` | `apify_serp.py` | `mos-seo` | SERP pra keyword research / SEO |
| `apify/instagram-scraper` | `apify_instagram.py` | `mos-research` | Top posts de concorrente IG |
| `curious_coder/facebook-ads-library-scraper` | `apify_meta_ads.py` | `mos-ads` | Anúncios ativos por keyword/marca |
| `clockworks/free-tiktok-scraper` | `apify_tiktok.py` | `mos-research`, `mos-video` | Top vídeos de TikTok (Actor FREE) |
| `streamers/youtube-scraper` | `apify_youtube.py` | `mos-video`, `mos-research` | Vídeos de canal YouTube com métricas |

## Notas sobre Actors específicos

- **Meta Ad Library** (`curious_coder/facebook-ads-library-scraper`): exige `count >= 10` no input. O script eleva valores menores automaticamente (pra evitar HTTP 400). Bodies de creative dinâmico vêm com placeholders `{{product.brand}}` — preservados como vêm.
- **TikTok** (`clockworks/free-tiktok-scraper`): Actor FREE, sem custo via API (cobertura igual ao paid em volume baixo). Para profiles privados ou com 0 vídeos, retorna apenas metadados (`note: "Profile has no videos..."`).
