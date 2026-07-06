# Controle de custo, contexto e modelo

> Canônico. Atualizado em 2026-07-06. Snapshot de contexto: cobrança por uso passa a valer para o modelo de fronteira em jul/2026; nomes de modelos e preços envelhecem rápido, valide o estado atual antes de citar (mesma regra dos snapshot guards das KBs). Os princípios abaixo não dependem de preço.

## Princípio geral

Custo tem 3 alavancas, nesta ordem de impacto: **o que você lê** (contexto de entrada), **quem processa** (tier de modelo) e **o que você escreve** (volume de output). Otimize nessa ordem.

## 1. O que você lê (contexto)

Baseline do repo (medido 2026-07-06, referência no [ADR-0001](adr/0001-arquitetura-two-tier.md)):

| Camada | Tamanho | Quando carrega |
|---|---|---|
| Tier 1 (18 agents) | 4.411 linhas somadas (~245/agent) | Sempre que a sessão abre |
| SKILL.md | 430 linhas | Ao invocar a skill |
| Tier 2 (18 KBs) | 66.201 linhas somadas (800 a 6.529 por KB) | Sob demanda, por Read |
| Swipe-files, clones, references | variável | Sob demanda, por Read |

Regras:

- **A camada mais cara de inflar é a mais alta.** 10 linhas a mais num Tier 1 custam em toda sessão; 100 linhas numa KB custam só quando lida. Na dúvida, empurre pra baixo (H2.1).
- **Leia a PARTE, não o arquivo** (H5.2). KB tem índice pra isso; KB sem índice é bug de custo (F-COST-01).
- **Grep antes de Read** em tarefa de manutenção: localizar primeiro, ler o trecho depois.
- **Não re-derive o que a sessão já estabeleceu**: scout re-verifica estado, não re-lê tudo.

## 2. Quem processa (tier de modelo)

Vocabulário por capacidade (nomes específicos datam; capacidade não):

| Tier | Usar para | No repo hoje |
|---|---|---|
| Fronteira (Fable-class) | Arquitetura, auditoria multi-sistema, escrita de docs canônicos, decisões de trade-off, copy high-stakes com red team | Sessões de manutenção como esta; agents `model: opus` |
| Intermediário (Sonnet-class) | Produção padrão dos agents, geração com schema definido, tarefas com gates determinísticos cobrindo a saída | Maioria dos `agents/mos-*.md` |
| Leve (Haiku-class) | Classificação, extração, julgamento LLM-graded com rubrica fixa, resumo mecânico | Futuro julgador de evals (§4 da estratégia) |

Regras:

- **`model:` no frontmatter do agent é decisão de engenharia, não default.** Precedente: commit e46eeca subiu para opus só os agents de raciocínio pesado (copy, research, launch, funnel). Agent de tarefa mecânica com modelo de fronteira é F-COST-03.
- **Quanto mais determinística a validação da saída, mais leve pode ser o gerador.** O gate segura a qualidade; o modelo não precisa ser o mais caro pra errar menos onde o erro é barrado.
- **Use o modelo de fronteira pra construir alavancas, não pra operar manivelas**: uma sessão cara que produz heurística/guard/eval paga por muitas sessões baratas futuras. É a razão de existir desta pasta.

## 3. O que você escreve (output)

- **Gere 5-10, entregue top 2-3** com justificativa (H5.4). Volume interno de iteração não vai pro output.
- **Red team e processo pesado só em peça high-stakes** (F-COST-02). O trigger está definido no próprio mos-copy; replicar o padrão ao dar red team a outros agents.
- **Sem eco de briefing** no output; schema enxuto; tabela só para fato enumerável.
- **Em manutenção**: relatório denso no final da rodada em vez de narração passo a passo.

## 4. Determinístico antes de modelo

Se um script resolve, o modelo não roda:

| Necessidade | Script (zero tokens) |
|---|---|
| Score de headline / comparação de variações | `scripts/headline_scorer.py --compare` |
| Lint completo de peça (acentos, hook, CTA, vícios de IA) | `scripts/quality_gate.py` |
| Bloqueio de AI-tells na escrita | hook (roda sozinho no harness) |
| Datas comerciais BR | `scripts/seasonal_calendar_br.py` |
| Validação de agents/manifests/pacote | `validate_agents.py`, `claude plugin validate`, `validate_codex_plugin.py` |
| Estrutura de commands e roteamento | suite pytest |

O mesmo vale em sessão de manutenção: rodar a suite é mais barato e mais confiável que pedir pro modelo "conferir se está tudo certo".

## 5. Registro de custo

O template de worklog tem campo "Custo aproximado". Preencha com o que houver: tokens reportados pela plataforma, tempo de sessão, número de arquivos lidos/escritos, modelo usado. Quando não houver medição disponível, registre "não medido" com o motivo. A série histórica nos worklogs é o que permite dizer se o custo por rodada está caindo (métrica da [EVALS-STRATEGY.md](EVALS-STRATEGY.md) §6).
