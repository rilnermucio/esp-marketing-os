# Getting Started com Marketing OS

Guia prático: como instalar, como trabalhar por projeto e os cenários mais comuns.

## Instalação rápida

No Claude Code (terminal ou app desktop):

```
/plugin marketplace add rilnermucio/esp-marketing-os
/plugin install marketing-os@mos-marketplace
```

Pronto. O orquestrador é a skill `/marketing-os` e os especialistas ficam disponíveis como agents `marketing-os:mos-*` (copy, SEO, social, vídeo, oferta, funil e os demais).

**Use uma origem só.** Se você também adicionou um marketplace do Marketing OS nas configurações de plugins da sua conta claude.ai, o app desktop pode carregar essa cópia sincronizada em vez da instalada acima, e ela pode estar desatualizada. Para ver todas as cópias da máquina, peça ao Claude: "rode o diagnóstico de instalação do Marketing OS". O caso está detalhado no [TROUBLESHOOTING](./TROUBLESHOOTING.md).

## Conceito-chave: um projeto por pasta

O Marketing OS aprende **por projeto**. Crie uma pasta dedicada para cada cliente:

```bash
mkdir ~/Code/clientes/wellness-science
cd ~/Code/clientes/wellness-science
claude  # ou abra o app desktop nessa pasta
```

Tudo que é seu fica nessa pasta, nunca dentro da pasta do plugin:

- **Memória dos agents** em `.claude/agent-memory/marketing-os-mos-*/`. A plataforma injeta essa memória no agent a cada sessão. Para preparar os diretórios de uma vez, peça: "inicialize a memória do Marketing OS neste projeto".
- **Entregas e materiais** em `workspace/` (rascunhos, swipe files aprovados, auditorias, mídia, clones de voz pessoais).

**Regra prática:** uma pasta, um cliente ou projeto. Não misture trabalhos diferentes na mesma pasta.

## Primeiro passo: perfil da marca

```
/configurar-marca Clínica Sorriso Pleno, odontologia estética em Curitiba
```

O perfil (nicho, público, oferta, voz, proibições, categoria regulada e canais) fica em `workspace/brand/perfil.md`, e todos os especialistas o leem antes de produzir. O orquestrador deixa de repetir as mesmas perguntas a cada sessão, e o avatar, a USP e a oferta criados depois são salvos na mesma pasta.

## Não sabe qual command usar?

Descreva o que precisa com `/mo`. O meta-orquestrador escolhe o command ou o especialista certo e diz qual escolheu:

```
/mo preciso vender uma mentoria de R$ 5.000 para dentistas
```

## Cenários comuns

### Headlines para produto novo (dispatch simples)

```
/marketing-os escreve 5 headlines pro meu curso de Python para devs juniores
```

O orquestrador reconhece "headlines", despacha o `mos-copy`, aplica os quality gates (sem travessão, sem "brutal", PT-BR correto) e entrega as headlines com variações A/B e sugestão de teste.

### Carrossel completo (dispatch composto)

```
/criar-carrossel 7 erros de copy para LinkedIn
```

Dispara em paralelo `mos-social` (estrutura), `mos-copy` (texto dos slides) e `mos-design` (paleta e tipografia) e consolida: estrutura, texto de cada slide, design spec, legenda, hashtags e sugestão de enquete.

### Base estratégica antes de produzir

```
/criar-avatar coach de carreira para mulheres em transição
/criar-usp mentoria de posicionamento no LinkedIn
/criar-oferta mentoria de 3 meses, R$ 3.000
```

Avatar, USP e oferta viram o contexto que as peças seguintes usam. Os três commands aceitam dados reais que você colar (depoimentos, reviews, números de vendas).

### Página de aplicação BOFU

```
/criar-landing-page página de aplicação para a mentoria do Dr. Victor
```

`mos-funnel` analisa a estrutura BOFU (CTA, escassez, anti-avatar, FAQ), `mos-copy` escreve e revisa, `mos-design` define a direção visual. Se você pedir HTML de fato, o brief consolidado vai para a skill de frontend.

### Lançamento de infoproduto

```
/criar-infoproduto curso de IA para empreendedores, ticket R$ 1.997
/campanha-lancamento
```

`/criar-infoproduto` valida mercado e estrutura o produto (módulos, preço, materiais). `/campanha-lancamento` monta a campanha inteira (pesquisa, modelo de lançamento, funil, copy, emails, anúncios, design e métricas).

### Briefing vago

```
/marketing-os cria copy
```

O orquestrador não chuta. Pergunta de uma vez nicho, avatar, ticket, plataforma e urgência, e pula o que já estiver na memória do projeto.

## Aprender com os resultados

Depois de publicar, traga as métricas:

```
/aprender cole aqui o export de métricas dos reels do mês
```

O `mos-analytics` interpreta o que funcionou e, com a sua aprovação, grava os aprendizados na memória do agent dono de cada peça. Nas próximas peças, esse agent já parte do que performou no seu projeto.

## Compliance regulatório

Em nichos regulados, o plugin adiciona os disclaimers necessários em qualquer peça final:

| Nicho | Órgão | O que muda na peça |
|---|---|---|
| Medicina | CFM/CRM, CONAR | "Resultados variam" em depoimentos; CRM visível; sem "cura" |
| Odontologia | CFO/CRO, CONAR | CRO visível; sem promessa de resultado garantido |
| Nutrição | CFN/CRN, CONAR | CRN visível; sem prescrição individual em conteúdo genérico |
| Psicologia | CFP/CRP | CRP visível; sem promessa de cura |
| Advocacia | OAB | Publicidade só informativa, sem captação de clientela |
| Suplementos | ANVISA | "Auxilia/contribui", nunca cura ou trata |
| Finanças e investimentos | CVM | "Rentabilidade passada não garante resultado futuro" |
| Cosméticos | ANVISA | Sem prometer tratar doença de pele |

O nicho é detectado pela memória do cliente, pela pasta atual ou pela primeira pergunta do briefing.

## Commands por necessidade

| Quero... | Command |
|---|---|
| Perfil de marca do projeto | `/configurar-marca` |
| Um post, carrossel ou calendário | `/criar-post`, `/criar-carrossel`, `/criar-calendario` |
| Várias peças de uma vez | `/batch` |
| Email ou sequência | `/criar-email`, `/criar-sequencia` |
| Anúncio | `/criar-anuncio` |
| Vídeo, roteiro, thumbnail ou Reels produzido | `/criar-video`, `/gerar-thumbnail`, `/produzir-reels` |
| Áudio a partir de roteiro | `/narrar-roteiro` |
| Imagem (só o prompt, ou o PNG) | `/gerar-imagem`, `/renderizar-imagem` |
| Artigo SEO ou landing page | `/criar-artigo`, `/criar-landing-page` |
| Funil, webinar ou infoproduto | `/criar-funil`, `/criar-webinar`, `/criar-infoproduto` |
| Avatar, USP ou oferta | `/criar-avatar`, `/criar-usp`, `/criar-oferta` |
| Melhorar ou revisar uma peça pronta | `/otimizar-copy` |
| Teste A/B | `/criar-teste-ab` |
| Responder comentários e DMs (rascunho) | `/responder-comentarios` |
| Prospectar creators | `/prospectar-creators` |
| Auditar página, perfil ou anúncios | `/auditoria`, `/auditoria-pro` |
| Datas comerciais do ano | `/datas-sazonais` |
| Campanha completa por objetivo | `/campanha` (lista os presets) |
| Projeto em etapas com aprovação | `/projeto` |
| Aprender com métricas | `/aprender` |

## Voice clones

Quando o briefing pede estilo específico:

```
/marketing-os escreve uma sales letter no estilo do Gary Halbert para produto de finanças
```

O `mos-copy` carrega o clone do copywriter (profile, frameworks, voz e exemplos) e escreve no estilo. Há clones de copywriters e criadores como Halbert, Hopkins, Kennedy, Ogilvy, Schwartz, Sugarman, Hormozi, GaryVee, MrBeast, Brunson, Cialdini, Codie Sanchez, Abdaal, Conrado e Joel Jota.

Para clonar a **sua** voz a partir das suas amostras (posts, emails, artigos):

```
/criar-meu-clone me-seunome
```

O clone pessoal é salvo no projeto, em `workspace/clones/`, e o `mos-copy` o usa quando você pedir "no meu estilo".

## Quando algo dá errado

Ver [TROUBLESHOOTING.md](./TROUBLESHOOTING.md): instalação e sincronização, versão antiga no app desktop, memória e dispatch.
