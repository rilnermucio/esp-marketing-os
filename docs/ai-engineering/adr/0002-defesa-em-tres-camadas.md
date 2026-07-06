# ADR-0002: Quality gates com defesa em 3 camadas e hook como fonte canônica

**Status**: aceito
**Data**: 2026-07-06
**Autor**: Claude Fable 5 (mantenedor sênior)

## Contexto

As regras de qualidade de output (travessão, "brutal", antítese, acentos, fact-check, compliance...) existem em 3 mecanismos: instrução de prompt (agents/SKILL/AGENTS.md), hook PreToolUse determinístico e CLI de lint. A regra em prosa está duplicada em ~20 arquivos (F-BLOAT-03). O risco se materializou uma vez: a proibição de antítese existia fora do sistema muito antes de entrar nele (jun/2026), e as camadas ficaram meses desalinhadas.

## Decisão

**Manter as 3 camadas (elas têm papéis diferentes) e estabelecer hierarquia canônica:**

1. `scripts/hooks/quality_gate_hook.py` é a **fonte da verdade executável** pra toda regra regexável. Regra nova entra primeiro nele (com testes), depois nas demais camadas.
2. `docs/ai-engineering/QUALITY-GATES.md` é o **mapa humano**: lista completa, severidades, exemplos calibrados, receita de atualização.
3. As tabelas nos prompts (agents, SKILL, AGENTS.md) são **derivadas**: educam o modelo e cobrem o não-regexável (tom, aspas, enquete). Elas nunca contradizem o hook; em divergência, o hook vence e a tabela é corrigida.

**Plano de redução gradual da duplicação (sem big bang)**: ao tocar qualquer agent por outro motivo, encolher a tabela de gates local para: referência ao conceito + apenas os itens específicos do domínio ou não-regexáveis. Não remover a camada de prompt por completo: instrução previne a violação antes do bloqueio, e o bloqueio sem instrução gera loop de tentativa-erro (custo).

## Alternativas consideradas

1. **Fonte única via include/import nos prompts**: rejeitado. Expansão de imports em arquivos de agent não é portável entre Claude Code e Codex; criaria dependência de mecanismo de um runner só (R5).
2. **Só o hook, sem instrução de prompt**: rejeitado. O modelo escreveria violações e seria bloqueado repetidamente; o hook não cobre regra não-regexável.
3. **Gerador que injeta as tabelas nos 20 arquivos a partir do hook**: adiado. Automação de sincronia vale a pena se a divergência reincidir após o plano gradual (H8.3: abstração na segunda repetição, não na primeira... esta seria a segunda; na terceira, construir).

## Consequências

Positivas: regra nova tem UM ponto de entrada definido e receita testada (worked example: gate de antítese); divergência entre camadas passa a ser bug com dono.

Negativas (custo aceito): a duplicação em prosa continua existindo até as tabelas encolherem organicamente; disciplina de "hook primeiro" depende de processo (OPERATING-MODEL + handbook), não de guard. Se divergência reincidir, promover a alternativa 3 a plano ativo.

## Critério de revisão

Reabrir se: divergência entre camadas for encontrada 2x após esta data, ou se o Codex runner passar a suportar hooks nativamente (hoje a camada 2 é garantida só no Claude Code; no Codex valem as camadas 1 e 3).
