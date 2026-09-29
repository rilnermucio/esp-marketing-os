# STORY-016: Integração com Instagram Business API

**ID:** STORY-016
**Tipo:** Integration
**Prioridade:** P1
**Estimativa:** G (> 4 horas)
**Status:** Backlog
**Sprint:** A definir

---

## User Story

**Como** usuário do Marketing OS,
**Quero** conectar minhas contas do Instagram ao sistema,
**Para que** possa obter métricas reais de performance, publicar conteúdo diretamente e monitorar engajamento sem sair do sistema.

---

## Contexto

Atualmente o Marketing OS gera conteúdo mas não tem visibilidade sobre performance real. Os scripts de analytics trabalham com dados simulados ou inseridos manualmente. A integração com a Instagram Business API via Meta Graph API permitiria:

- Métricas reais (alcance, impressões, engajamento, saves, shares)
- Publicação de posts e carrosséis diretamente via script
- Análise de performance de conteúdo histórico
- Insights de audiência (demografia, horários de pico)

---

## Acceptance Criteria

```
[ ] Script `scripts/instagram_api.py` criado com funções:
    - get_insights(post_id, metrics) → dados de performance
    - get_account_insights(period) → métricas da conta
    - get_audience_demographics() → dados de audiência
    - publish_photo(image_url, caption) → publicação de foto
    - publish_carousel(images, caption) → publicação de carrossel
    - get_recent_posts(limit) → últimos posts com métricas

[ ] Autenticação via token de acesso configurável em .env:
    - INSTAGRAM_ACCESS_TOKEN
    - INSTAGRAM_ACCOUNT_ID

[ ] Testes criados em `scripts/tests/test_instagram_api.py`:
    - Mock das chamadas à API
    - Teste de todas as funções principais
    - Teste de tratamento de erros

[ ] Documentação em `references/instagram-api.md`:
    - Como obter o Access Token
    - Permissões necessárias no Facebook App
    - Exemplos de uso de cada função

[ ] Integração com analytics_agent.md:
    - Subagente pode solicitar dados via script
    - Exemplo de uso documentado no SKILL.md
```

---

## Dependências Técnicas

- Meta Developer App com permissões: `instagram_basic`, `instagram_content_publish`, `instagram_manage_insights`
- Conta do Instagram conectada à Página do Facebook
- Token de acesso de longa duração (60 dias, renovável)
- Python: `requests` (já disponível)

---

## Referências

- Meta Graph API: https://developers.facebook.com/docs/instagram-api
- Instagram Insights API: https://developers.facebook.com/docs/instagram-api/guides/insights
- Publicação via API: https://developers.facebook.com/docs/instagram-api/guides/content-publishing

---

## Notas de Implementação

- Usar OAuth 2.0 para autenticação
- Implementar refresh automático do token antes do vencimento
- Rate limit: 200 chamadas por hora por usuário
- Armazenar tokens em variáveis de ambiente (nunca no código)
- Adicionar ao `.env.example` as variáveis necessárias
