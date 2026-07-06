# Runbook: install do plugin falhando

> Origem: debug real das versões v6.1.0 a v6.1.6, quando 7 causas distintas quebraram install em produção. Falhas de manifest são F-MAN-01/02; de pacote Codex, F-CODEX-01..03.

## Sintoma → primeiro passo

| Sintoma | Vá para |
|---|---|
| "Plugin validation failed" no Desktop | Passo 2 (gotchas de manifest) |
| "source type your Claude Code version does not support" | Passo 2, item source `./` |
| Install passa mas plugin não aparece / não sincroniza | Passo 3 (cache de marketplace) |
| Falha sem mensagem útil | Passo 1 (extrair o erro real) |
| Install Codex falha | Passo 4 |

## Passo 1: extrair o erro real (macOS)

```bash
log show --predicate 'process == "Claude" OR process == "Claude Helper"' \
  --info --debug --last 10m \
  | grep -iE "marketplace|github|git|fetch|fail|error|sync|plugin"
```

Rode logo após reproduzir a falha (janela de 10 min). A mensagem real quase sempre está aqui, não na UI.

## Passo 2: validar contra os gotchas conhecidos

```bash
claude plugin validate .
```

Depois confira manualmente a tabela "Plugin distribution gotchas" do `AGENTS.md` (cada linha quebrou install uma vez): `plugin.json` DENTRO de `.claude-plugin/`; `author` como object; `category` singular; sem field `skills`; `source` começando com `./` no marketplace.json; description/version top-level no marketplace.json; nomes kebab-case; nenhum nome reservado (`claude-code-marketplace`, `anthropic-plugins`, etc.).

Lembrete que custou 6 patches: **`claude plugin validate` passar é necessário, não suficiente.** O teste que fecha é install real num projeto limpo.

## Passo 3: cache de marketplace server-side

A Anthropic cacheia estado por NOME de marketplace. Se o seu marketplace já teve syncs quebrados, o nome pode estar envenenado. Solução comprovada: renomear o marketplace (precedente: `marketing-os-marketplace` → `mos-marketplace`) e reinstalar.

## Passo 4: pacote Codex

```bash
python scripts/build_codex_plugin.py
python scripts/validate_codex_plugin.py
```

Conferir: versão base semver + sufixo `+codex.YYYYMMDD`; estrutura do pacote em `plugins/marketing-os/`; nenhum conteúdo pessoal no pacote (workspace/, memory, mídia de teste). Install de referência:

```bash
codex plugin marketplace add rilnermucio/esp-marketing-os --ref <tag>
codex plugin add marketing-os@marketing-os-marketplace
```

## Se resolver por caminho novo

Documente: linha nova na tabela de gotchas do `AGENTS.md` (se for gotcha de plataforma) ou atualização deste runbook + ID novo na [FAILURE-TAXONOMY.md](../FAILURE-TAXONOMY.md) se for classe nova de falha.
