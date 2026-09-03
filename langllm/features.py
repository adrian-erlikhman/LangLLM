"""Step 4 — 21 interpretable stylometric features, defined on Universal Dependencies so each
means the same thing in every language. Parsing: Stanza (tokenize, pos, lemma, depparse).

Groups
  lexical      mattr, hapax_rate, mean_token_len, zipf_slope
  syntactic    sent_len_mean, sent_len_sd, burstiness, dep_depth, subord_rate,
               func_word_ratio, first_person_rate
  structure    para_count, para_len_mean, question_rate, connective_rate
  punctuation  comma_per_1k, colon_per_1k, dash_per_1k, semicolon_per_1k   (script equivalents mapped)
  character    bigram_entropy, digit_rate

English-only measures (Flesch, Fog, hedges, passive, contractions) are deliberately absent.

    python -m langllm.features             # data/features/features.csv from kept responses
    python -m langllm.features --all       # ignore the validation `keep` flag
"""
from __future__ import annotations
import argparse
import math
import re
import unicodedata
from collections import Counter
import numpy as np
import pandas as pd
from .config import load_config, ROOT, FEATURES_DIR
from .collect import iter_raw

FEATURE_NAMES = [
    "mattr", "hapax_rate", "mean_token_len", "zipf_slope",
    "sent_len_mean", "sent_len_sd", "burstiness", "dep_depth", "subord_rate", "func_word_ratio", "first_person_rate",
    "para_count", "para_len_mean", "question_rate", "connective_rate",
    "comma_per_1k", "colon_per_1k", "dash_per_1k", "semicolon_per_1k",
    "bigram_entropy", "digit_rate",
]
FEATURE_GROUPS = {
    "lexical": FEATURE_NAMES[0:4], "syntactic": FEATURE_NAMES[4:11], "structure": FEATURE_NAMES[11:15],
    "punctuation": FEATURE_NAMES[15:19], "character": FEATURE_NAMES[19:21],
}
META_COLS = ["cell_id", "model_key", "model_served", "prompt_id", "lang", "gen", "fk_tier", "stance", "n_tokens", "n_sentences"]

FUNCTION_UPOS = {"ADP", "AUX", "CCONJ", "DET", "PART", "PRON", "SCONJ"}
SUBORD_DEPRELS = {"acl", "advcl", "ccomp", "xcomp", "csubj"}
CONNECTIVE_DEPRELS = {"cc", "mark"}
# zh/ja UD treebanks carry no Person feature; first person is lexical there.
FIRST_PERSON_LEXICON = {"我", "我们", "我們", "咱们", "私", "わたし", "僕", "俺", "私たち", "我々", "われわれ"}

COMMA_CHARS = set(",，、")
COLON_CHARS = set(":：")
SEMICOLON_CHARS = set(";；")
DASH_CHARS = set("—–―")
QUESTION_CHARS = set("?？")
_SPACED_HYPHEN = re.compile(r"(?<=\s)-{1,2}(?=\s)")  # ' - ' / ' -- ' used as a dash

# ---------------------------------------------------------------------------- Stanza
_PIPES: dict[str, object] = {}


def pipeline(lang: str):
    """Cached Stanza pipeline for a language (models must already be downloaded)."""
    if lang not in _PIPES:
        import stanza
        cfg = load_config()
        mdir = str(ROOT / cfg["features"]["stanza_dir"])
        pkg = cfg["languages"][lang]["stanza"]
        # zh/ja: Stanza does not split on 。！？ reliably, so we pre-split and disable its splitter.
        _PIPES[lang] = stanza.Pipeline(pkg, dir=mdir, processors="tokenize,pos,lemma,depparse",
                                       download_method=None, use_gpu=False, verbose=False,
                                       tokenize_no_ssplit=(lang in CJK_LANGS))
    return _PIPES[lang]


CJK_LANGS = {"zh", "ja"}
_CJK_SENT_END = re.compile(r"(?<=[。！？!?])\s*")


def presplit_cjk(text: str) -> str:
    """One sentence per blank-line-separated block, so Stanza treats each as a sentence."""
    sents = []
    for para in paragraphs(text):
        sents.extend(s for s in _CJK_SENT_END.split(para) if s.strip())
    return "\n\n".join(sents)


# ---------------------------------------------------------------------------- helpers
def mattr(tokens: list[str], window: int) -> float:
    """Moving-average type-token ratio (Covington & McFall 2010)."""
    n = len(tokens)
    if n == 0:
        return float("nan")
    if n <= window:
        return len(set(tokens)) / n
    counts = Counter(tokens[:window])
    ttrs = [len(counts) / window]
    for i in range(window, n):
        out_tok, in_tok = tokens[i - window], tokens[i]
        counts[out_tok] -= 1
        if counts[out_tok] == 0:
            del counts[out_tok]
        counts[in_tok] += 1
        ttrs.append(len(counts) / window)
    return float(np.mean(ttrs))


def zipf_slope(tokens: list[str]) -> float:
    """Least-squares slope of log(frequency) on log(rank). Near -1 for natural text; flatter = more even use."""
    freqs = sorted(Counter(tokens).values(), reverse=True)
    if len(freqs) < 5:
        return float("nan")
    x = np.log(np.arange(1, len(freqs) + 1))
    y = np.log(np.array(freqs, dtype=float))
    return float(np.polyfit(x, y, 1)[0])


def burstiness(lengths: list[int]) -> float:
    """Goh & Barabási burstiness B = (σ − μ)/(σ + μ) in [-1, 1]; 0 ≈ Poisson, >0 bursty."""
    if len(lengths) < 2:
        return float("nan")
    mu, sd = float(np.mean(lengths)), float(np.std(lengths, ddof=1))
    return (sd - mu) / (sd + mu) if (sd + mu) else float("nan")


def bigram_entropy(text: str) -> float:
    s = re.sub(r"\s+", " ", text.strip())
    if len(s) < 3:
        return float("nan")
    c = Counter(s[i:i + 2] for i in range(len(s) - 1))
    n = sum(c.values())
    return float(-sum((v / n) * math.log2(v / n) for v in c.values()))


def tree_depth(sentence) -> int:
    """Max distance from root over words in a Stanza sentence."""
    heads = {w.id: w.head for w in sentence.words}
    best = 0
    for wid in heads:
        d, cur, seen = 0, wid, set()
        while cur and cur not in seen:
            seen.add(cur)
            cur = heads.get(cur, 0)
            d += 1
        best = max(best, d)
    return best


def paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n|\n", text) if p.strip()]


def is_punct(word) -> bool:
    return word.upos == "PUNCT" or (word.text and all(unicodedata.category(ch).startswith("P") for ch in word.text))


# ---------------------------------------------------------------------------- extraction
def extract(text: str, lang: str, window: int = 50) -> dict:
    """All 21 features + n_tokens / n_sentences for one response."""
    text = unicodedata.normalize("NFC", text)
    doc = pipeline(lang)(presplit_cjk(text) if lang in CJK_LANGS else text)

    sent_lens, depths, subord, connect, first_person, func = [], [], 0, 0, 0, 0
    tokens: list[str] = []
    n_questions = sum(1 for ch in text if ch in QUESTION_CHARS)  # robust to splitter quirks
    for sent in doc.sentences:
        words = [w for w in sent.words if not is_punct(w)]
        if not words:
            continue
        sent_lens.append(len(words))
        depths.append(tree_depth(sent))
        first_content = True
        for w in words:
            tokens.append(w.text.lower())
            rel = (w.deprel or "").split(":")[0]
            if rel in SUBORD_DEPRELS:
                subord += 1
            if rel in CONNECTIVE_DEPRELS or (first_content and w.upos in {"ADV", "CCONJ", "SCONJ"}):
                connect += 1
            if w.upos in FUNCTION_UPOS:
                func += 1
            feats = w.feats or ""
            if "Person=1" in feats or w.text in FIRST_PERSON_LEXICON:
                first_person += 1
            first_content = False

    n_tok = len(tokens)
    n_sent = len(sent_lens)
    per_1k = (lambda c: 1000.0 * c / n_tok) if n_tok else (lambda c: float("nan"))
    counts = Counter(tokens)
    nonspace = [ch for ch in text if not ch.isspace()]
    paras = paragraphs(text)

    return {
        "n_tokens": n_tok, "n_sentences": n_sent,
        # lexical
        "mattr": mattr(tokens, window),
        "hapax_rate": (sum(1 for v in counts.values() if v == 1) / n_tok) if n_tok else float("nan"),
        "mean_token_len": float(np.mean([len(t) for t in tokens])) if tokens else float("nan"),
        "zipf_slope": zipf_slope(tokens),
        # syntactic
        "sent_len_mean": float(np.mean(sent_lens)) if sent_lens else float("nan"),
        "sent_len_sd": float(np.std(sent_lens, ddof=1)) if len(sent_lens) > 1 else float("nan"),
        "burstiness": burstiness(sent_lens),
        "dep_depth": float(np.mean(depths)) if depths else float("nan"),
        "subord_rate": (subord / n_sent) if n_sent else float("nan"),
        "func_word_ratio": (func / n_tok) if n_tok else float("nan"),
        "first_person_rate": per_1k(first_person),
        # structure
        "para_count": len(paras),
        "para_len_mean": (n_tok / len(paras)) if paras else float("nan"),
        "question_rate": (min(n_questions, n_sent) / n_sent) if n_sent else float("nan"),
        "connective_rate": per_1k(connect),
        # punctuation (script equivalents mapped; '--' counted as one dash)
        "comma_per_1k": per_1k(sum(1 for ch in text if ch in COMMA_CHARS)),
        "colon_per_1k": per_1k(sum(1 for ch in text if ch in COLON_CHARS)),
        "dash_per_1k": per_1k(sum(1 for ch in text if ch in DASH_CHARS) + len(_SPACED_HYPHEN.findall(text))
                              + len(re.findall(r"(?<![\s-])--(?![\s-])", text))),
        "semicolon_per_1k": per_1k(sum(1 for ch in text if ch in SEMICOLON_CHARS)),
        # character
        "bigram_entropy": bigram_entropy(text),
        "digit_rate": (1000.0 * sum(1 for ch in nonspace if unicodedata.category(ch) == "Nd") / len(nonspace)) if nonspace else float("nan"),
    }


def build_from(records, out_name: str, keep: set[str] | None = None, extra_cols: tuple[str, ...] = ()) -> pd.DataFrame:
    """Extract features for an iterable of raw-shaped records and write data/features/{out_name}."""
    window = load_config()["features"]["mattr_window"]
    rows = []
    from tqdm import tqdm
    for r in tqdm(list(records), unit="doc"):
        if keep is not None and r["cell_id"] not in keep:
            continue
        if not (r.get("text") or "").strip():
            continue
        feats = extract(r["text"], r["lang"], window)
        rows.append({"cell_id": r["cell_id"], "model_key": r["model_key"], "model_served": r.get("model_served"),
                     "prompt_id": r["prompt_id"], "lang": r["lang"], "gen": r["gen"],
                     "fk_tier": r["fk_tier"], "stance": r["stance"], **{c: r.get(c) for c in extra_cols}, **feats})
    df = pd.DataFrame(rows, columns=META_COLS + list(extra_cols) + FEATURE_NAMES)
    FEATURES_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(FEATURES_DIR / out_name, index=False)
    print(f"wrote {len(df)} rows × {len(FEATURE_NAMES)} features to {FEATURES_DIR / out_name}")
    return df


def build(use_all: bool = False) -> pd.DataFrame:
    keep: set[str] | None = None
    if not use_all:
        vpath = ROOT / "data" / "validation.csv"
        if not vpath.exists():
            raise SystemExit("run python -m langllm.validate first (or pass --all)")
        v = pd.read_csv(vpath)
        keep = set(v.loc[v["keep"], "cell_id"])
    return build_from(iter_raw(), "features.csv", keep)


def build_translated() -> pd.DataFrame:
    from .translate import iter_translated
    return build_from(iter_translated(), "features_translated.csv", None, extra_cols=("translator", "source_cell_id"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--all", action="store_true", help="ignore the validation keep flag")
    ap.add_argument("--translated", action="store_true", help="features for data/translated/*.jsonl instead")
    a = ap.parse_args()
    build_translated() if a.translated else build(use_all=a.all)
