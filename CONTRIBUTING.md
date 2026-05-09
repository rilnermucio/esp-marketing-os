# Guia de Contribuicao

Obrigado por considerar contribuir com o **Marketing OS**! Este documento fornece diretrizes para contribuicoes.

---

## Como Contribuir

### 1. Reportar Bugs

Se encontrar um bug:

1. Verifique se já não foi reportado nas [Issues](https://github.com/rilnermucio/Agents/issues)
2. Se não, crie uma nova issue com:
   - Descricao clara do problema
   - Passos para reproduzir
   - Comportamento esperado vs atual
   - Screenshots (se aplicavel)
   - Ambiente (OS, Python version, etc.)

### 2. Sugerir Funcionalidades

Para sugerir novas funcionalidades:

1. Abra uma issue com a tag `enhancement`
2. Descreva:
   - O problema que a funcionalidade resolve
   - Como você imagina a solucao
   - Exemplos de uso

### 3. Contribuir com Codigo

#### Setup do Ambiente

```bash
# Clone o repositorio
git clone https://github.com/rilnermucio/Agents.git
cd "Marketing OS"

# (Opcional) Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Os scripts usam apenas biblioteca padrao do Python 3.8+
# Nenhuma dependencia externa necessaria
```

#### Workflow de Desenvolvimento

1. **Fork** o repositorio
2. **Crie uma branch** para sua feature:
   ```bash
   git checkout -b feature/nome-da-feature
   ```
3. **Faca suas mudancas** seguindo os padroes do projeto
4. **Teste** suas mudancas
5. **Commit** com mensagens descritivas:
   ```bash
   git commit -m "feat: adiciona novo template de webinar"
   ```
6. **Push** para sua branch:
   ```bash
   git push origin feature/nome-da-feature
   ```
7. **Abra um Pull Request**

#### Testando dispatches via `claude -p` (modo nao-interativo)

Util pra rodar a VALIDATION-GUIDE.md ou validar workflows novos sem abrir sessao interativa.

**Quirk importante:** comandos slash em `claude -p` exigem namespace explicito do plugin:

```bash
# NAO funciona em -p (mas funciona em sessao interativa)
claude -p "/criar-anuncio Meta Ads pra curso de Copy"
# -> Unknown command: /criar-anuncio

# Funciona em -p
claude -p "/marketing-os:criar-anuncio Meta Ads pra curso de Copy"

# A skill /marketing-os (sem comando) funciona sem namespace
claude -p "/marketing-os escreve 5 headlines pra curso de Python"
```

**Por que:** o resolver de slash commands em print mode nao herda o namespace default; em sessao interativa (`claude` sem `-p`), o `/criar-X` resolve direto. Detalhes de validacao em `docs/VALIDATION-RESULTS-v6.5.0.md`.

**Outras gotchas do `-p`:**

- `AskUserQuestion` nao recebe resposta. Se um agent precisar de contexto (avatar, ticket, urgencia, etc), pre-bake no proprio briefing.
- `--permission-mode bypassPermissions` evita prompts de permissao, util pra rodar batches.
- `--output-format stream-json --include-hook-events --verbose` captura events (incluindo dispatches `Agent`) pra parseamento posterior.

---

## Padroes de Codigo

### Python

- **Python 3.8+** compativel
- Apenas **biblioteca padrao** (sem dependencias externas)
- Docstrings em todas as funcoes publicas
- Type hints quando possivel
- Nomes de variaveis em ingles ou portugues (consistente no arquivo)

```python
def analyze_content(content: str, keyword: str = None) -> dict:
    """
    Analisa conteúdo para SEO.

    Args:
        content: Texto a ser analisado
        keyword: Keyword principal (opcional)

    Returns:
        dict: Metricas de analise
    """
    pass
```

### Markdown

- Usar acentuacao quando possivel em documentacao
- Headers com hierarquia correta (H1 > H2 > H3)
- Tabelas formatadas consistentemente
- Links relativos para arquivos internos

### Commits

Seguir [Conventional Commits](https://www.conventionalcommits.org/):

| Tipo | Descricao |
|------|-----------|
| `feat:` | Nova funcionalidade |
| `fix:` | Correcao de bug |
| `docs:` | Documentacao |
| `style:` | Formatacao (sem mudanca de codigo) |
| `refactor:` | Refatoracao |
| `test:` | Testes |
| `chore:` | Manutencao |

Exemplos:
```
feat: adiciona template de YouTube Shorts
fix: corrige calculo de densidade de keyword no seo_analyzer
docs: atualiza README com novos scripts
```

---

## Areas para Contribuicao

### Alta Prioridade

- [ ] Testes unitarios para scripts Python
- [ ] Documentacao de API dos scripts
- [ ] Type hints em todos os scripts

### Media Prioridade

- [ ] Novos templates de conteúdo
- [ ] Novos nichos e personas
- [ ] Melhorias nos scripts existentes
- [ ] Traducoes

### Baixa Prioridade

- [ ] GitHub Actions para CI
- [ ] Scripts de automacao de instalacao
- [ ] Dashboard de metricas

---

## Estrutura do Projeto

```
Marketing OS/
|
+-- Skill.md                    # Arquivo principal da skill
+-- README.md                   # Documentacao
+-- CHANGELOG.md                # Historico de versoes
+-- CONTRIBUTING.md             # Este arquivo
|
+-- subagents/                  # 11 subagentes especializados
+-- scripts/                    # 19 scripts Python
+-- assets/
|   +-- templates/              # 26 templates de conteúdo
|   +-- swipe-files/            # Exemplos e referencias
|   +-- personas/               # Personas por nicho
|   +-- prompts/                # Prompts para IA
|   +-- frameworks/             # Frameworks de crescimento
|
+-- references/                 # Guias de referencia
+-- workflows/                  # 7 workflows de campanha
+-- docs/
    +-- stories/                # Stories de desenvolvimento
        +-- active/             # Em andamento
        +-- backlog/            # Pendentes
        +-- completed/          # Concluidas
```

---

## Code Review

Todos os PRs passam por review. Checklist:

- [ ] Codigo segue os padroes do projeto
- [ ] Documentacao atualizada (se aplicavel)
- [ ] Sem quebra de funcionalidade existente
- [ ] Commits com mensagens claras

---

## Duvidas?

- Abra uma issue com a tag `question`
- Ou entre em contato com [@rilnermucio](https://github.com/rilnermucio)

---

Obrigado por contribuir!
