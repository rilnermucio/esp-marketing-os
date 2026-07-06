# Âncoras e protocolo de julgamento LLM-graded (v1 manual)

> Materializa a EVALS-STRATEGY §4. Enquanto não há automação, este é o protocolo manual calibrado; quando a automação vier, ela usa exatamente estas âncoras e regras. Criado em 2026-07-06.

## Regras de julgamento (anti-fragilidade)

1. **Par-a-par, nunca nota absoluta**: o julgador compara A vs B (ou candidato vs âncora) e responde qual vence em CADA critério da rubrica, com 1 frase de motivo. Nota absoluta isolada deriva com o humor do modelo; comparação é estável.
2. **Rubrica fixa**: os critérios de R4 (RUBRICS.md) + Copy Score System (PARTE XV do copy-agent) pra peças de copy. O julgador recebe a rubrica no prompt, nunca julga "de gosto".
3. **Ordem alternada**: rode cada par 2x invertendo a ordem (A/B e B/A). Divergência entre as duas rodadas = empate, não vitória (viés de posição é real).
4. **Julgador barato**: tier leve (Haiku-class) com a rubrica dada resolve; guardar o de fronteira pra arbitrar empates.
5. **Calibração antes de confiança**: antes de usar em decisão, rode 10 pares com veredito humano conhecido; acordo mínimo de 8/10. Abaixo disso, ajuste a rubrica do prompt, não o julgador.

## Âncora POSITIVA (post Instagram, referência do que "bom" significa)

```
Você posta todo dia e o alcance continua caindo?

O algoritmo não está te punindo. Ele só entrega mais do que segura
atenção nos primeiros 3 segundos, e a maioria dos posts perde ali.

Testa isso no próximo post: comece pela pergunta que seu cliente
faria no Google às 23h. A gente fez isso com uma nutricionista e o
salvamento por post triplicou em 3 semanas (de 40 pra 120+).

Salva esse post pra testar amanhã.

Enquete nos stories: "Você olha o alcance de cada post? Sim / Só quando cai"
```

Por que é âncora: hook de pergunta específica, promessa com mecanismo, prova com número e contexto, CTA único, enquete incluída (gate global), zero AI-tells, PT-BR natural.

## Âncora NEGATIVA (mesmo briefing, referência do que reprovar)

```
No mundo digital de hoje — em constante evolução — o conteúdo é rei.

Não é sobre postar mais. É sobre postar melhor. Seja autêntico,
agregue valor e os resultados virão de forma incrível.

Poste com consistência brutal e veja a mágica acontecer! 🚀✨💪
```

Por que reprova: travessão, antítese negação→afirmação, "brutal", clichês ("conteúdo é rei", "agregue valor"), superlativo vago, 3 emojis, zero especificidade, sem CTA concreto, sem enquete. Serve de calibração: um julgador que não reprova isto está quebrado.

## Procedimento manual (até a automação)

1. Pegue o output real do agent + o briefing que o gerou.
2. Monte o par: output vs âncora positiva (mesmo formato de peça; adapte a âncora ao formato quando necessário e registre a adaptação).
3. Prompt do julgador: rubrica R4 + Copy Score + "compare A e B critério a critério; declare o vencedor por critério com 1 frase; sem nota numérica".
4. Rode 2x com ordem invertida. Consolide: vitória só quando consistente nas duas.
5. Registre no worklog da rodada: peça julgada, resultado por critério, ação tomada (aprovar, refazer, ajustar agent).

## Escopo e evolução

- Cobre: qualidade de copy/output (R4). Voice match de clones usa o Voice Match Scoring da PARTE XV-B do copy-agent com este mesmo protocolo par-a-par.
- Não cobre: roteamento (camada determinística + viva já cobrem) e estratégia (human-review permanente).
- Automação futura: quando implementada, roda por amostragem pós-sessão, nunca inline no fluxo de produção (custo e latência).
