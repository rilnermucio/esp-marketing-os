---
description: "Cria ou atualiza o perfil de marca do projeto (nicho, público, oferta, voz, proibições, categoria regulada, canais) em workspace/brand/perfil.md, que todos os especialistas leem antes de produzir. Use quando começar um projeto ou quando a marca mudar."
argument-hint: "<nome da marca ou negócio> [materiais: site, perfil, textos colados]"
---

# /configurar-marca: Perfil de marca do projeto

Monta, uma vez por projeto, o contexto que hoje o orquestrador pergunta a cada sessão e que cada agent reconstruía sozinho. O resultado é `workspace/brand/perfil.md`, **no projeto do usuário**. Todos os agents do Marketing OS leem esse arquivo antes de produzir, e ele prevalece sobre suposições genéricas.

## Quando usar

- Primeira sessão num projeto ou cliente novo
- A marca mudou (nova oferta, novo público, novo tom, rebranding)
- Os resultados estão saindo genéricos ou fora do tom

## Inputs (pergunte o que faltar, numa lista única)

1. **Negócio**: nome, nicho, oferta principal e ticket
2. **Público**: quem compra e qual dor principal resolve (se já existir `workspace/brand/avatar.md`, use-o)
3. **Voz**: 3 adjetivos, 2 ou 3 textos que soam como a marca, e o que a marca nunca diria
4. **Proibições**: palavras, promessas e temas fora de pauta
5. **Categoria regulada**: saúde (qual profissão), finanças, suplementos, cosméticos, advocacia ou nenhuma
6. **Canais**: plataformas prioritárias, frequência e CTA padrão
7. **Materiais opcionais**: site, perfis, posts, emails, apresentações

Se o usuário colar materiais, extraia deles o que puder e pergunte só o resto.

## Pre-flight (orquestrador inline)

1. Se `workspace/brand/perfil.md` já existir, leia e pergunte se é para atualizar campos específicos ou refazer.
2. Leia, se existirem, `workspace/brand/avatar.md`, `workspace/brand/usp.md` e `workspace/brand/oferta.md` (criados por `/criar-avatar`, `/criar-usp` e `/criar-oferta`) e passe o essencial ao agent.
3. Se houver clone pessoal em `workspace/clones/*/`, registre o slug no campo de voz.

## Dispatch

```
Agent(subagent_type: "marketing-os:mos-brand", prompt: "Monte o Perfil de Marca do projeto [nome] a partir dos inputs abaixo e dos materiais anexados. Inputs: [nicho, oferta e ticket, público, voz, proibições, categoria regulada, canais]. Materiais: [trechos colados ou resumo dos arquivos]. Dossiês existentes: [resumo de avatar/usp/oferta, se houver].

Entregue EXATAMENTE no schema abaixo, em PT-BR, sem inventar dado que não foi informado (marque 'a definir' e diga qual pergunta fecharia o campo):

# Perfil de marca: [nome]
> Atualizado em [AAAA-MM-DD] por /configurar-marca. Os agents do Marketing OS leem este arquivo antes de produzir.

## Negócio
- Nicho:
- Oferta principal e ticket:
- Diferencial (USP), em uma frase:

## Público
- Quem compra:
- Dor principal e desejo principal:
- Objeções mais comuns:

## Voz
- Tom (3 adjetivos):
- A marca fala assim (2 exemplos curtos):
- A marca nunca fala assim (2 exemplos curtos):
- Clone de voz pessoal: [slug em workspace/clones/ ou 'nenhum']

## Proibições
- Palavras e expressões proibidas:
- Promessas proibidas:
- Temas fora de pauta:

## Compliance
- Categoria regulada e órgão: [ex: odontologia, CFO/CRO; ou 'nenhuma']
- Disclaimers obrigatórios:

## Canais
- Plataformas prioritárias e frequência:
- CTA padrão:

## Referências
- Concorrentes e marcas de referência:

Regras: frases curtas; nada de travessão, 'brutal' ou antítese negação/afirmação; categoria regulada com o conselho correto (medicina CFM/CRM, odontologia CFO/CRO, nutrição CFN/CRN, psicologia CFP/CRP, advocacia OAB, suplementos e cosméticos ANVISA, investimentos CVM)."
)
```

## Consolidação

1. Mostre o perfil ao usuário e aplique as correções pedidas.
2. Salve em `workspace/brand/perfil.md` (crie a pasta se preciso). Se já existia, preserve a versão anterior como `workspace/brand/perfil-AAAA-MM-DD.md`.
3. Diga ao usuário o que muda: os próximos pedidos já saem no tom e nas regras do perfil, e o orquestrador deixa de repetir as perguntas de nicho, público e canal.

## Quality Gates

Aplique os gates globais do SKILL.md do Marketing OS ao texto do perfil (sem travessão, sem "brutal", sem antítese, PT-BR acentuado). Campo sem informação fica como "a definir", nunca inventado.

## Por que esse dispatch

Identidade, voz e posicionamento são o domínio do `mos-brand`. Um perfil único no projeto evita que 21 especialistas deduzam a marca cada um do seu jeito, e é o que transforma a memória por agent em contexto compartilhado.
