# Validation Guide — Marketing OS v6.5.0

Test cases pra validar que o orquestrador está dispatching corretamente nos workflows da v6.x e que os 25 slash commands cumprem o contrato de dispatch padronizado a partir da v6.5.0.

## Como rodar os testes

1. Abra Claude Code numa pasta de teste (não no repo do plugin):
   ```bash
   mkdir ~/Code/test-marketing-os && cd $_
   claude
   ```

2. Pra cada caso abaixo, cole o briefing, observe **quais agents foram dispatched** e marque ✅ ou ❌.

3. Se algum dispatch falhar, abra issue com:
   - Versão do plugin (`/plugin` mostra)
   - Briefing usado
   - Agents que apareceram (esperados vs observados)

---

## Test cases

### Test 1 — Dispatch simples (workflow #1)

**Briefing:**
```
/marketing-os escreve 5 headlines pra meu curso de Python pra devs juniores
```

**Esperado:**
- ✅ Dispatch único: `mos-copy`
- ✅ Output: 5 headlines + 2-3 variações A/B
- ✅ Quality gates aplicados (sem `—`, sem "brutal", PT-BR correto)

---

### Test 2 — Dispatch paralelo (workflow #2)

**Briefing:**
```
/marketing-os tenho um curso novo de IA pra empreendedores BR, preciso de pesquisa de mercado + tom de marca + 5 headlines iniciais
```

**Esperado:**
- ✅ Dispatch paralelo (single message, 3 Agent calls): `mos-research` + `mos-brand` + `mos-copy`
- ✅ Outputs consolidados num único entregável

---

### Test 3 — Página de aplicação (workflow #5)

**Briefing:**
```
/marketing-os cria página de aplicação pra mentoria de marketing digital high-ticket (R$ 15.000)
```

**Esperado:**
- ✅ NÃO delegar direto a `frontend-design` ❌
- ✅ Dispatch paralelo Fase 1: `mos-funnel` + `mos-copy` + `mos-design`
- ✅ Brief consolidado entregue
- ✅ Pergunta se quer HTML/CSS de fato — só aí delega a `frontend-design`

**Como saber se está certo:** se o output só fala HTML/CSS sem mencionar "estrutura BOFU", "anti-avatar", "stack value", "paleta sugerida" → orquestrador pulou Fase 1 (bug).

---

### Test 4 — Carrossel completo (workflow #8)

**Briefing:**
```
/marketing-os cria um carrossel sobre 10 erros de copy que matam conversão, pra LinkedIn
```

**Esperado:**
- ✅ Dispatch paralelo: `mos-social` + `mos-copy` + `mos-design`
- ✅ Output: estrutura de slides + texto de cada slide + design spec + caption + hashtags + sugestão de enquete obrigatória

---

### Test 5 — VSL (workflow #9)

**Briefing:**
```
/marketing-os cria VSL completa pra produto de finanças (curso de R$ 1.997)
```

**Esperado:**
- ✅ Dispatch paralelo: `mos-storytelling` + `mos-copy` + `mos-video`
- ✅ Roteiro consolidado: arco narrativo + estrutura copy (big idea, mecanismo único, anti-avatar, stack value, garantia, FAQ) + ciência de retenção
- ✅ Disclaimer CVM aplicado automaticamente (nicho finanças)

---

### Test 6 — Briefing vago (protocolo de pergunta)

**Briefing:**
```
/marketing-os cria copy
```

**Esperado:**
- ✅ NÃO chuta nicho/avatar/plataforma
- ✅ Pergunta as 5 chaves de uma vez (numeradas):
  1. Nicho?
  2. Avatar?
  3. Ticket?
  4. Plataforma?
  5. Urgência?

---

### Test 7 — Memory persistente (project-scope)

**Setup:**
1. Pasta `~/Code/clientes/test-cliente-A`
2. Bootstrap dos diretórios de memory (uma vez por projeto):
   ```bash
   python3 scripts/init_agent_memory.py
   ```
   Isso cria os 9 diretórios `.claude/agent-memory/mos-{copy,research,brand,seo,social,ads,email,funnel,design}/` no formato canônico.
3. Rodar Test 3 acima nessa pasta
4. Sair do Claude Code, voltar pra mesma pasta dias depois

**Briefing follow-up:**
```
/marketing-os gera 3 variações de headline pra essa página de aplicação
```

**Esperado:**
- ✅ `mos-copy` carrega memory de `.claude/agent-memory/mos-copy/` (path canônico padronizado no P1-3 — antes era `marketing-os-mos-copy/`)
- ✅ Não pergunta nicho/avatar/ticket de novo (já tem no memory)
- ✅ Headlines coerentes com posicionamento da sessão anterior

---

### Test 8 — Compliance regulatório

**Briefing (saúde):**
```
/marketing-os cria post Instagram pra clínica de nutrologia, com 3 dicas de saúde
```

**Esperado:**
- ✅ Detecta nicho saúde
- ✅ Aplica disclaimers automaticamente:
  - "Resultados variam"
  - CRM visível
  - Sem prometer "cura" ou "tratamento"

**Briefing (finanças):**
```
/marketing-os cria carrossel sobre fundo de investimento pra LinkedIn
```

**Esperado:**
- ✅ Detecta nicho finanças
- ✅ Adiciona "Rentabilidade passada não garante futura"
- ✅ Sem promessa de retorno

---

### Test 9 — Voice clone (assets/clones/)

**Briefing:**
```
/marketing-os escreve sales letter no estilo do Gary Halbert pra produto de finanças (curso R$ 997)
```

**Esperado:**
- ✅ `mos-copy` lê `assets/clones/halbert/`
- ✅ Output em estilo direto, agressivo, story-driven (típico Halbert)
- ✅ Disclaimer CVM aplicado (nicho finanças)

---

### Test 10 — Skill colision com `frontend-design`

**Setup:** plugins `frontend-design` e `marketing-os` instalados juntos.

**Briefing:**
```
/marketing-os preciso de uma página de aplicação BOFU pra mentoria de saúde
```

**Esperado:**
- ✅ Marketing-os assume controle (declarado em workflow #5)
- ✅ Dispatcha mos-funnel + mos-copy + mos-design ANTES de qualquer build
- ✅ Se user pediu HTML, entrega ao `frontend-design` Fase 2 com brief consolidado

**Se falhar:** o `frontend-design` interceptou direto sem passar pelos `mos-*`. Investigar dispatch priorities.

---

### Test 11 — Slash command direto: `/criar-anuncio`

**Briefing:**
```
/criar-anuncio Meta Ads pra curso de Copy de R$ 1.997, audiência empreendedores BR
```

**Esperado:**
- ✅ Dispatch `mos-ads` (em paralelo com `mos-research` se nicho/avatar pouco conhecido)
- ✅ Output: 5 versões com angles diferentes (problema/solução, social proof, contraste, FOMO, autoridade)
- ✅ Cada versão com primary text + headline + description + CTA + creative direction
- ✅ Quality gates aplicados (sem CAPS abusivo, sem `—`, sem "brutal", PT-BR correto)

**Como saber se está certo:** se a saída tem só uma variação ou pula a creative direction → falta de seguir o output schema do `mos-ads`.

---

### Test 12 — Slash command direto: `/criar-artigo`

**Briefing:**
```
/criar-artigo sobre 'estrutura de funil de vendas' targeting 'funil de vendas SaaS'
```

**Esperado:**
- ✅ Dispatch sequencial: `mos-research` (intenção + SERP) → `mos-seo` (keyword map + meta) → opcional `mos-copy` (corpo do artigo)
- ✅ Output: keyword map (primária + LSI) + meta tags (title + description) + outline H2/H3 + artigo completo (≥ 1.500 palavras) + SEO checklist (densidade, links internos, alt text)
- ✅ Compliance: claims baseados em fonte verificada (cita fonte explícita)

**Como saber se está certo:** se o output pula meta tags ou SEO checklist → command rodou inline em vez de dispatchar.

---

### Test 13 — Slash command direto: `/criar-clone`

**Briefing:**
```
/criar-clone Russell Brunson (slug: brunson)
```

**Esperado:**
- ✅ Dispatch sequencial: `mos-research` (web research do expert + frameworks + cases) → `mos-copy` (gera os 4 arquivos em `assets/clones/brunson/`)
- ✅ 4 arquivos criados:
  - `profile.md` (bio, posicionamento, audiência)
  - `voice.md` (tom, ritmo, vocabulário, regras)
  - `frameworks.md` (Hook-Story-Offer, Perfect Webinar, etc.)
  - `examples.md` (sales letters, scripts, posts reais)
- ✅ Total ~700 linhas de conteúdo (não placeholders)
- ✅ `assets/clones/clone-manifest.yaml` atualizado com a nova entrada

**Como saber se está certo:** rode `ls assets/clones/brunson/` — se faltar algum dos 4 arquivos ou o manifest não estiver atualizado → command rodou parcialmente.

---

### Test 14 — Workflow multi-fase: `/campanha lancamento`

**Briefing:**
```
/campanha lancamento --produto='Curso de IA' --clone=brunson --ticket=997
```

**Esperado:**
- ✅ Dispatch multi-fase orquestrado:
  - **Fase 1 (paralelo):** `mos-research` (mercado + concorrência) + `mos-launch` (estrutura de lançamento) + `mos-funnel` (TOFU/MOFU/BOFU)
  - **Fase 2 (paralelo):** `mos-copy` (sales page + emails) + `mos-storytelling` (big idea + arco) + `mos-social` (aquecimento) + `mos-email` (sequência de lançamento)
  - **Fase 3 (sequencial):** `mos-design` (visual stack) → `mos-ads` (campanhas pagas) → `mos-analytics` (KPIs + funil de medição)
- ✅ Output consolidado:
  - Cronograma completo (aquecimento → lançamento → fechamento)
  - Checklist de Lançamento por fase
  - KPIs por etapa
  - Sequência de emails (≥ 7 emails)
  - Posts de aquecimento (≥ 5)
  - Briefing de criativos pagos
- ✅ Voice clone Brunson aplicado em copy + emails (lê `assets/clones/brunson/`)

**Como saber se está certo:** se o output só faz Fase 1 e para → orquestrador não seguiu o workflow multi-fase. Se a copy não soa Brunson → voice clone não foi carregado.

---

### Test 15 — Roteador multi-paralelo: `/batch`

**Briefing:**
```
/batch 10 posts sobre 'IA aplicada a marketing' Instagram
```

**Esperado:**
- ✅ Dispatch multi-paralelo: 10x `mos-social` em chunks de 3-5 paralelos (cada chunk em single message com múltiplas Agent calls)
- ✅ Cada peça com hook, angle e framework diferente da rotação interna do `mos-social`
- ✅ Output com estatísticas de diversidade no topo:
  - Hooks únicos: 10/10
  - Angles únicos: ≥ 8/10
  - Frameworks usados (lista)
- ✅ Cada post com: hook + corpo + CTA + caption + hashtags + sugestão de enquete obrigatória

**Como saber se está certo:** se 3+ posts repetem o mesmo hook/angle → rotação não aplicada. Se rodou tudo sequencial em vez de paralelo → ineficiência (mas funcional).

---

## Checklist de validação completa

Marque cada um após rodar:

- [ ] Test 1: dispatch simples (mos-copy)
- [ ] Test 2: dispatch paralelo (3 agents)
- [ ] Test 3: workflow #5 (página)
- [ ] Test 4: workflow #8 (carrossel)
- [ ] Test 5: workflow #9 (VSL)
- [ ] Test 6: protocolo de briefing vago
- [ ] Test 7: memory persistente
- [ ] Test 8: compliance regulatório (saúde + finanças)
- [ ] Test 9: voice clone (Halbert)
- [ ] Test 10: skill collision com frontend-design
- [ ] Test 11: `/criar-anuncio` → mos-ads
- [ ] Test 12: `/criar-artigo` → mos-research → mos-seo → mos-copy
- [ ] Test 13: `/criar-clone` → mos-research → mos-copy (4 arquivos)
- [ ] Test 14: `/campanha lancamento` → workflow multi-fase
- [ ] Test 15: `/batch` → multi-paralelo com rotação

Se 13+ passam: orquestração está saudável.
Se <12 passam: abrir issue com casos que falharam.

## Conhecidos limites

- **34 dos 38 slash commands dispatcham `mos-*` diretamente** (padrão dispatch-based desde a v6.5.0). Os 4 utilities intencionais sem dispatch são `/publicar-notion`, `/campanha` (índice), `/projeto` e `/datas-sazonais`; a lista canônica é o set `UTILITY_COMMANDS` em `scripts/tests/test_commands_dispatch.py`.
- **Validação estática automatizada:** rodar `python -m pytest scripts/tests/test_commands_dispatch.py -v` valida estrutura de dispatch de todos os commands em CI sem precisar Claude Code interativo (test cases parametrizados por arquivo, cobrem commands novos automaticamente).
- **Tier 2 smoke tests deferred:** rodar localmente com `python -m pytest scripts/tests/test_agents_smoke.py -v -m smoke` se quiser cobertura mais profunda (precisa Claude Code rodando).
