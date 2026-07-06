# Quality Gates: regras, implementação e manutenção

> Canônico. Atualizado em 2026-07-06. Este documento é o mapa das regras de qualidade de output. A implementação bloqueante canônica é `scripts/hooks/quality_gate_hook.py`; as tabelas nos prompts (agents, SKILL, AGENTS.md) são derivadas dela (ver [ADR-0002](adr/0002-defesa-em-tres-camadas.md)).

## As regras atuais

| Regra | Severidade | Racional |
|---|---|---|
| Sem travessão `—` | Bloqueante | AI-tell nº 1; denuncia texto gerado |
| Sem a palavra "brutal" | Bloqueante | AI-tell; substitutos: intenso, forte, pesado, impactante |
| Sem antítese negação→afirmação ("Não é X / É Y", "Não faça X / Faça Y" e variações) | Bloqueante | AI-tell estrutural; reescrever afirmando direto |
| Sem PALAVRAS EM CAPS gratuitas | Gate de prompt | Grita, não persuade |
| Sem aspas em roteiros/falas; sem aspas de ênfase | Gate de prompt | Fala escrita direto soa humano |
| Máximo 0-1 emoji (2 em contextos justificados) | Gate de prompt | Poluição visual |
| Acentuação PT-BR correta, sempre | Bloqueante por score | Texto desacentuado é rascunho |
| Clichês de IA ("em um mundo onde", "sem mais delongas", superlativo vago...) | Warning | Uso legítimo raro existe; agent decide |
| Fact-check de pessoa/estatística/case via WebSearch (CONFIRMADO / PROVÁVEL / NÃO USAR) | Bloqueante por processo | Claim inventado destrói confiança (F-CLAIM-01) |
| Disclaimer regulatório quando trigger presente (CVM, ANVISA, CONAR, afiliado) | Warning de compliance | F-CLAIM-02 |
| Conteúdo social inclui sugestão de enquete | Gate de prompt | Regra global de engajamento |
| Limites de plataforma (280 chars no X, subject 30-50, etc.) | Score | F-COPY-03 |

## Onde cada camada mora

| Camada | Arquivo | Natureza | Cobre |
|---|---|---|---|
| 1. Gates de prompt | `agents/mos-*.md` (seção Quality Gates), `skills/marketing-os/SKILL.md`, `AGENTS.md` | Instrução ao modelo (depende de obediência) | Todas as regras, incluindo as não-regexáveis (tom, aspas, enquete) |
| 2. Hook PreToolUse | `scripts/hooks/quality_gate_hook.py` | **Determinística e bloqueante** (exit 2 em HARD BLOCK; warnings em stderr) | Travessão, "brutal", antíteses, clichês, compliance |
| 3. Lint CLI | `scripts/quality_gate.py` | Determinística, score 0-100 com veredicto (vício de IA capa o score em 60) | Acentos, hook, CTA, legibilidade, formato, hashtags, vícios de IA |
| Guards da camada | `scripts/tests/test_quality_gate_hook.py`, `scripts/tests/test_quality_gate.py` | Testes | Regexes com casos positivos E negativos |

Por que 3 camadas: a camada 1 educa o modelo e cobre o que regex não alcança; a camada 2 garante (roda no harness em todo Write/Edit dos agents, independe de obediência); a camada 3 dá número comparável e roda sob demanda (agents com Bash a invocam na auto-iteração).

## Como validar

```bash
# Testes das duas camadas determinísticas
python -m pytest scripts/tests/test_quality_gate_hook.py scripts/tests/test_quality_gate.py -q

# Lint de uma peça específica
python3 scripts/quality_gate.py peca.md --type post   # post|artigo|email|landing-page|anuncio

# Simular o hook manualmente
echo '{"tool_name":"Write","tool_input":{"file_path":"workspace/x.md","content":"SEU TEXTO"}}' \
  | python3 scripts/hooks/quality_gate_hook.py; echo "exit=$?"   # 2 = bloqueado
```

## Exemplos calibrados (positivos e negativos)

| Texto | Veredicto | Por quê |
|---|---|---|
| "Não é sobre vender mais. É sobre vender melhor." | BLOQUEIA | Antítese negação→afirmação clássica |
| "Não foi sorte. Foi estratégia." | BLOQUEIA | Variação com verbo repetido |
| "Não é fácil crescer um perfil do zero. Esse processo leva meses." | PASSA | Negação simples sem paralelo de afirmação |
| "Você não sabe por onde começar, comece pelo básico. Sabe qual é o maior erro?" | PASSA | Verbo repetido em frase nova não relacionada (o span do regex exclui pontuação justamente pra isso) |
| "A verdade brutal sobre vendas" | BLOQUEIA | Palavra proibida |
| "A brutalidade do algoritmo" | PASSA | Lookaround protege palavra contida |
| "O segredo — que ninguém conta" | BLOQUEIA | Travessão |

## Como atualizar sem quebrar os agents

Ordem obrigatória (worked example real: gate de antítese, jun/2026):

1. **Regex no hook** (`HARD_BLOCK_PATTERNS` ou `WARN_PATTERNS`). Regras de engenharia do regex: span interno exclui pontuação pra não atravessar cláusulas; `find_hard_violations` aplica IGNORECASE em tudo (necessário pro backreference `\1` casar "faça/Faça"); mensagem diz o que fazer, não só o que está errado.
2. **Testes junto**: casos que disparam E casos parecidos que NÃO podem disparar (falso positivo é regressão de usabilidade).
3. **Espelhar no CLI** (`AI_TELL_PATTERNS` em `quality_gate.py`) se a regra é de copy.
4. **Atualizar as tabelas derivadas**: Gate do(s) agent(s) afetado(s), SKILL.md, AGENTS.md, e a tabela deste documento.
5. **Rodar a suite completa** (`-m "not smoke"`).

Pegadinhas conhecidas:

- **`SKIP_PATH_PATTERNS` do hook**: commands/, subagents/, docs/, scripts/ e afins são pulados (são tooling/KB, não copy). `agents/` e `skills/` NÃO são pulados. Consequência: exemplo de padrão proibido dentro de um agent deve ser escrito em forma que não casa com o próprio regex (por isso as tabelas usam "Não é X / É Y" com barra em vez de pontuação).
- **Nunca enfraquecer um HARD BLOCK pra acomodar um caso**: se apareceu falso positivo legítimo, ajuste o regex com um teste que fixa o caso, não remova a regra.
- **Regra que só o modelo consegue julgar** (tom, adaptação BR) fica na camada 1 e, futuramente, na camada LLM-graded ([EVALS-STRATEGY.md](EVALS-STRATEGY.md) §4). Não force regex onde não cabe.
