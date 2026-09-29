# Architecture Decision Records

Decisões estruturais ou difíceis de reverter, com contexto e alternativas rejeitadas. Escreva um ADR quando a decisão: muda a forma do sistema (camadas, fronteiras de agents, formato de distribuição), será questionada de novo no futuro, ou rejeita um caminho que parece óbvio.

Numeração sequencial, status `proposto | aceito | substituído por ADR-NNNN`. ADR aceito não se edita para mudar a decisão; escreve-se outro que o substitui.

| ADR | Título | Status |
|---|---|---|
| [0001](0001-arquitetura-two-tier.md) | Arquitetura two-tier com skill orquestradora | Aceito |
| [0002](0002-defesa-em-tres-camadas.md) | Quality gates: defesa em 3 camadas com hook canônico | Aceito (fiação corrigida pela 0005) |
| [0003](0003-gate-na-fronteira-de-output.md) | Contrato de qualidade na fronteira de output | Aceito (fiação corrigida pela 0005) |
| [0004](0004-chatgpt-work-skills-only.md) | ChatGPT Work e Codex por pacote universal skills-only | Aceito |
| [0005](0005-plugin-instalado-runtime.md) | Plugin instalado: recursos pela raiz do plugin, dispatch qualificado e gates no nível do plugin | Aceito |
| [0006](0006-memoria-no-diretorio-nativo.md) | Memória dos agents no diretório nativo de agent de plugin | Aceito |
| [0007](0007-command-com-context-fork.md) | Dispatch garantido pela plataforma em command de agent único (`context: fork`) | Aceito (piloto em `/gerar-imagem`) |

Template: [TEMPLATE.md](TEMPLATE.md)
