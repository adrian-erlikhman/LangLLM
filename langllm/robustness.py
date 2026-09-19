"""RQ7b (review response, second pass): things a careful reviewer asks for.

R1  Prompt-clustered bootstrap CIs (resample the 12 prompts, not the responses) for RQ1
    accuracy, the n-gram baseline and each LLM judge, per language.
R2  RQ2 effect-size framing: 95% CI on the GLM rank coefficient, the largest decline it
    excludes (in accuracy points across the seven-rank range), and the same gradient test
    on the n-gram baseline.
R3  Per-cell binomial tests with Holm over all 42 off-diagonal cells of BOTH transfer
    matrices (features and char n-grams), plus a count of constant-prediction cells.
R4  A fair n-gram transfer: vocabulary fit on the union of train and test language, TF-IDF
    columns z-scored within each language (the same adaptation the features get), train on
    A, test on B. And a script-neutral char model (punctuation, digits, whitespace only)
    trained and transferred the same way.

    python -m langllm.robustness     # -> results/rq7b_*.csv/json
"""
from __future__ import annotations
import json
import re
import warnings
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from statsmodels.stats.multitest import multipletests
import statsmodels.api as sm
import statsmodels.formula.api as smf
from .config import load_config, resource_rank, language_codes, RESULTS_DIR
from .analysis import CHANCE
from .baselines import kept_texts, RS

warnings.filterwarnings("ignore")
NB = 2000


# ---------------------------------------------------------------------------- R1
def cluster_ci(correct: np.ndarray, groups: np.ndarray, rng: np.random.Generator) -> tuple[float, float]:
    G = np.unique(groups)
    by = {g: correct[groups == g] for g in G}
    vals = []
    for _ in range(NB):
        pick = rng.choice(G, size=len(G), replace=True)
        s = np.concatenate([by[g] for g in pick]); vals.append(s.mean())
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def r1_cluster_cis(cfg: dict) -> pd.DataFrame:
    rng = np.random.default_rng(RS)
    feat = pd.read_csv(RESULTS_DIR / "rq1_cell_correct.csv")
    ng = pd.read_csv(RESULTS_DIR / "rq7_ngram_cell_correct.csv").merge(feat[["cell_id", "prompt_id"]], on="cell_id")
    from .judge import load_judgements
    jd = load_judgements()
    rows = []
    for lang in language_codes(cfg):
        d = feat[feat.lang == lang]; lo, hi = cluster_ci(d["correct"].to_numpy(float), d["prompt_id"].to_numpy(), rng)
        rows.append({"lang": lang, "system": "features_logreg", "accuracy": d["correct"].mean(), "ci_lo_cluster": lo, "ci_hi_cluster": hi})
        for b in ("char_ngram", "word_ngram"):
            e = ng[(ng.lang == lang) & (ng.baseline == b)]; lo, hi = cluster_ci(e["correct"].to_numpy(float), e["prompt_id"].to_numpy(), rng)
            rows.append({"lang": lang, "system": b, "accuracy": e["correct"].mean(), "ci_lo_cluster": lo, "ci_hi_cluster": hi})
        for j, e in jd[jd.lang == lang].groupby("judge"):
            lo, hi = cluster_ci(e["correct"].to_numpy(float), e["prompt_id"].to_numpy(), rng)
            rows.append({"lang": lang, "system": f"judge_{j}", "accuracy": e["correct"].mean(), "ci_lo_cluster": lo, "ci_hi_cluster": hi})
        e = jd[jd.lang == lang]
        rows.append({"lang": lang, "system": "judge_mean_of_5", "accuracy": e["correct"].mean(), "ci_lo_cluster": np.nan, "ci_hi_cluster": np.nan})
    out = pd.DataFrame(rows); out["rank"] = out["lang"].map(resource_rank(cfg))
    out.to_csv(RESULTS_DIR / "rq7b_cluster_ci.csv", index=False)
    return out


# ---------------------------------------------------------------------------- R2
def r2_gradient(cfg: dict) -> dict:
    cells = pd.read_csv(RESULTS_DIR / "rq1_cell_correct.csv")
    glm = smf.glm("correct ~ rank", data=cells, family=sm.families.Binomial()).fit(
        cov_type="cluster", cov_kwds={"groups": cells["prompt_id"].astype("category").cat.codes})
    b, se = float(glm.params["rank"]), float(glm.bse["rank"])
    lo, hi = b - 1.96 * se, b + 1.96 * se
    p0 = cells[cells["rank"] == 1]["correct"].mean()
    def acc_at(rank, beta):  # accuracy at a rank under a log-odds slope from the English baseline
        lo0 = np.log(p0 / (1 - p0)); return 1 / (1 + np.exp(-(lo0 + beta * (rank - 1))))
    worst = acc_at(7, lo)  # steepest decline compatible with the CI
    ng = pd.read_csv(RESULTS_DIR / "rq7_ngram_accuracy.csv"); c = ng[ng.baseline == "char_ngram"].sort_values("rank")
    rho, p = stats.spearmanr(c["rank"], c["accuracy"])
    ngc = pd.read_csv(RESULTS_DIR / "rq7_ngram_cell_correct.csv").merge(cells[["cell_id", "prompt_id", "rank"]], on="cell_id")
    ngc = ngc[ngc.baseline == "char_ngram"]
    g2 = smf.glm("correct ~ rank", data=ngc, family=sm.families.Binomial()).fit(
        cov_type="cluster", cov_kwds={"groups": ngc["prompt_id"].astype("category").cat.codes})
    out = {"features_glm": {"beta": b, "se": se, "ci95": [lo, hi], "p": float(glm.pvalues["rank"]),
                            "acc_english": float(p0), "steepest_decline_compatible_acc_at_rank7": float(worst),
                            "steepest_decline_points": float((p0 - worst) * 100)},
           "char_ngram": {"spearman_rho": float(rho), "spearman_p": float(p), "acc_english": float(c.iloc[0]["accuracy"]),
                          "acc_hindi": float(c.iloc[-1]["accuracy"]), "glm_beta": float(g2.params["rank"]), "glm_se": float(g2.bse["rank"]),
                          "glm_p": float(g2.pvalues["rank"])}}
    json.dump(out, open(RESULTS_DIR / "rq7b_gradient.json", "w"), indent=2)
    return out


# ---------------------------------------------------------------------------- R3
def r3_transfer_tests(cfg: dict, n_per_lang: dict[str, int]) -> pd.DataFrame:
    rows = []
    for name, f in (("features", "rq3_transfer_matrix.csv"), ("char_ngram", "rq7_ngram_transfer_matrix.csv")):
        M = pd.read_csv(RESULTS_DIR / f, index_col=0)
        for a in M.index:
            for b in M.columns:
                if a == b:
                    continue
                n = n_per_lang[b]; k = int(round(M.loc[a, b] * n))
                rows.append({"representation": name, "train": a, "test": b, "accuracy": M.loc[a, b], "n": n, "k": k,
                             "p_raw": stats.binomtest(k, n, CHANCE, alternative="greater").pvalue,
                             "constant_prediction": bool(abs(M.loc[a, b] - CHANCE) < 0.006)})
    out = pd.DataFrame(rows)
    for name, d in out.groupby("representation"):
        rej, ph, _, _ = multipletests(d["p_raw"], alpha=0.05, method="holm")
        out.loc[d.index, "p_holm"] = ph; out.loc[d.index, "significant_holm_05"] = rej
    out.to_csv(RESULTS_DIR / "rq7b_transfer_tests.csv", index=False)
    return out


# ---------------------------------------------------------------------------- R4
_PUNCT_ONLY = re.compile(r"[^\W\d_]+", re.UNICODE)  # strip letters; keep punctuation, digits, whitespace


def _script_neutral(text: str) -> str:
    t = _PUNCT_ONLY.sub("w", text)              # every word becomes one token 'w'
    return re.sub(r"[ \t]+", " ", t)


def r4_fair_ngram_transfer(cfg: dict, df: pd.DataFrame) -> dict:
    langs = language_codes(cfg)
    out = {}
    for variant, prep, analyzer, ngr in (("union_vocab_zscored", lambda s: s, "char_wb", (1, 4)),
                                         ("script_neutral_punct_digits", _script_neutral, "char", (1, 5))):
        M = pd.DataFrame(index=langs, columns=langs, dtype=float)
        for a in langs:
            for b in langs:
                da, db = df[df.lang == a], df[df.lang == b]
                ta, tb = da["text"].map(prep), db["text"].map(prep)
                if a == b:
                    # LOPO within language, same preprocessing, so the diagonal is comparable
                    pred = np.empty(len(da), dtype=object); P = da["prompt_id"].to_numpy()
                    for p in sorted(set(P)):
                        te = P == p
                        vec = TfidfVectorizer(analyzer=analyzer, ngram_range=ngr, min_df=2, sublinear_tf=True, max_features=60000)
                        Xtr = vec.fit_transform(ta[~te]); Xte = vec.transform(ta[te])
                        pred[te] = LogisticRegression(C=1.0, max_iter=5000, random_state=RS).fit(Xtr, da["model_key"][~te]).predict(Xte)
                    M.loc[a, b] = accuracy_score(da["model_key"], pred); continue
                vec = TfidfVectorizer(analyzer=analyzer, ngram_range=ngr, min_df=2, sublinear_tf=True, max_features=60000)
                vec.fit(pd.concat([ta, tb]))
                Xa, Xb = vec.transform(ta).toarray(), vec.transform(tb).toarray()
                # within-language z-scoring, exactly as the feature transfer matrix does
                Xa = (Xa - Xa.mean(0)) / (Xa.std(0) + 1e-9); Xb = (Xb - Xb.mean(0)) / (Xb.std(0) + 1e-9)
                clf = LogisticRegression(C=1.0, max_iter=5000, random_state=RS).fit(Xa, da["model_key"])
                M.loc[a, b] = accuracy_score(db["model_key"], clf.predict(Xb))
            print(f"[R4] {variant} train={a} done", flush=True)
        M.to_csv(RESULTS_DIR / f"rq7b_ngram_transfer_{variant}.csv")
        off = M.to_numpy()[~np.eye(len(langs), dtype=bool)]
        out[variant] = {"diag_mean": float(np.diag(M).mean()), "offdiag_mean": float(off.mean()),
                        "offdiag_n_above_chance": int((off > CHANCE).sum()), "offdiag_min": float(off.min()), "offdiag_max": float(off.max())}
    json.dump(out, open(RESULTS_DIR / "rq7b_ngram_transfer_summary.json", "w"), indent=2)
    return out


def run() -> None:
    cfg = load_config()
    df = kept_texts()
    n_per = df.groupby("lang").size().to_dict()
    r1 = r1_cluster_cis(cfg); print(r1[r1.system.isin(["features_logreg", "char_ngram"])].round(3).to_string(index=False))
    print(json.dumps(r2_gradient(cfg), indent=1))
    t = r3_transfer_tests(cfg, n_per)
    print(t.groupby("representation").agg(n_sig=("significant_holm_05", "sum"), n_const=("constant_prediction", "sum"), mean_acc=("accuracy", "mean")))
    print(json.dumps(r4_fair_ngram_transfer(cfg, df), indent=1))


if __name__ == "__main__":
    run()
