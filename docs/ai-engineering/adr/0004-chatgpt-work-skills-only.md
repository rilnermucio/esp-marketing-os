# ADR-0004: ChatGPT Work e Codex por pacote universal skills-only

**Status**: aceito
**Data**: 2026-08-05
**Autor**: Codex (GPT-5)

## Contexto

O Marketing OS já tinha uma distribuição própria para o Claude Code e um pacote `.codex-plugin` consumido pelo Codex. O ChatGPT Work passou a aceitar plugins compostos somente por skills, usando o mesmo manifesto e a mesma convenção de `SKILL.md` que o Codex.

O pedido atual exige disponibilizar Avatar, USP, Oferta e os demais fluxos também no ChatGPT. Há dois caminhos tecnicamente válidos:

1. Reaproveitar o pacote existente como plugin `skills-only`.
2. Criar um aplicativo MCP com servidor hospedado, autenticação, ferramentas remotas e, opcionalmente, interface própria.

O Marketing OS hoje entrega raciocínio, conhecimento versionado, templates e scripts locais. Ele não depende de estado remoto, conta externa nem componente visual próprio para cumprir o contrato principal.

## Decisão

Distribuir ChatGPT Work e Codex a partir do mesmo pacote universal `skills-only` em `.codex-plugin/plugin.json`.

1. O manifesto público declara somente `skills` e metadados de interface. `apps` e `mcpServers` ficam ausentes.
2. `skills/marketing-os/SKILL.md` reconhece o ambiente ChatGPT Work, a invocação por `@Marketing OS` e o fallback quando o host não expõe multi-agent ou shell.
3. `skills/marketing-os/agents/openai.yaml` concentra metadados específicos da interface OpenAI e permite invocação implícita.
4. O marketplace repo-scoped em `.agents/plugins/marketplace.json` serve ao desenvolvimento local no ChatGPT Desktop e no Codex.
5. O validador canônico verifica limites da listagem pública, categorias aceitas, starter prompts, metadados de skill e a fronteira `skills-only`.

## Alternativas consideradas

1. **Criar MCP agora**: adiado porque acrescentaria hospedagem, autenticação, política de dados, observabilidade e manutenção operacional sem necessidade funcional comprovada.
2. **Manter um pacote separado para ChatGPT Work**: rejeitado porque duplicaria skill, knowledge bases e regras de distribuição, aumentando o risco de drift.
3. **Restringir a skill por `policy.products`**: rejeitado por compatibilidade entre validadores e hosts. A ausência do campo permite descoberta universal, enquanto o marketplace e o manifesto continuam delimitando a instalação.
4. **Executar produção inline sem a arquitetura Tier 1/Tier 2**: rejeitado porque mudaria o contrato de especialização e reduziria consistência entre os três ambientes.

## Consequências

Positivas: uma fonte de verdade atende ChatGPT Work e Codex; Avatar, USP e Oferta ficam disponíveis por linguagem natural; o pacote continua instalável sem infraestrutura remota; testes detectam regressões nos metadados públicos.

Negativas: hosts sem shell não executam os aceleradores Python; hosts sem multi-agent consolidam o trabalho no agente principal; o plugin não oferece UI própria, sincronização remota nem conectores autenticados.

## Critério de revisão

Reabrir esta decisão quando surgir pelo menos uma necessidade real de ferramenta remota, estado compartilhado, autenticação externa, UI interativa ou telemetria centralizada. Nesse cenário, o MCP deve ser desenhado como uma camada complementar, mantendo as skills como interface de instrução sempre que possível.
