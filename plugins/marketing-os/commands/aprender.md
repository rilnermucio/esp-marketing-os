---
description: Loop de aprendizado com métricas reais. Coleta via MCP ou export manual, normaliza com metrics_collector, interpreta via mos-analytics e persiste aprendizados aprovados na memory dos agents-dono. Dispara em "aprender", "o que funcionou", "métricas do mês", "guarda na memory".
argument-hint: "<plataforma/canal> <período> [métrica primária, ex: retention|ctr|open_rate]"
---

# /aprender: Loop de Aprendizado (métricas → memory)

Fecha o ciclo Fase 4 do ROADMAP: métricas reais viram patterns transferíveis nas memories opt-in dos agents. O runtime **coleta** (MCP ou export manual); os scripts Python **normalizam e persistem**; o `mos-analytics` **interpreta**.

## Required inputs (ask if missing)

1. **Plataforma/canal** (obrigatório): Instagram, TikTok, Threads, YouTube, Meta Ads, email (Resend/outro), GSC, etc.
2. **Período** (obrigatório): últimos 7/30/90 dias, mês calendário, ou intervalo explícito
3. **Fonte dos dados** (obrigatório): MCP disponível no ambiente OU export manual (JSON/CSV colado ou arquivo)
4. **Métrica primária** (obrigatório pra ranqueamento): retention, ctr, open_rate, views, CPA, take rate, etc.
5. **Mapeamento peça → agent-dono** (opcional): se o usuário souber qual post/email/anúncio foi de qual agent, acelera a atribuição. Sem mapeamento, o mos-analytics infere pelo tipo de peça.

## Fase 1: coleta (runtime)

No ambiente com MCP, puxe métricas com as tools disponíveis. Exemplos por plataforma:

| Plataforma | Tools / scripts de exemplo |
|---|---|
| Instagram | `instagram_get_insights`, insights de mídia do perfil |
| TikTok / Threads | tools de insights da plataforma quando conectadas |
| YouTube | `python scripts/youtube_analytics.py` ou `mos youtube top-videos` |
| Meta Ads | `mcp_meta-ads_get_insights`, `get_insights` por campanha/ad |
| GSC | `mos gsc top-pages`, `mos gsc ctr-opportunities` |
| Email | export do provedor (open rate, CTR por subject) |

**Export manual:** peça JSON ou CSV com identificador (`id`, `titulo`, `title` ou `name`) + campos numéricos livres (`views`, `ctr`, `retention`, `open_rate`, etc.). Salve em `workspace/` (gitignored), nunca no plugin.

Monte uma lista JSON uniforme, um objeto por peça analisada.

## Fase 2: normalização (Bash local)

Rode o normalizador com amostra mínima (default 5). Se a lista for menor, o script barra com exit 1 (aprendizado com 3 posts é ruído).

```bash
python3 scripts/metrics_collector.py --input workspace/metricas-instagram-jul.json \
  --metrica retention --min-amostra 5

# ou via CLI unificado
python3 scripts/mos.py metrics summarize --input workspace/metricas-instagram-jul.json \
  --metrica retention --min-amostra 5
```

Capture o markdown de stdout. Se exit ≠ 0, pare e informe o usuário (amostra insuficiente ou input inválido). Não invente números.

## Fase 3: interpretação (dispatch)

Despache o mos-analytics pra transformar o resumo em aprendizados acionáveis **por agent-dono** (máximo 3-5 por rodada, formato curto, pattern transferível):

```
Agent(subagent_type: "mos-analytics", prompt: "Interprete este resumo de métricas e proponha aprendizados por agent-dono.

PLATAFORMA: [plataforma]
PERÍODO: [período]
MÉTRICA PRIMÁRIA: [métrica]

RESUMO (metrics_collector):
[colar markdown da Fase 2]

MAPEAMENTO PEÇA→AGENT (se houver):
[ex: reel-3 → mos-video, email-12 → mos-email]

Regras:
- Máximo 3-5 aprendizados no total, cada um com 1 frase curta (≤400 chars)
- Só PATTERN transferível (o que repetir ou evitar), nunca dump de dados brutos
- Categorias permitidas: resultado, pattern, anti-padrao, voz, benchmark-local
- Atribua cada aprendizado ao agent-dono correto:
  - CTR/thumbnail/retention de vídeo → mos-video
  - subject line/open rate → mos-email
  - take rate/value stack/oferta → mos-offer
  - engajamento de post/carrossel → mos-social
  - hook/copy de anúncio → mos-ads ou mos-copy conforme peça
  - keyword/posição orgânica → mos-seo
- Se não houver sinal forte (>30% vs média no resumo), diga explicitamente e não force aprendizado

Entregue tabela: agent-dono | categoria | aprendizado proposto | evidência (1 linha)")
```

## Fase 4: persistência (após aprovação humana)

**Gate obrigatório:** mostre os aprendizados propostos e peça confirmação antes de gravar. Só persista o que o usuário aprovar.

Verifique memory opt-in:

```bash
python3 scripts/init_agent_memory.py --check
```

Se `.claude/agent-memory/` não existir, ofereça rodar `python3 scripts/init_agent_memory.py` e só persista depois do bootstrap.

Para cada aprendizado aprovado:

```bash
python3 scripts/memory_writer.py --agent mos-video --categoria pattern \
  --texto "Hooks com pergunta nos 3s primeiros correlacionam com retenção acima da média" \
  --fonte "/aprender [plataforma] [período]"

# ou
python3 scripts/mos.py memory write --agent mos-email --categoria resultado \
  --texto "Subject com número específico abriu 18% acima da média do lote" \
  --fonte "/aprender [plataforma] [período]"
```

Exit 0 = gravado; exit 1 = duplicado, categoria inválida, limite diário ou texto longo demais. Reporte o motivo ao usuário.

## Fase 5: relatório final

Consolide o que foi coletado, interpretado e persistido (ver schema abaixo).

## Consolidação

Entregue ao usuário:

```markdown
## /aprender — [plataforma] · [período]

### Coleta
- Fonte: [MCP / export manual / script local]
- Itens analisados: [N]
- Métrica primária: [métrica]

### Resumo do que performou
[colar ou resumir o markdown do metrics_collector]

### Aprendizados propostos (por agent-dono)
| Agent | Categoria | Aprendizado | Status |
|---|---|---|---|
| mos-video | pattern | [...] | aprovado / descartado / pendente |

### Persistido na memory
- [agent]: [texto gravado] (ou "nenhum: usuário não aprovou / memory não inicializada")

### Próxima rodada
- [quando repetir, qual métrica testar, amostra mínima a acumular]
```

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Amostra mínima respeitada (metrics_collector barra abaixo do `--min-amostra`)
- Aprendizado é pattern transferível, nunca dump de métricas brutas
- Usuário aprovou antes de persistir
- Memory é opt-in (bootstrap oferecido se `.claude/agent-memory` ausente)
- Máximo 3-5 aprendizados por rodada; texto ≤400 chars por entrada
- Sem travessão, sem "brutal", sem antítese negação→afirmação, acentos PT-BR

## Por que esse dispatch

Coleta de métricas vive no runtime (MCP/tools do ambiente), não em Python do plugin. O `metrics_collector` só normaliza com stdlib; o `memory_writer` só persiste com regras anti-poluição. A interpretação "o que isso significa pra cada domínio" é competência do `mos-analytics`, que já cruza benchmarks e sinais sem contaminar a memory com ruído numérico. Separar coleta → normalização → interpretação → persistência mantém cada camada testável e evita que um post viral vire dump eterno na memory do agent errado.
