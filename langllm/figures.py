"""Step 6 — figures from results/*.csv into results/figures/*.png.

F1 rq1_accuracy      per-language attribution accuracy with 95% CI, chance line
F2 rq1_confusion     7 confusion matrices (logistic regression)
F3 rq2_gradient      accuracy vs resource rank
F4 rq3_eta2          per-feature partial η² for model / language / interaction
F5 rq3_transfer      cross-lingual transfer heatmap
F6 rq4_separation    model separation vs rank (three metrics)
F7 pca_by_language   PCA of within-language z-scored features, coloured by model

    python -m langllm.figures
    python -m langllm.figures --features data/features/synthetic.csv
"""
from __future__ import annotations
import argparse
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from .config import load_config, resource_rank, RESULTS_DIR, FIG_DIR, FEATURES_DIR
from .features import FEATURE_NAMES, FEATURE_GROUPS
from .analysis import zscore_within_language, load_features, CHANCE

plt.rcParams.update({"figure.dpi": 150, "savefig.dpi": 200, "font.size": 9, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.grid": True, "grid.alpha": 0.25})
MODEL_COLORS = {"gpt": "#4C72B0", "gemini": "#DD8452", "claude": "#55A868", "grok": "#C44E52", "deepseek": "#8172B3"}
GROUP_COLORS = {"lexical": "#4C72B0", "syntactic": "#55A868", "structure": "#DD8452", "punctuation": "#C44E52", "character": "#8172B3"}


def _langs(cfg):
    return sorted(cfg["languages"], key=lambda l: cfg["languages"][l]["rank"])


def _save(fig, name):
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(FIG_DIR / f"{name}.png")
    plt.close(fig)
    print("wrote", FIG_DIR / f"{name}.png")


def f1_accuracy(cfg, tag=""):
    acc = pd.read_csv(RESULTS_DIR / f"rq1_accuracy{tag}.csv")
    langs = [l for l in _langs(cfg) if l in set(acc["lang"])]
    fig, ax = plt.subplots(figsize=(7, 3.6))
    w = 0.38
    for i, (kind, off, col) in enumerate([("logreg", -w / 2, "#4C72B0"), ("rf", w / 2, "#999999")]):
        a = acc[acc.classifier == kind].set_index("lang").loc[langs]
        x = np.arange(len(langs)) + off
        ax.bar(x, a["accuracy"], w, color=col, label={"logreg": "logistic regression", "rf": "random forest"}[kind])
        ax.errorbar(x, a["accuracy"], yerr=[a["accuracy"] - a["acc_ci_lo"], a["acc_ci_hi"] - a["accuracy"]],
                    fmt="none", ecolor="k", capsize=2, lw=0.8)
    ax.axhline(CHANCE, ls="--", c="k", lw=0.8, label="chance (1/5)")
    ax.set_xticks(range(len(langs)), [f"{l}\n#{cfg['languages'][l]['rank']}" for l in langs])
    ax.set_ylim(0, 1.0); ax.set_ylabel("attribution accuracy (LOPO-CV)")
    ax.set_xlabel("language (resource rank)"); ax.legend(frameon=False, ncol=3, fontsize=8)
    ax.set_title("RQ1 — five-way model attribution from 21 UD-based features")
    _save(fig, f"F1_rq1_accuracy{tag}")


def f2_confusions(cfg, tag=""):
    langs = [l for l in _langs(cfg) if (RESULTS_DIR / f"rq1_confusion_{l}{tag}.csv").exists()]
    if not langs:
        return
    fig, axes = plt.subplots(2, 4, figsize=(11, 5.6))
    for ax, l in zip(axes.flat, langs):
        cm = pd.read_csv(RESULTS_DIR / f"rq1_confusion_{l}{tag}.csv", index_col=0)
        norm = cm.div(cm.sum(axis=1), axis=0)
        ax.imshow(norm, cmap="Blues", vmin=0, vmax=1)
        ax.set_xticks(range(len(cm)), cm.columns, rotation=45, ha="right", fontsize=7)
        ax.set_yticks(range(len(cm)), cm.index, fontsize=7)
        for i in range(len(cm)):
            for j in range(len(cm)):
                ax.text(j, i, f"{norm.iat[i, j]:.2f}", ha="center", va="center", fontsize=6,
                        color="white" if norm.iat[i, j] > 0.5 else "black")
        ax.set_title(f"{l} (rank {cfg['languages'][l]['rank']})", fontsize=9); ax.grid(False)
        ax.set_xlabel("predicted", fontsize=7); ax.set_ylabel("true", fontsize=7)
    for ax in axes.flat[len(langs):]:
        ax.axis("off")
    fig.suptitle("RQ1 — row-normalised confusion (logistic regression, LOPO-CV)")
    _save(fig, f"F2_rq1_confusion{tag}")


def f3_gradient(cfg, tag=""):
    acc = pd.read_csv(RESULTS_DIR / f"rq1_accuracy{tag}.csv")
    with open(RESULTS_DIR / f"rq2_gradient{tag}.json") as f:
        g = json.load(f)
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    for kind, col in [("logreg", "#4C72B0"), ("rf", "#999999")]:
        a = acc[acc.classifier == kind].sort_values("rank")
        ax.errorbar(a["rank"], a["accuracy"], yerr=[a["accuracy"] - a["acc_ci_lo"], a["acc_ci_hi"] - a["accuracy"]],
                    fmt="o-", color=col, capsize=2, label=f"{kind}  ρ={g[kind]['spearman_rho']:.2f}, p={g[kind]['spearman_p']:.2f}")
        for _, r in a.iterrows():
            ax.annotate(r["lang"], (r["rank"], r["accuracy"]), textcoords="offset points", xytext=(4, 4), fontsize=7)
    ax.axhline(CHANCE, ls="--", c="k", lw=0.8)
    glm = g["glm_cell_level"]
    ax.set_title(f"RQ2 — accuracy vs resource rank\ncell-level GLM: β={glm['coef_rank_logodds']:.3f} log-odds/rank, p={glm['p']:.3g}", fontsize=9)
    ax.set_xlabel("resource rank (1 = English … 7 = Hindi)"); ax.set_ylabel("attribution accuracy"); ax.set_ylim(0, 1)
    ax.legend(frameon=False, fontsize=7)
    _save(fig, f"F3_rq2_gradient{tag}")


def f4_eta2(cfg, tag=""):
    eta = pd.read_csv(RESULTS_DIR / f"rq3_anova_eta2{tag}.csv")
    eta = eta[eta.feature != "MEAN"].sort_values("eta2_model", ascending=True)
    fig, ax = plt.subplots(figsize=(7, 5.5))
    y = np.arange(len(eta))
    ax.barh(y, eta["eta2_model"], color="#4C72B0", label="model")
    ax.barh(y, eta["eta2_lang"], left=eta["eta2_model"], color="#DD8452", label="language")
    ax.barh(y, eta["eta2_interaction"], left=eta["eta2_model"] + eta["eta2_lang"], color="#55A868", label="model × language")
    ax.set_yticks(y, eta["feature"], fontsize=8)
    for lbl in ax.get_yticklabels():
        grp = next(g for g, fs in FEATURE_GROUPS.items() if lbl.get_text() in fs)
        lbl.set_color(GROUP_COLORS[grp])
    ax.set_xlabel("partial η² (prompt as blocking factor)"); ax.legend(frameon=False, loc="lower right")
    ax.set_title("RQ3 — how much of each feature is model, language, or their interaction")
    _save(fig, f"F4_rq3_eta2{tag}")


def f5_transfer(cfg, tag=""):
    M = pd.read_csv(RESULTS_DIR / f"rq3_transfer_matrix{tag}.csv", index_col=0)
    fig, ax = plt.subplots(figsize=(5.2, 4.4))
    im = ax.imshow(M.to_numpy(float), cmap="viridis", vmin=0, vmax=1)
    ax.set_xticks(range(len(M)), M.columns); ax.set_yticks(range(len(M)), M.index)
    for i in range(len(M)):
        for j in range(len(M)):
            v = M.iat[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=7, color="white" if v < 0.55 else "black")
    ax.set_xlabel("test language"); ax.set_ylabel("train language"); ax.grid(False)
    fig.colorbar(im, ax=ax, fraction=0.046, label="accuracy (chance 0.20)")
    ax.set_title("RQ3 — cross-lingual transfer of a within-language\nz-scored classifier (diagonal = LOPO-CV)", fontsize=9)
    _save(fig, f"F5_rq3_transfer{tag}")


def f6_separation(cfg, tag=""):
    sep = pd.read_csv(RESULTS_DIR / f"rq4_separation{tag}.csv").sort_values("rank")
    with open(RESULTS_DIR / f"rq4_summary{tag}.json") as f:
        s = json.load(f)
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.3))
    for ax, k, lab in zip(axes, ["centroid_dist", "silhouette", "between_within_ratio"],
                          ["mean pairwise centroid distance", "silhouette (model labels)", "between / within trace"]):
        yerr = [np.clip(sep[k] - sep[f"{k}_ci_lo"], 0, None), np.clip(sep[f"{k}_ci_hi"] - sep[k], 0, None)]
        ax.errorbar(sep["rank"], sep[k], yerr=yerr, fmt="o-", color="#4C72B0", capsize=2)
        for _, r in sep.iterrows():
            ax.annotate(r["lang"], (r["rank"], r[k]), textcoords="offset points", xytext=(4, 4), fontsize=7)
        ax.set_title(f"{lab}\nρ={s[k]['spearman_rho_vs_rank']:.2f}, p={s[k]['p']:.2f}", fontsize=8.5)
        ax.set_xlabel("resource rank")
    fig.suptitle("RQ4 — do the five models converge stylistically as resources fall?", fontsize=10)
    _save(fig, f"F6_rq4_separation{tag}")


def f7_pca(cfg, features_path=None):
    df = zscore_within_language(load_features(features_path))
    langs = [l for l in _langs(cfg) if l in set(df["lang"])]
    fig, axes = plt.subplots(2, 4, figsize=(11, 5.6))
    for ax, l in zip(axes.flat, langs):
        d = df[df.lang == l]
        P = PCA(2, random_state=0).fit(d[FEATURE_NAMES])
        Z = P.transform(d[FEATURE_NAMES])
        for m in sorted(d.model_key.unique()):
            sel = (d.model_key == m).to_numpy()
            ax.scatter(Z[sel, 0], Z[sel, 1], s=10, alpha=0.7, color=MODEL_COLORS.get(m, None), label=m)
            c = Z[sel].mean(axis=0)
            ax.scatter(*c, s=90, marker="X", color=MODEL_COLORS.get(m, None), edgecolor="k", lw=0.6)
        ax.set_title(f"{l} (rank {cfg['languages'][l]['rank']})  var={P.explained_variance_ratio_.sum():.0%}", fontsize=8)
        ax.set_xticks([]); ax.set_yticks([])
    for ax in axes.flat[len(langs):]:
        ax.axis("off")
    axes.flat[0].legend(frameon=False, fontsize=7, loc="best")
    fig.suptitle("Within-language PCA of the 21 features (X = model centroid)", fontsize=10)
    _save(fig, "F7_pca_by_language")


def f8_translation(cfg):
    t1 = pd.read_csv(RESULTS_DIR / "rq5_translation_accuracy.csv")
    langs = [l for l in _langs(cfg) if l in set(t1["lang"])]
    trs = list(t1["translator"].unique())
    fig, axes = plt.subplots(1, len(trs), figsize=(5.2 * len(trs), 3.8), sharey=True)
    axes = np.atleast_1d(axes)
    for ax, tr in zip(axes, trs):
        d = t1[t1.translator == tr].set_index("lang").loc[langs]
        x = np.arange(len(langs)); w = 0.27
        ax.bar(x - w, d["acc_native_same_lang"], w, color="#BBBBBB", label="native responses in that language")
        ax.bar(x, d["acc_translated_lopo"], w, color="#4C72B0", label="translated from English (LOPO)")
        ax.errorbar(x, d["acc_translated_lopo"], yerr=[d["acc_translated_lopo"] - d["ci_lo"], d["ci_hi"] - d["acc_translated_lopo"]],
                    fmt="none", ecolor="k", capsize=2, lw=0.8)
        ax.bar(x + w, d["acc_train_native_test_translated"], w, color="#DD8452", label="train native → test translated")
        ax.axhline(d["acc_english_originals"].iloc[0], ls=":", c="#4C72B0", lw=1, label="English originals (LOPO)")
        ax.axhline(CHANCE, ls="--", c="k", lw=0.8)
        ax.set_xticks(x, [f"{l}
#{cfg['languages'][l]['rank']}" for l in langs]); ax.set_ylim(0, 1)
        ax.set_title({"google": "Google Translate", "llm": "LLM translator (non-subject)"}.get(tr, tr))
    axes[0].set_ylabel("attribution accuracy"); axes[0].legend(frameon=False, fontsize=7, loc="upper right")
    fig.suptitle("RQ5 — does translation destroy the fingerprint?", fontsize=10)
    _save(fig, "F8_rq5_translation")


def f9_feature_survival(cfg):
    t3 = pd.read_csv(RESULTS_DIR / "rq5_feature_survival.csv")
    trs = list(t3["translator"].unique())
    fig, axes = plt.subplots(1, len(trs), figsize=(4.6 * len(trs), 6), sharey=True)
    axes = np.atleast_1d(axes)
    order = [f for g in FEATURE_GROUPS.values() for f in g]
    for ax, tr in zip(axes, trs):
        M = t3[t3.translator == tr].pivot(index="feature", columns="lang", values="spearman_rho").loc[order]
        M = M[[l for l in _langs(cfg) if l in M.columns]]
        im = ax.imshow(M.to_numpy(float), cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
        ax.set_xticks(range(M.shape[1]), M.columns); ax.set_yticks(range(len(order)), order, fontsize=7)
        for lbl in ax.get_yticklabels():
            grp = next(g for g, fs in FEATURE_GROUPS.items() if lbl.get_text() in fs); lbl.set_color(GROUP_COLORS[grp])
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                ax.text(j, i, f"{M.iat[i, j]:.2f}", ha="center", va="center", fontsize=6)
        ax.set_title({"google": "Google Translate", "llm": "LLM translator"}.get(tr, tr), fontsize=9); ax.grid(False)
    fig.colorbar(im, ax=axes, fraction=0.03, label="Spearman ρ, original vs translation (n = English sources)")
    fig.suptitle("RQ5 — which features survive translation?", fontsize=10)
    FIG_DIR.mkdir(parents=True, exist_ok=True); fig.savefig(FIG_DIR / "F9_rq5_feature_survival.png", bbox_inches="tight"); plt.close(fig)
    print("wrote", FIG_DIR / "F9_rq5_feature_survival.png")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--features", help="features.csv used for the PCA panel")
    ap.add_argument("--tag", default="", help="results suffix, e.g. _lenctl")
    ap.add_argument("--rq5", action="store_true", help="only the translation figures F8/F9")
    a = ap.parse_args()
    cfg = load_config()
    if a.rq5:
        f8_translation(cfg); f9_feature_survival(cfg); return
    f1_accuracy(cfg, a.tag); f2_confusions(cfg, a.tag); f3_gradient(cfg, a.tag)
    if not a.tag:
        f4_eta2(cfg); f5_transfer(cfg); f6_separation(cfg); f7_pca(cfg, a.features)


if __name__ == "__main__":
    main()
