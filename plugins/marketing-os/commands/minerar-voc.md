---
description: "Extrai a voz do cliente de reviews, comentários, respostas de pesquisa, tickets ou reclamações: dores, desejos, objeções e as palavras literais do público. Use quando pedirem para entender o que os clientes dizem ou buscar linguagem real para copy e oferta."
argument-hint: "<material: arquivo, texto colado ou fontes públicas> [produto ou nicho]"
---

# /minerar-voc: Voz do cliente

Transforma o que o público já escreveu em matéria-prima de copy, oferta e avatar: dores, desejos, objeções e resultados, com a frase literal de quem disse. Copy com as palavras do cliente soa verdadeira e dá prova para as decisões de oferta.

## Inputs (pergunte o que faltar)

1. **Material**: reviews, comentários, respostas de pesquisa, tickets de suporte, transcrições de call de venda ou reclamações. Aceita arquivo `.txt`, `.csv` ou `.json`, ou texto colado.
2. **Produto ou nicho** analisado.
3. **Sem material próprio?** O agent pode buscar fontes públicas (reclamações no Reclame Aqui, reviews de concorrentes, comentários de vídeos do nicho), com o link de cada trecho.

## Dispatch

```
Agent(subagent_type: "mos-research", prompt: "Minere a voz do cliente sobre [produto ou nicho].

PASSO 1, extração determinística (se houver arquivo): rode `python3 scripts/voc_extractor.py --input <arquivo> [--coluna <coluna> | --campo <campo>]`. O script separa frases literais por sinal (dor, desejo, objeção, resultado) e conta expressões repetidas. Com texto colado, salve num arquivo temporário e rode igual. Sem material, busque fontes públicas e guarde o link de cada trecho.

PASSO 2, interpretação sobre o que o script trouxe:
- Dores, desejos, objeções e resultados, cada um com 2 ou 3 frases literais, a frequência e a intensidade
- Gatilhos de compra e de desistência
- Segmentos que aparecem no material (quem fala o quê)
- Glossário do cliente: palavras e expressões que o público usa e a marca deveria usar
- Lacunas: o que o público pede e ninguém oferece

Regras: frase literal só se estiver no material; anonimize nomes, perfis e qualquer dado pessoal (LGPD); não generalize a partir de 1 ou 2 relatos sem dizer que é sinal fraco.

Entregue também um Handoff Context curto para mos-copy (frases de gancho), mos-offer (objeções a quebrar) e mos-research (atualizar o avatar).")
```

## Consolidação

1. Tabelas de dores, desejos, objeções e resultados com frase literal, frequência e intensidade.
2. Glossário do cliente e lacunas.
3. Próximos passos sugeridos: `/criar-avatar` com este material, `/criar-oferta` para as objeções, `/otimizar-copy` com o glossário.
4. Salve em `workspace/brand/voc.md` no projeto do usuário (preserve a versão anterior com data no nome). Se `workspace/brand/perfil.md` existir, acrescente as 3 objeções principais na seção Público.

## Quality Gates

Aplique os gates globais do SKILL.md do Marketing OS ao texto de análise. As frases literais do cliente ficam como estão, entre aspas, porque são citação de fato; nada de corrigir a fala do público. Nenhum nome ou perfil identificável na entrega.

## Por que esse dispatch

Pesquisa de público é domínio do `mos-research`, que tem Bash para o extrator e WebSearch para fontes públicas. O script garante que as frases citadas existem no material; o agent faz a leitura qualitativa em cima delas.
