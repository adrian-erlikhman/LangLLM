"""RQ5 (extension) — does translation destroy the stylometric fingerprint?

Inputs: data/features/features.csv (native responses) and data/features/features_translated.csv
(kept English responses translated into the six other languages by each translator).

T1  Identifiability after translation. Per (translator, target language): LOPO-CV 5-way
    attribution on translated texts alone. Compared with (a) the same classifier on the
    English originals and (b) native responses in that language. Chance = 0.20.
T2  Does translated GPT look like native GPT? Train on native language-L responses, test on
    translated-into-L texts (features z-scored within each domain). Above chance ⇒ the model's
    native-L fingerprint is partly recoverable through translation.
T3  Feature survival. For each feature, Spearman ρ between the English original and its
    translation across the 120 source texts; and the share of model-explained variance
    (η² by model) before vs after translation.

    python -m langllm.analysis_translation
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import accuracy_score
import statsmodels.formula.api as smf
import statsmodels.api as sm
from .config import load_config, resource_rank, FEATURES_DIR, RESULTS_DIR
from .features import FEATURE_NAMES
from .analysis import load_features, cv_predict, _clf, bootstrap_ci, CHANCE


def _z(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for f in FEATURE_NAMES:
        out[f] = (out[f] - out[f].mean()) / (out[f].std() or 1)
    return out


def _eta_model(d: pd.DataFrame) -> float:
    vals = []
    for f in FEATURE_NAMES:
        m = smf.ols("y ~ C(model_key) + C(prompt_id)", data=d[["model_key", "prompt_id", f]].rename(columns={f: "y"})).fit()
        aov = sm.stats.anova_lm(m, typ=2)
        vals.append(aov.loc["C(model_key)", "sum_sq"] / (aov.loc["C(model_key)", "sum_sq"] + aov.loc["Residual", "sum_sq"]))
    return float(np.mean(vals))


def run() -> None:
    cfg = load_config()
    rs, nb = cfg["analysis"]["random_state"], cfg["analysis"]["n_bootstrap"]
    rank = resource_rank(cfg)
    native = load_features()
    tr = pd.read_csv(FEATURES_DIR / "features_translated.csv")
    for f in FEATURE_NAMES:
        tr[f] = tr.groupby(["translator", "lang"])[f].transform(lambda s: s.fillna(s.median()))
    en = native[native.lang == "en"]
    RESULTS_DIR.mkdir(exist_ok=True)

    # ---- T1 + T2
    rows = []
    # English baseline (same sources)
    Xe, ye, ge = en[FEATURE_NAMES].to_numpy(float), en["model_key"].to_numpy(), en["prompt_id"].to_numpy()
    pe, _ = cv_predict(Xe, ye, ge, "logreg", rs)
    en_acc = float((pe == ye).mean())
    for (trn, lang), d in tr.groupby(["translator", "lang"]):
        if d["model_key"].nunique() < 2 or d["prompt_id"].nunique() < 2:
            continue
        X, y, g = d[FEATURE_NAMES].to_numpy(float), d["model_key"].to_numpy(), d["prompt_id"].to_numpy()
        p, _ = cv_predict(X, y, g, "logreg", rs)
        correct = (p == y).astype(float)
        lo, hi = bootstrap_ci(correct, nb, rs)
        nat = native[native.lang == lang]
        # native accuracy for this language (from RQ1 table if present, else recompute)
        pn, _ = cv_predict(nat[FEATURE_NAMES].to_numpy(float), nat["model_key"].to_numpy(), nat["prompt_id"].to_numpy(), "logreg", rs)
        nat_acc = float((pn == nat["model_key"].to_numpy()).mean())
        # T2: train native-L (z within native-L), test translated-into-L (z within translated set)
        clf = _clf("logreg", rs).fit(_z(nat)[FEATURE_NAMES].to_numpy(float), nat["model_key"].to_numpy())
        t2 = accuracy_score(y, clf.predict(_z(d)[FEATURE_NAMES].to_numpy(float)))
        # T2 reverse: train English originals, test translated
        clf_en = _clf("logreg", rs).fit(_z(en)[FEATURE_NAMES].to_numpy(float), ye)
        t2_en = accuracy_score(y, clf_en.predict(_z(d)[FEATURE_NAMES].to_numpy(float)))
        rows.append({"translator": trn, "lang": lang, "rank": rank[lang], "n": len(y),
                     "acc_translated_lopo": correct.mean(), "ci_lo": lo, "ci_hi": hi,
                     "acc_english_originals": en_acc, "acc_native_same_lang": nat_acc,
                     "acc_train_native_test_translated": t2, "acc_train_english_test_translated": t2_en,
                     "p_vs_chance": stats.binomtest(int(correct.sum()), len(correct), CHANCE, alternative="greater").pvalue})
    t1 = pd.DataFrame(rows).sort_values(["translator", "rank"])
    t1.to_csv(RESULTS_DIR / "rq5_translation_accuracy.csv", index=False)

    # ---- T3 feature survival
    srows = []
    en_idx = en.set_index("cell_id")
    for (trn, lang), d in tr.groupby(["translator", "lang"]):
        d = d[d["source_cell_id"].isin(en_idx.index)]
        src = en_idx.loc[d["source_cell_id"]]
        eta_before, eta_after = _eta_model(src.reset_index()), _eta_model(d)
        for f in FEATURE_NAMES:
            rho, p = stats.spearmanr(src[f].to_numpy(float), d[f].to_numpy(float))
            srows.append({"translator": trn, "lang": lang, "rank": rank[lang], "feature": f, "spearman_rho": rho, "p": p,
                          "eta2_model_before": eta_before, "eta2_model_after": eta_after})
    t3 = pd.DataFrame(srows)
    t3.to_csv(RESULTS_DIR / "rq5_feature_survival.csv", index=False)

    summ = {}
    for trn, d in t1.groupby("translator"):
        s3 = t3[t3.translator == trn]
        summ[trn] = {"mean_acc_translated_lopo": float(d["acc_translated_lopo"].mean()),
                     "acc_english_originals": en_acc,
                     "mean_acc_native_same_lang": float(d["acc_native_same_lang"].mean()),
                     "mean_acc_train_native_test_translated": float(d["acc_train_native_test_translated"].mean()),
                     "mean_acc_train_english_test_translated": float(d["acc_train_english_test_translated"].mean()),
                     "mean_feature_rho": float(s3["spearman_rho"].mean()),
                     "features_rho_above_0.5": int((s3.groupby("feature")["spearman_rho"].mean() > 0.5).sum()),
                     "mean_eta2_model_before": float(s3["eta2_model_before"].mean()),
                     "mean_eta2_model_after": float(s3["eta2_model_after"].mean())}
    with open(RESULTS_DIR / "rq5_summary.json", "w") as f:
        json.dump(summ, f, indent=2)
    print(t1[["translator", "lang", "acc_translated_lopo", "acc_english_originals", "acc_native_same_lang",
              "acc_train_native_test_translated", "acc_train_english_test_translated"]].round(3).to_string(index=False))
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    run()
