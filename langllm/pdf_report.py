"""Build docs/LangLLM_results.pdf — methodology, every result table, all figures, interpretation.

    python -m langllm.pdf_report
"""
from __future__ import annotations
import datetime as dt
import json
import re
from pathlib import Path
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak,
                                KeepTogether, ListFlowable, ListItem, CondPageBreak)
from reportlab.lib.utils import ImageReader
from .config import load_config, RESULTS_DIR, FIG_DIR, ROOT, resource_rank

DOCS = ROOT / "docs"
OUT = DOCS / "LangLLM_results.pdf"
LANG_NAME = {"en": "English", "es": "Spanish", "zh": "Chinese", "ru": "Russian", "ja": "Japanese", "tr": "Turkish", "hi": "Hindi"}
MODEL_NAME = {"gpt": "GPT-5.5", "gemini": "Gemini 3.5 Flash", "claude": "Claude Opus 4.7", "grok": "Grok 4.3", "deepseek": "DeepSeek V4 Pro"}

# ---------------------------------------------------------------------------- fonts
def _fonts():
    import matplotlib
    d = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
    pdfmetrics.registerFont(TTFont("Serif", str(d / "DejaVuSerif.ttf")))
    pdfmetrics.registerFont(TTFont("Serif-Bold", str(d / "DejaVuSerif-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Serif-Italic", str(d / "DejaVuSerif-Italic.ttf")))
    pdfmetrics.registerFont(TTFont("Sans", str(d / "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("Sans-Bold", str(d / "DejaVuSans-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Mono", str(d / "DejaVuSansMono.ttf")))
    from reportlab.pdfbase.pdfmetrics import registerFontFamily
    registerFontFamily("Serif", normal="Serif", bold="Serif-Bold", italic="Serif-Italic", boldItalic="Serif-Bold")
    registerFontFamily("Sans", normal="Sans", bold="Sans-Bold", italic="Sans", boldItalic="Sans-Bold")


INK = colors.HexColor("#1E2430"); INK2 = colors.HexColor("#4A5160"); MUTE = colors.HexColor("#7A8090")
RULE = colors.HexColor("#C9C8C0"); ACCENT = colors.HexColor("#3F66A8"); BG2 = colors.HexColor("#EFEEE9")

S = {}


def _styles():
    S["title"] = ParagraphStyle("title", fontName="Serif-Bold", fontSize=24, leading=29, textColor=INK, spaceAfter=8)
    S["sub"] = ParagraphStyle("sub", fontName="Serif", fontSize=12.5, leading=17, textColor=INK2, spaceAfter=14)
    S["eyebrow"] = ParagraphStyle("eyebrow", fontName="Mono", fontSize=8, leading=11, textColor=MUTE, spaceAfter=4)
    S["h1"] = ParagraphStyle("h1", fontName="Serif-Bold", fontSize=15, leading=19, textColor=INK, spaceBefore=16, spaceAfter=8)
    S["h2"] = ParagraphStyle("h2", fontName="Sans-Bold", fontSize=10.5, leading=14, textColor=INK, spaceBefore=10, spaceAfter=4)
    S["body"] = ParagraphStyle("body", fontName="Serif", fontSize=9.6, leading=13.6, textColor=INK, spaceAfter=6, alignment=TA_LEFT)
    S["small"] = ParagraphStyle("small", fontName="Sans", fontSize=8, leading=10.5, textColor=INK2, spaceAfter=4)
    S["cap"] = ParagraphStyle("cap", fontName="Sans", fontSize=8, leading=10.5, textColor=MUTE, spaceBefore=3, spaceAfter=10)
    S["tcap"] = ParagraphStyle("tcap", fontName="Sans-Bold", fontSize=8, leading=10.5, textColor=INK2, spaceBefore=8, spaceAfter=3)
    S["cell"] = ParagraphStyle("cell", fontName="Sans", fontSize=7.4, leading=9, textColor=INK)
    S["cellb"] = ParagraphStyle("cellb", fontName="Sans-Bold", fontSize=7.4, leading=9, textColor=INK2)
    S["mono"] = ParagraphStyle("mono", fontName="Mono", fontSize=7.6, leading=10, textColor=INK, backColor=BG2, borderPadding=6, spaceBefore=4, spaceAfter=10)
    S["tile_num"] = ParagraphStyle("tn", fontName="Serif-Bold", fontSize=13, leading=16, textColor=INK)
    S["tile_cap"] = ParagraphStyle("tc", fontName="Sans", fontSize=7.4, leading=9.4, textColor=INK2)
    S["bullet"] = ParagraphStyle("bullet", parent=S["body"], spaceAfter=3)


# ---------------------------------------------------------------------------- helpers
def _csv(n):
    p = RESULTS_DIR / n
    return pd.read_csv(p) if p.exists() else None


def _json(n):
    p = RESULTS_DIR / n
    return json.load(open(p)) if p.exists() else None


def esc(s) -> str:
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def md(s: str) -> str:
    """Markdown-ish inline → reportlab markup."""
    t = esc(s)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*(?!\*)(.+?)\*", r"<i>\1</i>", t)
    t = re.sub(r"`(.+?)`", r'<font face="Mono" size="8.4">\1</font>', t)
    return t


def md_blocks(text: str) -> list:
    """Paragraphs and bullet lists from the interpretation file."""
    out, para, items = [], [], []

    def flush_para():
        nonlocal para
        if para:
            out.append(Paragraph(md(" ".join(para)), S["body"])); para = []

    def flush_list():
        nonlocal items
        if items:
            out.append(ListFlowable([ListItem(Paragraph(md(i), S["bullet"]), leftIndent=12) for i in items],
                                    bulletType="bullet", bulletFontName="Sans", bulletFontSize=7, leftIndent=12, start="•"))
            out.append(Spacer(1, 4)); items = []
    for line in text.splitlines():
        if line.startswith("* "):
            flush_para(); items.append(line[2:].strip())
        elif line.startswith("  ") and items:
            items[-1] += " " + line.strip()
        elif not line.strip():
            flush_para(); flush_list()
        else:
            flush_list(); para.append(line.strip())
    flush_para(); flush_list()
    return out


def table(df: pd.DataFrame, fmt="{:.3f}", caption: str = "", col_widths=None, first_col_bold=False, font=7.4) -> list:
    d = df.copy()
    for c in d.columns:
        if d[c].dtype.kind == "f":
            d[c] = d[c].map(lambda v: "" if pd.isna(v) else fmt.format(v))
    cs = ParagraphStyle("c", parent=S["cell"], fontSize=font, leading=font + 1.8)
    hs = ParagraphStyle("h", parent=S["cellb"], fontSize=font, leading=font + 1.8)
    data = [[Paragraph(esc(c), hs) for c in d.columns]]
    for r in d.itertuples(index=False):
        data.append([Paragraph(esc(v), ParagraphStyle("cb", parent=cs, fontName="Sans-Bold") if (first_col_bold and i == 0) else cs) for i, v in enumerate(r)])
    t = Table(data, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, 0), 0.9, INK2),
        ("LINEBELOW", (0, 1), (-1, -1), 0.3, RULE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    out = []
    if caption:
        out.append(Paragraph(esc(caption), S["tcap"]))
    out.append(t); out.append(Spacer(1, 8))
    return out


def figure(name: str, caption: str, width=6.9 * inch) -> list:
    p = FIG_DIR / f"{name}.png"
    if not p.exists():
        return []
    iw, ih = ImageReader(str(p)).getSize()
    h = width * ih / iw
    if h > 7.6 * inch:
        h = 7.6 * inch; width = h * iw / ih
    return [KeepTogether([Image(str(p), width=width, height=h), Paragraph(esc(caption), S["cap"])])]


def _footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Sans", 7.5); canvas.setFillColor(MUTE)
    canvas.drawString(0.8 * inch, 0.55 * inch, "LangLLM — Do LLM fingerprints survive outside English?  ·  Adrian Erlikhman  ·  September 2026")
    canvas.drawRightString(letter[0] - 0.8 * inch, 0.55 * inch, f"{doc.page}")
    canvas.restoreState()


# ---------------------------------------------------------------------------- build
def build() -> Path:
    _fonts(); _styles()
    cfg = load_config()
    rank = resource_rank(cfg)
    langs = sorted(cfg["languages"], key=rank.get)
    interp = (DOCS / "REPORT_interpretation.md").read_text(encoding="utf-8")
    sec = {}
    for tag in ("summary", "rq1", "rq2", "rq3", "rq4", "rq5", "limitations"):
        m = interp.split(f"<!-- {tag} -->")
        sec[tag] = m[1].strip() if len(m) > 1 else ""

    acc = _csv("rq1_accuracy.csv"); g = _json("rq2_gradient.json"); eta = _csv("rq3_anova_eta2.csv")
    ts = _json("rq3_transfer_summary.json") or {}; s4 = _json("rq4_summary.json") or {}; s5 = _json("rq5_summary.json") or {}
    v = _csv("validation_summary.csv")
    lr = acc[acc.classifier == "logreg"].set_index("lang") if acc is not None else None
    W = 6.9 * inch
    st = []

    # ---- title
    st.append(Paragraph("LANGLLM · RESULTS REPORT · " + dt.date.today().strftime("%d %B %Y").upper(), S["eyebrow"]))
    st.append(Paragraph("Do LLM fingerprints survive outside English?", S["title"]))
    st.append(Paragraph("Interpretable stylometric attribution of five frontier models across a seven-language resource gradient, with a translation extension. Adrian Erlikhman. Repository: github.com/adrian-erlikhman/LangLLM", S["sub"]))
    tiles = []
    if lr is not None:
        tiles.append(("RQ1", f"{lr['accuracy'].min():.0%}–{lr['accuracy'].max():.0%}", "five-way attribution accuracy in every language (chance 20%)"))
    if g:
        tiles.append(("RQ2", f"β = {g['glm_cell_level']['coef_rank_logodds']:+.3f}", f"log-odds per resource rank, p = {g['glm_cell_level']['p']:.2f}: no gradient"))
    if eta is not None:
        mean = eta[eta.feature == "MEAN"].iloc[0]
        tiles.append(("RQ3", f"η² {mean.eta2_lang:.2f} vs {mean.eta2_model:.2f}", f"language vs model; cross-lingual transfer {ts.get('mean_offdiag_accuracy', 0):.0%}"))
    if s4:
        tiles.append(("RQ4", f"ρ = {s4['centroid_dist']['spearman_rho_vs_rank']:.2f}", "model separation vs rank: models converge as resources fall"))
    if s5:
        ks = list(s5)
        tiles.append(("RQ5", " / ".join(f"{s5[k]['mean_acc_translated_lopo']:.0%}" for k in ks), f"attribution after {' / '.join(ks)} translation (English {s5[ks[0]]['acc_english_originals']:.0%})"))
    cells = [[Paragraph(a, S["eyebrow"]), Paragraph(b, S["tile_num"]), Paragraph(c, S["tile_cap"])] for a, b, c in tiles]
    tt = Table([[cells[i][0] for i in range(len(cells))], [cells[i][1] for i in range(len(cells))], [cells[i][2] for i in range(len(cells))]],
               colWidths=[W / len(cells)] * len(cells), hAlign="LEFT")
    tt.setStyle(TableStyle([("LINEABOVE", (0, 0), (-1, 0), 2, ACCENT), ("BACKGROUND", (0, 0), (-1, -1), BG2),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                            ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8)]))
    st += [tt, Spacer(1, 14)]
    st.append(Paragraph("Summary", S["h1"]))
    st += md_blocks(sec["summary"])

    # ---- 1 design
    st.append(PageBreak())
    st.append(Paragraph("1 · Design and method", S["h1"]))
    st += table(pd.DataFrame([{"model": MODEL_NAME[k], "OpenRouter string": val} for k, val in cfg["models"].items()]),
                caption="Subject models (served through OpenRouter; the served model string is logged per response)", col_widths=[1.6 * inch, 3.2 * inch], first_col_bold=True)
    st += table(pd.DataFrame([{"rank": rank[l], "language": LANG_NAME[l], "Stanza/UD package": cfg["languages"][l]["stanza"], "native length target (in the prompt language)": {"zh": "about 600 characters", "ja": "about 800 characters"}.get(l, "about 350 words")} for l in langs]),
                caption="Languages in decreasing order of approximate training-data share (the RQ2 covariate)", col_widths=[0.5 * inch, 1.1 * inch, 1.3 * inch, 2.9 * inch])
    st.append(Paragraph(md(f"**Cells.** 5 models × 12 prompts × 7 languages × 2 generations = 840 responses. Single user turn, no system prompt, temperature {cfg['generation']['temperature']}, seeds fixed per generation index, reasoning at low effort with the trace excluded (Gemini 3.5 Flash cannot disable reasoning, so this is the one setting all five accept), {cfg['generation']['max_tokens']:,}-token budget."), S["body"]))
    st.append(Paragraph(md(f"**Prompts.** Twelve English schemas each fix a topic, a stance (6 for / 6 against), three sub-claims and a reading-level tier (a prompt control only, since Flesch–Kincaid is English-specific). For every language a non-subject model (`{cfg['prompt_writer']}`) composes a native prompt from the schema, never by translation, so all seven versions share topic, stance and sub-claims and only style is free. A third-family reviewer (`{cfg['prompt_reviewer']}`) extracted topic, stance and points from each native prompt blind and matched them to the schema; failing prompts were regenerated with the reviewer's note as feedback until all 84 passed. Earlier wordings are retained in each prompt record."), S["body"]))
    st.append(Paragraph(md("**Validation.** Language identification (lingua, seven-language closed set, confidence ≥ 0.6), a 150–900 word-equivalent window (Chinese and Japanese converted from characters), a per-language refusal pattern, truncation, and a count of heading or bullet lines."), S["body"]))
    st.append(Paragraph(md("**Features.** Every text is parsed with Stanza on Universal Dependencies (tokenize, pos, lemma, depparse), so each of the 21 features has one definition in all seven languages. English-only measures (Flesch, Fog, hedges, passive rate, contractions) are excluded. Chinese and Japanese are pre-split on their terminal punctuation because Stanza's splitter does not handle it."), S["body"]))
    st += table(pd.DataFrame([
        {"group": "Lexical", "features": "MATTR (window 50); hapax rate; mean token length; Zipf slope"},
        {"group": "Syntactic", "features": "sentence length mean and SD; burstiness; dependency depth; subordinate-clause rate (acl, advcl, ccomp, xcomp, csubj); function-word ratio; first-person rate (Person=1, lexical fallback for zh/ja)"},
        {"group": "Structure", "features": "paragraph count; paragraph length; question rate; connective rate (cc, mark, sentence-initial ADV/CCONJ/SCONJ)"},
        {"group": "Punctuation", "features": "comma, colon, dash, semicolon per 1 000 tokens, with full-width and ideographic script equivalents mapped"},
        {"group": "Character", "features": "character-bigram entropy; digit rate (Unicode Nd per 1 000 characters)"},
    ]), caption="The 21 features", col_widths=[1.0 * inch, 5.9 * inch], first_col_bold=True)
    st.append(Paragraph("Analysis", S["h2"]))
    st += md_blocks("""* **RQ1** — per-language five-way attribution, leave-one-prompt-out (both generations of a prompt stay on one side of the split). Logistic regression on standardised features is the interpretable primary; a random forest is the ceiling. Chance = 0.20; 95% bootstrap CIs; exact binomial tests.
* **RQ2** — Spearman ρ over the seven languages and a cell-level binomial GLM correct ~ rank with prompt-clustered standard errors. Robustness: features residualised on log length within language.
* **RQ3** — per feature, two-way ANOVA (model × language, prompt as blocking factor) with partial η²; and a cross-lingual transfer matrix of within-language z-scored classifiers.
* **RQ4** — within-language model separation after pooled z-scoring: mean pairwise centroid distance, silhouette of model labels, between/within scatter ratio; stratified reflected bootstrap CIs; Spearman against rank.
* **RQ5** (extension suggested by Philo) — every kept English response translated into the six other languages by Google Translate and by a free non-subject, non-Gemini LLM (MiniMax M3; four fallbacks to Llama 4 Maverick). T1: attribution on translated text alone. T2: classifiers trained on native responses in the target language, and on the English originals, applied to the translations. T3: per-feature Spearman ρ between original and translation.
* Pre-specified decision rules are in docs/analysis_plan.md; RQ5 was added to the plan before any translated data existed.""")

    # ---- 2 data quality
    if v is not None:
        st.append(Paragraph("2 · Data quality", S["h1"]))
        st.append(Paragraph("839 of 840 responses are used. Ten DeepSeek cells spent an entire 4 000-token budget on hidden reasoning and returned nothing; they were re-collected at 16 000 tokens, with the override recorded per response. One Grok response to a Hindi prompt came back in English and is excluded. Median hidden reasoning tokens per response: Claude 0, GPT 23, Grok 489, DeepSeek 552, Gemini 1 122.", S["body"]))
        keep = v.pivot(index="model_key", columns="lang", values="keep_rate")[langs]; keep.index = [MODEL_NAME[m] for m in keep.index]
        med = v.pivot(index="model_key", columns="lang", values="median_words")[langs]; med.index = [MODEL_NAME[m] for m in med.index]
        cw = [1.4 * inch] + [0.6 * inch] * 7
        st += table(keep.reset_index().rename(columns={"index": "model"}), "{:.2f}", "Keep rate per model × language (after the re-collection)", cw, True)
        st += table(med.reset_index().rename(columns={"index": "model"}), "{:.0f}", "Median response length in word-equivalents (Chinese and Japanese converted from characters)", cw, True)
        f = pd.read_csv(ROOT / "data" / "features" / "features.csv")
        tok = f.pivot_table(index="model_key", columns="lang", values="n_tokens", aggfunc="median")[langs]; tok.index = [MODEL_NAME[m] for m in tok.index]
        st += table(tok.reset_index().rename(columns={"index": "model"}), "{:.0f}", "Median Stanza tokens per response: GPT-5.5 is the longest and Grok the shortest in every language", cw, True)

    # ---- 3 RQ1
    if lr is not None:
        st.append(CondPageBreak(3.2 * inch)); st.append(Paragraph("3 · RQ1 — attribution within each language", S["h1"]))
        st += figure("F1_rq1_accuracy", "Figure 1. Five-way attribution accuracy per language, leave-one-prompt-out, 95% bootstrap CIs. Dashed line: chance (0.20).")
        t = lr.loc[langs].reset_index()[["lang", "rank", "n", "accuracy", "acc_ci_lo", "acc_ci_hi", "macro_f1"]]
        t["rf"] = acc[acc.classifier == "rf"].set_index("lang").loc[langs]["accuracy"].to_numpy()
        t["lang"] = t["lang"].map(LANG_NAME); t.columns = ["language", "rank", "n", "accuracy (logreg)", "CI lo", "CI hi", "macro-F1", "random forest"]
        st += table(t, caption="Table 3.1. Attribution accuracy (every binomial test against chance has p < 0.001)")
        st += figure("F2_rq1_confusion", "Figure 2. Row-normalised confusion matrices, logistic regression, leave-one-prompt-out.")
        imp = _csv("rq1_feature_importance.csv")
        if imp is not None:
            top = (imp.sort_values(["lang", "mean_abs_coef"], ascending=[True, False]).groupby("lang").head(5)
                      .groupby("lang")["feature"].apply(lambda s: ", ".join(s)).reindex(langs).reset_index())
            top["lang"] = top["lang"].map(LANG_NAME); top.columns = ["language", "five most discriminative features (mean |standardised coefficient| over folds)"]
            st += table(top, caption="Table 3.2. Most discriminative features per language", col_widths=[1.1 * inch, 5.8 * inch], first_col_bold=True)
        st += md_blocks(sec["rq1"])

    # ---- 4 RQ2
    if g:
        st.append(CondPageBreak(3.2 * inch)); st.append(Paragraph("4 · RQ2 — the resource gradient", S["h1"]))
        st += figure("F3_rq2_gradient", "Figure 3. Attribution accuracy against resource rank (1 = English … 7 = Hindi).", width=4.6 * inch)
        gl = _json("rq2_gradient_lenctl.json") or {}
        rows = [{"test": "Spearman ρ, accuracy vs rank (logreg, n = 7)", "estimate": f"{g['logreg']['spearman_rho']:.2f}", "p": f"{g['logreg']['spearman_p']:.3f}"},
                {"test": "Spearman ρ (random forest)", "estimate": f"{g['rf']['spearman_rho']:.2f}", "p": f"{g['rf']['spearman_p']:.3f}"},
                {"test": "OLS slope, accuracy per rank step", "estimate": f"{g['logreg']['ols_slope_per_rank']:+.3f}", "p": f"{g['logreg']['ols_p']:.3f}"},
                {"test": f"Cell-level GLM β(rank), log-odds, n = {g['glm_cell_level']['n_cells']}, prompt-clustered SE", "estimate": f"{g['glm_cell_level']['coef_rank_logodds']:+.3f} (SE {g['glm_cell_level']['se']:.3f})", "p": f"{g['glm_cell_level']['p']:.3f}"}]
        if gl:
            rows.append({"test": "GLM β(rank) with length-residualised features", "estimate": f"{gl['glm_cell_level']['coef_rank_logodds']:+.3f}", "p": f"{gl['glm_cell_level']['p']:.3f}"})
        st += table(pd.DataFrame(rows), caption="Table 4.1. Gradient tests", col_widths=[4.0 * inch, 1.7 * inch, 0.8 * inch])
        lc = _csv("rq1_accuracy_lenctl.csv")
        if lc is not None:
            p2 = lc.pivot(index="lang", columns="classifier", values="accuracy").loc[langs].reset_index()
            p2["lang"] = p2["lang"].map(LANG_NAME); p2.columns = ["language", "logreg, length-residualised", "random forest, length-residualised"]
            st += table(p2, caption="Table 4.2. Robustness: each feature residualised on log length within language", col_widths=[1.2 * inch, 2.0 * inch, 2.2 * inch])
        st += md_blocks(sec["rq2"])

    # ---- 5 RQ3
    if eta is not None:
        st.append(CondPageBreak(3.2 * inch)); st.append(Paragraph("5 · RQ3 — model style vs language style", S["h1"]))
        st += figure("F4_rq3_eta2", "Figure 4. Partial η² per feature for model, language and their interaction (prompt as blocking factor). Label colour = feature group.", width=5.6 * inch)
        e = eta[eta.feature != "MEAN"][["feature", "eta2_model", "eta2_lang", "eta2_interaction", "eta2_prompt", "p_model", "p_interaction"]].sort_values("eta2_model", ascending=False)
        mean = eta[eta.feature == "MEAN"].iloc[0]
        e.columns = ["feature", "η² model", "η² language", "η² model×language", "η² prompt", "p model", "p interaction"]
        st += table(e, caption=f"Table 5.1. Partial η² per feature, sorted by model effect. Mean over 21 features: model {mean.eta2_model:.3f}, language {mean.eta2_lang:.3f}, interaction {mean.eta2_interaction:.3f}.", col_widths=[1.3 * inch] + [0.9 * inch] * 6)
        M = _csv("rq3_transfer_matrix.csv")
        if M is not None:
            M = M.rename(columns={M.columns[0]: "train \\ test"})
            st += figure("F5_rq3_transfer", "Figure 5. Cross-lingual transfer of a within-language z-scored classifier (diagonal = leave-one-prompt-out).", width=4.4 * inch)
            st += table(M, "{:.2f}", f"Table 5.2. Transfer accuracy, rows = training language, columns = test language. Mean off-diagonal {ts.get('mean_offdiag_accuracy', 0):.3f} vs diagonal {ts.get('mean_diag_accuracy', 0):.3f}; {ts.get('n_offdiag_above_chance')}/{ts.get('n_offdiag')} off-diagonal cells above chance.", [1.0 * inch] + [0.6 * inch] * 7, True)
        st += md_blocks(sec["rq3"])

    # ---- 6 RQ4
    sep = _csv("rq4_separation.csv")
    if sep is not None:
        st.append(CondPageBreak(3.2 * inch)); st.append(Paragraph("6 · RQ4 — convergence in low-resource languages", S["h1"]))
        st += figure("F6_rq4_separation", "Figure 6. Three separation metrics against resource rank with reflected bootstrap CIs (1 000 resamples, stratified by model).")
        t = sep.sort_values("rank")[["lang", "rank", "centroid_dist", "centroid_dist_ci_lo", "centroid_dist_ci_hi", "silhouette", "silhouette_ci_lo", "silhouette_ci_hi", "between_within_ratio"]].copy()
        t["lang"] = t["lang"].map(LANG_NAME); t.columns = ["language", "rank", "centroid dist.", "dist. CI lo", "dist. CI hi", "silhouette", "sil. CI lo", "sil. CI hi", "between/within"]
        st += table(t, caption="Table 6.1. Within-language model separation (features z-scored on the pooled language sample)")
        srows = pd.DataFrame([{"metric": k.replace("_", " "), "Spearman ρ vs rank": f"{x['spearman_rho_vs_rank']:.2f}", "p": f"{x['p']:.3f}", "English": f"{x['english']:.3f}", "Hindi": f"{x['lowest_resource']:.3f}"} for k, x in s4.items()])
        st += table(srows, caption="Table 6.2. Trend tests", col_widths=[1.6 * inch, 1.3 * inch, 0.8 * inch, 0.9 * inch, 0.9 * inch])
        pw = _csv("rq4_pairwise.csv")
        if pw is not None:
            pw["pair"] = pw["model_a"].map(MODEL_NAME) + " – " + pw["model_b"].map(MODEL_NAME)
            pp = pw.pivot(index="pair", columns="lang", values="centroid_dist")[langs].reset_index()
            st += table(pp, "{:.2f}", "Table 6.3. Pairwise centroid distance between models, within-language z-scored units", [2.1 * inch] + [0.62 * inch] * 7, True)
        st += figure("F7_pca_by_language", "Figure 7. Within-language PCA of the 21 features; crosses mark model centroids.")
        st += md_blocks(sec["rq4"])

    # ---- 7 RQ5
    t1 = _csv("rq5_translation_accuracy.csv")
    if t1 is not None:
        st.append(CondPageBreak(3.2 * inch)); st.append(Paragraph("7 · RQ5 — does translation destroy the fingerprint?", S["h1"]))
        st += figure("F8_rq5_translation", "Figure 8. Attribution on translated text (blue) against native responses in the same language (grey), the English originals (dotted) and a native-trained classifier applied to the translations (orange).")
        t = t1.sort_values(["translator", "rank"])[["translator", "lang", "n", "acc_translated_lopo", "ci_lo", "ci_hi", "acc_native_same_lang", "acc_train_native_test_translated", "acc_train_english_test_translated"]].copy()
        t["lang"] = t["lang"].map(LANG_NAME)
        t.columns = ["translator", "language", "n", "translated, LOPO", "CI lo", "CI hi", "native, same lang.", "train native → test transl.", "train English → test transl."]
        st += table(t, caption="Table 7.1. Attribution after translation (English originals: 0.717; every binomial test p < 0.001)", col_widths=[0.7 * inch, 0.8 * inch, 0.4 * inch, 0.8 * inch, 0.55 * inch, 0.55 * inch, 0.85 * inch, 1.1 * inch, 1.1 * inch])
        srows = pd.DataFrame([{"translator": k, **{kk.replace("_", " "): (f"{vv:.3f}" if isinstance(vv, float) else vv) for kk, vv in x.items()}} for k, x in s5.items()]).T.reset_index()
        srows.columns = ["quantity"] + list(s5.keys())
        srows = srows[srows["quantity"] != "translator"]
        st += table(srows, caption="Table 7.2. Per-translator summary", col_widths=[3.2 * inch, 1.2 * inch, 1.2 * inch], first_col_bold=True)
        st += figure("F9_rq5_feature_survival", "Figure 9. Which features survive translation: Spearman ρ between each English original and its translation, per target language.", width=6.4 * inch)
        t3 = _csv("rq5_feature_survival.csv")
        if t3 is not None:
            fs = t3.groupby(["translator", "feature"])["spearman_rho"].mean().unstack(0).reset_index().sort_values(t3["translator"].unique()[0], ascending=False)
            st += table(fs, "{:.2f}", "Table 7.3. Mean Spearman ρ between original and translation per feature, averaged over the six target languages (question rate is undefined: the essays contain no questions)", [1.6 * inch, 1.0 * inch, 1.0 * inch], True)
        st += md_blocks(sec["rq5"])

    # ---- 8, 9
    st.append(CondPageBreak(3.2 * inch)); st.append(Paragraph("8 · Limitations", S["h1"]))
    st += md_blocks(sec["limitations"])
    st.append(Paragraph("9 · Reproduction", S["h1"]))
    st.append(Paragraph("Code, prompts, every raw response, translation, feature table and result file are versioned at github.com/adrian-erlikhman/LangLLM. The pipeline is a handful of resumable commands:", S["body"]))
    st.append(Paragraph("python -m langllm.prompts; python -m langllm.review; python -m langllm.refine<br/>python -m langllm.collect; python -m langllm.validate; python -m langllm.features<br/>python -m langllm.analysis; python -m langllm.figures<br/>python -m langllm.translate; python -m langllm.features --translated<br/>python -m langllm.analysis_translation; python -m langllm.figures --rq5<br/>python -m langllm.report; python -m langllm.artifact; python -m langllm.pdf_report", S["mono"]))
    st.append(Paragraph("Total API spend for the study, including prompt writing, review, collection and 1 440 translations, was under fifteen US dollars.", S["small"]))

    # ---- appendix: validation exclusions + univariate F
    bad = v[(v.wrong_language_rate > 0) | (v.refusal_rate > 0) | (v.error_rate > 0) | (v.truncated_rate > 0) | (v.too_short_rate > 0) | (v.too_long_rate > 0)] if v is not None else None
    uni = _csv("rq1_univariate_F.csv")
    if (bad is not None and len(bad)) or uni is not None:
        st.append(CondPageBreak(3.2 * inch)); st.append(Paragraph("Appendix", S["h1"]))
        if bad is not None and len(bad):
            b = bad[["model_key", "lang", "n", "wrong_language_rate", "refusal_rate", "truncated_rate", "too_short_rate", "too_long_rate", "keep_rate"]].copy()
            b["model_key"] = b["model_key"].map(MODEL_NAME); b["lang"] = b["lang"].map(LANG_NAME)
            st += table(b, "{:.2f}", "Table A.1. Model × language cells with any exclusion (final data, after the DeepSeek re-collection)")
        if uni is not None:
            piv = uni.pivot(index="feature", columns="lang", values="F")[langs]
            piv["mean F"] = piv.mean(axis=1)
            piv = piv.sort_values("mean F", ascending=False).reset_index()
            st += table(piv, "{:.1f}", "Table A.2. One-way ANOVA F of each feature by model, within language (higher = more separable by that feature alone)", [1.3 * inch] + [0.62 * inch] * 8, True)

    doc = SimpleDocTemplate(str(OUT), pagesize=letter, leftMargin=0.8 * inch, rightMargin=0.8 * inch, topMargin=0.75 * inch, bottomMargin=0.85 * inch,
                            title="LangLLM — Do LLM fingerprints survive outside English?", author="Adrian Erlikhman", subject="Stylometric attribution of LLMs across languages")
    doc.build(st, onFirstPage=_footer, onLaterPages=_footer)
    print("wrote", OUT, f"{OUT.stat().st_size/1e6:.1f} MB")
    return OUT


if __name__ == "__main__":
    build()
