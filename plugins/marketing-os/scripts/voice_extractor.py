#!/usr/bin/env python3
"""
Voice Extractor - Marketing OS

Analisa amostras de copy em PT-BR e extrai dados objetivos pra alimentar
o workflow `/criar-meu-clone`. Substitui analise qualitativa manual do
Claude por dados estatisticos sobre vocabulario, cadencia e padroes.

Uso:
    python3 scripts/voice_extractor.py --input PATH [PATH ...] [--output FORMAT]

Argumentos:
    --input          Arquivos individuais ou diretorios com .md/.txt
    --output {md|json}  Formato do relatorio (padrao: md)
    --top-words N    Quantas palavras distintivas listar (padrao: 30)
    --top-ngrams N   Quantos n-grams listar (padrao: 20)
    --min-freq N     Frequencia minima pra considerar palavra (padrao: 2)

Saida:
    - Top N palavras distintivas (frequencia >= min-freq, fora de stopwords)
    - Distribuicao de tamanho de frase (% < 8 / 8-15 / 15-25 / > 25)
    - Top N bigramas e trigramas frequentes
    - Contagem de pontuacao distintiva (:, parenteses, travessao, ?, !, ...)
    - Primeiras e ultimas frases de cada amostra
    - Total de amostras + total de palavras

Sem dependencias externas (stdlib only).
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

# Stopwords PT-BR comuns. Lista pratica, nao exaustiva.
STOPWORDS = set("""
a as o os um uma uns umas
e ou mas que se nao sim ja la aqui ali
de da do das dos
em no na nos nas
para por pelo pela pelos pelas
com sem sob sobre
ante apos ate contra desde entre perante
segundo conforme mediante durante
eu voce ele ela nos vos eles elas
me te se lhe lhes
mim ti si comigo contigo consigo conosco convosco
meu minha teu tua seu sua nosso nossa vosso vossa
este esta esse essa aquele aquela
isto isso aquilo
ser estar ter fazer dizer ir vir ver dar
querer saber poder dever parecer ficar deixar passar dar
muito pouco mais menos quanto tanto tao todo todos toda todas
quem qual quais cuja cujo cujas cujos
onde quando como porque
nem tambem so apenas ainda
sao foi era foram esta estao estava estavam
seja sejam fosse fossem ser sera sera serao
ha houve havia haver havera
isso esse essa este esta essa
voce vc tu
porem entao entretanto contudo todavia
agora hoje ontem amanha
depois antes durante
ja ainda nunca sempre quase talvez certamente
realmente certamente provavelmente
muito pouco bastante demais
bem mal melhor pior
""".split())


def read_files(paths: list) -> list:
    """Carrega arquivos de paths (arquivos individuais ou diretorios)."""
    samples = []
    for p in paths:
        path = Path(p)
        if not path.exists():
            print(f"AVISO: nao existe: {p}", file=sys.stderr)
            continue
        if path.is_file():
            try:
                samples.append(
                    {
                        "name": path.name,
                        "text": path.read_text(encoding="utf-8"),
                    }
                )
            except Exception as e:
                print(f"AVISO: falha lendo {p}: {e}", file=sys.stderr)
        elif path.is_dir():
            for f in sorted(path.rglob("*.md")) + sorted(path.rglob("*.txt")):
                try:
                    samples.append(
                        {
                            "name": str(f.relative_to(path)),
                            "text": f.read_text(encoding="utf-8"),
                        }
                    )
                except Exception as e:
                    print(f"AVISO: falha lendo {f}: {e}", file=sys.stderr)
    return samples


def normalize(text: str) -> str:
    """Remove markdown headers, links, code blocks, e excesso de whitespace."""
    text = re.sub(r"```[^`]*```", " ", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]+`", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^#{1,6}\s.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^---+$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize_words(text: str) -> list:
    """Tokeniza em palavras, lowercase, mantendo acentos PT-BR."""
    words = re.findall(r"[a-záàâãéêíïóôõúüç]+", text.lower())
    return [w for w in words if len(w) >= 4 and w not in STOPWORDS]


def tokenize_sentences(text: str) -> list:
    """Tokeniza em frases simples (split por . ! ? + quebras de paragrafo)."""
    sentences = re.split(r"(?<=[.!?])\s+|\n\n+", text)
    return [s.strip() for s in sentences if len(s.strip()) > 5]


def extract_distinctive_words(samples: list, top_n: int, min_freq: int) -> list:
    """Top N palavras com freq >= min_freq, ordenadas por (freq * cross-sample presence)."""
    word_counter = Counter()
    sample_presence = {}

    for sample in samples:
        text = normalize(sample["text"])
        words = tokenize_words(text)
        unique_words = set(words)
        for w in words:
            word_counter[w] += 1
        for w in unique_words:
            sample_presence[w] = sample_presence.get(w, 0) + 1

    candidates = []
    for word, freq in word_counter.items():
        if freq < min_freq:
            continue
        presence = sample_presence.get(word, 0)
        score = freq * (1 + presence * 0.3)
        candidates.append((word, freq, presence, score))

    candidates.sort(key=lambda x: x[3], reverse=True)
    return candidates[:top_n]


def extract_ngrams(samples: list, n: int, top_k: int, min_freq: int) -> list:
    """N-grams (n=2 ou 3) mais frequentes, com filtro de stopwords nas bordas."""
    counter = Counter()
    for sample in samples:
        text = normalize(sample["text"])
        words = re.findall(r"[a-záàâãéêíïóôõúüç]+", text.lower())
        for i in range(len(words) - n + 1):
            ngram = words[i : i + n]
            if ngram[0] in STOPWORDS or ngram[-1] in STOPWORDS:
                continue
            if any(len(w) < 3 for w in ngram):
                continue
            counter[" ".join(ngram)] += 1

    return [(ng, c) for ng, c in counter.most_common(top_k) if c >= min_freq]


def sentence_length_distribution(samples: list) -> dict:
    """Distribuicao de tamanho de frase em palavras."""
    buckets = {
        "< 8 palavras": 0,
        "8-15 palavras": 0,
        "15-25 palavras": 0,
        "> 25 palavras": 0,
    }
    total = 0
    lengths = []

    for sample in samples:
        text = normalize(sample["text"])
        sentences = tokenize_sentences(text)
        for s in sentences:
            n = len(s.split())
            lengths.append(n)
            total += 1
            if n < 8:
                buckets["< 8 palavras"] += 1
            elif n < 15:
                buckets["8-15 palavras"] += 1
            elif n < 25:
                buckets["15-25 palavras"] += 1
            else:
                buckets["> 25 palavras"] += 1

    if total == 0:
        return {"distribution": buckets, "avg": 0, "median": 0, "total_sentences": 0}

    lengths.sort()
    median = lengths[len(lengths) // 2]
    avg = sum(lengths) / total

    distribution_pct = {k: round(100 * v / total, 1) for k, v in buckets.items()}
    return {
        "distribution_pct": distribution_pct,
        "distribution_abs": buckets,
        "avg_words_per_sentence": round(avg, 1),
        "median_words_per_sentence": median,
        "total_sentences": total,
    }


def punctuation_analysis(samples: list) -> dict:
    """Conta uso de pontuacao distintiva."""
    total_chars = 0
    counts = {
        "em_dash": 0,
        "colon": 0,
        "parens_open": 0,
        "question": 0,
        "exclamation": 0,
        "ellipsis": 0,
        "hyphen": 0,
        "semicolon": 0,
    }
    for sample in samples:
        text = sample["text"]
        total_chars += len(text)
        counts["em_dash"] += text.count("—")
        counts["colon"] += text.count(":")
        counts["parens_open"] += text.count("(")
        counts["question"] += text.count("?")
        counts["exclamation"] += text.count("!")
        counts["ellipsis"] += text.count("...") + text.count("…")
        counts["hyphen"] += text.count(" - ")
        counts["semicolon"] += text.count(";")

    if total_chars == 0:
        return counts
    return {
        "counts_absolute": counts,
        "per_1000_chars": {
            k: round(1000 * v / total_chars, 2) for k, v in counts.items()
        },
        "total_chars": total_chars,
    }


def opening_closing_sentences(samples: list) -> dict:
    """Coleta primeiras e ultimas frases de cada amostra."""
    openings = []
    closings = []
    for sample in samples:
        text = normalize(sample["text"])
        sentences = tokenize_sentences(text)
        if not sentences:
            continue
        openings.append({"sample": sample["name"], "sentence": sentences[0][:200]})
        if len(sentences) > 1:
            closings.append({"sample": sample["name"], "sentence": sentences[-1][:200]})
    return {"openings": openings[:15], "closings": closings[:15]}


def render_markdown(report: dict) -> str:
    out = []
    out.append("# Voice Extraction Report")
    out.append("")
    out.append(f"**Total de amostras**: {report['samples_count']}")
    out.append(f"**Total de palavras analisadas**: {report['total_words']}")
    out.append(f"**Gerado em**: {report['generated_at']}")
    out.append("")

    out.append("## Top Palavras Distintivas")
    out.append("")
    out.append("| Posicao | Palavra | Freq Total | Presenca em N amostras | Score |")
    out.append("|---------|---------|-----------|----------------------|-------|")
    for i, (word, freq, presence, score) in enumerate(report["top_words"], 1):
        out.append(f"| {i} | `{word}` | {freq} | {presence} | {round(score, 1)} |")
    out.append("")

    out.append("## Cadencia (Tamanho de Frase)")
    out.append("")
    sld = report["sentence_length"]
    out.append(f"- Media: **{sld['avg_words_per_sentence']}** palavras/frase")
    out.append(f"- Mediana: **{sld['median_words_per_sentence']}** palavras/frase")
    out.append(f"- Total de frases analisadas: {sld['total_sentences']}")
    out.append("")
    out.append("Distribuicao:")
    for bucket, pct in sld["distribution_pct"].items():
        out.append(f"- **{bucket}**: {pct}%")
    out.append("")

    out.append("## Top Bigramas")
    out.append("")
    for ng, c in report["bigrams"]:
        out.append(f"- `{ng}` ({c}x)")
    out.append("")

    out.append("## Top Trigramas")
    out.append("")
    for ng, c in report["trigrams"]:
        out.append(f"- `{ng}` ({c}x)")
    out.append("")

    out.append("## Pontuacao Distintiva (por 1000 chars)")
    out.append("")
    pa = report["punctuation"]
    if "per_1000_chars" in pa:
        for k, v in pa["per_1000_chars"].items():
            out.append(f"- **{k}**: {v}")
    out.append("")

    out.append("## Primeiras Frases (Aberturas)")
    out.append("")
    for o in report["opening_closing"]["openings"]:
        out.append(f"- *[{o['sample']}]* {o['sentence']}")
    out.append("")

    out.append("## Ultimas Frases (Fechamentos)")
    out.append("")
    for c in report["opening_closing"]["closings"]:
        out.append(f"- *[{c['sample']}]* {c['sentence']}")
    out.append("")

    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(
        description="Extrai dados objetivos de amostras de copy para voice cloning",
    )
    parser.add_argument(
        "--input",
        nargs="+",
        required=True,
        help="Arquivos ou diretorios com amostras (.md, .txt)",
    )
    parser.add_argument(
        "--output",
        choices=["md", "json"],
        default="md",
        help="Formato do relatorio (padrao: md)",
    )
    parser.add_argument(
        "--top-words",
        type=int,
        default=30,
        help="Quantas palavras distintivas listar (padrao: 30)",
    )
    parser.add_argument(
        "--top-ngrams", type=int, default=20, help="Quantos n-grams listar (padrao: 20)"
    )
    parser.add_argument(
        "--min-freq", type=int, default=2, help="Frequencia minima (padrao: 2)"
    )
    args = parser.parse_args()

    samples = read_files(args.input)
    if not samples:
        print("ERRO: nenhuma amostra carregada", file=sys.stderr)
        return 1

    if len(samples) < 5:
        print(
            f"AVISO: apenas {len(samples)} amostras. Recomendado >= 10 para qualidade.",
            file=sys.stderr,
        )

    total_words = sum(
        len(re.findall(r"[a-záàâãéêíïóôõúüç]+", s["text"].lower())) for s in samples
    )

    from datetime import datetime

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "samples_count": len(samples),
        "total_words": total_words,
        "top_words": extract_distinctive_words(samples, args.top_words, args.min_freq),
        "sentence_length": sentence_length_distribution(samples),
        "bigrams": extract_ngrams(
            samples, n=2, top_k=args.top_ngrams, min_freq=args.min_freq
        ),
        "trigrams": extract_ngrams(
            samples, n=3, top_k=args.top_ngrams, min_freq=args.min_freq
        ),
        "punctuation": punctuation_analysis(samples),
        "opening_closing": opening_closing_sentences(samples),
    }

    if args.output == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(report))

    return 0


if __name__ == "__main__":
    sys.exit(main())
