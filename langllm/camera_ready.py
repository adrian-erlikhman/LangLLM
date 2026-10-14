"""Camera-ready analyses for the IEEE BigData 2026 HSS reviews (SP19343, Oct 2026).

C1  Equal tuning (reviewer 2, point 1). The paper's comparison used C = 1 for both the 21
    features and the character n-grams, fixed in the analysis plan. Here the logistic-regression
    C is chosen by nested leave-one-prompt-out CV for BOTH representations from the same grid
    with the same inner folds. Feature standardisation and the TF-IDF vocabulary/IDF are fit on
    the training prompts only, inside every inner and outer fold.
C2  Prompt-level tests (reviewer 2, point 3). Texts from one prompt are related, so every
    headline test is redone on the 12 per-prompt accuracies with an exact sign-flip permutation
    test (4,096 sign assignments): the 28 Holm-corrected comparisons, the LLM judges, all 42
    off-diagonal transfer cells for features and adapted n-grams, and prompt-clustered intervals
    for attribution on machine translations.
C4  RQ4 separation intervals that resample prompts rather than texts (reviewer 2, point 3).
C3  Fragility (reviewer 2, point 4). The prompts carry a reading-level instruction (4 general,
    4 educated, 4 expert). Leave-one-reading-level-out trains on two levels and tests on the
    third, so the test texts answer an instruction the classifier never saw. Also: the 21
    features minus the two paragraph features, which a format instruction could change directly.

    python -m langllm.camera_ready            # all three -> results/cr_*.csv / cr_*.json
    python -m langllm.camera_ready --only c2  # one part
"""
from __future__ import annotations
import argparse
import itertools
import json
import warnings
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.multitest import multipletests
from .config import load_config, resource_rank, language_codes, RESULTS_DIR, FEATURES_DIR
from .features import FEATURE_NAMES
from .analysis import load_features, zscore_within_language, CHANCE
from .baselines import kept_texts, _vec, RS

warnings.filterwarnings("ignore")
GRID = [0.01, 0.1, 1.0, 10.0, 100.0]
NB = 2000
PARA = ["para_count", "para_len_mean"]


# ---------------------------------------------------------------------------- helpers
def _signs(k: int) -> np.ndarray:
    return np.array(list(itertools.product([1.0, -1.0], repeat=k)))


def signflip_p(diffs, alternative: str = "two-sided") -> float:
    """Exact sign-flip permutation p for H0: per-prompt differences symmetric about 0."""
    d = np.asarray(diffs, float)
    S = _signs(len(d)); obs = d.mean(); null = (S * d).mean(axis=1)
    if alternative == "greater":
        return float((null >= obs - 1e-12).mean())
    return float((np.abs(null) >= abs(obs) - 1e-12).mean())


def per_prompt(correct: np.ndarray, prompts: np.ndarray) -> pd.Series:
    return pd.Series(correct, dtype=float).groupby(np.asarray(prompts)).mean()


def cluster_ci(correct: np.ndarray, prompts: np.ndarray, rng: np.random.Generator) -> tuple[float, float]:
    G = np.unique(prompts); by = {g: correct[prompts == g] for g in G}
    vals = [np.concatenate([by[g] for g in rng.choice(G, len(G), replace=True)]).mean() for _ in range(NB)]
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def _pick(scores: dict[float, float]) -> float:
    """Best inner accuracy; ties go to the C closest to 1 (the pre-specified value), then the smaller C."""
    best = max(scores.values())
    return sorted([c for c, s in scores.items() if s >= best - 1e-12], key=lambda c: (abs(np.log10(c)), c))[0]


def _lr(C: float) -> LogisticRegression:
    return LogisticRegression(C=C, max_iter=5000, random_state=RS)


# ---------------------------------------------------------------------------- C1 equal tuning
def _nested_features(X, y, g):
    pred = np.empty(len(y), dtype=object); chosen = []
    for p in sorted(set(g)):
        tr = g != p; inner = {c: 0 for c in GRID}
        for q in sorted(set(g[tr])):
            itr, ite = tr & (g != q), g == q
            for c in GRID:
                inner[c] += int((make_pipeline(StandardScaler(), _lr(c)).fit(X[itr], y[itr]).predict(X[ite]) == y[ite]).sum())
        c = _pick(inner); chosen.append(c)
        pred[g == p] = make_pipeline(StandardScaler(), _lr(c)).fit(X[tr], y[tr]).predict(X[g == p])
    return pred, chosen


def _nested_ngrams(T, y, g):
    pred = np.empty(len(y), dtype=object); chosen = []
    for p in sorted(set(g)):
        tr = g != p; inner = {c: 0 for c in GRID}
        for q in sorted(set(g[tr])):
            itr, ite = tr & (g != q), g == q
            vec = _vec("char"); Xi = vec.fit_transform(T[itr]); Xq = vec.transform(T[ite])
            for c in GRID:
                inner[c] += int((_lr(c).fit(Xi, y[itr]).predict(Xq) == y[ite]).sum())
        c = _pick(inner); chosen.append(c)
        vec = _vec("char"); Xtr = vec.fit_transform(T[tr])
        pred[g == p] = _lr(c).fit(Xtr, y[tr]).predict(vec.transform(T[g == p]))
    return pred, chosen


def _c1_lang(lang, feat_d, text_d):
    X, y, g = feat_d[FEATURE_NAMES].to_numpy(float), feat_d["model_key"].to_numpy(), feat_d["prompt_id"].to_numpy()
    pf, cf = _nested_features(X, y, g)
    t = text_d.set_index("cell_id").loc[feat_d["cell_id"]]  # same texts, same order
    pn, cn = _nested_ngrams(t["text"].to_numpy(), t["model_key"].to_numpy(), t["prompt_id"].to_numpy())
    print(f"[C1] {lang}: features {np.mean(pf == y):.3f} (C {sorted(set(cf))}), n-grams {np.mean(pn == y):.3f} (C {sorted(set(cn))})", flush=True)
    cells = pd.DataFrame({"cell_id": feat_d["cell_id"].to_numpy(), "lang": lang, "prompt_id": g,
                          "feat_correct": (pf == y).astype(int), "ngram_correct": (pn == y).astype(int)})
    return cells, {"lang": lang, "features_C": cf, "ngram_C": cn}


def c1_equal_tuning(cfg: dict, feat: pd.DataFrame, texts: pd.DataFrame) -> pd.DataFrame:
    langs = language_codes(cfg); rank = resource_rank(cfg)
    out = Parallel(n_jobs=2)(delayed(_c1_lang)(l, feat[feat.lang == l], texts[texts.lang == l]) for l in langs)
    cells = pd.concat([o[0] for o in out]); cells.to_csv(RESULTS_DIR / "cr_tuned_cell_correct.csv", index=False)
    rng = np.random.default_rng(RS); rows = []
    for l in langs:
        d = cells[cells.lang == l]; P = d["prompt_id"].to_numpy()
        fl, fh = cluster_ci(d["feat_correct"].to_numpy(float), P, rng); nl, nh = cluster_ci(d["ngram_correct"].to_numpy(float), P, rng)
        diff = per_prompt(d["ngram_correct"].to_numpy(), P) - per_prompt(d["feat_correct"].to_numpy(), P)
        rows.append({"lang": l, "rank": rank[l], "n": len(d), "features_tuned": d["feat_correct"].mean(), "features_ci_lo": fl, "features_ci_hi": fh,
                     "ngram_tuned": d["ngram_correct"].mean(), "ngram_ci_lo": nl, "ngram_ci_hi": nh,
                     "gap_pts": 100 * (d["ngram_correct"].mean() - d["feat_correct"].mean()), "gap_p_signflip": signflip_p(diff.to_numpy())})
    res = pd.DataFrame(rows).sort_values("rank")
    res["gap_p_holm7"] = multipletests(res["gap_p_signflip"], method="holm")[1]
    res.to_csv(RESULTS_DIR / "cr_tuned_accuracy.csv", index=False)
    json.dump({o[1]["lang"]: {"features_C": o[1]["features_C"], "ngram_C": o[1]["ngram_C"]} for o in out},
              open(RESULTS_DIR / "cr_tuned_chosen_C.json", "w"), indent=1)
    return res


# ---------------------------------------------------------------------------- C2 prompt-level tests
def _best_judge(cfg) -> dict[str, str]:
    per = pd.read_csv(RESULTS_DIR / "rq6_judge_by_language.csv")
    return per.sort_values("accuracy", ascending=False).groupby("lang").head(1).set_index("lang")["judge"].to_dict()


def c2_prompt_tests(cfg: dict, feat: pd.DataFrame, texts: pd.DataFrame) -> dict:
    from .judge import load_judgements
    langs = language_codes(cfg)
    fc = pd.read_csv(RESULTS_DIR / "rq1_cell_correct.csv").set_index("cell_id")
    ng = pd.read_csv(RESULTS_DIR / "rq7_ngram_cell_correct.csv"); ng = ng[ng.baseline == "char_ngram"].set_index("cell_id")
    jd = load_judgements(); best = _best_judge(cfg)
    rows = []
    for l in langs:
        f = fc[fc.lang == l]; P = f["prompt_id"]
        a_f = per_prompt(f["correct"].to_numpy(), P.to_numpy())
        a_n = per_prompt(ng.loc[f.index, "correct"].to_numpy(), P.to_numpy())
        j = jd[(jd.lang == l) & (jd.judge == best[l])].set_index("cell_id").loc[f.index]
        a_j = per_prompt(j["correct"].to_numpy(), P.to_numpy())
        rows += [{"family": "features vs chance", "lang": l, "effect": a_f.mean() - CHANCE, "p_raw": signflip_p((a_f - CHANCE).to_numpy(), "greater"),
                  "prompts_favouring": int((a_f > CHANCE).sum())},
                 {"family": "char n-gram vs chance", "lang": l, "effect": a_n.mean() - CHANCE, "p_raw": signflip_p((a_n - CHANCE).to_numpy(), "greater"),
                  "prompts_favouring": int((a_n > CHANCE).sum())},
                 {"family": "features vs char n-gram", "lang": l, "effect": a_f.mean() - a_n.mean(), "p_raw": signflip_p((a_f - a_n).to_numpy()),
                  "prompts_favouring": int((a_n > a_f).sum())},
                 {"family": f"features vs best judge ({best[l]})", "lang": l, "effect": a_f.mean() - a_j.mean(), "p_raw": signflip_p((a_f - a_j).to_numpy()),
                  "prompts_favouring": int((a_f > a_j).sum())}]
    h = pd.DataFrame(rows)
    rej, ph, _, _ = multipletests(h["p_raw"], alpha=0.05, method="holm"); h["p_holm"] = ph; h["significant_holm_05"] = rej
    h.to_csv(RESULTS_DIR / "cr_holm_prompt_level.csv", index=False)

    # judges, pooled over languages, per-prompt
    jrows = []
    for jn, d in jd.groupby("judge"):
        acc = per_prompt(d["correct"].to_numpy(), d["prompt_id"].to_numpy())
        own = d[d.is_own]; oth = d[~d.is_own]
        diff = per_prompt(own["correct"].to_numpy(), own["prompt_id"].to_numpy()) - per_prompt(oth["names_self"].to_numpy(), oth["prompt_id"].to_numpy())
        jrows.append({"judge": jn, "accuracy": d["correct"].mean(), "p_vs_chance_signflip": signflip_p((acc - CHANCE).to_numpy(), "greater"),
                      "prompts_above_chance": int((acc > CHANCE).sum()), "own_minus_false_self": diff.mean(),
                      "self_recognition_p_signflip": signflip_p(diff.to_numpy(), "greater"), "prompts_own_gt_false": int((diff > 0).sum())})
    J = pd.DataFrame(jrows); J.to_csv(RESULTS_DIR / "cr_judges_prompt_level.csv", index=False)

    # transfer cells: features (z within language) and adapted char n-grams (union vocabulary, z within language)
    z = zscore_within_language(feat)
    trows, tcells = [], []
    for a in langs:
        da = z[z.lang == a]
        clf = make_pipeline(StandardScaler(), _lr(1.0)).fit(da[FEATURE_NAMES].to_numpy(float), da["model_key"].to_numpy())
        ta = texts.set_index("cell_id").loc[feat[feat.lang == a]["cell_id"]]
        for b in langs:
            if a == b:
                continue
            db = z[z.lang == b]
            c = (clf.predict(db[FEATURE_NAMES].to_numpy(float)) == db["model_key"].to_numpy()).astype(float)
            tcells.append(pd.DataFrame({"representation": "features", "train": a, "test": b, "cell_id": db["cell_id"].to_numpy(),
                                        "prompt_id": db["prompt_id"].to_numpy(), "correct": c}))
            pp = per_prompt(c, db["prompt_id"].to_numpy())
            trows.append({"representation": "features", "train": a, "test": b, "accuracy": c.mean(), "p_raw": signflip_p((pp - CHANCE).to_numpy(), "greater")})
            tb = texts.set_index("cell_id").loc[feat[feat.lang == b]["cell_id"]]
            vec = _vec("char"); vec.fit(pd.concat([ta["text"], tb["text"]]))
            Xa, Xb = vec.transform(ta["text"]).toarray(), vec.transform(tb["text"]).toarray()
            Xa = (Xa - Xa.mean(0)) / (Xa.std(0) + 1e-9); Xb = (Xb - Xb.mean(0)) / (Xb.std(0) + 1e-9)
            c = (_lr(1.0).fit(Xa, ta["model_key"]).predict(Xb) == tb["model_key"].to_numpy()).astype(float)
            tcells.append(pd.DataFrame({"representation": "char_ngram_adapted", "train": a, "test": b, "cell_id": tb.index.to_numpy(),
                                        "prompt_id": tb["prompt_id"].to_numpy(), "correct": c}))
            pp = per_prompt(c, tb["prompt_id"].to_numpy())
            trows.append({"representation": "char_ngram_adapted", "train": a, "test": b, "accuracy": c.mean(), "p_raw": signflip_p((pp - CHANCE).to_numpy(), "greater")})
        print(f"[C2] transfer from {a} done", flush=True)
    T = pd.DataFrame(trows)
    for r, d in T.groupby("representation"):
        rej, ph, _, _ = multipletests(d["p_raw"], alpha=0.05, method="holm"); T.loc[d.index, "p_holm"] = ph; T.loc[d.index, "significant_holm_05"] = rej
    T.to_csv(RESULTS_DIR / "cr_transfer_prompt_level.csv", index=False)
    TC = pd.concat(tcells); TC.to_csv(RESULTS_DIR / "cr_transfer_cells.csv", index=False)
    # paired: per prompt, mean over the 42 cells of (features - adapted n-grams) accuracy
    pc = TC.groupby(["representation", "prompt_id"])["correct"].mean().unstack(0)
    dpp = pc["features"] - pc["char_ngram_adapted"]
    transfer_paired = {"mean_diff": float(dpp.mean()), "prompts_features_ahead": int((dpp > 0).sum()), "n_prompts": int(len(dpp)),
                       "p_signflip_two_sided": signflip_p(dpp.to_numpy())}

    # translations: LOPO per (translator, language), prompt-clustered CI and sign-flip vs chance
    from .analysis import cv_predict
    tr = pd.read_csv(FEATURES_DIR / "features_translated.csv")
    for fn in FEATURE_NAMES:
        tr[fn] = tr.groupby(["translator", "lang"])[fn].transform(lambda s: s.fillna(s.median()))
    rng = np.random.default_rng(RS); rrows = []
    for (t, l), d in tr.groupby(["translator", "lang"]):
        X, y, g = d[FEATURE_NAMES].to_numpy(float), d["model_key"].to_numpy(), d["prompt_id"].to_numpy()
        p, _ = cv_predict(X, y, g, "logreg", RS); c = (p == y).astype(float)
        lo, hi = cluster_ci(c, g, rng)
        rrows.append({"translator": t, "lang": l, "accuracy": c.mean(), "ci_lo_cluster": lo, "ci_hi_cluster": hi,
                      "p_signflip": signflip_p((per_prompt(c, g) - CHANCE).to_numpy(), "greater")})
    R = pd.DataFrame(rrows); R.to_csv(RESULTS_DIR / "cr_translation_prompt_level.csv", index=False)

    summ = {"holm28": {fam: int(d.significant_holm_05.sum()) for fam, d in h.assign(fam=h.family.str.replace(r" \(.*\)", "", regex=True)).groupby("fam")},
            "holm28_max_p_holm_vs_chance": float(h[h.family == "features vs chance"]["p_holm"].max()),
            "holm28_max_p_holm_vs_judge": float(h[h.family.str.startswith("features vs best judge")]["p_holm"].max()),
            "ngram_sig_langs": h[(h.family == "features vs char n-gram") & h.significant_holm_05]["lang"].tolist(),
            "transfer_sig": {r: int(d.significant_holm_05.sum()) for r, d in T.groupby("representation")},
            "transfer_features_vs_ngram": transfer_paired,
            "translation_min_ci_lo": float(R["ci_lo_cluster"].min()), "translation_all_ci_exclude_chance": bool((R["ci_lo_cluster"] > CHANCE).all())}
    json.dump(summ, open(RESULTS_DIR / "cr_prompt_level_summary.json", "w"), indent=1)
    print(json.dumps(summ, indent=1)); print(J.round(4).to_string(index=False))
    return summ


# ---------------------------------------------------------------------------- C3 fragility
def _feat_split(X, y, train, test):
    return (make_pipeline(StandardScaler(), _lr(1.0)).fit(X[train], y[train]).predict(X[test]) == y[test]).astype(float)


def _ngram_split(T, y, train, test):
    vec = _vec("char"); Xtr = vec.fit_transform(T[train])
    return (_lr(1.0).fit(Xtr, y[train]).predict(vec.transform(T[test])) == y[test]).astype(float)


def c3_fragility(cfg: dict, feat: pd.DataFrame, texts: pd.DataFrame) -> pd.DataFrame:
    langs = language_codes(cfg); rank = resource_rank(cfg); rng = np.random.default_rng(RS)
    nopara = [f for f in FEATURE_NAMES if f not in PARA]
    rows = []
    for l in langs:
        d = feat[feat.lang == l].reset_index(drop=True); y = d["model_key"].to_numpy(); g = d["prompt_id"].to_numpy(); tier = d["fk_tier"].to_numpy()
        T = texts.set_index("cell_id").loc[d["cell_id"], "text"].to_numpy()
        Xa, Xn = d[FEATURE_NAMES].to_numpy(float), d[nopara].to_numpy(float)
        res = {}
        for name, splits in (("lopo", [(g != p, g == p) for p in sorted(set(g))]), ("loto", [(tier != t, tier == t) for t in sorted(set(tier))])):
            c_all = np.empty(len(y)); c_np = np.empty(len(y)); c_ng = np.empty(len(y))
            for trn, tst in splits:
                c_all[tst] = _feat_split(Xa, y, trn, tst); c_np[tst] = _feat_split(Xn, y, trn, tst); c_ng[tst] = _ngram_split(T, y, trn, tst)
            for k, c in (("features", c_all), ("features_no_paragraph", c_np), ("char_ngram", c_ng)):
                lo, hi = cluster_ci(c, g, rng)
                res[f"{name}_{k}"] = c.mean(); res[f"{name}_{k}_ci_lo"] = lo; res[f"{name}_{k}_ci_hi"] = hi
                res[f"{name}_{k}_p_signflip"] = signflip_p((per_prompt(c, g) - CHANCE).to_numpy(), "greater")
        rows.append({"lang": l, "rank": rank[l], "n": len(y), **res})
        print(f"[C3] {l}: LOPO feat {res['lopo_features']:.3f} -> LOTO {res['loto_features']:.3f}; no-para LOPO {res['lopo_features_no_paragraph']:.3f}, "
              f"LOTO {res['loto_features_no_paragraph']:.3f}; n-gram LOPO {res['lopo_char_ngram']:.3f} -> LOTO {res['loto_char_ngram']:.3f}", flush=True)
    out = pd.DataFrame(rows).sort_values("rank"); out.to_csv(RESULTS_DIR / "cr_fragility.csv", index=False)
    return out


# ---------------------------------------------------------------------------- C4 RQ4 with prompt-clustered intervals
def c4_rq4_cluster(cfg: dict, feat: pd.DataFrame) -> pd.DataFrame:
    """RQ4 separation statistics with intervals that resample prompts (not texts); basic (reflected)
    interval as in the original analysis."""
    from .analysis import separation_stats
    langs = language_codes(cfg); rank = resource_rank(cfg); rng = np.random.default_rng(RS)
    z = zscore_within_language(feat); rows = []
    for l in langs:
        d = z[z.lang == l]; Z, lab, g = d[FEATURE_NAMES].to_numpy(float), d["model_key"].to_numpy(), d["prompt_id"].to_numpy()
        base = separation_stats(Z, lab); G = np.unique(g); idx_by = {p: np.where(g == p)[0] for p in G}
        boots = {k: [] for k in base}
        for _ in range(NB):
            idx = np.concatenate([idx_by[p] for p in rng.choice(G, len(G), replace=True)])
            s_ = separation_stats(Z[idx], lab[idx])
            for k in boots:
                boots[k].append(s_[k])
        row = {"lang": l, "rank": rank[l], **base}
        for k in base:
            q_lo, q_hi = np.percentile(boots[k], [2.5, 97.5]); row[f"{k}_ci_lo"], row[f"{k}_ci_hi"] = 2 * base[k] - q_hi, 2 * base[k] - q_lo
        rows.append(row)
    out = pd.DataFrame(rows).sort_values("rank"); out.to_csv(RESULTS_DIR / "cr_rq4_prompt_cluster.csv", index=False)
    print(out.round(3).to_string(index=False))
    return out


def run(only: str | None = None) -> None:
    cfg = load_config(); feat = load_features(); texts = kept_texts()
    assert set(feat["cell_id"]) <= set(texts["cell_id"])
    if only in (None, "c3"):
        c3_fragility(cfg, feat, texts)
    if only in (None, "c2"):
        c2_prompt_tests(cfg, feat, texts)
    if only in (None, "c4"):
        c4_rq4_cluster(cfg, feat)
    if only in (None, "c1"):
        print(c1_equal_tuning(cfg, feat, texts).round(3).to_string(index=False))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", choices=["c1", "c2", "c3", "c4"])
    run(ap.parse_args().only)
