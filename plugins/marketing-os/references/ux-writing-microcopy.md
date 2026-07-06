# Guia Completo de UX Writing e Microcopy

## Sumário
1. [Fundamentos de UX Writing](#fundamentos-de-ux-writing)
2. [Diferença entre UX Writing e Copywriting](#diferença-entre-ux-writing-e-copywriting)
3. [Categorias de Microcopy](#categorias-de-microcopy)
4. [Frameworks de UX Writing](#frameworks-de-ux-writing)
5. [Design Conversacional](#design-conversacional)
6. [UX Writing para Mobile](#ux-writing-para-mobile)
7. [Métricas de UX Writing](#métricas-de-ux-writing)
8. [Exemplos de Excelência](#exemplos-de-excelência)
9. [Ferramentas](#ferramentas)

---

## Fundamentos de UX Writing

### O que é UX Writing?

UX Writing é a arte de criar textos claros, concisos e úteis que guiam usuários através de interfaces digitais. Cada palavra tem um propósito: reduzir fricção, esclarecer ações e criar experiências intuitivas.

### Os 3 C's do UX Writing

| Princípio | Definição | Por que importa |
|-----------|-----------|-----------------|
| **Clarity (Clareza)** | Textos fáceis de entender na primeira leitura | Métrica #1 de UX writing. Se o usuário precisa reler, o design falhou |
| **Conciseness (Concisão)** | Eficiência nas palavras, não apenas brevidade | Remove palavras que não agregam valor. Usuários escaneiam, não leem |
| **Consistency (Consistência)** | Mesmo tom, terminologia e padrões | Cria familiaridade e reduz carga cognitiva |

### Princípios Adicionais

- **Utilidade (Usefulness)**: Todo texto deve ter um propósito claro
- **Voz da Marca**: Consistente com personalidade e valores
- **Empatia**: Considera modelos mentais, emoções e habilidades dos usuários

### Boas Práticas Gerais

```
✓ Use linguagem simples e direta
✓ Prefira voz ativa (diz exatamente quem faz o quê)
✓ Evite jargão técnico desnecessário
✓ Escreva para escaneabilidade (textos curtos, idéias limitadas)
✓ Use verbos de ação (Download, Send, Create)
✓ Seja específico, não genérico

✗ Evite redundância
✗ Não use "autenticando" se "verificando" funciona
✗ Não use "bufferizando" se "carregando" é claro
✗ Evite sentenças longas e complexas
```

### Considerações para 2025-2026

**IA no UX Writing:**
- IA pode acelerar rascunhos e variações
- Ainda exige contexto, compreensão de produto e revisão humana
- Especialmente crítico em momentos sensíveis e casos extremos
- 34% dos adultos nos EUA usaram ChatGPT em 2025 (dobro de 2023)

---

## Diferença entre UX Writing e Copywriting

| Aspecto | UX Writing | Copywriting |
|---------|------------|-------------|
| **Objetivo** | Guiar e facilitar ações | Persuadir e vender |
| **Extensão** | Micro (botões, mensagens, labels) | Macro (páginas, emails, anúncios) |
| **Contexto** | Interface de produto | Marketing e vendas |
| **Métrica** | Taxa de conclusão, erros, tempo | Conversão, cliques, vendas |
| **Tom** | Funcional, útil, claro | Emocional, persuasivo, criativo |

**Exemplo:**
- **Copywriting**: "Transforme seu negócio com nossa plataforma revolucionária! 50% OFF por tempo limitado!"
- **UX Writing**: "Criar conta" (botão), "Enviando..." (loading), "Conta criada com sucesso" (confirmação)

---

## Categorias de Microcopy

### 1. Button Labels (CTAs)

**Princípios:**
- Use verbo + objeto: "Download report", "Add to cart", "Continue to payment"
- Seja específico, não genérico
- Indique o que acontece a seguir
- Inclua texto secundário quando necessário

#### Exemplos Before/After

```
GENÉRICO vs ESPECÍFICO:
✗ Before: "Submit"
✓ After: "Send invoice"
Resultado: +18% de cliques (ferramenta B2B)

✗ Before: "Click Here"
✓ After: "Download Free Report"

✗ Before: "Continue"
✓ After: "Continue to payment"

✗ Before: "OK"
✓ After: "Save changes"
```

#### Templates de CTAs

```
VALOR + URGÊNCIA:
• Claim Your Free Trial
• Get Instant Access
• Unlock Exclusive Content

AÇÃO + RESULTADO:
• Download your report
• Get a quote now (melhor que "Submit")
• Start your free trial

ESPECÍFICO + CONTEXTO:
• Send invoice (+ "We'll email your client a copy")
• Create account (+ "No credit card required")
• Download (+ "PDF, 2.5 MB")
```

---

### 2. Error Messages

**Princípios:**
- Balance brevidade com clareza
- Priorize transparência em erros de sistema
- Tenha paciência com erros do usuário
- Explique COMO resolver, não apenas O QUE está errado

#### Tipos de Erro

**Validação de Formulário:**
```
✗ Before: "Invalid email"
✓ After: "This email format isn't recognized. Try: example@email.com"

✗ Before: "Password must be 8 characters"
✓ After: "Almost there! Make sure your password has at least 8 characters"

✗ Before: "Error"
✓ After: "We couldn't save your changes. Please try again"
```

**Erros de Sistema:**
```
✗ Before: "Error 500"
✓ After: "Our servers are temporarily unavailable. We're working to resolve this quickly"

✗ Before: "Failed to load"
✓ After: "We couldn't load your data. Check your connection and try again"

✗ Before: "Something went wrong"
✓ After: "We couldn't complete this action. Try refreshing the page"
```

**404 Errors:**
```
✗ Before: "404 - Page not found"
✓ After: "We're sorry, that page can't be found. Let's get you back on track:"

Elementos de um bom 404:
• Seja empático (não culpe o usuário)
• Explique o erro em linguagem simples
• Ofereça próximos passos claros
• Mantenha tom consistente com marca
• Use visuais coerentes
```

#### Best Practices para Erros

```
✓ Use inline validation (feedback em tempo real)
✓ Forneça microcopy preventivo (evite erros antes que aconteçam)
✓ Seja específico sobre o problema
✓ Ofereça solução clara
✓ Mantenha tom encorajador, não punitivo

✗ Não use jargão técnico
✗ Não culpe o usuário
✗ Não seja vago ("Failed", "Error")
```

---

### 3. Empty States

**Princípios:**
- Transforme momentos vazios em oportunidades
- Guie o usuário para a próxima ação
- Use ilustrações + texto
- Regra: 2 partes instrução, 1 parte personalidade

#### Tipos de Empty State

**First-time Use:**
```
✗ Before: "No data"
✓ After: "Start by adding your first project"

✗ Before: "This folder is empty"
✓ After: [Ilustração de upload]
        "Drag and drop your first file"
        [Botão: Upload file]
```

**No Data / Zero Results:**
```
✗ Before: "No results found"
✓ After: "We couldn't find anything matching 'search term'"
        "Try different keywords or check your spelling"

✗ Before: "Empty"
✓ After: "No messages yet"
        "Your inbox will show new messages here"
```

**No Items / Empty List:**
```
✗ Before: "You don't have any data assets"
✓ After: "Start by adding data assets"

✗ Before: "0 contacts"
✓ After: "Add your first contact to get started"
        [Botão: Add contact]
```

#### Exemplos de Excelência

**Slack:**
```
Before (redesign): Tela em branco com dicas mínimas
After: Ilustrações convidativas + guias integrados
       "Say hi to yourself" (sugestão de primeira ação)
```

**Pinterest:**
```
Before: Boards vazios, usuário precisa buscar manualmente
After: Perguntas sobre interesses no signup
       Boards pré-populados com pins relevantes
       Sugestões de boards para seguir
```

**Dropbox:**
```
Before: "This folder is empty" em tela branca
After: Área grande de drag-and-drop
       Ilustração amigável
       Botão proeminente "Upload your first file"
```

---

### 4. Onboarding Flows

**Princípios:**
- Welcome users sem sobrecarregar
- Progressive disclosure (mostre o necessário, quando necessário)
- Celebre pequenas vitórias
- Guie para o "aha moment" rapidamente

#### Estrutura de Onboarding

```
1. WELCOME
   "Welcome to [Product]!"
   "Let's get you set up in 2 minutes"

2. VALUE PROPOSITION
   "Here's what you can do:"
   • [Benefício 1]
   • [Benefício 2]
   • [Benefício 3]

3. SETUP STEPS
   "Step 1 of 3: [Ação]"
   [Instrução clara]
   [Botão: Continue]

4. FIRST ACTION
   "You're all set! Try [ação] to get started"
   [Guia interativo]

5. SUCCESS
   "Great job! You've [conquista]"
   [Próximos passos]
```

#### Templates

```
WELCOME:
• "Welcome! Let's personalize your experience"
• "You're in! Here's what to do first"
• "Hi [Name]! Ready to get started?"

TUTORIAL:
• "Tap here to [ação]"
• "This is where you'll find [recurso]"
• "Try it: [ação específica]"

COMPLETION:
• "You're all set! Here's what's next"
• "Nice work! You've completed setup"
• "Ready to dive in?"
```

---

### 5. Tooltips e Helper Text

**Princípios:**
- Tooltips = explicações breves on-hover/tap
- Helper text = prompts dentro ou perto de campos
- Use apenas quando necessário (não repita óbvio)
- Mantenha curto e direto

#### Tooltips

```
✓ Use para:
  • Definir termos não familiares
  • Fornecer contexto adicional
  • Explicar ícones/elementos visuais

✗ Evite para:
  • Repetir texto de botão
  • Informações críticas (use inline)
  • Textos longos (difícil de ler)

EXEMPLOS:
✗ "Click to submit" (no botão "Submit")
✓ "Your changes will be saved immediately" (explicação útil)

✗ "Settings" (no ícone de engrenagem óbvio)
✓ "Advanced filters: Date range, categories, tags" (contexto útil)
```

#### Helper Text

```
✓ Use para:
  • Requisitos de formato (senha, telefone)
  • Explicar por que você pede a informação
  • Fornecer exemplos do input esperado

✗ Evite:
  • Texto genérico ("Enter text here")
  • Substituir labels (use em conjunto)
  • Jargão técnico

EXEMPLOS:
✗ "Type something"
✓ "e.g., john.smith@company.com"

✗ "Enter password"
✓ "At least 8 characters with 1 number and 1 symbol"

✗ "Phone"
✓ "We'll text you a verification code"
```

#### Placeholder Text

```
PRINCÍPIOS:
• Seja específico e descritivo
• Forneça exemplo do formato esperado
• Não substitua labels
• Deve desaparecer quando usuário digita

EXEMPLOS:
✗ "Enter text here"
✓ "Search by name, email, or company"

✗ "Phone number"
✓ "(555) 123-4567"

✗ "Enter email"
✓ "you@example.com"
```

---

### 6. Loading States e Progress Indicators

**Princípios:**
- Dê visibilidade do status do sistema
- Gerencie expectativas (quanto tempo?)
- Use linguagem simples e direta
- Tranquilize o usuário

#### Loading Messages

```
BÁSICO:
• "Loading..."
• "Just a moment..."
• "Please wait..."

COM CONTEXTO:
• "Loading your dashboard..."
• "Fetching your data..."
• "Preparing your report..."

COM TEMPO ESTIMADO:
• "This usually takes about 30 seconds"
• "Almost there..."
• "Processing... 75% complete"

ENGAJANTE:
• "Brewing your coffee... ☕"
• "Gathering your insights..."
• "Making magic happen..."
```

#### Progress Indicators

```
DETERMINADO (% conhecido):
• "Uploading... 45%"
• "3 of 10 files uploaded"
• "Step 2 of 5"

INDETERMINADO (% desconhecido):
• "Processing..."
• "Hang tight, this might take a minute"
• "Working on it..."

EXEMPLOS DE EXCELÊNCIA:
Google Docs: "Saving..." → "Saved to Drive" ✓
Stripe: Indicador sutil sem detalhes visuais excessivos ✓
```

#### Best Practices

```
✓ Seja breve e direto
✓ Comunique o que está acontecendo
✓ Indique tempo esperado quando possível
✓ Use linguagem simples (não jargão técnico)

✗ Não use "buffering" (use "loading")
✗ Não use "authenticating" (use "checking")
✗ Não deixe usuário sem feedback
```

---

### 7. Success e Confirmation Messages

**Princípios:**
- Confirme que a ação foi concluída
- Guie para próximo passo (não deixe na confirmação)
- Pode ser inline (no local da ação)
- Balance celebração com utilidade

#### Templates

```
SIMPLES:
• "Saved"
• "Done!"
• "Changes saved"

ESPECÍFICO:
✗ "Success!" (vago)
✓ "Invoice sent to client"

✗ "Completed" (genérico)
✓ "Your profile has been updated"

COM PRÓXIMO PASSO:
• "Payment confirmed! Check your email for receipt"
• "File uploaded. Share with your team?"
• "Account created. Let's set up your profile"
```

#### Exemplos Before/After

```
✗ Before: "Success!"
✓ After: "Your report is ready to download"

✗ Before: "Done"
✓ After: "Changes saved automatically"

✗ Before: "Operation completed"
✓ After: "Team invite sent to sarah@company.com"
```

#### Best Practices

```
✓ Seja específico sobre o que foi concluído
✓ Confirme detalhes importantes (email enviado para quem?)
✓ Ofereça próxima ação lógica
✓ Use tom positivo mas não excessivo

✗ Evite mensagens vagas ("Success", "Done")
✗ Não deixe usuário sem orientação
✗ Não exagere na celebração (para ações rotineiras)
```

---

### 8. Navigation Labels

**Princípios:**
- Use termos familiares e previsíveis
- Seja consistente em toda interface
- Prefira substantivos (Dashboard, Settings)
- Teste compreensão com usuários

#### Best Practices

```
✓ FAMILIAR:
  • Home (não "Hub")
  • Settings (não "Preferences")
  • Help (não "Support Center")

✓ ESPECÍFICO:
  • My Projects (não "Workspace")
  • Team Members (não "People")
  • Billing (não "Account")

✓ ESCANÁVEL:
  • Use 1-2 palavras quando possível
  • Agrupe itens relacionados
  • Use hierarquia clara
```

#### Mobile Navigation

```
BOTTOM BAR (3-5 itens):
• Home
• Search
• Create
• Notifications
• Profile

THUMB-FRIENDLY:
• Rótulos curtos e reconhecíveis
• Ícones + texto (quando possível)
• Limite escolhas por tela (3-5 ações max)
```

---

### 9. Placeholder Text

Ver seção [Tooltips e Helper Text](#5-tooltips-e-helper-text) acima.

---

### 10. Modal/Dialog Copy

**Princípios:**
- Seja direto sobre o propósito
- Use títulos claros e descritivos
- Botões devem refletir ações específicas
- Considere consequências (especialmente destrutivas)

#### Estrutura

```
[TÍTULO]
Descreva ação ou decisão claramente

[CORPO]
Contexto necessário (1-2 frases)
Consequências se aplicável

[BOTÕES]
[Ação Secundária] [Ação Primária]
```

#### Exemplos

**Confirmação Simples:**
```
Delete this file?
This action cannot be undone.

[Cancel] [Delete]
```

**Ação Destrutiva:**
```
✗ Before:
   Are you sure?
   [No] [Yes]

✓ After:
   Delete your account?
   All your data will be permanently removed.

   [Keep account] [Delete account]
```

**Informativo:**
```
Changes not saved
You have unsaved changes. Do you want to save before leaving?

[Don't save] [Cancel] [Save changes]
```

#### Best Practices

```
✓ Use títulos em forma de pergunta ou declaração
✓ Explique consequências de ações destrutivas
✓ Botões devem ser verbos específicos (não "OK"/"Cancel" genéricos)
✓ Ação primária à direita, secundária à esquerda

✗ Não use "Are you sure?" (seja específico)
✗ Não use "Yes/No" (use ações específicas)
✗ Não esconda informações críticas
```

---

### 11. Notification Copy (In-app e Push)

**Princípios:**
- Seja breve e direto ao ponto
- Uma ideia por mensagem
- Use linguagem simples
- Indique ação quando necessário

#### In-app Notifications

```
INFORMATIVA:
• "New message from Sarah"
• "Your report is ready"
• "3 new comments on your post"

ACIONÁVEL:
• "Your trial ends in 3 days. [Upgrade now]"
• "Review pending approval. [Review now]"
• "Update available. [Install]"

URGENTE:
• "Payment failed. Update billing info"
• "Security alert: New login from unknown device"
• "Connection lost. Reconnecting..."
```

#### Push Notifications

```
ESTRUTURA:
[Título conciso]
[Corpo: contexto necessário]
[CTA se aplicável]

EXEMPLOS:
✗ "You have a notification"
✓ "Sarah mentioned you in a comment"

✗ "Update"
✓ "New feature: Dark mode is here!"

✗ "Action required"
✓ "Your payment is due tomorrow"
```

#### Best Practices

```
✓ Mantenha título sob 40 caracteres
✓ Corpo sob 120 caracteres (visível na notificação)
✓ Seja específico (quem, o quê, quando)
✓ Use urgência apropriada

✗ Não seja vago
✗ Não exagere em urgência
✗ Não envie notificações não solicitadas
✗ Não use jargão
```

---

### 12. Accessibility Text (Alt Text, ARIA Labels)

**Princípios:**
- Alt text para imagens, ARIA labels para elementos interativos
- Seja descritivo e específico
- Não adicione "botão" ou "imagem" (screen reader já anuncia)
- Faça informações críticas visíveis para todos

#### Alt Text

```
PRINCÍPIOS:
• Descreva o conteúdo e função da imagem
• Seja conciso mas completo
• Considere contexto
• Imagens decorativas: alt=""

EXEMPLOS:
✗ "Image"
✓ "Marketing team celebrating Q4 success"

✗ "Logo"
✓ "Acme Corp logo"

✗ "Button"
✓ [Sem alt text - use aria-label no botão]

CONTEXTO IMPORTA:
Imagem: CEO apresentando
• Em artigo de notícias: "CEO Jane Smith announcing new product line"
• Em galeria: "Jane Smith at keynote presentation"
```

#### ARIA Labels

```
QUANDO USAR:
• Botões apenas com ícone
• Controles sem texto visível
• Adicionar contexto para screen readers

NÃO USAR QUANDO:
• Existe texto visível (use <label> ou aria-labelledby)
• Pode tornar texto visível (melhor para todos)

EXEMPLOS:
✗ <button aria-label="Search button">🔍</button>
✓ <button aria-label="Search">🔍</button>
  (screen reader já anuncia "button")

✗ <button aria-label="Click here">➜</button>
✓ <button aria-label="Add to cart">➜</button>

✓ <nav aria-label="Product categories">
✓ <button aria-label="Close dialog">✕</button>
✓ <input aria-label="Search products">
```

#### Best Practices

```
✓ Seja autoexplicativo e preciso
✓ Descreva propósito do elemento
✓ Mantenha conciso
✓ Não repita informações já anunciadas (role do elemento)

✗ Não use "button", "image", "link" no label
✗ Não seja vago ("Click here", "Icon")
✗ Não esconda informações críticas apenas em aria-label
```

---

## Frameworks de UX Writing

### 1. Voice & Tone

**Voice = Personalidade consistente da marca**
- Imutável, baseada em valores
- Fundação de toda comunicação
- Definida por 3-5 adjetivos principais

**Tone = Adaptação emocional ao contexto**
- Muda com a situação
- Responde às emoções do usuário
- Ajustado para cada momento

#### As 4 Dimensões de Tom (Nielsen Norman Group)

| Dimensão | Espectro |
|----------|----------|
| **Humor** | Funny ←→ Serious |
| **Formalidade** | Formal ←→ Casual |
| **Respeito** | Respectful ←→ Irreverent |
| **Entusiasmo** | Enthusiastic ←→ Matter-of-fact |

#### Exemplos por Contexto

```
SITUAÇÃO: Onboarding (primeira vez)
Voice: Profissional e suportivo
Tone: Entusiástico + casual
Exemplo: "Welcome! Let's get you set up in just 2 minutes 🎉"

SITUAÇÃO: Erro crítico
Voice: Profissional e suportivo
Tone: Sério + respeitoso
Exemplo: "We couldn't process your payment. Please verify your card details."

SITUAÇÃO: Sucesso
Voice: Profissional e suportivo
Tone: Encorajador + casual
Exemplo: "Nice work! Your changes have been saved."

SITUAÇÃO: Ação destrutiva
Voice: Profissional e suportivo
Tone: Sério + direto
Exemplo: "Delete this project? This action cannot be undone."
```

#### Voice & Tone Guide (Componentes)

**Brand Voice Chart:**
```
3-5 adjetivos descrevendo a voz

Exemplo:
• CLARO: Usamos linguagem simples, sem jargão
• ÚTIL: Cada palavra tem um propósito
• HUMANO: Conversamos, não palestramos
• CONFIÁVEL: Honestos sobre limitações
• ENCORAJADOR: Celebramos progressos
```

**Tone Mapping:**
```
Contexto → Ajuste de Tom

Primeiro uso → Mais encorajador, guiado
Uso frequente → Mais eficiente, direto
Momentos de erro → Mais empático, suportivo
Confirmações → Mais celebratório, positivo
Ações críticas → Mais sério, claro
```

---

### 2. Content Style Guide

**Componentes essenciais:**

```
LINGUÍSTICA:
• Gramática e pontuação
• Formatação (números, datas, moeda)
• Capitalização (Title Case, Sentence case)
• Contrações (use: we'll, don't | evite: sha'n't)

TERMINOLOGIA:
• Glossário de termos do produto
• Termos a evitar
• Nomes de features (sempre iguais)

FORMATAÇÃO:
• Headlines e subheads
• Listas e bullets
• Links e CTAs
• Tratamento de erros

ACESSIBILIDADE:
• Alt text
• ARIA labels
• Limites de caracteres
• Linguagem inclusiva
```

---

### 3. BLUF (Bottom Line Up Front)

**Definição:**
Princípio de comunicação onde a informação mais importante vem primeiro.

**Não encontrado em frameworks de UX** específicos nas fontes pesquisadas, mas amplamente usado em:
- Comunicação militar
- Jornalismo (pirâmide invertida)
- Comunicação empresarial

**Aplicação em UX:**
```
✗ Sem BLUF:
   "We've been working on some exciting updates
    and after testing with beta users, we're
    happy to announce..."

✓ Com BLUF:
   "New feature available: Dark mode"
   "You can now switch to dark mode in Settings."
```

**Quando usar em UX:**
- Error messages (problema primeiro, explicação depois)
- Confirmações (resultado primeiro, detalhes depois)
- Notificações (ação primeiro, contexto depois)

---

### 4. Content Design Methodology

**Definição:**
Abordagem sistemática para criar, gerenciar e escalar conteúdo de produtos.

#### Componentes

**1. Content Audit**
```
• Inventário de todo conteúdo existente
• Avaliação de qualidade e consistência
• Identificação de gaps e redundâncias
• Priorização de melhorias
```

**2. Content Guidelines**
```
• Voice & tone guide
• Style guide
• Component library (microcopy padrão)
• Templates reutilizáveis
```

**3. Workflow**
```
• Processo de criação (quem escreve?)
• Processo de revisão (quem aprova?)
• Localização (como traduzir?)
• Manutenção (como atualizar?)
```

**4. Ferramentas**
```
• Content management platform
• Design system integration
• Version control
• Collaboration tools
```

#### Systematic Voice & Tone Development

```
1. DEFINIR BRAND VOICE
   • 3-5 adjetivos principais
   • Exemplos do que fazer/não fazer
   • Parâmetros de implementação

2. MAPEAR CONTEXTOS
   • Identificar momentos-chave da UX
   • Definir tom apropriado para cada
   • Criar exemplos de referência

3. CRIAR CONTENT STYLE GUIDE
   • Regras linguísticas
   • Terminologia padrão
   • Padrões de formatação

4. IMPLEMENTAR & ESCALAR
   • Treinar equipe
   • Integrar em design system
   • Revisar e iterar
```

---

## Design Conversacional

### O que é Conversation Design?

**Definição:**
Arte de criar diálogos envolventes, intuitivos e eficazes entre humanos e sistemas alimentados por IA (chatbots, assistentes de voz, agentes de IA).

**Diferença de UX Writing:**
- **Conversation Design**: Diálogos completos e fluxos de interação
- **UX Writing**: Textos curtos dentro de apps

### Tendências 2025-2026

```
ESTATÍSTICAS:
• 50% dos knowledge workers usarão assistente virtual diariamente em 2025 (Gartner)
• Aumento de <2% em 2019 para 50% em 2025
• 34% dos adultos nos EUA usaram ChatGPT em 2025 (dobro de 2023)

PAPÉIS EMERGENTES:
• Conversation Designer
• AI Trainer
• Prompt Designer
• UX Writer (com foco conversacional)

NOTA: Conversation design raramente é cargo full-time
       Geralmente cai sob: PMs, UX, Marketing, IT, Suporte
```

### Princípios de Copy para Chatbots

**1. Naturalidade**
```
✓ Use contrações (we'll, don't, can't)
✓ Mimetize diálogo natural
✓ Evite frases rígidas

✗ "The system will process your request"
✓ "I'll process that for you"
```

**2. Benefício no Final**
```
DIFERENTE de conteúdo tradicional:
• Não lidere com benefício
• Termine com benefício
• Usuário deve conseguir completar ação baseado na ÚLTIMA frase

✗ "To save time, click here to..."
✓ "Click here to complete your order. You'll save time and skip the queue."
```

**3. Clareza e Funcionalidade**
```
✓ Respostas alinhadas com personalidade da marca
✓ Claras e funcionais
✓ User-friendly
✓ Natural e útil

✗ Personalidade à custa de clareza
✗ Muito formal ou robótico
✗ Ambíguo ou confuso
```

### Estrutura de Diálogo

```
GREETING:
Bot: "Hi! I'm here to help. What can I do for you today?"

ENTENDIMENTO:
User: "I need to change my shipping address"
Bot: "I can help with that. What's your order number?"

CONFIRMAÇÃO:
User: "#12345"
Bot: "Got it! Order #12345. What's your new address?"

AÇÃO:
User: [fornece endereço]
Bot: "Perfect! I've updated your shipping address to:
      123 Main St, New York, NY 10001
      Your order will arrive by Friday. Anything else?"

ENCERRAMENTO:
User: "No, thanks"
Bot: "You're all set! Reach out if you need anything else. Have a great day!"
```

### Best Practices

```
✓ Seja claro sobre o que o bot pode/não pode fazer
✓ Ofereça opções quando não entender
✓ Confirme informações críticas
✓ Forneça escape para humano quando necessário
✓ Mantenha tom consistente

✗ Não finja ser humano (seja transparente)
✗ Não deixe usuário sem saída
✗ Não repita perguntas já respondidas
✗ Não sobrecarregue com texto
```

---

## UX Writing para Mobile

### Limitações e Desafios

**Espaço reduzido:**
- Telas pequenas
- Teclados ocupam 50% da tela
- Usuários escaneiam, não leem

**Interação:**
- Navegação com polegar
- Toques imprecisos
- Contexto dividido (multitarefa)

**Comportamento:**
- Sessões curtas
- Menor paciência
- Abandono rápido se confuso

### Limites de Caracteres

#### Teoria de Legibilidade

```
LINHA DE TEXTO:
• 50-75 caracteres = máxima legibilidade
• Reduz fadiga visual
• Mantém foco e fluxo
• Previne desconforto em telas

WCAG (Acessibilidade):
• Máximo 80 caracteres para inglês/português/espanhol
• Máximo 40 caracteres para chinês/japonês/coreano
```

#### Labels e Microcopy

```
BOTÕES:
• 1-3 palavras idealmente
• Máximo 5 palavras
• Thumb-friendly

HEADLINES:
• 25-40 caracteres (Meta Ads)
• 25-30 caracteres recomendado
• Mobile: ainda mais curto

BODY TEXT:
• 80-100 caracteres por linha
• Parágrafos curtos (2-3 linhas)
• Espaçamento generoso
```

### Best Practices Mobile

**1. Simplicidade Vence**
```
✗ "Tap the button below to proceed to the next step of the process"
✓ "Continue"

✗ "Please enter your electronic mail address"
✓ "Email"
```

**2. Hierarquia Clara**
```
✓ Agrupe logicamente
✓ Limite 3-5 ações por tela
✓ Navegação consistente
✓ Ação primária proeminente

BOTTOM NAV (máx 5 itens):
• Home
• Search
• Create
• Alerts
• Profile
```

**3. Thumb-Friendly**
```
✓ Ícones reconhecíveis + texto
✓ Targets de toque: mínimo 44x44px
✓ Espaçamento entre elementos
✓ Ações importantes: fácil alcance
```

**4. Microcopy Essencial**
```
✓ Helper text visível (não em tooltip)
✓ Validação inline
✓ Loading states informativos
✓ Erros concisos com solução

✗ Tooltips para info crítica
✗ Texto longo e detalhado
✗ Pop-ups excessivos
```

### Desafios com Limites Rígidos

**Problema:**
Limites rígidos de caracteres não escalam entre:
- Idiomas diversos (alemão vs. inglês)
- Tamanhos de tela (mobile vs. tablet)
- Acessibilidade (texto ampliado)

**Solução:**
```
✓ Use limites flexíveis
✓ Teste em múltiplos idiomas cedo
✓ Permita quebra de linha inteligente
✓ Priorize clareza sobre brevidade forçada

✗ Corte texto arbitrariamente
✗ Use caracteres muito pequenos
✗ Ignore edge cases
```

### Acessibilidade Mobile (WCAG 2.2)

```
CONTRASTE:
• Mínimo 4.5:1 para texto normal
• Mínimo 3:1 para texto grande (>24px)

TOQUE:
• Targets mínimo 44x44px
• Espaçamento entre elementos
• Suporte a gestos alternativos

TEXTO:
• Redimensionável até 200%
• Legível sem zoom
• Não corte texto ao ampliar

NAVEGAÇÃO:
• Suporte a teclado/switch control
• Ordem lógica de foco
• Skip links para conteúdo
```

---

## Métricas de UX Writing

### 1. Task Completion Rate (Taxa de Conclusão)

**Definição:**
Percentual de usuários que completam uma tarefa com sucesso.

**Cálculo:**
```
Taxa = (Usuários que completaram / Total de usuários) × 100
```

**Benchmarks:**
```
• Média geral: ~78% (análise de 1.100+ tarefas)
• Aceitável: 78-80%
• Bom: 80-90%
• Problemático: <70-75%
```

**Como UX writing impacta:**
```
✓ CTAs claros aumentam conclusão
✓ Instruções simples reduzem abandono
✓ Erros bem escritos permitem recuperação
✓ Onboarding eficaz acelera adoção

EXEMPLO:
"Practice for 5 Minutes" (Duolingo)
Resultado: +22% daily active users
```

---

### 2. Error Rate (Taxa de Erro)

**Definição:**
Número de erros cometidos por usuários ao interagir com o produto.

**O que mede:**
- Cliques no botão errado
- Navegação para página incorreta
- Desvios do caminho ideal
- Tentativas falhadas

**Benchmark:**
```
• Alvo: <5% de taxa de erro
• Alto: >10% indica problemas sérios
```

**Como UX writing impacta:**
```
✓ Labels claros previnem cliques errados
✓ Helper text previne erros de input
✓ Validação inline corrige em tempo real
✓ Mensagens de erro ajudam recuperação

EXEMPLO:
Erro de email: "You forgot the @ symbol!" (Mailchimp)
Resultado: Correção imediata, usuário continua
```

---

### 3. Time on Task (Tempo na Tarefa)

**Definição:**
Quanto tempo usuários levam para completar uma tarefa.

**Interpretação:**
- Tempo menor = mais eficiente (geralmente bom)
- Tempo maior = fricção ou confusão (geralmente ruim)
- Exceção: Conteúdo educacional (tempo maior pode ser bom)

**Como UX writing impacta:**
```
✓ Instruções claras aceleram execução
✓ Microcopy preventivo evita erros (economiza tempo)
✓ Navigation labels intuitivos reduzem busca
✓ Loading states gerenciam expectativas

EXEMPLO:
"Send invoice" vs "Submit"
Resultado: -12% de tempo (usuários entendem imediatamente)
```

---

### 4. System Usability Scale (SUS)

**Definição:**
Questionário padronizado de 10 itens para medir percepção de usabilidade.

**Estrutura:**
- 10 perguntas
- Escala Likert de 5 pontos (discordo totalmente → concordo totalmente)
- Score final: 0-100

**Cálculo:**
```
Para cada pergunta ímpar (1,3,5,7,9): Score = Resposta - 1
Para cada pergunta par (2,4,6,8,10): Score = 5 - Resposta
SUS = Soma de scores × 2.5
```

**Benchmarks:**
```
• Média geral: 68
• Abaixo de 68: Problemas de usabilidade
• 68-80: Aceitável
• 80+: Excelente
```

**Como UX writing impacta:**
```
SUS mede PERCEPÇÃO de usabilidade, onde copy é crucial:

✓ Consistência terminológica → menos confusão
✓ Linguagem clara → menos complexidade percebida
✓ Tom apropriado → maior satisfação
✓ Mensagens úteis → maior confiança

PERGUNTAS SUS IMPACTADAS POR COPY:
• "Achei o sistema fácil de usar" → clareza de linguagem
• "Achei o sistema desnecessariamente complexo" → jargão
• "Acho que precisaria de suporte técnico" → instruções
• "As várias funções estavam bem integradas" → consistência
```

---

### 5. Métricas Adicionais

**Bounce Rate (Taxa de Rejeição):**
```
Usuários que abandonam após ver uma tela

EXEMPLO:
Slack: "Hmm, this channel doesn't exist... yet!"
Resultado: -18% bounce rate
```

**Comprehension Rate (Taxa de Compreensão):**
```
% de usuários que entendem instrução/label na primeira leitura

TESTE:
• Mostre microcopy
• Pergunte o que acontece ao clicar/fazer ação
• Mede: compreensão correta vs total

BENCHMARK:
• >90%: Excelente
• 70-90%: Aceitável
• <70%: Precisa revisão
```

**Findability (Encontrabilidade):**
```
Quão rápido usuários encontram o que procuram

IMPACTO DE UX WRITING:
• Navigation labels claros
• Search placeholder útil
• Categorização lógica
• Breadcrumbs descritivos
```

### Como Medir Impacto de UX Writing

**A/B Testing:**
```
VARIÁVEL: Microcopy
CONTROLE: Versão original
VARIAÇÃO: Nova versão
MÉTRICA: Conversão, conclusão, erros, tempo

EXEMPLO:
A: "Submit"
B: "Send invoice"
Resultado: +18% click-through (ferramenta B2B)
```

**Usability Testing:**
```
1. Defina tarefas críticas
2. Observe usuários executando
3. Identifique onde copy causa confusão
4. Revise microcopy problemático
5. Teste novamente
```

**Analytics:**
```
RASTREIE:
• Drop-off points (onde abandonam?)
• Clicks em botões específicos
• Tempo em páginas/telas
• Erros de validação
• Uso de help/suporte
```

---

## Exemplos de Excelência

### 1. Slack

**Por que é referência:**
- Tom amigável e conversacional
- Mensagens de erro com humor apropriado
- Onboarding guiado e encorajador
- Microcopy contextual

**Exemplos:**

```
ERROR 404:
"Hmm, this channel doesn't exist... yet!"
→ Humor leve + esperança (pode criar)
→ Resultado: -18% bounce rate

ONBOARDING:
Antes: Tela branca com workspace vazio
Depois: Ilustrações + guias integrados
        "Say hi to yourself" (primeira ação sugerida)
→ Resultado: Adoção mais rápida

EMPTY STATE:
"No messages yet"
"This is the beginning of your conversation with @username"
→ Positivo, não negativo

SISTEMA:
"Hmm. We're having trouble connecting."
→ Empático, honesto, não técnico
```

---

### 2. Mailchimp

**Por que é referência:**
- Tom amigável e encorajador
- Humor na medida certa
- Error messages úteis e claras
- Copy que ensina

**Exemplos:**

```
ERROR - EMAIL INVÁLIDO:
"You forgot the @ symbol!"
→ Específico, útil, amigável
→ Não culpa o usuário

USERNAME JÁ EXISTE:
"Great minds think alike! Someone already has this username."
"If it's you, log in."
→ Humor + solução
→ Não frustrante

HIGH FIVE (sucesso):
[Ilustração de high five]
"Your campaign is on its way!"
→ Celebratório mas não excessivo

HELPER TEXT:
"What should we call your audience?"
"Be specific so you can find it later"
→ Explica o "por quê"
```

---

### 3. Stripe

**Por que é referência:**
- Extremamente claro e direto
- Transparente sobre processos técnicos
- Error messages acionáveis
- Sem fluff, máxima utilidade

**Exemplos:**

```
SUCCESS STATE:
"Payment successful"
[Checkmark verde sutil]
→ Claro, sem detalhes visuais excessivos
→ Próximo passo imediatamente visível

ERROR - CARTÃO RECUSADO:
"Your card was declined. Try another card or contact your bank."
→ Direto, sem jargão
→ Duas soluções claras

LOADING:
"Processing payment..."
→ Simples, transparente

API ERRORS (para desenvolvedores):
"The card was declined for an unknown reason."
"Suggested action: The customer should contact their bank."
→ Honesto sobre limitações
→ Próximo passo claro
```

---

### 4. Duolingo

**Por que é referência:**
- Tom motivacional e celebratório
- Gamificação através de copy
- Encoraja consistência
- Personalizado

**Exemplos:**

```
SUCCESS:
"You're on fire! 🔥"
→ Celebra progresso
→ Motiva continuar

CTA:
"Practice for 5 Minutes"
(vs "Start Lesson")
→ Baixa fricção
→ Específico e alcançável
→ Resultado: +22% daily active users

NOTIFICAÇÃO:
"These reminders don't seem to be working. We'll stop sending them for now."
→ Auto-aware
→ Respeita o usuário
→ Não insiste

STREAK REMINDER:
"Don't lose your 47-day streak!"
→ Loss aversion
→ Número específico (pessoal)
```

---

### 5. Outros Exemplos Notáveis

**Google Docs:**
```
SALVAMENTO AUTOMÁTICO:
"Saving..." → "Saved to Drive"
→ Feedback contínuo
→ Tranquiliza usuário
```

**Medium:**
```
TEMPO DE LEITURA:
"5 min read"
→ Gerencia expectativas
→ Ajuda decisão de leitura
```

**Airbnb:**
```
EMPTY STATE - WISHLIST:
"Create your first wishlist"
"As you search, tap the heart icon to save your favorite places to stay."
→ Instrução + benefício
→ Guia para ação
```

**Headspace:**
```
ONBOARDING:
"Welcome. Take a seat."
"Get comfortable. This is your time."
→ Tom zen, alinhado com produto
→ Cria mood apropriado
```

---

## Ferramentas

### 1. Figma Plugins

**Frontitude (UX Writing Assistant):**
```
FEATURES:
• Sugestões de copy baseadas em contexto
• Consideração de character limits
• Alternativas para botões, headers, etc.
• Integração com guidelines da marca

USO:
• AI-powered
• Funciona dentro do Figma
• Atualização em tempo real
```

**Frontitude (UX Content Management):**
```
FEATURES:
• Biblioteca central de microcopy
• Sincronização design ↔ dev
• Colaboração entre writers e designers
• Gestão de traduções/localização

USO:
• Plugin + plataforma web
• Organizar, editar, sincronizar copy
• Consistência entre ferramentas
```

**FigGPT:**
```
FEATURES:
• Gera copy dentro do Figma
• Headlines, product descriptions, error messages
• Baseado em GPT

USO:
• Pergunte para gerar qualquer tipo de UX copy
• Rápido para prototipagem
```

**Grammarly:**
```
FEATURES:
• Verificação gramatical
• Sugestões de tom
• Destaca erros e problemas

USO:
• Integração direta no Figma
• Real-time feedback
• Suite completa de IA
```

**Writer:**
```
FEATURES:
• Enforce style guides
• Terminologia consistente
• Específico para product content

USO:
• Define regras
• Verifica conformidade
• Garante consistência
```

---

### 2. Content Management Platforms

**Frontitude:**
```
TIPO: UX Copy Manager
FEATURES:
• Biblioteca central de microcopy
• Sincronização Figma ↔ código
• Colaboração
• Localização
• Versionamento

IDEAL PARA:
• Equipes de produto
• Manter consistência em escala
• Múltiplos idiomas
```

**Ditto:**
```
TIPO: Copy Management
FEATURES:
• Similar a Frontitude
• Integração com dev tools
• Component library
• Workflow de aprovação

IDEAL PARA:
• Design systems
• Documentação de copy
• Equipes distribuídas
```

**Phrase:**
```
TIPO: Translation Management
FEATURES:
• Gestão de traduções
• Integração com ferramentas dev
• Workflow de localização
• Quality checks

IDEAL PARA:
• Produtos globais
• Múltiplos idiomas
• Equipes de localização
```

---

### 3. UX Writing Tools

**Hemingway Editor:**
```
PROPÓSITO: Simplificar escrita
FEATURES:
• Detecta sentenças complexas
• Sugere alternativas mais simples
• Calcula nível de leitura
• Destaca voz passiva

IDEAL PARA:
• Microcopy claro
• Reduzir complexidade
• Melhorar legibilidade
```

**Readable:**
```
PROPÓSITO: Análise de legibilidade
FEATURES:
• Múltiplas métricas (Flesch, etc.)
• Score de legibilidade
• Sugestões de melhoria

IDEAL PARA:
• Validar clareza
• Garantir acessibilidade
• Benchmarking
```

**Character Counter Tools:**
```
PROPÓSITO: Validar limites
FEATURES:
• Contagem de caracteres
• Simulação de truncamento
• Preview em múltiplos devices

EXEMPLOS:
• charactercounttool.com
• wordcounter.net
• Integrado em CMS
```

---

### 4. Testing & Analytics

**UserTesting:**
```
PROPÓSITO: Testar compreensão
FEATURES:
• Testes moderados/não moderados
• Feedback de usuários reais
• Video recordings

IDEAL PARA:
• Validar microcopy
• Testar alternativas
• Identificar confusão
```

**Hotjar:**
```
PROPÓSITO: Behavioral analytics
FEATURES:
• Heatmaps
• Session recordings
• Feedback polls

IDEAL PARA:
• Ver onde usuários clicam
• Identificar pontos de drop-off
• Coletar feedback in-app
```

**Maze:**
```
PROPÓSITO: Prototype testing
FEATURES:
• Testes de usabilidade
• Métricas automáticas
• Análise de caminhos

IDEAL PARA:
• Testar copy em prototypes
• Medir task completion
• A/B testing de microcopy
```

---

### 5. Referências e Recursos

**UX Writing Hub:**
```
TIPO: Educação + Comunidade
CONTEÚDO:
• Cursos
• Blog posts
• Templates
• Newsletter

URL: uxwritinghub.com
```

**Content Design London:**
```
TIPO: Treinamento
CONTEÚDO:
• Workshops
• Readability guidelines
• Blog

URL: contentdesign.london
```

**Material Design (Google):**
```
TIPO: Guidelines
CONTEÚDO:
• Writing principles
• Communication guidelines
• Component copy examples

URL: material.io/design/communication
```

**Nielsen Norman Group:**
```
TIPO: Pesquisa UX
CONTEÚDO:
• Artigos
• Research studies
• Best practices
• Tone of voice guidelines

URL: nngroup.com
```

---

## Checklist de UX Writing

### ✅ Clareza
- [ ] Usuário entende na primeira leitura?
- [ ] Evitou jargão e termos técnicos?
- [ ] Usou linguagem simples e direta?
- [ ] Especificou ação/resultado claramente?

### ✅ Concisão
- [ ] Removeu palavras desnecessárias?
- [ ] Cada palavra tem um propósito?
- [ ] Respeitou limites de caracteres?
- [ ] Priorizou eficiência sobre elegância?

### ✅ Consistência
- [ ] Tom alinhado com contexto?
- [ ] Terminologia consistente?
- [ ] Formatação padronizada?
- [ ] Voz da marca mantida?

### ✅ Utilidade
- [ ] Ajuda o usuário a completar tarefa?
- [ ] Fornece contexto necessário?
- [ ] Oferece próximo passo quando apropriado?
- [ ] Resolve dúvidas/preocupações?

### ✅ Acessibilidade
- [ ] Alt text descritivo?
- [ ] ARIA labels quando necessário?
- [ ] Contraste adequado?
- [ ] Legível em texto ampliado?

### ✅ Mobile
- [ ] Funciona em telas pequenas?
- [ ] Thumb-friendly?
- [ ] Escaneável rapidamente?
- [ ] Loading states informativos?

---

## Recursos Adicionais

### Leitura Recomendada

**Livros:**
- "Microcopy: The Complete Guide" - Kinneret Yifrah
- "Strategic Writing for UX" - Torrey Podmajersky
- "Nicely Said" - Nicole Fenton & Kate Kiefer Lee
- "Writing Is Designing" - Michael J. Metts & Andy Welfle

**Websites:**
- UX Writing Hub (uxwritinghub.com)
- Nielsen Norman Group (nngroup.com)
- Material Design Writing Guidelines (material.io)
- Content Design London (contentdesign.london)

**Comunidades:**
- UX Content Collective (Slack)
- Content + UX (Slack)
- Writers of Silicon Valley (Meetup)

---

## Glossário

| Termo | Definição |
|-------|-----------|
| **Microcopy** | Pequenos bits de texto que guiam usuários (botões, erros, tooltips) |
| **CTA** | Call-to-Action, texto que incentiva ação específica |
| **Voice** | Personalidade consistente da marca |
| **Tone** | Ajuste emocional do voice para contexto específico |
| **Helper Text** | Texto auxiliar que explica campo ou ação |
| **Placeholder** | Texto exemplo dentro de campo de input |
| **Tooltip** | Explicação breve que aparece ao hover/tap |
| **Empty State** | Tela/seção sem conteúdo (primeira vez ou sem dados) |
| **Loading State** | Feedback durante processamento/carregamento |
| **ARIA Label** | Texto para screen readers, não visível |
| **Alt Text** | Descrição de imagem para acessibilidade |
| **Inline Validation** | Verificação em tempo real durante input |
| **BLUF** | Bottom Line Up Front, informação importante primeiro |
| **WCAG** | Web Content Accessibility Guidelines |
| **SUS** | System Usability Scale, questionário de usabilidade |

---

**Versão:** 1.0 | **Atualizado:** 2026-02-07
**Fontes:** Nielsen Norman Group, UX Writing Hub, Baymard Institute, WCAG 2.2

---

## Sources

- [Guide to UX writing: how to write clear, concise and effective texts - IED](https://www.ied.edu/news/guide-to-ux-writing-how-to-write-clear-concise-and-effective-texts)
- [UX Writing 10 Best Practices: Guide (2025) - ParallelHQ](https://www.parallelhq.com/blog/ux-writing-best-practices)
- [UX Writing Best Practices - UX Writing Hub](https://uxwritinghub.com/ux-writing-best-practices/)
- [Mastering UX Writing: A Comprehensive Guide for 2026 - UX Playbook](https://uxplaybook.org/articles/ux-writing-guide-2026)
- [7 Basic Principles of Good UX Copywriting - Vilmate](https://vilmate.com/blog/seven-principles-of-good-ux-writing/)
- [7 Effective UX Writing Best Practices in 2026 - Design Studio UI/UX](https://www.designstudiouiux.com/blog/ux-writing-best-practices/)
- [Material's Communication Principles - Google Codelabs](https://codelabs.developers.google.com/codelabs/material-communication-guidance)
- [Writing Microcopy: A 2026 Guide for Ecommerce UX - Shopify](https://www.shopify.com/enterprise/blog/how-to-write-microcopy-that-influences-customers-even-if-they-don-t-read-it)
- [Essential Microcopy Guide - UXPin](https://www.uxpin.com/studio/blog/microcopy-that-converts/)
- [The Art of Microcopy: Tiny Text, Massive Impact - Academy of Continuing Education](https://www.academyofcontinuingeducation.com/blog/the-art-of-microcopy-tiny-text-massive-impact)
- [Microcopy UX: Tips and Examples - Userpilot](https://userpilot.com/blog/microcopy-ux/)
- [How To Improve Your Microcopy - Smashing Magazine](https://www.smashingmagazine.com/2024/06/how-improve-microcopy-ux-writing-tips-non-ux-writers/)
- [The Art of Voice and Tone in UX Writing - UX Writing Hub](https://uxwritinghub.com/ux-writing-voice-and-tone/)
- [How To Create a Tone of Voice for UX Writing - UX Design Institute](https://www.uxdesigninstitute.com/blog/tone-of-voice-for-ux-writing/)
- [Understanding Tone of Voice in UX Writing - Maya Pillai Writes](https://mayapillaiwrites.com/understanding-tone-of-voice-in-ux-writing-the-4-dimensions-every-writer-needs-to-master/)
- [The Four Dimensions of Tone of Voice in UX Writing - Nielsen Norman Group](https://www.nngroup.com/videos/tone-of-voice-dimensions/)
- [Conversational AI Design in 2025 - Botpress](https://botpress.com/en/blog/conversation-design)
- [AI Conversational Design & Natural Language Processing - UX Writing Hub](https://uxwritinghub.com/ai-conversational-design-natural-language-processing/)
- [Chatbot Design Guide 2025 - Botpress](https://botpress.com/blog/chatbot-design)
- [ChatGPT and UX: AI-Powered Copy in Interfaces - Medium](https://medium.com/design-bootcamp/chatgpt-and-ux-the-rise-of-ai-powered-copy-in-interfaces-b26128f712a1)
- [UX for AI Chatbots: Complete Guide (2025) - ParallelHQ](https://www.parallelhq.com/blog/ux-ai-chatbots)
- [Optimal Line Length for Readability - UXPin](https://www.uxpin.com/studio/blog/optimal-line-length-for-readability/)
- [Mobile App UI/UX Best Practices 2025 - Orbix](https://www.orbix.studio/blogs/mobile-app-ux-best-practices-guide)
- [Essential UX Accessibility Tips for Designers 2025 - WCAG](https://www.wcag.com/resource/ux-quick-tips-for-designers/)
- [Accessibility in UI/UX Design: 2025 Best Practices - Orbix](https://orbix.studio/blogs/accessibility-uiux-design-best-practices-2025)
- [Accessible UX writing - UX Content Collective](https://uxcontent.com/accessible-ux-writing-a-guide-for-inclusive-content-design/)
- [Accessibility in UX Writing - UX Writing Hub](https://uxwritinghub.com/accessibility-in-ux-writing/)
- [14 Good UX Writing Examples - Userpilot](https://userpilot.com/blog/ux-writing-examples/)
- [11 Examples of Good UX Writing - Netguru](https://www.netguru.com/blog/good-ux-writing-examples)
- [40 UX Writing Examples - Technical Writer HQ](https://technicalwriterhq.com/writing/ux-writing/ux-writing-examples/)
- [Onboarding UX Writing Examples - UserOnBoarding](https://useronboarding.academy/post/onboarding-ux-writing)
- [Designing Empty States - UXPin](https://www.uxpin.com/studio/blog/ux-best-practices-designing-the-overlooked-empty-states/)
- [Empty State UX Examples - Pencil & Paper](https://www.pencilandpaper.io/articles/empty-states)
- [Empty states in UX done right - LogRocket](https://blog.logrocket.com/ux-design/empty-states-ux-examples/)
- [6 UX Metrics and KPIs to Measure User Experience 2025 - Survicate](https://survicate.com/blog/ux-metrics/)
- [12 Key Usability Metrics - Maze](https://maze.co/collections/reporting-analysis/measure-usability-metrics/)
- [10 Benchmarks for User Experience Metrics - MeasuringU](https://measuringu.com/ux-benchmarks/)
- [Task Success Rate in UX - Medium](https://medium.com/@claus.nisslmueller/task-success-rate-in-ux-how-to-use-the-simplest-metric-in-a-serious-way-34177fede27f)
- [Best Figma plugins for UX writing - html.to.design](https://html.to.design/blog/best-figma-plugins-for-ux-writing/)
- [Frontitude UX Content Management](https://frontitude.com/)
- [Best Figma Plugins for Writers in 2025 - Frontitude](https://frontitude.com/blog/best-figma-plugins-for-writers-in-2025)
- [Tools for UX writers - UX done Write](https://adinacretu.com/tools-for-ux-writers)
- [Error Messages: Examples, Best Practices - CXL](https://cxl.com/blog/error-messages/)
- [Best 10 Examples And Guidelines For Error Messages - UX Writing Hub](https://uxwritinghub.com/error-message-examples/)
- [Best Practices for Displaying Form Errors - Tuts+](https://webdesign.tutsplus.com/courses/best-practices-for-displaying-form-errors/lessons/use-microcopy)
- [Tooltip Guidelines - Jen Dennis Medium](https://jendennis2000.medium.com/tooltip-hint-text-from-helpful-to-human-2239d4666f1d)
- [Tooltip Guidelines: Best Practices - UX Design World](https://uxdworld.com/tooltip-guidelines/)
- [8 Recommendations for Creating Effective Input Fields - Baymard](https://baymard.com/learn/input-fields)
- [Help Text vs Tooltips - UX Movement](https://uxmovement.substack.com/p/help-text-vs-tooltips-which-is-better)
- [aria-label examples and best practices - Aditus](https://www.aditus.io/aria/aria-label/)
- [aria-label or title? Screen Reader Behaviour - A11y Collective](https://www.a11y-collective.com/blog/aria-label-vs-title/)
- [ARIA6: Using aria-label - WCAG](https://www.w3.org/TR/WCAG20-TECHS/ARIA6.html)
- [Developing Accessible Software With ARIA Labels - Learnosity](https://learnosity.com/edtech-blog/developing-accessible-software-aria-labels-alt-text/)
- [Success Message UX Examples - Pencil & Paper](https://www.pencilandpaper.io/articles/success-ux)
- [UX Design Patterns for Loading - Pencil & Paper](https://www.pencilandpaper.io/articles/ux-pattern-analysis-loading-feedback)
- [Write Engaging UX Microcopy for Loading Text - Faqprime](https://faqprime.com/en/write-engaging-ux-microcopy-for-loading-text-free-templates/)
- [UX Writing for Empty States, Errors, and Success Messages - Medium](https://medium.com/@rounakbajoriastar/ux-writing-for-empty-states-errors-and-success-messages-tiny-texts-big-impact-70559a28306d)
