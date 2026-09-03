"""Step 2 — collect 5 models × 12 prompts × 7 languages × 2 generations = 840 responses.

Each response is one JSONL line in data/raw/{model_key}.jsonl with the *served* model string,
usage, finish_reason and provider. Runs are resumable: existing (model, prompt, lang, gen)
cells are skipped. The subject model sees only the native prompt as a single user turn —
no system prompt — so nothing but the prompt language differs across cells.

    python -m langllm.collect                       # everything missing
    python -m langllm.collect --model gpt --lang en # one cell block
    python -m langllm.collect --dry-run             # count + cost estimate only
"""
from __future__ import annotations
import argparse
import json
import datetime as dt
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from .config import load_config, load_schemas, RAW_DIR, language_codes
from .openrouter import chat, text_of, usage_of, OpenRouterError
from .prompts import load_native


def cell_id(model_key: str, pid: str, lang: str, gen: int) -> str:
    return f"{model_key}|{pid}|{lang}|{gen}"


def raw_path(model_key: str):
    return RAW_DIR / f"{model_key}.jsonl"


def load_done(model_key: str) -> set[str]:
    p = raw_path(model_key)
    if not p.exists():
        return set()
    done = set()
    with open(p, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                done.add(json.loads(line)["cell_id"])
    return done


def iter_raw(model_keys: list[str] | None = None):
    """Yield every stored response dict across models."""
    for p in sorted(RAW_DIR.glob("*.jsonl")):
        if model_keys and p.stem not in model_keys:
            continue
        with open(p, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    yield json.loads(line)


def plan(cfg: dict, models: list[str], langs: list[str]) -> list[dict]:
    schemas = load_schemas()
    n = cfg["generation"]["n_per_cell"]
    jobs = []
    for mk in models:
        done = load_done(mk)
        for lang in langs:
            native = load_native(lang)
            for s in schemas:
                if s["id"] not in native:
                    raise SystemExit(f"missing native prompt {s['id']} for {lang}: run python -m langllm.prompts")
                for g in range(n):
                    cid = cell_id(mk, s["id"], lang, g)
                    if cid not in done:
                        jobs.append({"cell_id": cid, "model_key": mk, "model": cfg["models"][mk],
                                     "prompt_id": s["id"], "lang": lang, "gen": g,
                                     "prompt": native[s["id"]]["prompt"], "fk_tier": s["fk_tier"],
                                     "stance": s["stance"]})
    return jobs


def run_job(job: dict, gcfg: dict) -> dict:
    messages = [{"role": "user", "content": job["prompt"]}]
    rec = {k: job[k] for k in ("cell_id", "model_key", "model", "prompt_id", "lang", "gen", "fk_tier", "stance")}
    rec["requested_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
    rec["params"] = {"temperature": gcfg["temperature"], "max_tokens": gcfg["max_tokens"],
                     "reasoning": gcfg.get("reasoning"), "seed": 1000 + job["gen"]}
    try:
        resp = chat(job["model"], messages, temperature=gcfg["temperature"], max_tokens=gcfg["max_tokens"],
                    reasoning=gcfg.get("reasoning"), seed=1000 + job["gen"], max_retries=gcfg["max_retries"])
        ch = resp["choices"][0]
        rec.update({
            "text": text_of(resp), "model_served": resp.get("model"), "provider": resp.get("provider"),
            "finish_reason": ch.get("finish_reason"), "native_finish_reason": ch.get("native_finish_reason"),
            "usage": usage_of(resp), "response_id": resp.get("id"), "error": None,
        })
    except OpenRouterError as e:
        rec.update({"text": "", "model_served": None, "provider": None, "finish_reason": "error",
                    "native_finish_reason": None, "usage": {}, "response_id": None, "error": str(e)[:1000]})
    return rec


def collect(models: list[str], langs: list[str], dry_run: bool = False, workers: int | None = None,
            max_tokens: int | None = None) -> None:
    cfg = load_config()
    gcfg = dict(cfg["generation"])
    if max_tokens:  # re-runs after reasoning overflow; the override is recorded in each record's params
        gcfg["max_tokens"] = max_tokens
    jobs = plan(cfg, models, langs)
    total = len(cfg["models"]) * len(load_schemas()) * len(cfg["languages"]) * gcfg["n_per_cell"]
    print(f"{len(jobs)} cells to collect (study total {total}); models={models} langs={langs}")
    if dry_run or not jobs:
        # rough cost: ~350 prompt tokens in, ~700 out; multilingual tokenisation inflates zh/ja/hi
        print("dry run: nothing sent. Expect on the order of 1k tokens per cell; see OpenRouter pricing per model.")
        return
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    by_model: dict[str, list[dict]] = {}
    with ThreadPoolExecutor(max_workers=workers or gcfg["workers"]) as ex:
        futs = {ex.submit(run_job, j, gcfg): j for j in jobs}
        for fut in tqdm(as_completed(futs), total=len(futs), unit="resp"):
            rec = fut.result()
            with open(raw_path(rec["model_key"]), "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            by_model.setdefault(rec["model_key"], []).append(rec)
    for mk, recs in by_model.items():
        errs = sum(1 for r in recs if r["error"])
        print(f"{mk}: {len(recs)} written, {errs} errors (errors are re-tried on the next run: delete the line first)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", nargs="*", help="model keys from config.yaml (default: all)")
    ap.add_argument("--lang", nargs="*", help="language codes (default: all)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--workers", type=int)
    ap.add_argument("--max-tokens", type=int, help="override generation.max_tokens (e.g. after reasoning overflow)")
    a = ap.parse_args()
    cfg = load_config()
    collect(a.model or list(cfg["models"]), a.lang or language_codes(cfg), dry_run=a.dry_run, workers=a.workers,
            max_tokens=a.max_tokens)


if __name__ == "__main__":
    main()
