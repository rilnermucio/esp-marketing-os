# Marketing OS — Arquitetura do Sistema

> **Snapshot histórico (fev a mai/2026, v5 a v6.1).** Descreve estruturas que já mudaram (pasta `squads/`, "Sistema A/B", contagens de agents e commands). Estrutura e contagens atuais: [AGENTS.md](../AGENTS.md) e [README.md](../README.md). Decisões posteriores: [docs/ai-engineering/adr/](ai-engineering/adr/).

> Documentação técnica completa. Renderizar com **Markdown Preview Enhanced** no VSCode.
> Última atualização: 2026-02-18

---

## Índice

1. [Visão Geral](#1-visão-geral)
2. [Camadas do Sistema](#2-camadas-do-sistema)
3. [Fluxo Principal de Request](#3-fluxo-principal-de-request)
4. [Sistemas Paralelos (A vs B)](#4-sistemas-paralelos-a-vs-b)
5. [Arquitetura de Subagentes](#5-arquitetura-de-subagentes)
6. [Sistema de Clones](#6-sistema-de-clones)
7. [Fluxo: Reels de 90 Segundos](#7-fluxo-reels-de-90-segundos)
8. [Integrações MCP](#8-integrações-mcp)
9. [Scripts Python](#9-scripts-python)
10. [Mapa de Arquivos](#10-mapa-de-arquivos)

---

## 1. Visão Geral

Marketing OS é um sistema operacional de marketing digital com **duas camadas de entrada**, **17 subagentes especializados**, **34 clones de voz** e **30+ scripts Python**.

```mermaid
mindmap
  root((Marketing OS))
    Entrada
      Plugin raiz
      Plugin commands
      Slash commands
      Skill triggers
    Subagentes
      Research
      Copy
      SEO
      Social
      Video
      Audio
      Design
      Analytics
      Email
      Ads
      Brand
      Storytelling
      Funnel
      Growth
      Launch
      AI Tools
      Infoproduct
    Clones
      Copywriters clássicos
      Criadores de vídeo
      Empreendedores BR
      Growth experts
    Automação
      30 scripts Python
      9 workflows
      5 MCPs
```

---

## 2. Camadas do Sistema

```mermaid
graph TB
    subgraph ENTRADA["🚪 Camada de Entrada"]
        P1["plugin.json\n(raiz / Sistema A)"]
        P2[".claude-plugin/plugin.json\n(marketing-os / Sistema B)"]
        CMD["24 Slash Commands\n/criar-video, /criar-post..."]
        SKILL["Skill Trigger\n(palavra-chave no chat)"]
    end

    subgraph ORQUESTRADOR["🎛️ Camada de Orquestração"]
        MOS["marketing-os SKILL.md\nOrquestrador Principal"]
        CM["Clone Manifest\nclone-manifest.yaml"]
        BRIEF["Briefing Engine\nColeta: nicho, objetivo,\npúblico, tom, CTA"]
    end

    subgraph AGENTES["🤖 Camada de Subagentes (17)"]
        VA["Video Agent"]
        CA["Copy Agent"]
        SA["Social Agent"]
        SEO["SEO Agent"]
        RA["Research Agent"]
        AA["Audio Agent"]
        DA["Design Agent"]
        AN["Analytics Agent"]
        EA["Email Agent"]
        ADS["Ads Agent"]
        BA["Brand Agent"]
        STA["Storytelling Agent"]
        FA["Funnel Agent"]
        GA["Growth Agent"]
        LA["Launch Agent"]
        AIT["AI Tools Agent"]
        IA["Infoproduct Agent"]
    end

    subgraph CLONES["🎭 Camada de Clones (34)"]
        VIRAL["Viral\nMrBeast"]
        COPY["Copywriting\nHormozi · Halbert · Schwartz"]
        EDU["Educativo\nAbdaal · Ogilvy"]
        BR["Brasileiro\nFlávio · Joel Jota · Conrado"]
        VENDA["Vendas\nBrunson · Suby · Kennedy"]
    end

    subgraph OUTPUT["📦 Camada de Output"]
        ROT["Roteiro / Script"]
        POST["Post / Caption"]
        ART["Artigo SEO"]
        EMAIL["Email / Sequência"]
        RELAT["Relatório Analytics"]
        NOTION["→ Notion MCP"]
    end

    P1 --> MOS
    P2 --> CMD
    CMD --> MOS
    SKILL --> MOS
    MOS --> BRIEF
    BRIEF --> CM
    CM --> AGENTES
    MOS --> AGENTES
    AGENTES --> CLONES
    CLONES --> OUTPUT

    style ENTRADA fill:#1a1a2e,color:#eee,stroke:#4a4a8a
    style ORQUESTRADOR fill:#16213e,color:#eee,stroke:#4a4a8a
    style AGENTES fill:#0f3460,color:#eee,stroke:#4a4a8a
    style CLONES fill:#533483,color:#eee,stroke:#8a4aaa
    style OUTPUT fill:#0d7377,color:#eee,stroke:#14a085
```

---

## 3. Fluxo Principal de Request

```mermaid
flowchart TD
    U(["👤 Usuário\n'Crie conteúdo para mim'"])

    U --> DET{"Tipo de\nrequest?"}

    DET -->|"Slash command\n/criar-video"| SC["Carregar\ncreate-video.md"]
    DET -->|"Palavra-chave\n(reels, post, blog...)"| SK["Ativar Skill\nmarketing-os"]
    DET -->|"Pedido livre\n'crie um post'"| SK

    SC --> BRF
    SK --> BRF

    BRF["📋 Briefing\nNicho · Objetivo · Público\nTom · Duração · CTA"]

    BRF --> RES["🔍 Research Agent\nTendências · Concorrência\nKeywords · Dados"]

    RES --> CLONE{"🎭 Seleção\nde Clone"}

    CLONE -->|"Viral"| MB["MrBeast\nRetenção extrema"]
    CLONE -->|"Venda"| BRU["Brunson\nHook-story-offer"]
    CLONE -->|"Educação"| ABD["Abdaal\nEvidence-based"]
    CLONE -->|"Copy/Texto"| HOR["Hormozi / Ogilvy\nOutros 31 clones..."]

    MB --> AG
    BRU --> AG
    ABD --> AG
    HOR --> AG

    AG{"🤖 Subagente\nEspecializado"}

    AG -->|"Vídeo"| VID["Video Agent\nRoteiro · Timecodes\nRe-hooks · CTA"]
    AG -->|"Post social"| SOC["Social Agent\nCaption · Hashtags\nHorário"]
    AG -->|"Artigo"| SEOA["SEO Agent\nEstrutura E-E-A-T\nKeywords"]
    AG -->|"Email"| EML["Email Agent\nSequência\nAutomação"]

    VID --> QG
    SOC --> QG
    SEOA --> QG
    EML --> QG

    QG["✅ Quality Gate\n- Sem palavras proibidas\n- Acentuação correta\n- Fatos verificados\n- Enquete incluída"]

    QG --> OUT["📦 Output\nConteúdo principal\n+ 2-3 variações A/B\n+ Métricas-alvo\n+ Próximos passos"]

    OUT --> NOT["→ Notion (MCP)"]
    OUT --> FILE["→ Arquivo .md"]

    style U fill:#2d3561,color:#fff
    style BRF fill:#16213e,color:#fff
    style CLONE fill:#533483,color:#fff
    style AG fill:#0f3460,color:#fff
    style QG fill:#0d7377,color:#fff
    style OUT fill:#14a085,color:#fff
```

---

## 4. Sistemas Paralelos (A vs B)

O Marketing OS tem dois sistemas em execução paralela. Entender a diferença é crítico.

```mermaid
graph LR
    subgraph SA["Sistema A — Skill Package"]
        direction TB
        SA1["plugin.json (raiz)\nv4.0.0"]
        SA2["skills/marketing-os/\nSKILL.md (v16)"]
        SA3["skills/marketing-os/\nsubagents/ (16)"]
        SA4["skills/marketing-os/\nassets/templates/ (23)"]
        SA5["skills/marketing-os/\nassets/swipe-files/ (7)"]
        SA6["skills/marketing-os/\nscripts/ (30)"]
        SA1 --> SA2 --> SA3
        SA2 --> SA4
        SA2 --> SA5
        SA2 --> SA6
    end

    subgraph SB["Sistema B — Command Plugin (Enhanced)"]
        direction TB
        SB1["marketing-os/.claude-plugin/\nplugin.json"]
        SB2["marketing-os/skills/marketing-os/\nSKILL.md (symlink → skills/marketing-os/)"]
        SB3["marketing-os/commands/\n24 slash commands"]
        SB5["marketing-os/CONNECTORS.md\nMCP integrations"]
        SB1 --> SB2
        SB1 --> SB3
        SB2 --> SB5
    end

    subgraph SHARED["Recursos Compartilhados"]
        SHR1["subagents/ (18 .md)"]
        SHR2["squads/marketing-os/\ndata/clones/ (34 clones)"]
        SHR3["workflows/ (9)"]
        SHR4["references/ (9)"]
    end

    SA3 -.->|"referencia"| SHR1
    SB4 -.->|"referencia"| SHR1
    SA2 -.->|"referencia"| SHR2
    SB2 -.->|"referencia"| SHR2

    note1["⚠️ Sistema B tem\n17 subagentes (inclui\nInfoproduct Builder)"]
    note2["⚠️ Sistema A tem\nregras de qualidade\nmais completas"]

    SA -.-> note2
    SB -.-> note1

    style SA fill:#1a1a2e,color:#eee,stroke:#4a4a8a
    style SB fill:#0f3460,color:#eee,stroke:#4a8aaa
    style SHARED fill:#16213e,color:#eee,stroke:#888
```

### Diferenças Críticas

| Característica | Sistema A | Sistema B |
|---|---|---|
| Subagentes | 16 | 17 (+ Infoproduct Builder) |
| Interface | Skill trigger | 24 slash commands |
| Palavras proibidas | ✅ Completo | ✅ Sincronizado (corrigido 2026-02-18) |
| Verificação de fatos | ✅ Obrigatória | ✅ Sincronizado (corrigido 2026-02-18) |
| Enquetes obrigatórias | ✅ Sim | ✅ Sincronizado (corrigido 2026-02-18) |
| Checklist qualidade | 11 itens | 11 itens (sincronizado) |
| MCPs integrados | Não | Notion, Figma, Canva, Slack, SimilarWeb |
| Batch production | Não | `/batch` command |

---

## 5. Arquitetura de Subagentes

```mermaid
graph TB
    MOS(["🎛️ Marketing OS\nOrquestrador"])

    MOS --> CORE["Agentes Core\n(sempre ativados)"]
    MOS --> SPEC["Agentes Especializados\n(ativados por tipo)"]
    MOS --> AUX["Agentes Auxiliares\n(ativados por necessidade)"]

    subgraph CORE_GROUP["Core"]
        RA["🔍 Research Agent\nTendências · Keywords\nConcorrência · Dados"]
        CPA["✍️ Copy Agent\nHeadlines · CTAs\nVariações A/B"]
    end

    subgraph SPEC_GROUP["Especializados por Formato"]
        VID["🎬 Video Agent\nYouTube · Reels · TikTok\nShorts · VSL\nCiência de retenção"]
        SOC["📱 Social Agent\nInstagram · LinkedIn\nTikTok · Twitter\nHashtags · Timing"]
        SEO["📈 SEO Agent\nArtigos · Blog\nE-E-A-T · On-page"]
        AUD["🎙️ Audio Agent\nPodcasts · Spots\nAudiobooks"]
        EML["📧 Email Agent\nSequências · Newsletters\nAutomações"]
        ADS["📣 Ads Agent\nMeta · Google · TikTok\nAd copy"]
    end

    subgraph AUX_GROUP["Auxiliares"]
        DES["🎨 Design Agent\nDireção criativa\nPaletas · Specs"]
        AIT["🤖 AI Tools Agent\nPrompts Midjourney\nDALL-E · Runway"]
        ANA["📊 Analytics Agent\nMétricas · KPIs\nDashboards"]
        BRA["🏷️ Brand Agent\nIdentidade · Tom\nPositioning"]
        STO["📖 Storytelling Agent\nNarrativas · Arcos\nConexão emocional"]
        FUN["🔄 Funnel Agent\nFunis · Jornada\nConversão"]
        GRO["🚀 Growth Agent\nGrowth hacking\nAquisição · Viral loops"]
        LAU["🚀 Launch Agent\nLançamentos\nGo-to-market"]
        INF["📚 Infoproduct Agent\nCursos · Ebooks\nMemberships"]
    end

    CORE --> CORE_GROUP
    SPEC --> SPEC_GROUP
    AUX --> AUX_GROUP

    style MOS fill:#533483,color:#fff
    style CORE fill:#1a1a2e,color:#eee,stroke:#4a4a8a
    style SPEC fill:#0f3460,color:#eee,stroke:#4a8aaa
    style AUX fill:#16213e,color:#eee,stroke:#888
```

### Quando cada agente é ativado

```mermaid
flowchart LR
    REQ["Request do usuário"]

    REQ --> V{"Vídeo?"}
    REQ --> S{"Post social?"}
    REQ --> A{"Artigo/Blog?"}
    REQ --> E{"Email?"}
    REQ --> AD{"Anúncio?"}
    REQ --> P{"Podcast?"}
    REQ --> C{"Campanha?"}

    V -->|sim| VA["Video Agent\n+ Copy Agent\n+ Design Agent"]
    S -->|sim| SA["Social Agent\n+ Copy Agent"]
    A -->|sim| SEA["SEO Agent\n+ Copy Agent\n+ Research Agent"]
    E -->|sim| EA["Email Agent\n+ Copy Agent"]
    AD -->|sim| ADA["Ads Agent\n+ Copy Agent\n+ Research Agent"]
    P -->|sim| PA["Audio Agent\n+ Copy Agent"]
    C -->|sim| ALL["Todos os agentes\nrelevantes para\na campanha"]
```

---

## 6. Sistema de Clones

```mermaid
graph TD
    CM["clone-manifest.yaml\n70+ regras de matching"]

    CM --> CAT1["Vídeo / Viral"]
    CM --> CAT2["Copywriting Clássico"]
    CM --> CAT3["Vendas / Funil"]
    CM --> CAT4["Educação / Conteúdo"]
    CM --> CAT5["Growth / Tech"]
    CM --> CAT6["Mercado Brasileiro"]
    CM --> CAT7["Especialistas"]

    subgraph VID_CLONES["Vídeo / Viral"]
        MB["MrBeast\nReels · TikTok · YouTube\nViral, challenge-driven"]
        GV["GaryVee\nSocial media\nSem filtro, motivacional"]
        ABD["Ali Abdaal\nYouTube · Podcast\nEvidence-based, calmo"]
    end

    subgraph COPY_CLONES["Copywriting Clássico"]
        OG["David Ogilvy\nBrand, elegante"]
        HAL["Gary Halbert\nDirect response, emocional"]
        SCH["Eugene Schwartz\nAwareness, científico"]
        SUG["Joseph Sugarman\nLong copy, hipnótico"]
        HOP["Claude Hopkins\nFactual, sem hype"]
        CAP["John Caples\nHeadlines testadas"]
        COL["Robert Collier\nSales letters, íntimo"]
        PRO["Gary Provost\nRitmo, variação"]
        CIA["Robert Cialdini\nPsicologia, persuasão"]
    end

    subgraph SALES_CLONES["Vendas / Funil"]
        HOR["Alex Hormozi\nNúmeros, escalabilidade"]
        BRU["Russell Brunson\nFunnels, webinars"]
        KEN["Dan Kennedy\nDirect response, anti-branding"]
        SUB["Sabri Suby\nSell Like Crazy, sistemas"]
        LEI["Leila Hormozi\nOperações, liderança"]
        IMN["Iman Gadzhi\nAgency, high-ticket"]
    end

    subgraph EDU_CLONES["Educação / Conteúdo"]
        GOD["Seth Godin\nPermission, filosófico"]
        WEL["Justin Welsh\nSolopreneur, LinkedIn"]
        COE["Nicolas Cole\nDigital writing, atomic"]
        MEL["Mel Robbins\n5 Second Rule, hábitos"]
    end

    subgraph GROWTH_CLONES["Growth / Tech"]
        ELL["Sean Ellis\nGrowth hacking, PMF"]
        CHE["Andrew Chen\nNetwork effects, ensaístico"]
        PAT["Neil Patel\nSEO, conteúdo, analytics"]
        RAC["Lenny Rachitsky\nProduct, SaaS, benchmarks"]
        EZR["Ezra Firestone\nE-commerce, DTC, email"]
        COD["Codie Sanchez\nContrarian, boring biz"]
        ABR["Jay Abraham\n3 pilares, cross-industry"]
        MIL["Donald Miller\nStoryBrand framework"]
        HOW["Park Howell\nABT storytelling"]
    end

    subgraph BR_CLONES["Mercado Brasileiro"]
        FLA["Flávio Augusto\nGeração de Valor, informal BR"]
        JOE["Joel Jota\nAlta performance, esporte"]
        CON["Conrado Adolpho\n8Ps, metodologia BR"]
    end

    CAT1 --> VID_CLONES
    CAT2 --> COPY_CLONES
    CAT3 --> SALES_CLONES
    CAT4 --> EDU_CLONES
    CAT5 --> GROWTH_CLONES
    CAT6 --> BR_CLONES

    style CM fill:#533483,color:#fff
    style VID_CLONES fill:#1a1a2e,color:#eee,stroke:#4a4a8a
    style COPY_CLONES fill:#0f3460,color:#eee,stroke:#4a8aaa
    style SALES_CLONES fill:#16213e,color:#eee,stroke:#888
    style EDU_CLONES fill:#0d4f4f,color:#eee,stroke:#0d7377
    style GROWTH_CLONES fill:#1a2e1a,color:#eee,stroke:#4a8a4a
    style BR_CLONES fill:#2e1a1a,color:#eee,stroke:#8a4a4a
```

### Regras de Seleção de Clone por Content Type

```mermaid
graph LR
    CT["Content Type"] --> R1["reels → MrBeast\n(alt: Brunson, Abdaal)"]
    CT --> R2["reels_venda → Brunson\n(alt: Hormozi, GaryVee)"]
    CT --> R3["youtube → MrBeast\n(alt: Abdaal)"]
    CT --> R4["tiktok → MrBeast\n(alt: GaryVee, Abdaal)"]
    CT --> R5["copy_vendas → Hormozi\n(alt: Halbert, Schwartz)"]
    CT --> R6["landing_page → Brunson\n(alt: Hormozi, Ogilvy)"]
    CT --> R7["email → Halbert\n(alt: Ogilvy, Collier)"]
    CT --> R8["artigo_seo → Ogilvy\n(alt: Schwartz)"]
    CT --> R9["anuncio → Schwartz\n(alt: Hormozi, Brunson)"]
    CT --> R10["newsletter → Andrew Chen\n(alt: Abdaal, Halbert)"]
    CT --> R11["post_instagram → Joel Jota\n(alt: Mel Robbins, Flávio)"]
    CT --> R12["post_linkedin → Ogilvy\n(alt: Hormozi)"]
    CT --> R13["podcast → Abdaal"]
    CT --> R14["social_media → GaryVee\n(alt: Howell, Ogilvy)"]
    CT --> R15["sales_letter → Kennedy\n(alt: Collier, Halbert)"]
    CT --> R16["post_blog → Seth Godin\n(alt: Ogilvy, Cole)"]

    style CT fill:#533483,color:#fff
```

---

## 7. Fluxo: Reels de 90 Segundos

Exemplo detalhado do pipeline completo para o caso de uso mais comum.

```mermaid
sequenceDiagram
    actor U as Usuário
    participant CMD as criar-video.md
    participant MOS as Marketing OS
    participant CM as Clone Manifest
    participant MB as Clone MrBeast
    participant RA as Research Agent
    participant VA as Video Agent
    participant CPA as Copy Agent
    participant QG as Quality Gate
    participant OUT as Output

    U->>CMD: "Crie um Reels de 90s viral sobre produtividade"

    CMD->>MOS: Ativar Video Agent + coletar briefing
    MOS->>U: Confirmar: nicho, público, CTA?
    U->>MOS: Empreendedorismo · Seguidores · Seguir perfil

    MOS->>CM: content_type = "reels", objetivo = "viral"
    CM-->>MOS: primary = mrbeast

    MOS->>MB: Carregar profile.md + voice.md + frameworks.md
    MB-->>MOS: Tom épico, challenge-driven, re-hooks a cada 30s

    MOS->>RA: Pesquisar tendências produtividade + empreendedorismo
    RA-->>MOS: Hooks em alta, formato em alta, dados relevantes

    MOS->>VA: Gerar roteiro 90s com clone MrBeast
    Note over VA: Estrutura 90s:<br/>Hook (0-3s) → Promessa (3-8s)<br/>Ponto 1 (8-28s) → Re-hook (28-32s)<br/>Ponto 2 (32-52s) → Ponto 3 (52-72s)<br/>CTA + Loop (72-90s)
    VA-->>MOS: Roteiro completo com timecodes

    MOS->>CPA: Gerar 3 variações A/B do hook
    CPA-->>MOS: Hook A (curiosidade) · B (controvérsia) · C (resultado)

    MOS->>QG: Validar conteúdo
    Note over QG: ✓ Sem travessão longo<br/>✓ Sem aspas em roteiro<br/>✓ Sem caps<br/>✓ Acentuação correta<br/>✓ Enquete incluída<br/>✓ Fatos verificados

    QG-->>MOS: Aprovado

    MOS->>OUT: Montar output final
    OUT-->>U: Roteiro completo + hooks A/B +<br/>specs técnicos + caption +<br/>hashtags + enquete + métricas-alvo
```

### Estrutura Interna do Roteiro de 90s

```mermaid
gantt
    title Estrutura de Reels 90 Segundos
    dateFormat ss
    axisFormat %Ss

    section Atenção
    HOOK — Pattern interrupt visual + Frase de parada de scroll    : crit, 00, 3s
    PROMESSA — O que vão aprender / ganhar                        : 03, 5s

    section Conteúdo
    PONTO 1 — Primeiro insight com exemplo real                    : 08, 20s
    RE-HOOK — Frase que recupera atenção (obrigatório)            : crit, 28, 4s
    PONTO 2 — Segundo insight com prova/dado                      : 32, 20s
    PONTO 3 — Insight mais surpreendente (melhor para o final)    : 52, 20s

    section Conversão
    CTA + LOOP — Ação clara + frase que conecta ao início         : crit, 72, 18s
```

---

## 8. Integrações MCP

```mermaid
graph LR
    MOS(["Marketing OS"])

    MOS <-->|"Criar páginas\nAtualizar databases\nPublicar conteúdo"| N["📓 Notion MCP\nGerenciamento de conteúdo\ncalendário editorial"]

    MOS <-->|"Ler specs de design\nExtrair paletas\nSync variáveis"| F["🎨 Figma MCP\nDesign specs\nStyle guides"]

    MOS <-->|"Criar designs\nTemplates\nVisual content"| C["🖌️ Canva MCP\nDesign automation"]

    MOS <-->|"Notificações\nAprovals\nTeam updates"| S["💬 Slack MCP\nTeam collaboration"]

    MOS <-->|"Análise de tráfego\nShare of voice\nCompetidores"| SW["📊 SimilarWeb MCP\nCompetitor intelligence"]

    MOS <-->|"Captura screenshots\nTeste de landing pages\nScraping visual"| PW["🎭 Playwright MCP\nBrowser automation"]

    style MOS fill:#533483,color:#fff
    style N fill:#0f3460,color:#eee
    style F fill:#1a1a2e,color:#eee
    style C fill:#16213e,color:#eee
    style S fill:#2d3561,color:#eee
    style SW fill:#0d4f4f,color:#eee
    style PW fill:#1a2e1a,color:#eee
```

---

## 9. Scripts Python

```mermaid
graph TB
    CLI["mos.py\nCLI principal"]

    subgraph CONTENT["Geração de Conteúdo"]
        RG["reels_script_generator.py\nScripts Reels 15/30/60/90s"]
        HG["hook_generator.py\nHooks virais por categoria"]
        HVG["hook_variant_generator.py\nVariações A/B de hooks"]
        CIG["content_idea_generator.py\nIdeias de conteúdo por nicho"]
        CRG["content_repurposer.py\nRepurpose entre formatos"]
        CAP["caption_generator.py\nLegendas por objetivo"]
        CSG["carousel_structure_generator.py\nEstruturas de carrossel"]
        CCG["content_calendar.py\nCalendário editorial"]
    end

    subgraph ANALYTICS["Analytics e Otimização"]
        SEO["seo_analyzer.py\nAnálise SEO on-page"]
        GSC["gsc_analyzer.py\nGoogle Search Console"]
        HS["headline_scorer.py\nScore de headlines"]
        RC["readability_checker.py\nLegibilidade e clareza"]
        CA["content_audit.py\nAuditoria de conteúdo"]
        YT["youtube_analytics.py\nMétricas YouTube"]
        AB["ab_generator.py\nVariações A/B"]
        WR["weekly_report.py\nRelatório semanal"]
    end

    subgraph RESEARCH["Pesquisa e Trends"]
        CX["competitor_analyzer.py\nAnálise de concorrentes"]
        TT["trend_tracker.py\nMonitoramento de tendências"]
        TTS["tiktok_trends_scraper.py\nTrends TikTok"]
        TA["trend_adapter.py\nAdaptar trends ao nicho"]
        IHR["instagram_hashtag_research.py\nPesquisa hashtags IG"]
        HH["hashtag_generator.py\nGeração de hashtags"]
    end

    subgraph INTEGRATIONS["Integrações e APIs"]
        NOT["notion_api.py\nNotion REST API"]
        IG["instagram_api.py\nInstagram Graph API"]
        META["meta_ads_api.py\nMeta Ads API"]
    end

    subgraph INFRA["Infraestrutura"]
        VAL["validators.py\nValidação de inputs"]
        QG["quality_gate.py\nGate de qualidade"]
        OF["output_formatter.py\nJSON · Markdown · HTML"]
        PM["project_manager.py\nWorkflow + handoffs + approval gates"]
    end

    CLI --> CONTENT
    CLI --> ANALYTICS
    CLI --> RESEARCH
    CLI --> INTEGRATIONS
    CONTENT --> INFRA
    ANALYTICS --> INFRA
    RESEARCH --> INFRA
    INTEGRATIONS --> INFRA

    style CONTENT fill:#0f3460,color:#eee,stroke:#4a8aaa
    style ANALYTICS fill:#1a1a2e,color:#eee,stroke:#4a4a8a
    style RESEARCH fill:#16213e,color:#eee,stroke:#888
    style INTEGRATIONS fill:#0d4f4f,color:#eee,stroke:#0d7377
    style INFRA fill:#2e1a1a,color:#eee,stroke:#8a4a4a
```

---

## 10. Mapa de Arquivos

```mermaid
graph TD
    ROOT["📁 Marketing OS/"]

    ROOT --> SK["📁 skills/marketing-os/\nSistema A — Skill Package"]
    ROOT --> MO["📁 marketing-os/\nSistema B — Command Plugin"]
    ROOT --> SQ["📁 squads/marketing-os/\nDados e Clones"]
    ROOT --> SC["📁 scripts/\n30 scripts Python"]
    ROOT --> WF["📁 workflows/\n9 workflows"]
    ROOT --> RF["📁 references/\n9 arquivos de referência"]
    ROOT --> SA["📁 subagents/\n18 subagentes .md"]
    ROOT --> DC["📁 docs/\nDocumentação"]
    ROOT --> CL["📁 .claude/\nCommands e Regras"]

    SK --> SK1["SKILL.md (v16)\nOrquestrador"]
    SK --> SK2["subagents/ (16)"]
    SK --> SK3["assets/\ntemplates · swipe-files\nframeworks · checklists"]
    SK --> SK4["scripts/ (symlink)"]
    SK --> SK5["references/ (symlink)"]

    MO --> MO1["skills/marketing-os/\nSKILL.md (v5.0 / 17 agents)"]
    MO --> MO2["commands/ (24)\n/criar-video · /criar-post..."]
    MO --> MO3["skills/ (19 packages\nindividuais)"]
    MO --> MO4[".claude-plugin/\nplugin.json"]
    MO --> MO5["CONNECTORS.md\nMCPs documentados"]

    SQ --> SQ1["data/clones/\nclone-manifest.yaml\n+ 34 pastas de clones"]
    SQ --> SQ2["cada clone/\nprofile.md · voice.md\nframeworks.md · examples.md"]

    CL --> CL1["commands/\nmarketing-os.md (v11 → sync)"]
    CL --> CL2["rules/\nworkflow-execution.md\nstory-lifecycle.md\nids-principles.md\nagent-authority.md"]

    style ROOT fill:#533483,color:#fff
    style SK fill:#0f3460,color:#eee,stroke:#4a8aaa
    style MO fill:#1a1a2e,color:#eee,stroke:#4a4a8a
    style SQ fill:#16213e,color:#eee,stroke:#888
    style SC fill:#0d4f4f,color:#eee,stroke:#0d7377
    style CL fill:#2e1a1a,color:#eee,stroke:#8a4a4a
```

---

## Resumo Executivo

| Componente | Quantidade | Localização |
|---|---|---|
| Sistemas de entrada | 2 (A + B) | `plugin.json` raiz + `marketing-os/.claude-plugin/` |
| Slash commands | 24 | `marketing-os/commands/` |
| Subagentes | 18 | `subagents/` + `skills/marketing-os/subagents/` |
| Clones de voz | 34 | `squads/marketing-os/data/clones/` |
| Regras de matching | 70+ | `clone-manifest.yaml` |
| Templates | 23+ | `skills/marketing-os/assets/templates/` |
| Swipe files | 7 | `skills/marketing-os/assets/swipe-files/` |
| Workflows | 9 | `workflows/` |
| Scripts Python | 30+ | `scripts/` |
| Integrações MCP | 6 | Notion · Figma · Canva · Slack · SimilarWeb · Playwright |
| Nichos suportados | 10+ | `references/niches.md` |

---

*Última atualização: 2026-05-06 (plugin-first refactor)*
*Renderizar com Markdown Preview Enhanced (VSCode)*
