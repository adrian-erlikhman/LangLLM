"""Conference poster, 48 x 36 in landscape, in the layout used at NeurIPS / ICML poster sessions:
title band with authors, affiliations and a QR code; a TL;DR strip; three numbered columns
(motivation + method with a pipeline diagram; results; results + takeaways); one large figure
per result with a one-sentence caption. Built from results/figures + summary numbers.

The build refuses to finish if any em dash, en dash or arrow glyph survives in the text layer.

    python -m langllm.poster      # -> docs/LangLLM_poster_URTC2026.pdf
"""
from __future__ import annotations
import json
import tempfile
from pathlib import Path
import pandas as pd
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Frame, Image, Spacer, Table, TableStyle, HRFlowable
from .config import RESULTS_DIR, FIG_DIR, ROOT

OUT = ROOT / "docs" / "LangLLM_poster_URTC2026.pdf"
REPO = "https://github.com/adrian-erlikhman/LangLLM"
W, H = 48 * inch, 36 * inch
M = 1.0 * inch
INK, INK2, MUTE = HexColor("#1B2130"), HexColor("#4A5160"), HexColor("#6F7583")
ACCENT, ACCENT2 = HexColor("#2B4C8C"), HexColor("#E8EDF6")
BG, TILE, RULE = white, HexColor("#F4F5F8"), HexColor("#C8CCD6")
FORBIDDEN = "—–→←→⇒"
OVERFLOW: list[str] = []

S = {
    "h": ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=42, leading=48, textColor=ACCENT, spaceBefore=6, spaceAfter=4),
    "b": ParagraphStyle("b", fontName="Helvetica", fontSize=26, leading=33, textColor=INK, spaceAfter=10),
    "bs": ParagraphStyle("bs", fontName="Helvetica", fontSize=24, leading=31, textColor=INK, spaceAfter=6),
    "cap": ParagraphStyle("cap", fontName="Helvetica-Oblique", fontSize=20, leading=25, textColor=MUTE, spaceAfter=10),
    "tldr": ParagraphStyle("tldr", fontName="Helvetica", fontSize=29, leading=37, textColor=INK),
    "tldrh": ParagraphStyle("tldrh", fontName="Helvetica-Bold", fontSize=29, leading=37, textColor=ACCENT),
    "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=23, leading=29, textColor=INK),
    "cellb": ParagraphStyle("cellb", fontName="Helvetica-Bold", fontSize=23, leading=29, textColor=INK),
    "take": ParagraphStyle("take", fontName="Helvetica", fontSize=24, leading=31, textColor=INK),
}


def img(name: str, width: float) -> Image:
    from PIL import Image as PILImage
    p = FIG_DIR / f"{name}.png"
    w, h = PILImage.open(p).size
    return Image(str(p), width=width, height=width * h / w)


def section(title: str) -> list:
    return [Paragraph(title, S["h"]), HRFlowable(width="100%", thickness=2.2, color=ACCENT, spaceBefore=2, spaceAfter=12)]


def kv_table(rows: list[tuple[str, str]], width: float, key_w: float = 3.1 * inch) -> Table:
    data = [[Paragraph(k, S["cellb"]), Paragraph(v, S["cell"])] for k, v in rows]
    t = Table(data, colWidths=[key_w, width - key_w])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -2), 0.8, RULE),
                           ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 8)]))
    return t


def pipeline(width: float) -> Drawing:
    """Two-row flow diagram of the study pipeline."""
    steps = [
        ("12 English prompts", "topic, stance, three supporting points, reading tier, prose only"),
        ("Native prompts, 7 languages", "written from the prompt by Llama 4, never translated; each checked by Qwen 3.7 against the original"),
        ("840 essays", "5 models x 7 languages x 12 prompts x 2 generations; no system prompt"),
        ("Validation", "language ID, 150 to 900 words, refusal and truncation checks; 839 kept"),
        ("Stanza UD parse", "21 features with one definition in every language"),
        ("Pre-registered tests", "RQ1 to RQ6; analysis plan fixed before collection"),
    ]
    cols, gap = 3, 0.35 * inch
    bw = (width - (cols - 1) * gap) / cols
    bh = 2.55 * inch
    rows = 2
    d = Drawing(width, rows * bh + (rows - 1) * gap)
    from reportlab.lib.utils import simpleSplit
    for i, (head, body) in enumerate(steps):
        r, c = divmod(i, cols)
        x = c * (bw + gap)
        y = (rows - 1 - r) * (bh + gap)
        d.add(Rect(x, y, bw, bh, rx=8, ry=8, fillColor=ACCENT2, strokeColor=ACCENT, strokeWidth=1.4))
        d.add(String(x + 14, y + bh - 34, head, fontName="Helvetica-Bold", fontSize=24, fillColor=ACCENT))
        lines = simpleSplit(body, "Helvetica", 19, bw - 28)
        for k, ln in enumerate(lines[:4]):
            d.add(String(x + 14, y + bh - 64 - k * 24, ln, fontName="Helvetica", fontSize=19, fillColor=INK))
        # arrow to the next box
        if i < len(steps) - 1:
            if c < cols - 1:
                ax0, ay = x + bw, y + bh / 2
                d.add(Line(ax0 + 3, ay, ax0 + gap - 10, ay, strokeColor=ACCENT, strokeWidth=3))
                d.add(Polygon([ax0 + gap - 12, ay - 9, ax0 + gap - 12, ay + 9, ax0 + gap - 1, ay], fillColor=ACCENT, strokeColor=ACCENT))
            else:  # wrap: down from end of row 1 to start of row 2
                sx, sy = x + bw / 2, y
                ex, ey = bw / 2, y - gap
                d.add(Line(sx, sy - 3, sx, sy - gap / 2, strokeColor=ACCENT, strokeWidth=3))
                d.add(Line(sx, sy - gap / 2, ex, sy - gap / 2, strokeColor=ACCENT, strokeWidth=3))
                d.add(Line(ex, sy - gap / 2, ex, ey + 12, strokeColor=ACCENT, strokeWidth=3))
                d.add(Polygon([ex - 9, ey + 13, ex + 9, ey + 13, ex, ey + 1], fillColor=ACCENT, strokeColor=ACCENT))
    return d


def qr_png() -> Path:
    import segno
    p = Path(tempfile.gettempdir()) / "langllm_qr.png"
    segno.make(REPO, error="m").save(str(p), scale=12, border=1, dark="#1B2130")
    return p


def fill(c, x, y, w, h, items, name):
    f = Frame(x, y, w, h, showBoundary=0, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    left = list(items)
    f.addFromList(left, c)
    if left:
        OVERFLOW.append(f"{name}: {len(left)} flowables did not fit")


def build() -> None:
    acc = pd.read_csv(RESULTS_DIR / "rq1_accuracy.csv"); lr = acc[acc.classifier == "logreg"].set_index("lang")
    g = json.load(open(RESULTS_DIR / "rq2_gradient.json")); eta = pd.read_csv(RESULTS_DIR / "rq3_anova_eta2.csv")
    ts = json.load(open(RESULTS_DIR / "rq3_transfer_summary.json")); s4 = json.load(open(RESULTS_DIR / "rq4_summary.json"))
    s5 = json.load(open(RESULTS_DIR / "rq5_summary.json")); j6 = pd.read_csv(RESULTS_DIR / "rq6_judge_summary.csv").set_index("judge")
    mean = eta[eta.feature == "MEAN"].iloc[0]
    lo, hi = lr["accuracy"].min(), lr["accuracy"].max()

    c = canvas.Canvas(str(OUT), pagesize=(W, H))
    c.setTitle("Do LLM fingerprints survive outside English?")
    c.setFillColor(BG); c.rect(0, 0, W, H, fill=1, stroke=0)

    # ------------------------------------------------------------------ title band
    band = 5.4 * inch
    c.setFillColor(ACCENT); c.rect(0, H - 0.22 * inch, W, 0.22 * inch, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 86)
    c.drawString(M, H - 1.55 * inch, "Do LLM fingerprints survive outside English?")
    c.setFont("Helvetica", 36); c.setFillColor(INK2)
    c.drawString(M, H - 2.35 * inch, "Interpretable attribution of five frontier models across seven languages, under translation, and against the models as judges")
    c.setFont("Helvetica", 31); c.setFillColor(INK)
    c.drawString(M, H - 3.2 * inch, "Adrian Erlikhman")
    x = M + c.stringWidth("Adrian Erlikhman", "Helvetica", 31); c.setFont("Helvetica", 20); c.drawString(x, H - 3.05 * inch, "1")
    c.setFont("Helvetica", 31); c.drawString(x + 0.55 * inch, H - 3.2 * inch, "Michael Tarekegn")
    x2 = x + 0.55 * inch + c.stringWidth("Michael Tarekegn", "Helvetica", 31); c.setFont("Helvetica", 20); c.drawString(x2, H - 3.05 * inch, "1")
    c.setFont("Helvetica", 31); c.drawString(x2 + 0.55 * inch, H - 3.2 * inch, "Philo Juang")
    x3 = x2 + 0.55 * inch + c.stringWidth("Philo Juang", "Helvetica", 31); c.setFont("Helvetica", 20); c.drawString(x3, H - 3.05 * inch, "2")
    c.setFont("Helvetica", 24); c.setFillColor(INK2)
    c.drawString(M, H - 3.8 * inch, "1 Los Angeles Center for Enriched Studies (LACES)     2 University of California, Los Angeles")
    c.setFont("Helvetica", 22); c.setFillColor(MUTE)
    c.drawString(M, H - 4.45 * inch, "2026 IEEE MIT Undergraduate Research Technology Conference, Technology of Computation")
    # QR + label, right edge
    q = qr_png(); qs = 2.9 * inch
    c.drawImage(str(q), W - M - qs, H - 0.55 * inch - qs, qs, qs)
    c.setFont("Helvetica", 19); c.setFillColor(MUTE)
    c.drawRightString(W - M, H - 0.55 * inch - qs - 0.32 * inch, "code, prompts, all data, full report")
    c.drawRightString(W - M, H - 0.55 * inch - qs - 0.62 * inch, "github.com/adrian-erlikhman/LangLLM")
    c.setStrokeColor(RULE); c.setLineWidth(1.5); c.line(M, H - band, W - M, H - band)

    # ------------------------------------------------------------------ TL;DR strip
    ty, th = H - band - 0.3 * inch, 2.15 * inch
    c.setFillColor(TILE); c.roundRect(M, ty - th, W - 2 * M, th, 10, fill=1, stroke=0)
    c.setFillColor(ACCENT); c.rect(M, ty - th, 0.14 * inch, th, fill=1, stroke=0)
    tldr = [
        Paragraph("TL;DR", S["tldrh"]),
        Paragraph(f"Twenty-one interpretable features defined on Universal Dependencies attribute text to one of five frontier LLMs at {lo:.0%} to {hi:.0%} accuracy in all seven languages (chance 20%), "
                  f"and accuracy does not fall from English to Hindi. The fingerprint is largely language-invariant, survives Google Translate and an LLM translator, "
                  f"and is invisible to the models themselves, which judge authorship at chance. Models do converge stylistically as resources fall, so the register of low-resource languages is flattening.", S["tldr"]),
    ]
    fill(c, M + 0.45 * inch, ty - th + 0.2 * inch, W - 2 * M - 0.9 * inch, th - 0.35 * inch, tldr, "tldr")

    # ------------------------------------------------------------------ columns
    gap = 0.75 * inch
    top = ty - th - 0.45 * inch
    bottom = 0.85 * inch
    cw = (W - 2 * M - 2 * gap) / 3
    cols = [M + i * (cw + gap) for i in range(3)]

    col1 = [
        *section("1  Motivation"),
        Paragraph("Detection of AI-written text is mature and is known to weaken outside English. Attributing a text to a <b>specific</b> model is a different task: it has been studied almost only in English, with opaque embedding classifiers.", S["b"]),
        Paragraph("Yet the need for attribution, in disinformation tracing, academic integrity and moderation, is mostly non-English. If fingerprints fade with a language's training-data share, attribution fails where it matters most. If models converge on one style in low-resource languages, LLM use is flattening the written register of the languages with the least data.", S["b"]),
        Paragraph("No prior work had measured attribution with interpretable features across a resource gradient, separated model style from language style, tested stylistic convergence, or checked whether translation removes the signal.", S["b"]),
        Spacer(1, 14),
        *section("2  Study design"),
        kv_table([
            ("Models", "GPT-5.5, Gemini 3.5 Flash, Claude Opus 4.7, Grok 4.3, DeepSeek V4 Pro, all through one OpenRouter key with served model strings logged"),
            ("Languages", "English, Spanish, Chinese, Russian, Japanese, Turkish, Hindi, in decreasing training-data share (rank 1 to 7)"),
            ("Prompts", "12 persuasive-essay prompts; each fixes a topic, a stance (6 for, 6 against) and three supporting points, so content is held constant and only style varies"),
            ("Generation", "single user turn, no system prompt, temperature 0.7, fixed seeds, hidden reasoning excluded"),
        ], cw),
        Spacer(1, 18),
        pipeline(cw),
        Spacer(1, 18),
        *section("3  Features"),
        Paragraph("Every text is parsed with Stanza on Universal Dependencies, so each feature means the same thing in Chinese, Turkish and Hindi. English-only measures (Flesch, Fog, hedges, passive voice, contractions) are excluded.", S["b"]),
        kv_table([
            ("Lexical", "moving-average type-token ratio, hapax rate, mean token length, Zipf slope"),
            ("Syntactic", "sentence length mean and SD, burstiness, dependency depth, subordinate-clause rate, function-word ratio, first-person rate"),
            ("Structure", "paragraph count and length, question rate, connective rate"),
            ("Punctuation", "comma, colon, dash, semicolon per 1,000 tokens, script equivalents mapped"),
            ("Character", "character-bigram entropy, digit rate"),
        ], cw, key_w=2.9 * inch),
    ]

    col2 = [
        *section("4  Attribution works in every language"),
        img("F1_rq1_accuracy", cw * 0.86),
        Paragraph(f"Five-way accuracy per language, leave-one-prompt-out cross-validation (both generations of a prompt stay on one side). Logistic regression on standardised features is the interpretable primary; a random forest is the ceiling. Every 95% interval excludes chance. GPT-5.5 and Grok 4.3 are the easiest to identify, DeepSeek the blurriest. The signal is structural: paragraph count, comma and colon density and lexical-diversity slope carry most of it; dependency depth and subordination contribute little.", S["cap"]),
        *section("5  No resource gradient"),
        img("F3_rq2_gradient", cw * 0.55),
        Paragraph(f"Spearman rho = {g['logreg']['spearman_rho']:.2f} (p = {g['logreg']['spearman_p']:.2f}) across the seven languages; a cell-level binomial GLM with prompt-clustered errors gives {g['glm_cell_level']['coef_rank_logodds']:+.3f} log-odds per rank step (p = {g['glm_cell_level']['p']:.2f}, n = {g['glm_cell_level']['n_cells']}). Japanese matches English and Hindi exceeds Spanish. The pre-registered gradient hypothesis is not supported.", S["cap"]),
        *section("6  Model style is mostly language-invariant"),
        img("F5_rq3_transfer", cw * 0.6),
        Paragraph(f"Language explains most feature variance (mean partial eta squared {mean.eta2_lang:.2f} for language, {mean.eta2_model:.2f} for model, {mean.eta2_interaction:.2f} for their interaction). Remove each language's mean, and a classifier trained on any one language beats chance on every other: {ts['n_offdiag_above_chance']} of {ts['n_offdiag']} pairs, mean {ts['mean_offdiag_accuracy']:.2f} against {ts['mean_diag_accuracy']:.2f} within language.", S["cap"]),
    ]

    col3 = [
        *section("7  Models converge as resources fall"),
        img("F6_rq4_separation", cw * 0.95),
        Paragraph(f"Within-language separation of the five model centroids falls monotonically from English to Hindi (centroid distance rho = {s4['centroid_dist']['spearman_rho_vs_rank']:.2f}; between-to-within ratio {s4['between_within_ratio']['english']:.2f} in English, {s4['between_within_ratio']['lowest_resource']:.2f} in Hindi). Almost all of the change is Grok's terse English register disappearing into the pack. Convergence in the bulk of features, attribution sustained by a few.", S["cap"]),
        *section("8  Translation does not remove the fingerprint"),
        img("F8_rq5_translation", cw * 0.95),
        Paragraph(f"All 120 English responses were translated into the six other languages by Google Translate and by a free open model (MiniMax M3). Attribution on translated text alone is {s5['google']['mean_acc_translated_lopo']:.2f} and {s5['llm']['mean_acc_translated_lopo']:.2f}; a classifier trained on the English originals reads the translations at {s5['google']['mean_acc_train_english_test_translated']:.2f}. Structure survives translation (paragraph count rho = 1.00, sentence length 0.89); vocabulary is rewritten (MATTR about 0.3).", S["cap"]),
        *section("9  Baseline: the models themselves cannot do this"),
        img("F10_rq6_judge", cw * 0.92),
        Paragraph(f"Each model was shown each essay and asked which of the five wrote it (five names in shuffled order, temperature 0, hidden reasoning off). GPT-5.5 {j6.loc['gpt','accuracy']:.1%}, Grok {j6.loc['grok','accuracy']:.1%}, Gemini {j6.loc['gemini','accuracy']:.1%}, DeepSeek {j6.loc['deepseek','accuracy']:.1%}: chance in all seven languages, each defaulting to one fixed answer. Claude, at {j6.loc['claude','accuracy']:.1%}, is the only judge above chance, and only just.", S["cap"]),
        Spacer(1, 8),
        Table([[[
            Paragraph("<b>Takeaways</b>", S["tldrh"]),
            Paragraph(f"Interpretable, cross-lingually defined features attribute LLM text in every language tested and beat every LLM judge by 35 to 50 points.", S["take"]),
            Paragraph("The fingerprint does not fade with resource level and survives translation, so provenance across a language boundary works from an English-trained classifier.", S["take"]),
            Paragraph("The five models write more alike in Hindi than in English: the register of low-resource languages is flattening.", S["take"]),
            Paragraph("Limits: one genre; length is part of the linear signal; ordinal resource rank; dated model snapshots.", S["take"]),
        ]]], colWidths=[cw], style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), TILE), ("BOX", (0, 0), (-1, -1), 0, TILE),
                                               ("LEFTPADDING", (0, 0), (-1, -1), 22), ("RIGHTPADDING", (0, 0), (-1, -1), 22),
                                               ("TOPPADDING", (0, 0), (-1, -1), 12), ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                                               ("LINEBEFORE", (0, 0), (0, -1), 8, ACCENT)])),
    ]
    for x, items, name in zip(cols, [col1, col2, col3], ["column 1", "column 2", "column 3"]):
        fill(c, x, bottom, cw, top - bottom, items, name)

    c.setFillColor(MUTE); c.setFont("Helvetica", 17)
    c.drawString(M, 0.42 * inch, "Analysis plan pre-specified 3 September 2026. All 840 responses, 1,440 translations, 4,195 judgments, feature tables and result files are in the repository. Contact: erlikhman.adrian@gmail.com")
    c.showPage(); c.save()
    if OVERFLOW:
        raise SystemExit("; ".join(OVERFLOW) + "; shrink text or figures")

    # ---- hard check: no dash or arrow glyphs in the text layer
    from pypdf import PdfReader
    text = "".join(p.extract_text() for p in PdfReader(str(OUT)).pages)
    bad = sorted({ch for ch in text if ch in FORBIDDEN})
    if bad:
        raise SystemExit(f"forbidden glyphs in poster text: {[hex(ord(b)) for b in bad]}")
    print("wrote", OUT, "(no dash or arrow glyphs in text layer)")


if __name__ == "__main__":
    build()
