"""Paper figures (vector PDF, IEEE column widths) into paper/figures/.

fig1_accuracy   per-language accuracy: UD features (cluster CI), char n-gram, LLM-judge range, chance
fig2_transfer   cross-lingual transfer, features vs char n-gram with the same within-language adaptation
fig3_curve      nested feature-selection curve, per language + pooled, n-gram reference
fig4_survival   feature survival under translation (Spearman rho original vs translation)

    python -m langllm.paper_figures
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from .config import load_config, language_codes, RESULTS_DIR, ROOT
from .features import FEATURE_GROUPS
from .analysis import CHANCE

OUT = ROOT / "paper" / "figures"
COL, DCOL = 3.45, 7.1  # inches
BLUE, RED, GREY, GOLD = "#2B4C8C", "#B23A3A", "#8A8F99", "#D9A441"
plt.rcParams.update({"font.size": 7.5, "font.family": "serif", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.4, "axes.linewidth": 0.6, "xtick.major.width": 0.5,
                     "ytick.major.width": 0.5, "legend.fontsize": 6.5, "pdf.fonttype": 42})
LANG = {"en": "English", "es": "Spanish", "zh": "Chinese", "ru": "Russian", "ja": "Japanese", "tr": "Turkish", "hi": "Hindi"}
FEAT = {"mattr": "MATTR", "hapax_rate": "hapax rate", "mean_token_len": "token length", "zipf_slope": "Zipf slope", "sent_len_mean": "sentence length",
        "sent_len_sd": "sentence-length SD", "burstiness": "burstiness", "dep_depth": "dependency depth", "subord_rate": "subordination",
        "func_word_ratio": "function-word ratio", "first_person_rate": "first-person rate", "para_count": "paragraph count", "para_len_mean": "paragraph length",
        "question_rate": "question rate", "connective_rate": "connective rate", "comma_per_1k": "comma rate", "colon_per_1k": "colon rate",
        "dash_per_1k": "dash rate", "semicolon_per_1k": "semicolon rate", "bigram_entropy": "char-bigram entropy", "digit_rate": "digit rate"}


def fig1(langs):
    cci = pd.read_csv(RESULTS_DIR / "rq7b_cluster_ci.csv")
    f = cci[cci.system == "features_logreg"].set_index("lang").loc[langs]
    n = cci[cci.system == "char_ngram"].set_index("lang").loc[langs]
    j = cci[cci.system.str.startswith("judge_") & (cci.system != "judge_mean_of_5")]
    jmin = j.groupby("lang")["accuracy"].min().loc[langs]; jmax = j.groupby("lang")["accuracy"].max().loc[langs]
    x = np.arange(len(langs))
    fig, ax = plt.subplots(figsize=(COL, 2.05))
    ax.fill_between(x, jmin, jmax, color=GOLD, alpha=0.35, lw=0, label="LLM judges (range of 5)")
    ax.errorbar(x, n["accuracy"], yerr=[n["accuracy"] - n["ci_lo_cluster"], n["ci_hi_cluster"] - n["accuracy"]], fmt="s--", ms=3.5, color=RED, lw=0.9, capsize=2, label="character n-grams (opaque)")
    ax.errorbar(x, f["accuracy"], yerr=[f["accuracy"] - f["ci_lo_cluster"], f["ci_hi_cluster"] - f["accuracy"]], fmt="o-", ms=3.5, color=BLUE, lw=1.1, capsize=2, label="21 UD features (interpretable)")
    ax.axhline(CHANCE, color="k", ls=":", lw=0.7); ax.text(6.35, CHANCE + 0.015, "chance", fontsize=6, ha="right")
    ax.set_xticks(x, [LANG[l] for l in langs], rotation=25, ha="right"); ax.set_ylim(0, 1); ax.set_ylabel("5-way accuracy")
    ax.set_xlabel(r"language, decreasing resource level $\rightarrow$", labelpad=1)
    ax.legend(frameon=False, loc="upper center", ncol=2, bbox_to_anchor=(0.5, -0.58), handlelength=1.8, columnspacing=1.0)
    fig.tight_layout(pad=0.3); fig.savefig(OUT / "fig1_accuracy.pdf", bbox_inches="tight", pad_inches=0.02); plt.close(fig)


def fig2(langs):
    """Column-width, two panels side by side, no colorbar (values are printed in every cell)."""
    F = pd.read_csv(RESULTS_DIR / "rq3_transfer_matrix.csv", index_col=0).loc[langs, langs]
    N = pd.read_csv(RESULTS_DIR / "rq7b_ngram_transfer_union_vocab_zscored.csv", index_col=0).loc[langs, langs]
    fig, axes = plt.subplots(1, 2, figsize=(COL, 1.95))
    for ax, M, title in zip(axes, [F, N], ["(a) UD features", "(b) char n-grams, adapted"]):
        ax.imshow(M.to_numpy(float), cmap="Blues", vmin=0.15, vmax=0.9)
        ax.set_xticks(range(7), langs, fontsize=5.5); ax.set_yticks(range(7), langs, fontsize=5.5)
        for i in range(7):
            for k in range(7):
                v = M.iat[i, k]; ax.text(k, i, f"{v:.2f}".lstrip("0"), ha="center", va="center", fontsize=4.6, color="white" if v > 0.6 else "black", fontweight="bold" if i == k else "normal")
        off = M.to_numpy(float)[~np.eye(7, dtype=bool)]
        ax.set_title(f"{title}
off-diagonal mean {off.mean():.2f}".replace("mean 0.", "mean ."), fontsize=6); ax.grid(False)
        ax.set_xlabel("test language", fontsize=6, labelpad=1); ax.tick_params(length=2, pad=1)
    axes[0].set_ylabel("train language", fontsize=6, labelpad=1); axes[1].set_yticks([])
    fig.tight_layout(pad=0.25, w_pad=0.6); fig.savefig(OUT / "fig2_transfer.pdf"); plt.close(fig)


def fig3(langs):
    cv = pd.read_csv(RESULTS_DIR / "rq7_feature_curve.csv")
    ng = pd.read_csv(RESULTS_DIR / "rq7_ngram_accuracy.csv"); ngm = ng[ng.baseline == "char_ngram"]["macro_f1"].mean()
    fig, ax = plt.subplots(figsize=(COL, 1.8))
    for l in langs:
        d = cv[cv.lang == l]; ax.plot(d["k"], d["macro_f1"], "-", color=BLUE, alpha=0.28, lw=0.8)
    d = cv[cv.lang == "pooled"]; ax.plot(d["k"], d["macro_f1"], "o-", color=BLUE, ms=2.8, lw=1.3, label="pooled, z-scored within language")
    ax.plot([], [], "-", color=BLUE, alpha=0.4, lw=0.8, label="each language")
    ax.axhline(ngm, color=RED, ls="--", lw=0.9, label=f"char n-grams, all, mean macro-F1 {ngm:.2f}".replace(" 0.", " ."))
    ax.axhline(CHANCE, color="k", ls=":", lw=0.7)
    ax.set_xlim(0.5, 21.5); ax.set_ylim(0.15, 0.9); ax.set_xticks([1, 3, 5, 10, 15, 21]); ax.set_xlabel("number of features, ranked on the training fold only")
    ax.set_ylabel("macro-F1 (LOPO)"); ax.legend(frameon=False, loc="lower right", bbox_to_anchor=(1.0, 0.12))
    fig.tight_layout(pad=0.3); fig.savefig(OUT / "fig3_curve.pdf"); plt.close(fig)


def fig4(langs):
    fs = pd.read_csv(RESULTS_DIR / "rq5_feature_survival.csv"); s = fs.groupby("feature")["spearman_rho"].mean().drop("question_rate", errors="ignore").sort_values()
    GC = {"lexical": "#8172B3", "syntactic": "#55A868", "structure": "#DD8452", "punctuation": "#C44E52", "character": "#8172B3"}
    grp = {f: g for g, fl in FEATURE_GROUPS.items() for f in fl}
    fig, ax = plt.subplots(figsize=(COL, 2.6))
    ax.barh(range(len(s)), s.values, color=[GC[grp[f]] for f in s.index], height=0.7)
    ax.set_yticks(range(len(s)), [FEAT[f] for f in s.index], fontsize=6.3); ax.set_xlim(0, 1.0); ax.set_xlabel(r"Spearman $\rho$, original vs. translation")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=c, label=g) for g, c in [("structure", "#DD8452"), ("syntax", "#55A868"), ("punctuation", "#C44E52"), ("lexical / character", "#8172B3")]],
              frameon=False, loc="lower right", fontsize=6); ax.grid(axis="y", alpha=0)
    fig.tight_layout(pad=0.3); fig.savefig(OUT / "fig4_survival.pdf"); plt.close(fig)


def fig3_features(langs):
    """Two-panel figure for the 20 Sept draft: (a) nested selection curve with per-language band, (b) survival."""
    cv = pd.read_csv(RESULTS_DIR / "rq7_feature_curve.csv")
    ng = pd.read_csv(RESULTS_DIR / "rq7_ngram_accuracy.csv"); ngm = ng[ng.baseline == "char_ngram"]["macro_f1"].mean()
    fs = pd.read_csv(RESULTS_DIR / "rq5_feature_survival.csv"); s = fs.groupby("feature")["spearman_rho"].mean().drop("question_rate", errors="ignore").sort_values()
    GC = {"lexical": "#8172B3", "syntactic": "#55A868", "structure": "#DD8452", "punctuation": "#C44E52", "character": "#8172B3"}
    grp = {f: g for g, fl in FEATURE_GROUPS.items() for f in fl}
    fig, (a, b) = plt.subplots(2, 1, figsize=(COL, 3.15), gridspec_kw={"height_ratios": [0.8, 1.55]})
    per = cv[cv.lang != "pooled"].pivot(index="k", columns="lang", values="macro_f1")
    a.fill_between(per.index, per.min(axis=1), per.max(axis=1), color=BLUE, alpha=0.15, lw=0, label="range over 7 languages")
    d = cv[cv.lang == "pooled"]; a.plot(d["k"], d["macro_f1"], "o-", color=BLUE, ms=2.6, lw=1.2, label="pooled, z-scored within language")
    a.axhline(ngm, color=RED, ls="--", lw=0.9, label=f"char n-grams, all, mean macro-F1 {ngm:.2f}".replace(" 0.", " ."))
    a.axhline(CHANCE, color="k", ls=":", lw=0.7)
    a.set_xlim(0.5, 21.5); a.set_ylim(0.15, 0.9); a.set_xticks([1, 3, 5, 10, 15, 21]); a.set_xlabel("number of features, ranked on the training folds")
    a.set_ylabel("macro-F1 (LOPO)", fontsize=6.5); a.legend(frameon=False, loc="lower right", fontsize=5.5); a.set_title("(a)", loc="left", fontsize=8)
    b.barh(range(len(s)), s.values, color=[GC[grp[f]] for f in s.index], height=0.78); b.tick_params(axis="y", length=1.5, pad=1)
    b.set_yticks(range(len(s)), [FEAT[f] for f in s.index], fontsize=5.0); b.set_xlim(0, 1.0); b.set_xlabel(r"Spearman $\rho$, original vs. translation")
    from matplotlib.patches import Patch
    b.legend(handles=[Patch(color=c, label=g) for g, c in [("structure", "#DD8452"), ("syntax", "#55A868"), ("punctuation", "#C44E52"), ("lexical / character", "#8172B3")]],
             frameon=False, loc="lower right", fontsize=6); b.grid(axis="y", alpha=0); b.set_title("(b)", loc="left", fontsize=8)
    fig.tight_layout(pad=0.3); fig.savefig(OUT / "fig3_features.pdf"); plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    langs = language_codes(load_config())
    fig1(langs); fig2(langs); fig3(langs); fig4(langs); fig3_features(langs)
    print("wrote", sorted(p.name for p in OUT.glob("*.pdf")))


if __name__ == "__main__":
    main()
