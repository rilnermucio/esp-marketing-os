# reels_script_generator.py — Gerador de roteiros para Reels com timestamps e direções de câmera

O `reels_script_generator.py` gera roteiros completos para vídeos curtos no formato Reels (Instagram, TikTok, YouTube Shorts), com timestamps, tipo de cena, descrição editorial e direção de câmera para cada parte. O script seleciona automaticamente um hook e um CTA adequados ao tema e imprime o roteiro formatado no terminal. Suporta oito estruturas narrativas distintas e quatro durações padrão.

## Uso via CLI

```bash
# Roteiro tutorial de 30 segundos (padrão)
python scripts/reels_script_generator.py "5 dicas de produtividade"

# Especificar duração
python scripts/reels_script_generator.py "marketing digital" 60

# Especificar formato
python scripts/reels_script_generator.py "finanças pessoais" 30 listicle

# Formato storytelling de 90 segundos
python scripts/reels_script_generator.py "minha jornada empreendedora" 90 storytime

# Listar todos os formatos disponíveis
python scripts/reels_script_generator.py --formatos
```

## Argumentos

| Argumento | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `tema` | `str` (posicional) | Sim | — | Tema do vídeo (máx. 200 caracteres) |
| `duracao` | `int` (posicional) | Não | `30` | Duração em segundos. Valores válidos: `15`, `30`, `60`, `90`. Outros valores são normalizados para `30` |
| `formato` | `str` (posicional) | Não | `tutorial` | Estrutura narrativa. Ver formatos disponíveis abaixo |
| `--formatos` | flag | Não | — | Lista todos os formatos disponíveis e encerra |

**Formatos disponíveis:**

| Chave | Nome | Descrição |
|-------|------|-----------|
| `tutorial` | Tutorial/How-To | Hook → Contexto → Passos → Resultado → CTA |
| `listicle` | Lista/Dicas | Hook → até 5 itens numerados → CTA |
| `storytime` | Storytelling | Hook → Setup → Conflito → Resolução → Lição/CTA |
| `antes_depois` | Antes e Depois | Hook → Antes → Transição → Depois → CTA |
| `pov` | POV (Point of View) | Setup POV → Cena → Reação/CTA |
| `trend` | Trend Adaptada | Sync → Conteúdo adaptado → Twist/CTA |
| `problema_solucao` | Problema → Solução | Hook → Problema → Virada → Solução → CTA |
| `react` | React/Dueto | Contexto → Reação → Opinião → CTA |

## Funções

### `gerar_roteiro(tema: str, duracao: int, formato: str) -> Dict`

Gera o roteiro completo para o Reels selecionando aleatoriamente um hook e um CTA, associando direções de câmera a cada parte da estrutura narrativa do formato escolhido.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `tema` | `str` | Tema do vídeo |
| `duracao` | `int` | Duração em segundos (15, 30, 60 ou 90) |
| `formato` | `str` | Chave do formato em `ESTRUTURAS`. Fallback para `"tutorial"` se inválido |

**Retorno:** `Dict` com chaves:

| Chave | Tipo | Descrição |
|-------|------|-----------|
| `tema` | `str` | Tema informado |
| `formato` | `str` | Nome do formato escolhido |
| `duracao` | `str` | Duração com sufixo `" segundos"` |
| `estrutura` | `List[Dict]` | Partes do roteiro com `tempo`, `tipo`, `descricao` e `direcao` |
| `hook_sugerido` | `str` | Hook gerado aleatoriamente |
| `cta_sugerido` | `str` | CTA gerado aleatoriamente |
| `direcoes_camera` | `List[str]` | Direções de câmera selecionadas para o roteiro |

---

### `formatar_saida(roteiro: Dict) -> str`

Formata o dicionário de roteiro como texto visual com bordas, seções destacadas (hook, estrutura, CTA) e dicas de gravação, pronto para exibição no terminal.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `roteiro` | `Dict` | Saída de `gerar_roteiro()` |

**Retorno:** `str` — Texto formatado para exibição no terminal.

---

### `listar_formatos() -> None`

Imprime no terminal a lista de todos os formatos disponíveis com seus respectivos nomes descritivos.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| — | — | Sem parâmetros |

**Retorno:** `None` (imprime no stdout)

## Constantes

| Constante | Tipo | Descrição |
|-----------|------|-----------|
| `ESTRUTURAS` | `Dict[str, Dict]` | 8 estruturas narrativas. Cada entrada contém `nome` (str) e `estrutura` (List[Dict] com `tempo`, `tipo` e `descricao` para cada parte). Chaves: `tutorial`, `listicle`, `storytime`, `antes_depois`, `pov`, `trend`, `problema_solucao`, `react` |
| `HOOKS` | `Dict[str, List[str]]` | 5 categorias com 5 templates de hook cada. Placeholders: `{tema}`, `{tempo}`, `{resultado}`, `{especialistas}`, etc. Categorias: `curiosidade`, `promessa`, `controversia`, `identificacao`, `resultado` |
| `CTAS` | `Dict[str, List[str]]` | 4 categorias com 5 templates de CTA cada. Placeholder: `{tema}`, `{palavra}`. Categorias: `engajamento`, `salvamento`, `seguidores`, `conversao` |
| `DIRECOES_CAMERA` | `List[str]` | 10 direções de câmera predefinidas (ex: `"Close no rosto"`, `"Insert/B-roll"`, `"Slow motion"`) |
| `USO` | `str` | String de ajuda exibida quando o script é chamado sem argumentos |
| `_DURACOES_VALIDAS` | `set[int]` | Conjunto de durações aceitas sem aviso: `{15, 30, 60, 90}` |
