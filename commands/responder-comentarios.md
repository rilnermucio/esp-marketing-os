---
description: Triagem e rascunhos de resposta para comentários/DMs no tom da marca. Dispatches mos-community; publicação só com aprovação humana item a item.
argument-hint: "<comentários colados ou peça (reels/post) + contexto de marca/tom, ex: 'último reels de skincare, tom acolhedor'>"
---

# /responder-comentarios: Fila de Rascunhos de Comunidade (Dispatch-Based)

Classifica comentários e DMs, redige rascunhos no tom da marca e entrega fila pra aprovação orquestrando `Agent(subagent_type: "mos-community")`. **Nada é publicado automaticamente.**

## Required inputs (ask if missing)

1. **Comentários ou peça** (obrigatório): texto colado, export, ou identificação da publicação
2. **Plataforma** (obrigatório): Instagram, TikTok, YouTube, LinkedIn, etc.
3. **Contexto de marca/tom** (obrigatório se memory vazia): guidelines, exemplos de respostas anteriores, ou pedir `mos-brand` antes
4. **Políticas** (opcional): o que pode prometer (reembolso, desconto), SLA desejado, tom proibido

## Coleta de comentários

```
Comentários disponíveis?
  ├── Usuário colou/exportou → usar direto no dispatch
  ├── MCP instagram_get_comments disponível → buscar comentários da peça
  └── MCP tiktok_get_comments disponível → buscar comentários da peça
```

Se nenhuma fonte: pedir ao usuário colar os comentários ou informar o link/ID da peça.

## Dispatch Simples

```
Agent(subagent_type: "mos-community", prompt: "Monte a fila de rascunhos de resposta. Plataforma: [plataforma]. Peça: [post/reels/DM]. Comentários: [lista ou resumo da coleta MCP]. Tom de voz: [guidelines/memory]. Políticas: [o que pode/não pode prometer]. Classifique cada interação (elogio, dúvida, objeção, reclamação, troll/hate, lead quente, spam). Para itens sensíveis, entregue 2-3 variações de tom e red team. Entregue no Output Schema: fila com comentário original → classificação → rascunho → ação recomendada. Modo: RASCUNHO ONLY. Nada publicado sem aprovação humana. Aplicar quality gates globais.")
```

## Publicação opcional (após aprovação humana)

Somente se **MCP disponível** E usuário aprovou **item a item**:

```
Para cada item aprovado:
  instagram_reply_comment(comment_id, text)  # ou equivalente da plataforma
```

Declarar no output final: **modo rascunho** (default) ou **modo publicado** (itens enviados com confirmação).

## Consolidação

Entregue ao usuário:

```markdown
## Fila de Rascunhos: [plataforma / peça]

### Modo de entrega
[RASCUNHO | PUBLICADO (itens: N)]

### Resumo
- Total: [N] | Por tipo: [elogio X, dúvida Y, ...]
- Prioridade imediata: [itens <24h]
- Exigem humano: [lista]

### Fila
[Tabela: original → classificação → rascunho → ação]

### Próximos passos
- Revisar e aprovar cada rascunho
- Publicar manualmente ou autorizar MCP item a item
- Registrar respostas que performaram bem na memory do mos-community
```

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md` + gates do mos-community:
- **Aprovação humana obrigatória** antes de qualquer publicação
- Declarar modo (rascunho vs publicado) explicitamente
- Sem promessas de resultado/reembolso não autorizadas
- Sem `—`, sem "brutal", sem antítese negação→afirmação, acentos PT-BR

## Por que esse dispatch

Responder comentário exige classificação, tom de marca e julgamento de escalação em cada item. Misturar isso com criação de post (mos-social) contamina o fluxo. O `mos-community` isola triagem + rascunho com red team condicional e nunca publica: o humano mantém controle sobre o que a marca diz publicamente.
