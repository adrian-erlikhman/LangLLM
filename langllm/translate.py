"""Step 7 (extension) — does translation destroy the fingerprint?

Every *kept* English response from the five subject models is translated into the other six
languages by two translators:
  google   Google Translate (public Chrome-extension endpoint; no key; polite rate)
  llm      a free, non-subject, non-Gemini model (config `translators.llm`, with fallbacks)

Output: data/translated/{translator}.jsonl — records shaped like raw responses (so validate /
features work unchanged) plus `source_cell_id`, `translator`, `translator_served`.

    python -m langllm.translate                    # both translators, all targets
    python -m langllm.translate --translator llm --lang ja
"""
from __future__ import annotations
import argparse
import json
import random
import time
import datetime as dt
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import requests
from tqdm import tqdm
from .config import load_config, ROOT, language_codes
from .collect import iter_raw
from .openrouter import chat, text_of, OpenRouterError

TRANS_DIR = ROOT / "data" / "translated"
GOOGLE_CODES = {"es": "es", "zh": "zh-CN", "ru": "ru", "ja": "ja", "tr": "tr", "hi": "hi"}


# ---------------------------------------------------------------------------- Google
def google_translate(text: str, tgt: str, max_retries: int = 6) -> str:
    """Paragraph-wise calls to the public web endpoint, preserving paragraph breaks."""
    out = []
    for para in text.split("\n"):
        if not para.strip():
            out.append("")
            continue
        for attempt in range(max_retries):
            try:
                # the `gtx` client is throttled hard; the Chrome-extension client is not (probed 2026-09-03)
                r = requests.get("https://clients5.google.com/translate_a/t",
                                 params={"client": "dict-chrome-ex", "sl": "en", "tl": GOOGLE_CODES[tgt], "q": para},
                                 headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}, timeout=30)
                if r.status_code == 200:
                    j = r.json()
                    item = j[0] if isinstance(j, list) and j else j
                    out.append(item[0] if isinstance(item, list) else str(item))
                    break
                if r.status_code != 429:
                    r.raise_for_status()
            except (requests.RequestException, ValueError):
                pass
            time.sleep(min(90, 3 * 2 ** attempt + random.random()))
        else:
            raise RuntimeError(f"google translate gave up on paragraph for {tgt}")
        time.sleep(0.8 + random.random())  # be polite; this is an unofficial endpoint
    return "\n".join(out)


# ---------------------------------------------------------------------------- LLM
LLM_PROMPT = ("Translate the following English text into {name}. Produce a faithful, natural translation. "
              "Keep the same paragraph breaks. Output only the translation — no notes, no preamble.\n\n{text}")


def llm_translate(text: str, tgt: str, cfg: dict) -> tuple[str, str]:
    models = [cfg["translators"]["llm"]] + cfg["translators"].get("llm_fallbacks", [])
    name = cfg["languages"][tgt]["name_en"]
    last = None
    for m in models:
        try:
            r = chat(m, [{"role": "user", "content": LLM_PROMPT.format(name=name, text=text)}],
                     temperature=0.0, max_tokens=4000, reasoning={"enabled": False}, max_retries=3)
            t = text_of(r)
            if t and r["choices"][0].get("finish_reason") != "length":
                return t, r.get("model") or m
            last = f"{m}: empty/truncated"
        except OpenRouterError as e:
            last = f"{m}: {str(e)[:120]}"
    raise RuntimeError(f"all translators failed: {last}")


# ---------------------------------------------------------------------------- driver
def english_sources() -> list[dict]:
    v = pd.read_csv(ROOT / "data" / "validation.csv")
    keep = set(v.loc[v["keep"], "cell_id"])
    return [r for r in iter_raw() if r["lang"] == "en" and r["cell_id"] in keep]


def out_path(translator: str):
    return TRANS_DIR / f"{translator}.jsonl"


def done_ids(translator: str) -> set[str]:
    p = out_path(translator)
    if not p.exists():
        return set()
    return {json.loads(l)["cell_id"] for l in open(p, encoding="utf-8") if l.strip()}


def make_record(src: dict, tgt: str, translator: str, text: str, served: str | None) -> dict:
    return {**{k: src[k] for k in ("model_key", "model", "prompt_id", "gen", "fk_tier", "stance")},
            "cell_id": f"{src['model_key']}|{src['prompt_id']}|{tgt}|{src['gen']}|{translator}",
            "source_cell_id": src["cell_id"], "lang": tgt, "translator": translator, "translator_served": served,
            "model_served": src.get("model_served"), "text": text, "finish_reason": "translated", "error": None,
            "usage": {}, "translated_at": dt.datetime.now(dt.timezone.utc).isoformat()}


def run(translators: list[str], langs: list[str], workers: int) -> None:
    cfg = load_config()
    srcs = english_sources()
    TRANS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"{len(srcs)} kept English sources → {langs} × {translators}")
    for tr in translators:
        done = done_ids(tr)
        jobs = [(s, t) for s in srcs for t in langs if f"{s['model_key']}|{s['prompt_id']}|{t}|{s['gen']}|{tr}" not in done]
        print(f"[{tr}] {len(jobs)} translations to do")
        if not jobs:
            continue

        def work(job):
            s, t = job
            try:
                if tr == "google":
                    return make_record(s, t, tr, google_translate(s["text"], t), "google-translate-web")
                text, served = llm_translate(s["text"], t, cfg)
                return make_record(s, t, tr, text, served)
            except Exception as e:  # noqa: BLE001 — record and move on; rerun picks it up
                rec = make_record(s, t, tr, "", None)
                rec.update({"finish_reason": "error", "error": str(e)[:500]})
                return rec

        w = 1 if tr == "google" else workers
        with ThreadPoolExecutor(max_workers=w) as ex, open(out_path(tr), "a", encoding="utf-8") as f:
            for fut in tqdm(as_completed([ex.submit(work, j) for j in jobs]), total=len(jobs), unit="tr"):
                rec = fut.result()
                if rec["error"]:
                    print("  error:", rec["cell_id"], rec["error"][:100])
                    continue  # not written → retried next run
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()


def iter_translated(translators: list[str] | None = None):
    for p in sorted(TRANS_DIR.glob("*.jsonl")):
        if translators and p.stem not in translators:
            continue
        for line in open(p, encoding="utf-8"):
            if line.strip():
                yield json.loads(line)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--translator", nargs="*", default=["llm", "google"])
    ap.add_argument("--lang", nargs="*")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    run(a.translator, a.lang or [l for l in language_codes() if l != "en"], a.workers)


if __name__ == "__main__":
    main()
