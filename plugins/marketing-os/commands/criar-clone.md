---
description: Create a complete expert clone (profile/voice/frameworks/examples) via dispatch, mos-research busca a base factual, mos-copy gera os 4 arquivos no padrão dos clones existentes em assets/clones/.
argument-hint: "<expert-name> [specialty]"
---

# /criar-clone: Clone de Expert Externo (Workflow estruturado, dispatch real)

Cria clone de copywriter / autoridade externa pesquisando via web e gerando os 4 arquivos canônicos em `assets/clones/{slug}/`. Estrutura em fases, mas execução **toda via dispatch** (não inline).

> **Diferença de `/criar-meu-clone`**: este pesquisa expert externo via web (Halbert, Hopkins, Hormozi, etc.). O outro analisa amostras LOCAIS do usuário.

## Required inputs (ask if missing)

1. **Expert name** (obrigatório): nome completo (ex: "Gary Vaynerchuk", "Seth Godin")
2. **Slug** (obrigatório): identificador curto kebab-case (ex: "gary-vee", "seth-godin"). Se não fornecido, derivar do nome.
3. **Specialty** (opcional): área primária. Se não fornecido, deixar `mos-research` determinar.
4. **Niches** (opcional): ex: "marketing-digital, empreendedorismo"
5. **Tone** (opcional): tom dominante de voz. Se não fornecido, sai da pesquisa.

## Pre-flight check (orquestrador inline)

Antes de dispatchar:

1. Verificar que `assets/clones/{slug}/` NÃO existe. Se existir, perguntar ao user: overwrite ou abortar.
2. Verificar que `assets/clones/clone-manifest.yaml` existe.
3. Listar 2-3 clones existentes (`assets/clones/hormozi/`, etc.) como referência de padrão.

## Phase 1: Research (Dispatch, mos-research)

```
Agent(subagent_type: "mos-research", prompt: "Pesquisa profunda sobre o expert [Nome completo]. Use WebSearch em múltiplas queries: '\"[nome]\" filosofia frameworks methodology', '\"[nome]\" writing style voice', '\"[nome]\" books career biography', '\"[nome]\" content examples copy', '\"[nome]\" frameworks proprietários', '\"[nome]\" famous quotes phrases'.

Retorne brief estruturado nas 7 categorias canônicas dos clones:
1. Identidade, nome, empresa(s), papel atual, livros, reconhecimento público (com números quando possível)
2. Filosofia, central + 3-5 princípios fundamentais com exemplos concretos
3. Trajetória, narrativa de carreira + marcos com datas
4. Audiência típica, 4-6 segmentos
5. Voz, tom, padrões de linguagem, vocabulário típico, palavras que ele NUNCA usa, tom por contexto (sales/landing/ad/video/post)
6. Frameworks, 4-6 frameworks proprietários (apenas REAIS, não inventar) com componentes e como aplicar
7. Exemplos de estilo, padrões de copy de venda, ad, email, post LinkedIn

REGRA CRÍTICA: apenas informação verificada. Não inventar frameworks, quotes ou conquistas. Marcar incertezas como [VERIFICAR]. Considere memory existente do cliente neste projeto."
)
  → Aguarde brief de research
```

`mos-research` tem memory project, cita explicitamente.

## Phase 2: Geração dos 4 arquivos (Dispatch, mos-copy)

Com o brief em mãos, dispatcha `mos-copy` para gerar os 4 arquivos seguindo o padrão dos clones existentes.

```
Agent(subagent_type: "mos-copy", prompt: "Gere os 4 arquivos canônicos do clone de [Nome] em assets/clones/{slug}/ usando este research como única fonte factual: [colar brief inteiro do mos-research].

Padrão de referência: clones já existentes em assets/clones/ (ex: hormozi/, halbert/, hopkins/). Você já conhece o schema dos 4 arquivos via knowledge base do agent. Resumo dos targets:

1. profile.md (~100 linhas), Identidade, Filosofia Central + Princípios Fundamentais (5), Trajetória + Marcos, Audiência Típica, Estilo de Comunicação (tabela), Diferenciação (5), Quando Usar Este Clone (tabela com Excelente/Muito bom/Não recomendado), Tópicos de Domínio (8)

2. voice.md (~190 linhas), Visão Geral, 5 Características Fundamentais (cada uma com 'Não faça / Faça' OU exemplos concretos), Estrutura Narrativa (padrão principal + secundário), Vocabulário Típico (tabela de categorias + tabela de palavras NUNCA usadas com motivo), Tom por Tipo de Conteúdo (sales/landing/ad/video/post), Regras de Formatação (6), Exemplos de Adaptação de Tom (formal vs estilo dele, motivacional vazio vs estilo dele), Checklist de Voz (8 items)

3. frameworks.md (~200 linhas), 4-6 frameworks REAIS do expert. Cada um: descrição (1-2 frases), Componentes (tabela), Aplicação na Copy (passo a passo), exemplos. Tabela-resumo no final ('Use quando...'). NÃO INVENTAR frameworks.

4. examples.md (~200 linhas), 4 exemplos completos (não snippets) na voz autêntica do expert: Copy de Vendas, Anúncio para Redes Sociais, Email de Vendas (com subject + body + P.S.), Post LinkedIn. Cada exemplo seguido de tabela 'Análise: Elemento | Técnica Aplicada'. Vocabulário e frameworks devem ser os mesmos do voice.md/frameworks.md.

REGRAS:
- Tudo em PT-BR com acentuação correta
- Aplicar quality gates globais (sem '—', sem 'brutal', sem CAPS, sem aspas em falas, máx 1-2 emojis)
- Apenas info do research, se algo está [VERIFICAR], suavizar ou omitir
- Salvar via Write em: assets/clones/{slug}/profile.md, voice.md, frameworks.md, examples.md
- Total alvo: ~700 linhas nos 4 arquivos somados

Considere memory existente do cliente neste projeto."
)
  → Aguarde criação dos 4 arquivos
```

`mos-copy` tem memory project, cita explicitamente.

## Phase 3: Update do manifest (orquestrador inline)

Append entry em `assets/clones/clone-manifest.yaml`, na seção `clones:` (ANTES de `matching_rules:`), seguindo o formato dos existentes:

```yaml
  {slug}:
    name: "{Nome completo}"
    specialty: "{Specialty (do research ou do user)}"
    best_for: ["{tipo1}", "{tipo2}", "{tipo3}", "{tipo4}"]
    niches: ["{niche1}", "{niche2}", "{niche3}"]
    tone: "{descrição de tom em PT-BR}"
    path: "{slug}/"
```

## Phase 4: Validação (orquestrador inline)

Verifique:

- [ ] `profile.md` tem 8 seções (Identidade, Filosofia, Trajetória, Audiência, Estilo, Diferenciação, Quando Usar, Tópicos)
- [ ] `voice.md` tem 8 seções (Visão Geral, Características, Estrutura, Vocabulário, Tom por Tipo, Regras, Adaptação, Checklist)
- [ ] `frameworks.md` tem 4-6 frameworks + tabela-resumo
- [ ] `examples.md` tem 4 exemplos + tabelas de análise
- [ ] Manifest atualizado com nova entrada
- [ ] Tudo em PT-BR com acentuação
- [ ] Nenhuma informação não verificada (cruzar com brief do mos-research)
- [ ] Total ~700 linhas somando os 4 arquivos

Reporte falhas específicas se algo faltar e dispatcha `mos-copy` de novo pra correção pontual.

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Sem `—`, sem "brutal", sem CAPS gratuito, sem aspas em falas (escrever direto)
- Acentuação PT-BR correta em tudo
- Compliance: se o expert atua em saúde/finanças/suplementos, exemplos de copy precisam respeitar disclaimers do nicho
- Fact-check: qualquer claim citável (livros, prêmios, números de empresa) precisa estar CONFIRMADO via 2+ fontes ou marcado [VERIFICAR]

## Final output

Após completar, mostre:

```
Clone criado: [Nome do expert]

Arquivos gerados:
  assets/clones/{slug}/
  ├── profile.md    ([N] linhas)
  ├── voice.md      ([N] linhas)
  ├── frameworks.md ([N] linhas)
  └── examples.md   ([N] linhas)

Total: [N] linhas
Manifest atualizado: clone-manifest.yaml

Pra usar: 'gere copy no estilo {slug}' ou 'estilo [Nome]' em qualquer chamada que envolva mos-copy.
```

Pergunte se quer:
1. Revisar/ajustar arquivo específico
2. Adicionar mais frameworks ou exemplos
3. Criar outro clone
4. Testar o clone com peça de exemplo

## Por que esse workflow estruturado (e não dispatch simples)

Clone de expert é peça de longa duração que vai ser consultada por anos pelo `mos-copy`. Pular a fase de research = clone com info inventada (falha em compliance e em qualidade). Pular a separação research → geração = `mos-copy` chuta detalhes biográficos e mistura mestres. Os 4 arquivos têm schemas distintos que o `mos-copy` já conhece via Tier 2, por isso não precisam de templates inline aqui.
