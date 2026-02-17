# API Reference — Marketing OS Scripts

Documentação de referência para todos os scripts Python do Marketing OS.

## Índice

### Geração de Conteúdo
- [hook_generator.py](./hook_generator.md) — Hooks virais para vídeos e posts
- [hook_variant_generator.py](./hook_variant_generator.md) — Variantes A/B de hooks
- [reels_script_generator.py](./reels_script_generator.md) — Roteiros completos para Reels
- [carousel_structure_generator.py](./carousel_structure_generator.md) — Estrutura de carrosséis
- [caption_generator.py](./caption_generator.md) — Legendas otimizadas
- [content_idea_generator.py](./content_idea_generator.md) — Ideias de conteúdo por nicho
- [content_repurposer.py](./content_repurposer.md) — Reutilização entre plataformas
- [ab_generator.py](./ab_generator.md) — Variações A/B de copy

### Análise e SEO
- [seo_analyzer.py](./seo_analyzer.md) — Análise SEO de conteúdo Markdown
- [headline_scorer.py](./headline_scorer.md) — Pontuação de headlines
- [readability_checker.py](./readability_checker.md) — Análise de legibilidade
- [content_audit.py](./content_audit.md) — Auditoria de conteúdo existente

### Planejamento
- [content_calendar.py](./content_calendar.md) — Calendário editorial
- [hashtag_generator.py](./hashtag_generator.md) — Geração de hashtags
- [instagram_hashtag_research.py](./instagram_hashtag_research.md) — Pesquisa de hashtags Instagram

### Tendências e Pesquisa
- [trend_tracker.py](./trend_tracker.md) — Rastreamento de tendências
- [trend_adapter.py](./trend_adapter.md) — Adaptação de trends ao nicho
- [tiktok_trends_scraper.py](./tiktok_trends_scraper.md) — Análise de trends TikTok
- [competitor_analyzer.py](./competitor_analyzer.md) — Análise competitiva

### Relatórios
- [weekly_report.py](./weekly_report.md) — Relatório semanal automático

### Integrações de API
- [instagram_api.py](./instagram_api.md) — Meta Graph API (Instagram Business)
- [gsc_analyzer.py](./gsc_analyzer.md) — Google Search Console
- [meta_ads_api.py](./meta_ads_api.md) — Meta Ads API (Facebook/Instagram Ads)

### Utilitários
- [validators.py](./validators.md) — Módulo de validação centralizado
- [mos.py](./mos.md) — CLI unificado do Marketing OS

---

## Convenções

### Variáveis de Ambiente

| Variável | Script | Descrição |
|----------|--------|-----------|
| `INSTAGRAM_ACCESS_TOKEN` | instagram_api.py | Token de acesso Meta Graph API |
| `GSC_CREDENTIALS_FILE` | gsc_analyzer.py | Caminho para service-account.json do GSC |
| `GSC_SERVICE_ACCOUNT_JSON` | gsc_analyzer.py | JSON inline das credenciais GSC |
| `META_ACCESS_TOKEN` | meta_ads_api.py | Token de acesso Meta Ads API |
| `META_AD_ACCOUNT_ID` | meta_ads_api.py | ID da conta de anúncios (act_XXXXXXXXX) |

### Formato de Output

Todos os scripts suportam dois modos de saída:
- **Humano** (padrão): tabelas e texto formatado
- **JSON** (`--json` ou `--format json`): saída estruturada para integração

### Códigos de Saída

| Código | Significado |
|--------|------------|
| `0` | Sucesso |
| `1` | Erro de validação ou de API |

---

*Marketing OS v4.0 — Última atualização: 2026-02-17*
