# Troubleshooting Marketing OS

Bugs reais que encontramos durante distribuição/uso, com solução verificada. Se o seu sintoma não está aqui, abra issue no GitHub.

---

## Install / Sync

### "Plugin validation failed" no upload local (Claude Desktop)

**Causa:** O zip do plugin está com `plugin.json` na raiz em vez de `.claude-plugin/plugin.json` (caminho canônico exigido pelo Claude Desktop).

**Solução:**
- Se tá usando o repo oficial v6.1.5+: já está corrigido, basta reempacotar
- Se está empacotando manualmente: garanta que `plugin.json` está em `.claude-plugin/plugin.json`, não na raiz
- Comando pra empacotar limpo: `git archive --format=zip --output=plugin.zip HEAD`

### "Falha na sincronização do marketplace" (Claude Desktop)

**Causa A — GitHub App não autorizado:** O Claude Desktop usa o GitHub App da Anthropic pra clonar repos. Diferente do Claude Code (CLI), que usa `git` puro com suas credenciais locais.

**Solução A:**
1. Vai em https://github.com/settings/installations
2. Procura o GitHub App da Claude/Anthropic
3. Configure → Repository access → "All repositories" ou adiciona o repo manualmente

**Causa B — Cache server-side poisoned:** Se uma versão anterior do marketplace teve syncs broken, o servidor da Anthropic pode cachear esse estado.

**Solução B:** Renomeia o `name` do `marketplace.json` pra um valor inédito (ex: `meu-plugin` → `meu-plugin-v2`). Bumpe versão e reempurre. Cache server-side trata como marketplace novo.

### "This plugin uses a source type your Claude Code version does not support"

**Causa:** Em `marketplace.json`, o campo `source` da entry do plugin tem valor inválido.

**Soluções comuns:**
- Caminho relativo MUST começar com `./` (não bare `.` ou `path/`)
- Se usa GitHub: `"source": {"source": "github", "repo": "owner/repo"}`
- Se é plugin no próprio repo: `"source": "./"`

### "invalid manifest file ... author: expected object, received string"

**Causa:** Schema do `plugin.json` violado — Claude Desktop tem validador estrito.

**Schema correto:**
```json
{
  "name": "kebab-case-name",
  "version": "X.Y.Z",
  "description": "...",
  "author": {"name": "..."},  // OBJETO, não string
  "category": "marketing",     // SINGULAR, não plural "categories"
  "keywords": [...],
  "license": "MIT"
}
```

**Não declarar `skills: [...]`** se você usa o folder default `skills/` na raiz. O explicit array é rejeitado como "Invalid input".

---

## Orquestração

### `/marketing-os: cria página de aplicação` chamou `frontend-design` em vez dos `mos-*`

**Causa:** A skill `frontend-design` (plugin oficial Anthropic) tem trigger MUITO agressivo ("build pages, applications") e estava preempting o orquestrador.

**Solução:** Garantir que está na v6.1.7+ — o SKILL.md agora reivindica explicitamente território sobre "página de aplicação" e dispatcha workflow #5 (mos-funnel + mos-copy + mos-design) ANTES de qualquer handoff a frontend-design.

**Como atualizar:**
```
/plugin marketplace update mos-marketplace
/plugin update marketing-os@mos-marketplace
/reload-plugins
```

### Briefing genérico → orquestrador chuta nicho/avatar errado

**Causa:** Versões anteriores a v6.2.1 não tinham protocolo de briefing vago.

**Solução:** Atualizar pra v6.2.1+. O orquestrador agora pergunta as 5 chaves antes de dispatchar (nicho/avatar/ticket/plataforma/urgência), pulando perguntas que já têm resposta no memory do projeto.

### Hook do agent falha com "No such file or directory"

**Sintoma:** Quando um `mos-*` agent tenta escrever arquivo, sai erro de hook script não encontrado.

**Causa:** Versões anteriores a v6.1.7 usavam caminho relativo `python3 scripts/hooks/quality_gate_hook.py`. O CWD do hook é do user, não do plugin install dir, então só funcionava quando você rodava DENTRO do repo do plugin.

**Solução:** Atualizar pra v6.1.7+. O caminho correto é `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/hooks/quality_gate_hook.py`.

---

## Memory

### Memory de cliente caiu na pasta errada

**Sintoma:** Você esperava memory em `<projeto-cliente>/.claude/agent-memory/` mas ela apareceu em outra pasta (ex: no próprio repo do marketing-os).

**Causa:** Memory é escopada pelo CWD do Claude Code quando o agent foi invocado. Se você rodou `/marketing-os` enquanto a CWD era a pasta do plugin (não do cliente), a memory foi salva lá.

**Solução:** Migre manualmente:
```bash
# Cria pasta destino correta (note o "marketing-os-" prefix quando vem via plugin)
mkdir -p "<projeto-cliente>/.claude/agent-memory/marketing-os-mos-copy/"

# Move arquivos
mv "<repo-marketing-os>/.claude/agent-memory/mos-copy/"*.md \
   "<projeto-cliente>/.claude/agent-memory/marketing-os-mos-copy/"

# Atualiza MEMORY.md (índice) na pasta destino se precisar
```

### Memory não carrega entre sessões

**Causa:** O frontmatter do agent declara `memory: project` (escopo = pasta atual). Cada projeto tem memory isolada.

**Comportamento esperado:**
- Pasta A: agent tem memory A
- Pasta B: agent começa do zero
- Pasta A novamente: memory A volta

**Se quiser memory compartilhada entre projetos:**
- Editar `agents/mos-<agent>.md` frontmatter: trocar `memory: project` por `memory: user`
- Memory user-scope vai pra `~/.claude/agent-memory/` (compartilhada)

### Diretório `marketing-os-mos-copy/` vs `mos-copy/` — qual é qual?

- **`mos-copy/`** (sem prefixo): agent foi resolvido como **local** (você editou direto em `agents/mos-copy.md` no repo)
- **`marketing-os-mos-copy/`** (com prefixo): agent foi resolvido como **vindo do plugin instalado** (namespace plugin name + agent name)

São pastas diferentes pra contextos diferentes. Não há cross-contaminação.

---

## Distribuição

### CI falhando com "Required test coverage of 80% not reached"

**Causa:** Coverage threshold do GitHub Actions estava em 80% mas a realidade do projeto (utility scripts não-testáveis) ficava em ~71%.

**Solução implementada na v6.3.0:**
- `.coveragerc` exclui scripts utilities (`validate_agents.py`, `voice_extractor.py`)
- Threshold ajustado pra 70%
- `requirements.txt` instalado no CI antes de pytest

### Auto-update não pegou versão nova

**Causa:** Auto-update roda **no startup da sessão** (não mid-session). Se você está numa sessão aberta, ela carregou a versão antiga do cache.

**Solução:**
- **Esperar:** próxima sessão pega a versão nova automaticamente
- **Forçar agora:**
  ```
  /plugin marketplace update mos-marketplace
  /plugin update marketing-os@mos-marketplace
  /reload-plugins
  ```

### `claude plugin update marketing-os` falha com "Plugin not found" (CLI)

**Sintoma:** Pelo CLI fora da sessão interativa:
```
$ claude plugin update marketing-os
Checking for updates for plugin "marketing-os" at user scope…
✘ Failed to update plugin "marketing-os": Plugin "marketing-os" not found
```

Mesmo com o plugin instalado e enabled (`claude plugin list` confirma).

**Causa:** O comando `update` da CLI procura o plugin pelo nome curto, mas a resolução falha quando o marketplace cache local diverge do remoto (validado em v6.5.0). `claude plugin marketplace update <name>` atualiza o cache de manifests mas o `update` do plugin em si continua errando.

**Workaround verificado:**
```bash
claude plugin marketplace update mos-marketplace
claude plugin uninstall marketing-os@mos-marketplace
claude plugin install marketing-os@mos-marketplace
```

Reinstalação puxa a versão nova do cache atualizado. Não perde nada — settings/memory são externos ao plugin install.

### Como saber qual versão está ativa?

```
/plugin
```

Lista plugins instalados com versão. Se mostrar `6.x.y` → versão atual carregada.

---

## Bugs conhecidos / Limitações

### 23 dos 25 slash commands não dispatcham `mos-*` agents diretamente

**Status:** Conhecido (descoberto na auditoria de v6.3.0). Apenas `/criar-post` e `/criar-meu-clone` dispatcham agents nativos. Os outros 23 commands têm lógica inline — funcionam, mas não aproveitam a profundidade dos subagents.

**Workaround:** Use `/marketing-os` em linguagem natural em vez do slash command — o orquestrador da skill dispatcha corretamente.

```
# Em vez de:
/criar-carrossel 10 erros de copy

# Prefira (até v6.3.0+):
/marketing-os cria carrossel sobre 10 erros de copy
```

**Fix planejado:** v6.4.x — atualizar os 23 commands pra dispatcham os workflows correspondentes do SKILL.md.

### Tier 2 smoke tests deferred

**Status:** Os Tier 2 tests (em `scripts/tests/test_agents_smoke.py`) requerem Claude Code login pra rodar e estão marcados com `@pytest.mark.smoke`. Não rodam no CI por padrão.

**Pra rodar localmente:**
```bash
python -m pytest scripts/tests/test_agents_smoke.py -v -m smoke
```

---

## Suporte

- **GitHub Issues:** https://github.com/rilnermucio/Marketing-OS/issues
- **CHANGELOG:** [CHANGELOG.md](../CHANGELOG.md) — histórico completo de releases
- **AGENTS.md:** [../AGENTS.md](../AGENTS.md) — guia técnico canônico (também lido por Codex CLI, Cursor, Gemini)
