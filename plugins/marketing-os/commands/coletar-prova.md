---
description: "Monta o kit para coletar depoimentos e cases de clientes: roteiro de entrevista, mensagem de pedido, modelo de case com números verificáveis e termo de autorização de uso (CONAR e LGPD). Use quando pedirem depoimentos, prova social ou cases de clientes."
argument-hint: "<produto ou serviço> [quem anuncia: profissão ou categoria] [canal do pedido: WhatsApp, email, formulário]"
---

# /coletar-prova: Depoimentos e cases com autorização

Prova social forte vem de cliente real, com resultado que se comprova e autorização por escrito. Este command monta o kit de coleta: a entrevista que tira a história e os números, o pedido que o cliente responde, o modelo de case e o termo de autorização. A base legal está em `references/compliance-br.md`.

## Inputs (pergunte o que faltar)

1. **Produto ou serviço** e o resultado que ele entrega.
2. **Quem anuncia**: se for profissional de saúde, advogado ou psicólogo, as regras mudam muito (ver abaixo). Se `workspace/brand/perfil.md` existir, a categoria regulada está lá.
3. **Canal do pedido**: WhatsApp, email, formulário ou conversa ao vivo.
4. **Onde a prova vai aparecer**: página de vendas, anúncio, post, apresentação comercial.

## Regras que valem para todo depoimento

- Genuíno, comprovável e autorizado por escrito (CONAR, art. 27, §9º). Consumidor comum fala só da própria experiência (Anexo Q).
- Depoimento sintético feito com IA é proibido na Hotmart (item 4.19) e é enganoso pelo CDC (art. 37).
- Autorização de uso de nome, imagem e voz com base no consentimento da LGPD: livre, informado, para finalidade determinada, em cláusula destacada e revogável a qualquer momento (arts. 7º, I, e 8º).
- Resultado individual acompanha a frase de que resultados variam.

## Categorias com regra própria

| Quem anuncia | O que muda |
|---|---|
| Médico | Repost de depoimento de paciente vale como post do médico: sóbrio, sem superlativo nem promessa. Antes e depois só educativo, sem identificar o paciente e com autorização (CFM 2.336/2023, arts. 8º e 14) |
| Dentista | Imagem de paciente só com TCLE; antes e depois só diagnóstico e conclusão (CFO-196/2019) |
| Nutricionista | Imagem corporal atribuindo resultado é proibida, mesmo com autorização (CFN 599/2018, art. 58) |
| Psicólogo | A Nota Técnica CFP 1/2022 desaconselha depoimento mesmo com consentimento escrito; nada que identifique o atendido |
| Advogado | Caso concreto para oferta de serviço é vedado (Provimento OAB 205/2021, art. 6º) |

Nessas categorias, o kit troca "depoimento de resultado" por prova permitida: tempo de atuação, formação verificável, conteúdo educativo, avaliações da plataforma quando a regra do conselho aceitar.

## Dispatch

Single message, dois agents em paralelo (as entregas são independentes):

```
Agent(subagent_type: "mos-storytelling", prompt: "Monte o roteiro de entrevista para extrair um case de cliente de [produto ou serviço]. Quem anuncia: [categoria]. Onde o case vai aparecer: [destino].

Entregue:
1. Roteiro de entrevista em 3 blocos (antes, virada, depois), 10 a 14 perguntas abertas, cada uma com o objetivo e uma pergunta de aprofundamento. Inclua perguntas que tragam número verificável (tempo, dinheiro, quantidade) e a objeção que o cliente tinha antes de comprar.
2. Modelo de case em markdown: contexto do cliente, problema, o que tentou antes, por que escolheu, o que fez, resultado com número e prazo, frase literal do cliente, e o campo 'como comprovar' (print, relatório, nota fiscal).
3. Versões de uso do mesmo case: frase curta para anúncio, parágrafo para página de vendas, roteiro de 30 s para vídeo.

Regras: não invente números nem falas; marque com [preencher] o que depende do cliente. Siga references/compliance-br.md para a categoria.")

Agent(subagent_type: "mos-copy", prompt: "Monte a parte de pedido e autorização do kit de coleta de depoimentos para [produto ou serviço]. Quem anuncia: [categoria]. Canal do pedido: [canal].

Entregue:
1. Mensagem de pedido no canal [canal], curta e pessoal, em 2 versões (cliente recente e cliente antigo), com o motivo do pedido e o que o cliente ganha em participar. Se o cliente receber qualquer benefício pelo depoimento, a menção vira publicidade e precisa ser identificada (Guia CONAR de Influenciadores 2026).
2. Lembrete de acompanhamento para quem não respondeu.
3. Termo de autorização de uso de depoimento, nome, imagem e voz: finalidade determinada (onde e por quanto tempo), declaração de que o depoimento é verdadeiro e reflete a experiência do cliente, cláusula destacada de consentimento (LGPD, art. 8º), direito de revogar a qualquer momento e como fazer isso, e campo de assinatura com data.
4. Checklist de publicação: autorização assinada arquivada, prova do número guardada, frase de que resultados variam, identificação de publicidade se houve benefício ao cliente.

Base: references/compliance-br.md (CONAR art. 27, §9º, e Anexo Q; LGPD arts. 7º e 8º; regra do conselho da categoria). Avise que o termo é modelo e não substitui revisão jurídica.")
```

## Saída (consolidação do orquestrador)

1. Kit em quatro partes: pedido, entrevista, modelo de case e termo de autorização, mais o checklist de publicação.
2. Se a categoria tem regra própria, a lista de provas permitidas no lugar do depoimento de resultado.
3. Salve em `workspace/brand/provas/kit-coleta.md` no projeto do usuário e crie `workspace/brand/provas/registro.md` com uma tabela de controle (cliente, data da autorização, onde pode ser usado, prova do número, validade).
4. Próximos passos: `/checar-compliance` na peça que usar o case; `/otimizar-copy` para encaixar a prova na página.

## Quality Gates

Aplique os gates globais do SKILL.md do Marketing OS ao texto do kit. Falas de cliente reproduzidas no case ficam como o cliente disse, entre aspas.

## Por que esse dispatch

O `mos-storytelling` é dono da entrevista e da estrutura narrativa do case; o `mos-copy` é dono do pedido, do termo e das versões curtas. As duas partes não dependem uma da outra, então rodam em paralelo. A regra jurídica vem da mesma referência de compliance que os outros especialistas usam.
