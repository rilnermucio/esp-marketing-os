# Workflow: Copy Agent Knowledge Refresh

> **Cadência recomendada**: anual (Janeiro), ou ad-hoc quando notar que outputs estão referenciando dados/tendências defasadas.

Audit periódico de `subagents/copy-agent.md` para evitar drift de informação. Stats de marketing, modelos de IA, tendências, e benchmarks envelhecem rápido. Sem refresh, o agent vai citar dados de anos anteriores como se fossem atuais.

## Quando rodar

- **Calendário**: 1x por ano em Janeiro
- **Trigger ad-hoc**: ao notar que output cita stat/modelo/trend obsoleto
- **Trigger contextual**: após mudança importante no setor (novo modelo Claude lançado, nova regulação, etc.)

## Pre-Flight

1. `git status` deve estar clean (refresh é commit isolado)
2. Branch nova: `chore/copy-refresh-{YYYY-MM}`
3. Backup: o próprio git é seu backup, mas confirme que está em branch dedicada

## Phase 1: Inventário de itens com data/versão

Use `Grep` em `subagents/copy-agent.md` para encontrar candidatos a refresh:

```bash
grep -n -E "(20[0-9]{2}|GPT-[0-9]|Claude.*[0-9]\.[0-9]|Gemini [0-9]|Última Atualização|McKinsey|R\$[0-9]+)" subagents/copy-agent.md
```

Categorize as ocorrências:

| Categoria | Exemplos | Ação |
|-----------|----------|------|
| Versões de modelo AI | "Claude Opus 4.6", "GPT-4o", "Gemini 2.0" | Atualizar para versão atual |
| Stats com fonte | "63% mais tráfego (McKinsey)" | WebSearch validar; atualizar ou remover |
| Trends temporais | "PARTE XVI: Tendências de Copy 2026" | Renomear para ano atual; revisar 10 trends |
| Preços de ferramentas | "$20/mês", "$49/mês" | Validar via site da ferramenta |
| Datas em exemplos | "março de 2024", "Dezembro/2025" | Atualizar ou tornar atemporal |
| "Última Atualização: Fev 2026" | Linha 11 do arquivo | Bump para mês atual |

## Phase 2: Validação de cada item

Para cada item identificado:

### Modelos de IA (PARTE VI seção 6.2)

```
Validar via:
- Site oficial Anthropic: claude versions atuais
- Site OpenAI: GPT versions atuais
- Site Google AI: Gemini versions atuais

Atualizar:
- Modelo (versao)
- Preço (USD/BRL)
- Forças/diferenciais (mudaram?)
```

### Stats de mercado

Para cada stat citado (ex: "63% mais tráfego orgânico"):
1. WebSearch da claim com source
2. Se confirmado e data >= 12 meses → manter, atualizar fonte
3. Se confirmado e data < 12 meses → ok
4. Se não confirmado → REMOVER ou substituir por linguagem direcional ("substancialmente mais")

### Tendências (PARTE XVI)

Para cada uma das 10 trends:
1. Ainda relevante? (sim → atualizar evidências)
2. Substituída por trend mais nova? (sim → trocar)
3. Reverteu? (sim → remover)

Renomear título PARTE XVI para ano atual.

### Power Words & Glossário (Apêndice)

- Adicionar termos novos do mercado (e.g., "AI Overviews", "agentic", "LLM-native")
- Marcar termos obsoletos como `(legado)` em vez de remover

## Phase 3: Verificar consistência cross-document

Após editar `copy-agent.md`, verificar referências em:

- `subagents/copy-agent.md` — Última Atualização (linha 11)
- `.claude/agents/mos-copy.md` — capacidades referenciam PARTE X (sem mudar números)
- `README.md` — versão se mudou
- `CHANGELOG.md` — adicionar entrada

```bash
grep -rn "PARTE [IVX]\+" .claude/agents/ subagents/ commands/ workflows/ 2>/dev/null
```

Se a numeração de PARTES mudou (improvável em refresh, mas check), atualize cross-references.

## Phase 4: Re-run validações

```bash
# Markdown válido (se usa markdownlint)
# python -m markdownlint subagents/copy-agent.md

# Pytest (incluso test_subagents.py)
python3 -m pytest scripts/tests/test_subagents.py -v

# Quality gate hook não bloqueia (sample em-dash)
echo '{"tool_name":"Write","tool_input":{"file_path":"subagents/copy-agent.md","content":"sample"}}' | python3 scripts/hooks/quality_gate_hook.py
```

## Phase 5: Commit

```bash
git add subagents/copy-agent.md CHANGELOG.md README.md
git commit -m "chore(copy-agent): annual knowledge refresh ${YYYY}-${MM}"
git push origin {branch}
```

PR opcional para revisão.

## Phase 6: Memory hygiene

Após refresh, considerar limpar `.claude/agent-memory/mos-copy/MEMORY.md` de aprendizados que ficaram obsoletos pela atualização. Ler MEMORY.md, comparar com novo conhecimento, podar entradas que conflitam.

## Critérios de Done

- [ ] Todas versões de modelo AI atualizadas
- [ ] Stats sem fonte foram validados (WebSearch) ou removidos
- [ ] Tendências revisadas, ano renomeado
- [ ] Preços de ferramentas validados
- [ ] Última Atualização (linha 11) bumped
- [ ] Pytest passa
- [ ] CHANGELOG entry adicionada
- [ ] Commit em branch dedicada, PR aberto se aplicável

## Anti-padrões (NÃO faça)

- ❌ Refresh sem WebSearch (vai re-introduzir dados obsoletos)
- ❌ Atualizar só "Última Atualização" sem revisar conteúdo
- ❌ Remover stats sem alternativa (deixa lacuna no agent)
- ❌ Refresh em main branch direto (sempre via branch dedicada)
- ❌ Atualizar copy-agent.md sem atualizar mos-copy.md (Tier 1) se houver dependência

## Histórico de refreshes

| Data | Versão antes → depois | Notas |
|------|------------------------|-------|
| 2026-02 | v3.1 inicial | Última atualização registrada |

(Adicionar linhas a cada refresh.)
