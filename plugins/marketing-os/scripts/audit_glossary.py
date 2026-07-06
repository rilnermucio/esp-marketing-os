"""Glossário técnico curado pra relatórios /auditoria-pro.

50+ termos técnicos com definições em PT-BR, voltados pra cliente final
não-técnico mas educado. Cada definição: 1-2 frases, sem jargão circular.

Uso: render_glossary_md(used_terms) filtra apenas os termos efetivamente
mencionados no relatório, mantendo a seção de glossário enxuta.
"""

from __future__ import annotations

GLOSSARY: dict[str, str] = {
    "CWV": "Core Web Vitals. Métricas do Google que medem performance percebida pelo usuário: LCP (Largest Contentful Paint), INP (Interaction to Next Paint) e CLS (Cumulative Layout Shift).",
    "LCP": "Largest Contentful Paint. Tempo até o maior elemento da página renderizar. Bom: até 2.5s.",
    "INP": "Interaction to Next Paint. Latência de resposta a interações do usuário. Bom: até 200ms.",
    "CLS": "Cumulative Layout Shift. Quanto a página se reorganiza durante o carregamento. Bom: até 0.1.",
    "schema markup": "Marcação estruturada (geralmente JSON-LD) que ajuda buscadores a entender o conteúdo da página, habilitando rich snippets nos resultados de busca.",
    "JSON-LD": "Formato leve de dados linkados, padrão recomendado pelo Google para schema markup.",
    "rich snippets": "Resultados de busca enriquecidos com informações estruturadas (preço, rating, FAQ), gerados a partir de schema markup.",
    "hreflang": "Atributo HTML que sinaliza variantes de idioma e região de uma página, evitando que o Google penalize conteúdo duplicado entre versões.",
    "CTA": "Call-to-Action. Elemento (botão, link, frase) que pede uma ação específica do usuário. Exemplos: 'Comece agora', 'Falar com vendas'.",
    "value proposition": "Promessa central de valor. O motivo principal pelo qual um usuário deveria escolher um produto vs alternativas. Geralmente comunicada no headline da homepage.",
    "headline": "Título principal de uma página, geralmente acima do fold. Carrega o peso da promessa de valor.",
    "subheadline": "Texto de apoio ao headline, expande ou esclarece a promessa.",
    "above the fold": "Conteúdo visível sem rolar a página. Tradicionalmente o espaço mais valioso da landing.",
    "fold": "Linha horizontal imaginária onde a página é cortada pela parte inferior da viewport.",
    "social proof": "Prova social. Evidências de que outras pessoas/empresas usam o produto: depoimentos, logos, números, reviews.",
    "trust signals": "Sinais de confiança. Elementos que reduzem a percepção de risco do usuário: certificações, garantias, badges de segurança, números de uso.",
    "friction": "Atrito no funil. Qualquer obstáculo que reduz conversão: formulários longos, exigência de cartão, etapas desnecessárias.",
    "funnel": "Funil de conversão. Sequência de etapas que um visitante percorre até virar cliente.",
    "TOFU": "Top of Funnel. Topo do funil. Estágio de descoberta, audiência fria, sem intenção de compra clara.",
    "MOFU": "Middle of Funnel. Meio do funil. Estágio de avaliação, audiência considerando alternativas.",
    "BOFU": "Bottom of Funnel. Fundo do funil. Estágio de decisão, audiência pronta pra comprar ou trocar.",
    "lead magnet": "Conteúdo gratuito (ebook, checklist, webinar) oferecido em troca do email do visitante. Captura de lead no TOFU.",
    "lead": "Pessoa que demonstrou interesse fornecendo dados de contato. Ainda não é cliente.",
    "tripwire": "Oferta de baixo ticket no início do funil pra converter lead em comprador (mesmo de baixo valor) e quebrar a barreira psicológica de pagar.",
    "upsell": "Oferta de produto/plano superior após uma compra inicial.",
    "downsell": "Oferta alternativa de menor valor quando o usuário rejeita o upsell.",
    "PLG": "Product-Led Growth. Modelo de aquisição onde o produto é o motor principal de crescimento (free trial, freemium, viralidade).",
    "AARRR": "Pirate Metrics. Framework de funil: Aquisição, Ativação, Retenção, Receita, Referência (Acquisition, Activation, Retention, Revenue, Referral).",
    "ICP": "Ideal Customer Profile. Perfil ideal de cliente. Características da empresa/persona que melhor encaixa no produto.",
    "persona": "Representação semi-ficcional do cliente ideal, baseada em pesquisa. Inclui demografia, dor, motivação, objeções.",
    "engagement rate": "Taxa de engajamento. Razão entre interações (likes, comments, saves) e seguidores ou impressões.",
    "viewport": "Área visível de uma página em um dispositivo. 'viewport mobile' = 375x812, 'viewport desktop' = 1440x900 ou similar.",
    "responsive design": "Design responsivo. Layout que se adapta automaticamente a diferentes viewports (mobile, tablet, desktop).",
    "mobile-first": "Abordagem de design onde o layout é construído primeiro pra mobile e expande pra telas maiores.",
    "viewport meta tag": "Tag HTML que controla como o navegador mobile renderiza a página. Sem ela, mobile renderiza como desktop e o usuário precisa dar zoom.",
    "WCAG": "Web Content Accessibility Guidelines. Diretrizes do W3C para acessibilidade web. Níveis A, AA, AAA.",
    "contrast ratio": "Razão de contraste entre texto e fundo. WCAG AA exige 4.5:1 para texto normal e 3:1 para texto grande.",
    "alt text": "Texto alternativo de uma imagem. Descrição lida por leitores de tela e usada por buscadores. Imagens decorativas usam alt vazio.",
    "skip link": "Link no topo da página que permite usuários de teclado pular direto pro conteúdo principal, ignorando navegação repetitiva.",
    "ARIA": "Accessible Rich Internet Applications. Conjunto de atributos HTML que ajudam tecnologias assistivas a interpretar componentes complexos.",
    "lazy loading": "Carregamento preguiçoso. Imagens fora do viewport só carregam quando o usuário rola até elas, reduzindo o peso inicial da página.",
    "preload": "Tag HTML que diz ao navegador para baixar um recurso crítico (fonte, imagem hero) antes do parser HTML chegar nele.",
    "preconnect": "Tag HTML que diz ao navegador para abrir conexão antecipada com um domínio externo (CDN, fonts, analytics).",
    "CDN": "Content Delivery Network. Rede de servidores distribuídos geograficamente que serve conteúdo estático (imagens, CSS, JS) com baixa latência.",
    "SSR": "Server-Side Rendering. Renderização da página no servidor antes de enviar pro navegador, melhorando tempo de primeira pintura e SEO.",
    "CSR": "Client-Side Rendering. Renderização no navegador via JavaScript após receber HTML mínimo do servidor. Pior pra SEO se mal configurado.",
    "hydration": "Processo onde o JavaScript do cliente 'reidrata' o HTML estático do SSR, anexando event handlers e tornando a página interativa.",
    "title tag": "Tag HTML <title>. Aparece como título da aba do navegador e como título do resultado nos buscadores. Recomendado: até 60 caracteres.",
    "meta description": "Atributo HTML que descreve a página em ~155 caracteres. Aparece abaixo do title nos resultados de busca. Influencia CTR.",
    "CTR": "Click-Through Rate. Taxa de cliques. Razão entre cliques e impressões. CTR de SERP, de email, de ad creative, etc.",
    "SERP": "Search Engine Results Page. Página de resultados de um buscador.",
    "anchor text": "Texto clicável de um link. Importante pra SEO: descreve o destino do link.",
    "internal linking": "Links entre páginas do mesmo site. Distribui autoridade SEO e melhora navegação.",
    "backlink": "Link de outro site apontando pro seu. Sinal forte de autoridade pro Google.",
    "canonical": "Tag HTML rel=canonical. Aponta a versão 'oficial' de uma página quando há duplicatas, evitando penalidade SEO.",
    "robots.txt": "Arquivo na raiz do site que diz a buscadores quais páginas podem ou não ser rastreadas.",
    "sitemap.xml": "Arquivo XML que lista todas as páginas do site, ajudando buscadores a descobrir conteúdo novo.",
    "ad creative": "Criativo de anúncio. Imagem, vídeo ou texto usado em campanhas pagas.",
    "hook": "Primeiro elemento de um conteúdo (frase, imagem, primeiros 3 segundos) que captura atenção e faz o usuário continuar.",
    "retention": "Retenção. (1) % de usuários que continuam usando o produto ao longo do tempo. (2) % de viewers que assistem além de um certo ponto de um vídeo.",
    "churn": "Cancelamento. Taxa de clientes que deixam o produto em um período.",
    "MRR": "Monthly Recurring Revenue. Receita recorrente mensal. Métrica fundamental de SaaS.",
    "ARR": "Annual Recurring Revenue. MRR x 12.",
    "LTV": "Lifetime Value. Receita total esperada por cliente ao longo do relacionamento.",
    "CAC": "Customer Acquisition Cost. Custo de aquisição por cliente. LTV/CAC > 3 é referência saudável.",
    "ROAS": "Return on Ad Spend. Receita gerada por real investido em ads.",
    "CPA": "Cost Per Acquisition. Custo por aquisição (de lead ou cliente, conforme contexto).",
    "CPM": "Cost Per Mille. Custo por mil impressões. Métrica padrão de exposição em ads.",
    "SEO": "Search Engine Optimization. Conjunto de técnicas para melhorar a visibilidade orgânica de um site nos resultados de buscadores.",
}


def render_glossary_md(used_terms: set[str] | None = None) -> str:
    """Render glossary as markdown. Filter by used_terms when provided."""
    if used_terms is None:
        terms_to_render = GLOSSARY
    else:
        terms_to_render = {
            k: v
            for k, v in GLOSSARY.items()
            if any(t.lower() in k.lower() or k.lower() in t.lower() for t in used_terms)
        }

    if not terms_to_render:
        return ""

    lines = ["## Glossário", "", "Termos técnicos mencionados neste relatório:", ""]
    for term in sorted(terms_to_render):
        lines.append(f"**{term}.** {terms_to_render[term]}")
        lines.append("")
    return "\n".join(lines)
