"""Conference poster (48 × 36 in landscape) from results/figures + summary numbers.

    python -m langllm.poster      # -> docs/LangLLM_poster_URTC2026.pdf
"""
from __future__ import annotations
import json
import pandas as pd
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Frame, Image, Spacer, Table, TableStyle
from .config import RESULTS_DIR, FIG_DIR, ROOT

OUT = ROOT / "docs" / "LangLLM_poster_URTC2026.pdf"
W, H = 48 * inch, 36 * inch
INK, INK2, MUTE, RULE = HexColor("#1E2430"), HexColor("#4A5160"), HexColor("#7A8090"), HexColor("#C9C8C0")
ACCENT, BG, TILE = HexColor("#3F66A8"), HexColor("#F6F5F1"), HexColor("#FFFFFF")
GAP = 0.45 * inch

S = {
    "h": ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=46, leading=52, textColor=ACCENT, spaceAfter=14),
    "b": ParagraphStyle("b", fontName="Helvetica", fontSize=30, leading=38, textColor=INK, spaceAfter=12),
    "bs": ParagraphStyle("bs", fontName="Helvetica", fontSize=26, leading=33, textColor=INK2, spaceAfter=10),
    "cap": ParagraphStyle("cap", fontName="Helvetica-Oblique", fontSize=23, leading=29, textColor=MUTE, spaceAfter=18),
    "num": ParagraphStyle("num", fontName="Helvetica-Bold", fontSize=58, leading=62, textColor=INK),
    "numcap": ParagraphStyle("numcap", fontName="Helvetica", fontSize=20, leading=25, textColor=INK2),
    "eyebrow": ParagraphStyle("eyebrow", fontName="Helvetica-Bold", fontSize=14, leading=17, textColor=ACCENT),
}


def img(name, width):
    from PIL import Image as PILImage
    p = FIG_DIR / f"{name}.png"
    w, h = PILImage.open(p).size
    return Image(str(p), width=width, height=width * h / w)


def build():
    acc = pd.read_csv(RESULTS_DIR / "rq1_accuracy.csv"); lr = acc[acc.classifier == "logreg"]
    g = json.load(open(RESULTS_DIR / "rq2_gradient.json")); eta = pd.read_csv(RESULTS_DIR / "rq3_anova_eta2.csv")
    ts = json.load(open(RESULTS_DIR / "rq3_transfer_summary.json")); s4 = json.load(open(RESULTS_DIR / "rq4_summary.json"))
    s5 = json.load(open(RESULTS_DIR / "rq5_summary.json")); j6 = pd.read_csv(RESULTS_DIR / "rq6_judge_summary.csv").set_index("judge")
    mean = eta[eta.feature == "MEAN"].iloc[0]

    c = canvas.Canvas(str(OUT), pagesize=(W, H))
    c.setFillColor(BG); c.rect(0, 0, W, H, fill=1, stroke=0)
    # ---- title band
    c.setFillColor(TILE); c.rect(0, H - 5.1 * inch, W, 5.1 * inch, fill=1, stroke=0)
    c.setFillColor(ACCENT); c.rect(0, H - 5.1 * inch, W, 0.12 * inch, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 78)
    c.drawString(1.2 * inch, H - 2.0 * inch, "Do LLM fingerprints survive outside English?")
    c.setFont("Helvetica", 34); c.setFillColor(INK2)
    c.drawString(1.2 * inch, H - 2.85 * inch, "Interpretable attribution of five frontier models across seven languages, under translation, and against the models themselves as judges")
    c.setFont("Helvetica", 26); c.setFillColor(INK)
    c.drawString(1.2 * inch, H - 3.75 * inch, "Adrian Erlikhman¹ · Michael Tarekegn¹ · Philo Juang²        ¹ LACES, Los Angeles   ² UCLA")
    c.setFont("Helvetica", 20); c.setFillColor(MUTE)
    c.drawString(1.2 * inch, H - 4.45 * inch, "IEEE MIT Undergraduate Research Technology Conference 2026 · Technology of Computation · github.com/adrian-erlikhman/LangLLM")

    # ---- headline tiles across the top
    tiles = [
        (f"{lr['accuracy'].min():.0%}–{lr['accuracy'].max():.0%}", "five-way attribution accuracy from 21 interpretable features, in every one of 7 languages (chance 20%)"),
        (f"p = {g['glm_cell_level']['p']:.2f}", "no resource gradient: accuracy does not fall from English to Hindi (cell-level GLM, n = 839)"),
        (f"{ts['n_offdiag_above_chance']}/{ts['n_offdiag']}", "cross-lingual transfers above chance: the fingerprint is largely language-invariant (mean 0.49)"),
        (f"ρ = {s4['centroid_dist']['spearman_rho_vs_rank']:.2f}", "models converge stylistically as resources fall: separation shrinks monotonically to Hindi"),
        (f"{s5['google']['mean_acc_translated_lopo']:.0%}", "attribution after Google Translate; English-trained classifier reads translations at 66%"),
        (f"{j6.loc['claude', 'accuracy']:.0%} vs 20%", "only Claude beats chance as a judge of authorship; the other four default to one fixed answer"),
    ]
    tw = (W - 2.4 * inch - 5 * 0.3 * inch) / 6
    y0 = H - 5.1 * inch - 0.35 * inch
    for i, (n, capt) in enumerate(tiles):
        x = 1.2 * inch + i * (tw + 0.3 * inch)
        c.setFillColor(TILE); c.roundRect(x, y0 - 2.7 * inch, tw, 2.7 * inch, 6, fill=1, stroke=0)
        c.setFillColor(ACCENT); c.rect(x, y0 - 0.06 * inch, tw, 0.06 * inch, fill=1, stroke=0)
        f = Frame(x + 0.2 * inch, y0 - 2.7 * inch, tw - 0.4 * inch, 2.65 * inch, showBoundary=0, leftPadding=0, rightPadding=0, topPadding=8, bottomPadding=4)
        f.addFromList([Paragraph(n, S["num"]), Spacer(1, 4), Paragraph(capt, S["numcap"])], c)

    # ---- four columns
    top = y0 - 2.7 * inch - 0.45 * inch
    bottom = 0.9 * inch
    cw = (W - 2.4 * inch - 3 * GAP) / 4
    cols = [1.2 * inch + i * (cw + GAP) for i in range(4)]
    fw = cw  # figure width inside a column

    col1 = [
        Paragraph("Why", S["h"]),
        Paragraph("Provenance tools are built and tested in English, but the need to attribute text to a specific model — disinformation tracing, academic integrity, moderation — is mostly non-English. Detection is known to weaken off English; attribution to a <i>specific</i> model has been English-only and black-box.", S["b"]),
        Paragraph("Nobody had measured attribution with <b>interpretable</b> features across a resource gradient, separated model style from language style, tested convergence in low-resource languages, or checked whether translation launders the signal.", S["b"]),
        Spacer(1, 18),
        Paragraph("Design", S["h"]),
        Paragraph("<b>5 models</b>: GPT-5.5 · Gemini 3.5 Flash · Claude Opus 4.7 · Grok 4.3 · DeepSeek V4 Pro (one OpenRouter key; served model strings logged).", S["b"]),
        Paragraph("<b>7 languages</b> in decreasing training-data share: English → Spanish → Chinese → Russian → Japanese → Turkish → Hindi.", S["b"]),
        Paragraph("<b>12 essay prompts</b>, each fixing a topic, a stance (6 for / 6 against) and three supporting points. A non-subject model (Llama 4) writes a native version of each prompt in every language — never a translation — and a third-family reviewer (Qwen) verifies every version against the original. Content is held fixed; only style is free.", S["b"]),
        Paragraph("<b>840 responses</b> (× 2 generations), no system prompt, temperature 0.7, reasoning traces excluded. 839 pass language ID, length and refusal checks.", S["b"]),
        Spacer(1, 18),
        Paragraph("21 features, one definition in every language", S["h"]),
        Paragraph("All text parsed with Stanza on Universal Dependencies, so each feature means the same thing in Chinese, Turkish or Hindi.", S["b"]),
        Paragraph("<b>Lexical</b> MATTR · hapax rate · token length · Zipf slope<br/><b>Syntactic</b> sentence length μ, σ · burstiness · dependency depth · subordination · function-word ratio · first person<br/><b>Structure</b> paragraph count, length · question rate · connectives<br/><b>Punctuation</b> comma · colon · dash · semicolon per 1k, script equivalents mapped<br/><b>Character</b> bigram entropy · digit rate", S["bs"]),
        Paragraph("English-only measures (Flesch, Fog, hedges, passive, contractions) are deliberately excluded. All tests pre-specified before collection.", S["bs"]),
    ]
    col2 = [
        Paragraph("1 · Attribution works in every language", S["h"]),
        img("F1_rq1_accuracy", fw),
        Paragraph("Leave-one-prompt-out CV; logistic regression on standardised features (interpretable) and random forest (ceiling). Every CI excludes chance. GPT and Grok are most identifiable; DeepSeek the blur.", S["cap"]),
        Paragraph("2 · … and does not fade with resource level", S["h"]),
        img("F3_rq2_gradient", fw * 0.92),
        Paragraph(f"Spearman ρ = {g['logreg']['spearman_rho']:.2f} (p = {g['logreg']['spearman_p']:.2f}); cell-level GLM β = {g['glm_cell_level']['coef_rank_logodds']:+.3f} log-odds per rank (p = {g['glm_cell_level']['p']:.2f}). Japanese matches English; Hindi beats Spanish. The pre-registered gradient hypothesis is <b>not</b> supported.", S["cap"]),
        Paragraph("The fingerprint is structural: paragraph count, comma and colon density, and lexical-diversity slope carry it; dependency depth and subordination barely contribute.", S["b"]),
    ]
    col3 = [
        Paragraph("3 · Model style is mostly language-invariant", S["h"]),
        img("F5_rq3_transfer", fw * 0.92),
        Paragraph(f"Language explains most feature variance (mean partial η² {mean.eta2_lang:.2f} vs {mean.eta2_model:.2f} for model, {mean.eta2_interaction:.2f} interaction). But remove each language's mean and a classifier trained on any language beats chance on every other: {ts['n_offdiag_above_chance']}/{ts['n_offdiag']} pairs, mean {ts['mean_offdiag_accuracy']:.2f} vs {ts['mean_diag_accuracy']:.2f} within-language. About three quarters of the fingerprint transfers.", S["cap"]),
        Paragraph("4 · Yet models converge as resources fall", S["h"]),
        img("F6_rq4_separation", fw),
        Paragraph(f"Within-language separation of the five model centroids falls monotonically from English to Hindi (centroid distance ρ = {s4['centroid_dist']['spearman_rho_vs_rank']:.2f}; between/within ratio {s4['between_within_ratio']['english']:.2f} → {s4['between_within_ratio']['lowest_resource']:.2f}). Almost all of it is Grok's terse English register disappearing into the pack. Convergence in the bulk of features, attribution sustained by a few.", S["cap"]),
    ]
    col4 = [
        Paragraph("5 · Translation does not launder the fingerprint", S["h"]),
        img("F8_rq5_translation", fw),
        Paragraph(f"All 120 English responses translated into the six other languages by Google Translate and by a free open model (MiniMax M3). Attribution on translated text alone: {s5['google']['mean_acc_translated_lopo']:.2f} / {s5['llm']['mean_acc_translated_lopo']:.2f}. An <b>English-trained</b> classifier reads the translations at {s5['google']['mean_acc_train_english_test_translated']:.2f}: structure (paragraph count ρ = 1.00, sentence length 0.89) survives; vocabulary is rewritten (MATTR 0.3).", S["cap"]),
        Paragraph("6 · Baseline: the models themselves cannot do this", S["h"]),
        img("F10_rq6_judge", fw),
        Paragraph(f"Each model asked which of the five wrote each text (reasoning off, options shuffled). GPT {j6.loc['gpt','accuracy']:.1%}, Grok {j6.loc['grok','accuracy']:.1%}, Gemini {j6.loc['gemini','accuracy']:.1%}, DeepSeek {j6.loc['deepseek','accuracy']:.1%}: chance, each defaulting to one answer (GPT names itself 82% of the time). Claude {j6.loc['claude','accuracy']:.1%} is the only judge above chance, and only just. The fingerprint is real but not one the models read off their own output.", S["cap"]),
        Spacer(1, 6),
        Paragraph("Takeaways", S["h"]),
        Paragraph("• Interpretable, UD-based features attribute LLM text in every language and beat every LLM judge by 35–50 points.<br/>• Fingerprints do not fade with resource level and survive translation — provenance across a language boundary works from an English-trained model.<br/>• Low-resource registers are flattening: the five models write more alike in Hindi than in English.<br/>• Limits: one genre; length is part of the linear signal; ordinal resource rank; dated model snapshots.", S["b"]),
    ]
    for x, items in zip(cols, [col1, col2, col3, col4]):
        Frame(x, bottom, cw, top - bottom, showBoundary=0, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0).addFromList(items, c)
    c.setFillColor(MUTE); c.setFont("Helvetica", 16)
    c.drawString(1.2 * inch, 0.45 * inch, "Data, prompts, code, all responses and translations: github.com/adrian-erlikhman/LangLLM · analysis plan pre-specified 3 Sep 2026 · contact erlikhman.adrian@gmail.com")
    c.showPage(); c.save()
    print("wrote", OUT)


if __name__ == "__main__":
    build()
