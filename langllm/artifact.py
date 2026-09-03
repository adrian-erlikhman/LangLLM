"""Build docs/report.html — a self-contained page (figures embedded) from results/ + the
interpretation file. Same content as REPORT.md, designed for reading.

    python -m langllm.artifact
"""
from __future__ import annotations
import base64
import html
import json
import pandas as pd
from .config import load_config, RESULTS_DIR, FIG_DIR, ROOT, resource_rank

DOCS = ROOT / "docs"
LANG_NAME = {"en": "English", "es": "Spanish", "zh": "Chinese", "ru": "Russian", "ja": "Japanese", "tr": "Turkish", "hi": "Hindi"}
MODEL_NAME = {"gpt": "GPT-5.5", "gemini": "Gemini 3.5 Flash", "claude": "Claude Opus 4.7", "grok": "Grok 4.3", "deepseek": "DeepSeek V4 Pro"}


def _csv(n):
    p = RESULTS_DIR / n
    return pd.read_csv(p) if p.exists() else None


def _json(n):
    p = RESULTS_DIR / n
    return json.load(open(p)) if p.exists() else None


def fig(name: str, caption: str) -> str:
    p = FIG_DIR / f"{name}.png"
    if not p.exists():
        return ""
    b = base64.b64encode(p.read_bytes()).decode()
    return f'<figure><img src="data:image/png;base64,{b}" alt="{html.escape(caption)}"><figcaption>{caption}</figcaption></figure>'


def table(df: pd.DataFrame, fmt: str = "{:.3f}", caption: str = "") -> str:
    d = df.copy()
    for c in d.columns:
        if d[c].dtype.kind == "f":
            d[c] = d[c].map(lambda v: "" if pd.isna(v) else fmt.format(v))
    head = "".join(f"<th>{html.escape(str(c))}</th>" for c in d.columns)
    body = "".join("<tr>" + "".join(f"<td>{html.escape(str(v))}</td>" for v in r) + "</tr>" for r in d.itertuples(index=False))
    cap = f"<caption>{caption}</caption>" if caption else ""
    return f'<div class="tw"><table>{cap}<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def md_inline(s: str) -> str:
    """Tiny markdown: **bold**, *em*, `code`, paragraphs, bullet lists. Enough for the interpretation file."""
    import re
    out, buf, in_list = [], [], False

    def flush():
        nonlocal buf
        if buf:
            out.append("<p>" + " ".join(buf) + "</p>")
            buf = []
    for line in s.splitlines():
        t = html.escape(line.rstrip())
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"(?<!\*)\*(?!\*)(.+?)\*", r"<em>\1</em>", t)
        t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
        if t.startswith("* "):
            flush()
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append(f"<li>{t[2:]}</li>")
        elif not t.strip():
            flush()
            if in_list:
                out.append("</ul>"); in_list = False
        else:
            if in_list and t.startswith("  "):
                out[-1] = out[-1][:-5] + " " + t.strip() + "</li>"
            else:
                if in_list:
                    out.append("</ul>"); in_list = False
                buf.append(t.strip())
    flush()
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def build() -> str:
    cfg = load_config()
    rank = resource_rank(cfg)
    langs = sorted(cfg["languages"], key=rank.get)
    interp = (DOCS / "REPORT_interpretation.md").read_text(encoding="utf-8")
    sec = {}
    for tag in ("summary", "rq1", "rq2", "rq3", "rq4", "rq5", "limitations"):
        m = interp.split(f"<!-- {tag} -->")
        sec[tag] = md_inline(m[1].strip()) if len(m) > 1 else ""

    acc = _csv("rq1_accuracy.csv"); g = _json("rq2_gradient.json"); eta = _csv("rq3_anova_eta2.csv")
    ts = _json("rq3_transfer_summary.json") or {}; s4 = _json("rq4_summary.json") or {}; s5 = _json("rq5_summary.json") or {}
    v = _csv("validation_summary.csv")
    lr = acc[acc.classifier == "logreg"].set_index("lang") if acc is not None else None

    # ---- headline tiles
    tiles = []
    if lr is not None:
        tiles.append(("RQ1", f"{lr['accuracy'].min():.0%}–{lr['accuracy'].max():.0%}", "five-way attribution accuracy, every language (chance 20%)"))
    if g:
        tiles.append(("RQ2", f"β = {g['glm_cell_level']['coef_rank_logodds']:+.3f}", f"log-odds per resource rank, p = {g['glm_cell_level']['p']:.2f} · no gradient"))
    if eta is not None:
        mean = eta[eta.feature == "MEAN"].iloc[0]
        tiles.append(("RQ3", f"{mean.eta2_lang:.2f} vs {mean.eta2_model:.2f}", f"mean η² language vs model · transfer {ts.get('mean_offdiag_accuracy', 0):.0%} cross-lingual"))
    if s4:
        tiles.append(("RQ4", f"ρ = {s4['centroid_dist']['spearman_rho_vs_rank']:.2f}", "model separation vs rank · models converge in low-resource languages"))
    if s5:
        k = list(s5)[0]
        tiles.append(("RQ5", f"{s5[k]['mean_acc_translated_lopo']:.0%} · {s5[list(s5)[-1]]['mean_acc_translated_lopo']:.0%}" if len(s5) > 1 else f"{s5[k]['mean_acc_translated_lopo']:.0%}",
                      "attribution after Google / LLM translation (from " + f"{s5[k]['acc_english_originals']:.0%} in English)"))
    tiles_html = "".join(f'<div class="tile"><span class="eyebrow">{a}</span><span class="num">{b}</span><span class="cap">{c}</span></div>' for a, b, c in tiles)

    parts = []
    parts.append(f"""
<header>
  <p class="eyebrow">LangLLM · September 2026</p>
  <h1>Do LLM fingerprints survive outside English?</h1>
  <p class="lede">Interpretable stylometric attribution of five frontier models across a seven-language resource gradient, with a translation extension.</p>
  <div class="tiles">{tiles_html}</div>
</header>
<section id="summary"><h2>Summary</h2>{sec['summary']}</section>
""")

    # ---- design
    model_rows = "".join(f"<tr><td>{MODEL_NAME[k]}</td><td><code>{v}</code></td></tr>" for k, v in cfg["models"].items())
    lang_rows = "".join(f"<tr><td>{rank[l]}</td><td>{LANG_NAME[l]}</td><td><code>{cfg['languages'][l]['stanza']}</code></td><td>{cfg['languages'][l]['length_hint']}</td></tr>" for l in langs)
    parts.append(f"""
<section id="method"><h2>1 · Design and method</h2>
<div class="two">
<div class="tw"><table><caption>Subject models (served through OpenRouter; the served model string is logged per response)</caption><thead><tr><th>Model</th><th>String</th></tr></thead><tbody>{model_rows}</tbody></table></div>
<div class="tw"><table><caption>Languages in resource order · Stanza package · native length target</caption><thead><tr><th>Rank</th><th>Language</th><th>UD</th><th>Length</th></tr></thead><tbody>{lang_rows}</tbody></table></div>
</div>
<p><strong>Cells.</strong> 5 models × 12 prompts × 7 languages × 2 generations = 840 responses. Single user turn, no system prompt, temperature {cfg['generation']['temperature']}, seeds fixed per generation index, reasoning at low effort with the trace excluded (Gemini 3.5 Flash cannot disable reasoning, so this is the one setting all five accept), {cfg['generation']['max_tokens']:,}-token budget.</p>
<p><strong>Prompts.</strong> Twelve English schemas each fix a topic, a stance (6 for / 6 against), three sub-claims and a reading-level tier (a prompt control only, since Flesch–Kincaid is English-specific). For every language a non-subject model (<code>{cfg['prompt_writer']}</code>) composes a native prompt from the schema, never by translation, so all seven versions share topic, stance and sub-claims and only style is free. A third-family reviewer (<code>{cfg['prompt_reviewer']}</code>) extracted topic, stance and points from each native prompt blind and matched them to the schema; failing prompts were regenerated with the reviewer's note as feedback until all 84 passed. Earlier wordings are retained in each prompt record.</p>
<p><strong>Validation.</strong> Language identification (lingua, seven-language closed set, confidence ≥ 0.6), a 150–900 word-equivalent window (Chinese and Japanese converted from characters), a per-language refusal pattern, truncation, and a count of heading or bullet lines.</p>
<p><strong>Features.</strong> Every text is parsed with Stanza on Universal Dependencies, so each of the 21 features has one definition in all seven languages.</p>
<div class="tw"><table><caption>The 21 features</caption><thead><tr><th>Group</th><th>Features</th></tr></thead><tbody>
<tr><td>Lexical</td><td>MATTR (window 50) · hapax rate · mean token length · Zipf slope</td></tr>
<tr><td>Syntactic</td><td>sentence length mean and SD · burstiness · dependency depth · subordinate-clause rate (<code>acl advcl ccomp xcomp csubj</code>) · function-word ratio · first-person rate</td></tr>
<tr><td>Structure</td><td>paragraph count · paragraph length · question rate · connective rate (<code>cc</code>, <code>mark</code>, sentence-initial ADV/CCONJ/SCONJ)</td></tr>
<tr><td>Punctuation</td><td>comma · colon · dash · semicolon per 1 000 tokens, script equivalents mapped (<code>，、</code> <code>：</code> <code>— – ―</code> <code>；</code>)</td></tr>
<tr><td>Character</td><td>character-bigram entropy · digit rate</td></tr>
</tbody></table></div>
<p><strong>Analysis.</strong> RQ1: per-language five-way attribution, leave-one-prompt-out (both generations of a prompt stay on one side), logistic regression on standardised features as the interpretable primary and a random forest as ceiling; bootstrap CIs and exact binomial tests against 0.20. RQ2: Spearman ρ over the seven languages and a cell-level binomial GLM <code>correct ~ rank</code> with prompt-clustered errors; robustness with length-residualised features. RQ3: per-feature two-way ANOVA (model × language, prompt blocked) with partial η², plus a cross-lingual transfer matrix of within-language z-scored classifiers. RQ4: within-language model separation (centroid distance, silhouette, between/within scatter) with stratified bootstrap CIs. RQ5: every kept English response translated into the six other languages by Google Translate and by a free non-subject, non-Gemini LLM (<code>{cfg['translators']['llm']}</code>); attribution on translated text, transfer from native classifiers, and per-feature survival. The pre-specified decision rules are in <code>docs/analysis_plan.md</code>.</p>
</section>""")

    # ---- data quality
    if v is not None:
        keep = v.pivot(index="model_key", columns="lang", values="keep_rate")[langs]
        keep.index = [MODEL_NAME[m] for m in keep.index]
        med = v.pivot(index="model_key", columns="lang", values="median_words")[langs]
        med.index = [MODEL_NAME[m] for m in med.index]
        parts.append(f"""<section id="data"><h2>2 · Data quality</h2>
<p>839 of 840 responses are used. Ten DeepSeek cells spent an entire 4 000-token budget on hidden reasoning and returned nothing; they were re-collected at 16 000 tokens (override recorded per response). One Grok response to a Hindi prompt came back in English and is excluded. Reasoning tokens per response (median): Claude 0, GPT 23, Grok 489, DeepSeek 552, Gemini 1 122.</p>
<div class="two">{table(keep.reset_index().rename(columns={'index': 'model'}), '{:.2f}', 'Keep rate per model × language')}{table(med.reset_index().rename(columns={'index': 'model'}), '{:.0f}', 'Median length, word-equivalents')}</div>
</section>""")

    # ---- RQ1
    if lr is not None:
        t = lr.loc[langs].reset_index()[["lang", "rank", "n", "accuracy", "acc_ci_lo", "acc_ci_hi", "macro_f1"]]
        t["rf"] = acc[acc.classifier == "rf"].set_index("lang").loc[langs]["accuracy"].to_numpy()
        t["lang"] = t["lang"].map(LANG_NAME)
        t.columns = ["language", "rank", "n", "accuracy (logreg)", "CI lo", "CI hi", "macro-F1", "random forest"]
        parts.append(f"""<section id="rq1"><h2>3 · RQ1 — attribution within each language</h2>
{fig('F1_rq1_accuracy', 'Five-way attribution accuracy per language, leave-one-prompt-out, with 95% bootstrap CIs. Dashed line: chance.')}
{table(t, '{:.3f}')}
{fig('F2_rq1_confusion', 'Row-normalised confusion matrices (logistic regression).')}
{sec['rq1']}</section>""")

    # ---- RQ2
    if g:
        gl = _json("rq2_gradient_lenctl.json") or {}
        rows = pd.DataFrame([
            {"test": "Spearman ρ, accuracy vs rank (logreg, n = 7)", "estimate": f"{g['logreg']['spearman_rho']:.2f}", "p": f"{g['logreg']['spearman_p']:.3f}"},
            {"test": "Spearman ρ (random forest)", "estimate": f"{g['rf']['spearman_rho']:.2f}", "p": f"{g['rf']['spearman_p']:.3f}"},
            {"test": "OLS slope, accuracy per rank step", "estimate": f"{g['logreg']['ols_slope_per_rank']:+.3f}", "p": f"{g['logreg']['ols_p']:.3f}"},
            {"test": f"Cell-level GLM β(rank), log-odds, n = {g['glm_cell_level']['n_cells']}, prompt-clustered SE", "estimate": f"{g['glm_cell_level']['coef_rank_logodds']:+.3f} (SE {g['glm_cell_level']['se']:.3f})", "p": f"{g['glm_cell_level']['p']:.3f}"},
        ] + ([{"test": "GLM β(rank), length-residualised features", "estimate": f"{gl['glm_cell_level']['coef_rank_logodds']:+.3f}", "p": f"{gl['glm_cell_level']['p']:.3f}"}] if gl else []))
        lc = _csv("rq1_accuracy_lenctl.csv")
        lc_html = ""
        if lc is not None:
            p2 = lc.pivot(index="lang", columns="classifier", values="accuracy").loc[langs].reset_index()
            p2["lang"] = p2["lang"].map(LANG_NAME); p2.columns = ["language", "logreg (length-residualised)", "random forest (length-residualised)"]
            lc_html = table(p2, "{:.3f}", "Robustness: attribution with each feature residualised on log length within language")
        parts.append(f"""<section id="rq2"><h2>4 · RQ2 — the resource gradient</h2>
{fig('F3_rq2_gradient', 'Attribution accuracy against resource rank.')}
{table(rows, caption='Gradient tests')}
{lc_html}
{sec['rq2']}</section>""")

    # ---- RQ3
    if eta is not None:
        e = eta[eta.feature != "MEAN"][["feature", "eta2_model", "eta2_lang", "eta2_interaction", "eta2_prompt"]].sort_values("eta2_model", ascending=False)
        M = _csv("rq3_transfer_matrix.csv")
        mh = ""
        if M is not None:
            M = M.rename(columns={M.columns[0]: "train ⧵ test"})
            mh = table(M, "{:.2f}", f"Cross-lingual transfer, within-language z-scored (diagonal = LOPO-CV). Mean off-diagonal {ts.get('mean_offdiag_accuracy', 0):.3f}, diagonal {ts.get('mean_diag_accuracy', 0):.3f}; {ts.get('n_offdiag_above_chance')}/{ts.get('n_offdiag')} off-diagonal cells above chance.")
        parts.append(f"""<section id="rq3"><h2>5 · RQ3 — model style vs language style</h2>
{fig('F4_rq3_eta2', 'Partial η² per feature for model, language and their interaction (prompt as blocking factor).')}
{table(e, '{:.3f}', 'Partial η² per feature, sorted by model effect')}
{fig('F5_rq3_transfer', 'Cross-lingual transfer matrix.')}
{mh}
{sec['rq3']}</section>""")

    # ---- RQ4
    sep = _csv("rq4_separation.csv")
    if sep is not None:
        t = sep.sort_values("rank")[["lang", "rank", "centroid_dist", "centroid_dist_ci_lo", "centroid_dist_ci_hi", "silhouette", "between_within_ratio"]].copy()
        t["lang"] = t["lang"].map(LANG_NAME); t.columns = ["language", "rank", "centroid distance", "CI lo", "CI hi", "silhouette", "between / within"]
        srows = pd.DataFrame([{"metric": k.replace("_", " "), "Spearman ρ vs rank": f"{x['spearman_rho_vs_rank']:.2f}", "p": f"{x['p']:.3f}", "English": f"{x['english']:.3f}", "Hindi": f"{x['lowest_resource']:.3f}"} for k, x in s4.items()])
        pw = _csv("rq4_pairwise.csv"); ph = ""
        if pw is not None:
            pw["pair"] = pw["model_a"].map(MODEL_NAME) + " – " + pw["model_b"].map(MODEL_NAME)
            pp = pw.pivot(index="pair", columns="lang", values="centroid_dist")[langs].reset_index()
            ph = table(pp, "{:.2f}", "Pairwise centroid distance between models, within-language z-scored units")
        parts.append(f"""<section id="rq4"><h2>6 · RQ4 — convergence in low-resource languages</h2>
{fig('F6_rq4_separation', 'Three separation metrics against resource rank, with reflected bootstrap CIs.')}
{table(t, '{:.3f}')}
{table(srows, caption='Trend tests')}
{ph}
{fig('F7_pca_by_language', 'Within-language PCA of the 21 features; crosses are model centroids.')}
{sec['rq4']}</section>""")

    # ---- RQ5
    t1 = _csv("rq5_translation_accuracy.csv")
    if t1 is not None:
        t = t1.sort_values(["translator", "rank"])[["translator", "lang", "n", "acc_translated_lopo", "ci_lo", "ci_hi", "acc_native_same_lang", "acc_train_native_test_translated", "acc_train_english_test_translated"]].copy()
        t["lang"] = t["lang"].map(LANG_NAME)
        t.columns = ["translator", "language", "n", "translated, LOPO", "CI lo", "CI hi", "native same language", "train native → test translated", "train English → test translated"]
        srows = pd.DataFrame([{"translator": k, **{kk.replace("_", " "): (f"{vv:.3f}" if isinstance(vv, float) else vv) for kk, vv in x.items()}} for k, x in s5.items()])
        t3 = _csv("rq5_feature_survival.csv"); fh = ""
        if t3 is not None:
            fs = t3.groupby(["translator", "feature"])["spearman_rho"].mean().unstack(0).reset_index().sort_values(t3["translator"].unique()[0], ascending=False)
            fh = table(fs, "{:.2f}", "Mean Spearman ρ between original and translation per feature, averaged over the six target languages")
        parts.append(f"""<section id="rq5"><h2>7 · RQ5 — does translation destroy the fingerprint?</h2>
{fig('F8_rq5_translation', 'Attribution on translated text versus native responses and the English originals.')}
{table(t, '{:.3f}')}
{table(srows, caption='Per-translator summary')}
{fig('F9_rq5_feature_survival', 'Which features survive translation: Spearman ρ between each original and its translation.')}
{fh}
{sec['rq5']}</section>""")

    parts.append(f"""<section id="limits"><h2>8 · Limitations</h2>{sec['limitations']}</section>
<section id="repro"><h2>9 · Reproduction</h2>
<p>Code, prompts, every raw response, translation, feature table and result file are in <a href="https://github.com/adrian-erlikhman/LangLLM">github.com/adrian-erlikhman/LangLLM</a>. The pipeline is seven commands, each resumable:</p>
<pre>python -m langllm.prompts &amp;&amp; python -m langllm.review &amp;&amp; python -m langllm.refine
python -m langllm.collect &amp;&amp; python -m langllm.validate &amp;&amp; python -m langllm.features
python -m langllm.analysis &amp;&amp; python -m langllm.figures
python -m langllm.translate &amp;&amp; python -m langllm.features --translated
python -m langllm.analysis_translation &amp;&amp; python -m langllm.figures --rq5</pre>
</section>
<footer><p>LangLLM · Adrian Erlikhman · analysis plan pre-specified 3 September 2026 · report generated from <code>results/</code></p></footer>""")

    body = "\n".join(parts)
    page = CSS_HEAD + body
    (DOCS / "report.html").write_text(page, encoding="utf-8")
    print("wrote", DOCS / "report.html", f"{len(page)/1e6:.1f} MB")
    return page


CSS_HEAD = """<title>LangLLM Fingerprints</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Public+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{
  --bg:#F6F5F1; --bg2:#EDECE6; --ink:#1E2430; --ink2:#4A5160; --mute:#7A8090; --rule:#D9D8D1;
  --model:#3F66A8; --lang:#C8783F; --inter:#4E8F5E; --accent:#3F66A8; --accent-ink:#2C4B82; --tile:#FFFFFF;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --bg:#14171D; --bg2:#1C2028; --ink:#E8E9EC; --ink2:#BFC3CC; --mute:#8A909C; --rule:#2C313B;
  --model:#7FA3E0; --lang:#E0A070; --inter:#7DBE8C; --accent:#7FA3E0; --accent-ink:#A9C3EE; --tile:#1C2028; }}
:root[data-theme="dark"]{
  --bg:#14171D; --bg2:#1C2028; --ink:#E8E9EC; --ink2:#BFC3CC; --mute:#8A909C; --rule:#2C313B;
  --model:#7FA3E0; --lang:#E0A070; --inter:#7DBE8C; --accent:#7FA3E0; --accent-ink:#A9C3EE; --tile:#1C2028; }
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Public Sans",system-ui,-apple-system,"Segoe UI",sans-serif;font-size:16px;line-height:1.55}
header,section,footer{max-width:1080px;margin:0 auto;padding:0 28px}
header{padding-top:56px;padding-bottom:8px}
h1{font-family:"Fraunces","Iowan Old Style",Georgia,serif;font-weight:600;font-size:clamp(34px,5vw,54px);line-height:1.05;letter-spacing:-0.01em;margin:8px 0 14px;max-width:18ch;text-wrap:balance}
h2{font-family:"Fraunces",Georgia,serif;font-weight:500;font-size:28px;line-height:1.15;margin:0 0 18px;text-wrap:balance;padding-top:44px;border-top:1px solid var(--rule)}
section{padding-bottom:12px}
.eyebrow{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}
.lede{font-size:19px;color:var(--ink2);max-width:62ch;margin:0 0 30px}
p{max-width:72ch}
section > p, section > ul{max-width:72ch}
strong{font-weight:600}
code{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:.88em;background:var(--bg2);padding:1px 5px;border-radius:3px}
pre{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:13px;background:var(--bg2);padding:16px 18px;border-radius:4px;overflow-x:auto;line-height:1.5}
a{color:var(--accent-ink)}
ul{padding-left:20px}
li{margin:6px 0;max-width:72ch}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;margin:0 0 20px}
.tile{background:var(--tile);border:1px solid var(--rule);border-top:3px solid var(--accent);padding:14px 16px 12px;display:flex;flex-direction:column;gap:6px;min-height:118px}
.tile .num{font-family:"Fraunces",Georgia,serif;font-size:28px;font-weight:600;line-height:1.05;font-variant-numeric:tabular-nums;color:var(--ink)}
.tile .cap{font-size:12.5px;color:var(--ink2);line-height:1.35}
figure{margin:22px 0}
figure img{width:100%;height:auto;display:block;border:1px solid var(--rule);background:#fff}
figcaption{font-size:13px;color:var(--mute);margin-top:8px;max-width:80ch}
.tw{overflow-x:auto;margin:18px 0}
table{border-collapse:collapse;font-size:13.5px;min-width:100%;font-variant-numeric:tabular-nums}
caption{text-align:left;font-size:13px;color:var(--mute);padding:0 0 8px;caption-side:top}
th{text-align:left;font-weight:600;color:var(--ink2);border-bottom:1.5px solid var(--ink2);padding:6px 10px;white-space:nowrap;font-size:12.5px}
td{padding:5px 10px;border-bottom:1px solid var(--rule);white-space:nowrap}
tbody tr:hover td{background:var(--bg2)}
.two{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:20px;align-items:start}
footer{padding:40px 28px 60px;color:var(--mute);font-size:13px;border-top:1px solid var(--rule);margin-top:40px}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
@media (prefers-reduced-motion: reduce){*{animation:none!important;transition:none!important}}
@media (max-width:640px){header,section{padding:0 18px} header{padding-top:36px} h2{font-size:24px}}
</style>
"""


if __name__ == "__main__":
    build()
