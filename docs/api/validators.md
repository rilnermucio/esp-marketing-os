# validators.py — Módulo de Validação Centralizado

Módulo de validação de entrada reutilizável para todos os scripts do Marketing OS.
Fornece funções com mensagens de erro padronizadas em português e integração com o sistema de CLI.

## Importação

```python
from validators import (
    ValidationError,
    validar_texto,
    validar_inteiro,
    validar_float,
    validar_arquivo,
    validar_diretorio_saida,
    validar_plataforma,
    validar_lista_plataformas,
    validar_formato,
    validar_data,
    validar_semana_iso,
    validar_url,
    handle_validation_error,
)
```

## Exceções

### `ValidationError`

Subclasse de `ValueError`. Levantada por todas as funções de validação quando a entrada é inválida.

```python
try:
    validar_inteiro("abc", campo="quantidade")
except ValidationError as e:
    print(e)  # 'quantidade' deve ser um número inteiro. Recebeu: 'abc'
```

## Constantes

### `PLATAFORMAS_VALIDAS: set[str]`
Plataformas suportadas pelo Marketing OS:
`instagram`, `tiktok`, `youtube`, `shorts`, `linkedin`, `twitter`, `x`, `facebook`, `pinterest`, `reels`

### `FORMATOS_VALIDOS: set[str]`
Formatos de conteúdo válidos:
`reels`, `carrossel`, `post`, `stories`, `tutorial`, `shorts`, `video`, `artigo`, `newsletter`, `thread`

### `MAX_FILE_SIZE: int`
Tamanho máximo de arquivo: `10 MB` (10 × 1024 × 1024 bytes)

---

## Funções

### `validar_texto(valor, campo, min_len, max_len) -> str`

Valida uma string de texto.

**Parâmetros:**
| Nome | Tipo | Padrão | Descrição |
|------|------|--------|-----------|
| `valor` | `str` | — | Valor a validar |
| `campo` | `str` | `"texto"` | Nome do campo (para mensagens de erro) |
| `min_len` | `int` | `1` | Comprimento mínimo |
| `max_len` | `int` | `500` | Comprimento máximo |

**Retorna:** String validada, sem espaços extras nas bordas.

**Levanta:** `ValidationError` se vazio, abaixo do mínimo, acima do máximo, ou não for string.

```python
tema = validar_texto(sys.argv[1], campo="tema", max_len=200)
```

---

### `validar_inteiro(valor, campo, min_val, max_val) -> int`

Valida e converte um valor para inteiro dentro de um intervalo.

**Parâmetros:**
| Nome | Tipo | Padrão | Descrição |
|------|------|--------|-----------|
| `valor` | `str \| int` | — | Valor a validar |
| `campo` | `str` | `"número"` | Nome do campo |
| `min_val` | `int` | `1` | Valor mínimo (inclusive) |
| `max_val` | `int` | `1000` | Valor máximo (inclusive) |

**Retorna:** Inteiro validado.

```python
quantidade = validar_inteiro(sys.argv[2], campo="quantidade", min_val=1, max_val=50)
```

---

### `validar_float(valor, campo, min_val, max_val) -> float`

Valida e converte um valor para float dentro de um intervalo.

**Parâmetros:**
| Nome | Tipo | Padrão | Descrição |
|------|------|--------|-----------|
| `valor` | `str \| float` | — | Valor a validar |
| `campo` | `str` | `"número"` | Nome do campo |
| `min_val` | `float` | `0.0` | Valor mínimo (inclusive) |
| `max_val` | `float` | `100.0` | Valor máximo (inclusive) |

```python
budget = validar_float(args.budget, campo="budget_diario", min_val=100.0, max_val=10_000_000.0)
```

---

### `validar_arquivo(caminho, extensoes, campo) -> str`

Valida que um arquivo existe, é legível, não está vazio, e tem extensão permitida.

**Parâmetros:**
| Nome | Tipo | Padrão | Descrição |
|------|------|--------|-----------|
| `caminho` | `str` | — | Caminho do arquivo |
| `extensoes` | `list[str] \| None` | `None` | Extensões permitidas (ex: `[".md", ".txt"]`) |
| `campo` | `str` | `"arquivo"` | Nome do campo |

**Retorna:** Caminho absoluto validado.

**Levanta:** `ValidationError` se o arquivo não existir, não for legível, estiver vazio, exceder 10 MB, ou tiver extensão inválida.

```python
filepath = validar_arquivo(sys.argv[1], extensoes=[".md", ".txt"], campo="arquivo")
```

---

### `validar_diretorio_saida(caminho, campo) -> str`

Valida um diretório de saída, criando-o se não existir.

**Parâmetros:**
| Nome | Tipo | Padrão | Descrição |
|------|------|--------|-----------|
| `caminho` | `str` | — | Caminho do diretório |
| `campo` | `str` | `"diretório de saída"` | Nome do campo |

**Retorna:** Caminho absoluto do diretório.

---

### `validar_plataforma(plataforma, campo) -> str`

Valida que a plataforma é suportada pelo Marketing OS.

**Retorna:** Plataforma em minúsculas validada.

```python
plataforma = validar_plataforma(sys.argv[2], campo="plataforma")
# "Instagram" → "instagram"
```

---

### `validar_lista_plataformas(plataformas, campo) -> list[str]`

Valida uma lista de plataformas, removendo duplicatas.

```python
platforms = validar_lista_plataformas(sys.argv[3:], campo="plataformas")
```

---

### `validar_formato(formato, campo) -> str`

Valida um formato de conteúdo (reels, carrossel, post, etc.).

```python
formato = validar_formato(sys.argv[3], campo="formato")
# "REELS" → "reels"
```

---

### `validar_data(data_str, campo, formato) -> datetime`

Valida e converte uma string de data para `datetime`.

**Parâmetros:**
| Nome | Tipo | Padrão | Descrição |
|------|------|--------|-----------|
| `data_str` | `str` | — | String de data |
| `campo` | `str` | `"data"` | Nome do campo |
| `formato` | `str` | `"%Y-%m-%d"` | Formato esperado |

```python
data = validar_data("2026-02-17")
data_br = validar_data("17/02/2026", formato="%d/%m/%Y")
```

---

### `validar_semana_iso(semana_str, campo) -> str`

Valida o formato de semana ISO (`YYYY-Www`). Aceita semanas W01–W53.

```python
semana = validar_semana_iso("2026-W07")  # → "2026-W07"
```

---

### `validar_url(url, campo) -> str`

Valida o formato básico de uma URL (http/https).

```python
url = validar_url(args.image_url, campo="image_url")
```

---

### `handle_validation_error(error, mostrar_uso) -> None`

Imprime mensagem de erro formatada e encerra o processo com código 1.

**Parâmetros:**
| Nome | Tipo | Padrão | Descrição |
|------|------|--------|-----------|
| `error` | `ValidationError` | — | Erro de validação |
| `mostrar_uso` | `str \| None` | `None` | String de uso a exibir |

```python
try:
    tema = validar_texto(sys.argv[1], campo="tema")
except ValidationError as e:
    handle_validation_error(e, mostrar_uso="Uso: script.py <tema>")
```

---

## Padrão de Uso em Scripts CLI

```python
from validators import ValidationError, validar_texto, validar_inteiro, handle_validation_error

USO = 'Uso: python meu_script.py "tema" [quantidade]'

def main() -> None:
    if len(sys.argv) < 2:
        print(USO)
        sys.exit(1)

    try:
        tema = validar_texto(sys.argv[1], campo="tema", max_len=200)
        quantidade = validar_inteiro(sys.argv[2], campo="quantidade", min_val=1, max_val=50) if len(sys.argv) > 2 else 10
    except ValidationError as e:
        handle_validation_error(e, mostrar_uso=USO)
        return

    # ... lógica principal ...
```
