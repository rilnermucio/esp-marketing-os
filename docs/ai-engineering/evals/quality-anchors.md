# Âncoras e protocolo de julgamento LLM-graded (v2 assistido)

> Materializa a EVALS-STRATEGY §4. O runner monta as duas ordens e consolida os veredictos; a chamada ao modelo julgador continua externa. Criado em 2026-07-06 e atualizado em 2026-08-03.

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

## Procedimento assistido

1. Pegue o output real do agent + o briefing que o gerou.
2. Monte o par: output vs âncora positiva (mesmo formato de peça; adapte a âncora ao formato quando necessário e registre a adaptação).
3. Gere o prompt normal com `python3 scripts/copy_output_eval.py pair --candidato output.md --referencia baseline.md --briefing briefing.md --profile <perfil>`.
4. Gere a segunda ordem repetindo o comando com `--inverter`.
5. Salve somente os JSONs retornados pelo julgador e rode `python3 scripts/copy_output_eval.py consolidate --normal normal.json --invertida invertida.json --profile <perfil>`.
6. Trate `inconclusivo` como ausência de vitória. Arbitre com revisão humana ou com um modelo de fronteira.
7. Registre no worklog: peça julgada, resultado por critério e ação tomada.

## Escopo e evolução

- Cobre hoje: quality gate determinístico e critérios par-a-par para os perfis versionados em `scripts/evals/output-profiles.json`. Voice match de clones usa o Voice Match Scoring da PARTE XV-B do copy-agent com o mesmo protocolo.
- Baseline calibrado disponível: copy. E-mail, anúncios, oferta, funil, SEO e vídeo ainda precisam de âncoras positivas próprias.
- Continua fora do escopo: roteamento, já coberto pelas camadas determinística e viva, e aprovação estratégica final, que permanece humana.
- Execução: amostragem pós-sessão. O fluxo de produção inline não chama o julgador por custo e latência.
