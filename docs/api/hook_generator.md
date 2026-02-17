# hook_generator.py — Gerador de hooks virais para vídeos e posts

O `hook_generator.py` gera hooks virais para conteúdo de vídeo e posts em redes sociais, baseando-se em oito categorias comprovadas de padrões de engajamento (curiosidade, controvérsia, número, história, urgência, identificação, promessa e prova social). O script adapta os hooks ao estilo e limite de caracteres de cada plataforma e imprime o resultado formatado no terminal além de um bloco JSON para integração.

## Uso via CLI

```bash
# Gerar 10 hooks para "produtividade" no Instagram Reels (padrão)
python scripts/hook_generator.py "produtividade"

# Especificar plataforma
python scripts/hook_generator.py "marketing digital" tiktok

# Especificar quantidade
python scripts/hook_generator.py "produtividade com IA" reels 10

# LinkedIn com 5 hooks
python scripts/hook_generator.py "liderança" linkedin 5

# YouTube com 15 hooks
python scripts/hook_generator.py "finanças pessoais" youtube 15
```

## Argumentos

| Argumento | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `tema` | `str` (posicional) | Sim | — | Tema central dos hooks (máx. 200 caracteres) |
| `plataforma` | `str` (posicional) | Não | `reels` | Plataforma de destino: `reels`, `tiktok`, `youtube`, `shorts`, `linkedin`, `twitter` |
| `quantidade` | `int` (posicional) | Não | `10` | Número de hooks a gerar (1–50) |

## Funções

### `generate_hooks(tema: str, plataforma: str, quantidade: int) -> Dict`

Gera hooks virais para o tema especificado, percorrendo as categorias de `HOOK_TEMPLATES` de forma embaralhada e aplicando o estilo (posição do emoji, limite de caracteres) da plataforma selecionada.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `tema` | `str` | Tema central a ser inserido nos templates |
| `plataforma` | `str` | Plataforma de destino (chave em `PLATFORM_SPECS`) |
| `quantidade` | `int` | Número de hooks a gerar |

**Retorno:** `Dict` com chaves:

| Chave | Tipo | Descrição |
|-------|------|-----------|
| `tema` | `str` | Tema informado |
| `plataforma` | `str` | Plataforma informada |
| `specs` | `Dict` | Especificações da plataforma (max_chars, style, emoji_position, tip) |
| `hooks` | `List[Dict]` | Lista de hooks com `hook`, `categoria`, `emoji`, `chars` |
| `categorias_usadas` | `List[str]` | Categorias únicas utilizadas |
| `total_gerado` | `int` | Total de hooks gerados |

---

### `print_results(results: Dict) -> None`

Imprime os resultados do gerador no terminal com formatação visual, exibindo cada hook com contagem de caracteres, aviso de limite da plataforma, categorias utilizadas e dicas de uso.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `results` | `Dict` | Saída de `generate_hooks()` |

**Retorno:** `None` (imprime no stdout)

## Constantes

| Constante | Tipo | Descrição |
|-----------|------|-----------|
| `HOOK_TEMPLATES` | `Dict[str, List[str]]` | 8 categorias com 8 templates de hook cada. Placeholder `{tema}` é substituído pelo tema informado. Categorias: `curiosidade`, `controversia`, `numero`, `historia`, `urgencia`, `identificacao`, `promessa`, `prova_social` |
| `EMOJIS` | `Dict[str, List[str]]` | 5 emojis por categoria, selecionados aleatoriamente para cada hook |
| `PLATFORM_SPECS` | `Dict[str, Dict]` | Especificações por plataforma: `max_chars` (int), `style` (str), `emoji_position` (`"início"`, `"fim"` ou `"opcional"`), `tip` (str). Plataformas: `reels`, `tiktok`, `youtube`, `shorts`, `linkedin`, `twitter` |
| `USO` | `str` | String de ajuda exibida quando o script é chamado sem argumentos |
