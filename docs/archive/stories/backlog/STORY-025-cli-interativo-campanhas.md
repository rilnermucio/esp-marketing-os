# STORY-025: CLI Interativo para Execução de Campanhas

**ID:** STORY-025
**Tipo:** Feature
**Prioridade:** P3
**Estimativa:** G (> 4 horas)
**Status:** Backlog
**Sprint:** A definir

---

## User Story

**Como** usuário do Marketing OS,
**Quero** um CLI interativo que me guie na criação e execução de campanhas passo a passo,
**Para que** possa usar todo o poder do sistema sem precisar lembrar de todos os comandos e parâmetros disponíveis.

---

## Contexto

O Marketing OS tem muitas capacidades mas a interface é baseada em conversação com Claude. Um CLI interativo tornaria o sistema mais acessível para fluxos de trabalho repetitivos e execução autônoma.

---

## Acceptance Criteria

```
[ ] Script `scripts/mos_cli.py` criado (extensão do mos.py existente):
    - Menu interativo com as principais ações
    - Wizard guiado para criar campanhas
    - Histórico de campanhas criadas
    - Modo batch para executar múltiplas ações

[ ] Comandos disponíveis no CLI:
    - `mos campanha` → wizard de nova campanha
    - `mos campanha --tipo lancamento` → preset específico
    - `mos clone [nome]` → ativar clone de voz
    - `mos relatorio` → gerar relatório semanal
    - `mos audit [arquivo]` → auditar conteúdo
    - `mos hashtags [nicho] [plataforma]` → gerar hashtags
    - `mos status` → ver campanhas e projetos ativos

[ ] Wizard de campanha com perguntas interativas:
    - Tipo de campanha (lista de opções)
    - Produto/serviço sendo promovido
    - Nicho e avatar
    - Canais de distribuição
    - Budget (se aplicável)
    - Prazo da campanha

[ ] Integração com os presets de campanha:
    - `/campanha lancamento`, `/campanha prospeccao`, etc.
    - Output gerado e salvo em `output/projects/[nome-campanha]/`

[ ] Help contextual:
    - `mos --help` → lista todos os comandos
    - `mos campanha --help` → detalhes do wizard

[ ] Testes em `scripts/tests/test_mos_cli.py`
```

---

## Referências

- Script existente: `scripts/mos.py` (base a expandir)
- Comandos existentes: `marketing-os/commands/`
- Presets de campanha: `marketing-os/commands/campanha.md`
