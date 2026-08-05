# Guia de Contribuicao

Obrigado por considerar contribuir com o **Marketing OS**! Este documento fornece diretrizes para contribuicoes.

---

## Como Contribuir

### 1. Reportar Bugs

Se encontrar um bug:

1. Verifique se já não foi reportado nas [Issues](https://github.com/rilnermucio/esp-marketing-os/issues)
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
git clone https://github.com/rilnermucio/esp-marketing-os.git
cd esp-marketing-os

# (Opcional) Crie um ambiente virtual
python3.12 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Instale runtime e ferramentas de desenvolvimento
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pytest pytest-cov "black==26.5.1" flake8

# Valide o checkout
python -m pytest scripts/tests/ -m "not smoke"
python scripts/validate_agents.py --strict
python scripts/build_codex_plugin.py --check
python scripts/validate_codex_plugin.py plugins/marketing-os
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

**Por que:** o resolver de slash commands em print mode nao herda o namespace default; em sessao interativa (`claude` sem `-p`), o `/criar-X` resolve direto. Detalhes de validacao em `docs/archive/VALIDATION-RESULTS-v6.5.0.md`.

**Outras gotchas do `-p`:**

- `AskUserQuestion` nao recebe resposta. Se um agent precisar de contexto (avatar, ticket, urgencia, etc), pre-bake no proprio briefing.
- `--permission-mode bypassPermissions` evita prompts de permissao, util pra rodar batches.
- `--output-format stream-json --include-hook-events --verbose` captura events (incluindo dispatches `Agent`) pra parseamento posterior.

---

## Padroes de Codigo

### Python

- **Python 3.12**, mesma versão usada na CI
- Dependências de runtime declaradas em `requirements.txt`
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

- [ ] Aumentar cobertura dos scripts com menor cobertura medida
- [ ] Calibrar âncoras positivas para e-mail, anúncios, oferta, funil, SEO e vídeo
- [ ] Documentação de API dos scripts
- [ ] Type hints em todos os scripts

### Media Prioridade

- [ ] Novos templates de conteúdo
- [ ] Novos nichos e personas
- [ ] Melhorias nos scripts existentes
- [ ] Traducoes

### Baixa Prioridade

- [ ] Dashboard de métricas de qualidade e custo
- [ ] Melhorias de ergonomia no setup local

---

## Estrutura do Projeto

```
esp-marketing-os/
├── .claude-plugin/             # Manifestos Claude Code/Desktop
├── .codex-plugin/              # Manifesto-fonte do pacote Codex
├── agents/                     # Tier 1: prompts nativos mos-*
├── subagents/                  # Tier 2: knowledge bases profundas
├── commands/                   # Slash commands Claude
├── skills/marketing-os/        # Orquestrador e symlinks distribuíveis
├── scripts/                    # CLIs, validadores, hooks e testes
├── scripts/evals/              # Perfis versionados de avaliação de output
├── hooks/                      # Registro global de hooks Claude
├── plugins/marketing-os/       # Pacote Codex gerado
├── assets/                     # Templates, clones, personas e frameworks
├── workflows/                  # Workflows de campanha
└── docs/                       # Produto, operação e engenharia de IA
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
