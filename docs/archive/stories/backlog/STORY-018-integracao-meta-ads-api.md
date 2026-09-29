# STORY-018: Integração com Meta Ads API

**ID:** STORY-018
**Tipo:** Integration
**Prioridade:** P2
**Estimativa:** G (> 4 horas)
**Status:** Backlog
**Sprint:** A definir

---

## User Story

**Como** usuário do Marketing OS que investe em anúncios pagos,
**Quero** gerenciar e analisar campanhas do Meta Ads diretamente no sistema,
**Para que** possa criar campanhas baseadas no copy gerado pelos agentes, monitorar ROAS e otimizar investimentos sem sair do Marketing OS.

---

## Contexto

O `ads-agent.md` hoje cria estratégia e copy para anúncios, mas não tem conexão com as plataformas reais. A integração com a Meta Marketing API permitiria fechar o loop entre geração de copy e execução real de campanhas.

---

## Acceptance Criteria

```
[ ] Script `scripts/meta_ads_api.py` criado com funções:
    - get_campaigns(account_id) → lista de campanhas + status
    - get_campaign_insights(campaign_id, date_range) → métricas
    - get_ad_performance(ad_id) → ROAS, CPC, CTR, conversões
    - create_campaign(name, objective, budget) → criar campanha
    - create_ad_set(campaign_id, audience, placement) → criar adset
    - create_ad(adset_id, creative, copy) → criar anúncio
    - pause_ad(ad_id) → pausar anúncio com baixa performance
    - get_audience_insights(targeting) → análise de audiência

[ ] Autenticação via Meta Business SDK:
    - META_ACCESS_TOKEN em variável de ambiente
    - META_AD_ACCOUNT_ID em variável de ambiente

[ ] Dashboard simples de performance:
    - ROAS por campanha
    - CPA por objetivo
    - CTR por criativo
    - Gasto vs. receita

[ ] Integração com ads-agent.md:
    - Agente pode solicitar dados de campanhas ativas
    - Agente pode criar rascunho de campanha a partir de copy

[ ] Testes em `scripts/tests/test_meta_ads_api.py`

[ ] Documentação em `references/meta-ads-api.md`
```

---

## Dependências Técnicas

- Meta Business App com permissões: `ads_management`, `ads_read`, `business_management`
- Conta de Anúncios do Meta (Ad Account)
- Python: `facebook-business` SDK (Meta oficial)

---

## Referências

- Meta Marketing API: https://developers.facebook.com/docs/marketing-apis
- Python SDK: https://github.com/facebook/facebook-python-business-sdk
