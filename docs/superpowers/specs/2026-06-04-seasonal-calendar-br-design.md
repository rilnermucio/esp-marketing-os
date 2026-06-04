# Spec — seasonal_calendar_br (camada de dados)

**Status:** aprovado 2026-06-04. Fase 1 do `docs/ROADMAP.md` (Grupo A).

## Objetivo
Camada de dados determinística das efemérides comerciais BR, computada pra qualquer ano (sem dataset estático que precise de manutenção anual). Alimenta `content_calendar`/agents e dá descoberta via command.

## Abordagem
Módulo Python que computa 3 tipos de data:
- **Fixas:** Ano Novo (01/01), Consumidor (15/03), Namorados (12/06), Cliente (15/09), Crianças (12/10), Natal (25/12).
- **Por regra (N-ésimo dia da semana):** Mães (2º dom. maio), Pais (2º dom. agosto BR), Black Friday (4ª sexta nov.), Cyber Monday (segunda após Black Friday), Solteiro (11/11).
- **Móveis (Computus a partir da Páscoa):** Carnaval (Páscoa-47), Sexta-feira Santa (Páscoa-2), Páscoa, Corpus Christi (Páscoa+60).

## Schema por data
`{data: "YYYY-MM-DD", nome, tipo: comercial|cultural|religiosa, dias_antecedencia_ideal: int, nichos_fortes: [str]}`

## Interface
- `scripts/seasonal_calendar_br.py`: `--ano AAAA` | `--from --to` | `--proximos N` (default próximos 90 dias a partir de hoje), `--json` ou saída humana. Usa `add_output_args` (padrão dos demais scripts).
- `mos.py`: nova categoria `seasonal` → `list`.
- `commands/datas-sazonais.md`: utilitário não-dispatch (igual `/campanha` index). Mostra datas da janela + dias de antecedência + sugere preset de campanha (Black Friday → `/campanha-black-friday`) e agent que encaixa.

## Alvos de teste (computados e confirmados)
- 2026: Páscoa 04-05, Carnaval 02-17, Sexta Santa 04-03, Corpus 06-04, Mães 05-10, Pais 08-09, Black Friday 11-27.
- 2027: Páscoa 03-28, Carnaval 02-09, Mães 05-09, Pais 08-08, Black Friday 11-26.
- Filtro de janela (`--from/--to`, `--proximos`) retorna só o intervalo, ordenado por data.
- Schema completo em cada item; `--json` é JSON válido.

## Arquivos
Novos: `scripts/seasonal_calendar_br.py`, `scripts/tests/test_seasonal_calendar_br.py`, `commands/datas-sazonais.md`.
Editados (forçados pelos guard-rails): `scripts/mos.py` (categoria seasonal), `README.md` + `AGENTS.md` (35→36 commands, não-dispatch 3→4), `scripts/tests/test_commands_dispatch.py` (allowlist).

## Fora de escopo
Geração de ângulos/conteúdo por data (os agents já fazem quando recebem a data). Sem dispatch no command.
