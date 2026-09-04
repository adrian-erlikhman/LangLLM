"""RQ6 — LLM-as-judge attribution and self-recognition (continuation of the CompLLM protocol).

Each of the five subject models is shown one kept response, with no metadata, and asked which
of the five models wrote it. Option order is shuffled per text (seeded by cell id) so no judge
sees a fixed position. Scored two ways:
  attribution      five-way accuracy per judge × language (chance 0.20)
  self-recognition own-text recall vs the rate at which the judge names itself on others' text

Judges run cheapest-first so a credit shortfall costs tail data, not Claude. Resumable.

    python -m langllm.judge                 # judge all kept originals with all five judges
    python -m langllm.judge --judge claude  # one judge
    python -m langllm.judge --analyse       # results/rq6_*.csv + figure F10
"""
from __future__ import annotations
import argparse
import json
import random
import datetime as dt
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
import pandas as pd
import requests
from scipy import stats
from tqdm import tqdm
from .config import load_config, ROOT, RESULTS_DIR, FIG_DIR, resource_rank, language_codes
from .collect import iter_raw
from .openrouter import chat, text_of, usage_of, api_key, OpenRouterError

JUDGE_DIR = ROOT / "data" / "judge"
JUDGE_ORDER = ["deepseek", "grok", "gemini", "claude", "gpt"]  # cheap → expensive
LABEL = {"claude": "Claude (Anthropic)", "deepseek": "DeepSeek", "gemini": "Gemini (Google)", "gpt": "GPT (OpenAI)", "grok": "Grok (xAI)"}
PROMPT = """The essay below was written by one of five AI language models. Read it and decide which model wrote it.

The five candidates are:
{options}

Base your decision on the writing itself. Answer with exactly one candidate key from this list and nothing else: {keys}.

Essay:
<<<
{text}
>>>"""


def options_for(cell_id: str) -> list[str]:
    keys = sorted(LABEL)
    random.Random(cell_id).shuffle(keys)
    return keys


def parse_answer(text: str, keys: list[str]) -> str | None:
    t = (text or "").strip().lower()
    hits = [(t.find(k), k) for k in keys if k in t]
    if not hits:
        aliases = {"anthropic": "claude", "openai": "gpt", "chatgpt": "gpt", "google": "gemini", "xai": "grok", "x.ai": "grok"}
        hits = [(t.find(a), k) for a, k in aliases.items() if a in t]
    return min(hits)[1] if hits else None


def kept_originals() -> list[dict]:
    v = pd.read_csv(ROOT / "data" / "validation.csv")
    keep = set(v.loc[v["keep"], "cell_id"])
    return [r for r in iter_raw() if r["cell_id"] in keep]


def out_path(judge: str):
    return JUDGE_DIR / f"{judge}.jsonl"


def done_ids(judge: str) -> set[str]:
    p = out_path(judge)
    return {json.loads(l)["cell_id"] for l in open(p, encoding="utf-8") if l.strip()} if p.exists() else set()


def credits_remaining() -> float | None:
    try:
        d = requests.get("https://openrouter.ai/api/v1/credits", headers={"Authorization": f"Bearer {api_key()}"}, timeout=20).json()["data"]
        return float(d["total_credits"]) - float(d["total_usage"])
    except Exception:  # noqa: BLE001
        return None


def judge_one(judge: str, model: str, r: dict, gcfg: dict) -> dict:
    keys = options_for(r["cell_id"])
    prompt = PROMPT.format(options="\n".join(f"- {k}: {LABEL[k]}" for k in keys), keys=", ".join(keys), text=r["text"])
    rec = {"cell_id": r["cell_id"], "judge": judge, "judge_model": model, "author": r["model_key"], "lang": r["lang"],
           "prompt_id": r["prompt_id"], "gen": r["gen"], "option_order": keys, "judged_at": dt.datetime.now(dt.timezone.utc).isoformat()}
    try:
        resp = chat(model, [{"role": "user", "content": prompt}], temperature=0.0, max_tokens=800,
                    reasoning=gcfg.get("reasoning"), seed=7, max_retries=4)
        raw = text_of(resp)
        rec.update({"raw": raw[:300], "answer": parse_answer(raw, keys), "judge_served": resp.get("model"),
                    "finish_reason": resp["choices"][0].get("finish_reason"), "usage": usage_of(resp), "error": None})
    except OpenRouterError as e:
        rec.update({"raw": "", "answer": None, "judge_served": None, "finish_reason": "error", "usage": {}, "error": str(e)[:300]})
    return rec


def run(judges: list[str], workers: int = 6, min_credit: float = 0.75) -> None:
    cfg = load_config()
    gcfg = cfg["generation"]
    srcs = kept_originals()
    JUDGE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"{len(srcs)} kept originals; judges in order: {judges}")
    for j in judges:
        done = done_ids(j)
        todo = [r for r in srcs if r["cell_id"] not in done]
        rem = credits_remaining()
        print(f"[{j}] {len(todo)} to judge; credit remaining: {rem if rem is None else round(rem, 2)}")
        if not todo:
            continue
        if rem is not None and rem < min_credit:
            print(f"[{j}] stopping: credit below {min_credit}")
            break
        n_err = 0
        with ThreadPoolExecutor(max_workers=workers) as ex, open(out_path(j), "a", encoding="utf-8") as f:
            futs = [ex.submit(judge_one, j, cfg["models"][j], r, gcfg) for r in todo]
            for fut in tqdm(as_completed(futs), total=len(futs), unit="judge"):
                rec = fut.result()
                if rec["error"]:
                    n_err += 1
                    continue  # not written → retried next run
                f.write(json.dumps(rec, ensure_ascii=False) + "\n"); f.flush()
        print(f"[{j}] done, {n_err} errors")


# ---------------------------------------------------------------------------- analysis
def load_judgements() -> pd.DataFrame:
    rows = []
    for p in sorted(JUDGE_DIR.glob("*.jsonl")):
        rows += [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]
    df = pd.DataFrame(rows)
    df["correct"] = (df["answer"] == df["author"]).astype(float)
    df["names_self"] = (df["answer"] == df["judge"]).astype(float)
    df["is_own"] = (df["author"] == df["judge"])
    df["unparsed"] = df["answer"].isna()
    return df


def analyse() -> None:
    cfg = load_config()
    rank = resource_rank(cfg)
    langs = language_codes(cfg)
    df = load_judgements()
    RESULTS_DIR.mkdir(exist_ok=True)
    rows = []
    for (j, l), d in df.groupby(["judge", "lang"]):
        n = len(d); k = int(d["correct"].sum())
        lo, hi = stats.binomtest(k, n).proportion_ci(0.95)
        own = d[d.is_own]; oth = d[~d.is_own]
        rows.append({"judge": j, "lang": l, "rank": rank[l], "n": n, "accuracy": k / n, "ci_lo": lo, "ci_hi": hi,
                     "p_vs_chance": stats.binomtest(k, n, 0.2, alternative="greater").pvalue,
                     "own_recall": own["correct"].mean() if len(own) else np.nan, "n_own": len(own),
                     "false_self_rate": oth["names_self"].mean() if len(oth) else np.nan,
                     "self_claim_rate": d["names_self"].mean(), "unparsed_rate": d["unparsed"].mean()})
    per = pd.DataFrame(rows).sort_values(["judge", "rank"])
    per.to_csv(RESULTS_DIR / "rq6_judge_by_language.csv", index=False)

    # per-judge overall + self-recognition test: own recall vs false-self rate (Fisher exact)
    srows = []
    for j, d in df.groupby("judge"):
        own = d[d.is_own]; oth = d[~d.is_own]
        a, b = int(own["correct"].sum()), int(len(own) - own["correct"].sum())
        c, e = int(oth["names_self"].sum()), int(len(oth) - oth["names_self"].sum())
        _, p_fisher = stats.fisher_exact([[a, b], [c, e]], alternative="greater")
        k, n = int(d["correct"].sum()), len(d)
        srows.append({"judge": j, "n": n, "accuracy": k / n, "p_vs_chance": stats.binomtest(k, n, 0.2, alternative="greater").pvalue,
                      "own_recall": a / max(1, a + b), "false_self_rate": c / max(1, c + e),
                      "self_recognition_p_fisher": p_fisher, "self_claim_rate": d["names_self"].mean(), "unparsed_rate": d["unparsed"].mean()})
    summ = pd.DataFrame(srows).sort_values("accuracy", ascending=False)
    summ.to_csv(RESULTS_DIR / "rq6_judge_summary.csv", index=False)

    # confusion per judge (who they think wrote what)
    for j, d in df.groupby("judge"):
        pd.crosstab(d["author"], d["answer"].fillna("none")).to_csv(RESULTS_DIR / f"rq6_confusion_{j}.csv")

    # comparison with the feature classifier
    acc = pd.read_csv(RESULTS_DIR / "rq1_accuracy.csv")
    feat = acc[acc.classifier == "logreg"].set_index("lang")["accuracy"]
    comp = per.pivot(index="lang", columns="judge", values="accuracy").loc[langs]
    comp["feature_classifier"] = feat.loc[langs]
    comp.to_csv(RESULTS_DIR / "rq6_judge_vs_features.csv")
    print(summ.round(3).to_string(index=False)); print(); print(comp.round(3).to_string())

    # ---- figure F10
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from .figures import MODEL_COLORS
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    ax = axes[0]
    for j in JUDGE_ORDER:
        if j in comp.columns:
            ax.plot([rank[l] for l in langs], comp[j], "o-", color=MODEL_COLORS[j], label=f"{j} as judge")
    ax.plot([rank[l] for l in langs], comp["feature_classifier"], "s--", color="k", label="feature classifier (RQ1)")
    ax.axhline(0.2, ls=":", c="k", lw=0.8); ax.set_ylim(0, 1); ax.set_xticks(range(1, 8), langs)
    ax.set_xlabel("language (resource rank)"); ax.set_ylabel("five-way attribution accuracy"); ax.legend(frameon=False, fontsize=7)
    ax.set_title("Who can tell the models apart?", fontsize=10)
    ax = axes[1]
    x = np.arange(len(summ)); w = 0.38
    ax.bar(x - w / 2, summ["own_recall"], w, color=[MODEL_COLORS[j] for j in summ["judge"]], label="recall on own text")
    ax.bar(x + w / 2, summ["false_self_rate"], w, color=[MODEL_COLORS[j] for j in summ["judge"]], alpha=0.4, label="names itself on others' text")
    ax.axhline(0.2, ls=":", c="k", lw=0.8); ax.set_xticks(x, summ["judge"]); ax.set_ylim(0, 1)
    ax.set_title("Self-recognition (all languages pooled)", fontsize=10); ax.legend(frameon=False, fontsize=7)
    fig.suptitle("RQ6 — LLM-as-judge attribution and self-recognition", fontsize=10); fig.tight_layout()
    FIG_DIR.mkdir(parents=True, exist_ok=True); fig.savefig(FIG_DIR / "F10_rq6_judge.png", dpi=200); plt.close(fig)
    print("wrote", FIG_DIR / "F10_rq6_judge.png")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--judge", nargs="*", help="judge keys (default: all, cheapest first)")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--analyse", action="store_true")
    a = ap.parse_args()
    if a.analyse:
        analyse()
    else:
        run(a.judge or JUDGE_ORDER, a.workers)


if __name__ == "__main__":
    main()
