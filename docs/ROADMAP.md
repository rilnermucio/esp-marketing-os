# Roadmap — Marketing OS

## Princípio de escopo (decisão de identidade do plugin)

Marketing OS é um **sistema de skills de geração, estratégia e inteligência de marketing**. O valor está em gerar e validar conteúdo/estratégia de alta qualidade sob demanda, com contexto isolado por agent e knowledge base profunda.

O que **aprofunda** essa identidade entra no roadmap. O que empurra pra **ops/automação stateful** fica de fora do plugin (papel de MCP ou ferramenta dedicada).

## Fora de escopo (decidido, não construir no plugin)

| Item | Por que não |
|------|-------------|
| Fila de agendamento / cron / `/agendar-conteudo` | Claude Code não tem cron persistente; scheduler stateful briga com o meio. Papel de Buffer/Meta Suite/n8n. |
| Construção de workflow n8n / `/ativar-funil` | Vira plataforma de execução; depende de credencial externa por node. n8n faz isso melhor direto. |
| Disparo de WhatsApp em massa | Efeito irreversível + aprovação de template Meta. Wrapper fino de MCP, não infra de plugin. |
| Publicar campanha paga no Meta Ads | Move dinheiro real. Usar o MCP Meta Ads diretamente, com gate humano. |
| Pipeline de publicação social stateful | O valor está na geração + validação (já feito); postar é wrapper de MCP, não precisa de fila/estado próprios. |

O plugin **gera e valida**; quem executa/agenda é o MCP ou a ferramenta dedicada.

## Grupo A — construir (ordenado por impacto)

### Fase 1: quick wins (esforço S)
- ~~**`/narrar-roteiro`**~~ **ENTREGUE (jul/2026)**: roteiro do mos-audio/mos-video vira áudio PT-BR com fallback explícito por ambiente.
- ~~**mos-analytics + `memory: project`**~~ **ENTREGUE (jul/2026)**: agent nivelado e incluído no bootstrap idempotente de memória.
- ~~**`seasonal_calendar_br.py` + `/datas-sazonais`**~~ **ENTREGUE (jul/2026)**: calendário comercial BR determinístico, com feriados móveis calculados e saída texto/JSON.

### Fase 2: geração real de mídia (fecha o gap "só gera prompt")
- ~~**`/renderizar-imagem`**~~ **ENTREGUE (jul/2026)**: prompt do mos-ai-tools vira PNG via skill do ambiente (gpt-image-2 / ai-image-generation), com fallback pra entrega do prompt.
- ~~**`/gerar-thumbnail`**~~ **ENTREGUE (jul/2026)**: Thumbnail Brief do mos-video vira 1280x720 (fundo sem texto via skill + overlay tipográfico determinístico em `scripts/thumbnail_composer.py`).
- ~~**`/produzir-reels`**~~ **ENTREGUE (jul/2026)**: pipeline em degraus roteiro → narração (/narrar-roteiro) → HyperFrames, com fallback honesto por degrau. Visão geral em `docs/MEDIA-PIPELINE.md`.

### Fase 3: novos agents (puro "mais skill", encaixa no Tier-1/Tier-2)
- ~~**mos-offer + `/criar-oferta`**~~ **Entregue (jul/2026), hardening (ago/2026)**: arquitetura de oferta com value stack, garantia, preço, evidências e validação; preserva o Handoff da USP, usa research antes de oferta high-ticket sem dados e entrega claims aprovados/bloqueados. Possui desempate offer/copy/funnel/infoproduct, memory opt-in e KB própria (`subagents/offer-agent.md`).
- ~~**mos-community + `/responder-comentarios`**~~ **ENTREGUE (jul/2026)**: triagem e resposta de comentários/DMs no tom da marca (modo rascunho com confirmação humana; nunca publica sem aprovação).
- ~~**mos-partnerships + `/prospectar-creators`**~~ **ENTREGUE (jul/2026)**: descoberta e outreach de creators (Gmail create_draft quando MCP disponível, nunca envio direto).

### Fase 4: loop de aprendizado (deixa as skills melhores com o tempo)
- ~~**`scripts/memory_writer.py`**~~ **ENTREGUE (jul/2026)**: API append-only idempotente com schema anti-poluição (categorias, 400 chars, 20/dia) em `.claude/agent-memory/marketing-os-mos-*/MEMORY.md`.
- ~~**`/aprender` + `metrics_collector.py`**~~ **ENTREGUE (jul/2026)**: coleta no runtime (MCP ou export manual) → normalização stdlib → interpretação mos-analytics → persistência aprovada via memory_writer.

Nota: atribuição peça↔métrica fica aproximada (manual) sem pipeline de publicação. Aceitável: o loop pull-de-métrica + writeback já fecha o ciclo sem precisar de infra de publishing. Desde set/2026 o `scripts/utm_builder.py` gera o link com `piece_id` estável junto com a peça, o que fecha a atribuição quando o export de métricas traz o `utm_content`.

### Fase 5: plugin instalado e mercado brasileiro (auditoria de set/2026)
- ~~**Runtime instalado**~~ **ENTREGUE (set/2026)**: caminhos pela raiz do plugin, dispatch qualificado `marketing-os:mos-*`, gate em `hooks/hooks.json`, memória no diretório nativo e smoke de instalação real (ADR-0005 e ADR-0006).
- ~~**Dispatch pela plataforma**~~ **PILOTO (set/2026)**: `/gerar-imagem` roda dentro do `mos-ai-tools` via `context: fork` (ADR-0007). Candidatos seguintes: `/minerar-voc` e `/narrar-roteiro` com material em arquivo, depois de uso real sem regressão.
- ~~**Contexto de marca**~~ **ENTREGUE (set/2026)**: `/configurar-marca` e perfil lido pelos 21 especialistas.
- ~~**Voz do cliente e prova social**~~ **ENTREGUE (set/2026)**: `/minerar-voc` com `voc_extractor.py` e `/coletar-prova` com termo de autorização.
- ~~**Compliance BR**~~ **ENTREGUE (set/2026)**: `references/compliance-br.md` com normas conferidas no texto integral, `/checar-compliance`, `compliance_check.py` e frases de risco no hook. Revisão trimestral avisada pelo `mos.py facts check`.
- ~~**Busca por IA e plataformas BR**~~ **ENTREGUE (set/2026)**: GEO e AEO na KB de SEO; Kwai, WhatsApp (Status e Canais), Threads, LinkedIn e marketplaces nas KBs de social, copy e ads; registro de fatos com fonte e data.
- ~~**Reaproveitamento e revisão**~~ **ENTREGUE (set/2026)**: `/reaproveitar`, `/otimizar-copy` para qualquer formato e modo avaliações no `/responder-comentarios`.
- **Evals de output**: golden set e baselines de mos-social, mos-email e mos-ads entregues em set/2026; falta a primeira rodada julgada par a par contra essas baselines.

## Disciplina ao construir

Cada feature: brainstorming de design antes de codar, encaixe no padrão existente (command dá dispatch, agent novo passa `validate_agents.py --strict`, script novo entra no `mos.py` + tem teste), e os guard-rails de drift/segurança continuam verdes. Atualizar contagens (README/AGENTS) quando adicionar agent/command — os testes de consistência travam isso.
