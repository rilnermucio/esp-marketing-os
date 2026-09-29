# Runbook: refresh de fatos de plataforma

Limites de formato e nomes de produto mudam sem aviso. Em 2026-09 a auditoria achou Reels "até 90s" (3 min desde jan/2025), Shorts "< 60s" (3 min desde out/2024), Stories "15s", carrossel "10 slides" (20 desde ago/2024) e "Advantage+ Shopping" (Advantage+ Sales desde fev/2025).

## Quando rodar

- A cada release (passo do [RELEASE-CHECKLIST](../RELEASE-CHECKLIST.md)).
- A cada 90 dias, mesmo sem release.
- Quando um usuário ou agent apontar um limite ou nome divergente.

## Passos

1. `python3 scripts/mos.py facts check` lista as linhas de `references/platform-facts.md` com verificação vencida (padrão: mais de 180 dias).
2. Para cada linha vencida, confirme via WebSearch em fonte primária (blog oficial da plataforma) ou em duas fontes secundárias independentes. Atualize valor, fonte e `Verificado em`.
3. Se o valor mudou, procure menções antigas: `grep -rn "<valor antigo>" agents subagents references commands assets`. Corrija limite técnico; recomendação de duração ou estrutura ideal é decisão da KB e pode ficar.
4. Fato novo que um agent passou a citar com número entra no registro na mesma rodada.
5. Registre no worklog da rodada o que mudou e a fonte.

## Fora do escopo

Benchmarks de mercado (CTR, taxa de conversão) não entram no registro: são faixas direcionais com fact-check próprio (F-CLAIM-01).
