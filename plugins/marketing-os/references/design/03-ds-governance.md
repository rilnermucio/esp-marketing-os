# 03. Design System Governance (2026)

> Parte da stack de companions do `design-agent` (v4.0).
> Referência aplicada sobre governance de design systems: versionamento, RFCs, contribuição, deprecation, release cadence e métricas de saúde.

**Quando consultar:** ao estruturar o modelo de governo de um DS novo, ao definir processo de RFC para componentes propostos, ao criar deprecation policy, ao decidir release cadence, ao medir saúde/adoção do sistema, ao abrir contribuição externa, ou ao diagnosticar DS que cresceu sem regras e virou inconsistente.

**Pré-requisitos:** leitura prévia de `references/design/01-tokens-w3c-spec.md` (tokens) e `references/design/02-atomic-design-playbook.md` (níveis de componentes). Governance opera sobre esses artefatos.

---

## Índice

1. Por que governance importa
2. Semver aplicado a DS
3. RFC process
4. Modelo de contribuição
5. Design review rituals
6. Deprecation policy
7. Breaking changes
8. Release cadence
9. Metrics
10. Contribution checklist
11. Roadmap e backlog
12. Governance comms
13. External contributions
14. Case studies (Carbon, Polaris, Lightning)

---

## 1. Por que governance importa

Um DS sem governance vira um repositório de componentes. Dois times adicionam o mesmo botão com especificações diferentes. Um token é renomeado sem aviso e quebra 42 telas em produção. Em seis meses, o DS vira o oposto do que era para ser: fonte de divergência no lugar de fonte única de verdade.

Governance é o conjunto de regras, papéis e rituais que mantêm o DS coerente conforme ele cresce. Não é burocracia por burocracia, é a cola que permite contribuição plural sem virar anarquia.

### 1.1. Falhas históricas de DS sem governance

Quatro padrões recorrentes (observados em múltiplas empresas, alguns públicos, outros anonimizados em relatos de consultoria).

**Padrão A, o DS fantasma.** Time de plataforma lança o DS em evento interno, publica Figma, sobe pacote npm. Seis meses depois, auditoria revela que 70% dos produtos continuam com código legado. Causa raiz: não houve plano de adoção gradual, nem métricas, nem support SLA. O DS existe no papel, não na prática.

**Padrão B, o DS fragmentado.** Cada squad forka o DS para customizar. Depois de um ano, há 11 variantes do Button rodando em produção, cada uma com bug fix próprio. Causa raiz: ausência de RFC process. Contribuições novas não tinham caminho formal, então squads criaram fork como workaround.

**Padrão C, o DS congelado.** Core team sobrecarregado com backlog de 180 issues. Para proteger qualidade, fecham contribuição externa. Comunidade desengaja, DS vira legado mesmo ainda sendo oficial. Causa raiz: governance não escalou com o crescimento da base.

**Padrão D, o DS com dívida oculta.** Deprecations foram anunciadas mas nunca removidas. Três gerações de Button convivem: `Button`, `ButtonV2`, `NewButton`. Ninguém sabe qual usar. Causa raiz: falta de deprecation policy com sunset definido.

Governance bem feita previne os quatro padrões.

---

## 2. Semver aplicado a DS

Semantic Versioning (MAJOR.MINOR.PATCH) foi desenhado para APIs de biblioteca. Em DS, a API pública inclui: nomes e assinaturas de componentes, props, nomes de tokens, valores visíveis (cores, spacing, radii), acessibilidade exposta (roles, aria), documentação publicada e exports do pacote.

Uma mudança é breaking quando quebra um consumidor que usava a API corretamente. A regra é conservadora, na dúvida, trate como MAJOR.

### 2.1. Quando é MAJOR

- Remover um componente do export público.
- Renomear um componente (`Dropdown` para `Select`).
- Renomear uma prop ou remover prop existente.
- Mudar o tipo de uma prop (string para enum restrito).
- Alterar o comportamento default (default `size` de `md` para `lg`).
- Remover ou renomear um token público.
- Alterar valor de token de forma visível (aumentar `spacing-4` de 16px para 20px, mesmo mantendo o nome).
- Mudar role ARIA ou estrutura semântica de um componente.
- Alterar markup interno que consumidores customizam via CSS selectors públicos.

### 2.2. Quando é MINOR

- Adicionar novo componente ao export.
- Adicionar nova variant (`variant="ghost"` em Button).
- Adicionar nova prop opcional com default backward-compatible.
- Adicionar novo token (novo tom de cinza, nova escala de radius).
- Expor novo slot em um componente composicional.
- Adicionar novas localizações internacionais.
- Adicionar novas keyboard shortcuts sem conflitar com existentes.

### 2.3. Quando é PATCH

- Corrigir bug de renderização (borda sumindo em Safari, foco invisível em Firefox).
- Ajustar valor de token por alinhamento fino (1px de spacing, decimais de rgb).
- Melhorar performance sem mudar API.
- Corrigir typo em documentação.
- Corrigir contraste de cor para atender WCAG, sem mudar nome de token (caso o nome já sinalize o uso).
- Atualizar dependências internas sem impacto externo.

### 2.4. Tabela de 20 exemplos concretos

| Mudança | Tipo | Razão |
|---|---|---|
| `Button` vira `PrimaryButton` | MAJOR | Rename público. |
| Adicionar `<Stepper>` ao sistema | MINOR | Novo componente. |
| `color-primary` muda de `#0066CC` para `#0052A3` | MAJOR | Valor visível mudou. |
| Bug: checkbox não marca com `Enter` | PATCH | Comportamento esperado restaurado. |
| Adicionar `size="xl"` em Input | MINOR | Nova variant opcional. |
| Remover `variant="ghost"` de Button | MAJOR | Remoção de API pública. |
| Token `spacing-md` renomeado para `spacing-400` | MAJOR | Rename público. |
| Adicionar novo ícone `arrow-right-bold` | MINOR | Novo export. |
| Corrigir alinhamento vertical no Badge em 1px | PATCH | Bug fix visual. |
| `Modal` passa de `role="dialog"` para `role="alertdialog"` | MAJOR | Semântica ARIA mudou. |
| Adicionar dark mode sem quebrar light | MINOR | Adição, não alteração. |
| Default de `Card` padding muda de `16px` para `24px` | MAJOR | Default mudou. |
| Adicionar prop `onValueChange` em Select | MINOR | Prop opcional nova. |
| Remover prop `theme` de Button (agora via context) | MAJOR | Remoção de prop. |
| `<Icon name="chevron-down">` vira `<ChevronDown />` | MAJOR | Pattern de uso mudou. |
| Melhorar tree-shaking reduzindo bundle em 40% | PATCH | Sem mudança de API. |
| Adicionar prop `data-testid` automaticamente | MINOR | Novo comportamento aditivo. |
| Reorganizar arquivos internos (`src/` para `dist/`) | PATCH ou MINOR | Depende de imports expostos. |
| Remover suporte a React 17 | MAJOR | Peer dependency quebrou. |
| Traduzir documentação para espanhol | PATCH | Docs, não API. |

### 2.5. Pré-MAJOR: avisando antes

MAJOR doloroso sem aviso destrói confiança. Padrão recomendado:

1. Lançar nova API como MINOR adjacente (novo nome coexiste com antigo).
2. Deprecation warning no console do antigo.
3. Migration guide publicado, codemod disponível se possível.
4. Janela de 2 a 3 MAJORs (6 a 9 meses) para consumidores migrarem.
5. Remoção acontece no MAJOR planejado, comunicada com 30 dias de antecedência.

Detalhes em seção 6 (Deprecation policy).

---

## 3. RFC process

RFC (Request for Comments) é o documento formal que propõe uma mudança significativa no DS, novo componente, variant importante, redesign de token, mudança de convenção. Sem RFC, mudanças grandes viram discussão em canal de Slack e se perdem.

### 3.1. Quando abrir RFC

Sempre que a mudança afete mais de um time consumidor, envolva MAJOR em potencial, crie novo componente no catálogo oficial, mude padrão transversal (naming, tokens, a11y), ou custe mais de 1 semana de core team para implementar. Mudanças triviais (bug fix, copy) vão direto pra PR.

### 3.2. Template completo (inline)

```markdown
# RFC-{NNNN}: {Título conciso}

- **Autor:** {Nome + squad}
- **Data:** {YYYY-MM-DD}
- **Status:** Draft | Review | Approved | Rejected | Deferred
- **Deciders:** {Core team names ou role}
- **Tags:** {component, token, a11y, migration, etc}

## Proposal
Resumo de 3 frases. O leitor entende o que e por que sem ler o resto.

## Problem
Qual problema concreto isso resolve? Quem sente essa dor? Quantos times? Traga dados (ex: "12 squads reportaram necessidade de Stepper nos últimos 4 meses; 3 já forkaram").

## Solution
Descrição técnica: nome e hierarquia (Atomic Design level), props/variants/estados, tokens envolvidos, comportamento em mobile/keyboard/screen reader, mock Figma, exemplos de uso em 2 a 3 produtos reais.

## Alternatives
Outras abordagens consideradas e razões de rejeição (ex: "Material UI Stepper rejeitado por bundle +12kb e a11y inconsistente").

## Impact
Consumidores afetados (squads, telas), breaking changes, bundle size, acessibilidade (WCAG AA/AAA), performance, i18n/RTL.

## Migration
Se houver substituição: codemod disponível (s/n), timeline sugerida, link para migration guide.

## Success Metrics
Adoption em 90 dias, redução de forks, zero imports da versão antiga em 6 meses.

## Timeline
Semanas 1 a 2 (review), 3 a 4 (implementação), 5 (QA), 6 (RC), 7 (release).

## Open questions
Dúvidas abertas que precisam discussão em review.

## Related
Links para RFCs anteriores, issues, discussões.
```

### 3.3. Quem escreve, quem aprova

- **Escreve:** qualquer contribuidor (interno ou externo), de qualquer squad. Templates e exemplos em `rfcs/` do repositório. Autor do RFC é o owner do documento até ser aprovado/rejeitado.
- **Revisa:** core team (design + engineering + a11y, mínimo 3 reviewers). Revisores comentam inline, sugerem alternativas, pedem esclarecimentos.
- **Aprova:** maintainer designado (ou comitê em casos de alto impacto). Aprovação exige quórum de 2 de 3 reviewers + ausência de vetos justificados.
- **Veta:** qualquer maintainer pode vetar com razão técnica documentada (não "não gostei", precisa ser concreto: "quebra a11y", "conflita com RFC-0042", "custo de manutenção não justificado").

### 3.4. SLA

- Primeiro feedback do core team em até **5 dias úteis** após abertura.
- Decisão final (approve/reject/defer) em até **15 dias úteis** após RFC entrar em status Review.
- Deferral: RFC não rejeitado, mas adiado por priorização. Volta ao backlog, reavaliado no próximo planning trimestral.

### 3.5. Status válidos

- **Draft:** autor ainda está refinando, não pronto para revisão.
- **Review:** aberto para comentários públicos.
- **Approved:** aprovado, entra no roadmap de implementação.
- **Rejected:** rejeitado com razão documentada. RFC rejeitado não some, fica no histórico para evitar repetição.
- **Deferred:** adiado, sem rejeição explícita.
- **Withdrawn:** autor retirou (mudança de prioridade, solução alternativa encontrada).

---

## 4. Modelo de contribuição

DS maduros operam com **core team + community**. Core team protege qualidade e direção. Community amplia capacidade e mantém o DS conectado à realidade dos produtos.

### 4.1. Roles e permissões

| Role | Quem | Pode | Não pode |
|---|---|---|---|
| **Maintainer** | Core team (4 a 8 pessoas) | Merge direto, aprovar RFCs, publicar releases, definir roadmap | Bypass do processo de RFC para mudanças MAJOR |
| **Reviewer** | Seniors designados (interno ou community) | Revisar PRs, aprovar (2 approvals = merge), comentar RFCs | Merge próprio, publicar release |
| **Contributor** | Qualquer funcionário com acesso ao repo | Abrir RFC, enviar PR, reportar issue, propor tokens | Aprovar, publicar |
| **Designer** | Designers de produto | Propor variants via Figma + RFC, participar de design review | Commitar código sem pair |
| **User** | Consumidor do DS | Reportar bugs, sugerir melhorias, participar de office hours | Modificar diretamente |

### 4.2. Caminho de progressão

`User -> Contributor -> Reviewer -> Maintainer`. Promoção baseada em track record: quantidade e qualidade de contribuições, consistência em reviews, alinhamento com princípios do DS. Processo documentado, não arbitrário.

### 4.3. Core team, composição ideal

Para DS de ~50 componentes atendendo 5 a 20 produtos:

- 1 Tech Lead (engenheiro senior, ownership técnico)
- 1 Design Lead (designer senior, ownership visual e UX)
- 2 a 3 Engenheiros (full-stack ou front-end focados)
- 1 a 2 Designers de sistema
- 1 especialista em a11y (pode ser part-time ou consultoria)
- 1 advocate/DX (documentação, suporte, onboarding)

Total: 6 a 10 pessoas dedicadas. Abaixo disso, o sistema sofre com backlog infinito. Acima de 15, a coordenação interna vira overhead.

### 4.4. Community contribution flow

```
1. User identifica gap ou bug
2. Busca em issues/RFCs se já existe
3. Abre issue ou RFC (depende da escala)
4. Core team triages em até 3 dias úteis
5. Label: accepted | needs-info | wontfix | duplicate
6. Se accepted, entra no backlog priorizado
7. Contributor pode assumir implementação ou aguardar core team
8. PR passa por review (2 approvals + CI verde)
9. Merge -> entra no próximo release
```

---

## 5. Design review rituals

Rituais regulares que mantêm o DS vivo e conectado aos times.

### 5.1. Weekly sync (core team, 45 min)

Agenda: 5 min status de releases, 10 min triagem de RFCs novos, 15 min deep dive em 1 tópico técnico (rotativo: a11y, tokens, perf, docs), 10 min issues bloqueantes de squads, 5 min prioridades. Output: notas no canal público, decisões tagged.

### 5.2. Biweekly design review (aberto, 60 min)

Participantes: core team + designers de squads convidados. Agenda: 10 min updates de core team, 30 min em 2 a 3 propostas de design (15 min cada), 15 min padrões emergentes, 5 min Q&A. Output: feedback estruturado em cada RFC.

### 5.3. Monthly showcase (aberto a toda org, 45 min)

Agenda: 10 min release notes do mês, 20 min em 2 a 3 squads apresentando casos de uso, 10 min roadmap próximo mês, 5 min convite para contribuição. Output: gravação publicada + recap no email digest.

### 5.4. Quarterly roadmap review (2h)

Participantes: core team + heads de eng/design + PMs. Agenda: 30 min métricas do trimestre, 30 min retrospectiva, 45 min proposta do próximo trimestre, 15 min compromissos e riscos. Output: roadmap público atualizado.

### 5.5. Office hours (suporte aberto)

2x/semana, 1h cada, formato drop-in. Cobertura: 1 engenheiro + 1 designer do core em escala rotativa. Tema: dúvidas de uso, diagnóstico, review de código, onboarding. Objetivo: reduzir custo de adoção e capturar sinais de dor cedo.

---

## 6. Deprecation policy

Deprecation sem policy é sinônimo de dívida técnica perpétua. Policy eficaz define timeline, comunicação e enforcement.

### 6.1. Timeline padrão (6 meses)

```
Mês 0: Deprecation anunciada
  - Release notes com warning
  - Migration guide publicado
  - Console warning no componente
  - Codemod disponível (quando aplicável)

Mês 1 a 3: Grace period
  - Comunicação mensal em release notes
  - Suporte ativo para migração
  - Métricas: quantos squads ainda usam versão antiga?

Mês 4: Last call
  - Email direto para squads ainda não migrados
  - Warning escalado (console.error em dev)
  - Office hours focadas em migração

Mês 5: Freeze
  - Versão antiga não recebe mais bug fixes (só security)
  - Lint rule bloqueia novos usos em CI

Mês 6: Remoção
  - Componente removido no próximo MAJOR
  - Release notes destacam remoção
  - Migration guide arquivado (fica acessível, mas sinalizado como histórico)
```

Timeline padrão é 6 meses. Pode ser estendida para 9 ou 12 em componentes críticos de alto uso, ou reduzida para 3 em betas/experimentais nunca oficializados. Nunca menor que 3 meses para componentes oficiais.

### 6.2. Cadência de comunicação

| Fase | Canal | Frequência |
|---|---|---|
| Anúncio inicial | Release notes + email + Slack | 1x (M0) |
| Recall | Release notes | Todo release (M1 a M5) |
| Email direto para squads | Email (owner técnico do squad) | M1, M3, M4 |
| Warning escalado | Console do navegador (dev) | Contínuo a partir de M0 |
| Last call | Email + Slack + reunião opcional | M4 |

### 6.3. Migration guide (template)

```markdown
# Migration guide: {ComponentOld} -> {ComponentNew}

## Por que a mudança
Contexto em 2 frases.

## Diff resumido
Tabela antes/depois com 5 a 8 exemplos de uso.

## Passo a passo
1. Instalar nova versão.
2. Rodar codemod (se disponível): `npx @ds/codemod v2-migrate`
3. Atualizar imports manualmente onde o codemod não cobre.
4. Revisar CSS custom que usa seletores internos (lista).
5. Rodar testes visuais.

## Casos especiais
- Se você usa prop X, migração é direta.
- Se você sobrescreve estilos via Y, veja seção.

## Suporte
- Office hours: link
- Slack: #ds-migration
- Issue tracker: label "migration-help"
```

---

## 7. Breaking changes

Breaking change é todo change que quebra consumidor. Detecção e comunicação precisam ser sistemáticas.

### 7.1. Detecção automática

- **API diff:** ferramentas como `@microsoft/api-extractor` ou `api-extractor-lite` geram snapshot da API pública. CI compara e bloqueia merge se houver diff não documentado em changelog.
- **Visual regression:** Chromatic, Percy ou Loki. PR roda snapshot de cada componente, comparado contra baseline. Diff visual flagado para review manual.
- **Type checking:** se DS é TypeScript, CI roda `tsc --noEmit` contra fixtures que importam publicamente. Falha se tipo mudou.
- **Contract tests:** tests específicos que importam como consumidor ("integration tests em miniatura"). Quebra se API quebra.
- **Changelog lint:** CI obriga entrada em CHANGELOG por PR que mexa em export público.

### 7.2. Canais de comunicação

| Canal | Quando | Responsável |
|---|---|---|
| Release notes (GitHub + site) | Todo release | Core team |
| Email digest (quinzenal) | Releases da quinzena | Advocate/DX |
| Slack #ds-announcements | Releases MAJOR e features importantes | Tech Lead |
| Email direto para techlead de squad | Breaking change MAJOR + deprecation | Advocate/DX |
| Blog post | MAJORs grandes, redesigns | Design Lead + Tech Lead |
| Office hours | Sempre | Rotativo |

### 7.3. Rollback plan

Cada release MAJOR deve ter rollback plan documentado antes do release, não depois.

```markdown
# Rollback plan: v{N}.0.0

## Critérios para rollback
- P95 de erros no bundle cresce >10% em 24h
- >5 squads reportam regressão crítica
- Breaking change não documentado é descoberto

## Procedimento
1. Tech Lead declara rollback no canal público
2. Publicar tag `v{N-1}.X.Y-rollback` como release recomendado
3. Republish do pacote npm com tag `latest` apontando para versão anterior
4. Comunicado: email + Slack + release notes
5. Post-mortem agendado em até 72h

## Pré-condição
Versão anterior testada como rollback target antes do MAJOR ser lançado.
```

### 7.4. Semver pre-release tags

Para validar MAJORs em produção antes do cut final, usar tags pre-release:

- `v2.0.0-alpha.1` - primeiras versões instáveis, só para early adopters
- `v2.0.0-beta.1` - API estável, documentação em andamento
- `v2.0.0-rc.1` - release candidate, bug fixes apenas
- `v2.0.0` - release oficial

Tempo mínimo entre RC e oficial: 2 semanas (DS pequeno) a 6 semanas (DS grande).

---

## 8. Release cadence

Quatro modelos, escolha depende de maturidade, tamanho do core team e necessidade dos consumidores.

- **Weekly:** feedback rápido e momentum, mas overhead alto (changelog, QA, comms). Usar em DS early-stage (<1 ano) com core team >=6 FTE e alta demanda de fixes.
- **Monthly:** equilíbrio clássico entre cadência e overhead. Bug fix crítico sai como patch fora de banda. Usar em DS maduro, 20 a 100 componentes, 5 a 30 produtos, core team 4 a 8 FTE.
- **Every 3 weeks (ritmo Carbon):** sweet spot entre weekly e monthly, exige disciplina de schedule. Usar em DS grande (>=100 componentes), core team >=8 FTE, adoção em org grande.
- **On-demand:** sem overhead fixo, releases "cheios". Imprevisibilidade é o trade-off. Usar em DS early-stage sem time dedicado full-time ou open source com commit voluntário.

### 8.5. Trade-offs resumidos

| Dimensão | Weekly | Monthly | 3-weekly | On-demand |
|---|---|---|---|---|
| Previsibilidade | alta | alta | alta | baixa |
| Overhead | alto | médio | médio | baixo |
| Momentum | alto | médio | médio-alto | baixo |
| Absorção por consumidor | difícil | fácil | equilibrado | variável |

Recomendação para DS típico (10 a 50 componentes, 5 a 20 produtos): **monthly ou a cada 3 semanas** para MINOR/MAJOR, **patches on-demand** para fixes críticos.

---

## 9. Metrics

Sem métricas, governance é opinião. Cinco métricas essenciais.

### 9.1. Adoption rate

% de produtos/squads que usam o DS vs total que deveria usar. Medir via scan automatizado de imports (`import from "@org/ds"`), telemetria opcional em componentes, survey quadrimestral com techleads. **Benchmark:** 80%+ em 18 meses após lançamento; 95%+ em DS maduro (>3 anos).

### 9.2. Consistency score

% de UI usando tokens vs hard-coded. Medir via linter que flagga hex, rgb, px literais; análise estática em CI dos produtos; relatório mensal de "hex count" por produto. **Benchmark:** <5% hard-coded em produtos maduros; tolerância de até 15% em migração.

### 9.3. Token compliance

Subconjunto de consistency score, foca em tokens específicos. Separar por categoria (`color-compliance`, `spacing-compliance`, `typography-compliance`), dashboard por produto com atualização semanal. **Benchmark:** cada categoria >=90%.

### 9.4. Debt tracker

Inventário de dívidas conhecidas (deprecations não migradas, forks ativos, bugs de longa data). Tabela pública com item, owner, impacto, prazo. Revisada em weekly sync. **Benchmark:** nenhuma dívida high por >90 dias; nenhuma med por >180 dias.

### 9.5. Feedback volume

Número e qualidade de interações (issues, RFCs, reviews, office hours). Medir via issue tracker analytics + NPS quadrimestral. **Benchmark:** 5 a 15 novas issues/semana, 2 a 5 RFCs ativos, NPS >=40 entre techleads.

### 9.6. Dashboard público

Combinar as 5 métricas em dashboard acessível a toda org, atualização semanal automatizada.

```
[Adoption: 87%] [Consistency: 94%] [Token compliance: 91%]
[Debt items: 12] [Open RFCs: 4] [NPS: 48]

Últimos releases
- v2.5.0, há 3 dias, 0 rollbacks
- v2.4.2, há 17 dias, 1 hotfix

Top 3 dívidas
1. Migração Button v1->v2 (62%, prazo M+2)
2. Deprecated Modal prop "title" (84%, M+1)
3. Fork do Dropdown no squad Billing (owner: @foo)
```

---

## 10. Contribution checklist

Toda contribuição (nova feature, bug fix, mudança) deve passar por checklist antes do merge.

### 10.1. Técnico
- [ ] Test coverage: unitários cobrem >80% do diff
- [ ] Test visual: snapshot atualizado e revisado
- [ ] Lint, Types: CI sem warnings, TS/Flow limpos
- [ ] Bundle size: impacto documentado (+/- kb); acima de threshold exige RFC

### 10.2. Documentação
- [ ] Props: JSDoc em cada prop pública
- [ ] Storybook: história com casos principais
- [ ] Migration guide: atualizado se aplicável
- [ ] Docs site: página do componente com novos exemplos

### 10.3. A11y
- [ ] Keyboard: navegação testada (Tab, Shift+Tab, Enter, Space, Escape, Arrow keys)
- [ ] Screen reader: NVDA ou VoiceOver, labels corretos
- [ ] Contraste: WCAG AA (4.5:1 texto, 3:1 elementos grandes)
- [ ] Focus visible: outline presente, respeita `prefers-reduced-motion`
- [ ] ARIA: roles e states apropriados, sem redundância com semantics nativo

### 10.4. Aprovações
- [ ] 2 approvals mínimo (1 designer + 1 engineer do core)
- [ ] Label: `approved-design`, `approved-eng`, `approved-a11y`
- [ ] CodeRabbit/SonarQube: sem issues HIGH/CRITICAL
- [ ] Changelog entry adicionada
- [ ] Figma atualizado (arquivo mestre reflete código)
- [ ] Tag correta no PR: `patch`/`minor`/`major`

### 10.5. Migração (se breaking)
- [ ] Migration guide escrito
- [ ] Codemod disponível (ou justificativa)
- [ ] Deprecation warning na versão anterior
- [ ] Comunicação planejada (email, Slack, release notes)
- [ ] Timeline comunicada aos squads impactados

---

## 11. Roadmap e backlog

Roadmap é o compromisso público do que vem pela frente. Backlog é o inventário do que está sendo considerado mas ainda não priorizado.

### 11.1. Template de roadmap trimestral

```markdown
# DS Roadmap {Q{N}} {Ano}

## Theme do trimestre
{1 frase de direção estratégica, ex: "Preparar base para dark mode em Q4"}

## Committed (vamos entregar)
1. Componente Stepper (RFC-042) - release v3.2 (M2)
2. Redesign de tokens de typography (RFC-039) - release v4.0 (M3)
3. Codemod para migração Button v1->v2 - release v3.1 (M1)

## In progress (RFC em andamento)
- RFC-044: Sistema de Toasts unificado
- RFC-045: Nova família de tokens para motion

## Under consideration (backlog priorizado)
- Componente DatePicker rewrite
- Biblioteca de ícones v3
- Suporte a RTL em Table

## Deferred (não entra este trimestre)
- Redesign completo do Navigation
- Migração para Web Components
```

Roadmap público, atualizado mensalmente (ou ao fim de cada sprint). Qualquer pessoa da org pode ler. Qualquer squad pode comentar.

### 11.2. Priorização RICE

Cada item do backlog recebe score RICE:

- **R**each: quantos squads/produtos se beneficiam
- **I**mpact: tamanho do benefício (1 = baixo, 3 = alto)
- **C**onfidence: certeza sobre impact e reach (0.5 a 1.0)
- **E**ffort: esforço em FTE-semanas

**Score:** `(Reach * Impact * Confidence) / Effort`

Ranking do backlog por score. Itens acima de X entram no Committed do trimestre.

### 11.3. Priorização WSJF (alternativa SAFe)

Weighted Shortest Job First, útil em contextos com múltiplas unidades de negócio:

- **CoD (Cost of Delay):** business value + time criticality + risk reduction
- **Job size:** esforço em story points ou semanas

**Score:** `CoD / Job size`

WSJF é mais usado em orgs grandes com tradição em SAFe. RICE tende a ser suficiente para DS médio.

### 11.4. Critérios de corte

Nem tudo que é proposto entra no roadmap. Critérios explícitos:

- **Alinhamento com princípios:** o item reforça o DS ou contradiz direção?
- **Demand signal:** há dor documentada ou é feature wishlist?
- **ROI:** payback em menos de 2 trimestres?
- **Risco de fragmentação:** resolve ou cria?
- **Capacidade:** cabe sem estourar bandwidth do core team?

Items rejeitados recebem justificativa pública. Não sumam silenciosamente.

---

## 12. Governance comms

Comunicação é metade da governance. Documentos perfeitos que ninguém lê não governam nada.

### 12.1. Changelog format

Seguir convenção [Keep a Changelog](https://keepachangelog.com) com adaptações.

```markdown
# Changelog

## [Unreleased]

### Added
- Novo componente Stepper (RFC-042)

### Changed
- Ajuste no spacing padrão do Card (PATCH)

### Deprecated
- `<Modal title=...>` deprecado, migrar para `<Modal.Header>`

### Removed
- Componente `SpinnerOld` (era deprecated há 9 meses)

### Fixed
- Focus não aparecia no Safari (issue #4223)

### Security
- Atualização de dependência com CVE-2026-XXXX

## [2.5.0] - 2026-04-15

...
```

### 12.2. Release notes template

```markdown
# v2.5.0 - "Stepper + tokens de motion"

Lançado em 2026-04-15.

## Highlights
- Stepper chegou (ver docs: link)
- Nova família de tokens de motion (`motion-fast`, `motion-standard`, `motion-slow`)
- Performance: bundle reduzido em 8% com tree-shaking aprimorado

## Upgrade path
Release é MINOR, não há breaking changes. `npm upgrade @org/ds@2.5.0`.

## What's new
[lista detalhada, com screenshots quando aplicável]

## Contributors
@pessoa1, @pessoa2, @pessoa3. Obrigado!
```

### 12.3. Canais de comunicação

| Canal | Propósito | Cadência |
|---|---|---|
| `#ds-announcements` | Releases, breaking changes, deprecations | Por evento |
| `#ds-dev` | Discussões técnicas do core team | Diário |
| `#ds-support` | Perguntas de consumidores | Diário (office hours) |
| `#ds-rfc` | Discussões sobre RFCs ativos | Por RFC |
| Email digest | Roundup quinzenal | 2x/mês |
| Blog | Features grandes, post-mortems | Por evento |
| Calendar público | Releases, office hours, reviews | Contínuo |

### 12.4. Email digest (template)

```
Assunto: DS digest - 2026-04-15 a 2026-04-30

Highlights
- v2.5.0 lançada com Stepper
- RFC-046 (Toasts unificados) entrou em Review, participe

Métricas do mês
- Adoption: 87% (+2% vs mês anterior)
- Open RFCs: 4
- New components released: 1

Upcoming
- v2.6.0 em 2026-05-15
- Office hours: toda terça e quinta, 14h

Contribuições em destaque
- Agradecimento a @foo pelo Migration Codemod do Button

Links úteis
- Roadmap Q2: [link]
- Métricas dashboard: [link]
- Canal Slack: [link]
```

### 12.5. Office hours (operação)

2 slots/semana de 1h, drop-in (link zoom público), escala rotativa do core. Temas mais perguntados geram FAQ. Sem gravação padrão (safe space), notas publicadas.

---

## 13. External contributions

Se o DS vira open source ou aceita contribuições de fora da empresa, governance precisa de camada extra.

### 13.1. Fork model

- Repositório principal público (GitHub/GitLab)
- Contribuições externas via fork + PR
- Proteção de branch principal (`main`): requer 2 approvals + CI verde
- Code owners automáticos (CODEOWNERS file)

### 13.2. CLA (Contributor License Agreement)

CLA define termos de propriedade intelectual. Dois padrões: **Individual CLA** (assinado por pessoa) e **Corporate CLA** (assinado pela empresa, cobre funcionários). Motivação: proteger projeto e mantenedora de disputas de IP. Ferramentas como [CLA Assistant](https://cla-assistant.io/) automatizam assinatura via PR. Modelos base: Apache ICLA, Eclipse CLA, ou custom revisado por legal.

### 13.3. Code of conduct

Obrigatório. Adotar padrão conhecido (Contributor Covenant é o de facto em open source). Definir: comportamentos esperados e inaceitáveis, como reportar violação (email, formulário), consequências graduais (warning, temporary ban, permanent ban), quem enforce (comitê rotativo de 2 a 3 pessoas).

### 13.4. Merge etiquette

Regras em PRs externos:
- **Primeiro contato em até 48h úteis** (mesmo que seja "obrigado, vamos olhar").
- **Feedback construtivo:** sugerir alternativa, não apenas apontar problema.
- **Credits:** contribuidor em changelog e release notes.
- **Não deixar PR pendurado:** silêncio é pior que rejeição educada.
- **Triage labels:** `good first issue`, `help wanted`, `needs-discussion`, `blocked`.

### 13.5. External contributor onboarding

Página dedicada (`CONTRIBUTING.md`) com: setup local, como rodar tests, estrutura do repo, convenções de código/commit, fluxo de PR, link para RFC template, canal de dúvidas, Code of Conduct. Primeiros 3 PRs de um contribuidor novo recebem atenção extra do maintainer.

---

## 14. Case studies

Três DS públicos maduros, com governance documentada. Detalhes verificados em fontes oficiais (abril 2026).

### 14.1. Carbon Design System (IBM)

Lançado pela IBM em 2016 como sistema unificado para produtos IBM. Open source desde o início.

**Governance (dois níveis):**
- **Steering committee:** Carbon practitioners da comunidade, cuidam de oversight e direção técnica.
- **Advisory board:** executivos IBM, cuidam de buy-in estratégico e alocação de recursos.
- **Core maintainers:** time fulltime (eng + design + a11y).

**Níveis de contribuição (modelo público):**
1. **Light:** pequenos tweaks de design, correções visuais.
2. **Medium:** adicionar ou mudar guidelines, contribuir ícone.
3. **Heavy:** contribuir componente inteiro.

Cada nível tem requisitos progressivos de testes, docs, review e aprovação.

**Release cadence:** releases a cada **3 semanas**, flexível conforme necessidade de adopter teams e crescimento da biblioteca. Carbon cobre React, Web Components, Angular, Vue e Svelte.

**Fontes:** [carbondesignsystem.com](https://carbondesignsystem.com) e [github.com/carbon-design-system/carbon](https://github.com/carbon-design-system/carbon).

**Lição:** o two-tier model (steering + advisory) permite decisão técnica rápida sem perder alinhamento estratégico. Níveis de contribuição com barreiras progressivas democratizam participação sem diluir qualidade.

### 14.2. Polaris (Shopify)

DS oficial do Shopify, usado no admin, checkout, customer accounts e apps. Em 2025, Shopify anunciou unificação do Polaris, agora baseada em Web Components e stable across all surfaces.

**Governance (documentada publicamente):**
- Polaris une design guidance, development opinions, code libraries e API documentation.
- Governance descrita como mecanismo para balancear estabilidade e inovação: prevenir fragmentação enquanto permite padrões emergirem via processo regularizado.
- Princípios: design tokens para estilos consistentes, component library para reuso, testes automatizados de a11y, governance model para change control.

**Integração:** padrões do Polaris expostos via MCP Server da Shopify, facilitando adoção por agentes e ferramentas. Apps que adotam Polaris herdam automaticamente updates do DS.

**Fontes:** [polaris-react.shopify.com](https://polaris-react.shopify.com) e [shopify.com/partners/blog/polaris-unified-and-for-the-web](https://www.shopify.com/partners/blog/polaris-unified-and-for-the-web).

**Lição:** governance forte permite consolidação. Polaris unificou múltiplas experiências (admin, checkout, apps) num único DS via processo maduro de change control. A aposta em Web Components reduz coupling com frameworks.

### 14.3. SLDS (Salesforce Lightning Design System)

DS oficial Salesforce desde 2015. Em Spring '25, Salesforce lançou SLDS 2. O SLDS 1 segue suportado para compatibilidade.

**Governance (público):**
- **Contributors:** criam elementos e patterns (internos ou externos).
- **Curators:** custodians do DS, mantêm e revisam propostas (equivalente a maintainer).
- **Usuários:** consumidores que dão feedback via issues e fóruns.

**Estrutura SLDS 1:** quatro elementos fundamentais: design tokens, utilities, guidelines, component blueprints. **SLDS 2 (2025)** existe paralelamente ao SLDS 1, permitindo migração gradual sem breaking change abrupto.

**Fontes:** [lightningdesignsystem.com](https://www.lightningdesignsystem.com) e [github.com/salesforce-ux/design-system](https://github.com/salesforce-ux/design-system).

**Lição:** modelo Contributors/Curators é minimalista e claro. Coexistência SLDS 1 + 2 mostra como grandes mudanças rodam em paralelo (não big-bang), preservando estabilidade dos consumidores enquanto o novo amadurece.

### 14.4. Padrões comuns aos três

Olhando Carbon, Polaris e SLDS lado a lado:

- **Separação core team + community:** os três têm time dedicado protegendo qualidade, com pathways para contribuição externa.
- **Documentação pública:** sites oficiais extensos e acessíveis.
- **Open source ou aberto:** repositórios principais públicos, PRs externos aceitos.
- **Release cadence regular:** Carbon (~3 semanas), Polaris e SLDS (ciclos de produto).
- **Tokens no centro:** todos usam tokens como camada 0 para temas, dark mode e unificação cross-surface.
- **Governance documentada:** regras, papéis e processos públicos, sem tribal knowledge.

---

## Fim do documento

Companion parte da trilogia de design systems:
- `01-tokens-w3c-spec.md` (camada 0: tokens)
- `02-atomic-design-playbook.md` (camada 1: hierarquia)
- `03-ds-governance.md` (camada 2: como o sistema evolui)

Governance separa DS vivo de DS morto. Consulte antes de: lançar publicamente, abrir contribuição distribuída, receber primeiro PR externo, planejar MAJOR, definir deprecation, abrir open source, criar RFC template, estabelecer release cadence. Em dúvida, volte aos três princípios-chave: clareza de papéis, previsibilidade de processo, comunicação constante.
