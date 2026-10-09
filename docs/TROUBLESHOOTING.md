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

### App desktop mostra versão antiga do plugin (cópia sincronizada da conta)

**Sintoma:** no app desktop faltam agents ou commands que existem na versão instalada (ex: sem `mos-offer`, `mos-community`, `mos-partnerships`, `/mo`, `/aprender`), mesmo com `/plugin` mostrando a versão nova no terminal.

**Causa:** marketplaces adicionados na sua conta claude.ai são sincronizados para `~/.claude/plugins/synced/`. Se um desses marketplaces parou de sincronizar, a cópia fica congelada e o app desktop pode carregar essa cópia em vez da instalada pelo marketplace local. Caso real (2026-09-28): marketplace de conta "Marketing-OS" congelado na v6.1.5 desde 2026-05-07, enquanto a 6.16.0 estava instalada.

**Diagnóstico:**
Peça ao Claude "rode o diagnóstico de instalação do Marketing OS" ou, num clone do repositório:
```bash
python3 scripts/mos.py install doctor
```
Lista todas as cópias do Marketing OS (cache, sincronizadas, registros de instalação) com a versão de cada uma e avisa quando alguma está atrás da referência.

**Solução:** nas configurações de plugins da sua conta claude.ai, remova o marketplace antigo (ou atualize-o para `rilnermucio/esp-marketing-os`) e mantenha uma só origem do plugin. Depois reabra o app e confirme que a lista de agents inclui `marketing-os:mos-offer`.

---

### Hook do agent falha com "No such file or directory"

**Sintoma:** Quando um `mos-*` agent tenta escrever arquivo, sai erro de hook script não encontrado.

**Causa:** Versões anteriores a v6.1.7 usavam caminho relativo `python3 scripts/hooks/quality_gate_hook.py`. O CWD do hook é do user, não do plugin install dir, então só funcionava quando você rodava DENTRO do repo do plugin.

**Solução:** Atualizar para a versão atual. Desde a ADR-0005 o gate vive só em `hooks/hooks.json`, com `"${CLAUDE_PLUGIN_ROOT}/scripts/hooks/quality_gate_hook.py"` entre aspas. Hooks no frontmatter de agent de plugin são ignorados pela plataforma e não devem ser declarados.

---

## Memory

### Memory de cliente caiu na pasta errada

**Sintoma:** você esperava memory em `<projeto-cliente>/.claude/agent-memory/` mas ela apareceu em outra pasta (ex: no próprio repo do marketing-os).

**Causa:** memory é escopada pelo diretório em que a sessão do Claude Code roda. Se você rodou o Marketing OS com a sessão aberta na pasta do plugin, a memory foi salva lá.

**Solução:** mova a pasta para o projeto certo, mantendo o nome nativo:
```bash
mkdir -p "<projeto-cliente>/.claude/agent-memory/"
mv "<repo-marketing-os>/.claude/agent-memory/marketing-os-mos-copy" \
   "<projeto-cliente>/.claude/agent-memory/"
```

### Memory não carrega entre sessões

**Causa:** o frontmatter do agent declara `memory: project` (escopo = pasta atual). Cada projeto tem memory isolada.

**Comportamento esperado:**
- Pasta A: agent tem memory A
- Pasta B: agent começa do zero
- Pasta A novamente: memory A volta

Se a memory existe mas o agent parece não enxergar, confira o nome do diretório (seção abaixo).

### Diretório `marketing-os-mos-copy/` vs `mos-copy/`: qual é qual?

- **`marketing-os-mos-copy/`**: diretório nativo que o Claude Code usa para o agent do plugin instalado. A plataforma injeta o início do `MEMORY.md` dele no contexto do agent. É o canônico desde a ADR-0006.
- **`mos-copy/`**: diretório que o plugin usou entre as versões 6.5 e 6.16. A plataforma não o lê para agent de plugin, então aprendizados gravados ali não chegavam ao agent.

**Solução:** rode `python3 scripts/init_agent_memory.py` no projeto (ou apenas grave um aprendizado novo com `memory_writer.py`). O conteúdo de `mos-*/` é movido para `marketing-os-mos-*/`; se os dois existirem, o antigo é anexado ao novo e a pasta antiga vira `mos-*.migrado`, sem apagar nada.

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

Lista plugins instalados com versão. Para ver todas as cópias da máquina (incluindo as sincronizadas da conta claude.ai, que o app desktop pode carregar), rode `python3 scripts/mos.py install doctor`.

---

## Bugs conhecidos / Limitações

### Commands de produção sem dispatch para `mos-*`

**Status:** Resolvido desde v6.5.0. Todos os commands de produção passam pelo contrato de dispatch. Quatro utilities permanecem sem dispatch por desenho: `/publicar-notion`, `/campanha`, `/projeto` e `/datas-sazonais`.

Se um command novo executar produção inline, rode `python -m pytest scripts/tests/test_commands_dispatch.py -v`. A suite identifica o arquivo que não declarou `Agent(subagent_type: "marketing-os:mos-*")`.

### Tier 2 smoke tests deferred

**Status:** os smoke tests (`scripts/tests/test_install_smoke.py` e `test_agents_smoke.py`) chamam o Claude real, exigem login e só rodam com `MOS_SMOKE=1`. Não rodam no CI. Os dois carregam a árvore de trabalho com `--plugin-dir` e a sessão fora do repo, como numa instalação real.

**Para rodar localmente:**
```bash
MOS_SMOKE=1 python -m pytest scripts/tests/test_install_smoke.py -m smoke -v
```

---

## Suporte

- **GitHub Issues:** https://github.com/rilnermucio/Marketing-OS/issues
- **CHANGELOG:** [CHANGELOG.md](../CHANGELOG.md) — histórico completo de releases
- **AGENTS.md:** [../AGENTS.md](../AGENTS.md) — guia técnico canônico (também lido por Codex CLI, Cursor, Gemini)
