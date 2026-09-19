"""RQ7 (review response): the interpretability trade-off, made explicit.

B1  Character n-gram baseline. TF-IDF over character 1-4-grams (fit inside each training fold),
    multinomial logistic regression, leave-one-prompt-out, per language. Also word 1-2-grams.
    Plus the n-gram cross-lingual transfer matrix (train A, test B) and n-gram attribution on
    the machine translations, so the baseline is compared on every axis the features are.
B2  Feature-selection curve. Per language and pooled, for k = 1..21: rank features by mean
    |standardised coefficient| on the training fold only, keep the top k, refit, predict the
    held-out prompt. Macro-F1 and accuracy against k. Nested, so no leakage.
B3  Feature-group ablation. Per language: only-this-group and all-but-this-group, LOPO macro-F1.
B4  Holm correction over every headline comparison: features vs chance (7 binomial tests),
    features vs n-gram (7 exact McNemar tests, paired on text), features vs best LLM judge
    (7 exact McNemar tests), n-gram vs chance (7).

    python -m langllm.baselines            # all four -> results/rq7_*.csv, figures F11-F13
"""
from __future__ import annotations
import json
import warnings
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.contingency_tables import mcnemar
from statsmodels.stats.multitest import multipletests
from .config import load_config, resource_rank, language_codes, ROOT, RESULTS_DIR, FIG_DIR
from .collect import iter_raw
from .features import FEATURE_NAMES, FEATURE_GROUPS
from .analysis import load_features, zscore_within_language, bootstrap_ci, CHANCE

warnings.filterwarnings("ignore")
RS = 0


# ---------------------------------------------------------------------------- data
def kept_texts() -> pd.DataFrame:
    v = pd.read_csv(ROOT / "data" / "validation.csv")
    keep = set(v.loc[v["keep"], "cell_id"])
    rows = [{"cell_id": r["cell_id"], "model_key": r["model_key"], "lang": r["lang"], "prompt_id": r["prompt_id"], "text": r["text"]}
            for r in iter_raw() if r["cell_id"] in keep]
    return pd.DataFrame(rows)


def translated_texts() -> pd.DataFrame:
    from .translate import iter_translated
    return pd.DataFrame([{"cell_id": r["cell_id"], "model_key": r["model_key"], "lang": r["lang"], "prompt_id": r["prompt_id"],
                          "translator": r["translator"], "text": r["text"]} for r in iter_translated()])


def lopo_folds(prompts: np.ndarray):
    for p in sorted(set(prompts)):
        te = prompts == p
        yield ~te, te


# ---------------------------------------------------------------------------- B1 n-grams
def _vec(kind: str) -> TfidfVectorizer:
    if kind == "char":
        return TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 4), min_df=2, sublinear_tf=True, max_features=60000)
    return TfidfVectorizer(analyzer="word", ngram_range=(1, 2), min_df=2, sublinear_tf=True, max_features=60000, token_pattern=r"(?u)\b\w+\b")


def ngram_lopo(texts: np.ndarray, y: np.ndarray, prompts: np.ndarray, kind: str) -> np.ndarray:
    pred = np.empty(len(y), dtype=object)
    for tr, te in lopo_folds(prompts):
        vec = _vec(kind)
        Xtr = vec.fit_transform(texts[tr]); Xte = vec.transform(texts[te])
        clf = LogisticRegression(C=1.0, max_iter=5000, random_state=RS).fit(Xtr, y[tr])
        pred[te] = clf.predict(Xte)
    return pred


def b1_ngram(df: pd.DataFrame, cfg: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    rank = resource_rank(cfg); nb = cfg["analysis"]["n_bootstrap"]
    rows, cells = [], []
    for kind in ("char", "word"):
        for lang, d in df.groupby("lang"):
            texts, y, g = d["text"].to_numpy(), d["model_key"].to_numpy(), d["prompt_id"].to_numpy()
            pred = ngram_lopo(texts, y, g, kind)
            correct = (pred == y).astype(float)
            lo, hi = bootstrap_ci(correct, nb, RS)
            rows.append({"baseline": f"{kind}_ngram", "lang": lang, "rank": rank[lang], "n": len(y), "accuracy": correct.mean(),
                         "acc_ci_lo": lo, "acc_ci_hi": hi, "macro_f1": f1_score(y, pred, average="macro"),
                         "p_vs_chance": stats.binomtest(int(correct.sum()), len(y), CHANCE, alternative="greater").pvalue})
            cells.extend({"cell_id": c, "baseline": f"{kind}_ngram", "lang": lang, "correct": int(k)} for c, k in zip(d["cell_id"], correct))
            print(f"[B1] {kind} {lang}: acc {correct.mean():.3f}", flush=True)
    acc = pd.DataFrame(rows); cell = pd.DataFrame(cells)
    acc.to_csv(RESULTS_DIR / "rq7_ngram_accuracy.csv", index=False)
    cell.to_csv(RESULTS_DIR / "rq7_ngram_cell_correct.csv", index=False)

    # transfer matrix, char n-grams: train on all of A, test on all of B
    langs = language_codes(cfg)
    M = pd.DataFrame(index=langs, columns=langs, dtype=float)
    fitted = {}
    for a in langs:
        da = df[df.lang == a]
        vec = _vec("char"); Xa = vec.fit_transform(da["text"])
        fitted[a] = (vec, LogisticRegression(C=1.0, max_iter=5000, random_state=RS).fit(Xa, da["model_key"]))
    for a in langs:
        vec, clf = fitted[a]
        for b in langs:
            db = df[df.lang == b]
            if a == b:
                M.loc[a, b] = acc[(acc.baseline == "char_ngram") & (acc.lang == a)]["accuracy"].iloc[0]
            else:
                M.loc[a, b] = accuracy_score(db["model_key"], clf.predict(vec.transform(db["text"])))
    M.to_csv(RESULTS_DIR / "rq7_ngram_transfer_matrix.csv")
    off = M.to_numpy()[~np.eye(len(langs), dtype=bool)]
    print(f"[B1] char n-gram transfer: mean off-diagonal {off.mean():.3f}, {int((off > CHANCE).sum())}/{off.size} above chance", flush=True)

    # translations: LOPO on translated text per translator x language, plus English-trained applied to translations
    tr = translated_texts()
    en = df[df.lang == "en"]
    vec_en = _vec("char"); Xen = vec_en.fit_transform(en["text"])
    clf_en = LogisticRegression(C=1.0, max_iter=5000, random_state=RS).fit(Xen, en["model_key"])
    trows = []
    for (t, lang), d in tr.groupby(["translator", "lang"]):
        pred = ngram_lopo(d["text"].to_numpy(), d["model_key"].to_numpy(), d["prompt_id"].to_numpy(), "char")
        trows.append({"translator": t, "lang": lang, "rank": rank[lang], "n": len(d),
                      "acc_translated_lopo": accuracy_score(d["model_key"], pred),
                      "acc_train_english_test_translated": accuracy_score(d["model_key"], clf_en.predict(vec_en.transform(d["text"])))})
    T = pd.DataFrame(trows).sort_values(["translator", "rank"])
    T.to_csv(RESULTS_DIR / "rq7_ngram_translation.csv", index=False)
    with open(RESULTS_DIR / "rq7_ngram_summary.json", "w") as f:
        json.dump({"char_mean_acc": float(acc[acc.baseline == "char_ngram"]["accuracy"].mean()),
                   "word_mean_acc": float(acc[acc.baseline == "word_ngram"]["accuracy"].mean()),
                   "char_transfer_mean_offdiag": float(off.mean()), "char_transfer_n_above_chance": int((off > CHANCE).sum()),
                   "char_translation_lopo_mean": float(T["acc_translated_lopo"].mean()),
                   "char_train_en_test_translated_mean": float(T["acc_train_english_test_translated"].mean())}, f, indent=2)
    return acc, cell


# ---------------------------------------------------------------------------- B2 feature-selection curve
def _rank_on_train(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    sc = StandardScaler().fit(X)
    clf = LogisticRegression(C=1.0, max_iter=5000, random_state=RS).fit(sc.transform(X), y)
    return np.argsort(-np.abs(clf.coef_).mean(axis=0))


def curve_lopo(X: np.ndarray, y: np.ndarray, prompts: np.ndarray, ks: range) -> tuple[dict[int, np.ndarray], list[list[str]]]:
    preds = {k: np.empty(len(y), dtype=object) for k in ks}
    orders = []
    for tr, te in lopo_folds(prompts):
        order = _rank_on_train(X[tr], y[tr]); orders.append([FEATURE_NAMES[i] for i in order])
        for k in ks:
            idx = order[:k]
            sc = StandardScaler().fit(X[tr][:, idx])
            clf = LogisticRegression(C=1.0, max_iter=5000, random_state=RS).fit(sc.transform(X[tr][:, idx]), y[tr])
            preds[k][te] = clf.predict(sc.transform(X[te][:, idx]))
    return preds, orders


def b2_curve(feat: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    rank = resource_rank(cfg)
    ks = range(1, len(FEATURE_NAMES) + 1)
    rows, top = [], []
    sets = [(lang, d) for lang, d in feat.groupby("lang")] + [("pooled", zscore_within_language(feat))]
    for lang, d in sets:
        X, y, g = d[FEATURE_NAMES].to_numpy(float), d["model_key"].to_numpy(), d["prompt_id"].to_numpy()
        preds, orders = curve_lopo(X, y, g, ks)
        for k in ks:
            rows.append({"lang": lang, "rank": rank.get(lang, 0), "k": k, "accuracy": accuracy_score(y, preds[k]),
                         "macro_f1": f1_score(y, preds[k], average="macro")})
        # consensus order: mean rank position across folds
        pos = {f: np.mean([o.index(f) for o in orders]) for f in FEATURE_NAMES}
        top.append({"lang": lang, "order": " > ".join(sorted(FEATURE_NAMES, key=pos.get))})
        print(f"[B2] {lang}: F1 at k=3 {rows[-19]['macro_f1']:.3f}, k=5 {rows[-17]['macro_f1']:.3f}, k=21 {rows[-1]['macro_f1']:.3f}", flush=True)
    out = pd.DataFrame(rows); out.to_csv(RESULTS_DIR / "rq7_feature_curve.csv", index=False)
    pd.DataFrame(top).to_csv(RESULTS_DIR / "rq7_feature_curve_order.csv", index=False)
    return out


# ---------------------------------------------------------------------------- B3 group ablation
def _lopo_f1(X: np.ndarray, y: np.ndarray, prompts: np.ndarray) -> tuple[float, float]:
    pred = np.empty(len(y), dtype=object)
    for tr, te in lopo_folds(prompts):
        sc = StandardScaler().fit(X[tr])
        clf = LogisticRegression(C=1.0, max_iter=5000, random_state=RS).fit(sc.transform(X[tr]), y[tr])
        pred[te] = clf.predict(sc.transform(X[te]))
    return f1_score(y, pred, average="macro"), accuracy_score(y, pred)


def b3_groups(feat: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    rank = resource_rank(cfg)
    rows = []
    for lang, d in feat.groupby("lang"):
        y, g = d["model_key"].to_numpy(), d["prompt_id"].to_numpy()
        full_f1, full_acc = _lopo_f1(d[FEATURE_NAMES].to_numpy(float), y, g)
        rows.append({"lang": lang, "rank": rank[lang], "condition": "all", "group": "all", "macro_f1": full_f1, "accuracy": full_acc})
        for grp, fs in FEATURE_GROUPS.items():
            f1o, acco = _lopo_f1(d[fs].to_numpy(float), y, g)
            rest = [f for f in FEATURE_NAMES if f not in fs]
            f1w, accw = _lopo_f1(d[rest].to_numpy(float), y, g)
            rows.append({"lang": lang, "rank": rank[lang], "condition": "only", "group": grp, "macro_f1": f1o, "accuracy": acco})
            rows.append({"lang": lang, "rank": rank[lang], "condition": "without", "group": grp, "macro_f1": f1w, "accuracy": accw,
                         "delta_f1_vs_all": f1w - full_f1})
        print(f"[B3] {lang} done", flush=True)
    out = pd.DataFrame(rows); out.to_csv(RESULTS_DIR / "rq7_group_ablation.csv", index=False)
    return out


# ---------------------------------------------------------------------------- B4 Holm
def _best_judge_cells(cfg: dict) -> pd.DataFrame:
    from .judge import load_judgements
    j = load_judgements()
    per = pd.read_csv(RESULTS_DIR / "rq6_judge_by_language.csv")
    best = per.sort_values("accuracy", ascending=False).groupby("lang").head(1).set_index("lang")["judge"]
    rows = []
    for lang, jd in best.items():
        d = j[(j.lang == lang) & (j.judge == jd)]
        rows.extend({"cell_id": c, "lang": lang, "judge": jd, "correct": int(k)} for c, k in zip(d["cell_id"], d["correct"]))
    return pd.DataFrame(rows)


def _mcnemar(a: pd.Series, b: pd.Series) -> tuple[int, int, float]:
    """a, b: aligned 0/1 correctness. Returns (a-only wins, b-only wins, exact two-sided p)."""
    n10 = int(((a == 1) & (b == 0)).sum()); n01 = int(((a == 0) & (b == 1)).sum())
    if n10 + n01 == 0:
        return n10, n01, 1.0
    return n10, n01, float(mcnemar([[0, n10], [n01, 0]], exact=True).pvalue)


def b4_holm(cfg: dict, ngram_cells: pd.DataFrame) -> pd.DataFrame:
    langs = language_codes(cfg)
    feat = pd.read_csv(RESULTS_DIR / "rq1_cell_correct.csv").set_index("cell_id")
    ng = ngram_cells[ngram_cells.baseline == "char_ngram"].set_index("cell_id")
    jd = _best_judge_cells(cfg).set_index("cell_id")
    rows = []
    for lang in langs:
        f = feat[feat.lang == lang]["correct"]
        k, n = int(f.sum()), len(f)
        rows.append({"family": "features vs chance", "lang": lang, "test": "exact binomial (greater)", "stat": f"{k}/{n}",
                     "effect": k / n - CHANCE, "p_raw": stats.binomtest(k, n, CHANCE, alternative="greater").pvalue})
        g = ng[ng.lang == lang]["correct"]; kg = int(g.sum())
        rows.append({"family": "char n-gram vs chance", "lang": lang, "test": "exact binomial (greater)", "stat": f"{kg}/{len(g)}",
                     "effect": kg / len(g) - CHANCE, "p_raw": stats.binomtest(kg, len(g), CHANCE, alternative="greater").pvalue})
        common = f.index.intersection(g.index)
        n10, n01, p = _mcnemar(f.loc[common], g.loc[common])
        rows.append({"family": "features vs char n-gram", "lang": lang, "test": "exact McNemar (two-sided)", "stat": f"feat-only {n10}, ngram-only {n01}",
                     "effect": f.loc[common].mean() - g.loc[common].mean(), "p_raw": p})
        jj = jd[jd.lang == lang]["correct"]; common = f.index.intersection(jj.index)
        n10, n01, p = _mcnemar(f.loc[common], jj.loc[common])
        rows.append({"family": f"features vs best judge ({jd[jd.lang == lang]['judge'].iloc[0]})", "lang": lang, "test": "exact McNemar (two-sided)",
                     "stat": f"feat-only {n10}, judge-only {n01}", "effect": f.loc[common].mean() - jj.loc[common].mean(), "p_raw": p})
    out = pd.DataFrame(rows)
    rej, p_holm, _, _ = multipletests(out["p_raw"], alpha=0.05, method="holm")
    out["p_holm"] = p_holm; out["significant_holm_05"] = rej
    out["n_comparisons_in_family_wide_correction"] = len(out)
    out.to_csv(RESULTS_DIR / "rq7_holm.csv", index=False)
    return out


# ---------------------------------------------------------------------------- figures
def figures(cfg: dict) -> None:
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"figure.dpi": 150, "savefig.dpi": 200, "font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                         "axes.grid": True, "grid.alpha": 0.25})
    langs = language_codes(cfg)
    NAME = {"en": "English", "es": "Spanish", "zh": "Chinese", "ru": "Russian", "ja": "Japanese", "tr": "Turkish", "hi": "Hindi", "pooled": "Pooled (z within language)"}
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    # F11 feature-selection curve
    cv = pd.read_csv(RESULTS_DIR / "rq7_feature_curve.csv")
    ng = pd.read_csv(RESULTS_DIR / "rq7_ngram_accuracy.csv"); ngc = ng[ng.baseline == "char_ngram"].set_index("lang")
    fig, axes = plt.subplots(2, 4, figsize=(12, 5.6), sharey=True)
    for ax, l in zip(axes.flat, langs + ["pooled"]):
        d = cv[cv.lang == l]
        ax.plot(d["k"], d["macro_f1"], "o-", ms=3, color="#2B4C8C", label="21 UD features, top-k")
        if l in ngc.index:
            ax.axhline(ngc.loc[l, "macro_f1"], color="#C44E52", ls="--", lw=1.2, label="char 1-4-gram TF-IDF (all)")
        ax.axhline(CHANCE, color="k", ls=":", lw=0.8)
        ax.set_title(NAME[l], fontsize=9); ax.set_xlim(0.5, 21.5); ax.set_ylim(0, 1); ax.set_xticks([1, 3, 5, 10, 15, 21])
    axes.flat[0].set_ylabel("macro-F1 (LOPO)"); axes.flat[4].set_ylabel("macro-F1 (LOPO)")
    for ax in axes.flat[4:]:
        ax.set_xlabel("number of features (ranked on training fold)")
    axes.flat[0].legend(frameon=False, fontsize=7, loc="lower right")
    fig.suptitle("Feature-selection curve: how many interpretable features it takes, against an opaque n-gram baseline", fontsize=10)
    fig.tight_layout(); fig.savefig(FIG_DIR / "F11_feature_curve.png"); plt.close(fig)

    # F12 group ablation heatmap (only / without), macro-F1
    ab = pd.read_csv(RESULTS_DIR / "rq7_group_ablation.csv")
    groups = list(FEATURE_GROUPS)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
    for ax, cond, title in zip(axes, ["only", "without"], ["only this group", "all groups except this one"]):
        Mx = ab[ab.condition == cond].pivot(index="group", columns="lang", values="macro_f1").loc[groups, langs]
        im = ax.imshow(Mx.to_numpy(float), cmap="Blues", vmin=0.2, vmax=0.8, aspect="auto")
        ax.set_xticks(range(len(langs)), langs); ax.set_yticks(range(len(groups)), groups)
        for i in range(len(groups)):
            for j in range(len(langs)):
                v = Mx.iat[i, j]; ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=7, color="white" if v > 0.55 else "black")
        ax.set_title(f"macro-F1, {title}", fontsize=9); ax.grid(False)
    full = ab[ab.condition == "all"].set_index("lang")["macro_f1"].loc[langs]
    axes[1].set_xticks(range(len(langs)), [f"{l}\nall: {full[l]:.2f}" for l in langs])
    fig.colorbar(im, ax=axes, fraction=0.025)
    fig.suptitle("Feature-group ablation per language (LOPO logistic regression)", fontsize=10)
    fig.savefig(FIG_DIR / "F12_group_ablation.png", bbox_inches="tight"); plt.close(fig)

    # F13 n-gram vs features on the three axes: within-language, transfer, translation
    acc = pd.read_csv(RESULTS_DIR / "rq1_accuracy.csv"); lr = acc[acc.classifier == "logreg"].set_index("lang")
    Mf = pd.read_csv(RESULTS_DIR / "rq3_transfer_matrix.csv", index_col=0); Mn = pd.read_csv(RESULTS_DIR / "rq7_ngram_transfer_matrix.csv", index_col=0)
    t5 = pd.read_csv(RESULTS_DIR / "rq5_translation_accuracy.csv"); t7 = pd.read_csv(RESULTS_DIR / "rq7_ngram_translation.csv")
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.6))
    x = np.arange(len(langs)); w = 0.38
    axes[0].bar(x - w / 2, [lr.loc[l, "accuracy"] for l in langs], w, color="#2B4C8C", label="21 UD features")
    axes[0].bar(x + w / 2, [ngc.loc[l, "accuracy"] for l in langs], w, color="#C44E52", label="char n-gram")
    axes[0].axhline(CHANCE, color="k", ls=":", lw=0.8); axes[0].set_xticks(x, langs); axes[0].set_ylim(0, 1)
    axes[0].set_title("within language (LOPO)", fontsize=9); axes[0].legend(frameon=False, fontsize=7)
    offf = Mf.to_numpy(float)[~np.eye(7, dtype=bool)]; offn = Mn.to_numpy(float)[~np.eye(7, dtype=bool)]
    axes[1].hist([offf, offn], bins=np.linspace(0, 0.8, 17), color=["#2B4C8C", "#C44E52"], label=["UD features", "char n-gram"])
    axes[1].axvline(CHANCE, color="k", ls=":", lw=0.8); axes[1].set_xlabel("accuracy, train language A, test language B (42 pairs)")
    axes[1].set_title("cross-lingual transfer", fontsize=9); axes[1].legend(frameon=False, fontsize=7)
    f5 = t5[t5.translator == "google"].set_index("lang"); n7 = t7[t7.translator == "google"].set_index("lang")
    L6 = [l for l in langs if l != "en"]; x6 = np.arange(len(L6))
    axes[2].bar(x6 - w / 2, [f5.loc[l, "acc_train_english_test_translated"] for l in L6], w, color="#2B4C8C")
    axes[2].bar(x6 + w / 2, [n7.loc[l, "acc_train_english_test_translated"] for l in L6], w, color="#C44E52")
    axes[2].axhline(CHANCE, color="k", ls=":", lw=0.8); axes[2].set_xticks(x6, L6); axes[2].set_ylim(0, 1)
    axes[2].set_title("English-trained classifier on Google translations", fontsize=9)
    fig.suptitle("Where the opaque baseline wins and where it cannot go", fontsize=10)
    fig.tight_layout(); fig.savefig(FIG_DIR / "F13_ngram_vs_features.png"); plt.close(fig)
    print("wrote F11, F12, F13")


def run() -> None:
    cfg = load_config()
    RESULTS_DIR.mkdir(exist_ok=True)
    df = kept_texts(); feat = load_features()
    print(f"{len(df)} texts, {len(feat)} feature rows")
    _, cells = b1_ngram(df, cfg)
    b2_curve(feat, cfg)
    b3_groups(feat, cfg)
    holm = b4_holm(cfg, cells)
    figures(cfg)
    print(holm[["family", "lang", "effect", "p_raw", "p_holm", "significant_holm_05"]].round(4).to_string(index=False))


if __name__ == "__main__":
    run()
