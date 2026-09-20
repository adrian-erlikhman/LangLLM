"""One-shot trim of main.tex to fit 5 pages. Each replacement must match exactly; the script aborts otherwise."""
from pathlib import Path
p = Path(__file__).with_name("main.tex")
s = p.read_text(encoding="utf-8")
R = [
# --- drop Fig 4 float, keep its content in text
(r"""\begin{figure}[t]
\centering
\includegraphics[width=\columnwidth]{fig4_survival.pdf}
\caption{Feature survival under translation. Structural and rhythmic features survive; vocabulary measures are rewritten. Question rate is omitted because the essays contain no questions.}
\label{fig:surv}
\end{figure}

""", ""),
(r"Fig.~\ref{fig:surv} shows why: paragraph count", r"Per-feature survival shows why: paragraph count"),
# --- Table I: drop Sep. column
(r"Judges: mean of the five LLM judges (best); Sep.: mean distance between model centroids ($z$-units). Chance accuracy is 0.20.}", r"Judges: mean of the five LLM judges (best). Chance accuracy is 0.20.}"),
(r"\begin{tabular}{l c l c l l c}", r"\begin{tabular}{l c l c l l}"),
(r"Language & Rank & LR [95\% CI] & F1 & $n$-gram [CI] & Judges & Sep. \\", r"Language & Rank & LR [95\% CI] & F1 & $n$-gram [CI] & Judges \\"),
(r"(\JudgeBesten{}) & \CentEn{} \\", r"(\JudgeBesten{}) \\"),
(r"(\JudgeBestes{}) & 3.11 \\", r"(\JudgeBestes{}) \\"),
(r"(\JudgeBestzh{}) & 3.01 \\", r"(\JudgeBestzh{}) \\"),
(r"(\JudgeBestru{}) & 2.97 \\", r"(\JudgeBestru{}) \\"),
(r"(\JudgeBestja{}) & 2.70 \\", r"(\JudgeBestja{}) \\"),
(r"(\JudgeBesttr{}) & 2.84 \\", r"(\JudgeBesttr{}) \\"),
(r"(\JudgeBesthi{}) & \CentHi{} \\", r"(\JudgeBesthi{}) \\"),
# --- references: drop three peripheral ones
(r"Zero-shot detectors~\cite{mitchell2023detectgpt,hans2024binoculars} and multilingual benchmarks~\cite{macko2023multitude,wang2024m4} separate human from machine text;", r"Zero-shot detectors~\cite{mitchell2023detectgpt} and multilingual benchmarks~\cite{macko2023multitude} separate human from machine text;"),
(r"Writing with LLMs reduces the diversity of human text~\cite{padmakumar2024diversity,sourati2026shrinking}, and a two-language benchmark compares model registers with human ones~\cite{milicka2025benchmark}; whether models converge on \emph{each other} where training data is thin has not been tested.", r"Writing with LLMs reduces the diversity of human text~\cite{padmakumar2024diversity,sourati2026shrinking}; whether models converge on \emph{each other} where training data is thin has not been tested."),
# --- intro trims
(r"Answering it lets an analyst link an influence campaign to a toolchain, check a vendor's claim about where its content came from, or apply platform rules that differ by provider. The attribution literature", r"Answering it lets an analyst link an influence campaign to a toolchain or apply platform rules that differ by provider. The attribution literature"),
(r" All decision rules were written down before data collection; deviations and additions are labelled.", r" Decision rules were fixed before data collection; additions are labelled."),
# --- related work trims
(r" These works ask human versus machine, not which machine, and the generator-identification subtask of SemEval-2024 Task 8 was English-only.", r" These works ask human versus machine, not which machine."),
(r"To our knowledge, no prior study attributes text to its source model with features that have the same definition in every language, holds content fixed across languages, tests attribution against a resource gradient, or measures what interpretability costs against an $n$-gram baseline; see~\cite{huang2024attribution} for a survey.", r"To our knowledge, no prior study attributes text to its source model with features that have the same definition in every language, holds content fixed across languages, or tests attribution against a resource gradient; see~\cite{huang2024attribution} for a survey."),
# --- method trims
(r"Twelve English prompts each fix a topic, a stance (six for, six against), three supporting claims, a prose-only instruction and a reading-level tier. For each language a model that is not a subject (Llama 4 Maverick) wrote a native version of each prompt from those elements rather than translating the English, so the wording is idiomatic while the content is fixed.", r"Twelve English prompts each fix a topic, a stance (six for, six against), three supporting claims, a prose-only instruction and a reading-level tier. For each language a non-subject model (Llama 4 Maverick) wrote a native version from those elements rather than translating the English."),
(r"For $n$-grams the fair counterpart fits the vocabulary on the union of $A$ and $B$ (no labels) and z-scores TF-IDF columns within each language, so both representations receive the same unlabelled adaptation to the target language.", r"For $n$-grams the fair counterpart fits the vocabulary on the union of $A$ and $B$ (no labels) and z-scores TF-IDF columns within each language, the same unlabelled adaptation."),
(r"We measure attribution on the translations alone, transfer from classifiers trained on the English originals or on native responses in the target language, and per-feature Spearman correlation between each original and its translation, for both representations.", r"We measure attribution on the translations alone, transfer from classifiers trained on the English originals or on native target-language responses, and per-feature Spearman correlation between original and translation."),
# --- results trims
(r" This is the expected result~\cite{sapkota2015ngrams}: $n$-grams see vocabulary, and the interpretable model does not. What the features give up within a language they recover across languages (Sec.~\ref{sec:rq3}) and under translation (Sec.~\ref{sec:rq5}).", r" This is expected~\cite{sapkota2015ngrams}: $n$-grams see vocabulary. What the features give up within a language they recover across languages (Sec.~\ref{sec:rq3}) and under translation (Sec.~\ref{sec:rq5})."),
(r" The features are not the only representation that transfers, but they transfer more, and they need no target-language text to do so. The transfer setting is transductive in one respect: the test language's own means and standard deviations (no labels) standardize its features, and all seven language versions share the same 12 prompts.", r" The features are not the only representation that transfers, but they transfer more and need no target-language text to do so. The setting is transductive in one respect: the test language's own means and SDs (no labels) standardize its features, and all languages share the same 12 prompts."),
(r" Grok's terse, lightly punctuated English register is the outlier that disappears; the other four were never far apart. Convergence and stable attribution are compatible: centroid distance averages over all \NFeatures{} features, most of which converge, while a classifier needs only the few that keep separating the models.", r" Grok's terse English register is the outlier that disappears; the other four were never far apart. Convergence and stable attribution are compatible: centroid distance averages over all \NFeatures{} features, most of which converge, while a classifier needs only the few that still separate the models."),
(r" This extends the English-to-Chinese translation result of~\cite{sun2025idiosyncrasies} to six languages, two translators and a representation whose surviving components can be named.", r" This extends the English-to-Chinese result of~\cite{sun2025idiosyncrasies} to six languages, two translators and a representation whose surviving components can be named."),
(r" Claude's best language is Hindi (\ClaudeHindiAcc{}), an exploratory observation across 35 judge--language cells.", ""),
# --- discussion / limitations / conclusion trims
(r"Three practical points follow. First, interpretable attribution does not require English: accuracy in Hindi and Turkish is within a few points of Spanish, and a classifier trained in one language transfers to the others. Second, the choice between an opaque and an interpretable representation is a choice about where the classifier will be used. Within one language, with training data in that language, character $n$-grams are the better tool by \GapNGmin{}--\GapNGmax{} points. Across a language or translation boundary, without retraining, they are not usable and the UD features are. Third, machine translation is not an effective way to hide which model wrote a text, because the features that carry the fingerprint are structural, and asking a model who wrote a text is not a substitute for measurement.", r"Three practical points follow. First, interpretable attribution does not require English, and a classifier trained in one language transfers to the others. Second, the choice between an opaque and an interpretable representation is a choice about where the classifier will be used: within one language, with training data in that language, character $n$-grams are better by \GapNGmin{}--\GapNGmax{} points; across a language or translation boundary, without retraining, only the UD features are usable. Third, machine translation does not hide which model wrote a text, because the fingerprint is structural, and asking a model who wrote a text is no substitute for measurement."),
(r"The convergence result bears on the homogenization literature~\cite{padmakumar2024diversity,sourati2026shrinking}: model-generated text in lower-resource languages is closer to a shared register than in English. As more of the text in these languages is machine-written, that register may become the default style that readers and future training sets encounter.", r"The convergence result bears on the homogenization literature~\cite{padmakumar2024diversity,sourati2026shrinking}: model-generated text in lower-resource languages is closer to a shared register than in English, and as more text in these languages is machine-written that register may become the default style readers and future training sets encounter."),
(r"(vi) Parser quality also falls with resource rank and is confounded with it. (vii) Results describe model versions served in September 2026. (viii) Judges were tested without extended reasoning.", r"(vi) Parser quality falls with resource rank and is confounded with it. (vii) Results describe model versions served in September 2026, and judges were tested without extended reasoning."),
(r" The models' styles converge where training data is thin, and the models themselves cannot read the fingerprint. Future work will test other genres, human-verified prompts, numeric resource covariates and reasoning-enabled judges.", r" The models' styles converge where training data is thin, and the models themselves cannot read the fingerprint. Future work: other genres, human-verified prompts, numeric resource covariates, reasoning-enabled judges."),
(r"""\section*{Data Availability}
Code, native prompts and their reviews, all \NResponses{} analyzed responses, \NTranslations{} translations, \NJudgments{} judge calls, features and every result table: \url{https://github.com/adrian-erlikhman/LangLLM}.""", r"""\noindent\textbf{Data availability.} Code, prompts and reviews, all \NResponses{} responses, \NTranslations{} translations, \NJudgments{} judge calls, features and result tables: \url{https://github.com/adrian-erlikhman/LangLLM}."""),
# --- figure sizes
(r"\includegraphics[width=0.96\textwidth]{fig2_transfer.pdf}", r"\includegraphics[width=0.9\textwidth]{fig2_transfer.pdf}"),
]
for a, b in R:
    assert a in s, "NOT FOUND: " + a[:80]
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8")
print("trim applied:", len(R), "edits")
