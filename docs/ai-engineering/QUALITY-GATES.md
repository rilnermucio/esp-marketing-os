# Quality Gates: regras, implementação e manutenção

> Canônico. Atualizado em 2026-08-03. Este documento é o mapa das regras de qualidade de output. A implementação bloqueante canônica é `scripts/hooks/quality_gate_hook.py`; as tabelas nos prompts (agents, SKILL, AGENTS.md) são derivadas dela (ver [ADR-0002](adr/0002-defesa-em-tres-camadas.md) e [ADR-0003](adr/0003-gate-na-fronteira-de-output.md)).

## As regras atuais

| Regra | Severidade | Racional |
|---|---|---|
| Sem travessão `—` | Bloqueante | AI-tell nº 1; denuncia texto gerado |
| Sem a palavra "brutal" | Bloqueante | AI-tell; substitutos: intenso, forte, pesado, impactante |
| Sem antítese negação→afirmação ("Não é X / É Y", "Não é X / São Y", "Não faça X / Faça Y" e variações; "não é X, e sim Y" gera aviso) | Bloqueante | AI-tell estrutural; reescrever afirmando direto |
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
| 2a. Hook PreToolUse | `hooks/hooks.json` + `scripts/hooks/quality_gate_hook.py`, só para escritas feitas por agents `mos-*` | **Determinística**: bloqueia travessão (e travessão curto usado como pontuação), "brutal" e variações, antíteses; avisa (additionalContext) clichês, CAPS, excesso de emojis e compliance | Arquivos de output dos agents |
| 2b. Hook SubagentStop | `hooks/hooks.json` + `scripts/hooks/quality_gate_hook.py` | **Determinística** na resposta final dos subagents `marketing-os:mos-*`: mesmos bloqueios e avisos | As mesmas regras, inclusive quando a entrega ocorre apenas no chat |
| 3. Lint CLI | `scripts/quality_gate.py` | Determinística, score 0-100 com veredicto (vício de IA capa o score em 60) | Acentos, hook, CTA, legibilidade, formato, hashtags, vícios de IA |
| Guards da camada | `scripts/tests/test_quality_gate_hook.py`, `scripts/tests/test_quality_gate.py` | Testes | Regexes com casos positivos E negativos |

Por que 3 camadas: a camada 1 educa o modelo e cobre o que regex não alcança; a camada 2 garante os padrões regexáveis tanto durante a escrita quanto na fronteira de resposta do Claude Code; a camada 3 dá número comparável e roda sob demanda. O `SubagentStop` concede uma tentativa de correção. Se a resposta corrigida ainda falhar e `stop_hook_active=true`, o hook registra `retry_exhausted` e libera a saída para impedir loop infinito.

No pacote Codex, a camada 2b ainda não possui adapter automático do runtime. As instruções de prompt e o lint continuam disponíveis, e essa diferença permanece explícita no ADR-0003.

## Como validar

```bash
# Testes das duas camadas determinísticas
python -m pytest scripts/tests/test_quality_gate_hook.py scripts/tests/test_quality_gate.py -q

# Lint de uma peça específica
python3 scripts/quality_gate.py peca.md --type post   # post|artigo|email|landing-page|anuncio

# Simular o hook manualmente
echo '{"tool_name":"Write","tool_input":{"file_path":"workspace/x.md","content":"SEU TEXTO"}}' \
  | python3 scripts/hooks/quality_gate_hook.py; echo "exit=$?"   # 2 = bloqueado

# Simular a validação da resposta final de um subagent
echo '{"hook_event_name":"SubagentStop","agent_type":"mos-copy","stop_hook_active":false,"last_assistant_message":"SEU TEXTO"}' \
  | python3 scripts/hooks/quality_gate_hook.py; echo "exit=$?"   # 2 = pede correção
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
3. **CLI herda sozinho**: `quality_gate.py` carrega `HARD_BLOCK_PATTERNS` do hook (fonte única desde 2026-09-28; guard `test_quality_gate.py::test_patterns_are_the_hook_hard_blocks`). Avisos (`WARN_PATTERNS`) ficam só no hook.
4. **Atualizar as tabelas derivadas**: Gate do(s) agent(s) afetado(s), SKILL.md, AGENTS.md, e a tabela deste documento.
5. **Rodar a suite completa** (`-m "not smoke"`).

Pegadinhas conhecidas:

- **Escopo do hook**: ele só avalia escritas e respostas finais de agents `marketing-os:mos-*`, e pula arquivos dentro da raiz do plugin (exceto `workspace/`), estado em `.claude/` e extensões de código (`SKIP_SUFFIXES`, `SKIP_BASENAMES`). Exemplo de padrão proibido dentro de agent, command ou SKILL continua escrito com barra ("Não é X / É Y"), porque o agent repete o que lê e a resposta final dele passa pelo `SubagentStop`.
- **`stop_hook_active` no SubagentStop**: nunca bloquear a segunda falha. Esse campo é o freio contra recursão e tem teste dedicado.
- **Nunca enfraquecer um HARD BLOCK pra acomodar um caso**: se apareceu falso positivo legítimo, ajuste o regex com um teste que fixa o caso, não remova a regra.
- **Regra que só o modelo consegue julgar** (tom, adaptação BR) fica na camada 1 e, futuramente, na camada LLM-graded ([EVALS-STRATEGY.md](EVALS-STRATEGY.md) §4). Não force regex onde não cabe.
