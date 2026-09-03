"""Synthetic features.csv with planted effects, to smoke-test analysis + figures before any
API spend. Model effects shrink with resource rank (so RQ2/RQ4 should come out positive),
languages have large main effects, prompts add block noise.

    python -m langllm.synthetic            # -> data/features/synthetic.csv
    python -m langllm.analysis --features data/features/synthetic.csv
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from .config import load_config, load_schemas, FEATURES_DIR, resource_rank
from .features import FEATURE_NAMES, META_COLS


def make(seed: int = 0, n_per_cell: int | None = None, model_effect: float = 1.2, decay: float = 0.15) -> pd.DataFrame:
    cfg = load_config()
    rng = np.random.default_rng(seed)
    models, langs, schemas = list(cfg["models"]), list(cfg["languages"]), load_schemas()
    n = n_per_cell or cfg["generation"]["n_per_cell"]
    k = len(FEATURE_NAMES)
    lang_mu = {l: rng.normal(0, 2.0, k) for l in langs}
    model_mu = {m: rng.normal(0, model_effect, k) for m in models}
    inter = {(m, l): rng.normal(0, 0.3, k) for m in models for l in langs}
    prompt_mu = {s["id"]: rng.normal(0, 0.5, k) for s in schemas}
    rank = resource_rank(cfg)
    rows = []
    for m in models:
        for l in langs:
            shrink = max(0.0, 1 - decay * (rank[l] - 1))
            for s in schemas:
                for g in range(n):
                    x = lang_mu[l] + shrink * model_mu[m] + inter[(m, l)] + prompt_mu[s["id"]] + rng.normal(0, 1, k)
                    n_tok = int(rng.normal(420, 60))
                    rows.append({"cell_id": f"{m}|{s['id']}|{l}|{g}", "model_key": m, "model_served": cfg["models"][m],
                                 "prompt_id": s["id"], "lang": l, "gen": g, "fk_tier": s["fk_tier"], "stance": s["stance"],
                                 "n_tokens": n_tok, "n_sentences": int(n_tok / 20), **dict(zip(FEATURE_NAMES, x))})
    df = pd.DataFrame(rows, columns=META_COLS + FEATURE_NAMES)
    FEATURES_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(FEATURES_DIR / "synthetic.csv", index=False)
    print(f"wrote {len(df)} synthetic rows to {FEATURES_DIR / 'synthetic.csv'}")
    return df


if __name__ == "__main__":
    make()
