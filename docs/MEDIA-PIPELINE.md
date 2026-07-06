# Media Pipeline (Fase 2): de prompt a arquivo real

> Como os commands de mídia real funcionam, o que exigem do ambiente e como degradam quando falta ferramenta. Padrão herdado do `/narrar-roteiro`: **o plugin prepara e valida; a execução local/skill externa renderiza**.

## Os 4 commands do pipeline

| Command | Entrega | Prepara (dispatch) | Executa (ambiente) |
|---|---|---|---|
| `/narrar-roteiro` | Áudio PT-BR narrado | mos-audio (texto falável + timing + tom) | `scripts/tts_runner.py` (say/kokoro, local) |
| `/renderizar-imagem` | PNG | mos-ai-tools (prompt sem texto embutido) | Skill `gpt-image-2` ou `ai-image-generation` |
| `/gerar-thumbnail` | Thumbnail 1280x720 | mos-video (brief) + mos-ai-tools (fundo) | Skill de imagem + `scripts/thumbnail_composer.py` (overlay tipográfico local) |
| `/produzir-reels` | Vídeo vertical legendado | mos-video (roteiro + timeline) + mos-audio | TTS local + HyperFrames (`npx hyperframes render`) + opcional `ai-video-generation` |

## Dependências de ambiente (nenhuma é distribuída pelo plugin)

| Ferramenta | Usada por | Como obter | Sem ela |
|---|---|---|---|
| Skill `gpt-image-2` | renderizar-imagem, gerar-thumbnail | Skill Claude Code (usa plano ChatGPT via Codex CLI local) | Fallback: prompt pronto + instruções manuais |
| Skill `ai-image-generation` | idem (alternativa) | Skill Claude Code | idem |
| Pillow (`pip install -r requirements.txt`) | gerar-thumbnail (overlay) | requirements.txt do repo | Script instrui a instalação |
| TTS local (say no macOS; kokoro fora) | narrar-roteiro, produzir-reels | `say` nativo; kokoro via skill hyperframes-media | Roteiro falável entregue pra gravação manual |
| HyperFrames (`npx hyperframes`) | produzir-reels | npm/npx (skill hyperframes documenta) | Composição pronta + comando de render entregues |
| Skill `ai-video-generation` | produzir-reels (b-roll opcional) | Skill Claude Code | Fundo sólido com legendas (estilo caption video) |

## Regras do pipeline (valem pra todos)

1. **Texto nunca vai no prompt de imagem.** Gerador renderiza texto mal; texto entra por overlay determinístico (`thumbnail_composer.py`) ou legenda HyperFrames. Prompt pedindo letreiro é FAIL de processo.
2. **Output sempre em `workspace/media/`** (gitignored): `imagens/`, `thumbnails/`, `reels/`. Nunca em path versionado (guard `test_workspace_separation.py`).
3. **Degradação honesta**: cada command declara o degrau alcançado e o que faltou. Reportar mídia que não foi renderizada é violação direta (F-REG na taxonomia de falhas).
4. **Resultado real alimenta memory**: CTR de thumbnail → mos-video; retenção de Reels → mos-video; imagem aprovada → prompt registrado. É o começo do loop da Fase 4 do ROADMAP.

## Escopo (o que este pipeline NÃO faz)

Publicar, agendar ou fazer upload nas plataformas. O plugin gera e valida o arquivo; publicação é papel de MCP/ferramenta externa com gate humano (princípio de escopo do `docs/ROADMAP.md`).
