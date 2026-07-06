---
description: Índice dos 6 presets de campanha disponíveis (lancamento, prospeccao, retencao, autoridade, growth, black-friday). Liste tipos e roteie pro sub-command correspondente. Roteador puro, sem dispatch direto.
argument-hint: "(sem argumentos: lista presets) | <preset> redireciona para /campanha-<preset>"
---

# /campanha: Índice de Presets de Campanha

Roteador puro. Lista os 6 presets disponíveis e direciona pro sub-command que despacha os agents da campanha escolhida. **Não despacha agents diretamente.**

Para ativar um preset, use o sub-command correspondente:

| Preset | Sub-command | Objetivo | Agents principais | Clone primário |
|--------|-------------|----------|-------------------|----------------|
| Lançamento | `/campanha-lancamento` | Lançar produto/serviço/curso/oferta com máximo impacto | mos-research, mos-launch, mos-funnel, mos-copy, mos-storytelling, mos-social, mos-email, mos-ads, mos-design, mos-analytics | `brunson` |
| Prospecção | `/campanha-prospeccao` | Gerar leads qualificados e novos clientes consistentemente | mos-research, mos-funnel, mos-copy, mos-ads, mos-email, mos-social, mos-analytics | `suby` |
| Retenção | `/campanha-retencao` | Aumentar LTV, reativar inativos, reduzir churn | mos-research, mos-analytics, mos-email, mos-copy, mos-social | `abraham` |
| Autoridade | `/campanha-autoridade` | Construir thought leadership e presença de marca | mos-research, mos-brand, mos-copy, mos-seo, mos-social, mos-storytelling, mos-audio | `ogilvy` |
| Growth | `/campanha-growth` | Experimentação acelerada para crescimento não-linear | mos-research, mos-analytics, mos-ab-testing, mos-growth, mos-copy | `ellis` |
| Black Friday | `/campanha-black-friday` | Maximizar receita em datas especiais | mos-launch, mos-copy, mos-email, mos-ads, mos-social, mos-analytics | `hormozi` |

## Como usar

1. Identifique o objetivo da campanha (lançamento? prospecção? retenção?).
2. Rode o sub-command direto: `/campanha-lancamento`, `/campanha-prospeccao`, etc.
3. Cada sub-command aceita customizações: `--produto=`, `--clone=`, `--canal=`, `--budget=`, `--nicho=`, `--preco=`, `--segmento=`, `--desconto=` conforme o preset.

Exemplos:

```
/campanha-lancamento --produto="Curso de Copy" --preco=997 --clone=hormozi
/campanha-prospeccao --canal=instagram --budget=500 --nicho=empreendedorismo
/campanha-retencao --segmento=inativos-90dias --desconto=20%
/campanha-autoridade --clone=garyvee
/campanha-black-friday --produto="Mentoria 1:1" --desconto=40%
```

## Quality Gates Globais (aplicáveis a todos os presets)

Ver `skills/marketing-os/SKILL.md`. Cada sub-command já reforça localmente, mas resumindo: sem `—` (travessão longo), sem "brutal", sem CAPS gratuito, sem aspas em roteiros/falas, máximo 1-2 emojis (preferir 0), acentuação PT-BR correta, fact-check via WebSearch em pessoas/estatísticas/cases, compliance regulatório se nicho saúde/finanças/suplementos, enquete obrigatória em conteúdo social, disclaimer "Resultados não garantidos" em promessa quantitativa.

## Recursos relacionados

- `workflows/end-to-end-campaign-workflow.md`: workflow completo de referência
- `workflows/content-pipeline.md`: pipeline de produção
- `assets/clones/clone-manifest.yaml`: sistema de clones (35 perfis)
- `subagents/ab-testing-agent.md`: testes A/B aprofundados
- `scripts/ab_generator.py`: geração automática de variantes

## Por que essa estrutura de presets

Campanhas falham quando se pula a estratégia e vai direto pra execução de copy. Cada preset força a sequência adequada ao objetivo: research/strategy primeiro, depois assets em paralelo, depois execução técnica (ads/tracking). Quebrar em sub-commands separados deixa autocomplete mais útil e reduz o tamanho do arquivo carregado por preset.
