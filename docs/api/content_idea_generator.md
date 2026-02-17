# content_idea_generator.py — Gerador de ideias de conteúdo por pilares

O `content_idea_generator.py` gera ideias de conteúdo combinando pilares estratégicos, temas específicos do nicho, formatos editoriais e ângulos de abordagem de forma aleatória e variada. Para cada ideia gerada, o script atribui um pilar, tema principal, formato e prioridade, organizando os resultados por pilar. O output é exibido no terminal com um histograma de distribuição por formato e também exportado como JSON.

## Uso via CLI

```bash
# Gerar 20 ideias para tecnologia (padrão)
python scripts/content_idea_generator.py tecnologia

# Especificar quantidade
python scripts/content_idea_generator.py marketing_digital 30

# Nicho de finanças com 15 ideias
python scripts/content_idea_generator.py financas 15

# Empreendedorismo com 50 ideias
python scripts/content_idea_generator.py empreendedorismo 50

# Listar nichos disponíveis
python scripts/content_idea_generator.py --help
```

## Argumentos

| Argumento | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `nicho` | `str` (posicional) | Sim | — | Nicho de mercado (máx. 100 caracteres). Se não encontrado na base, usa `"tecnologia"` |
| `quantidade` | `int` (posicional) | Não | `20` | Número de ideias a gerar (1–100) |

**Nichos disponíveis:** `tecnologia`, `marketing_digital`, `empreendedorismo`, `desenvolvimento_pessoal`, `financas`

## Funções

### `generate_ideas(nicho: str, quantidade: int) -> Dict`

Gera ideias de conteúdo combinando aleatoriamente pilares, temas, formatos e ângulos do nicho informado. Para cada ideia, substitui as variáveis dos templates (tema, número, ano, etc.) e, em 50% dos casos, acrescenta um ângulo de abordagem.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `nicho` | `str` | Nicho de mercado (chave em `PILARES`). Fallback para `"tecnologia"` se não encontrado |
| `quantidade` | `int` | Número de ideias a gerar |

**Retorno:** `Dict` com chaves:

| Chave | Tipo | Descrição |
|-------|------|-----------|
| `nicho` | `str` | Nicho utilizado |
| `pilares` | `List[str]` | Lista de pilares do nicho |
| `total_ideias` | `int` | Total de ideias geradas |
| `ideias` | `List[Dict]` | Lista completa de ideias (ver estrutura abaixo) |
| `ideias_por_pilar` | `Dict[str, List[Dict]]` | Ideias agrupadas por pilar |
| `formatos_usados` | `List[str]` | Lista de tipos de formato utilizados |

**Estrutura de cada item em `ideias`:**

| Chave | Tipo | Descrição |
|-------|------|-----------|
| `idea` | `str` | Texto da ideia gerada |
| `pilar` | `str` | Pilar estratégico associado |
| `tema_principal` | `str` | Tema específico do nicho |
| `formato` | `str` | Tipo de formato editorial |
| `prioridade` | `str` | `"alta"`, `"média"` ou `"baixa"` (aleatório) |

---

### `print_results(results: Dict) -> None`

Imprime os resultados no terminal com as ideias organizadas por pilar, indicadores de prioridade coloridos (emojis), distribuição por formato em histograma de blocos e próximos passos sugeridos.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `results` | `Dict` | Saída de `generate_ideas()` |

**Retorno:** `None` (imprime no stdout)

---

### `_uso_ideias() -> str`

Gera e retorna a string de ajuda com sintaxe de uso e lista de nichos disponíveis.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| — | — | Sem parâmetros |

**Retorno:** `str` — Texto de ajuda formatado.

## Constantes

| Constante | Tipo | Descrição |
|-----------|------|-----------|
| `PILARES` | `Dict[str, Dict]` | Base de dados por nicho. Cada nicho contém `pilares` (List[str]: 5 pilares estratégicos), `temas` (List[str]: 10 temas específicos) e `problemas` (List[str]: 5 dores da audiência). Nichos: `tecnologia`, `marketing_digital`, `empreendedorismo`, `desenvolvimento_pessoal`, `financas` |
| `FORMATOS` | `Dict[str, List[str]]` | 7 tipos de formato com templates de título. Templates usam placeholders: `{tema}`, `{tema2}`, `{numero}`, `{ano}`, `{ano2}`, `{resultado}`, `{antes}`, `{depois}`, `{tempo}`, `{problema}`. Tipos: `educativo`, `lista`, `comparativo`, `case`, `problema_solucao`, `opiniao`, `trending` |
| `ANGULOS` | `List[str]` | 10 ângulos/gatilhos de abordagem aplicados a 50% das ideias (ex: `"para iniciantes"`, `"sem gastar nada"`, `"na prática"`) |
