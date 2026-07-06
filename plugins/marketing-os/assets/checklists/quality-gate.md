# Quality Gate — Checklist de Qualidade para Conteúdo

## Visão Geral

O Quality Gate é um sistema de validação que todo conteúdo deve passar antes de ser publicado. Garante consistência, qualidade e aderência aos padrões do Marketing OS.

---

## Checklist Universal (Todos os Formatos)

### Linguagem e Escrita

- [ ] Acentuação portuguesa completa e correta (á, é, í, ó, ú, â, ê, ô, ã, õ, ç, à)
- [ ] Sem erros gramaticais ou ortográficos
- [ ] Tom consistente com a marca/clone definido
- [ ] Linguagem acessível para a audiência-alvo
- [ ] Sem jargão desnecessário ou termos técnicos não explicados

### Hook (Abertura)

- [ ] Primeira linha captura atenção imediatamente
- [ ] Hook é relevante para o tema (não é clickbait vazio)
- [ ] Hook cria curiosidade ou promete valor
- [ ] Hook é adaptado à plataforma (caracteres, formato)
- [ ] Score do hook > 70/100 (usar `headline_scorer.py`)

### CTA (Chamada para Ação)

- [ ] CTA presente e claro
- [ ] CTA usa linguagem de ação (verbos imperativos)
- [ ] CTA é contextual (faz sentido no conteúdo)
- [ ] CTA é específico (não genérico como "clique aqui")
- [ ] Apenas UM CTA principal por peça

### Conteúdo

- [ ] Entrega a promessa feita no hook
- [ ] Informações verificáveis e precisas
- [ ] Dados e estatísticas com fonte identificável
- [ ] Sem afirmações absolutas sem fundamentação
- [ ] Estrutura lógica com início, meio e fim

### Brand Voice

- [ ] Consistente com o tom da marca
- [ ] Se clone ativado: voz compatível com o expert
- [ ] Vocabulário adequado ao nicho
- [ ] Energia e ritmo consistentes

---

## Checklist por Formato

### Post de Rede Social

- [ ] Dentro do limite de caracteres da plataforma
- [ ] Hashtags relevantes (quantidade adequada por plataforma)
- [ ] Formatação visual (quebras de linha, espaçamento)
- [ ] Emojis usados com moderação e propósito
- [ ] Variação A/B disponível

| Plataforma | Limite Hook | Limite Total | Hashtags |
|------------|------------|-------------|----------|
| Instagram Feed | 125 char (visível) | 2.200 char | 10-15 |
| Instagram Reels | 150 char | 2.200 char | 3-5 |
| LinkedIn | 210 char (visível) | 3.000 char | 3-5 |
| Twitter/X | 280 char total | 280 char | 1-3 |
| TikTok | 100 char | 2.200 char | 3-5 |

### Artigo/Blog SEO

- [ ] Título com keyword principal
- [ ] Meta description com keyword + CTA (< 155 char)
- [ ] Keyword no primeiro parágrafo
- [ ] H2s com variações da keyword
- [ ] Keyword density entre 1-2%
- [ ] Mínimo 1.500 palavras (artigos padrão)
- [ ] Links internos sugeridos (2-3)
- [ ] Links externos para autoridades (1-2)
- [ ] Alt text para imagens sugerido
- [ ] Score SEO > 70/100 (usar `seo_analyzer.py`)
- [ ] Readability score > 60 (usar `readability_checker.py`)

### Email

- [ ] Subject line < 50 caracteres
- [ ] Preview text complementa o subject
- [ ] Personalização (nome, dados do lead)
- [ ] Um objetivo por email
- [ ] CTA em botão + link de texto
- [ ] Versão texto puro disponível
- [ ] Unsubscribe link mencionado
- [ ] Testado em mobile

### Anúncio (Ads)

- [ ] Headline dentro do limite da plataforma
- [ ] Primary text conciso e persuasivo
- [ ] Benefício claro nos primeiros 3 segundos/linhas
- [ ] CTA alinhado com o objetivo da campanha
- [ ] Sem promessas proibidas pela plataforma
- [ ] Sem linguagem sensacionalista excessiva
- [ ] Variações para teste A/B (mínimo 2)

### Vídeo/Reels

- [ ] Hook nos primeiros 3 segundos
- [ ] Script com timestamps
- [ ] CTA visual e falado
- [ ] Duração adequada ao formato
- [ ] Thumbnail concept descrito
- [ ] Título e descrição otimizados
- [ ] Closed captions / legendas considerados

### Landing Page

- [ ] Headline com benefício claro
- [ ] Proposta de valor única evidente
- [ ] CTAs visíveis (mínimo 3 na página)
- [ ] Prova social presente
- [ ] Garantia/redução de risco
- [ ] FAQ com objeções principais
- [ ] Mobile responsive considerado
- [ ] Velocidade de carregamento < 3s

---

## Sistema de Scoring

### Cálculo do Score de Qualidade

| Critério | Peso | Max |
|----------|------|-----|
| Hook/Abertura | 20% | 20 pts |
| Conteúdo/Substância | 25% | 25 pts |
| CTA/Conversão | 15% | 15 pts |
| Formatação/Plataforma | 15% | 15 pts |
| Brand Voice | 10% | 10 pts |
| SEO (se aplicável) | 10% | 10 pts |
| Fact-check | 5% | 5 pts |
| **Total** | **100%** | **100 pts** |

### Classificação

| Score | Classificação | Ação |
|-------|--------------|------|
| 90-100 | Excelente | Publicar imediatamente |
| 75-89 | Bom | Publicar com ajustes menores |
| 60-74 | Regular | Revisar antes de publicar |
| 40-59 | Fraco | Reescrever seções críticas |
| 0-39 | Reprovado | Refazer completamente |

---

## Uso com Scripts

```bash
# Verificar headline
python scripts/headline_scorer.py "Sua headline aqui"

# Analisar SEO de artigo
python scripts/seo_analyzer.py artigo.md "keyword principal"

# Verificar legibilidade
python scripts/readability_checker.py --file texto.md

# Gerar hashtags validadas
python scripts/hashtag_generator.py nicho plataforma
```

---

## Erros Comuns a Evitar

| Erro | Impacto | Solução |
|------|---------|---------|
| Texto sem acentos | Violação Constitution | Sempre acentuar |
| Hook genérico | Baixo engajamento | Usar fórmulas específicas |
| CTA vago | Baixa conversão | "Quero [benefício]" > "Clique aqui" |
| Copy muito longo | Abandono | Respeitar limites da plataforma |
| Dados sem fonte | Perda de credibilidade | Sempre citar origem |
| Promessas exageradas | Problemas legais/confiança | Ser específico e realista |
| Hashtags irrelevantes | Alcance errado | Pesquisar relevância |
| Sem variação A/B | Sem aprendizado | Sempre criar 2+ versões |
