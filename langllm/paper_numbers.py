"""Every number the paper cites, generated from results/ into paper/numbers.tex (LaTeX macros)
and docs/PAPER_NUMBERS.md (readable). Rounding is half-up everywhere (one rule, per the
numbers audit). Also computes the few small statistics the audit asked for that no other
module produced: a language-clustered RQ2 GLM and Clopper-Pearson CIs on judge own-recall.

    python -m langllm.paper_numbers
"""
from __future__ import annotations
import json
import re
from decimal import Decimal, ROUND_HALF_UP
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from .config import load_config, resource_rank, language_codes, RESULTS_DIR, ROOT
from .features import FEATURE_NAMES

PAPER = ROOT / "paper"; DOCS = ROOT / "docs"
LANG = {"en": "English", "es": "Spanish", "zh": "Chinese", "ru": "Russian", "ja": "Japanese", "tr": "Turkish", "hi": "Hindi"}
MODEL = {"gpt": "GPT-5.5", "gemini": "Gemini 3.5 Flash", "claude": "Claude Opus 4.7", "grok": "Grok 4.3", "deepseek": "DeepSeek V4 Pro"}
FEAT = {"mattr": "MATTR", "hapax_rate": "hapax rate", "mean_token_len": "token length", "zipf_slope": "Zipf slope", "sent_len_mean": "sentence length",
        "sent_len_sd": "sentence-length SD", "burstiness": "burstiness", "dep_depth": "dependency depth", "subord_rate": "subordination",
        "func_word_ratio": "function-word ratio", "first_person_rate": "first-person rate", "para_count": "paragraph count", "para_len_mean": "paragraph length",
        "question_rate": "question rate", "connective_rate": "connective rate", "comma_per_1k": "comma rate", "colon_per_1k": "colon rate",
        "dash_per_1k": "dash rate", "semicolon_per_1k": "semicolon rate", "bigram_entropy": "char-bigram entropy", "digit_rate": "digit rate"}


def r(x, nd=3):
    return str(Decimal(str(float(x))).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))


def d3(x): return r(x, 3).lstrip("0") if float(x) < 1 else r(x, 3)          # .717
def d2(x): return r(x, 2).lstrip("0") if float(x) < 1 else r(x, 2)
def pct(x, nd=1): return r(100 * float(x), nd) + r"\%"
def pct0(x): return r(100 * float(x), 0) + r"\%"
def pv(p):
    p = float(p)
    if p < 1e-4: return "$p < 10^{-4}$"
    return f"$p = {r(p, 3)}$" if p >= 0.001 else f"$p = {p:.1e}$"


def csv(n): return pd.read_csv(RESULTS_DIR / n)
def js(n): return json.load(open(RESULTS_DIR / n))


def build() -> None:
    cfg = load_config(); rank = resource_rank(cfg); langs = language_codes(cfg)
    M: dict[str, str] = {}; notes: list[str] = []

    # ---- design & data
    v = csv("validation_summary.csv"); val = pd.read_csv(ROOT / "data" / "validation.csv")
    M["NResponses"] = str(int(val["keep"].sum())); M["NCollected"] = str(len(val)); M["NTranslations"] = "1,440"; M["NJudgments"] = str(5 * int(val["keep"].sum()))
    M["NPrompts"] = "12"; M["NLangs"] = "7"; M["NModels"] = "5"; M["NFeatures"] = str(len(FEATURE_NAMES)); M["Chance"] = "20\\%"

    # ---- RQ1
    acc = csv("rq1_accuracy.csv"); lr = acc[acc.classifier == "logreg"].set_index("lang"); rf = acc[acc.classifier == "rf"].set_index("lang")
    cci = csv("rq7b_cluster_ci.csv"); cf = cci[cci.system == "features_logreg"].set_index("lang")
    for l in langs:
        M[f"LR{l}"] = d3(lr.loc[l, "accuracy"]); M[f"LRlo{l}"] = d2(cf.loc[l, "ci_lo_cluster"]); M[f"LRhi{l}"] = d2(cf.loc[l, "ci_hi_cluster"])
        M[f"Fone{l}"] = d3(lr.loc[l, "macro_f1"]); M[f"RF{l}"] = d3(rf.loc[l, "accuracy"])
    M["LRmin"] = d2(lr["accuracy"].min()); M["LRmax"] = d2(lr["accuracy"].max())
    M["LRminPct"] = pct0(lr["accuracy"].min()); M["LRmaxPct"] = pct0(lr["accuracy"].max())
    M["RFmin"] = d2(rf["accuracy"].min()); M["RFmax"] = d2(rf["accuracy"].max())
    M["ClusterCIminLo"] = d2(cf["ci_lo_cluster"].min()); M["ClusterCIhalfwidth"] = r(((cf["ci_hi_cluster"] - cf["ci_lo_cluster"]) / 2).mean() * 100, 0)
    lc = csv("rq1_accuracy_lenctl.csv"); lcl = lc[lc.classifier == "logreg"]; lcr = lc[lc.classifier == "rf"]
    M["LRlenMin"] = d2(lcl["accuracy"].min()); M["LRlenMax"] = d2(lcl["accuracy"].max()); M["RFlenMin"] = d2(lcr["accuracy"].min()); M["RFlenMax"] = d2(lcr["accuracy"].max())
    rec = {m: [] for m in MODEL}
    for l in langs:
        cm = pd.read_csv(RESULTS_DIR / f"rq1_confusion_{l}.csv", index_col=0)
        for m in MODEL: rec[m].append(cm.loc[m, m] / cm.loc[m].sum())
    for m in MODEL: M[f"Recall{m}Min"] = pct0(min(rec[m])); M[f"Recall{m}Max"] = pct0(max(rec[m]))
    imp = csv("rq1_feature_importance.csv"); top = imp.groupby("feature")["mean_abs_coef"].mean().sort_values(ascending=False)
    M["TopCoefFeatures"] = ", ".join(FEAT[f] for f in top.index[:5]); notes.append(f"mean |coef| ranking: {', '.join(f'{FEAT[f]} {x:.2f}' for f, x in top.items())}")
    pooled = csv("rq7_feature_curve_order.csv").set_index("lang").loc["pooled", "order"].split(" > ")
    M["PooledTopFive"] = ", ".join(FEAT[f] for f in pooled[:5])

    # ---- judges
    j6 = csv("rq6_judge_summary.csv").set_index("judge"); jl = csv("rq6_judge_by_language.csv")
    for j in MODEL:
        M[f"Judge{j}"] = pct(j6.loc[j, "accuracy"]); M[f"Judge{j}Own"] = pct0(j6.loc[j, "own_recall"]); M[f"Judge{j}False"] = pct0(j6.loc[j, "false_self_rate"])
        M[f"Judge{j}FisherP"] = pv(j6.loc[j, "self_recognition_p_fisher"]); M[f"Judge{j}SelfClaim"] = pct0(j6.loc[j, "self_claim_rate"])
    M["JudgeMin"] = pct(j6["accuracy"].min()); M["JudgeMax"] = pct(j6["accuracy"].max())
    for l in langs:
        d = jl[jl.lang == l]; M[f"JudgeMean{l}"] = d3(d["accuracy"].mean()); M[f"JudgeBest{l}"] = d3(d["accuracy"].max()); M[f"JudgeBestName{l}"] = MODEL[d.sort_values("accuracy").iloc[-1]["judge"]]
    gap = [lr.loc[l, "accuracy"] - jl[jl.lang == l]["accuracy"].max() for l in langs]; M["GapJudgeMin"] = r(min(gap) * 100, 0); M["GapJudgeMax"] = r(max(gap) * 100, 0)
    gapm = [lr.loc[l, "accuracy"] - jl[jl.lang == l]["accuracy"].mean() for l in langs]; M["GapJudgeMeanMin"] = r(min(gapm) * 100, 0); M["GapJudgeMeanMax"] = r(max(gapm) * 100, 0)
    own = jl[jl.judge == "claude"].set_index("lang")
    for l in langs:
        k, n = int(round(own.loc[l, "own_recall"] * own.loc[l, "n_own"])), int(own.loc[l, "n_own"]); lo, hi = stats.binomtest(k, n).proportion_ci(0.95)
        M[f"ClaudeOwn{l}"] = pct0(k / n); M[f"ClaudeOwnCI{l}"] = f"[{pct0(lo)}, {pct0(hi)}]"
    M["ClaudeHindiAcc"] = pct(own.loc["hi", "accuracy"]); M["ClaudeEnglishAcc"] = pct(own.loc["en", "accuracy"])

    # ---- n-gram baseline
    ng = csv("rq7_ngram_accuracy.csv"); ch = ng[ng.baseline == "char_ngram"].set_index("lang"); wd = ng[ng.baseline == "word_ngram"].set_index("lang")
    cn = cci[cci.system == "char_ngram"].set_index("lang")
    for l in langs:
        M[f"NG{l}"] = d3(ch.loc[l, "accuracy"]); M[f"NGlo{l}"] = d2(cn.loc[l, "ci_lo_cluster"]); M[f"NGhi{l}"] = d2(cn.loc[l, "ci_hi_cluster"]); M[f"WG{l}"] = d3(wd.loc[l, "accuracy"])
    M["NGmin"] = d2(ch["accuracy"].min()); M["NGmax"] = d2(ch["accuracy"].max()); M["NGmean"] = d2(ch["accuracy"].mean()); M["WGmean"] = d2(wd["accuracy"].mean())
    gapn = [(ch.loc[l, "accuracy"] - lr.loc[l, "accuracy"]) * 100 for l in langs]; M["GapNGmin"] = r(min(gapn), 0); M["GapNGmax"] = r(max(gapn), 0)
    hol = csv("rq7_holm.csv"); fn = hol[hol.family == "features vs char n-gram"]
    M["NGsigLangs"] = ", ".join(LANG[l] for l in fn[fn.significant_holm_05]["lang"]); M["NGsigN"] = str(int(fn.significant_holm_05.sum())); M["HolmN"] = str(len(hol))
    M["FeatVsChanceAllSig"] = "all seven" if hol[hol.family == "features vs chance"].significant_holm_05.all() else "not all"
    M["FeatVsJudgeAllSig"] = "all seven" if hol[hol.family.str.startswith("features vs best judge")].significant_holm_05.all() else "not all"
    g7 = js("rq7b_gradient.json"); M["NGrho"] = r(g7["char_ngram"]["spearman_rho"], 2); M["NGrhoP"] = pv(g7["char_ngram"]["spearman_p"]); M["NGen"] = d3(g7["char_ngram"]["acc_english"]); M["NGhi"] = d3(g7["char_ngram"]["acc_hindi"])
    M["NGglmBeta"] = f"{g7['char_ngram']['glm_beta']:+.3f}"; M["NGglmP"] = pv(g7["char_ngram"]["glm_p"])

    # ---- RQ2
    g = js("rq2_gradient.json"); gl = js("rq2_gradient_lenctl.json"); fg = g7["features_glm"]
    M["Beta"] = f"{fg['beta']:+.3f}"; M["BetaSE"] = r(fg["se"], 3); M["BetaLo"] = f"{fg['ci95'][0]:+.2f}"; M["BetaHi"] = f"{fg['ci95'][1]:+.2f}"; M["BetaP"] = pv(fg["p"])
    M["SteepestDeclinePts"] = r(fg["steepest_decline_points"], 0); M["SteepestDeclineAcc"] = d2(fg["steepest_decline_compatible_acc_at_rank7"])
    M["BetaLen"] = f"{gl['glm_cell_level']['coef_rank_logodds']:+.3f}"; M["BetaLenP"] = pv(gl["glm_cell_level"]["p"])
    M["RhoRQtwo"] = r(g["logreg"]["spearman_rho"], 2); M["RhoRQtwoP"] = pv(g["logreg"]["spearman_p"])
    cells = csv("rq1_cell_correct.csv")
    gL = smf.glm("correct ~ rank", data=cells, family=sm.families.Binomial()).fit(cov_type="cluster", cov_kwds={"groups": cells["lang"].astype("category").cat.codes})
    M["BetaLangSE"] = r(gL.bse["rank"], 3); M["BetaLangP"] = pv(gL.pvalues["rank"])
    cells["cl"] = cells["lang"] + "|" + cells["prompt_id"]
    gLP = smf.glm("correct ~ rank", data=cells, family=sm.families.Binomial()).fit(cov_type="cluster", cov_kwds={"groups": cells["cl"].astype("category").cat.codes})
    M["BetaLangPromptSE"] = r(gLP.bse["rank"], 3); M["BetaLangPromptP"] = pv(gLP.pvalues["rank"])

    # ---- RQ3
    eta = csv("rq3_anova_eta2.csv"); mean = eta[eta.feature == "MEAN"].iloc[0]; e = eta[eta.feature != "MEAN"].set_index("feature")
    M["EtaModel"] = d3(mean.eta2_model); M["EtaLang"] = d2(mean.eta2_lang); M["EtaInter"] = d2(mean.eta2_interaction); M["EtaPrompt"] = d2(mean.eta2_prompt)
    for f in ["mean_token_len", "func_word_ratio", "hapax_rate", "zipf_slope", "mattr", "comma_per_1k", "bigram_entropy", "para_count", "subord_rate", "question_rate", "dep_depth"]:
        M[f"EtaModel{f.replace('_', '')}"] = d2(e.loc[f, "eta2_model"]); M[f"EtaLang{f.replace('_', '')}"] = d2(e.loc[f, "eta2_lang"])
    M["EtaModelSmallMax"] = d2(e.loc[["subord_rate", "question_rate", "dep_depth"], "eta2_model"].max())
    ts = js("rq3_transfer_summary.json"); tt = csv("rq7b_transfer_tests.csv"); tf = tt[tt.representation == "features"]; tn = tt[tt.representation == "char_ngram"]
    M["TransferOff"] = d2(ts["mean_offdiag_accuracy"]); M["TransferDiag"] = d2(ts["mean_diag_accuracy"]); M["TransferMin"] = d2(tf["accuracy"].min()); M["TransferMax"] = d2(tf["accuracy"].max())
    M["TransferSig"] = str(int(tf.significant_holm_05.sum())); M["TransferRatio"] = pct0(ts["mean_offdiag_accuracy"] / ts["mean_diag_accuracy"])
    M["NGTransferOff"] = d2(tn["accuracy"].mean()); M["NGTransferSig"] = str(int(tn.significant_holm_05.sum())); M["NGTransferConst"] = str(int(tn.constant_prediction.sum())); M["NGTransferMax"] = d2(tn["accuracy"].max())
    fair = js("rq7b_ngram_transfer_summary.json")
    M["NGFairOff"] = d2(fair["union_vocab_zscored"]["offdiag_mean"]); M["NGFairAbove"] = str(fair["union_vocab_zscored"]["offdiag_n_above_chance"])
    M["PunctDiag"] = d2(fair["script_neutral_punct_digits"]["diag_mean"]); M["PunctOff"] = d2(fair["script_neutral_punct_digits"]["offdiag_mean"])

    # ---- RQ4
    sep = csv("rq4_separation.csv").set_index("lang"); s4 = js("rq4_summary.json"); pw = csv("rq4_pairwise.csv")
    M["CentEn"] = r(sep.loc["en", "centroid_dist"], 2); M["CentHi"] = r(sep.loc["hi", "centroid_dist"], 2); M["CentRho"] = r(s4["centroid_dist"]["spearman_rho_vs_rank"], 2); M["CentP"] = pv(s4["centroid_dist"]["p"])
    M["BWen"] = d2(sep.loc["en", "between_within_ratio"]); M["BWhi"] = d2(sep.loc["hi", "between_within_ratio"]); M["BWrho"] = r(s4["between_within_ratio"]["spearman_rho_vs_rank"], 2)
    M["SilEn"] = r(sep.loc["en", "silhouette"], 2); M["SilHi"] = r(sep.loc["hi", "silhouette"], 2); M["SilRho"] = r(s4["silhouette"]["spearman_rho_vs_rank"], 2); M["SilP"] = pv(s4["silhouette"]["p"])
    for k, nm in [("centroid_dist", "Cent"), ("between_within_ratio", "BW"), ("silhouette", "Sil")]:
        M[f"{nm}CIsep"] = "yes" if sep.loc["hi", f"{k}_ci_hi"] < sep.loc["en", f"{k}_ci_lo"] else "no"
        M[f"{nm}HiCIhi"] = r(sep.loc["hi", f"{k}_ci_hi"], 2); M[f"{nm}EnCIlo"] = r(sep.loc["en", f"{k}_ci_lo"], 2)
    pw["pair"] = pw.model_a + "-" + pw.model_b; P = pw.pivot(index="pair", columns="lang", values="centroid_dist")
    for a, b in [("claude", "grok"), ("deepseek", "grok"), ("gpt", "grok"), ("gemini", "grok")]:
        M[f"Pair{a}{b}En"] = r(P.loc[f"{a}-{b}", "en"], 2); M[f"Pair{a}{b}Hi"] = r(P.loc[f"{a}-{b}", "hi"], 2)
    en_sorted = P["en"].sort_values(ascending=False); M["PairLargestEn"] = ", ".join(f"{p.replace('-', '--')} ({x:.2f})" for p, x in en_sorted.head(3).items())

    # ---- RQ5
    t5 = csv("rq5_translation_accuracy.csv"); s5 = js("rq5_summary.json"); fs = csv("rq5_feature_survival.csv")
    for t in ("google", "llm"):
        d = t5[t5.translator == t]; T = t.capitalize() if t == "google" else "LLM"
        M[f"Tr{T}Min"] = d2(d["acc_translated_lopo"].min()); M[f"Tr{T}Max"] = d2(d["acc_translated_lopo"].max()); M[f"Tr{T}Mean"] = d3(s5[t]["mean_acc_translated_lopo"])
        M[f"Tr{T}TrainEn"] = d3(s5[t]["mean_acc_train_english_test_translated"]); M[f"Tr{T}TrainNative"] = d3(s5[t]["mean_acc_train_native_test_translated"])
        M[f"Tr{T}EtaBefore"] = d2(s5[t]["mean_eta2_model_before"]); M[f"Tr{T}EtaAfter"] = d2(s5[t]["mean_eta2_model_after"]); M[f"Tr{T}RhoAbove"] = str(s5[t]["features_rho_above_0.5"])
    M["TrAllMin"] = d2(t5["acc_translated_lopo"].min()); M["TrAllMax"] = d2(t5["acc_translated_lopo"].max()); M["TrNativeMean"] = d3(t5["acc_native_same_lang"].mean())
    M["TrLLMHiTrainEn"] = d2(t5[(t5.translator == "llm") & (t5.lang == "hi")]["acc_train_english_test_translated"].iloc[0])
    surv = fs.groupby("feature")["spearman_rho"].mean()
    for f in ["para_count", "para_len_mean", "sent_len_mean", "burstiness", "mattr", "func_word_ratio", "bigram_entropy"]:
        M[f"Surv{f.replace('_', '')}"] = d2(surv[f])
    n7 = csv("rq7_ngram_translation.csv"); gg = n7[n7.translator == "google"].set_index("lang")
    M["NGTrLopoMean"] = d2(n7["acc_translated_lopo"].mean()); M["NGTrLopoMin"] = d2(n7["acc_translated_lopo"].min()); M["NGTrLopoMax"] = d2(n7["acc_translated_lopo"].max())
    nonlat = gg.drop("es")["acc_train_english_test_translated"]; M["NGTrTrainEnNonLatinMin"] = d2(nonlat.min()); M["NGTrTrainEnNonLatinMax"] = d2(nonlat.max()); M["NGTrTrainEnEs"] = d2(gg.loc["es", "acc_train_english_test_translated"])
    M["NGTrTrainEnMean"] = d2(n7["acc_train_english_test_translated"].mean())
    fe = t5[t5.translator == "google"].set_index("lang")["acc_train_english_test_translated"]; M["TrTrainEnMin"] = d2(fe.min()); M["TrTrainEnMax"] = d2(fe.max())

    # ---- RQ7 curve + ablation
    cv = csv("rq7_feature_curve.csv"); c7 = cv[cv.lang != "pooled"]
    k5 = c7[c7.k == 5]; k10 = c7[c7.k == 10]; k21 = c7[c7.k == 21].set_index("lang")
    M["CurveKfiveMin"] = d2(k5["macro_f1"].min()); M["CurveKfiveMax"] = d2(k5["macro_f1"].max())
    within = max(k21.loc[l, "macro_f1"] - k10[k10.lang == l]["macro_f1"].iloc[0] for l in langs); M["CurveKtenWithin"] = r(max(within, 0) * 100, 0)
    kbest = c7.loc[c7.groupby("lang")["macro_f1"].idxmax()]; M["CurveJaPeakK"] = str(int(kbest[kbest.lang == "ja"]["k"].iloc[0])); M["CurveJaPeakF1"] = d2(kbest[kbest.lang == "ja"]["macro_f1"].iloc[0])
    ab = csv("rq7_group_ablation.csv"); wo = ab[ab.condition == "without"]; on = ab[ab.condition == "only"]
    M["AblMaxDrop"] = d2(-wo["delta_f1_vs_all"].min()); M["AblStructMin"] = d2(on[on.group == "structure"]["macro_f1"].min()); M["AblStructMax"] = d2(on[on.group == "structure"]["macro_f1"].max())
    M["AblPunctMin"] = d2(on[on.group == "punctuation"]["macro_f1"].min()); M["AblPunctMax"] = d2(on[on.group == "punctuation"]["macro_f1"].max())
    M["AblLexMin"] = d2(on[on.group == "lexical"]["macro_f1"].min()); M["AblLexMax"] = d2(on[on.group == "lexical"]["macro_f1"].max())

    # ---- write numbers.tex
    PAPER.mkdir(exist_ok=True)
    lines = ["% GENERATED by python -m langllm.paper_numbers from results/. Do not edit by hand.", "% Rounding: half-up. Accuracies as .xxx, percentages as xx.x\\%."]
    for k, val in M.items():
        k = re.sub(r"\d", lambda m: "abcdefghij"[int(m.group())], k)  # LaTeX macro names cannot contain digits
        lines.append(f"\\newcommand{{\\{k}}}{{{val}}}")
    (PAPER / "numbers.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ---- write PAPER_NUMBERS.md
    md = ["# LangLLM: every number for the paper (generated)", "", f"Source of truth: `results/`. Regenerate with `python -m langllm.paper_numbers`. Macros in `paper/numbers.tex`.", ""]
    md.append("## Table 1 (per language)\n\n| Language | Rank | LR acc [cluster 95% CI] | macro-F1 | RF | char n-gram [CI] | word n-gram | judge mean of 5 | best judge | centroid sep. |\n|---|---|---|---|---|---|---|---|---|---|")
    for l in langs:
        md.append(f"| {LANG[l]} | {rank[l]} | {M['LR'+l]} [{M['LRlo'+l]}, {M['LRhi'+l]}] | {M['Fone'+l]} | {M['RF'+l]} | {M['NG'+l]} [{M['NGlo'+l]}, {M['NGhi'+l]}] | {M['WG'+l]} | {M['JudgeMean'+l]} | {M['JudgeBest'+l]} ({M['JudgeBestName'+l]}) | {r(sep.loc[l,'centroid_dist'],2)} |")
    md += ["", "## Holm-corrected headline comparisons (28 tests)", "", hol[["family", "lang", "effect", "p_raw", "p_holm", "significant_holm_05"]].round(4).to_markdown(index=False), ""]
    md += ["## Per-judge (RQ6, single-text protocol, reasoning off)", "", j6.reset_index()[["judge", "n", "accuracy", "p_vs_chance", "own_recall", "false_self_rate", "self_recognition_p_fisher", "self_claim_rate", "unparsed_rate"]].round(4).to_markdown(index=False), ""]
    md += ["## Claude own-text recall per language (n = 24 each; Clopper-Pearson 95% CI)", ""] + [f"- {LANG[l]}: {M['ClaudeOwn'+l]} {M['ClaudeOwnCI'+l]}" for l in langs] + [""]
    md += ["## Transfer matrices", "", "Features (within-language z-scored):", "", pd.read_csv(RESULTS_DIR / "rq3_transfer_matrix.csv", index_col=0).round(2).to_markdown(), "",
           "Char n-gram, naive (vocabulary from train language only):", "", pd.read_csv(RESULTS_DIR / "rq7_ngram_transfer_matrix.csv", index_col=0).round(2).to_markdown(), "",
           "Char n-gram, fair (union vocabulary, z-scored within language; diagonal = LOPO without z-scoring, reference only):", "", pd.read_csv(RESULTS_DIR / "rq7b_ngram_transfer_union_vocab_zscored.csv", index_col=0).round(2).to_markdown(), "",
           "Script-neutral char model (punctuation, digits, whitespace only):", "", pd.read_csv(RESULTS_DIR / "rq7b_ngram_transfer_script_neutral_punct_digits.csv", index_col=0).round(2).to_markdown(), ""]
    md += ["## Translation (RQ5 and n-gram counterpart)", "", t5[["translator", "lang", "acc_translated_lopo", "ci_lo", "ci_hi", "acc_english_originals", "acc_native_same_lang", "acc_train_native_test_translated", "acc_train_english_test_translated"]].round(3).to_markdown(index=False), "", n7.round(3).to_markdown(index=False), ""]
    md += ["## Feature-selection curve (macro-F1, nested)", "", cv.pivot(index="lang", columns="k", values="macro_f1").round(2).to_markdown(), "", "Consensus orders:", ""] + [f"- {row.lang}: {row.order}" for row in csv("rq7_feature_curve_order.csv").itertuples()] + [""]
    md += ["## Group ablation (macro-F1)", "", "Only this group:", "", on.pivot(index="group", columns="lang", values="macro_f1").round(2).to_markdown(), "", "Without this group (delta vs all 21):", "", wo.pivot(index="group", columns="lang", values="delta_f1_vs_all").round(3).to_markdown(), ""]
    md += ["## RQ2 gradient", "", json.dumps(g7, indent=1), "", f"Language-clustered GLM: beta {M['Beta']}, SE {M['BetaLangSE']}, p {M['BetaLangP']}; language x prompt clustered: SE {M['BetaLangPromptSE']}, p {M['BetaLangPromptP']}.", ""]
    md += ["## RQ3 partial eta-squared", "", eta.round(3).to_markdown(index=False), ""]
    md += ["## RQ4 separation", "", sep.reset_index().round(3).to_markdown(index=False), "", P.round(2).to_markdown(), ""]
    md += ["## Feature survival under translation (mean Spearman rho over 6 languages x 2 translators)", "", surv.sort_values(ascending=False).round(2).to_markdown(), ""]
    md += ["## Notes from the audits", ""] + [f"- {n}" for n in notes] + [
        "- RQ2: report beta with 95% CI and the steepest compatible decline; three clusterings (prompt / language / language x prompt) all give p > 0.3.",
        "- RQ6 is the single-text protocol (Bai et al.); CompLLM's headline lineup allows reasoning and shows five responses side by side. CompLLM's single-text condition matches ours.",
        "- 'n-grams transfer at chance' is NOT supported once n-grams get within-language adaptation (0.41 vs 0.49 for features); the naive figure (0.28, 14 constant-prediction cells) is a vocabulary-overlap failure.",
        "- Novelty narrows to: same-definition features in every language, content held fixed, resource gradient, convergence. La Cava et al. (ACL 2026) and Sun et al. (ICML 2025) must be cited as prior multilingual / translation attribution.",
        "- Rounding rule everywhere: half-up.",
    ]
    (DOCS / "PAPER_NUMBERS.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"wrote {PAPER / 'numbers.tex'} ({len(M)} macros) and {DOCS / 'PAPER_NUMBERS.md'}")


if __name__ == "__main__":
    build()
