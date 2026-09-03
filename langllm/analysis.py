"""Step 5 — the four research questions, from data/features/features.csv to results/*.csv.

RQ1  Within each language, can the five models be told apart? Leave-one-prompt-out CV
     (both generations of a prompt sit on the same side of the split), logistic regression on
     standardised features (interpretable) and a random forest (ceiling). Chance = 0.20.
RQ2  Does accuracy fall with resource rank? Spearman over the seven languages plus a
     cell-level binomial GLM (correct ~ rank) with prompt-clustered SEs.
RQ3  Model style vs language style: per-feature two-way ANOVA (model × language, prompt as a
     blocking factor) → partial η²; plus cross-lingual transfer of a classifier trained on
     within-language z-scored features (language-invariant style ⇒ transfer above chance).
RQ4  Convergence in low-resource languages: within-language model separation (mean pairwise
     centroid distance, silhouette, between/within trace ratio) with bootstrap CIs, vs rank.

    python -m langllm.analysis                 # all RQs
    python -m langllm.analysis --features path/to/features.csv
"""
from __future__ import annotations
import argparse
import itertools
import json
import warnings
import numpy as np
import pandas as pd
from scipy import stats
from scipy.spatial.distance import pdist
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, silhouette_score
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
import statsmodels.formula.api as smf
from .config import load_config, resource_rank, FEATURES_DIR, RESULTS_DIR
from .features import FEATURE_NAMES

warnings.filterwarnings("ignore", category=FutureWarning)
CHANCE = 0.2


def load_features(path=None) -> pd.DataFrame:
    df = pd.read_csv(path or FEATURES_DIR / "features.csv")
    # impute rare NaNs (e.g. burstiness on a 1-sentence reply) with the within-language median
    for f in FEATURE_NAMES:
        df[f] = df.groupby("lang")[f].transform(lambda s: s.fillna(s.median()))
    return df


def zscore_within_language(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for f in FEATURE_NAMES:
        g = out.groupby("lang")[f]
        out[f] = (out[f] - g.transform("mean")) / g.transform("std").replace(0, 1)
    return out


def residualise_length(df: pd.DataFrame) -> pd.DataFrame:
    """Robustness: regress each feature on log(n_tokens) within language and keep residuals."""
    out = df.copy()
    logn = np.log(out["n_tokens"].clip(lower=1))
    for lang, idx in out.groupby("lang").groups.items():
        X = sm.add_constant(logn.loc[idx])
        for f in FEATURE_NAMES:
            out.loc[idx, f] = sm.OLS(out.loc[idx, f], X).fit().resid
    return out


def _clf(kind: str, rs: int):
    if kind == "logreg":
        return make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=5000, random_state=rs))
    # n_jobs=1 on purpose: with ~120 rows per fit, process-pool spawn cost (esp. Windows) dwarfs the work
    return make_pipeline(StandardScaler(), RandomForestClassifier(n_estimators=300, random_state=rs, n_jobs=1))


def cv_predict(X: np.ndarray, y: np.ndarray, groups: np.ndarray, kind: str, rs: int):
    """Leave-one-group-out predictions; also returns mean |coef| per feature for logreg."""
    pred = np.empty_like(y, dtype=object)
    coefs = []
    for tr, te in LeaveOneGroupOut().split(X, y, groups):
        clf = _clf(kind, rs).fit(X[tr], y[tr])
        pred[te] = clf.predict(X[te])
        if kind == "logreg":
            coefs.append(np.abs(clf[-1].coef_).mean(axis=0))
    return pred, (np.mean(coefs, axis=0) if coefs else None)


def bootstrap_ci(correct: np.ndarray, n: int, rs: int, stat=np.mean) -> tuple[float, float]:
    rng = np.random.default_rng(rs)
    vals = [stat(rng.choice(correct, size=len(correct), replace=True)) for _ in range(n)]
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


# ---------------------------------------------------------------------------- RQ1
def rq1(df: pd.DataFrame, cfg: dict, tag: str = "") -> tuple[pd.DataFrame, pd.DataFrame]:
    rs, nb = cfg["analysis"]["random_state"], cfg["analysis"]["n_bootstrap"]
    rank = resource_rank(cfg)
    rows, imp_rows, cell_rows = [], [], []
    for lang, d in df.groupby("lang"):
        X, y, g = d[FEATURE_NAMES].to_numpy(float), d["model_key"].to_numpy(), d["prompt_id"].to_numpy()
        if len(set(y)) < 2 or len(set(g)) < 2:
            continue
        for kind in ("logreg", "rf"):
            pred, coef = cv_predict(X, y, g, kind, rs)
            correct = (pred == y).astype(float)
            lo, hi = bootstrap_ci(correct, nb, rs)
            # exact binomial test against chance
            p_binom = stats.binomtest(int(correct.sum()), len(correct), CHANCE, alternative="greater").pvalue
            rows.append({"lang": lang, "rank": rank[lang], "classifier": kind, "n": len(y),
                         "accuracy": correct.mean(), "acc_ci_lo": lo, "acc_ci_hi": hi,
                         "macro_f1": f1_score(y, pred, average="macro"), "p_vs_chance": p_binom})
            if kind == "logreg":
                labels = sorted(set(y))
                cm = pd.DataFrame(confusion_matrix(y, pred, labels=labels), index=labels, columns=labels)
                cm.to_csv(RESULTS_DIR / f"rq1_confusion_{lang}{tag}.csv")
                for f, c in zip(FEATURE_NAMES, coef):
                    imp_rows.append({"lang": lang, "feature": f, "mean_abs_coef": c})
                cell_rows.extend({"cell_id": cid, "lang": lang, "rank": rank[lang], "prompt_id": pid,
                                  "model_key": m, "correct": int(c)} for cid, pid, m, c in zip(d["cell_id"], g, y, correct))
    acc = pd.DataFrame(rows)
    imp = pd.DataFrame(imp_rows)
    acc.to_csv(RESULTS_DIR / f"rq1_accuracy{tag}.csv", index=False)
    if not imp.empty:
        imp.to_csv(RESULTS_DIR / f"rq1_feature_importance{tag}.csv", index=False)
        # univariate separability: one-way ANOVA F of each feature by model, within language
        uni = []
        for lang, d in df.groupby("lang"):
            for f in FEATURE_NAMES:
                groups = [v[f].to_numpy(float) for _, v in d.groupby("model_key")]
                if len(groups) > 1 and all(len(x) > 1 for x in groups):
                    F, p = stats.f_oneway(*groups)
                    uni.append({"lang": lang, "feature": f, "F": F, "p": p})
        pd.DataFrame(uni).to_csv(RESULTS_DIR / f"rq1_univariate_F{tag}.csv", index=False)
    pd.DataFrame(cell_rows).to_csv(RESULTS_DIR / f"rq1_cell_correct{tag}.csv", index=False)
    return acc, imp


# ---------------------------------------------------------------------------- RQ2
def rq2(acc: pd.DataFrame, cfg: dict, tag: str = "") -> dict:
    out = {}
    cells = pd.read_csv(RESULTS_DIR / f"rq1_cell_correct{tag}.csv")
    for kind in acc["classifier"].unique():
        a = acc[acc["classifier"] == kind].sort_values("rank")
        rho, p = stats.spearmanr(a["rank"], a["accuracy"])
        slope, intercept, r, p_lin, se = stats.linregress(a["rank"], a["accuracy"])
        out[kind] = {"spearman_rho": float(rho), "spearman_p": float(p), "ols_slope_per_rank": float(slope),
                     "ols_p": float(p_lin), "acc_english": float(a.iloc[0]["accuracy"]),
                     "acc_lowest": float(a.iloc[-1]["accuracy"])}
    # cell-level GLM (logreg predictions), SEs clustered by prompt
    glm = smf.glm("correct ~ rank", data=cells, family=sm.families.Binomial()).fit(
        cov_type="cluster", cov_kwds={"groups": cells["prompt_id"].astype("category").cat.codes})
    out["glm_cell_level"] = {"coef_rank_logodds": float(glm.params["rank"]), "se": float(glm.bse["rank"]),
                             "p": float(glm.pvalues["rank"]), "n_cells": int(len(cells))}
    with open(RESULTS_DIR / f"rq2_gradient{tag}.json", "w") as f:
        json.dump(out, f, indent=2)
    return out


# ---------------------------------------------------------------------------- RQ3
def _partial_eta(aov: pd.DataFrame, term: str) -> float:
    ss, ss_res = aov.loc[term, "sum_sq"], aov.loc["Residual", "sum_sq"]
    return float(ss / (ss + ss_res))


def rq3_anova(df: pd.DataFrame, tag: str = "") -> pd.DataFrame:
    rows = []
    for f in FEATURE_NAMES:
        d = df[["model_key", "lang", "prompt_id", f]].rename(columns={f: "y"})
        d["y"] = (d["y"] - d["y"].mean()) / (d["y"].std() or 1)
        m = smf.ols("y ~ C(model_key) * C(lang) + C(prompt_id)", data=d).fit()
        aov = sm.stats.anova_lm(m, typ=2)
        rows.append({"feature": f,
                     "eta2_model": _partial_eta(aov, "C(model_key)"),
                     "eta2_lang": _partial_eta(aov, "C(lang)"),
                     "eta2_interaction": _partial_eta(aov, "C(model_key):C(lang)"),
                     "eta2_prompt": _partial_eta(aov, "C(prompt_id)"),
                     "p_model": float(aov.loc["C(model_key)", "PR(>F)"]),
                     "p_lang": float(aov.loc["C(lang)", "PR(>F)"]),
                     "p_interaction": float(aov.loc["C(model_key):C(lang)", "PR(>F)"])})
    res = pd.DataFrame(rows)
    res.loc[len(res)] = {"feature": "MEAN", **res[[c for c in res.columns if c.startswith("eta2")]].mean().to_dict(),
                         "p_model": np.nan, "p_lang": np.nan, "p_interaction": np.nan}
    res.to_csv(RESULTS_DIR / f"rq3_anova_eta2{tag}.csv", index=False)
    return res


def rq3_transfer(df: pd.DataFrame, cfg: dict, tag: str = "") -> pd.DataFrame:
    """Train on language A (within-language z-scored), test on B. Diagonal = LOPO within-language."""
    rs = cfg["analysis"]["random_state"]
    z = zscore_within_language(df)
    langs = sorted(z["lang"].unique(), key=lambda l: resource_rank(cfg)[l])
    M = pd.DataFrame(index=langs, columns=langs, dtype=float)
    for a in langs:
        da = z[z["lang"] == a]
        Xa, ya, ga = da[FEATURE_NAMES].to_numpy(float), da["model_key"].to_numpy(), da["prompt_id"].to_numpy()
        clf = _clf("logreg", rs).fit(Xa, ya)
        for b in langs:
            db = z[z["lang"] == b]
            if a == b:
                pred, _ = cv_predict(Xa, ya, ga, "logreg", rs)
                M.loc[a, b] = accuracy_score(ya, pred)
            else:
                M.loc[a, b] = accuracy_score(db["model_key"], clf.predict(db[FEATURE_NAMES].to_numpy(float)))
    M.to_csv(RESULTS_DIR / f"rq3_transfer_matrix{tag}.csv")
    off = M.to_numpy()[~np.eye(len(langs), dtype=bool)]
    with open(RESULTS_DIR / f"rq3_transfer_summary{tag}.json", "w") as f:
        json.dump({"mean_offdiag_accuracy": float(off.mean()), "mean_diag_accuracy": float(np.diag(M).mean()),
                   "chance": CHANCE, "n_offdiag_above_chance": int((off > CHANCE).sum()), "n_offdiag": int(off.size)}, f, indent=2)
    return M


# ---------------------------------------------------------------------------- RQ4
def separation_stats(Z: np.ndarray, labels: np.ndarray) -> dict:
    cents = {m: Z[labels == m].mean(axis=0) for m in np.unique(labels)}
    C = np.vstack(list(cents.values()))
    within = sum(((Z[labels == m] - cents[m]) ** 2).sum() for m in cents)
    between = sum((labels == m).sum() * ((cents[m] - Z.mean(axis=0)) ** 2).sum() for m in cents)
    return {"centroid_dist": float(pdist(C).mean()),
            "silhouette": float(silhouette_score(Z, labels)) if len(cents) > 1 else np.nan,
            "between_within_ratio": float(between / within) if within else np.nan}


def rq4(df: pd.DataFrame, cfg: dict, tag: str = "") -> pd.DataFrame:
    rs, nb = cfg["analysis"]["random_state"], cfg["analysis"]["n_bootstrap"]
    rank = resource_rank(cfg)
    rng = np.random.default_rng(rs)
    z = zscore_within_language(df)
    rows, pair_rows = [], []
    for lang, d in z.groupby("lang"):
        Z, lab = d[FEATURE_NAMES].to_numpy(float), d["model_key"].to_numpy()
        base = separation_stats(Z, lab)
        boots = {k: [] for k in base}
        idx_by = {m: np.where(lab == m)[0] for m in np.unique(lab)}
        for _ in range(nb):
            idx = np.concatenate([rng.choice(ix, size=len(ix), replace=True) for ix in idx_by.values()])
            s = separation_stats(Z[idx], lab[idx])
            for k in boots:
                boots[k].append(s[k])
        row = {"lang": lang, "rank": rank[lang], "n": len(lab), **base}
        for k in base:  # basic (reflected) bootstrap interval: corrects the upward bias of resampled distances
            q_lo, q_hi = np.percentile(boots[k], [2.5, 97.5])
            row[f"{k}_ci_lo"], row[f"{k}_ci_hi"] = 2 * base[k] - q_hi, 2 * base[k] - q_lo
        rows.append(row)
        cents = {m: Z[lab == m].mean(axis=0) for m in np.unique(lab)}
        for a, b in itertools.combinations(sorted(cents), 2):
            pair_rows.append({"lang": lang, "rank": rank[lang], "model_a": a, "model_b": b,
                              "centroid_dist": float(np.linalg.norm(cents[a] - cents[b]))})
    res = pd.DataFrame(rows).sort_values("rank")
    res.to_csv(RESULTS_DIR / f"rq4_separation{tag}.csv", index=False)
    pd.DataFrame(pair_rows).to_csv(RESULTS_DIR / f"rq4_pairwise{tag}.csv", index=False)
    summ = {}
    for k in ("centroid_dist", "silhouette", "between_within_ratio"):
        rho, p = stats.spearmanr(res["rank"], res[k])
        summ[k] = {"spearman_rho_vs_rank": float(rho), "p": float(p),
                   "english": float(res.iloc[0][k]), "lowest_resource": float(res.iloc[-1][k])}
    with open(RESULTS_DIR / f"rq4_summary{tag}.json", "w") as f:
        json.dump(summ, f, indent=2)
    return res


# ---------------------------------------------------------------------------- driver
def run_all(features_path=None, length_control: bool = True) -> None:
    cfg = load_config()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    df = load_features(features_path)
    print(f"{len(df)} responses, {df['lang'].nunique()} languages, {df['model_key'].nunique()} models")

    acc, _ = rq1(df, cfg)
    print("\nRQ1 — attribution accuracy (leave-one-prompt-out):")
    print(acc.pivot(index="lang", columns="classifier", values="accuracy").loc[
        sorted(acc["lang"].unique(), key=lambda l: resource_rank(cfg)[l])].round(3).to_string())

    g = rq2(acc, cfg)
    print("\nRQ2 — gradient:", json.dumps(g, indent=1))

    eta = rq3_anova(df)
    print("\nRQ3 — mean partial η²:", eta[eta.feature == "MEAN"][["eta2_model", "eta2_lang", "eta2_interaction"]].round(3).to_dict("records"))
    M = rq3_transfer(df, cfg)
    print("RQ3 — cross-lingual transfer (rows=train, cols=test):\n", M.round(2).to_string())

    sep = rq4(df, cfg)
    print("\nRQ4 — within-language model separation:\n", sep[["lang", "rank", "centroid_dist", "silhouette", "between_within_ratio"]].round(3).to_string(index=False))

    if length_control:
        print("\nRobustness — length-residualised features (tag _lenctl):")
        acc2, _ = rq1(residualise_length(df), cfg, tag="_lenctl")
        rq2(acc2, cfg, tag="_lenctl")
        print(acc2.pivot(index="lang", columns="classifier", values="accuracy").round(3).to_string())


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--features", help="path to features.csv (default data/features/features.csv)")
    ap.add_argument("--no-length-control", action="store_true")
    a = ap.parse_args()
    run_all(a.features, length_control=not a.no_length_control)
