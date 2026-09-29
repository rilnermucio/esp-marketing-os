# STORY-020: Script de Geração Automática de Relatório Semanal

**ID:** STORY-020
**Tipo:** Feature
**Prioridade:** P2
**Estimativa:** M (1-4 horas)
**Status:** Backlog
**Sprint:** A definir

---

## User Story

**Como** usuário do Marketing OS que produz conteúdo regularmente,
**Quero** receber um relatório automático semanal de performance,
**Para que** possa tomar decisões de otimização baseadas em dados sem precisar compilar informações manualmente.

---

## Contexto

O Marketing OS tem ferramentas de análise individuais (seo_analyzer, content_audit, etc.) mas não gera um relatório consolidado automaticamente. Um script de relatório semanal consolidaria todas as métricas relevantes em um único documento.

---

## Acceptance Criteria

```
[ ] Script `scripts/weekly_report.py` criado com funções:
    - generate_weekly_report(week_data) → relatório em Markdown
    - collect_content_metrics(content_list) → métricas de conteúdo
    - collect_seo_metrics(urls) → métricas de SEO
    - generate_next_week_recommendations() → sugestões baseadas nos dados
    - export_report(report, format='markdown') → salvar em output/

[ ] Relatório inclui seções:
    - Resumo executivo (KPIs principais da semana)
    - Performance de conteúdo (posts publicados, engajamento)
    - Performance de SEO (posições, tráfego orgânico)
    - Performance de email (se configurado)
    - Top 3 conteúdos da semana
    - Bottom 3 conteúdos (para otimização)
    - Recomendações para a próxima semana
    - Calendário sugerido da próxima semana

[ ] Geração automática via cron (documentada):
    - Exemplo de configuração de cron job para execução semanal
    - Instruções em `references/automation.md`

[ ] Testes em `scripts/tests/test_weekly_report.py`

[ ] Output salvo em `output/reports/semana-YYYY-WW.md`
```

---

## Estrutura do Relatório

```markdown
# Relatório Semanal — Semana [N] / [Ano]

## Resumo Executivo
| Métrica | Esta Semana | Semana Anterior | Δ |
|---------|-------------|-----------------|---|
| Posts publicados | | | |
| Engajamento médio | | | |
| Novos seguidores | | | |
| Tráfego orgânico | | | |

## Conteúdo da Semana
### Top 3 Conteúdos (melhor performance)
### Bottom 3 Conteúdos (menor performance)

## Insights e Padrões
[Análise gerada automaticamente]

## Recomendações para a Próxima Semana
1. [Recomendação baseada nos dados]
2. [Recomendação baseada nos dados]

## Calendário Sugerido
| Dia | Plataforma | Formato | Tema Sugerido |
|-----|-----------|---------|---------------|
```

---

## Dependências

- Scripts existentes: `content_audit.py`, `seo_analyzer.py`
- Dados de entrada: podem ser JSON manual ou via APIs (Stories 016-019)
- Python: `datetime`, `json` (já disponíveis)
