---
description: "Revisa uma peça pronta contra as regras de publicidade do Brasil: conselhos (CFM, CFO, CFN, CFP, OAB, CREF), ANVISA, CVM, CONAR, CDC e LGPD. Use quando perguntarem se pode publicar, se a peça tem risco legal ou o que falta de identificação profissional."
argument-hint: "<peça colada ou caminho do arquivo> [quem anuncia: profissão ou categoria] [plataforma]"
---

# /checar-compliance: Risco regulatório da peça

Revisa uma peça pronta (post, anúncio, landing page, email, roteiro) contra as regras de publicidade que valem no Brasil e devolve o que mudar, com a norma de cada ponto. A fonte é `${CLAUDE_PLUGIN_ROOT}/references/compliance-br.md`, verificada em 2026-09-28 no texto integral das normas. O resultado sinaliza risco e não substitui parecer jurídico.

## Inputs (pergunte o que faltar)

1. **Peça**: texto colado ou caminho do arquivo. Se o usuário apontar uma peça desta conversa, use o texto dela.
2. **Quem anuncia**: profissão e conselho (médico, dentista, nutricionista, psicólogo, advogado, educador físico), produto regulado (suplemento, cosmético, medicamento), finanças, infoproduto, e-commerce ou influenciador. Se `workspace/brand/perfil.md` existir no projeto, a categoria regulada está lá.
3. **Onde vai rodar**: orgânico ou anúncio, e em qual plataforma.

## Passo 1: checagem determinística (orquestrador)

Se a peça veio colada, salve num arquivo temporário. Rode:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/compliance_check.py" --input <arquivo-da-peca>
```

O script usa as mesmas regras do hook do plugin e lista cada trecho de risco com a norma. Guarde a saída para o dispatch.

## Dispatch

```
Agent(subagent_type: "marketing-os:mos-copy", prompt: "Revise o compliance desta peça para publicação no Brasil.

Leia antes: ${CLAUDE_PLUGIN_ROOT}/references/compliance-br.md (a seção da categoria, 'Frases de risco' e 'Identificações e avisos aceitos').

Peça completa: [texto integral]
Quem anuncia: [profissão, conselho ou categoria]
Onde vai rodar: [orgânico ou anúncio; plataforma]
Saída do checador automático: [colar a saída do compliance_check.py]

Entregue:
1. Veredito: pode publicar, publicar com ajustes ou não publicar.
2. Tabela com trecho, problema, norma e artigo, severidade (bloqueia, ajuste ou atenção) e reescrita sugerida.
3. Identificação obrigatória que falta (CRM e RQE, CRO, CRN, CRP, OAB, CREF ou registro no conselho).
4. Avisos exigidos para a categoria.
5. A peça completa já corrigida.
6. O que depende de documento fora da peça: TCLE, autorização escrita de depoimento, registro na CVM, licença de apostas, opt-in.

Regras: cite só normas que estão na referência; se a referência não cobre o caso, diga isso e recomende consulta ao conselho ou a um advogado; nunca invente artigo; entre conselho e plataforma, vale a regra mais restritiva. A reescrita segue a voz da marca e os quality gates.")
```

## Saída (consolidação do orquestrador)

1. Veredito no topo, em uma linha.
2. Tabela de pontos com a norma de cada um.
3. Peça corrigida, pronta para copiar.
4. Pendências fora da peça (documentos e autorizações).
5. Linha final: "Sinaliza risco com base nas normas verificadas em 2026-09-28 e não substitui parecer jurídico."

## Quality Gates

Aplique os gates globais do SKILL.md do Marketing OS à peça corrigida e ao texto da análise: sem travessão, sem "brutal", sem antítese negação e afirmação, sem CAPS gratuito (as identificações exigidas pelo CFM em caixa alta, como MÉDICO e NÃO ESPECIALISTA, são exceção por norma), PT-BR acentuado.

## Por que esse dispatch

O `mos-copy` é dono da reescrita e tem a PARTE XIV de compliance; a referência canônica é a mesma que os outros especialistas consultam. O checador roda antes porque é determinístico e dá ao agent os trechos exatos para revisar. O command não usa `context: fork` (ADR-0007) porque a peça costuma vir desta conversa, que o fork não vê.
