# STORY-017: Integração com Google Search Console

**ID:** STORY-017
**Tipo:** Integration
**Prioridade:** P1
**Estimativa:** G (> 4 horas)
**Status:** Backlog
**Sprint:** A definir

---

## User Story

**Como** usuário do Marketing OS com presença no Google,
**Quero** acessar dados reais do Google Search Console no sistema,
**Para que** possa otimizar conteúdo baseado em palavras-chave reais que já estão gerando tráfego e identificar oportunidades de melhoria de posicionamento.

---

## Contexto

O script `scripts/seo_analyzer.py` hoje faz análise técnica on-page mas não tem acesso a dados de busca reais. A integração com Google Search Console via Google APIs permitiria:

- Identificar as queries que já trazem tráfego
- Detectar páginas com alta impressão mas baixo CTR (Quick Wins de SEO)
- Monitorar posição média por keyword ao longo do tempo
- Encontrar oportunidades de conteúdo baseadas em busca real
- Identificar canibalizações de keywords

---

## Acceptance Criteria

```
[ ] Script `scripts/gsc_analyzer.py` criado com funções:
    - get_search_queries(site_url, date_range) → queries + métricas
    - get_top_pages(site_url, date_range) → páginas + métricas
    - get_ctr_opportunities(threshold=0.05) → páginas com baixo CTR
    - get_position_changes(days=30) → keywords com posição mudando
    - get_keyword_cannibalization() → URLs competindo pela mesma query
    - export_to_markdown(data) → relatório formatado

[ ] Autenticação via Google Service Account ou OAuth:
    - Suporte a arquivo de credenciais JSON
    - Variável de ambiente: GOOGLE_SERVICE_ACCOUNT_FILE

[ ] Testes criados em `scripts/tests/test_gsc_analyzer.py`:
    - Mock das chamadas à Google API
    - Teste de todas as funções principais
    - Teste de formatação de output

[ ] Integração com seo_analyzer.py existente:
    - Combinação de análise técnica on-page + dados de performance reais
    - Relatório unificado com as duas análises

[ ] Documentação em `references/google-apis.md`:
    - Como configurar Google Cloud Project
    - Como habilitar Search Console API
    - Como criar Service Account com as permissões corretas
    - Como adicionar a conta à propriedade do Search Console
```

---

## Dependências Técnicas

- Google Cloud Project com Search Console API habilitada
- Service Account com permissão de "leitura" na propriedade do Search Console
- Python: `google-auth`, `google-api-python-client` (adicionar ao requirements)
- Propriedade verificada no Google Search Console

---

## Estrutura do Output Esperado

```markdown
# Relatório GSC — [Domínio] — [Período]

## Quick Wins de CTR
| Página | Impressões | CTR Atual | CTR Esperado | Oportunidade |
|--------|-----------|-----------|--------------|--------------|

## Keywords em Ascensão (posição melhorando)
| Query | Posição Atual | Posição 30 dias atrás | Delta |
|-------|--------------|----------------------|-------|

## Páginas com Alto Potencial (muita impressão, pouco clique)
| Página | Impressões | Posição Média | CTR | Problema Sugerido |
|--------|-----------|--------------|-----|-------------------|
```

---

## Referências

- Google Search Console API: https://developers.google.com/webmaster-tools
- Autenticação Service Account: https://cloud.google.com/iam/docs/service-accounts
