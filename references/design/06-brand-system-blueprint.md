# 06. Brand System Blueprint Deep Reference (2026)

> Parte da stack de companions do `design-agent` (v4.0).
> Referência aplicada sobre construção de um sistema de marca completo: manifesto, missão, personas, voz, vocabulário, elevator pitches, logo, cor, tipografia, grid, fotografia, ilustração, ícones, motion, sonic, aplicações e governança.

**Quando consultar:** ao preencher `assets/templates/design/brand-guidelines.md.template`, auditar brand existente, iniciar rebrand, definir voz e tom, documentar regras de logo, criar paleta acessível, pairear fontes, especificar motion de marca ou estabelecer governança.

**Pré-requisitos:** `references/design/04-accessibility-wcag22.md` (§14), `references/design/05-motion-spec.md` (§22), `references/design/01-tokens-w3c-spec.md` (base §§ 11-16) e `assets/templates/design/brand-guidelines.md.template` (artefato final).

---

## Índice

1. Manifesto
2. Missão, Visão, Valores
3. Personas
4. Voz e Tom
5. Vocabulário
6. Elevator Pitches
7. Logo System
8. Logo Clear Space
9. Logo Minimum Size
10. Logo Don'ts
11. Paleta Primária
12. Paleta Secundária
13. Paleta Funcional
14. Contraste e Acessibilidade
15. Tipografia Famílias
16. Tipografia Hierarquia
17. Tipografia Pareamento e Regras
18. Grid e Layout
19. Direção de Fotografia
20. Sistema de Ilustração
21. Sistema de Ícones
22. Motion Principles
23. Sonic Brand
24. Aplicações Digital
25. Aplicações Print
26. Aplicações Merch
27. Aplicações Ambiente
28. Aplicações Embalagem
29. Co-branding
30. Governança de Marca

---

## 1. Manifesto

### O que é e por que importa

Manifesto é o documento emocional fundador da marca: três parágrafos que respondem qual dor existe no mundo, por que a marca existe e qual futuro ela promete. Não é slogan nem tagline. É o texto que um novo funcionário lê no primeiro dia e entende para que time entrou. Importa porque é o teste de decisão: quando a equipe precisa escolher entre duas direções com custos similares, o manifesto é a ponte.

### Framework decisório

Três parágrafos fixos, 300-450 palavras totais.

**Parágrafo 1. Tensão.** A dor, oportunidade ou contradição do mundo atual que justifica a marca. Evite "nós". Comece com "o mundo", "as pessoas". Concretize. Ruim: "Hoje o mundo muda rápido". Bom: "Todo ano, 40 milhões de pessoas mudam de cidade no Brasil e chegam precisando confiar em alguém".

**Parágrafo 2. Proposição.** Por que a marca existe frente a essa tensão. A marca é o agente, não o herói. Herói é o cliente. Marca é o guia.

**Parágrafo 3. Futuro.** O mundo que a marca promete criar. Tempo futuro ou presente aspiracional. Prometa o concreto grande.

### Exemplos

**Airbnb.** Rebrand de 2014 da DesignStudio trouxe "Belong Anywhere" como eixo: não tagline, tese. O símbolo Bélo combina cabeça (pessoa), pin (lugar), coração (amor) e A (marca), feito para ser redesenhado por qualquer pessoa.

**Stripe.** Manifesto implícito: "Increase the GDP of the internet." Documentação como obra de arte, paleta Cornflower Blue (#635BFF) navegando entre roxo da tecnologia e azul do banco tradicional porque Stripe é ponte.

**Linear.** Karri Saarinen descreve a marca como "software que parece profissional para engenheiros". Inter sans-serif em fundo preto, esfera gradiente roxa. Manifesto operacional em linear.app/method com princípios como "opinionated software".

**Duolingo.** Educação gratuita e divertida, tantas pessoas quanto possível. Duo, a coruja verde, é encarnação viva: "sweet tutor" vs "menacing coach".

**Patagonia.** "We're in business to save our home planet." Cada decisão (Earth Tax, "Don't Buy This Jacket") responde à frase.

### Common pitfalls

- Confundir manifesto com missão.
- Começar falando de si, não do mundo.
- Encher de jargão ("sinergia", "disrupção").
- Prometer o inalcançável sem concretizar.
- Escrever por comitê.
- Atualizar a cada pivô. Manifesto é âncora.

### Template de documentação

Três parágrafos (tensão / proposição / futuro) + origem (quem escreveu, quando, em resposta a que) + última revisão.

---

## 2. Missão, Visão, Valores

### O que é e por que importa

Se manifesto é emoção, missão/visão/valores é estrutura. Missão: o que a marca faz hoje. Visão: aonde quer chegar. Valores: princípios não negociáveis. Sistema operacional de decisão em escala.

### Framework decisório

**Missão:** uma frase no presente, 12-20 palavras. Bom: "Organizamos a informação do mundo e a tornamos universalmente acessível e útil." (Google). Ruim: "Ser o melhor player do mercado".

**Visão:** uma frase no futuro, 15-25 palavras. Bom: "Um mundo onde todas as lojas vendem online sem barreira técnica". Ruim: "Ser reconhecida globalmente como referência em inovação".

**Valores:** 3-5, cada um palavra forte + frase acionável. Evite clichês. Ruim: "Inovação". Bom: "Inovação incremental: fazemos o mesmo trabalho 1% melhor toda semana, não uma revolução por ano".

### Exemplos

**Stripe.** "Move with urgency and focus" (identificar a coisa mais importante e dar atenção desproporcional), "trust and amplify", "seek feedback". Cada um com descrição.

**Linear.** Linear Method inclui "build for the creators", "opinionated software", "less but better". Cada princípio tem artigo dedicado.

**Patagonia.** Qualidade, integridade, ambientalismo, justiça social. Cada um em decisões públicas (Earth Tax, Worn Wear, fechamento em dia de eleição).

**Notion.** "Tools for thought", "software as craft", "user sovereignty". O valor "craft" aparece em Inter, espaçamento de blocos, documentação cuidada.

### Common pitfalls

- Missão confusa com visão.
- Valores genéricos replicáveis a qualquer empresa.
- Mais de 5 valores.
- Valores nunca referenciados em reviews ou contratação.
- Reescrever missão a cada CEO novo.

### Template de documentação

Missão (1 frase presente) + Visão (1 frase futuro) + 3-5 Valores (palavra + frase acionável) + aplicação (onde referenciados: contratação, reviews, comitês).

---

## 3. Personas

### O que é e por que importa

Ser humano sintético que representa um segmento real. Tem nome, idade, contexto, dor, desejo, jeito de falar, quote. Existe para que decisões sejam tomadas em diálogo com pessoa específica, não com "o cliente" abstrato. Barreira real contra viés do criador.

### Framework decisório

**Regra de ouro:** persona nasce de pesquisa, não de opinião.

Fontes mínimas: 10+ entrevistas qualitativas por segmento, dados quantitativos (analytics, CRM), review de concorrência.

Número: 1 persona primária + 1-2 secundárias + 1 terciária opcional. Mais de 5 indica falta de foco.

Cada persona inclui nome (memorável), idade (faixa), contexto (onde vive, o que faz), dor principal (razão pela qual busca solução), o que quer (ganho concreto), como fala (vocabulário, canais), quote (frase real extraída de entrevista).

### Exemplos

**Airbnb.** Personas "Business Traveler", "Cultural Explorer", "Family Vacationer" em quadrantes motivação × grupo. Comunicação e direção de foto calibradas: home office ativa Business Traveler; brinquedos na estante ativam Family Vacationer.

**Stripe.** Persona primária é desenvolvedor sênior em time de engenharia. Site tem code snippets na primeira dobra; linguagem precisa sem ser jargonista.

**Duolingo.** Persona primária é aprendiz casual estudando 5-15 minutos por dia. Personalidade do Duo calibrada para esse perfil. Aprendiz sério de 2 horas odiaria Duo. Mas não é a persona primária.

### Common pitfalls

- Inventar persona sem entrevista.
- Persona demográfica pura ("mulher 30-45 classe AB"). Zero valor.
- Confundir buyer com user persona.
- Mais de 5 personas.
- Não atualizar a cada 18-24 meses.

### Template de documentação

Para cada persona (primária / secundária / terciária): nome, idade, contexto, dor principal, o que quer, como fala, quote (real), prioridade de decisão. Anexe fontes de pesquisa e última atualização.

---

## 4. Voz e Tom

### O que é e por que importa

Voz é o DNA verbal, não muda. Tom é o traje que a voz veste conforme contexto. Mesmo humano fala diferente no velório e no aniversário, mas é a mesma pessoa. Separar resolve dilemas: "podemos ser sérios em erro?" Sim, voz continua, tom muda.

### Framework decisório

**Voz:** 3-5 atributos adjetivais, cada um com descrição do que significa e do que não significa.

Matriz clássica (Nielsen Norman): funny vs sério, formal vs casual, respeitoso vs irreverente, entusiasmado vs factual.

**Tom:** matriz de contexto × tom.

| Contexto | Tom | Exemplo |
|----------|-----|---------|
| Onboarding | Acolhedor, entusiasmado | "Que bom ter você. Vamos começar." |
| Erro | Honesto, empático, acionável | "Algo não funcionou. O que fazer:" |
| Sucesso | Celebrador moderado | "Feito. Próximo passo: {{x}}." |
| CTA marketing | Urgente sem pressão | "Inscrição aberta até sexta." |
| Documentação técnica | Claro, preciso | "Execute {{comando}} no terminal." |
| Cobrança | Firme sem agressividade | "Sua mensalidade vence em 3 dias." |

### Exemplos

**Mailchimp.** Style guide aberto em styleguide.mailchimp.com: voz consistente no tempo, tom ajusta ao contexto emocional. Voz ativa, evitam passiva e jargão, preferem linguagem positiva. Humor subordinado à clareza; humor forçado evitado. Informal, mas "genuine and relates to customers' challenges" vem antes de engraçado.

**Duolingo.** Monotype descreve Duo como "charismatic owl whose personality ranges from playful encouragement to hilariously frustrated outbursts". Tom oscila entre "sweet tutor" e "menacing coach"; voz não muda. Feather Bold foi desenhada para carregar isso visualmente.

**Stripe.** Voz "clear, precise, friendly without being cute". Erros têm texto humano: quando pagamento falha, mensagem diz o motivo em linguagem humana e sugere próximo passo.

**Notion.** Voz "thoughtful, craft-oriented, empowering". Tom didático sem ser paternalista. Em lançamento, vira entusiasmado sem hipérbole.

### Common pitfalls

- Atributos genéricos ("amigável e profissional") sem gradiente.
- Cada canal com voz própria.
- Confundir voz com slogan.
- Nunca exemplificar.
- Não revisar voz após crescer.

### Template de documentação

Voz: 3-5 atributos com (significa X, não significa Y, exemplo). Tom: matriz de 6-8 contextos comuns com exemplos. Regras de escrita (ex: voz ativa, máximo 20 palavras por frase, zero jargão).

---

## 5. Vocabulário

### O que é e por que importa

Lista viva de palavras que a marca usa, que não usa e que banne. Importa porque linguagem molda percepção. "Host" em vez de "aluguel" diz algo sobre a marca. Vocabulário consistente é marca consistente.

### Framework decisório

Três listas: palavras on-brand (10-20), palavras off-brand (10-20), banned list (5-15) com motivo explícito.

Motivos típicos para banir: jargão corporativo sem tradução, clichê vazio, termo ofensivo, termo com conotação indesejada.

### Exemplos

**Airbnb.** On-brand: "host", "guest", "belong", "home", "stay", "local", "experience". Off-brand: "customer", "user", "room rental", "property", "landlord". Nunca se refere a quem hospeda como "proprietário" porque quer enquadrar a relação como humana, não transacional.

**Stripe.** On-brand: "developer", "integration", "API", "business", "transaction", "payment", "ledger". Off-brand: jargão bancário ("merchant acquirer", "PCI-compliant gateway") exceto em contextos técnicos.

**Duolingo.** On-brand: "learner", "lesson", "streak", "practice", "XP", "hearts". Off-brand: "student" (formal demais), "course" (acadêmico demais).

**Mailchimp.** Banned: jargão técnico de email sem explicação, linguagem agressiva de vendas, metáforas genéricas ("move the needle", "synergy").

### Common pitfalls

- Banir sem explicar motivo.
- Lista ultrapassada.
- Não revisar com suporte/vendas.
- Proibir palavra usada pelo público sem decisão consciente.

### Template de documentação

Três listas: on-brand (palavra + contexto), off-brand (palavra + alternativa), banned (palavra + motivo). Revisão a cada 6 meses.

---

## 6. Elevator Pitches

### O que é e por que importa

Quatro versões: 15s, 30s, 60s e tagline. Alguém será perguntado "o que vocês fazem?" e todos precisam ter resposta replicável.

### Framework decisório

- 15s (40-50 palavras): problema + solução + diferencial, sem jargão.
- 30s (75-90 palavras): adiciona prova (número, cliente, resultado).
- 60s (150-180 palavras): adiciona visão futura.
- Tagline (5-8 palavras): frase memorável condensando a tese.

Regra: todos da empresa sabem o pitch de 15s de cor.

### Exemplos

- **Airbnb:** "Belong Anywhere". 5 palavras.
- **Stripe:** "Payments infrastructure for the internet." 7 palavras.
- **Linear:** "Purpose-built tool for planning and building products." 8 palavras.
- **Duolingo:** "Free language education for the world." 7 palavras.
- **Notion:** "The connected workspace where better, faster work happens." 8 palavras.

### Common pitfalls

- Adjetivos vazios ("inovadora plataforma líder de mercado").
- Mencionar tecnologia antes de benefício.
- Tagline trocada a cada campanha.
- Pitch que só o fundador sabe contar.

### Template de documentação

15s / 30s / 60s / tagline + onde aparecem (logo-lockup, hero, assinatura, apresentações comerciais, pitches de investimento).

---

## 7. Logo System

### O que é e por que importa

Conjunto de aplicações oficiais: primário, símbolo isolado, lockups (horizontal, vertical, com tagline) e versões de cor (full color, mono preto, mono branco, inverso). Logo aparece em contextos de favicon 16×16 a outdoor. Sem sistema, cada contexto inventa.

### Framework decisório

- **Primary:** logo completo (símbolo + wordmark). Padrão com espaço suficiente.
- **Secondary (symbol/mark):** só o símbolo. Favicon, avatar social, espaços pequenos.
- **Lockups:** horizontal (padrão), vertical (espaços estreitos), com tagline (homepage).
- **Versões de cor:** full color (oficial), mono preto (uma cor), mono branco (fundos escuros/foto), inverso silhueta (raro).

### Exemplos

**Airbnb.** Bélo isolado (favicon), wordmark "airbnb" em Cereal, lockup horizontal. Símbolo funciona sozinho em tamanho pequeno porque tem silhueta forte e simétrica.

**Stripe.** Wordmark em tipografia custom rounded-geometric desde rebrand 2016. Sem símbolo separado oficial. Em contextos pequenos, usa "S" estilizada. Produtos derivados (Payments, Atlas, Capital) têm logo próprio mantendo família visual (estúdio Landscape).

**Linear.** Esfera gradiente roxa como símbolo, wordmark "Linear" em Inter bold. Esfera isolada como favicon e avatar.

**Duolingo.** Sistema rico: Duo como símbolo/mascote, wordmark em Feather Bold, múltiplos estados emocionais catalogados como variações oficiais.

**Notion.** "N" estilizada em duas formas (serifa no wordmark, letterform simples no símbolo).

### Common pitfalls

- Ter só uma versão (primary color).
- Não ter símbolo. Logo horizontal longo não cabe em favicon 16px.
- Cada time gerar variações.
- Lockup com tagline usado em tudo.
- Versão legada circulando.

### Template de documentação

Primary (padrão) + Symbol (favicon, avatar) + Lockups (horizontal/vertical/com tagline) + versões de cor + link para arquivos oficiais + formatos (SVG, PNG transparente, EPS, PDF).

---

## 8. Logo Clear Space

### O que é e por que importa

Zona de respeito ao redor do logo onde nenhum elemento pode entrar. Protege legibilidade e impacto. Sem regra, designers encostam logo em imagem ou texto.

### Framework decisório

Regra matemática: clear space = altura de uma letra de referência do wordmark (ou altura do símbolo em casos de símbolo isolado). Letra de referência: maiúscula mais alta; x-height em wordmarks all-lowercase; altura do símbolo quando isolado.

### Exemplos

**Airbnb.** Clear space derivado da altura do Bélo. Em qualquer aplicação, mantém espaço equivalente à altura do símbolo ao redor do lockup.

**Stripe.** Clear space = altura da letra "t" do wordmark. Em aplicações densas (docs, dashboards), aplicado rigorosamente para preservar leitura.

**Google.** Clear space público: altura do "G" do Google ao redor do wordmark. Aplicado em todos os produtos Google.

### Common pitfalls

- Não documentar unidade de medida.
- Ignorar em aplicações pequenas sem documentar exceções.
- Co-branding sem respeitar clear space de ambos. Ver §29.

### Template de documentação

Espaço mínimo X (altura da letra de referência). Nenhum elemento invade, exceto aplicações muito pequenas documentadas e co-branding (ver §29).

---

## 9. Logo Minimum Size

### O que é e por que importa

Abaixo de certo tamanho, logo perde legibilidade. Minimum size define tamanho por mídia e o que fazer abaixo (usar símbolo isolado).

### Framework decisório

| Mídia | Tamanho mínimo |
|-------|----------------|
| Digital web desktop | 120 px largura |
| Digital web mobile | 80 px |
| Favicon | 16 × 16 px (símbolo isolado) |
| Print alta resolução | 25 mm largura |
| Impressão tecido | 40 mm |
| Gravação em metal | 15 mm |
| Bordado | 30 mm altura |

Regra de ouro: abaixo do mínimo, use símbolo.

### Exemplos

**Airbnb.** Bélo funciona em 16×16 px porque foi desenhado para. Simplicidade (4 elementos geométricos) preserva reconhecimento.

**Linear.** Esfera gradiente funciona como favicon e ícone de app. Forma reduzida preserva identidade até miniatura.

### Common pitfalls

- Não testar em favicon 16px.
- Lockup vertical em camiseta pequena. Texto some.
- Não ter versão simplificada para bordado ou gravação.
- Ignorar densidade de pixel em impressão mobile retina.

### Template de documentação

Tabela por mídia (web desktop/mobile, favicon, print, camiseta, caneca, gravação, bordado) com tamanho mínimo. Abaixo do mínimo: símbolo isolado.

---

## 10. Logo Don'ts

### O que é e por que importa

Lista explícita de violações. Designer recém-chegado precisa ver exemplos do que NÃO fazer, com exemplo visual e justificativa curta.

### Framework decisório

Dez violações mínimas em qualquer brand guide:

1. Não distorça proporções (estique, esprema, rotacione).
2. Não mude as cores (use paletas oficiais).
3. Não aplique sombras, gradientes ou efeitos.
4. Não use sobre fundos de baixo contraste (mínimo 4.5:1).
5. Não coloque dentro de formas geométricas.
6. Não reproduza em baixa qualidade.
7. Não combine com outro logo sem espaçamento (ver §29).
8. Não reescreva ou trace o wordmark.
9. Não altere a proporção símbolo/wordmark.
10. Não use versões antigas.

### Exemplos

**Airbnb.** Brand book encoraja personalização do Bélo pela comunidade, mas com regras: personalização em contextos específicos (campanha de hosts, arte comunitária), nunca em material oficial. Distingue "personalização encorajada" de "violação proibida".

**Google.** Lista pública muito detalhada, com exemplos visuais para cada. Um dos mais rigorosos da indústria.

**NASA.** Lista icônica no guidelines de 1975 (The Graphics Standards Manual). Exemplos visuais explícitos. Virou referência do campo.

### Common pitfalls

- Lista só textual, sem exemplo visual.
- Don'ts genéricos sem contexto.
- Não atualizar após observar violações reais.
- Don'ts punitivos.

### Template de documentação

Lista numerada com 10+ violações, cada uma com exemplo visual + justificativa breve. Link para ativos oficiais no brand portal.

---

## 11. Paleta Primária

### O que é e por que importa

Conjunto de cores que encarnam a marca: dominante + variações (dark, light) + neutros. Cor é reconhecimento instantâneo (Tiffany Blue, Coca-Cola Red, Rausch Pink da Airbnb).

### Framework decisório

Estrutura mínima: primary (dominante), primary dark (hover/active), primary light (background sutil).

Formato documentação:

| Nome | Hex | RGB | HSL | CMYK | Pantone | Uso |
|------|-----|-----|-----|------|---------|-----|
| Primary | #635BFF | 99,91,255 | 244,100%,68% | 70,70,0,0 | 2091 C | CTA, links, destaques |
| Primary Dark | #4F47E5 | 79,71,229 | 243,75%,59% | 78,78,0,0 | 2091 XC | Hover, active |
| Primary Light | #EBE9FF | 235,233,255 | 244,100%,96% | 15,15,0,0 | 2092 C | Background sutil |

Psicologia comum: azul (confiança, tech); verde (natureza, crescimento); vermelho (energia, urgência); roxo (luxo, criatividade); laranja (entusiasmo); preto (sofisticação).

### Exemplos

**Airbnb Rausch.** Primary "Rausch" (#FF5A5F), coral-pink vibrante. Nome homenageia Rausch Street em SF. Substituiu azuis e cinzas corporativos. Decisão: cor humana e quente em vez das comuns de tech. Comunica que Airbnb é empresa de pessoas.

**Stripe Cornflower Blue.** Primary #635BFF, roxo-azul. Navega entre azul do banco tradicional e roxo da tecnologia. Complementam com Downriver (#0A2540) e Black Squeeze (#F6F9FC).

**Duolingo Verde.** Primary #58CC02. Escolha aconteceu quase por brincadeira entre cofundadores. Verde acabou servindo à brand story (crescimento, aprendizado, natureza da coruja).

**Linear Roxo.** Esfera gradiente roxa (dois tons com transição sutil). Casa com Inter sobre fundo preto. Comunica "tecnologia premium, focada".

**Notion Preto e Branco.** Quase ausente de cor saturada. "Ferramenta neutra, conteúdo do usuário é herói".

### Common pitfalls

- Cor só por estética.
- Copiar concorrente.
- Usar cor sem contraste AA mínimo.
- Documentar só em hex (CMYK, Pantone e HSL são necessários).
- Não testar em monitores reais.

### Template de documentação

Tabela com Primary / Primary Dark / Primary Light com hex, RGB, HSL, CMYK, Pantone, uso. Texto explicando origem da escolha (por que estas cores, o que comunicam). Aplicações típicas (CTA, links, progress bars, highlights).

---

## 12. Paleta Secundária

### O que é e por que importa

Cores de suporte. Não rouba foco da primária, mas amplia gama. Inclui secondary + 1-3 accents + neutros (escala de cinzas).

### Framework decisório

| Papel | Descrição | Quantidade |
|-------|-----------|------------|
| Secondary | Cor de suporte | 1 |
| Accents | Destaques pontuais | 2-4 |
| Neutrals | Escala de cinzas | 9-11 tons |

Neutrals recomendados (escala Tailwind-like):

| Token | Hex | Uso |
|-------|-----|-----|
| Neutral 0 | #FFFFFF | Background mais claro |
| Neutral 50 | #F9FAFB | Background alternativo |
| Neutral 100 | #F3F4F6 | Background de seção |
| Neutral 200 | #E5E7EB | Bordas claras |
| Neutral 400 | #9CA3AF | Texto desativado |
| Neutral 500 | #6B7280 | Texto secundário |
| Neutral 700 | #374151 | Texto destaque |
| Neutral 900 | #111827 | Texto hero |
| Neutral 1000 | #000000 | Preto puro (raro) |

### Exemplos

**Stripe.** Secundária inclui Downriver (#0A2540) como dark anchor, Black Squeeze (#F6F9FC) como background quase-branco. Accents variam por produto.

**Airbnb.** Coral mais suave, verde-água, bege-creme. Em ilustrações e fotografia styling, nunca competindo com Rausch.

**Notion.** Escala de cinzas com pequenos accents pastéis para highlight e cover colors.

**Linear.** Muito restrita: esfera primária em gradiente + tons de cinza/preto. Accent apenas em status colors.

### Common pitfalls

- Secundária briga com primária.
- Accents demais (5+).
- Escala de cinzas pobre (3-4 tons).
- Neutros com temperatura inconsistente.
- Não testar em dark mode.

### Template de documentação

Secondary (1) + Accents (2-4, cada um com hex e uso) + Neutrals (escala completa, ver `tokens.json`). Declarar temperatura dos neutros (quente/neutro/frio).

---

## 13. Paleta Funcional

### O que é e por que importa

Cores reservadas para feedback de sistema: sucesso, aviso, erro, informação. Carregam significado convencionado. Não usamos para decoração.

### Framework decisório

| Significado | Nome | Hex padrão | Uso |
|-------------|------|------------|-----|
| Sucesso | Success | #10B981 | Confirmações, completado |
| Aviso | Warning | #F59E0B | Atenção, pendente |
| Erro | Danger | #EF4444 | Erros, destrutivo |
| Informação | Info | #3B82F6 | Alertas neutros, dicas |

Regras:
- Não use verde/vermelho/amarelo para decoração.
- Cor nunca é único signal. Acompanhe com ícone + texto.
- Se primária é verde, escolha outro verde para Success.

Variações por background:

| Cor | Light mode | Dark mode |
|-----|-----------|-----------|
| Success bg | #D1FAE5 | #065F46 |
| Success text | #065F46 | #D1FAE5 |
| Success icon | #10B981 | #34D399 |

### Exemplos

**Stripe.** Artigo "Designing accessible color systems" (2018) detalha sistema. Success = verde #059669; Error = vermelho #DF1B41; Warning = âmbar #FFA500. Todos passam AAA em combinações padrão.

**GitHub.** Success (#2DA44E), error (#CF222E), warning (#9A6700), info (#0969DA). Consistentes entre light e dark via shifts calibrados.

**Material Design.** Success não é categoria oficial (Google prefere "positive feedback via primary"), Error sim.

### Common pitfalls

- Verde para CTA e Success. Usuário confunde.
- Vermelho em botão de destaque. Cria ansiedade.
- Ignorar daltonismo. Sempre acompanhe com ícone.
- Não testar em dark mode.

### Template de documentação

Tabela Success/Warning/Danger/Info (hex + uso) + regras (feedback de sistema, ícone+texto, testar light/dark, contraste AA mínimo) + variações por background.

---

## 14. Contraste e Acessibilidade

### O que é e por que importa

Contraste é a diferença de luminosidade entre texto e fundo. WCAG 2.2: AA (4.5:1 texto normal, 3:1 grande) e AAA (7:1 e 4.5:1). Sistema inacessível exclui 15-20% dos usuários e é litigável (ADA, EAA).

**Referência completa:** `references/design/04-accessibility-wcag22.md`.

### Framework decisório

| Nível | Texto normal | Texto grande | UI elements |
|-------|-------------|--------------|-------------|
| AA | 4.5:1 | 3:1 | 3:1 |
| AAA | 7:1 | 4.5:1 | não aplica |

Matriz de pares aprovados (exemplo):

| Texto | Fundo | Ratio | WCAG |
|-------|-------|-------|------|
| Neutral 900 (#111827) | Neutral 0 (#FFFFFF) | 19.5:1 | AAA |
| Neutral 700 (#374151) | Neutral 0 | 11.2:1 | AAA |
| Neutral 500 (#6B7280) | Neutral 0 | 4.84:1 | AA |
| Primary (#635BFF) | Neutral 0 | 4.7:1 | AA |
| Neutral 400 (#9CA3AF) | Neutral 0 | 2.7:1 | FAIL |

### Exemplos

**Stripe.** "Designing accessible color systems" reconstruiu o sistema para garantir que qualquer par pré-aprovado passasse AA. Cada token tem variações light/dark testadas.

**IBM Carbon.** Tokens `color-contrast-1` a `color-contrast-10`, cada par tem contrast ratio documentado. Ferramenta interna valida uso.

**Airbnb DLS.** Matriz pública mostrando combinações aceitáveis por peso tipográfico.

### Common pitfalls

- Testar só no branco puro.
- Ignorar texto sobre imagem.
- Não documentar pares proibidos.
- Aprovar par borderline (4.51:1). Margem quebra em bordas de pixel.
- Esquecer contraste em UI components (borders, icons, focus).

### Template de documentação

Matriz de pares aprovados (texto, fundo, ratio, WCAG) + pares proibidos com motivo FAIL + regras adicionais (peso mínimo 400/regular em 16px+, cor nunca é único signal, focus ring 2px contraste 3:1, teste em modo daltonismo). Ferramenta: https://webaim.org/resources/contrastchecker/

---

## 15. Tipografia Famílias

### O que é e por que importa

Famílias definem o tom visual verbal. Marca séria não usa Comic Sans. Escolha cuidadosa tem impacto enorme em percepção.

### Framework decisório

Quatro papéis:

| Papel | Uso | Exemplo |
|-------|-----|---------|
| Display | Títulos >=32px, hero, editorial | Playfair, Fraunces, Reckless |
| Body | Texto corrente, artigos | Source Serif, Merriweather, Charter |
| UI | Botões, menus, interface | Inter, SF Pro, Geist, Roboto |
| Mono | Código, dados numéricos | JetBrains Mono, SF Mono, Geist Mono |

Duas famílias é ideal. Mais que três é ruído (mono adicional aceitável).

Licenciamento:

| Fonte | Licença | Hosting | Custo |
|-------|---------|---------|-------|
| Inter | SIL OFL | Google Fonts, rsms.me/inter | $0 |
| SF Pro | Apple Font License | Apple dev | $0 (Apple apps) |
| Circular | Lineto proprietary | Lineto direct | $$$$ |
| Custom | Proprietary | Self-hosted | $$$$-$$$$$ |

### Exemplos

**Airbnb Cereal.** Custom da Dalton Maag (2018). Substituiu Circular (paga). Decisão estratégica: controle total, diferenciação, zero custo por uso. Sans-serif geométrica com detalhes humanistas.

**Stripe Camphor.** Custom baseada em Soleil. Geométrica-arredondada, mesma família do wordmark. Produto técnico para devs pede tipografia precisa e legível em tela.

**Linear Inter.** Inter (Rasmussen Andersson, gratuita). Referência em UI sans-serif para telas: x-height alto, espaçamento generoso, hinting excelente. Reforça "software profissional que respeita engenheiros".

**Duolingo Feather.** Custom da Monotype (2018-2019), inspirada em penas de coruja. Cada terminal tem suavização que evoca pluma. Carrega personalidade lúdica do Duo.

**Notion Inter.** Inter também. Decisão pragmática: ferramenta neutra, priorizar legibilidade, x-height alto reduz fadiga em sessões longas.

### Common pitfalls

- Fonte paga sem contrato licenciado.
- Escolher typeface só "porque é bonita" sem pensar em legibilidade.
- Misturar 4+ famílias.
- Não testar em tamanhos extremos (12px caption, 96px hero).
- Display pesada em corpo.
- Não documentar fallback fonts.

### Template de documentação

Para cada papel (Display/Body/UI/Mono): fonte, pesos disponíveis, uso, fallback fonts. Tabela de licenças e hosting com custo.

---

## 16. Tipografia Hierarquia

### O que é e por que importa

Escala de tamanhos + pesos que organiza informação. Sem hierarquia, leitor não sabe onde olhar.

### Framework decisório

Escala modular com fator consistente (1.25 "major third", 1.333 "perfect fourth", 1.5 "perfect fifth"). Base 16px.

Com fator 1.25: 12 (caption), 16 (body), 20, 24 (H4), 30 (H3), 36 (H2), 48 (H1), 60 (display).

| Nível | Tamanho | Line-height | Peso | Uso |
|-------|---------|-------------|------|-----|
| Display | 64px | 1.05 | Extrabold (800) | Hero extraordinário |
| H1 | 48px | 1.1 | Bold (700) | Página principal |
| H2 | 36px | 1.2 | Bold (700) | Seções principais |
| H3 | 30px | 1.25 | Semibold (600) | Subseções |
| H4 | 24px | 1.3 | Semibold (600) | Grupos internos |
| H5 | 20px | 1.4 | Medium (500) | Headers de blocos |
| H6 | 18px | 1.4 | Medium (500) | Headers menores |
| Body Large | 18px | 1.5 | Regular (400) | Lead paragraph |
| Body | 16px | 1.5 | Regular (400) | Parágrafos |
| Small | 14px | 1.5 | Regular (400) | Legendas |
| Caption | 12px | 1.4 | Regular (400) | Notas, labels mínimos |

### Exemplos

**Airbnb.** Cereal Bold 48-72px hero; Medium 32-40px H2; Book 16-18px body. Line-height generoso (1.4-1.5) para conforto em listings.

**Stripe.** Camphor Semibold 48-56px hero; Medium 32-36px H2; Book 16-18px body. Em docs técnicas, hierarquia mais contida (H1 32px, H2 24px) porque densidade é maior.

**Linear.** Inter. Hero 48-56px; H2 32px; body 14-16px (menor que Airbnb, interface mais densa).

**Duolingo.** Feather Bold em hero 56-64px com tracking apertado (reforça personalidade "fofa"). Body 16-18px em Feather Light.

### Common pitfalls

- Escala sem fator consistente (H1=50, H2=30, H3=20).
- Pesos demais (7 pesos). 3-4 é suficiente.
- Line-height igual para todos. Heading 1.1-1.2, body 1.5-1.6.
- Heading Heavy em tamanhos pequenos.
- Não documentar margin-top/bottom.

### Template de documentação

Escala modular (fator + base 16px) + tabela H1-H6 + Body/Small/Caption (tamanho, line-height, peso, margin, uso) + letter-spacing por nível + rhythm vertical em múltiplos de 4px.

---

## 17. Tipografia Pareamento e Regras

### O que é e por que importa

Pareamento combina duas famílias de forma complementar. Regras universais governam composição: line-length, tracking, aspas, hifenização.

### Framework decisório

Regras universais:

1. Nunca mais de 2 famílias (mono adicional aceitável).
2. Pareamento A: serif display + sans body.
3. Pareamento B: sans display pesada + sans body leve (mesma família, pesos diferentes).
4. Pareamento C: serif body + sans display (editorial invertido).
5. Line-length ideal: 50-75 caracteres por linha.
6. Hierarquia via tamanho + peso, não só cor (daltonismo).
7. Tracking moderado em body (0 a 0.01em).
8. Aspas tipográficas sempre (" " em vez de " ").
9. Hifenização por idioma.

Quando usar cada:

| Contexto | Pareamento |
|----------|------------|
| Editorial longo | Serif body + sans display |
| Produto digital (SaaS) | Sans everywhere |
| Marca técnica | Sans UI + mono para dados |
| Luxo | Serif alta + sans pequena (ou só serif) |
| Kids / entertainment | Sans arredondada + custom playful |

### Exemplos

**Airbnb.** Sans everywhere (Cereal). Decisão pragmática: opera em dezenas de idiomas e contextos. Uma família simplifica stack.

**Stripe.** Sans everywhere (Camphor + mono para código). Código é central, mono é prioritária. Display não é necessário porque tom é sóbrio.

**Linear.** Inter em todos os papéis. Exemplo canônico de "sans everywhere". Regular e Medium cobrem 90% do uso.

**The New York Times.** Pareamento A clássico: Cheltenham (serif) em headings + Imperial/Georgia (serif) em body + Franklin (sans) em UI. Três famílias, cada uma em seu domínio.

**Mailchimp.** Cooper BT (display serif pesada retrô-humanista) + Graphik (sans body limpa). "Divertido mas sério", coerente com voz.

### Common pitfalls

- Duas serifs com personalidades diferentes.
- Duas sans geométricas muito parecidas (DIN + Montserrat).
- Serif display em corpo. Cansativo.
- Sans UI em hero editorial. Perde peso.
- Ignorar line-length.
- Aspas burras (" "). Detalhe amador.

### Template de documentação

Pareamento oficial (Display/Body/UI/Mono) + estrutura escolhida + justificativa. Regras universais numeradas (máximo 2 famílias, line-length 50-75, hierarquia por tamanho+peso, tracking por nível, aspas tipográficas, hifenização).

---

## 18. Grid e Layout

### O que é e por que importa

Grid é a estrutura invisível que organiza layout. Sem grid, cada tela inventa sua estrutura. Cinco canvases cobrem aplicações: web desktop, mobile, print, social, merch/embalagem.

### Framework decisório

**Canvas 1. Web desktop.** Max width: 1200-1440px. Colunas: 12. Gutter: 24px. Margin: 64px. Breakpoints: 1440/1024/768/480/360.

**Canvas 2. Mobile.** Colunas: 4. Gutter: 16px. Margin: 16px. Safe area: respeite notch, status bar, home indicator.

**Canvas 3. Print.** Grid 6 ou 12 colunas. Margens: 20mm top, 15mm lateral. Bleed: 3mm.

**Canvas 4. Social media.** Ver `references/design-specs.md`. Instagram post: 1080×1350 (4:5). Stories: 1080×1920 (9:16). LinkedIn post: 1200×628.

**Canvas 5. Merch e embalagem.** Caso-a-caso (camiseta, caneca, caixa).

Espaçamento vertical (rhythm): múltiplos de 4px. Escala: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128.

### Exemplos

**Apple.com.** Grid 12 colunas, max-width variável (828px artigo, 1440px product page). Margens generosas (96px+ lateral). Rhythm em múltiplos de 8px.

**Airbnb.com.** Grid 12 colunas, max-width 1120px. Hero full-bleed com conteúdo contido. Listings em cards: 4 colunas desktop, 2 tablet, 1 mobile.

**Stripe.com.** Grid 12 colunas, max-width 1080px em conteúdo, 1440px em hero. Docs técnicas em layout de duas colunas: conteúdo + sidebar sticky.

**Linear.app.** Grid simples, max-width 1024px em marketing. Produto usa layout adaptativo. Rhythm em 4px base.

### Common pitfalls

- Grid só no desktop.
- Gutter inconsistente.
- Margens pequenas demais.
- Não documentar safe areas mobile.
- Grid rígido demais. Documente exceções (hero full-bleed, gallery).
- Rhythm ad-hoc (17px, 23px, 29px).

### Template de documentação

Cinco canvases (web desktop, mobile, print, social media, merch/embalagem) cada um com max-width, colunas, gutter, margin, breakpoints, safe area, bleed, especificações. Rhythm vertical em múltiplos de 4px ou 8px.

---

## 19. Direção de Fotografia

### O que é e por que importa

Foto carrega 60% da percepção em canais visuais. Direção documenta estilo, paleta, composição, presença de pessoas e o que evitar.

### Framework decisório

**Estilo.** Adjetivos + mood board. Ex: "cinematográfico, luz natural, paleta desaturada, composição aberta".

**Paleta visual.** Temperatura (quente/neutro/frio). Contraste (alto/médio/baixo). Cores banidas.

**Composição.** Enquadramento (frontal/lateral/3-4/top-down). Profundidade de campo. Ponto focal (terços, centro, assimétrico).

**Pessoas.** Diversidade obrigatória (idade, etnia, gênero, corpo, habilidade). Expressões autênticas. Contexto real.

**Evitar.** Stock photos genéricas; sorrisos artificiais direto pra câmera; iluminação clínica; composições simétricas centralizadas; filtros datados.

### Exemplos

**Airbnb.** Luz natural, locais reais (apartamentos de hosts), gente em contexto. Evita stock. Paleta desaturada deixa Rausch em contraste. Composição aberta.

**Apple.** Direção estrita: fundo branco ou ambiente premium, luz estúdio, produto em hero. Pessoas em momento aspiracional. Cor do produto sempre correta.

**Patagonia.** Atletas reais (não modelos), ambientes extremos reais, imperfeições preservadas (suor, lama, rugas). Evita foto perfeita demais. Paleta terrosa.

**Duolingo.** Foto menor que ilustração. Quando aparece, estudante real em contexto casual (café, trem, sofá), enquadramento candid, luz natural.

### Common pitfalls

- Mood board não documentado.
- Stock como default.
- Pessoas todas similares.
- Inconsistência entre shoots.
- Não briefar fotógrafo com paleta.
- Editar além do necessário (HDR, saturação artificial).

### Template de documentação

Estilo (adjetivos + 3-5 refs visuais) + paleta visual (predominância, temperatura, contraste, banido) + composição (enquadramento, DOF, ponto focal) + pessoas (diversidade, expressões, contexto) + lista de evitar + mood board vivo + fotógrafos aprovados.

---

## 20. Sistema de Ilustração

### O que é e por que importa

Ilustração é heroi de marcas digitais (Stripe, Notion, Shopify, Dropbox). Mais controle que foto, escala melhor, mais barata de atualizar, carrega personalidade.

### Framework decisório

**Estilo.** Escolha um e se mantenha fiel: flat 2D, isométrico, line-art minimalista, texturizado handmade, 3D estilizado.

**Paleta.** Exclusivamente da paleta oficial (§§ 11-13).

**Construção.** Geometria base (círculos, quadrados, triângulos, orgânicas); peso de linha consistente; cantos (radius ou agudos); sombras (sim/não). Escolha uma opção de cada.

**Bank.** Biblioteca central. Antes de criar nova, verifique se existente serve.

### Exemplos

**Stripe.** Isométrico em Stripe Press e Atlas. Paleta reduzida, peso de linha consistente, formas geométricas puras. Ilustra conceitos abstratos (transações, fluxos) com clareza. Equipe + estúdios parceiros (Landscape).

**Dropbox.** Reposicionamento de 2017 introduziu ilustração handmade texturizada com traço aparente e paleta vibrante. Marcou virada na indústria tech.

**Notion.** Minimalista, line-art, paleta quase-neutra com accents. Coerente com "software as craft".

**Shopify.** Híbrido: flat 2D + texturas sutis + paleta mais saturada que Stripe. Comunica "commerce acessível".

### Common pitfalls

- Mix de estilos no mesmo produto.
- Paleta fora da da marca.
- Ilustração ad-hoc por designer.
- Não briefar ilustradores externos com construção.
- Bank desorganizado.

### Template de documentação

Estilo escolhido + paleta (oficial) + construção (geometria, peso linha, cantos, sombras, outline) + link para bank + processo para nova ilustração (checar bank, brief, ilustrador, review, add ao bank) + ilustradores aprovados.

---

## 21. Sistema de Ícones

### O que é e por que importa

Ícones são ilustrações ultra-pequenas que representam ações ou conceitos. Um ícone mal desenhado quebra UI inteira.

### Framework decisório

**Metáfora.** Linha fina, contorno sólido, duotone, flat, outline + fill.

**Grid.** Base 24×24 px. Keyline 20×20 (padding 2px). Stroke weight 1.5px consistente. Cantos radius 2px (arredondados) ou 0px (agudos). Escolha um.

**Anatomia.** Só formas primárias (linha, círculo, quadrado, triângulo, arco). Zero detalhes sub-pixel. Testado em 16, 24, 32, 48 px.

**Bank.** Biblioteca centralizada com nome, categoria, SVG otimizado.

**Acessibilidade.** Ícone standalone tem `aria-label`. Ícone + texto é sempre preferível.

### Exemplos

**Phosphor Icons.** Helena Zhang e Tobias Fried. Outline, 6 pesos (Thin a Bold), grid 256×256, 1200+ ícones.

**Heroicons.** Tailwind Labs (Steve Schoger, Adam Wathan). Duas variações (outline e solid), grid 24×24, traço 1.5px.

**Lucide.** Fork open-source de Feather. Outline, 1000+ ícones, adotado por shadcn/ui.

**Linear icons.** Proprietário, outline 1.5px, cantos arredondados 2px.

**Airbnb Cereal Icons.** Arredondados com traço 2px em base 24px. Cantos suaves casam com estética humanista.

### Common pitfalls

- Misturar conjuntos diferentes (Material + FontAwesome + custom).
- Ícones em tamanhos inconsistentes.
- Stroke weight variável.
- Ícone sem texto em UI. Usuário adivinha.
- Não otimizar SVG.
- Não testar em dark mode.

### Template de documentação

Metáfora + grid (base 24x24, keyline 20x20, stroke, cantos) + anatomia (só primárias, zero sub-pixel, tamanhos testados) + link para bank + formato (SVG otimizado, viewbox, currentcolor) + acessibilidade (aria-label, aria-hidden).

---

## 22. Motion Principles

### O que é e por que importa

Motion é tempo e comportamento de mudança na interface. Marca pode ter cores e fontes iguais à outra, mas o jeito de mover distingue a personalidade.

**Referência completa:** `references/design/05-motion-spec.md`.

### Framework decisório

Personalidade em motion (arquétipos):

- Energética e bouncy: spring com overshoot, durações 300-500ms, easing elástico. Duolingo.
- Sutil e elegante: ease-out clássico, durações 150-250ms, sem overshoot. Apple, Linear.
- Rígida e institucional: linear ou ease-out minimal, durações 100-200ms. Bloomberg.
- Brincalhona: rotação, scale, rebote. Slack, Duolingo.

Tokens essenciais (resumo de §§ 2-3 de motion-spec):

| Token | Valor | Uso |
|-------|-------|-----|
| `duration.instant` | 100ms | Acknowledgement imediato |
| `duration.fast` | 150ms | Hover, tooltip |
| `duration.normal` | 250ms | Modal enter, toast |
| `duration.slow` | 400ms | Page transition |
| `easing.standard` | `cubic-bezier(0.4, 0, 0.2, 1)` | Default A → B |
| `easing.decelerate` | `cubic-bezier(0, 0, 0.2, 1)` | Entry |
| `easing.accelerate` | `cubic-bezier(0.4, 0, 1, 1)` | Exit |
| `easing.emphasized` | `cubic-bezier(0.2, 0, 0, 1)` | Transição importante |

Grammar: entrada (fade-in + subtle scale ou slide-up); saída (fade-out + scale-down); feedback (micro-bounce em click, shake em erro); continuidade (shared element transitions).

Reduced motion: sempre respeite `prefers-reduced-motion: reduce`.

### Exemplos

**Linear.** Sutil e elegante. Transições 150-200ms, ease-out. Zero overshoot. Coerente com "software profissional".

**Duolingo.** Bouncy. Duo pula, lições completam com confete, barra de progresso tem bounce. Coerente com "learning should be fun".

**Apple.** Sutil com timing distintivo. Durações 200-400ms com easing custom. Page transitions em iOS têm continuity: elemento clicado "cresce" para virar próxima tela.

**Stripe.** Mínima e funcional. Apenas o necessário para acknowledgement e feedback. Zero motion decorativa.

### Common pitfalls

- Motion sem tokens.
- Durações longas (500ms+) em interação frequente.
- Motion que persiste em erro.
- Não respeitar reduced-motion. Violação WCAG 2.3.3.
- Bouncy em tudo.

### Template de documentação

Personalidade escolhida + tokens (duração, easing) + grammar (entrada, saída, feedback, continuidade) + reduced motion (disable / reduce) + ferramenta de implementação (CSS / Framer Motion / Lottie / GSAP) + referência completa.

---

## 23. Sonic Brand

### O que é e por que importa

Som que a marca produz: jingle, UI sounds, voz de assistente. Nem toda marca precisa. Se tem aplicação sonora, precisa ser tão cuidada quanto visual.

### Framework decisório

Aplica quando: produtos com áudio (música, podcast, streaming); apps com UI sounds (jogos, pagamentos, mensageria); spots TV/rádio; música de espera, call center; assistentes de voz.

Não aplica quando: site institucional sem música, dashboard, docs técnicas, apps silenciosos.

Elementos: jingle principal (2-8 segundos); UI sounds (success, error, notification, message); música de espera; voz de assistente.

Princípios: volume moderado; curtos (< 500ms UI); sempre mute opcional; consistente entre plataformas; coerente com personalidade da marca.

### Exemplos

**Netflix Ta-Dum.** Dois tons (E-G#) em 2 segundos. Lon Bender. Reproduzido antes de cada título original. Virou "abertura de streaming".

**Intel Bong.** Cinco notas desde 1994. Uma das sonic identities mais reconhecidas do mundo.

**iPhone Marimba.** Ringtone Marimba (Apple, Kelly Jacklin). Associado ao iPhone desde 2007.

**Mastercard Sonic Logo.** Redesigned em 2019 por Mike Shinoda (Linkin Park) + agência. Três notas. Coerente em qualquer idioma.

**Duolingo UI sounds.** Success (xilofone ascendente), error (tom cômico), lesson complete (fanfarra curta). Carregam personalidade lúdica do Duo.

### Common pitfalls

- Som sem mute.
- Som longo (2+ segundos) em ação frequente.
- Inconsistência entre plataformas.
- Licença musical ignorada.
- Som ofensivo culturalmente.

### Template de documentação

Jingle + UI sounds (success/error/notification/message) + música de espera + princípios + licenças. Se não tem aplicação sonora: N/A.

---

## 24. Aplicações Digital

### O que é e por que importa

Site institucional, app/produto, email, redes sociais. Como a marca se manifesta em cada meio.

### Framework decisório

**Site institucional.** Hero: logo + tagline + CTA. Tipografia: display em H1, sans body resto. Paleta: neutros predominam, primary em CTAs. Imagens: foto + ilustração (§§ 19-20). Performance: Core Web Vitals verdes (LCP < 2.5s, INP < 200ms, CLS < 0.1). A11y: WCAG 2.2 AA.

**App/produto.** Tema primary em ações principais. Dark mode obrigatório. Motion sutil (<= 250ms). Responsivo 320-1920 px.

**Email.** Largura máxima 600px. Fallback fonts (Arial, Georgia). Dark mode compatível (`@media (prefers-color-scheme: dark)`). CTA único ideal. Alt text em imagens.

**Social media.** Dimensões em `references/design-specs.md`. Assinatura visual consistente. Cronograma documentado. Tom adaptado por plataforma, voz preservada.

### Exemplos

**Stripe.com.** Hero com código real, CTA "Start now", paleta neutra + Cornflower Blue em CTAs. Camphor em hero, body, UI. Docs em layout duas colunas. Dark mode no painel mas não no site marketing.

**Linear.app.** Site minimalista, hero "Linear is built for high-performance product teams", esfera roxa. Inter everywhere. Produto em dark mode default.

**Airbnb.com.** Hero rotativo com foto de destino, Rausch em CTA. Cards com foto dominante. Cereal. Mobile web e app têm paridade.

**Duolingo.com.** Hero com Duo + tagline. Verde primary em CTAs. Ilustrações onipresentes. App mobile é produto primário; site é marketing.

**Notion.so.** Hero com demo de produto. Inter. Paleta quase-neutra. Dark mode no produto e marketing.

### Common pitfalls

- Site e app com identidade diferente.
- Email sem dark mode.
- Social media com fonte diferente da web.
- Cronograma ad-hoc.
- Não adaptar voz por plataforma.

### Template de documentação

Para cada canal (site, app, email, social): hero/estrutura, tipografia, paleta, performance target, a11y, dark mode, breakpoints, tom por plataforma.

---

## 25. Aplicações Print

### O que é e por que importa

Print ainda existe em 2026. Cartão, papel timbrado, folder, outdoor, sinalização, flyer. Cada um com regras específicas.

### Framework decisório

**Cartão de visita.** Formato 85×55 mm (BR) ou 89×51 mm (US). Frente: logo + nome + cargo. Verso: tagline + contato + QR. Papel 300-400 g/m² (Casca de ovo, Reciclato, Couché fosco).

**Papel timbrado.** A4 (210×297 mm) ou Carta. Margens 20mm sup/inf, 15mm lateral. Papel 80-100 g/m² off-white.

**Folder / brochura.** A5 tri-fold, A4 quad-fold, A3 dobrado. Grid 6 colunas por página. Papel 150 g/m² couchê semi-mate.

**Outdoor / large format.** Hierarquia simplificada (1-2 elementos dominantes). Fonte mínima 120pt para leitura a 20m. Contraste máximo. Formato 9×3 m (BR standard), 6×2 m.

### Exemplos

**Airbnb impresso.** Guias de cidade para hosts (início 2010s). Couchê fosco, ilustrações próprias, Cereal, Rausch em destaques. Decisão premium: reforça autoridade.

**Stripe em conferências.** Material impresso minimalista para Sessions. Logo + frase em tipografia grande, paleta reduzida. Coerente com estética digital.

**Nike.** Outdoors icônicos. "Just do it." com atleta em tamanho real, logo pequeno no canto. Reproduzível em qualquer formato.

**Patagonia Black Friday 2011.** "Don't Buy This Jacket" full-page no NYT. Jaqueta + copy longo sobre impacto ambiental. Canal impresso reforçando valores.

### Common pitfalls

- Logo em baixa resolução (72dpi) em print.
- CMYK errado (exportar de RGB). Cor mudada.
- Bleed esquecido.
- Fonte só digital sem licença de impressão.
- Texto minúsculo em outdoor.

### Template de documentação

Cartão (formato, papel, frente/verso) + timbrado (A4, margens) + folder (formato, grid, papel) + outdoor (hierarquia, fonte mínima) + regras comuns (CMYK, bleed 3mm, 300dpi mínimo, teste em impressora real).

---

## 26. Aplicações Merch

### O que é e por que importa

Merch é merchandising: produtos físicos com a marca (camisetas, canecas, adesivos, bonés, canetas, blocos, chaveiros, ecobags). Grande multiplicador de awareness se bem feito, constrangimento se mal feito.

### Framework decisório

**Camisetas.** Logo no peito esquerdo ou centralizado. Tamanho 80-120 mm largura. Tecido algodão 100% ou blend. Técnica silkscreen (durável), DTG (full color), bordado (premium).

**Canecas.** Logo + tagline opcional. Mínimo 40mm. Impressão sublimação ou decalque. Material cerâmica branca ou esmaltada.

**Adesivos.** Formato redondo, retangular, die-cut. Versão logo primário ou símbolo isolado. Material vinil (outdoor) ou PVC (indoor).

**Outros brindes.** Canetas, blocos, chaveiros, ecobags, garrafas, capas de notebook. Sempre versão oficial. Ajustar tamanho, testar legibilidade.

### Exemplos

**GitHub Octocat plushie.** Mascote em pelúcia distribuído em conferências. Pequeno acessório de alta lembrança.

**Stripe Atlas merch.** Camisetas e adesivos para founders que usaram Atlas. Qualidade premium, silkscreen, tipografia limpa. Low-key, bem feito.

**Notion.** Linha leve (camisetas, meias, capas de notebook) com logo minimalista. Parcerias com comunidade. Material de qualidade.

**Figma.** Adesivos (Figgy) e camisetas em Config. Personalidade lúdica, qualidade premium.

### Common pitfalls

- Logo em merch de baixa qualidade.
- Logo grande demais.
- Cores fora da paleta por limitação técnica.
- Não testar proporção antes.
- Merch caro demais (tiragem pequena).
- Mensagem desatualizada após pivô.

### Template de documentação

Camisetas (posição, tamanho, tecido, técnica) + canecas (posição, mínimo, impressão) + adesivos (formato, material) + outros brindes (biblioteca central) + fornecedores aprovados (contato, preços, prazos).

---

## 27. Aplicações Ambiente

### O que é e por que importa

Como a marca se manifesta em espaços físicos: fachada, sinalização externa, wayfinding interno, escritório, loja. Cada decisão carrega mensagem.

### Framework decisório

**Fachada / sinalização externa.** Letreiro iluminado (backlight) ou não (frontlight). Material: acrílico, alumínio composto, aço, madeira. Iluminação LED ou neon. Dimensão proporcional ao edifício. Respeitar legislação municipal.

**Sinalização interna (wayfinding).** Ícones + tipografia (fonte UI). Contraste alto (WCAG 2.2 AA). Altura mínima de texto 15mm para leitura a 3m. Pictograma universal.

**Escritório / espaço.** Paleta neutros + accent em poucos pontos. Arte na parede: ilustrações do sistema. Ambiente reforça a voz: casual (madeira, plantas, pufes), formal (aço, vidro, salas fechadas), criativo (cores fortes, áreas lúdicas).

### Exemplos

**Apple Store.** Vidro, mesa de madeira clara, logo central retroiluminado. Design de loja virou case de estudo. Ambiente é produto.

**Google (escritórios).** Ambientes lúdicos (colorful, bean bags, jogos). Cada escritório regional tem elementos locais (arte local, referências culturais).

**Airbnb HQ (Brannan Street, SF).** Salas de reunião replicam listings reais. Conceito: quem trabalha na Airbnb vive o produto. Premiado em arquitetura corporativa.

### Common pitfalls

- Fachada ilegível a distância.
- Iluminação não pensada.
- Sinalização sem padrão.
- Escritório em desacordo com voz.
- Arte sem curadoria.
- Não considerar acessibilidade física.

### Template de documentação

Fachada (letreiro, material, iluminação, dimensão) + sinalização interna (wayfinding, contraste, altura mínima, pictogramas) + escritório (paleta, materiais, arte, mobiliário) + acessibilidade física (rampa, elevador, banheiros, braile, alerta sonoro).

---

## 28. Aplicações Embalagem

### O que é e por que importa

Se a marca tem produto físico, embalagem é o primeiro toque do cliente. Caixa, etiqueta, manual. Cada elemento comunica antes do produto ser usado.

### Framework decisório

Estrutura: caixa externa, embalagem interna, manual/instruções, etiqueta, sticker de selo/lacre.

Material: papelão (reciclável), kraft (sustentável), plástico recycled (evitar virgin), tecido (luxury), metal (premium).

Impressão: offset (qualidade, tiragem grande), flexografia (kraft), serigrafia (tecido), foil stamping (dourado), relevo/embossing (tátil).

Hierarquia: 1) logo + nome do produto; 2) descrição curta; 3) especificações técnicas; 4) brand elements.

Sustentabilidade (obrigatória em 2026): materiais recicláveis, minimizar camadas, tintas à base de água, selos FSC / Cradle to Cradle / B Corp.

### Exemplos

**Apple.** Embalagem de iPhone é lendária: caixa branca, tipografia precisa, ritmo de abertura (unboxing documentado em vídeos de milhões). Papel de qualidade, tinta preta única, ajuste milimétrico. Embalagem tornou-se parte do produto.

**Glossier.** Pink Glossier, pop de tecido reutilizável, tipografia custom. UGC de clientes desembalando virou marketing orgânico.

**Patagonia.** Minimalista, papel reciclado, informação ambiental no kraft. Selo Fair Trade. Coerência com "saving home planet".

**Lush.** Muitos produtos sem embalagem (Naked), outros em pote reutilizável. Manifesto ambiental impresso.

**Nintendo Switch.** Caixa projetada para revelar produto em ordem pensada (Joy-Con aparecem antes do dock). Unboxing como onboarding.

### Common pitfalls

- Embalagem excessiva. Percepção negativa em 2026.
- Materiais inconsistentes (caixa premium + insert barato).
- Tipografia pequena demais na etiqueta.
- Erro de versão.
- Não testar durabilidade.
- Certificações falsas ou não renovadas.

### Template de documentação

Estrutura (caixa + interna + manual + etiqueta + lacre) + material + impressão + hierarquia + sustentabilidade (% reciclado, % reciclável, tintas, certificações) + teste de durabilidade + fornecedores aprovados. Se não tem produto físico: N/A.

---

## 29. Co-branding

### O que é e por que importa

Duas marcas juntas: parceria comercial, certificação, produto colaborativo. Sem regras, a visualmente mais forte domina.

### Framework decisório

Quando fazer: parcerias comerciais oficiais (Spotify + Uber); eventos conjuntos; produtos colaborativos (Nike x Off-White); certificações (B Corp, Fair Trade).

Quando NÃO: parceria informal, controvérsia incompatível, só licenciamento.

Regras:

1. Logos lado a lado, separados por linha divisória vertical (1px).
2. Espaçamento = clear space do nosso (§8).
3. Logos em mesma altura visual (x-height do wordmark).
4. Se um tem muito mais peso visual, diminua o outro proporcionalmente.
5. Nunca combine em sobreposição.
6. Ordem: cliente/parceiro à esquerda, nós à direita (ou conforme contrato).
7. Clear space de ambos respeitado; usar o maior.

Tipos de lockup: horizontal (A | B), vertical (A / divisória / B), com "x" (A x B), com "by" (B by A), com "powered by" (A / Powered by B).

### Exemplos

**Nike x Off-White (Virgil Abloh).** Swoosh + "x" + quadrado Off-White. Proporções equilibradas. Virou padrão em sneaker culture.

**Spotify + Uber.** Colab 2014: playlist Spotify no Uber. Logos em igualdade, com "+" entre.

**Intel Inside.** PC OEM (Dell, HP, Lenovo) + selo "Intel Inside". Intel pagava parte do marketing em troca de co-branding. Transformou CPU commodity em marca de peso.

**Stripe Atlas.** Logo Stripe + logo Atlas com separador vertical. Atlas é produto dentro de Stripe, mas tem identidade própria para co-branding interno.

**Selos de certificação.** B Corp, Fair Trade, FSC. Regras rígidas: tamanho mínimo, proporção, cores exatas.

### Common pitfalls

- Logos em tamanhos diferentes sem justificativa.
- Sem separador.
- Ordem errada por contrato.
- Clear space ignorado.
- Versão errada de um dos logos.
- Co-branding em campanha efêmera sem contrato.

### Template de documentação

Quando usar (lista) + regras numeradas + tipos de lockup (horizontal, vertical, "x", "by", "powered by") + aprovações (contrato, briefing review pelo guardião §30, logos em alta resolução) + link para biblioteca aprovada.

---

## 30. Governança de Marca

### O que é e por que importa

Quem decide, como se decide, como se mantém, como evolui a marca no tempo. Sem governança, brand system decai em 12-18 meses.

### Framework decisório

**Guardião:** pessoa/equipe com autoridade final. Startup early-stage: fundador/designer. Scale-up: Head of Design, Head of Brand, CMO. Empresa grande: Brand Council + CCO.

Responsabilidades: aprovar novas aplicações; auditar em campo trimestralmente; manter brand portal (ativos, templates, fontes); evoluir guidelines; treinar novos integrantes.

**Processo de revisão:** self-review com checklist (logo §§ 7-10, cor §§ 11-14, tipo §§ 15-17, a11y §14) → peer-review → guardian review → publish + archive (sign-off por escrito).

**Turnaround:** rotineiro 24h; campanha 48-72h; grande impacto (OOH, TV, rebrand) 1-2 semanas.

**Versionamento (semver):** MAJOR (X.0.0) rebrand, mudança de logo ou paleta primária; MINOR (x.Y.0) adição de paleta secundária, nova família, novas aplicações; PATCH (x.y.Z) correção, ajuste de token, atualização de exemplo.

Frequência de revisão: a cada 12 meses mínimo, ou a cada release importante, ou a cada mudança estratégica.

### Exemplos

**Apple.** Governance centralizada, rigorosíssima. Cada aplicação em contexto público passa por revisão. Guidelines em developer.apple.com/design. Penalidades reais (MFi program).

**Google.** Brand Studio centralizado. Guidelines para produtos internos padronizados. Material Design como base técnica.

**NASA.** Design guidelines de 1975 (The NASA Graphics Standards Manual), reimpressas em 2023. Documento icônico, governança federalizada por décadas.

**Airbnb.** Guidelines em brand.airbnb.com. Guardian: Design Leadership. Community brand book para hosts customizarem Bélo em limites definidos.

**Linear.** Guidelines em linear.app/brand. Governance com Karri Saarinen e design team. Mudanças em release notes.

### Common pitfalls

- Sem guardião nomeado.
- Sem processo. Aprovação ad-hoc no Slack.
- Sem versionamento.
- Sem changelog.
- Portal desatualizado.
- Não treinar. Novo funcionário aprende por osmose.
- Guidelines descolados da realidade.

### Template de documentação

Guardião (nome, email, equipe) + brand portal (link) + processo de revisão (4 passos) + turnaround (3 níveis) + versionamento (MAJOR/MINOR/PATCH) + frequência + changelog (versão, data, mudança, aprovada por) + treinamento (onboarding, workshop anual, Slack channel) + enforcement.

---

## Conclusão

Este blueprint cobre os 30 capítulos canônicos de um brand system completo. Cada capítulo tem: definição e importância, framework decisório, exemplos reais (Airbnb, Stripe, Linear, Duolingo, Notion, Mailchimp, Apple, Patagonia, Nike, Netflix, Google, GitHub, Figma, Spotify, Uber, Intel, NASA, NYT, Shopify, Dropbox, Lush, Glossier, Nintendo, Mastercard), armadilhas comuns e template de documentação.

### Integrações com outros companions

| Seção | Companion relacionado |
|-------|----------------------|
| §14 Contraste | `references/design/04-accessibility-wcag22.md` |
| §§ 11-16 Cor e tipografia | `references/design/01-tokens-w3c-spec.md` |
| §22 Motion | `references/design/05-motion-spec.md` |
| §24 Aplicações Digital | `references/design/02-atomic-design-playbook.md` |
| §30 Governança | `references/design/03-ds-governance.md` |

### Artefato final

Todo o trabalho culmina no preenchimento de `assets/templates/design/brand-guidelines.md.template`. Use este documento como guia pedagógico e o template como produto. Revise a cada 12 meses ou a cada mudança estratégica relevante.

A marca boa não é a que tem o logo mais bonito. É a que tem a disciplina mais consistente.
