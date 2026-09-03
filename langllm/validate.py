"""Step 3 — language ID, length check and refusal detection for every raw response.

Writes data/validation.csv (one row per cell, with a `keep` flag) and
results/validation_summary.csv (wrong-language and refusal rates per model × language).

    python -m langllm.validate
"""
from __future__ import annotations
import re
import unicodedata
import pandas as pd
from .config import load_config, ROOT, RESULTS_DIR
from .collect import iter_raw

# --- language identification -------------------------------------------------------
_LINGUA = None


def _lingua(codes: list[str]):
    global _LINGUA
    if _LINGUA is None:
        from lingua import Language, LanguageDetectorBuilder
        by_iso = {l.iso_code_639_1.name.lower(): l for l in Language.all()}
        langs = [by_iso[c] for c in codes]
        _LINGUA = LanguageDetectorBuilder.from_languages(*langs).with_preloaded_language_models().build()
    return _LINGUA


def detect_language(text: str, codes: list[str]) -> tuple[str | None, float]:
    """Return (iso639-1 code, confidence) restricted to the study's languages."""
    if not text.strip():
        return None, 0.0
    det = _lingua(codes)
    vals = det.compute_language_confidence_values(text)
    if not vals:
        return None, 0.0
    top = vals[0]
    return top.language.iso_code_639_1.name.lower(), float(top.value)


# --- length --------------------------------------------------------------------------
_CJK = re.compile(r"[぀-ヿ㐀-䶿一-鿿豈-﫿]")


def word_equivalent(text: str, lang: str) -> int:
    """Approximate word count. zh/ja have no spaces: 1 word ≈ 1.6 Chinese chars / 2.2 Japanese chars
    (empirical ratios; the Stanza token count in features.py is the precise one)."""
    if lang == "zh":
        return round(len(_CJK.findall(text)) / 1.6)
    if lang == "ja":
        return round(len(_CJK.findall(text)) / 2.2)
    return len(re.findall(r"\S+", text))


# --- refusal -------------------------------------------------------------------------
REFUSAL_PATTERNS = {
    "en": r"\b(I can(?:'|no)t|I(?:'m| am) (?:not able|unable) to|I won(?:'|no)t|As an AI|I'm sorry, but)\b",
    "es": r"\b(no puedo|lo siento, pero|no me es posible|como (?:una )?IA)\b",
    "zh": r"(我无法|我不能|抱歉，我|作为(?:一个)?(?:AI|人工智能))",
    "ru": r"\b(я не могу|извините, но|как (?:ИИ|искусственный интеллект))",
    "ja": r"(できません|申し訳ありません|AIとして)",
    "tr": r"\b(yapamam|üzgünüm, ama|bir yapay zeka olarak)\b",
    "hi": r"(नहीं कर सकत|क्षमा करें|एक एआई के रूप में)",
}
STRUCTURE_PATTERNS = r"^\s*(#{1,6}\s|[-*•]\s|\d+[.)]\s)"  # headings / bullets / numbered lists


def looks_like_refusal(text: str, lang: str, wc: int) -> bool:
    if wc < 60:
        return True
    head = text[:400]
    pat = REFUSAL_PATTERNS.get(lang)
    return bool(pat and re.search(pat, head, flags=re.I))


def structure_violations(text: str) -> int:
    return sum(1 for line in text.splitlines() if re.match(STRUCTURE_PATTERNS, line))


def validate() -> pd.DataFrame:
    cfg = load_config()
    vcfg = cfg["validation"]
    codes = list(cfg["languages"])
    rows = []
    for r in iter_raw():
        text = unicodedata.normalize("NFC", r.get("text") or "")
        wc = word_equivalent(text, r["lang"])
        det, conf = detect_language(text, codes) if text else (None, 0.0)
        truncated = r.get("finish_reason") == "length"
        # empty/short output that hit the token budget is reasoning overflow, not a refusal
        refusal = looks_like_refusal(text, r["lang"], wc) if not (r.get("error") or (truncated and wc < 60)) else False
        wrong_lang = bool(text) and (det != r["lang"] or conf < vcfg["langid_min_confidence"])
        too_short, too_long = wc < vcfg["min_words"], wc > vcfg["max_words"]
        rows.append({
            "cell_id": r["cell_id"], "model_key": r["model_key"], "model_served": r.get("model_served"),
            "prompt_id": r["prompt_id"], "lang": r["lang"], "gen": r["gen"], "fk_tier": r["fk_tier"],
            "error": bool(r.get("error")), "finish_reason": r.get("finish_reason"),
            "truncated": truncated,
            "reasoning_tokens": (r.get("usage") or {}).get("reasoning_tokens"),
            "word_equiv": wc, "lang_detected": det, "lang_conf": round(conf, 3),
            "wrong_language": wrong_lang, "refusal": refusal, "too_short": too_short, "too_long": too_long,
            "structure_lines": structure_violations(text),
            "keep": not (r.get("error") or wrong_lang or refusal or too_short or too_long or truncated),
        })
    df = pd.DataFrame(rows)
    (ROOT / "data").mkdir(exist_ok=True)
    df.to_csv(ROOT / "data" / "validation.csv", index=False)
    if df.empty:
        print("no raw responses found")
        return df
    RESULTS_DIR.mkdir(exist_ok=True)
    summ = (df.groupby(["model_key", "lang"])
              .agg(n=("cell_id", "size"), wrong_language_rate=("wrong_language", "mean"),
                   refusal_rate=("refusal", "mean"), error_rate=("error", "mean"), truncated_rate=("truncated", "mean"),
                   too_short_rate=("too_short", "mean"), too_long_rate=("too_long", "mean"),
                   keep_rate=("keep", "mean"), median_words=("word_equiv", "median"))
              .reset_index())
    summ.to_csv(RESULTS_DIR / "validation_summary.csv", index=False)
    print(summ.to_string(index=False))
    print(f"\nkept {int(df['keep'].sum())} / {len(df)} responses")
    return df


if __name__ == "__main__":
    validate()
