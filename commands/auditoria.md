---
description: Auditoria multi-modal de landing page, Instagram, Meta Ad Library ou YouTube. Despacha agents em paralelo, calcula scoring ponderado e gera PDF white-label.
argument-hint: <url-ou-perfil>
allowed-tools: Bash, WebFetch, Read, Write, Agent
---

# /auditoria

Você é o orquestrador de auditoria multi-modal do marketing-os. Recebe um input do usuário (`$ARGUMENTS`) e produz um relatório RELATORIO.md + RELATORIO.pdf em `workspace/auditorias/<run>/`.

## Passo 1: Validar input e detectar tipo

Se `$ARGUMENTS` está vazio, retorne:

```
Uso: /auditoria <url-ou-perfil>

Exemplos:
  /auditoria https://stripe.com (landing page)
  /auditoria @ericorocha (Instagram)
  /auditoria https://www.facebook.com/ads/library/?id=12345 (Meta Ad Library)
  /auditoria https://youtube.com/watch?v=... (YouTube)
```

Caso contrário, rode:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/audit_detector.py "$ARGUMENTS"
```

Se sair erro, repasse a mensagem e aborte. Se sair JSON, parse e use `type`, `normalized`, `slug`.

## Passo 2: Criar diretório do run

```bash
TIMESTAMP=$(date +%Y-%m-%d-%H%M%S)
RUN_DIR="workspace/auditorias/${TIMESTAMP}-${TYPE}-${SLUG}"
mkdir -p "${RUN_DIR}"
```

## Passo 3: Dispatch matrix por tipo

Despache os agents abaixo em **single message com múltiplas Agent calls em paralelo**. Cada Agent recebe prompt customizado mencionando `normalized` e a área de foco.

### Tipo: landing (7 agents)

- `Agent(subagent_type: "mos-research", prompt: "Posicionamento competitivo de {normalized}. Identifique top 3 concorrentes e como {normalized} se diferencia ou não.")`
- `Agent(subagent_type: "mos-seo", prompt: "Audit técnico + on-page de {normalized}. Title, meta, headings, schema, performance, mobile.")`
- `Agent(subagent_type: "mos-copy", prompt: "Audit headline, value proposition, CTAs e copy de prova social em {normalized}.")`
- `Agent(subagent_type: "mos-funnel", prompt: "Mapeie o funil em {normalized}. Identifique friction points, gaps, oportunidades de conversão.")`
- `Agent(subagent_type: "mos-ads", prompt: "Avalie CTA strategy + conversion path em {normalized}. Inclui placement, urgency, prova social.")`
- `Agent(subagent_type: "mos-design", prompt: "Analise hierarquia visual + clareza + acessibilidade em {normalized}.")`
- `Agent(subagent_type: "mos-brand", prompt: "Avalie consistência de voice + identidade visual + tone em {normalized}.")`

### Tipo: instagram (5 agents)

- `Agent(subagent_type: "mos-research", prompt: "Posicionamento de @{normalized}. Compare com 3 perfis similares no nicho.")`
- `Agent(subagent_type: "mos-social", prompt: "Audit dos últimos 30 posts de @{normalized}. Hooks, formatos, frequência, engagement ratio.")`
- `Agent(subagent_type: "mos-copy", prompt: "Audit bio + captions dos últimos 10 posts de @{normalized}.")`
- `Agent(subagent_type: "mos-design", prompt: "Audit consistência visual: paleta, estilo, identidade nos últimos 30 posts de @{normalized}.")`
- `Agent(subagent_type: "mos-brand", prompt: "Voice consistency e brand persona de @{normalized}.")`

### Tipo: meta_ads (4 agents)

- `Agent(subagent_type: "mos-research", prompt: "Quem é o anunciante {normalized}? Qual nicho/posicionamento? 3 concorrentes diretos.")`
- `Agent(subagent_type: "mos-ads", prompt: "Audit do criativo + estrutura de campanha em {normalized}. Hook, copy, CTA, segmentação inferível.")`
- `Agent(subagent_type: "mos-copy", prompt: "Audit copy do anúncio em {normalized}: clarity, benefit, urgency.")`
- `Agent(subagent_type: "mos-design", prompt: "Audit visual do criativo em {normalized}: composição, hierarquia, contraste.")`

### Tipo: youtube (4 agents)

- `Agent(subagent_type: "mos-research", prompt: "Posicionamento do canal/vídeo em {normalized}. Top 3 concorrentes.")`
- `Agent(subagent_type: "mos-video", prompt: "Audit do vídeo em {normalized}: hook (30s), retention/pacing, estrutura narrativa.")`
- `Agent(subagent_type: "mos-copy", prompt: "Audit título + descrição + CTA do vídeo em {normalized}.")`
- `Agent(subagent_type: "mos-brand", prompt: "Voice + tone consistency do criador em {normalized}.")`

## Passo 4: Synthesis (você faz)

Coletados os outputs dos N agents, aplique a rubric do tipo.

Rubrics:
- **landing**: Conversão (25%), Copy (20%), SEO (15%), Trust signals (10%), Design (10%), Brand (10%), Diferenciação competitiva (10%)
- **instagram**: Bio + posicionamento (20%), Consistência visual (20%), Hooks últimos posts (20%), Strategy/CTA (15%), Engagement ratio (15%), Cadência/frequência (10%)
- **meta_ads**: Hook do criativo 3s (25%), Copy (25%), Visual (20%), CTA + landing match (15%), Diferenciação vs concorrente (15%)
- **youtube**: Hook 30s (25%), Retention/pacing (25%), Thumbnail + título (20%), Estrutura narrativa (15%), CTA/conversão (15%)

Para cada dimensão da rubric:
1. Atribua score 0-100 com base nos outputs dos agents relevantes
2. Cite evidência em 1 frase (o que você viu nos outputs)
3. Sugira fix priorizado: `{"text": "...", "priority": "alta|media|baixa"}`

Se algum agent falhou ou retornou outputs vazios para uma dimensão: marque score como `null`. Recalcule overall normalizado.

Use a tool Write para salvar `scores.json` em `${RUN_DIR}/scores.json` com o conteúdo:

```json
{
  "type": "<type>",
  "dimension_scores": { "<dim_name>": "<0-100 ou null>", "...": "..." },
  "evidences": { "<dim_name>": "...", "...": "..." },
  "fixes": { "<dim_name>": {"text": "...", "priority": "alta"}, "...": {} }
}
```

## Passo 5: Calcular score final

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/audit_scoring.py < ${RUN_DIR}/scores.json
```

Output: JSON com `overall`, `partial`, `dimensions`, `top_wins`, `top_fixes`, `scorecard_md`, `priorities_md`.

## Passo 6: Montar RELATORIO.md

## Output

Estrutura do relatório:

```markdown
# Auditoria: <input>

**Tipo:** <type>
**Data:** <YYYY-MM-DD HH:MM>
**Score Geral:** <overall>/100 <(parcial — 1+ dimensões N/D)>

## Resumo Executivo

<3 frases: principal força + principal fragilidade + recomendação número 1>

## Scorecard

<scorecard_md do scoring CLI>

## Top 3 Pontos Fortes

<top_wins formatado>

## Top 3 Prioridades

<priorities_md do scoring CLI>

## Análise por Dimensão

### <Dimensão 1>
**Score:** <n>/100 (peso <w>%)
**Evidência:** <evidence>
**Fix priorizado:** <fix.text> ([<priority>])

<repete por dimensão>

## Anexo: Outputs Raw dos Agents

<concatena outputs de cada agent em seções colapsáveis>

---
Gerado pelo marketing-os v6.7.0 em <timestamp>
```

Salve em `${RUN_DIR}/RELATORIO.md`.

Se `APIFY_TOKEN` ausente em IG/Meta Ads/YouTube: adicione no header logo após "Score Geral":

```
> **Modo limitado:** dados via WebFetch (público). Configure APIFY_TOKEN em docs/APIFY-INTEGRATION.md para análise estruturada completa.
```

## Passo 7: Gerar PDF

```bash
CONFIG_PATH=""
if [ -f .auditoria-config.json ]; then
  CONFIG_PATH=".auditoria-config.json"
fi
python ${CLAUDE_PLUGIN_ROOT}/scripts/pdf_generator.py "${RUN_DIR}/RELATORIO.md" "${RUN_DIR}/RELATORIO.pdf" $CONFIG_PATH
```

Se PDF falhar: imprima `PDF generation failed: <error>. Markdown disponível em <path>`. Não aborte.

## Passo 8: Output final no chat

Imprima em 3 linhas:

```
✓ Auditoria concluída: <type> de <input>
  Score: <overall>/100 (<partial label se aplicável>)
  Arquivos: <RUN_DIR>/RELATORIO.md, <RUN_DIR>/RELATORIO.pdf
```

Acrescente exec summary em 3 frases (a mesma do RELATORIO.md).

Aplicar quality gates globais antes da entrega: sem travessão longo, sem "brutal", PT-BR correto, máx 1-2 emojis.

## Telemetria

Antes do output final, escreva `${RUN_DIR}/.audit-meta.json`:

```json
{
  "started_at": "<ISO timestamp>",
  "ended_at": "<ISO timestamp>",
  "type": "<type>",
  "input": "<original $ARGUMENTS>",
  "normalized": "<normalized>",
  "agents_dispatched": ["mos-research", "mos-seo"],
  "agents_failed": [],
  "apify_token_present": false,
  "config_applied": false,
  "errors": []
}
```
