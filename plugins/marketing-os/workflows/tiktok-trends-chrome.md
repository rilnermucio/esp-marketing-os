# 🔍 Workflow: Buscar Trends TikTok via Chrome

Este workflow permite que eu (Claude) navegue no TikTok usando o browser para encontrar vídeos virais por nicho, hashtag ou assunto.

---

## 📋 Como Usar

### Solicite ao Claude:
```
"Busque no TikTok vídeos virais sobre [TEMA] com mais de 1 milhão de views"
"Encontre os trends de [NICHO] no TikTok"
"Pesquise hashtags virais de [ASSUNTO] no TikTok"
```

### Informações que você pode especificar:
- **Nicho/Tema**: marketing, fitness, beleza, gastronomia, etc.
- **Mínimo de views**: 100K, 500K, 1M, etc.
- **Período**: última semana, último mês
- **Tipo de conteúdo**: tutorial, storytime, trend, POV, etc.

---

## 🔄 Fluxo de Execução

### Etapa 1: Navegação Inicial
1. Abrir TikTok no Chrome
2. Ir para a aba de busca
3. Pesquisar pelo termo/hashtag solicitado

### Etapa 2: Aplicar Filtros
1. Filtrar por "Mais curtidos" ou "Mais recentes"
2. Verificar métricas de cada vídeo
3. Identificar vídeos acima do threshold de views

### Etapa 3: Coleta de Dados
Para cada vídeo viral encontrado, coletar:
- URL do vídeo
- @username do criador
- Número de views, likes, comentários, shares
- Descrição/caption
- Hashtags utilizadas
- Duração do vídeo
- Som/música usado

### Etapa 4: Análise
1. Identificar padrões nos vídeos virais
2. Listar hashtags mais frequentes
3. Analisar estrutura dos vídeos (hook, desenvolvimento, CTA)
4. Identificar sons/músicas em comum

### Etapa 5: Relatório
Gerar relatório com:
- Lista dos vídeos encontrados
- Análise de padrões
- Recomendações para criação de conteúdo

---

## 🎯 URLs Úteis para Busca

### Busca Geral
```
https://www.tiktok.com/search?q=[TERMO]
```

### Busca por Hashtag
```
https://www.tiktok.com/tag/[HASHTAG]
```

### Página de Trending
```
https://www.tiktok.com/trending
```

### Perfil de Criador
```
https://www.tiktok.com/@[USERNAME]
```

---

## 📊 Template de Coleta

### Dados por Vídeo:
```
📹 VÍDEO #[N]
━━━━━━━━━━━━━━━━━━━━
🔗 URL: [link]
👤 Criador: @[username]
📈 Métricas:
   - Views: [X]M
   - Likes: [X]K
   - Comments: [X]K
   - Shares: [X]K
⏱️ Duração: [X]s
📝 Descrição: [primeiras 100 palavras]
🏷️ Hashtags: #[1] #[2] #[3]
🎵 Som: [nome do som]
📅 Postado: [data aproximada]

💡 Por que viralizou:
[análise breve]
━━━━━━━━━━━━━━━━━━━━
```

---

## 🔥 Hashtags por Nicho para Busca

### Marketing Digital
- #marketingdigital #socialmedia #empreendedorismo
- #negociosonline #trafegopago #copywriting
- #infoprodutos #vendasonline #marketingtips

### Fitness
- #fitness #treino #academia #musculacao
- #personaltrainer #dieta #emagrecimento
- #fitnessmotivation #workout #vidasaudavel

### Beleza
- #makeup #skincare #maquiagem #beleza
- #grwm #beautytips #cuidadoscomapele
- #rotinadebeleza #cabelo #unhas

### Gastronomia
- #receitas #cozinha #receitafacil #comida
- #foodtiktok #airfryer #receitasfit
- #sobremesa #almoco #jantar

### Finanças
- #financas #investimentos #dinheiro #rendaextra
- #educacaofinanceira #criptomoedas #bolsa
- #economizar #independenciafinanceira

### Tecnologia
- #tech #tecnologia #iphone #android
- #ia #apps #gadgets #programacao
- #inteligenciaartificial #apple

### Lifestyle
- #rotina #dayinmylife #organizacao #produtividade
- #minimalismo #autocuidado #motivacao
- #mindset #qualidadedevida

---

## 📋 Checklist de Análise de Vídeo Viral

### Estrutura
- [ ] Como é o HOOK (primeiros 3 segundos)?
- [ ] Qual a estrutura do conteúdo?
- [ ] Tem CTA no final?
- [ ] Qual a duração total?

### Elementos Visuais
- [ ] Usa texto na tela?
- [ ] Tem transições?
- [ ] Qualidade do vídeo (luz, áudio)?
- [ ] Usa efeitos/filtros?

### Elementos de Engajamento
- [ ] Faz perguntas?
- [ ] Gera polêmica/debate?
- [ ] Conta história?
- [ ] Ensina algo prático?

### Otimização
- [ ] Quantas hashtags?
- [ ] Hashtags genéricas ou nichadas?
- [ ] Som trending ou original?
- [ ] Caption com gancho?

---

## 📈 Métricas de Referência

### Por Nível de Viralização:
| Nível | Views | Consideração |
|-------|-------|--------------|
| Micro-viral | 100K - 500K | Bom para nicho específico |
| Viral | 500K - 1M | Performance sólida |
| Super-viral | 1M - 5M | Excelente alcance |
| Mega-viral | 5M+ | Potencial de trend |

### Taxa de Engajamento Saudável:
- **Excelente**: > 10%
- **Bom**: 5% - 10%
- **Médio**: 2% - 5%
- **Baixo**: < 2%

Fórmula: `(likes + comments + shares) / views * 100`

---

## 💡 Dicas para Busca Eficiente

1. **Busque termos em português E inglês** - Muitos trends começam em inglês
2. **Verifique a data** - Trends de mais de 30 dias podem estar saturados
3. **Analise os comentários** - Indicam o que a audiência quer
4. **Olhe perfis similares** - Encontre criadores do mesmo nicho
5. **Use a aba "Para Você"** - Ajuda a entender o algoritmo atual

---

## 🎬 Exemplo de Relatório Final

```markdown
# 📊 Relatório TikTok Trends - Marketing Digital
**Data:** DD/MM/YYYY
**Termo buscado:** #marketingdigital
**Critério:** +1M views

## Resumo
- Vídeos analisados: 10
- Views total: 45M
- Engagement médio: 7.2%

## Top 3 Vídeos

### 1. "5 erros que todo empreendedor comete"
- @fulano - 5.2M views
- Por que viralizou: Formato lista + dor comum

### 2. "Storytime: Como faturei 100K"
- @ciclano - 3.8M views
- Por que viralizou: Prova social + curiosidade

### 3. "POV: Você descobriu tráfego pago"
- @beltrano - 2.1M views
- Por que viralizou: Relatabilidade + humor

## Padrões Identificados
- Duração média: 45s
- Hashtags comuns: #empreendedorismo #negociosonline
- Formato mais viral: Storytelling + Lista
- Som trending: [nome]

## Recomendações
1. Criar conteúdo de lista (3-5 itens)
2. Usar hook de "erro comum"
3. Duração ideal: 30-60s
4. Postar entre 18h-21h
```
