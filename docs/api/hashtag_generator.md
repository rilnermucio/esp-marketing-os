# hashtag_generator.py — Gerador de hashtags por nicho e plataforma

O `hashtag_generator.py` gera conjuntos de hashtags relevantes para um nicho de mercado e os adapta às regras e limites de cada plataforma de redes sociais. O script organiza as hashtags em três categorias (core, engagement, trending) e suporta adição de keywords customizadas. O resultado é exibido no terminal com dicas de boas práticas e exportado como JSON.

## Uso via CLI

```bash
# Hashtags básicas para marketing digital no Instagram
python scripts/hashtag_generator.py marketing_digital

# Especificar plataforma
python scripts/hashtag_generator.py empreendedorismo linkedin

# Adicionar keywords customizadas
python scripts/hashtag_generator.py marketing_digital instagram ia chatgpt growth

# TikTok com keywords extras
python scripts/hashtag_generator.py tecnologia tiktok automacao nocode

# Listar nichos disponíveis
python scripts/hashtag_generator.py --help
```

## Argumentos

| Argumento | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `nicho` | `str` (posicional) | Sim | — | Nicho de mercado (máx. 100 caracteres). Ver nichos disponíveis abaixo |
| `plataforma` | `str` (posicional) | Não | `instagram` | Plataforma de destino: `instagram`, `linkedin`, `twitter`, `tiktok`, `facebook` |
| `keywords...` | `str...` (posicionais) | Não | `None` | Keywords customizadas adicionais (máx. 50 chars cada, até 5 aproveitadas) |

**Nichos disponíveis:** `marketing_digital`, `empreendedorismo`, `tecnologia`, `saude_bem_estar`, `financas`, `moda_beleza`, `gastronomia`, `educacao`

## Funções

### `get_hashtags(nicho, platform, custom_keywords) -> Dict`

Gera as hashtags para o nicho e plataforma informados, combinando os grupos core, engagement e trending da base de dados, aplicando o limite recomendado da plataforma e incorporando keywords customizadas.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `nicho` | `str` | Nicho de mercado (normalizado para minúsculas e underscores) |
| `platform` | `str` | Plataforma de destino (padrão: `"instagram"`) |
| `custom_keywords` | `Optional[List[str]]` | Lista de keywords customizadas a formatar e incluir |

**Retorno em caso de sucesso:** `Dict` com chaves:

| Chave | Tipo | Descrição |
|-------|------|-----------|
| `nicho` | `str` | Nicho informado |
| `platform` | `str` | Plataforma informada |
| `recommended` | `Dict` | Hashtags no limite recomendado da plataforma: `hashtags`, `count`, `formatted` |
| `extended` | `Dict` | Hashtags até o máximo absoluto da plataforma: `hashtags`, `count`, `formatted` |
| `all_available` | `Dict` | Todas as hashtags disponíveis agrupadas: `core`, `engagement`, `trending` |
| `platform_tips` | `str` | Dica específica para a plataforma |
| `best_practices` | `List[str]` | 5 boas práticas gerais de uso de hashtags |

**Retorno em caso de nicho não encontrado:** `Dict` com `error`, `available_niches` e `suggestion`.

---

### `_uso_hashtag() -> str`

Gera e retorna a string de ajuda com sintaxe de uso e lista de nichos e plataformas disponíveis.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| — | — | Sem parâmetros |

**Retorno:** `str` — Texto de ajuda formatado.

## Constantes

| Constante | Tipo | Descrição |
|-----------|------|-----------|
| `HASHTAG_DATABASE` | `Dict[str, Dict]` | Base de hashtags com 8 nichos. Cada nicho contém três listas: `core` (5 hashtags fundamentais), `engagement` (4–5 hashtags de engajamento) e `trending` (4–5 hashtags em alta). Nichos: `marketing_digital`, `empreendedorismo`, `tecnologia`, `saude_bem_estar`, `financas`, `moda_beleza`, `gastronomia`, `educacao` |
| `PLATFORM_LIMITS` | `Dict[str, Dict]` | Limites por plataforma com `max` (absoluto), `recommended` (ideal) e `note` (dica). Plataformas: `instagram` (max 30, rec 10), `linkedin` (max 5, rec 3), `twitter` (max 2, rec 2), `tiktok` (max 5, rec 4), `facebook` (max 3, rec 2) |
