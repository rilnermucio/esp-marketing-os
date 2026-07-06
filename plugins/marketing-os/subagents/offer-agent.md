# Offer Agent: Knowledge Base de Arquitetura de Ofertas

> Tier 2 do `agents/mos-offer.md`. Engenharia da oferta: valor, preço, risco e condições. A APLICAÇÃO do stack em copy (como escrever na página) mora em `subagents/copy-agent.md` PARTE II-C; este arquivo é a fonte da arquitetura.

## ÍNDICE

- PARTE I: Fundamentos da Oferta (equação de valor, hierarquia de alavancas)
- PARTE II: Grand Slam Offer (anatomia, processo de construção)
- PARTE III: Value Stack e Engenharia de Bônus
- PARTE IV: Garantias (tipos, matemática, garantia legal BR)
- PARTE V: Precificação (psicologia, modelos, parcelamento BR)
- PARTE VI: Escassez, Urgência e Condições Éticas
- PARTE VII: Offer Score System e Diagnóstico
- PARTE VIII: Ofertas por Modelo de Negócio
- PARTE IX: Exemplos PT-BR Aplicados
- PARTE X: Anti-padrões e Erros Fatais
- PARTE XI: Referências Cruzadas

---

# PARTE I: FUNDAMENTOS DA OFERTA

## 1.1 Oferta ≠ produto ≠ copy

| Camada | O que é | Dono no Marketing OS |
|---|---|---|
| Produto | O que é entregue (curso, mentoria, serviço, software) | mos-infoproduct / usuário |
| **Oferta** | O pacote de valor, preço, risco e condições em torno do produto | **mos-offer** |
| Copy | Como a oferta é comunicada em cada peça | mos-copy |
| Funil | Onde cada oferta entra na jornada | mos-funnel |

O mesmo produto suporta ofertas radicalmente diferentes. Mudar a oferta costuma mover conversão mais que reescrever a copy, porque ataca a decisão econômica do comprador, e é mais barato que comprar mais tráfego.

## 1.2 A equação de valor (Hormozi)

```
                 Resultado dos sonhos × Probabilidade percebida de alcançá-lo
Valor percebido = ------------------------------------------------------------
                 Tempo até o resultado × Esforço e sacrifício exigidos
```

Toda decisão de arquitetura mexe em um dos 4 fatores:

| Fator | Como aumentar/diminuir | Elementos típicos |
|---|---|---|
| Resultado dos sonhos ↑ | Prometer o resultado que o público JÁ quer (não educar desejo) | Promessa central, naming |
| Probabilidade percebida ↑ | Prova, mecanismo único, garantia, cases | Garantia, depoimentos, demonstração |
| Tempo ↓ | Acelerar o primeiro resultado visível | Quick win na 1ª semana, templates prontos, done-for-you |
| Esforço ↓ | Remover trabalho do comprador | Suporte, comunidade, ferramentas, done-with-you |

Regra de leitura: oferta fraca quase sempre tem denominador alto (parece demorado e trabalhoso), não numerador baixo. Antes de inflar promessa, reduza tempo/esforço percebidos.

## 1.3 Hierarquia de alavancas

Em ordem de impacto sobre receita, com custo de mudança crescente pra baixo:

1. **Mercado/público** (quem você serve): starving crowd vence tudo
2. **Oferta** (este arquivo)
3. **Copy** (comunicação da oferta)
4. **Tráfego** (volume sobre a máquina acima)

Diagnóstico prático: se a página converte < 0,5% com tráfego qualificado e copy decente, suspeite da oferta antes de reescrever a página. Ver PARTE VII pra diagnóstico estruturado.

---

# PARTE II: GRAND SLAM OFFER

## 2.1 Anatomia

Uma Grand Slam Offer (conceito de $100M Offers) é uma oferta tão desproporcional em valor percebido que sai da comparação de preço com alternativas. Componentes:

1. **Promessa específica**: resultado + prazo + condição ("X em Y sem Z")
2. **Mecanismo único**: POR QUE esta oferta consegue o que as alternativas não conseguem (método nomeado, processo proprietário)
3. **Stack que resolve a jornada inteira**: cada obstáculo entre o comprador e o resultado tem um entregável correspondente
4. **Inversão de risco**: garantia desenhada pro medo específico do público
5. **Motivo real para agir**: deadline/condição verificável
6. **Naming**: nome que carrega a promessa (testar com headline_scorer)

## 2.2 Processo de construção em 5 passos

```
PASSO 1: LISTAR DORES E OBSTÁCULOS
  Do research (mos-research): tudo que impede o público de chegar ao
  resultado sozinho. Incluir obstáculos que surgem DEPOIS de comprar
  soluções concorrentes ("comprei curso e não assisti").

PASSO 2: MAPEAR SOLUÇÕES
  Para cada obstáculo, a solução ideal (ignorando custo por enquanto).
  Formato: "Como [resolver obstáculo] sem [sacrifício]".

PASSO 3: ESCOLHER VEÍCULOS DE ENTREGA
  Para cada solução, o formato: aula, template, ferramenta, call,
  comunidade, done-for-you, garantia de acesso. Critério: máximo valor
  percebido pelo menor custo marginal de entrega (templates e gravações
  escalam; calls individuais não).

PASSO 4: TRIM & STACK
  Cortar o que tem custo alto e valor percebido baixo. Empilhar o que
  sobra em componentes nomeados com valor individual justificável.

PASSO 5: ADICIONAR RISCO INVERTIDO + MOTIVO PRA AGIR
  Garantia da PARTE IV + mecanismo da PARTE VI.
```

## 2.3 Saindo da comparação de preço

Sinais de oferta commodity: o lead pergunta "quanto custa" antes de perguntar "como funciona"; comparação direta com concorrente mais barato; objeção dominante é preço. Correções em ordem: (1) estreitar público e promessa (nicho específico paga mais por especificidade), (2) nomear o mecanismo único, (3) mudar a unidade de comparação (de "curso de tráfego" para "sistema de aquisição instalado"), (4) só então mexer em preço.

---

# PARTE III: VALUE STACK E ENGENHARIA DE BÔNUS

> A apresentação do stack em copy (ordem de revelação, ancoragem na página) está em `copy-agent.md` PARTE II-C (2C.2). Aqui: o que entra no stack e por quê.

## 3.1 Estrutura do stack

| Camada | Função | Regra |
|---|---|---|
| Entregável core | O veículo principal do resultado | Nunca é "bônus"; carrega a promessa |
| Aceleradores | Reduzem tempo até o primeiro resultado | Templates, swipes, checklists prontos |
| Removedores de esforço | Reduzem trabalho percebido | Suporte, comunidade, revisões, ferramentas |
| Neutralizadores de objeção | Cada bônus mata UMA objeção nomeada | Ver 3.2 |
| Inversão de risco | Garantia (PARTE IV) | Fecha a conta emocional |

Tamanho: 4-7 componentes. Abaixo de 4, valor percebido raso; acima de 7, sobrecarga cognitiva e cheiro de filler.

## 3.2 Bônus que movem agulha vs filler

Um bônus só entra se responder SIM às três:

1. **Neutraliza uma objeção específica?** ("não tenho tempo" → bônus "implementação em 15 min/dia")
2. **Teria demanda vendido sozinho?** (teste mental do produto independente)
3. **O comprador consegue explicar o valor dele pra outra pessoa?**

Filler típico que conta CONTRA a oferta: PDF genérico requentado, "acesso ao grupo" sem moderação prometida, gravação de live antiga sem edição, "e-book bônus" que é capítulo do curso. O comprador experiente reconhece enchimento e desconta a credibilidade do stack inteiro.

## 3.3 Precificação honesta de bônus

Cada valor declarado precisa de um comparável defensável, numa destas bases:

| Base | Exemplo |
|---|---|
| Preço de venda real anterior | "Vendido separadamente por R$ 497 em [data/contexto]" |
| Preço de alternativa de mercado | "Uma consultoria dessa análise custa R$ X no mercado" |
| Custo de produção pro comprador | "Montar essas 40 planilhas levaria ~30h do seu time" |
| Valor do resultado que destrava | "Recuperar 1 cliente já paga o bônus" (com conta mostrada) |

Número redondo inventado pra inflar o total é o Gate 4 do agent: FAIL.

## 3.4 Naming e sequenciamento

- Nome de bônus carrega a objeção que mata: "Protocolo Anti-Procrastinação (pra quem já comprou curso e não assistiu)"
- Ordem de apresentação: core → acelerador mais desejado → neutralizadores → risco. O bônus mais forte nunca fica no meio da lista.
- Bônus expirante (PARTE VI) precisa ser destacável do stack sem quebrar a oferta base.

---

# PARTE IV: GARANTIAS

## 4.1 Tipos

| Tipo | Formato | Quando usar | Risco |
|---|---|---|---|
| Incondicional | "X dias, devolução sem perguntas" | Produto escalável de custo marginal baixo (curso gravado) | Refund oportunista; baixo em ticket < R$ 2k |
| Condicional | "Se fizer A e B e não obtiver C, devolvo" | High-ticket com entrega intensiva; filtra quem não executa | Precisa de termos claros e verificáveis |
| Dupla | Incondicional 7-30d + condicional estendida | Lançamentos: mata o medo inicial E o medo de longo prazo | Complexidade de comunicação |
| Performance | "Só pago se entregar X" / "trabalho até atingir Y" | Serviço/agência com controle sobre o resultado | Nunca prometer o que depende só do cliente |
| Anti-garantia | "Sem reembolso, e aqui está o porquê" | Acesso a material sensível, coortes pequenas premium | Exige prova social forte; reduz conversão, aumenta compromisso |

## 4.2 A matemática da garantia

Garantia boa é uma troca calculada: lift de conversão × ticket vs refunds adicionais.

```
Vale a pena se: (conversão_com - conversão_sem) × ticket × leads
                > refund_rate_adicional × ticket × compradores
```

Referências práticas pra modelar (validar com dados do projeto, não são leis): garantia incondicional costuma subir conversão de forma perceptível e o refund em infoproduto bem entregue tende a ficar em dígito único percentual; refund explode quando a promessa foi inflada (problema de oferta, não de garantia). Registrar os números reais do cliente na memory do agent.

## 4.3 Garantia legal BR (piso obrigatório)

- **CDC art. 49**: compra fora de estabelecimento comercial (online incluso) tem direito de arrependimento de **7 dias corridos** com devolução integral. Isso NÃO é diferencial de oferta; é lei.
- Consequência de arquitetura: a garantia de marketing começa ONDE a legal termina. "Garantia de 7 dias" anuncia o mínimo legal como se fosse generosidade; comprador informado percebe. Ofereça 14, 21, 30+ dias ou uma condicional estendida.
- Termos por escrito: prazo, condição de acionamento, canal, prazo de devolução do dinheiro. Ambiguidade vira disputa e chargeback.

## 4.4 Desenhando pro medo específico

A garantia certa espelha o medo dominante do público (research!): medo de "não ter tempo" pede garantia estendida com trilha mínima; medo de "não funcionar pra mim" pede condicional com acompanhamento; medo de "já comprei e me arrependi" pede incondicional simples e sem fricção.

---

# PARTE V: PRECIFICAÇÃO

## 5.1 Psicologia aplicada ao BR

| Técnica | Aplicação | Nota BR |
|---|---|---|
| Ancoragem | Apresentar valor total do stack (ou alternativa cara) antes do preço | Âncora precisa ser crível (PARTE III.3) |
| Parcelamento | Preço comunicado em "12x de R$ X" | Padrão cultural BR forte; o mensal É o preço percebido em ticket médio/baixo |
| Charm pricing | R$ 497, R$ 1.997 | Funciona em curso/ticket médio; high-ticket premium usa número redondo (R$ 15.000) |
| Decoy | Plano do meio desenhado pra vencer | Exige 3 opções genuínas; decoy falso é detectável |
| Reenquadramento | "R$ 3,30 por dia" / "menos que seu almoço" | Usar com parcimônia; clichê em nicho saturado |

## 5.2 Modelos de precificação

| Modelo | Estrutura | Melhor para |
|---|---|---|
| One-time | Preço único (à vista + parcelado) | Curso, workshop, produto pontual |
| Recorrência | Mensal/anual | Comunidade, membership, SaaS, mentoria contínua |
| Híbrido | Entrada + recorrência | Implementação + acompanhamento |
| Application-only | Preço revelado na call, após aplicação | High-ticket (> R$ 10k), coortes pequenas |
| Por performance | Base + variável sobre resultado | Serviço com resultado mensurável e controlável |

## 5.3 Ratio valor:preço

Regra prática de percepção: o valor total justificado do stack deve ficar na faixa de 5x a 10x o preço. Abaixo de 3x, a oferta parece cara; acima de ~15x, o número perde credibilidade e o comprador desconta tudo (inflação de âncora é anti-padrão, PARTE X).

## 5.4 Quando subir preço

Sinais: conversão alta com objeção de preço rara; agenda/turma lotando rápido; perfil de comprador abaixo do ideal (preço baixo atrai quem não executa); custo de suporte por aluno subindo. Como: subir na próxima coorte com motivo público (mais entrega, mais acompanhamento), avisar a base antes (urgência real de "último preço"), nunca subir silenciosamente no meio de um lançamento.

---

# PARTE VI: ESCASSEZ, URGÊNCIA E CONDIÇÕES ÉTICAS

## 6.1 Regra absoluta

Mecanismo de urgência precisa de justificativa VERIFICÁVEL. Fabricado (contador que reseta, "últimas vagas" infinitas, "turma fecha hoje" que reabre amanhã) é: (a) FAIL no Gate 2 do agent, (b) risco CONAR/CDC de publicidade enganosa, (c) destruição da confiança que mata a segunda venda. A urgência ética existe de sobra; não há motivo pra fabricar.

## 6.2 Mecanismos legítimos

| Mecanismo | Justificativa verificável | Observação |
|---|---|---|
| Coorte/turma com data | Onboarding em grupo, calendário real de aulas ao vivo | O mais forte pra curso/mentoria |
| Capacidade | Limite operacional real (vagas de acompanhamento, agenda) | Publicar o número e honrá-lo |
| Bônus expirante | Bônus de ação rápida sai em data X (a oferta base continua) | Preserva a integridade da oferta principal |
| Preço de lançamento | Preço sobe na próxima abertura (e sobe MESMO) | Histórico público de preços é a prova |
| Sazonalidade real | Data comercial, virada de ano fiscal, evento | Combinar com `/datas-sazonais` |

## 6.3 Deadline architecture

- Um mecanismo dominante por oferta (dois no máximo, se independentes: turma com data + bônus de ação rápida)
- O deadline aparece com o MOTIVO junto, sempre ("fechamos dia X porque o onboarding em grupo começa dia Y")
- Planejar o pós-deadline antes de abrir: o que acontece com quem chega depois (lista de espera, downsell perpétuo, próxima coorte) define se o deadline era real

---

# PARTE VII: OFFER SCORE SYSTEM E DIAGNÓSTICO

## 7.1 Score (0-100)

| Critério | Peso | Pergunta-teste |
|---|---|---|
| Clareza da promessa | 20 | Um lead frio repete a promessa depois de ler 1x? |
| Valor percebido vs preço | 25 | O ratio está em 5-10x com comparáveis defensáveis? |
| Credibilidade/prova | 20 | A probabilidade percebida tem sustentação (mecanismo + prova) pro nível de consciência do público? |
| Inversão de risco | 20 | A garantia espelha o medo dominante e é sustentável? |
| Motivo para agir | 15 | O deadline é real, justificado e comunicado com o porquê? |

Interpretação: 85+ pronta pra copy; 70-84 ajustar o critério mais fraco antes do handoff; < 70 rearquitetar (não adianta polir copy).

## 7.2 Diagnóstico de oferta fraca (sintoma → componente)

| Sintoma reportado | Componente suspeito | Primeira ação |
|---|---|---|
| Tráfego bom, página não converte | Promessa/clareza ou ratio | Teste de repetição da promessa; revisar comparáveis |
| Converte mas com objeção de preço dominante | Valor percebido / commodity | PARTE II.3 (sair da comparação) |
| Muitos "vou pensar" | Motivo pra agir + risco | Deadline real; garantia espelhando o medo |
| Vende mas refund alto | Promessa inflada vs entrega | Realinhar promessa; quick win na 1ª semana |
| Vende barato, não escala | Modelo de preço | PARTE V.4 (subir com motivo) |
| Lead pergunta "quanto custa" antes de tudo | Commodity | Mecanismo único + naming |

---

# PARTE VIII: OFERTAS POR MODELO DE NEGÓCIO

## 8.1 High-ticket (mentoria, consultoria, > R$ 5k)

- Estrutura: aplicação → call de diagnóstico → oferta na call (application-only)
- Stack enfatiza ACESSO (proximidade, revisões, rede) e personalização; menos volume de material, mais profundidade
- Garantia: condicional de execução ou performance; incondicional só com filtro de entrada forte
- Página de aplicação (workflow #5 da SKILL) qualifica em vez de vender preço

## 8.2 Curso / infoproduto (R$ 297 a R$ 3k)

- Stack clássico: curso core + aceleradores (templates) + comunidade + bônus anti-objeção + garantia incondicional 14-30d
- Order bump no checkout (complemento de consumo imediato, ~10-20% do ticket) e upsell pós-compra (aceleração/proximidade); a POSIÇÃO desses elementos no funil é decisão do mos-funnel
- Parcelamento 12x como preço comunicado

## 8.3 Serviço / agência

- Produtizar: escopo fechado com nome e preço (pacote), em vez de "orçamento sob consulta"
- Âncora em custo de fazer errado (contratação errada, tráfego queimado)
- Garantia de performance com condições controláveis; piloto pago como tripwire

## 8.4 SaaS / recorrência

- Trial vs garantia: trial serve produto self-service; garantia de N dias serve onboarding assistido
- Anual com desconto real (2 meses grátis) + bônus de implementação no anual
- Decoy no plano do meio; preço por unidade de valor (por usuário, por projeto) alinhado ao ganho do cliente

## 8.5 E-commerce

- Kit/bundle como unidade de oferta (sobe ticket médio e diferencia de marketplace)
- Frete e brinde como componentes do stack (frete grátis acima de X é oferta, não logística)
- Garantia estendida além do CDC como diferencial explícito

---

# PARTE IX: EXEMPLOS PT-BR APLICADOS

## 9.1 Mentoria high-ticket (gestores de tráfego, R$ 12.000/6 meses)

```
PROMESSA: Operação de tráfego rodando com CPA controlado em 90 dias,
          com você auditado semanalmente (não sozinho).
MECANISMO: Método [Nome]: diagnóstico → matriz de criativos → escala por gatilho
STACK:
  1. 6 meses de mentoria em grupo, 2 calls/semana ......... (acesso/proximidade)
  2. Auditoria individual mensal da conta ................. (personalização)
  3. Biblioteca de criativos validados por nicho .......... (acelerador; "R$ 4.900:
     custo de produzir 40 criativos com designer")
  4. Planilha de gestão de CPA com alertas ................ (esforço ↓)
  5. Bônus anti-objeção "sem equipe": SOPs de contratação
     do primeiro gestor júnior ............................ (mata "não tenho braço")
GARANTIA: Condicional: participou das calls e implementou as auditorias
          por 90 dias sem melhora de CPA → devolução integral.
          (Incondicional de 7d do CDC coberta e citada à parte.)
PREÇO: R$ 12.000 (ou 12x R$ 1.197). Âncora: custo médio de 6 meses de
       agência (R$ 21.000+) sem transferência de competência.
AGIR AGORA: Coorte de 20 (limite real das auditorias individuais),
            onboarding dia [X].
```

## 9.2 Curso gravado (confeitaria lucrativa, R$ 497)

```
PROMESSA: Primeiras 10 encomendas pagas em 30 dias, começando na
          cozinha de casa.
STACK: curso core (7 módulos) + tabela de precificação automática
       ("mata o 'não sei cobrar'") + pack de fotos/legendas prontas pra
       Instagram ("mata o 'não sei divulgar'") + comunidade com feedback
       semanal + aula bônus de embalagem barata que valoriza o produto.
GARANTIA: Incondicional 21 dias ("assista o módulo 1 inteiro; se não for
          pra você, devolvo tudo").
PREÇO: 12x R$ 49,70 (comunicado) / R$ 497 à vista com brinde físico.
AGIR AGORA: Bônus de ação rápida (pack de fotos) só nas primeiras 48h;
            curso continua disponível depois, sem o pack.
```

---

# PARTE X: ANTI-PADRÕES E ERROS FATAIS

1. **Inflação de âncora**: stack "de R$ 30.000 por R$ 97". Ratio acima de ~15x zera a credibilidade de TODOS os números.
2. **Bônus canibal**: bônus mais desejado que o core (sinal de que o core está errado, ou o bônus deveria SER o produto).
3. **Garantia de marketing = mínimo legal**: anunciar os 7 dias do CDC como generosidade.
4. **Urgência reciclada**: "última turma" toda semana. A audiência aprende em 2 ciclos e para de responder a QUALQUER deadline seu.
5. **Oferta de ar**: arquitetar stack antes do produto/entrega existir (pre-flight do agent barra).
6. **Preço por espelhamento**: copiar preço do concorrente sem conhecer o modelo de custo/entrega dele.
7. **Stack de 12 itens**: volume no lugar de relevância; sobrecarga cognitiva e cheiro de filler.
8. **Promessa média pra público amplo**: especificidade de público permite promessa (e preço) maiores; o genérico compete por preço.
9. **Deadline sem plano de pós-deadline**: quem chega depois encontra o quê? Sem resposta, o deadline era teatro.
10. **Ignorar a segunda venda**: oferta que espreme a primeira compra (urgência agressiva, garantia hostil) mata LTV; a arquitetura considera a relação, não a transação.

---

# PARTE XI: REFERÊNCIAS CRUZADAS

| Quando o trabalho envolver... | Handoff para | O que passar |
|---|---|---|
| Escrever a página/anúncio/emails da oferta | `mos-copy` (KB PARTE II-C pra aplicação do stack em copy) | Handoff Context JSON completo |
| Posição da oferta na jornada (tripwire/core/upsell) | `mos-funnel` | Modelo, ticket, papel pretendido |
| Mecânica de abertura/fechamento, coortes | `mos-launch` | Mecanismo de urgência escolhido |
| Curriculum/entrega do infoproduto | `mos-infoproduct` | Promessa e obstáculos mapeados (Passo 1-2) |
| Validar demanda e faixa de preço antes | `mos-research` | Hipóteses de promessa e ticket |
| Testar preço/garantia com tráfego | `mos-ab-testing` | Variantes e métrica primária |
