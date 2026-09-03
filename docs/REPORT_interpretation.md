<!-- summary -->
**Summary.** Five frontier models can be told apart from 21 interpretable, language-comparable
features in every one of seven languages, at 59–72% five-way accuracy against 20% chance
(logistic regression, leave-one-prompt-out; every 95% CI excludes chance). Contrary to the
hypothesis, attribution accuracy does **not** fall along the resource gradient: Japanese is as
identifiable as English, Hindi and Turkish sit within a few points of Spanish, and the cell-level
gradient coefficient is small and non-significant. Language explains far more feature variance
than model does (mean partial η² 0.54 vs 0.15), yet the model fingerprint is substantially
language-invariant: a classifier trained on one language and tested on another, after removing
each language's mean, is above chance in all 42 language pairs (mean 0.49). Models **do**
converge stylistically as resources fall: the multivariate separation between model centroids
shrinks monotonically from English to Hindi (Spearman ρ = −0.96, p < 0.001), driven mostly by
Grok, the outlier in English, drifting toward the pack. The apparent paradox, convergence
without loss of attribution, resolves as follows: models converge in the bulk of features while
a few high-signal features (paragraph count, comma and colon rates, lexical-diversity slope)
keep separating them. The translation extension (RQ5) is reported in §7.
<!-- summary -->

<!-- rq1 -->
**Interpretation.** Attribution works in every language. GPT-5.5 and Grok 4.3 are the most
identifiable (typically 75–90% recall); Claude Opus 4.7 and Gemini 3.5 Flash follow; DeepSeek
V4 Pro is the blur, at 25–58% recall, most often mistaken for Claude in English and for GPT or
Gemini in Hindi. The feature-importance tables show the fingerprint is carried by *structure and
punctuation* more than syntax: paragraph count and length, comma and colon density, and the
lexical-diversity measures (hapax rate, Zipf slope, bigram entropy) dominate in almost every
language, whereas dependency depth, subordination and question rate contribute little. Length
is part of the signal: GPT-5.5 writes the longest responses and Grok the shortest in all seven
languages (§2), and the length-residualised robustness run (§4) shows the *linear* fingerprint
loses 10–20 points without it, while the random forest does not, so the residual, non-length
fingerprint is real but non-linear.
<!-- rq1 -->

<!-- rq2 -->
**Interpretation.** The pre-registered decision rule (negative rank coefficient, p < 0.05) is
**not met**. The point estimate is negative but tiny: about −0.04 log-odds per rank step,
which is under one percentage point of accuracy per step, with p ≈ 0.36 (p ≈ 0.16 after length
control). The ordering is also not monotone: Japanese (rank 5) matches English, Hindi (rank 7)
beats Turkish (rank 6) and Spanish (rank 2). With interpretable features, the fingerprint does
not fade with training-data share; whatever these models do differently, they do it in Hindi
too. The one qualification is that our rank is ordinal and approximate; a numeric share
covariate might sharpen the picture, but the range of accuracies (0.59–0.72) leaves little
gradient to find.
<!-- rq2 -->

<!-- rq3 -->
**Interpretation.** Language dominates every feature that touches morphology or the lexicon:
mean token length, function-word ratio, MATTR, hapax rate and Zipf slope have language η² above
0.85, as expected when comparing Chinese characters, Turkish agglutination and Hindi
postpositions. Model effects are largest on the same lexical-diversity measures (hapax rate
0.38, Zipf slope 0.37), on comma density (0.32), bigram entropy (0.31) and paragraph count
(0.29), and smallest on subordination, question rate and dependency depth (≤ 0.03), so the
models differ in *how varied their vocabulary is and how they punctuate and paragraph*, not in
clause architecture. The interaction term is on average as large as the model term (0.13 vs
0.15), meaning each model adapts its style per language, but the transfer matrix shows the
invariant part is the larger share: after within-language standardisation, a classifier trained
on any language reaches 0.38–0.59 on any other (mean 0.49 against a within-language mean of
0.65; all 42 off-diagonal cells above chance). Roughly three quarters of within-language
performance transfers. The fingerprint is therefore mostly language-invariant with a
per-language accent.
<!-- rq3 -->

<!-- rq4 -->
**Interpretation.** All three separation metrics fall with rank, and all three Spearman
correlations are at or near −1 (centroid distance ρ = −0.96, p < 0.001; silhouette ρ = −0.93,
p = 0.003; between/within ratio ρ = −1.00). The between/within ratio more than halves from
English (0.41) to Hindi (0.18); the silhouette is small everywhere and negative in Hindi, so no
model forms a tight cluster in the low-resource languages. The pairwise table locates the
convergence: the two largest English distances, GPT–Grok (5.7) and DeepSeek–Grok (4.9),
collapse to 2.7 and 2.0 in Hindi, and Claude–Grok goes from 5.4 to 3.5. Grok's terse, sparsely
punctuated English register is the outlier that disappears; the other four models were never
far apart and stay that way. Convergence and sustained attribution accuracy are compatible
because the classifier needs only a handful of features to separate five classes, while the
centroid distance averages over all 21, most of which have converged. The practical reading for
register: in low-resource languages the five models write more alike than they do in English,
but not yet identically.
<!-- rq4 -->

<!-- rq5 -->
RQ5_PLACEHOLDER
<!-- rq5 -->

<!-- limitations -->
* **One prompt family.** Twelve persuasive-essay schemas with a fixed three-point structure.
  The paragraph-count and connective features that carry much of the fingerprint are partly a
  property of how each model handles that instruction; other genres may fingerprint differently.
* **Length is entangled with style.** Models differ systematically in length and the linear
  classifier uses it. The length-residualised run keeps attribution well above chance
  (non-linearly), but a deployment classifier should treat length as a feature to justify, not
  a given.
* **Resource rank is ordinal.** The gradient test has seven points; the cell-level GLM adds
  power but inherits the same coarse covariate.
* **Reasoning budgets.** Ten DeepSeek cells overflowed a 4 000-token budget with hidden
  reasoning and were re-collected at 16 000; the override is recorded per response. One Grok
  response to a Hindi prompt came back in English and was excluded. 839 of 840 cells are used.
* **Two generations per cell.** Within-cell variance is estimated from n = 2; the leave-one-prompt-
  out design prevents leakage but confidence intervals are correspondingly wide (±7–9 points).
* **Automated prompt review.** Prompt fidelity was checked by a model, not a person, in all seven
  languages. The review and every regenerated wording are versioned for audit.
* **Snapshot.** Model strings are dated snapshots served through OpenRouter in September 2026;
  fingerprints will drift with model updates.
<!-- limitations -->
