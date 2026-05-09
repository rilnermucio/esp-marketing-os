# Configuração White-label da Auditoria

O comando `/auditoria` gera RELATORIO.pdf com branding customizável. Pra agências/freelancers brasileiros que entregam pro cliente final.

## Setup rápido

Crie `.auditoria-config.json` na raiz do projeto onde você roda `/auditoria`:

```json
{
  "brand_name": "Sua Agência",
  "logo_path": "./logo.png",
  "primary_color": "#1a1a1a",
  "accent_color": "#0066cc",
  "footer_text": "© 2026 Sua Agência. Auditoria preparada para Cliente X."
}
```

Próximo `/auditoria` aplica o branding automaticamente.

## Schema completo

| Campo | Tipo | Obrigatório | Default |
|---|---|---|---|
| `brand_name` | string (não-vazio) | Sim | (n/a) |
| `logo_path` | string (path relativo ao config) | Não | sem logo |
| `primary_color` | hex `#RRGGBB` | Não | `#1a1a1a` |
| `accent_color` | hex `#RRGGBB` | Não | `#1a73e8` |
| `footer_text` | string | Não | `Auditoria gerada com marketing-os` |

Campos extras desconhecidos são rejeitados (config inteiro é ignorado, PDF sai neutro).

## Comportamento de erro

| Caso | Resultado |
|---|---|
| Sem config | PDF neutro (default theme + footer marketing-os) |
| JSON malformado | Warning em stderr, PDF neutro |
| Schema inválido | Warning em stderr com a falha do jsonschema, PDF neutro |
| `logo_path` aponta pra arquivo inexistente | Warning, PDF sem logo (resto do branding aplicado) |
| Cor fora do padrão hex | Schema inválido, PDF neutro |

## Exemplo: agência multi-cliente

Mantenha `.auditoria-config.json` por cliente em sub-pastas:

```
clientes/
  cliente-a/
    .auditoria-config.json  <- branding cliente A
    auditorias/...
  cliente-b/
    .auditoria-config.json  <- branding cliente B
```

`/auditoria` dentro de cada pasta usa o config local automaticamente.

## Limitações conhecidas

- Logo precisa estar em formato `.png`, `.jpg` ou `.svg`. SVG embutido funciona melhor pra escala.
- Cores são aplicadas via CSS variables. Não há suporte a gradientes na v1.
- Footer custom substitui completamente o footer padrão. Se quiser preservar a atribuição marketing-os, inclua manualmente em `footer_text`.
- macOS: se `weasyprint` falhar com erro de bibliotecas dinâmicas, instale dependências do sistema: `brew install cairo pango gdk-pixbuf libffi`. O `pdf_generator.py` configura `DYLD_FALLBACK_LIBRARY_PATH` automaticamente quando detecta as libs em `/opt/homebrew/lib`.
