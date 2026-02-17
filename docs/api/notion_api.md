# notion_api.py — Notion API

Integração com a Notion API v1 para publicação e gestão de conteúdo. Autentica via Integration Token (Internal Integration).

## Autenticação

```bash
# Token da integração (obrigatório)
export NOTION_TOKEN=secret_xxxxxxxxxxxxxxxx

# ID do banco de dados padrão (opcional)
export NOTION_DATABASE_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

## Uso via CLI

```bash
# Listar bancos de dados acessíveis
python notion_api.py list-databases

# Listar páginas de um banco de dados
python notion_api.py list-pages --database-id DB_ID [--limit 10]

# Detalhes de uma página
python notion_api.py get-page PAGE_ID

# Criar nova página
python notion_api.py create-page --database-id DB_ID --title "Título" [--content "Texto inicial"]

# Adicionar bloco de texto a uma página
python notion_api.py append-block PAGE_ID --text "Texto" [--type paragraph]

# Pesquisar páginas e bancos de dados
python notion_api.py search --query "termo" [--type page|database] [--limit 10]

# Schema de um banco de dados
python notion_api.py schema --database-id DB_ID

# Relatório completo
python notion_api.py full-report [--database-id DB_ID]

# Output JSON (machine-readable)
python notion_api.py list-databases --json
```

### Subcomandos

| Subcomando | Descrição |
|------------|-----------|
| `list-databases` | Lista todos os bancos de dados acessíveis pela integração |
| `list-pages` | Lista páginas de um banco de dados |
| `get-page` | Retorna detalhes de uma página |
| `create-page` | Cria nova página em um banco de dados |
| `append-block` | Adiciona bloco de texto a uma página existente |
| `search` | Pesquisa páginas e bancos de dados pelo título |
| `schema` | Retorna o schema (propriedades) de um banco de dados |
| `full-report` | Relatório completo: databases + páginas recentes |

### Argumentos comuns

| Argumento | Curto | Padrão | Descrição |
|-----------|-------|--------|-----------|
| `--database-id` | `-d` | — | ID do banco de dados |
| `--limit` | `-l` | `10` | Máximo de itens retornados |
| `--title` | `-t` | — | Título da página (create-page) |
| `--content` | `-c` | — | Conteúdo inicial do bloco (create-page) |
| `--text` | `-t` | — | Texto do bloco (append-block) |
| `--type` | — | `paragraph` | Tipo do bloco (append-block) ou filtro (search) |
| `--query` | `-q` | — | Termo de pesquisa (search) |
| `--json` | — | `False` | Saída em JSON puro |

## Exceções

### `NotionAPIError`

Erro base da integração com a Notion API.

| Atributo | Tipo | Descrição |
|----------|------|-----------|
| `message` | `str` | Mensagem de erro |
| `status` | `Optional[int]` | Código HTTP (quando disponível) |
| `code` | `Optional[str]` | Código de erro da Notion API (ex: `object_not_found`) |

`str()` formata como `[HTTP 404] Objeto não encontrado (código: object_not_found)`.

### `NotionAuthError`

Subclasse de `NotionAPIError`. Levantada quando o token não está configurado ou é inválido.

## Funções

### `list_databases(token, limit) -> List[Dict]`

Lista os bancos de dados acessíveis pela integração.

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `token` | `str` | — | Integration token |
| `limit` | `int` | `20` | Máximo de bancos de dados (1–100) |

**Retorno:** `List[Dict]`, cada item com:

| Chave | Tipo | Descrição |
|-------|------|-----------|
| `id` | `str` | ID do banco de dados |
| `titulo` | `str` | Título do banco de dados |
| `url` | `str` | URL no Notion |
| `criado_em` | `str` | Data de criação (`YYYY-MM-DD`) |
| `editado_em` | `str` | Última edição (`YYYY-MM-DD`) |

---

### `list_pages(token, database_id, limit, filter_payload) -> List[Dict]`

Lista páginas de um banco de dados Notion.

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `token` | `str` | — | Integration token |
| `database_id` | `str` | — | ID do banco de dados |
| `limit` | `int` | `10` | Máximo de páginas (1–100) |
| `filter_payload` | `Optional[Dict]` | `None` | Filtro no formato da Notion API |

**Retorno:** `List[Dict]`, cada item com:

| Chave | Tipo | Descrição |
|-------|------|-----------|
| `id` | `str` | ID da página |
| `titulo` | `str` | Título da página |
| `tipo` | `str` | Tipo do objeto (`page`) |
| `criado_em` | `str` | Data de criação (`YYYY-MM-DD`) |
| `editado_em` | `str` | Última edição (`YYYY-MM-DD`) |
| `url` | `str` | URL no Notion |
| `parent_tipo` | `str` | Tipo do pai (`database_id`, `page_id`, etc.) |
| `parent_id` | `str` | ID do objeto pai |

---

### `get_page(token, page_id) -> Dict`

Retorna os detalhes de uma página Notion.

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `token` | `str` | — | Integration token |
| `page_id` | `str` | — | ID da página |

**Retorno:** `Dict` com os campos de `list_pages` mais:

| Chave | Tipo | Descrição |
|-------|------|-----------|
| `propriedades` | `Dict[str, str]` | Mapa `{nome_propriedade: tipo}` |

---

### `create_page(token, database_id, title, content, properties) -> Dict`

Cria uma nova página em um banco de dados Notion.

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `token` | `str` | — | Integration token |
| `database_id` | `str` | — | ID do banco de dados pai |
| `title` | `str` | — | Título da página |
| `content` | `Optional[str]` | `None` | Texto para o primeiro parágrafo |
| `properties` | `Optional[Dict]` | `None` | Propriedades adicionais (formato Notion API) |

**Retorno:** `Dict` com:

| Chave | Tipo | Descrição |
|-------|------|-----------|
| `id` | `str` | ID da página criada |
| `titulo` | `str` | Título da página |
| `url` | `str` | URL no Notion |
| `criado_em` | `str` | Data de criação (`YYYY-MM-DD`) |

---

### `append_block(token, page_id, text, block_type) -> Dict`

Adiciona um bloco de texto a uma página Notion existente.

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `token` | `str` | — | Integration token |
| `page_id` | `str` | — | ID da página de destino |
| `text` | `str` | — | Texto a adicionar |
| `block_type` | `str` | `"paragraph"` | Tipo do bloco (ver `TIPOS_BLOCO`) |

**Retorno:** `Dict` com:

| Chave | Tipo | Descrição |
|-------|------|-----------|
| `page_id` | `str` | ID da página modificada |
| `blocos_criados` | `List[str]` | IDs dos blocos adicionados |
| `total` | `int` | Quantidade de blocos criados |

---

### `search(token, query, search_type, limit) -> List[Dict]`

Pesquisa páginas e bancos de dados acessíveis pela integração.

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `token` | `str` | — | Integration token |
| `query` | `str` | — | Termo de pesquisa |
| `search_type` | `Optional[str]` | `None` | Filtrar por `"page"` ou `"database"` |
| `limit` | `int` | `10` | Máximo de resultados (1–100) |

**Retorno:** `List[Dict]` no mesmo formato de `list_pages`.

---

### `get_database_schema(token, database_id) -> Dict`

Retorna o schema (propriedades) de um banco de dados.

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `token` | `str` | — | Integration token |
| `database_id` | `str` | — | ID do banco de dados |

**Retorno:** `Dict` com:

| Chave | Tipo | Descrição |
|-------|------|-----------|
| `id` | `str` | ID do banco de dados |
| `titulo` | `str` | Título do banco de dados |
| `propriedades` | `Dict[str, str]` | Mapa `{nome: tipo}` de todas as propriedades |
| `total_propriedades` | `int` | Quantidade de propriedades |

---

### `full_report(token, database_id) -> Dict`

Gera relatório completo: lista bancos de dados e opcionalmente detalha um banco.

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `token` | `str` | — | Integration token |
| `database_id` | `Optional[str]` | `None` | ID do banco de dados para detalhar |

**Retorno:** `Dict` com:

| Chave | Tipo | Descrição |
|-------|------|-----------|
| `gerado_em` | `str` | Timestamp de geração (`YYYY-MM-DD HH:MM`) |
| `total_databases` | `int` | Quantidade de bancos de dados encontrados |
| `databases` | `List[Dict]` | Lista de bancos de dados |
| `database_detalhado` | `Dict` | Schema do banco detalhado (quando `database_id` fornecido) |
| `paginas_recentes` | `List[Dict]` | Páginas recentes do banco detalhado |
| `total_paginas` | `int` | Quantidade de páginas retornadas |
| `erro_database` | `str` | Mensagem de erro (quando o banco não é acessível) |

---

## Funções internas

| Função | Descrição |
|--------|-----------|
| `_get_token() -> str` | Carrega token de `NOTION_TOKEN` ou levanta `NotionAuthError` |
| `_headers(token) -> Dict` | Gera cabeçalhos HTTP com `Authorization`, `Notion-Version` e `Content-Type` |
| `_api_get(path, token, params) -> Dict` | GET autenticado com tratamento de erros HTTP |
| `_api_post(path, token, payload) -> Dict` | POST autenticado com tratamento de erros HTTP |
| `_api_patch(path, token, payload) -> Dict` | PATCH autenticado com tratamento de erros HTTP |
| `_extract_title(page) -> str` | Extrai título de página ou banco de dados |
| `_extract_page_summary(page) -> Dict` | Extrai campos essenciais de uma página |
| `_make_rich_text(text) -> List` | Cria objeto `rich_text` para a Notion API |
| `_make_paragraph_block(text) -> Dict` | Cria bloco do tipo `paragraph` |
| `_make_heading_block(text, level) -> Dict` | Cria bloco `heading_1/2/3` |

## Constantes

| Constante | Tipo | Valor / Descrição |
|-----------|------|-------------------|
| `NOTION_API_BASE` | `str` | `"https://api.notion.com/v1"` |
| `NOTION_API_VERSION` | `str` | `"2022-06-28"` (versão do header `Notion-Version`) |
| `ENV_TOKEN` | `str` | `"NOTION_TOKEN"` |
| `ENV_DATABASE_ID` | `str` | `"NOTION_DATABASE_ID"` |
| `TIPOS_BLOCO` | `Set[str]` | 11 tipos de bloco suportados (paragraph, heading_1–3, etc.) |
| `PROPRIEDADES_MARKETING` | `List[str]` | Propriedades comuns para bancos de conteúdo de marketing |

## Tipos de bloco suportados (`TIPOS_BLOCO`)

`paragraph`, `heading_1`, `heading_2`, `heading_3`, `bulleted_list_item`, `numbered_list_item`, `to_do`, `toggle`, `quote`, `callout`, `divider`, `code`

## Dependências

- **Stdlib apenas** — usa `urllib`, `json`, `os`, `sys`, `argparse`, `datetime`
- **`output_formatter`** — módulo interno para formatação de saída
- **`validators`** — módulo interno para validação de argumentos CLI
