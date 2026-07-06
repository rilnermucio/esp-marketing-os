---
description: Turn an optimized AI image prompt into an actual PNG. Dispatches mos-ai-tools (prompt engineering) e executa a geração via skill de imagem disponível no ambiente (gpt-image-2 / ai-image-generation), com fallback pra entrega do prompt.
argument-hint: "<o que gerar + uso, ex: 'foto de produto do e-book, fundo clean, pra anúncio 1:1'>"
---

# /renderizar-imagem: Prompt vira PNG (Dispatch + Execução)

Fecha o gap "só gera prompt": o `mos-ai-tools` faz a engenharia do prompt e a skill de geração de imagem do ambiente renderiza o arquivo. O plugin **prepara e valida**; a skill externa **executa** (política de delegação da SKILL.md: estratégia antes do build técnico).

## Required inputs (ask if missing)

1. **Subject** (obrigatório): o que a imagem mostra
2. **Uso** (obrigatório): anúncio, post, capa, site, produto (define aspecto e estilo)
3. **Aspect ratio** (opcional): 1:1, 16:9, 9:16, 4:3 (default pelo uso)
4. **Estilo/mood** (opcional): fotorrealista, ilustração, 3D, minimalista, cinematic
5. **Texto na imagem?** Se a imagem precisa de TEXTO legível (thumbnail, capa com título), redirecionar pra `/gerar-thumbnail`: gerador renderiza texto mal; lá o overlay é tipográfico

## Fase 1: engenharia do prompt (dispatch)

```
Agent(subagent_type: "mos-ai-tools", prompt: "Gere prompt otimizado para geração de imagem. Subject: [subject]. Uso: [uso]. Aspect ratio: [ar]. Estilo: [estilo]. Mood: [mood]. IMPORTANTE: a imagem NÃO deve conter texto nem letreiros (texto entra em pós-produção quando necessário). Entregue: 1 prompt principal em inglês (modelos renderizam melhor) com descrição de composição, luz e lente; negative prompt quando aplicável; 2 variações de ângulo/estilo. Estruture em markdown.")
```

Se o usuário já vem com prompt pronto (ex: output do `/gerar-imagem`), pule a Fase 1 e valide apenas: sem texto embutido, aspect ratio definido.

## Fase 2: renderização (executa)

Detecte a skill de imagem disponível no ambiente, nesta ordem de preferência:

1. **`gpt-image-2`** (usa o plano ChatGPT do usuário, sem custo por imagem à parte)
2. **`ai-image-generation`**

Invoque a skill disponível com o prompt principal da Fase 1 e salve o resultado em:

```
workspace/media/imagens/<slug-do-subject>-<YYYYMMDD>.png
```

(crie o diretório se não existir; `workspace/` é pessoal e gitignored)

**Fallback (nenhuma skill de imagem no ambiente)**: entregue o prompt principal + variações + instruções de uso manual (colar no Midjourney/DALL-E/Flux) e diga explicitamente qual skill instalar pra automatizar da próxima vez. Nunca finja que renderizou.

## Consolidação

```markdown
## Imagem renderizada: [subject]

Arquivo: workspace/media/imagens/[nome].png | Aspect: [ar] | Skill usada: [gpt-image-2 | ai-image-generation | fallback manual]

### Prompt usado
[prompt principal]

### Variações disponíveis (se quiser re-renderizar)
[variação A, variação B]

### Próximos passos
- Precisa de texto na imagem: /gerar-thumbnail (overlay tipográfico legível)
- Usar no anúncio/post: o arquivo já está no workspace, referencie no criativo
```

## Quality Gates (antes de entregar)

Aplicar gates globais do `skills/marketing-os/SKILL.md`:
- Prompt sem pedido de texto embutido (texto renderizado por IA sai ilegível; é FAIL de processo)
- Imagem com pessoa reconhecível ou marca de terceiro: alertar direito de imagem/uso antes de entregar
- Arquivo salvo em `workspace/media/` (nunca em path versionado do plugin)
- Acentuação PT-BR correta na entrega

## Por que esse dispatch

Prompt engineering e renderização são competências separadas: o `mos-ai-tools` conhece a anatomia de prompt por ferramenta (o que o `/gerar-imagem` já entregava), e a skill externa executa com a credencial do usuário. O command fecha a ponte que faltava entre os dois, com fallback honesto quando o ambiente não tem skill de geração.
