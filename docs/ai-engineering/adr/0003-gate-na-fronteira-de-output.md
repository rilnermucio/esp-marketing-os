# ADR-0003: Contrato de qualidade na fronteira de output

**Status**: aceito
**Data**: 2026-08-03
**Autor**: Codex (GPT-5)

## Contexto

O hook canônico validava somente `Write`, `Edit` e `MultiEdit`. O baseline de output registrou uma entrega com padrões bloqueantes diretamente no chat, sem chamada de escrita, portanto fora da superfície observada. O avaliador par a par também estava preso aos critérios de copy e exigia consolidação manual das ordens A/B.

São duas manifestações da mesma fronteira incompleta: qualidade era medida em operações intermediárias, enquanto a saída realmente entregue e o resultado final do julgamento não tinham contrato executável.

## Decisão

Adotar uma interface executável na fronteira de output:

1. `scripts/hooks/quality_gate_hook.py` expõe `evaluate_event(data)` como núcleo puro compartilhado por `PreToolUse` e `SubagentStop`.
2. `hooks/hooks.json` registra o evento `SubagentStop` para `mos-.*`. A mensagem final em `last_assistant_message` passa pelos mesmos detectores canônicos.
3. O hook bloqueia a primeira falha. Uma nova falha com `stop_hook_active=true` é registrada como `retry_exhausted` e liberada para limitar a correção a uma tentativa.
4. `scripts/evals/output-profiles.json` versiona agent, tipo do quality gate e critérios por domínio. `scripts/copy_output_eval.py` preserva a interface legada e aceita perfis para copy, e-mail, anúncios, oferta, funil, SEO e vídeo.
5. O comando `consolidate` remapeia os rótulos físicos A/B e declara resultado somente quando as ordens normal e invertida concordam. Divergência vira `inconclusivo`.

O adapter automático de resposta final fica restrito ao Claude Code enquanto o runtime Codex não expuser um hook equivalente no formato do plugin. O score e o runner permanecem portáveis no pacote Codex.

## Alternativas consideradas

1. **Obrigar todo agent a salvar a entrega em arquivo**: rejeitado porque muda a experiência de uso e ainda permite uma resposta de chat divergente do arquivo validado.
2. **Duplicar regexes em cada agent**: rejeitado porque amplia F-BLOAT-03 e cria novas fontes de verdade.
3. **Bloquear indefinidamente até a resposta ficar limpa**: rejeitado pelo risco de loop e consumo sem limite. Uma tentativa é uma fronteira previsível.
4. **Chamar um modelo julgador dentro de toda produção**: rejeitado por custo, latência e variância. O julgamento continua amostrado e pós-sessão.
5. **Criar runners separados por domínio**: rejeitado porque a mecânica é idêntica. Perfis de dados isolam o que varia e mantêm uma única consolidação.

## Consequências

Positivas: respostas entregues no chat passam pelo detector no Claude Code; regexes continuam canônicas; o freio de retry tem teste; critérios de sete agentes prioritários ficam versionados; a consolidação remove o erro manual de mapear A/B.

Negativas: uma segunda saída inválida pode chegar ao usuário para evitar recursão; Codex ainda depende das camadas de prompt e CLI na resposta final; os novos domínios têm critérios, mas precisam de âncoras humanas calibradas antes de orientar releases.

## Critério de revisão

Reabrir se o runtime Codex oferecer hook de resposta final, se telemetria mostrar reincidência relevante após uma tentativa, ou se a calibração humana ficar abaixo de 8/10 em qualquer perfil.
