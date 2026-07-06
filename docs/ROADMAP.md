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
- **`/narrar-roteiro`** — roteiro do mos-audio/mos-video vira áudio PT-BR (skill hyperframes TTS Kokoro, sem API key). Fecha um pedaço do gap de mídia real.
- **mos-analytics + `memory: project`** — alinha o agent de dados com os outros 9; 1 linha de frontmatter + bloco de memory + entrada em `init_agent_memory.py`.
- **`seasonal_calendar_br.py` + `/datas-sazonais`** — efemérides comerciais BR (Carnaval/Páscoa via Computus) pro calendário.

### Fase 2: geração real de mídia (fecha o gap "só gera prompt")
- ~~**`/renderizar-imagem`**~~ **ENTREGUE (jul/2026)**: prompt do mos-ai-tools vira PNG via skill do ambiente (gpt-image-2 / ai-image-generation), com fallback pra entrega do prompt.
- ~~**`/gerar-thumbnail`**~~ **ENTREGUE (jul/2026)**: Thumbnail Brief do mos-video vira 1280x720 (fundo sem texto via skill + overlay tipográfico determinístico em `scripts/thumbnail_composer.py`).
- ~~**`/produzir-reels`**~~ **ENTREGUE (jul/2026)**: pipeline em degraus roteiro → narração (/narrar-roteiro) → HyperFrames, com fallback honesto por degrau. Visão geral em `docs/MEDIA-PIPELINE.md`.

### Fase 3: novos agents (puro "mais skill", encaixa no Tier-1/Tier-2)
- ~~**mos-offer + `/criar-oferta`**~~ **ENTREGUE (jul/2026)**: arquitetura de oferta (Grand Slam, value stack, garantia, bônus) com desempate offer/copy/funnel/infoproduct na SKILL.md, memory opt-in e KB própria (`subagents/offer-agent.md`).
- ~~**mos-community + `/responder-comentarios`**~~ **ENTREGUE (jul/2026)**: triagem e resposta de comentários/DMs no tom da marca (modo rascunho com confirmação humana; nunca publica sem aprovação).
- ~~**mos-partnerships + `/prospectar-creators`**~~ **ENTREGUE (jul/2026)**: descoberta e outreach de creators (Gmail create_draft quando MCP disponível, nunca envio direto).

### Fase 4: loop de aprendizado (deixa as skills melhores com o tempo)
- ~~**`scripts/memory_writer.py`**~~ **ENTREGUE (jul/2026)**: API append-only idempotente com schema anti-poluição (categorias, 400 chars, 20/dia) em `.claude/agent-memory/mos-*/MEMORY.md`.
- ~~**`/aprender` + `metrics_collector.py`**~~ **ENTREGUE (jul/2026)**: coleta no runtime (MCP ou export manual) → normalização stdlib → interpretação mos-analytics → persistência aprovada via memory_writer.

Nota: atribuição peça↔métrica fica aproximada (manual) sem pipeline de publicação. Aceitável: o loop pull-de-métrica + writeback já fecha o ciclo sem precisar de infra de publishing.

## Disciplina ao construir

Cada feature: brainstorming de design antes de codar, encaixe no padrão existente (command dá dispatch, agent novo passa `validate_agents.py --strict`, script novo entra no `mos.py` + tem teste), e os guard-rails de drift/segurança continuam verdes. Atualizar contagens (README/AGENTS) quando adicionar agent/command — os testes de consistência travam isso.
