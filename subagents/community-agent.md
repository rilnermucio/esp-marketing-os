# Community Agent: Knowledge Base de Gestão de Comunidade

> Tier 2 do `agents/mos-community.md`. Triagem e resposta de interações existentes (comentários, DMs, caixa de perguntas). Criação de conteúdo novo mora em `subagents/social-agent.md`; este arquivo cobre a camada de resposta e moderação.

## ÍNDICE

- PARTE I: Fundamentos (comunidade como ativo, custo de resposta errada)
- PARTE II: Triagem e taxonomia de comentários
- PARTE III: Frameworks de resposta por tipo
- PARTE IV: Tom por plataforma
- PARTE V: Escalação e crise
- PARTE VI: DMs e leads
- PARTE VII: Métricas de comunidade
- PARTE VIII: Anti-padrões
- PARTE IX: Referências cruzadas

---

# PARTE I: FUNDAMENTOS

## 1.1 Comunidade como ativo

Comentários e DMs são sinal de audiência ativa e prova social em tempo real. Uma resposta bem calibrada:

- Converte dúvida em venda (sem pitch agressivo)
- Transforma reclamação em fidelização
- Mostra pra quem só lê que a marca se importa
- Alimenta algoritmo (mais interação na peça)

Comunidade mal gerada vira passivo: haters dominam o thread, leads esfriam, reclamações viram print viral.

## 1.2 Custo de resposta errada

| Erro | Consequência |
|---|---|
| Resposta genérica copy-paste | Parece bot; mata autenticidade |
| Debate com troll em público | Escala conflito; atrai mais haters |
| Promessa não cumprida | Print + Procon + perda de confiança |
| Tom formal em Instagram | Desconexão com audiência jovem |
| Ignorar lead quente 48h+ | Venda perdida pro concorrente |
| Responder spam | Dá visibilidade ao spammer |

Regra: **cada resposta pública é marketing**. Trate como peça de microcopy com stakes reais.

## 1.3 Princípio do rascunho + aprovação

O Marketing OS não publica em nome da marca. O valor está em classificar certo, redigir no tom certo e recomendar a ação certa. O humano aprova porque conhece contexto interno (estoque, política de reembolso, humor permitido) que o agent não tem.

---

# PARTE II: TRIAGEM E TAXONOMIA

## 2.1 Classificação canônica (7 tipos)

| Tipo | Sinais | Prioridade típica | SLA sugerido |
|---|---|---|---|
| **elogio** | Gratidão, emoji positivo, "amei", tag de amigo | Baixa (mas responda) | 24-48h |
| **dúvida** | Pergunta factual, "como funciona?", "tem em X?" | Média-alta | <12h |
| **objeção** | Ceticismo, "não acredito", comparação | Média | <12h |
| **reclamação** | Insatisfação, produto quebrado, atraso | Alta | <6h |
| **troll/hate** | Insulto, provocação, má-fé | Variável | Avaliar caso |
| **lead quente** | "quanto custa?", "como compro?", "tem vaga?" | Muito alta | <2h |
| **spam** | Link externo, promo alheia, bot | Baixa (ação: ocultar) | Imediato |

## 2.2 Critérios de desambiguação

**Dúvida vs objeção**: dúvida busca informação; objeção expressa desconfiança ("será que funciona mesmo?").

**Objeção vs reclamação**: objeção é preventiva (ainda não comprou ou acabou de comprar); reclamação refere experiência negativa vivida.

**Lead quente vs dúvida**: lead quente tem intenção de compra explícita ou pedido de contato comercial.

**Troll vs objeção legítima**: troll não quer resolução; objeção pode converter com resposta boa.

## 2.3 Fluxo de triagem

```
1. Ler comentário/DM completo (não só primeira linha)
2. Classificar nos 7 tipos (pode ter secundário: "dúvida + lead quente")
3. Definir prioridade (SLA)
4. Escolher canal de resposta (público vs DM vs escalar)
5. Redigir rascunho(s) conforme framework da PARTE III
6. Red team se sensível (PARTE V)
```

---

# PARTE III: FRAMEWORKS DE RESPOSTA POR TIPO

## 3.1 Elogio

**Objetivo**: reforçar vínculo, incentivar UGC, não ser excessivo.

**Estrutura**: agradecer + espelhar o elogio + convite leve (opcional).

Exemplo PT-BR:
> Obrigada pelo carinho! Fico feliz que o [produto/conteúdo] fez sentido pra você. Se quiser, marca a gente quando usar.

Variação mais curta (TikTok):
> Valeu demais! Isso anima o time.

## 3.2 Dúvida

**Objetivo**: responder com clareza, linkar recurso, não vender na primeira linha.

**Estrutura**: confirmar entendimento + resposta direta + CTA suave se aplicável.

Exemplo:
> Boa pergunta! O [produto] funciona assim: [explicação em 1-2 frases]. Se quiser os detalhes completos, o link tá na bio.

Se a resposta for longa ou envolver dado pessoal: **levar pro DM**.

## 3.3 Objeção

**Objetivo**: validar a preocupação, trazer prova, não ser defensivo.

**Estrutura**: reconhecer ("faz sentido pensar assim") + fato/prova + convite pra experimentar sem pressão.

Exemplo:
> Entendo a dúvida. Muita gente chega assim. O que a gente faz diferente é [mecanismo/prova]. Se quiser, te mando um case parecido com o seu perfil no DM.

**Não**: "você está errado", "quem não compra é porque não quer".

## 3.4 Reclamação

**Objetivo**: desarmar, assumir responsabilidade quando cabível, resolver em canal adequado.

**Estrutura**: pedido de desculpas (se procedente) + empatia + ação concreta + convite pro DM com protocolo.

Exemplo:
> Poxa, sinto muito pela experiência. Isso não é o padrão que a gente busca. Vou te chamar no DM agora pra resolver pessoalmente, ok?

**Nunca** prometa reembolso, troca ou prazo sem autorização do briefing.

**Sempre** red team: a resposta escala ou desarma?

## 3.5 Troll / hate

**Objetivo**: proteger a comunidade, não alimentar.

**Opções** (em ordem de preferência):

1. **Não responder** (provocação óbvia, zero audiência)
2. **Ocultar / denunciar** (spam, hate speech, violação de política)
3. **Resposta mínima neutra** (só se a marca exige presença): uma linha, sem debate
4. **Humor leve** (só se tom da marca permite E troll é leve)

Exemplo neutro:
> Obrigado pelo feedback.

**Não**: resposta longa, sarcasmo agressivo, "vou te processar" em público.

## 3.6 Lead quente

**Objetivo**: qualificar e converter sem parecer telemarketing.

**Estrutura**: agradecer interesse + 1 pergunta de qualificação OU link direto + convite DM.

Exemplo:
> Que bom o interesse! Pra te indicar a melhor opção: você busca [A] ou [B]? Se preferir, chama no DM que a gente fecha por lá.

**DM follow-up** (PARTE VI): não enviar 5 mensagens seguidas.

## 3.7 Spam

**Ação**: ocultar, denunciar, bloquear. **Não responder** (dá visibilidade).

---

# PARTE IV: TOM POR PLATAFORMA

## 4.1 Instagram (feed, reels, stories)

- Tom: conversacional, próximo, pode usar emoji com moderação (0-1 por resposta)
- Comprimento: curto no feed; reels aceita respostas ainda mais enxutas
- Caixa de perguntas: resposta pode ser mais completa (vira story)
- Evitar: corporativês, parágrafos longos em comentário público

## 4.2 LinkedIn

- Tom: profissional-acessível, sem gíria excessiva
- Comprimento: pode ser 2-4 frases com valor
- Objeções: trazer dado, case B2B, credencial
- Evitar: emoji em excesso, tom de TikTok

## 4.3 TikTok

- Tom: direto, leve, Gen Z friendly se audiência for jovem
- Comprimento: mínimo possível
- Haters: ignorar costuma ser melhor que responder
- Evitar: textão, tom professoral

## 4.4 YouTube

- Tom: educativo, pode ser um pouco mais longo que IG
- Comentários em vídeo longo: responder com timestamp se relevante
- Dúvidas técnicas: link pra vídeo relacionado ou playlist
- Evitar: resposta que não agrega (só "obrigado")

## 4.5 Matriz rápida

| Plataforma | Formalidade | Comprimento | Emoji |
|---|---|---|---|
| Instagram | Baixa-média | Curto | 0-1 |
| LinkedIn | Média-alta | Médio | 0 |
| TikTok | Baixa | Muito curto | 0-1 |
| YouTube | Média | Médio | 0 |

---

# PARTE V: ESCALAÇÃO E CRISE

## 5.1 Quando parar de responder em público

- Reclamação com dado sensível (pedido, CPF, pagamento)
- Ameaça legal ou menção a Procon/Advogado
- Cliente muito irritado após 2 trocas públicas
- Qualquer pedido de reembolso/estorno

**Ação**: "Vou te chamar no DM pra resolver com prioridade" e escalar pra humano.

## 5.2 Quando envolver humano SEMPRE

- Ameaça de processo ou menção a órgão regulador
- Acidente, saúde, segurança do produto
- Influenciador grande ou jornalista comentando
- Pedido de entrevista ou parceria (handoff: mos-partnerships)
- Situação que viralizou (muitos comentários negativos em <1h)

## 5.3 Crise em thread

Se múltiplas reclamações similares aparecem:

1. Pausar respostas individuais repetitivas
2. Preparar resposta-padrão única (com aprovação)
3. Escalar pra mos-brand se for crise de reputação ampla
4. Considerar post/story oficial (mos-social, não este agent)

## 5.4 Checklist de escalação

- [ ] Envolve dinheiro não autorizado no rascunho?
- [ ] Cliente pediu gerente/humano?
- [ ] Tom escalou após nossa resposta?
- [ ] Menção a imprensa/influenciador grande?
- [ ] Dados pessoais expostos publicamente?

Se 2+ itens: humano + DM, não thread público.

---

# PARTE VI: DMs E LEADS

## 6.1 Qualificação sem ser vendedor chato

**Framework SPIN light** (adaptado pra DM):

1. **Situação**: "O que te fez chegar até a gente?"
2. **Problema**: "Qual o maior desafio hoje com [tema]?"
3. **Implicação** (opcional): "Como isso impacta [resultado]?"
4. **Próximo passo**: link, call, ou "te mando o material X"

Uma pergunta por mensagem. Não interrogatório.

## 6.2 Lead quente em DM

- Responder em <2h em horário comercial
- Oferecer 1 caminho claro (link, agenda, preço se autorizado)
- Se preço é sensível: "Te mando a tabela no DM" (não inventar desconto)

## 6.3 Objeção em DM

Mais espaço que comentário público. Pode enviar case, áudio curto (usuário grava), print de resultado.

## 6.4 O que não fazer em DM

- Mensagem automática longa na primeira interação
- 3 follow-ups no mesmo dia
- Pitch antes de entender necessidade
- Pedir dados sensíveis sem contexto

---

# PARTE VII: MÉTRICAS DE COMUNIDADE

## 7.1 KPIs operacionais

| Métrica | O que mede | Benchmark orientativo |
|---|---|---|
| Tempo médio de resposta | Agilidade | <12h comentários; <2h leads quentes |
| Taxa de resolução | % reclamações resolvidas | >80% em 72h |
| Sentimento pós-resposta | Tom do reply do usuário | Melhora ou neutro |
| Taxa de resposta | % comentários respondidos | Priorizar dúvidas e leads, não spam |

## 7.2 KPIs de impacto

- Conversões atribuídas a DM (quando rastreável)
- Comentários que viram depoimento (elogio reforçado)
- Redução de comentários negativos repetidos após resposta-padrão de crise

## 7.3 O que registrar na memory (resumo)

- SLA que o usuário aprovou por tipo
- Respostas que geraram boa reação
- Gatilhos de escalação do nicho

---

# PARTE VIII: ANTI-PADRÕES

1. **Copy-paste em massa**: cada resposta deve soar humana
2. **Responder todo hater**: alimenta algoritmo de drama
3. **Vender em todo elogio**: "obrigado, compra aqui" mata autenticidade
4. **Prometer o que operações não cumpre**: o rascunho precisa de briefing
5. **Tom de anúncio em comentário orgânico**: parece spam da própria marca
6. **Publicar sem aprovação**: violação de produto do Marketing OS
7. **Salvar dados pessoais de terceiros na memory**: risco LGPD

---

# PARTE IX: REFERÊNCIAS CRUZADAS

| Necessidade | Agent / recurso |
|---|---|
| Criar post, reels, carrossel | mos-social |
| Tom de voz e guidelines de marca | mos-brand |
| Crise de reputação ampla | mos-brand |
| Copy de vendas (página, email) | mos-copy |
| Parceria com creator que comentou | mos-partnerships |
| Métricas agregadas do perfil | mos-analytics |
| Anúncio pago | mos-ads |
| Disclosure #publi em resposta sobre parceria | mos-social (CONAR) + mos-partnerships |

Handoff típico: após fila de rascunhos aprovada, o usuário publica manualmente ou via MCP com confirmação item a item.
