# content_repurposer.py — Adaptador de conteúdo entre plataformas

O `content_repurposer.py` transforma um conteúdo original (artigo de blog, texto longo, roteiro) em seis formatos distintos para diferentes plataformas: carrossel do Instagram, roteiro de Reels, thread do Twitter/X, post do LinkedIn, newsletter por email e roteiro de YouTube. O script extrai automaticamente o título e os pontos-chave do texto de entrada e monta templates prontos para cada plataforma. Suporta entrada via arquivo (`--file`) ou texto direto na linha de comando.

## Uso via CLI

```bash
# Adaptar arquivo para todas as plataformas (visão geral)
python scripts/content_repurposer.py --file artigo.txt

# Adaptar para plataforma específica
python scripts/content_repurposer.py --file artigo.txt --platform instagram
python scripts/content_repurposer.py --file artigo.txt --platform twitter
python scripts/content_repurposer.py --file artigo.txt --platform linkedin
python scripts/content_repurposer.py --file artigo.txt --platform email
python scripts/content_repurposer.py --file artigo.txt --platform youtube

# Passar texto diretamente
python scripts/content_repurposer.py "Texto longo aqui..." --platform twitter

# Carrossel do Instagram
python scripts/content_repurposer.py --file artigo.md --platform carousel

# Reels do Instagram
python scripts/content_repurposer.py --file artigo.md --platform reels

# Compatibilidade retroativa com --output
python scripts/content_repurposer.py --file artigo.txt --output linkedin
```

## Argumentos

| Argumento | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `text` | `str...` (posicionais) | Condicional | — | Texto direto para adaptar. Obrigatório se `--file` não for informado |
| `--file`, `-f` | `str` | Condicional | `None` | Caminho para arquivo de texto. Obrigatório se `text` não for informado |
| `--platform`, `-p` | `str` | Não | `todos` | Plataforma de saída: `carousel`, `reels`, `twitter`, `linkedin`, `email`, `youtube`, `todos` |
| `--output` | `str` | Não | `None` | Alias legado de `--platform` (retrocompatibilidade, oculto no help) |

O texto de entrada deve ter no mínimo 100 caracteres.

## Funções

### `extract_key_points(text: str, max_points: int) -> List[str]`

Extrai pontos-chave do texto priorizando itens de listas numeradas ou com bullet points. Se não houver listas, seleciona sentenças com palavras de relevância semântica (ex: `"importante"`, `"essencial"`, `"dica"`) e as ordena por pontuação.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `text` | `str` | Texto completo de entrada |
| `max_points` | `int` | Número máximo de pontos a retornar (padrão: `7`) |

**Retorno:** `List[str]` — Lista de pontos-chave extraídos.

---

### `extract_title(text: str) -> str`

Tenta extrair o título do texto buscando, nas primeiras cinco linhas, uma linha iniciada com `#` ou uma linha curta (10–100 caracteres) sem ponto final. Se não encontrar, usa as primeiras dez palavras do texto.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `text` | `str` | Texto completo de entrada |

**Retorno:** `str` — Título extraído ou aproximação.

---

### `estimate_read_time(text: str) -> int`

Estima o tempo de leitura em minutos considerando uma velocidade de 200 palavras por minuto. Retorna no mínimo 1 minuto.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `text` | `str` | Texto completo de entrada |

**Retorno:** `int` — Tempo de leitura estimado em minutos.

---

### `to_instagram_carousel(text: str, num_slides: int) -> Dict`

Converte o texto em estrutura de carrossel para Instagram com slide de capa, slides de conteúdo (um ponto por slide), slide de resumo e slide de CTA, além de uma caption com hashtags sugeridas.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `text` | `str` | Texto original |
| `num_slides` | `int` | Número total de slides desejado (padrão: `10`) |

**Retorno:** `Dict` com `platform`, `slides` (List[Dict]), `total_slides`, `caption`, `hashtags_sugeridas`.

---

### `to_instagram_reels(text: str) -> Dict`

Converte o texto em roteiro simplificado para Reels (30–60s) com hook, setup, três pontos principais e CTA, além de uma caption.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `text` | `str` | Texto original |

**Retorno:** `Dict` com `platform`, `script`, `duracao_sugerida`, `formato`.

---

### `to_twitter_thread(text: str) -> Dict`

Converte o texto em thread para Twitter/X com tweet de hook, contexto, tweets de conteúdo (um ponto por tweet), resumo e CTA final.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `text` | `str` | Texto original |

**Retorno:** `Dict` com `platform`, `tweets` (List[Dict] com `number`, `content`, `chars`), `total_tweets`, `nota`.

---

### `to_linkedin_post(text: str) -> Dict`

Converte o texto em post profissional para LinkedIn com hook impactante, pontos em formato de lista com setas e CTA reflexivo.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `text` | `str` | Texto original |

**Retorno:** `Dict` com `platform`, `post`, `chars`, `max_chars` (3000), `dica`.

---

### `to_email_newsletter(text: str) -> Dict`

Converte o texto em template de newsletter por email com assunto, pré-header, saudação personalizada, pontos de aprendizado, seção de ações práticas e assinatura.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `text` | `str` | Texto original |

**Retorno:** `Dict` com `platform`, `email`, `subject_options` (List[str]), `tempo_leitura`.

---

### `to_youtube_script(text: str) -> Dict`

Converte o texto em roteiro estruturado para YouTube com hook (0:00–0:30), intro (0:30–2:00), seções de conteúdo com timestamps estimados, fechamento e notas de produção.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `text` | `str` | Texto original |

**Retorno:** `Dict` com `platform`, `script`, `duracao_estimada`, `estrutura`.

---

### `repurpose_all(text: str) -> Dict`

Executa todas as seis conversões e retorna o resultado consolidado em um único dicionário, incluindo também os metadados do conteúdo original (título, pontos-chave, tempo de leitura).

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `text` | `str` | Texto original |

**Retorno:** `Dict` com chaves `original`, `instagram_carousel`, `instagram_reels`, `twitter_thread`, `linkedin`, `email`, `youtube`.

---

### `print_output(result: Dict, platform: Optional[str]) -> None`

Imprime o resultado formatado no terminal. Quando `platform` é `None` ou `"todos"`, exibe um resumo de todas as versões geradas. Quando uma plataforma específica é informada, exibe o conteúdo completo daquela versão.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `result` | `Dict` | Saída de `repurpose_all()` |
| `platform` | `Optional[str]` | Plataforma específica ou `None`/`"todos"` para resumo |

**Retorno:** `None` (imprime no stdout)

## Constantes

Este script não define constantes de módulo próprias. As palavras de relevância semântica para extração de pontos-chave estão definidas inline em `extract_key_points()`:

| Variável interna | Tipo | Descrição |
|-----------------|------|-----------|
| `important_words` | `List[str]` | Palavras que aumentam o score de uma sentença: `"importante"`, `"principal"`, `"essencial"`, `"fundamental"`, `"primeiro"`, `"segundo"`, `"terceiro"`, `"dica"`, `"segredo"`, `"aprenda"`, `"descubra"`, `"como"`, `"por que"` |
