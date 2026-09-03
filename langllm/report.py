"""Assemble docs/REPORT.md — methodology (static) + every result table from results/ + figures.
Interpretation paragraphs are written by hand in docs/REPORT_interpretation.md and spliced in.

    python -m langllm.report
"""
from __future__ import annotations
import json
import pandas as pd
from .config import load_config, RESULTS_DIR, ROOT, resource_rank

DOCS = ROOT / "docs"


def _csv(name: str) -> pd.DataFrame | None:
    p = RESULTS_DIR / name
    return pd.read_csv(p) if p.exists() else None


def _json(name: str) -> dict | None:
    p = RESULTS_DIR / name
    return json.load(open(p)) if p.exists() else None


def _md(df: pd.DataFrame, floatfmt: str = "{:.3f}") -> str:
    d = df.copy()
    for c in d.columns:
        if d[c].dtype.kind == "f":
            d[c] = d[c].map(lambda v: "" if pd.isna(v) else floatfmt.format(v))
    return "| " + " | ".join(map(str, d.columns)) + " |\n|" + "---|" * len(d.columns) + "\n" + \
        "\n".join("| " + " | ".join(map(str, r)) + " |" for r in d.itertuples(index=False))


def build() -> str:
    cfg = load_config()
    rank = resource_rank(cfg)
    langs = sorted(cfg["languages"], key=rank.get)
    interp = (DOCS / "REPORT_interpretation.md").read_text(encoding="utf-8") if (DOCS / "REPORT_interpretation.md").exists() else ""
    sec = {}
    for tag in ("summary", "rq1", "rq2", "rq3", "rq4", "rq5", "limitations"):
        m = interp.split(f"<!-- {tag} -->")
        sec[tag] = m[1].strip() if len(m) > 1 else ""

    out = []
    out.append(f"""# LangLLM — Methodology and Results

*Do LLM stylistic fingerprints survive outside English?* Interpretable stylometric attribution of
five frontier models across a seven-language resource gradient. Repository:
https://github.com/adrian-erlikhman/LangLLM

{sec['summary']}

## 1. Design

| | |
|---|---|
| Subject models | {" · ".join(f"{k} = `{v}`" for k, v in cfg['models'].items())} |
| Languages (resource rank) | {" → ".join(f"{cfg['languages'][l]['name_en']} ({rank[l]})" for l in langs)} |
| Cells | {len(cfg['models'])} models × 12 prompts × {len(langs)} languages × {cfg['generation']['n_per_cell']} generations = {len(cfg['models']) * 12 * len(langs) * cfg['generation']['n_per_cell']} responses |
| Prompt writer | `{cfg['prompt_writer']}` (not a subject) |
| Prompt reviewer | `{cfg['prompt_reviewer']}` (not a subject, third family) |
| Translators (RQ5) | Google Translate (web endpoint); `{cfg['translators']['llm']}` with fallbacks {cfg['translators']['llm_fallbacks']} |
| Generation | single user turn, no system prompt, temperature {cfg['generation']['temperature']}, seeds fixed per generation index, reasoning {cfg['generation']['reasoning']}, {cfg['generation']['max_tokens']}-token budget |

### 1.1 Prompts
Twelve English schemas each fix a topic, a stance (6 for / 6 against), three sub-claims and a
reading-level tier (4 general / 4 educated / 4 expert). The tier is a prompt control only:
Flesch–Kincaid is English-specific, so no readability feature is measured. For every language
the prompt writer composes a native prompt *from the schema*, never by translation. All seven
versions of a prompt share topic, stance and sub-claims, so content is held fixed and only style
is free. Every native prompt was then checked blind by the reviewer model, which extracted
topic, stance and supporting points and matched them to the schema; failing prompts were
regenerated with the reviewer's note as feedback until all 84 passed (`prompts/native/REVIEW.md`;
earlier wordings are retained in each prompt record).

### 1.2 Validation
Language identification (lingua, restricted to the seven languages, confidence ≥ 0.6), a
word-equivalent length window of 150–900 (Chinese and Japanese converted from characters), a
per-language refusal heuristic, truncation, and a count of heading/bullet lines. Exclusion
rates are reported per model × language (§2).

### 1.3 Features
All text is parsed with Stanza (Universal Dependencies: tokenize, pos, lemma, depparse), so every
feature has the same definition in every language. 21 features in five groups:

| Group | Features |
|---|---|
| Lexical | MATTR (window 50), hapax rate, mean token length, Zipf slope |
| Syntactic | sentence length mean and SD, burstiness, dependency depth, subordinate-clause rate (`acl advcl ccomp xcomp csubj`), function-word ratio, first-person rate |
| Structure | paragraph count, paragraph length, question rate, connective rate (`cc`, `mark`, sentence-initial ADV/CCONJ/SCONJ) |
| Punctuation | comma, colon, dash, semicolon per 1 000 tokens, with script equivalents mapped (`，、` `：` `— – ―` `；`) |
| Character | character-bigram entropy, digit rate |

English-only measures (Flesch, Fog, hedges, passive rate, contractions) are excluded. Chinese and
Japanese are pre-split on `。！？` because Stanza's splitter does not handle them.

### 1.4 Analysis
* **RQ1** — per language, five-way attribution with leave-one-prompt-out cross-validation (both
  generations of a prompt stay on the same side of the split). Primary classifier: multinomial
  logistic regression on standardised features (interpretable); random forest as a ceiling.
  Chance = 0.20. 95% bootstrap CIs; exact binomial test against chance.
* **RQ2** — Spearman ρ of accuracy against resource rank (n = 7) and a cell-level binomial GLM
  `correct ~ rank` with prompt-clustered standard errors (n = all cells). Robustness: features
  residualised on log length within language.
* **RQ3** — per feature, two-way ANOVA (model × language, prompt as blocking factor) with partial
  η²; and a cross-lingual transfer matrix: a classifier trained on within-language z-scored
  features of language A, tested on language B.
* **RQ4** — within-language model separation after pooled z-scoring: mean pairwise centroid
  distance, silhouette of model labels, between/within scatter ratio; stratified bootstrap
  (reflected) CIs; Spearman against rank.
* **RQ5** (extension suggested by Philo) — every kept English response translated into the six
  other languages by two translators. T1: attribution on translated text alone; T2: a classifier
  trained on *native* responses in the target language applied to the translations, and one
  trained on the English originals; T3: per-feature Spearman ρ between original and translation.

Full pre-specified decision rules: `docs/analysis_plan.md`.
""")

    # ---- validation
    v = _csv("validation_summary.csv")
    if v is not None:
        piv = v.pivot(index="model_key", columns="lang", values="keep_rate")[langs]
        out.append("## 2. Data quality\n\nKeep rate per model × language (1.00 = all 24 responses usable):\n\n" + _md(piv.reset_index(), "{:.2f}"))
        bad = v[(v.wrong_language_rate > 0) | (v.refusal_rate > 0) | (v.error_rate > 0) | (v.truncated_rate > 0)]
        if len(bad):
            out.append("\nCells with any exclusion:\n\n" + _md(bad[["model_key", "lang", "n", "wrong_language_rate", "refusal_rate", "error_rate", "truncated_rate", "too_short_rate", "too_long_rate"]], "{:.2f}"))
        med = v.pivot(index="model_key", columns="lang", values="median_words")[langs]
        out.append("\nMedian length (word-equivalents):\n\n" + _md(med.reset_index(), "{:.0f}"))

    # ---- RQ1
    acc = _csv("rq1_accuracy.csv")
    if acc is not None:
        t = acc[acc.classifier == "logreg"].sort_values("rank")[["lang", "rank", "n", "accuracy", "acc_ci_lo", "acc_ci_hi", "macro_f1", "p_vs_chance"]]
        rf = acc[acc.classifier == "rf"].set_index("lang")["accuracy"]
        t["rf_accuracy"] = t["lang"].map(rf)
        out.append("## 3. RQ1 — attribution within each language\n\n![F1](../results/figures/F1_rq1_accuracy.png)\n\n" + _md(t) + "\n\n![F2](../results/figures/F2_rq1_confusion.png)\n\n" + sec["rq1"])
        imp = _csv("rq1_feature_importance.csv")
        if imp is not None:
            top = (imp.sort_values(["lang", "mean_abs_coef"], ascending=[True, False]).groupby("lang").head(5)
                      .groupby("lang")["feature"].apply(lambda s: ", ".join(s)).reindex(langs).reset_index())
            top.columns = ["lang", "top-5 features (mean |standardised coefficient|)"]
            out.append("\nMost discriminative features per language:\n\n" + _md(top))

    # ---- RQ2
    g = _json("rq2_gradient.json")
    if g is not None:
        gl = _json("rq2_gradient_lenctl.json") or {}
        rows = [{"test": "Spearman ρ (logreg), n=7", "value": f"{g['logreg']['spearman_rho']:.2f}", "p": f"{g['logreg']['spearman_p']:.3f}"},
                {"test": "Spearman ρ (random forest)", "value": f"{g['rf']['spearman_rho']:.2f}", "p": f"{g['rf']['spearman_p']:.3f}"},
                {"test": "OLS slope, accuracy per rank step", "value": f"{g['logreg']['ols_slope_per_rank']:+.3f}", "p": f"{g['logreg']['ols_p']:.3f}"},
                {"test": f"Cell-level GLM β(rank), log-odds, n={g['glm_cell_level']['n_cells']}, prompt-clustered", "value": f"{g['glm_cell_level']['coef_rank_logodds']:+.3f} (SE {g['glm_cell_level']['se']:.3f})", "p": f"{g['glm_cell_level']['p']:.2e}"}]
        if gl:
            rows.append({"test": "GLM β(rank) with length-residualised features", "value": f"{gl['glm_cell_level']['coef_rank_logodds']:+.3f}", "p": f"{gl['glm_cell_level']['p']:.2e}"})
        out.append("## 4. RQ2 — the resource gradient\n\n![F3](../results/figures/F3_rq2_gradient.png)\n\n" + _md(pd.DataFrame(rows)) + "\n\n" + sec["rq2"])

    # ---- RQ3
    eta = _csv("rq3_anova_eta2.csv")
    if eta is not None:
        e = eta[["feature", "eta2_model", "eta2_lang", "eta2_interaction", "eta2_prompt"]].sort_values("eta2_model", ascending=False)
        ts = _json("rq3_transfer_summary.json") or {}
        M = _csv("rq3_transfer_matrix.csv")
        out.append("## 5. RQ3 — model style vs language style\n\n![F4](../results/figures/F4_rq3_eta2.png)\n\nPartial η² per feature (MEAN row = average over the 21 features):\n\n" + _md(e))
        if M is not None:
            M = M.rename(columns={M.columns[0]: "train \\ test"})
            out.append("\nCross-lingual transfer (rows = training language, columns = test language, within-language z-scored; diagonal = LOPO-CV):\n\n" + _md(M, "{:.2f}") +
                       f"\n\nMean off-diagonal accuracy {ts.get('mean_offdiag_accuracy', float('nan')):.3f} vs diagonal {ts.get('mean_diag_accuracy', float('nan')):.3f}; "
                       f"{ts.get('n_offdiag_above_chance')} of {ts.get('n_offdiag')} off-diagonal cells above chance (0.20).\n\n![F5](../results/figures/F5_rq3_transfer.png)\n\n" + sec["rq3"])

    # ---- RQ4
    sep = _csv("rq4_separation.csv")
    if sep is not None:
        s4 = _json("rq4_summary.json") or {}
        t = sep[["lang", "rank", "centroid_dist", "centroid_dist_ci_lo", "centroid_dist_ci_hi", "silhouette", "silhouette_ci_lo", "silhouette_ci_hi", "between_within_ratio"]]
        rows = [{"metric": k, "Spearman ρ vs rank": f"{v['spearman_rho_vs_rank']:.2f}", "p": f"{v['p']:.3f}", "English": f"{v['english']:.3f}", "Hindi": f"{v['lowest_resource']:.3f}"} for k, v in s4.items()]
        out.append("## 6. RQ4 — convergence in low-resource languages\n\n![F6](../results/figures/F6_rq4_separation.png)\n\n" + _md(t) + "\n\n" + _md(pd.DataFrame(rows)) + "\n\n![F7](../results/figures/F7_pca_by_language.png)\n\n" + sec["rq4"])
        pw = _csv("rq4_pairwise.csv")
        if pw is not None:
            pw["pair"] = pw["model_a"] + "–" + pw["model_b"]
            pp = pw.pivot(index="pair", columns="lang", values="centroid_dist")[langs].reset_index()
            out.append("\nPairwise centroid distances (within-language z-scored units):\n\n" + _md(pp, "{:.2f}"))

    # ---- RQ5
    t1 = _csv("rq5_translation_accuracy.csv")
    if t1 is not None:
        s5 = _json("rq5_summary.json") or {}
        t = t1[["translator", "lang", "rank", "n", "acc_translated_lopo", "ci_lo", "ci_hi", "acc_english_originals", "acc_native_same_lang", "acc_train_native_test_translated", "acc_train_english_test_translated"]]
        srows = [{"translator": k, **{kk: f"{vv:.3f}" if isinstance(vv, float) else vv for kk, vv in v.items()}} for k, v in s5.items()]
        out.append("## 7. RQ5 — does translation destroy the fingerprint?\n\n![F8](../results/figures/F8_rq5_translation.png)\n\n" + _md(t) + "\n\nSummary per translator:\n\n" + _md(pd.DataFrame(srows)) + "\n\n![F9](../results/figures/F9_rq5_feature_survival.png)\n\n" + sec["rq5"])
        t3 = _csv("rq5_feature_survival.csv")
        if t3 is not None:
            fs = t3.groupby(["translator", "feature"])["spearman_rho"].mean().unstack(0).sort_values(t3["translator"].unique()[0], ascending=False).reset_index()
            out.append("\nMean Spearman ρ between original and translation, per feature (averaged over the six target languages):\n\n" + _md(fs, "{:.2f}"))

    out.append("## 8. Limitations\n\n" + sec["limitations"])
    out.append("## 9. Reproduction\n\n```\npip install -r requirements.txt && cp .env.example .env   # add OpenRouter key\npython -m langllm.prompts && python -m langllm.review && python -m langllm.refine\npython -m langllm.collect && python -m langllm.validate && python -m langllm.features\npython -m langllm.analysis && python -m langllm.figures\npython -m langllm.translate && python -m langllm.features --translated\npython -m langllm.analysis_translation && python -m langllm.figures --rq5\n```\n\nRaw responses (`data/raw/`), translations (`data/translated/`), features and every result table are versioned in the repository.")
    text = "\n\n".join(out) + "\n"
    (DOCS / "REPORT.md").write_text(text, encoding="utf-8")
    print("wrote", DOCS / "REPORT.md", len(text), "chars")
    return text


if __name__ == "__main__":
    build()
