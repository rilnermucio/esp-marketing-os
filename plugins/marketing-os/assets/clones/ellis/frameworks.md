# Sean Ellis - Frameworks

## 1. Product-Market Fit Test (40% Test)

O framework mais famoso de Ellis. Mede se um produto realmente tem product-market fit antes de investir em growth.

```
Pergunta aos usuários atuais:
"Como você se sentiria se não pudesse mais usar [produto]?"

Respostas:
a) Muito desapontado
b) Um pouco desapontado
c) Não me importaria
d) Não uso mais
```

### Interpretação

| % "Muito Desapontado" | Diagnóstico | Ação |
|------------------------|-------------|------|
| **40%+** | Product-Market Fit confirmado | Investir em growth |
| **25-39%** | Quase lá, ajustes necessários | Melhorar o produto antes de escalar |
| **< 25%** | Sem PMF | Pivotar ou redefinir o ICP (Ideal Customer Profile) |

### Como Implementar

```
1. Identifique usuários que usaram o produto pelo menos 2x
2. Envie a pesquisa com 4 perguntas:
   - "Muito desapontado" test
   - "Qual o principal benefício?"
   - "Para quem você recomendaria?"
   - "Como podemos melhorar?"
3. Analise as respostas
4. Segmente os "muito desapontados" - eles são seu ICP real
5. Use a linguagem deles no marketing
```

### Regra de Ouro

> "Não escale um produto sem product-market fit. É como colocar combustível em um carro com o motor quebrado."

---

## 2. Growth Hacking Funnel (AARRR / Pirate Metrics)

Framework para mapear e otimizar todo o funil de crescimento, atribuído a Dave McClure e amplamente utilizado por Ellis.

```
A - Acquisition:  Como os usuários chegam?
A - Activation:   Eles têm uma boa primeira experiência?
R - Retention:    Eles voltam?
R - Revenue:      Eles pagam?
R - Referral:     Eles indicam para outros?
```

### Métricas por Fase

| Fase | Métrica Principal | Benchmark SaaS |
|------|-------------------|----------------|
| **Acquisition** | Custo por lead qualificado | Varia por indústria |
| **Activation** | % que completa ação-chave em 7 dias | 20-40% |
| **Retention** | % ativos no dia 30 | 20-35% |
| **Revenue** | LTV / CAC ratio | > 3:1 |
| **Referral** | Viral coefficient (K-factor) | > 0.5 para organic growth |

### Onde Focar

```
Regra de Ellis:
1. Comece pela RETENÇÃO (se não retém, nada mais importa)
2. Depois ATIVAÇÃO (converta mais dos que chegam)
3. Depois REFERRAL (crescimento orgânico)
4. Por último, AQUISIÇÃO (escale o que funciona)

A maioria faz o contrário e fracassa.
```

---

## 3. ICE Scoring (Priorização de Experimentos)

Framework para priorizar quais experimentos rodar primeiro quando se tem dezenas de ideias.

```
ICE Score = Impact × Confidence × Ease
```

### Componentes

| Componente | Descrição | Escala |
|------------|-----------|--------|
| **Impact** | Quanto vai impactar a métrica alvo se funcionar? | 1-10 |
| **Confidence** | Quão confiante estou de que vai funcionar? | 1-10 |
| **Ease** | Quão fácil é implementar e testar? | 1-10 |

### Exemplo de Priorização

| Experimento | Impact | Confidence | Ease | Score |
|-------------|--------|------------|------|-------|
| Simplificar onboarding | 8 | 7 | 6 | 336 |
| Email de reengajamento D3 | 6 | 8 | 9 | 432 |
| Programa de referral | 9 | 5 | 3 | 135 |
| Mudar preço do plano básico | 7 | 4 | 8 | 224 |

### Regras

1. **Score mais alto primeiro** - Rode os experimentos com maior score
2. **Velocity importa** - Prefira testes que podem ser rodados em 1-2 semanas
3. **Reavalie semanalmente** - Scores mudam conforme você aprende
4. **Pipeline mínimo** - Sempre tenha 10+ ideias no backlog

---

## 4. Growth Team Structure

Framework para montar e operar uma equipe de growth.

### Composição Ideal

```
Growth Team = Growth Lead + Product Manager + Engineer(s) + Data Analyst + Designer

Mínimo viável: Growth Lead + 1 Engineer + acesso a dados
```

### Processo Semanal

```
SEGUNDA: Growth Meeting (1h)
  → Revisar resultados da semana anterior
  → Analisar métricas do dashboard
  → Priorizar experimentos da semana (ICE score)
  → Atribuir responsáveis

TERÇA-QUINTA: Execução
  → Implementar experimentos
  → Monitorar testes em andamento
  → Documentar aprendizados

SEXTA: Análise
  → Coletar dados dos testes da semana
  → Documentar resultados (funcionou/não funcionou/inconclusivo)
  → Atualizar backlog de ideias
  → Preparar report para a Growth Meeting de segunda
```

### Velocity de Experimentos

| Estágio | Testes/Semana | Foco |
|---------|---------------|------|
| **Iniciante** | 2-5 | Aprender o processo |
| **Intermediário** | 5-15 | Encontrar alavancas |
| **Avançado** | 15-30+ | Escalar aprendizados |

### Regra de Ouro

> "A equipe de growth que roda mais experimentos com qualidade vence. Não é sobre ter a ideia perfeita. É sobre testar rápido o suficiente para encontrá-la."

---

## 5. North Star Metric Framework

Sistema para definir a métrica mais importante da empresa, aquela que captura o valor entregue ao cliente.

### Critérios de uma Boa North Star Metric

```
1. Reflete o VALOR entregue ao cliente (não só receita)
2. É MENSURÁVEL de forma confiável
3. Toda a empresa pode INFLUENCIÁ-LA
4. É um INDICADOR ANTECIPADO de receita
5. É SIMPLES de entender
```

### Exemplos por Tipo de Negócio

| Tipo de Negócio | North Star Metric | Por quê |
|-----------------|-------------------|---------|
| **Marketplace** | Transações completadas por semana | Captura valor de ambos os lados |
| **SaaS** | Usuários ativos semanais (WAU) | Indica engajamento real |
| **E-commerce** | Pedidos por cliente por mês | Captura frequência e valor |
| **Media/Content** | Tempo de consumo por usuário/dia | Indica valor do conteúdo |
| **Freemium** | % de usuários que atingem "aha moment" em 7 dias | Prediz conversão e retenção |

### Como Definir sua NSM

```
Passo 1: Qual é o momento "aha" do seu produto?
  → Quando o cliente percebe o valor real

Passo 2: Qual ação do cliente indica esse momento?
  → A ação mensurável que correlaciona com retenção

Passo 3: Essa métrica pode ser influenciada por toda a equipe?
  → Se apenas marketing ou apenas produto pode, é estreita demais

Passo 4: Se essa métrica cresce, a receita cresce?
  → Se não há correlação com receita, é vanity metric
```

---

## 6. Activation Framework

Sistema para otimizar a ativação de novos usuários, a fase mais negligenciada do funil.

### O Conceito de "Aha Moment"

```
Aha Moment = O momento em que o usuário percebe o valor real do produto

Exemplos famosos:
- Facebook: adicionar 7 amigos em 10 dias
- Dropbox: salvar 1 arquivo em 1 dispositivo
- Slack: enviar 2.000 mensagens como equipe
```

### Framework de Ativação

```
1. IDENTIFICAR o aha moment (analisar dados de retenção)
2. MEDIR % de novos usuários que chegam lá (taxa de ativação)
3. MAPEAR o caminho entre signup e aha moment
4. REMOVER fricção em cada etapa do caminho
5. TESTAR variações que aceleram a chegada ao aha moment
6. ESCALAR o que funciona
```

### Métricas de Ativação

| Métrica | Definição | Meta |
|---------|-----------|------|
| **Time to Value** | Tempo entre signup e aha moment | Menor possível |
| **Activation Rate** | % de novos usuários que atingem aha moment | 25-50% |
| **Drop-off Points** | Etapas onde mais usuários abandonam | Identificar e eliminar |

---

## Resumo para Aplicação na Copy

| Framework | Use quando... |
|-----------|---------------|
| 40% Test | Precisa validar product-market fit |
| AARRR Funnel | Está mapeando e otimizando o funil completo |
| ICE Scoring | Precisa priorizar entre múltiplas ideias de growth |
| Growth Team Structure | Está montando ou organizando uma equipe de growth |
| North Star Metric | Precisa definir a métrica principal da empresa |
| Activation Framework | Está otimizando a experiência dos primeiros dias |
