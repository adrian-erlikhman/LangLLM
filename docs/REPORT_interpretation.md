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
keep separating them. Finally, translation does **not** destroy the fingerprint: after Google
Translate or a free non-subject LLM renders the English responses into the six other languages,
five-way attribution still runs 0.57–0.70, and an English-trained classifier reads the
translations at 0.66, because the surviving signal is structural (paragraphing, sentence rhythm,
punctuation) rather than lexical. Asked directly which model wrote a text, four of the five
models are at chance in every language (GPT names itself 82% of the time regardless of
author; the others default to "Claude"); only Claude is above chance (25.4%, p < 0.001) with
a genuine, if small, self-recognition signal (own-text recall 17% vs 7% false claims) that is
strongest in Hindi, not weakest. Interpretable features beat every LLM judge by 35 to 50
points in every language.
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
**Interpretation.** Neither translator destroys the fingerprint. Attribution on translated
text alone runs 0.57–0.70 (mean 0.625 for Google Translate, 0.629 for the LLM translator)
against 0.717 on the English originals and a mean of 0.644 for *native* responses in the same
languages; every CI excludes chance and every binomial test has p < 0.001. Translating a text
costs about nine points of accuracy, roughly what moving from English to a native low-resource
language costs, and no more.

The English fingerprint travels intact. A classifier trained on the English originals and
applied to their translations scores 0.66 on average for both translators (0.77 for the LLM's
Hindi), essentially the English accuracy, so what a translator outputs is still recognisably
the source model's *English* style in another script. A classifier trained on the model's own
native-language responses does worse on the translations (0.52–0.53): translated GPT resembles
English GPT more than it resembles native Spanish GPT. This also answers the "which style does
the translated text carry" question: the translator preserves the source's structural habits
rather than re-styling the text into the model's native register for that language.

Feature survival explains why. Structural and rhythmic features come through almost unchanged
(Spearman ρ between original and translation, averaged over six languages): paragraph count
1.00, paragraph length 0.98, digit rate 0.94–0.97, sentence length 0.89, burstiness 0.87,
first-person rate 0.82–0.86, colon rate 0.75–0.84, sentence-length SD 0.83, dependency depth
0.77, subordination 0.72–0.74. Lexical features are rewritten by the target language: MATTR
0.29–0.34, function-word ratio 0.46, bigram entropy 0.48, connective rate 0.49. Sixteen of the
twenty measurable features keep ρ > 0.5 under both translators. The share of feature variance
explained by model falls from 0.40 in the English sources to 0.32 (Google) and 0.30 (LLM) after
translation, a reduction, not an erasure. Question rate is undefined because these essays
contain no questions.

Google Translate and the LLM translator behave almost identically. The one visible difference
is punctuation: the LLM normalises semicolons and colons more (ρ 0.68 vs 0.88, 0.75 vs 0.84),
consistent with an LLM lightly imposing its own conventions, yet its translations are, if
anything, marginally *more* attributable. A free non-subject LLM therefore does not overwrite
the source fingerprint with its own. For provenance work the practical reading is that
translation is not an effective laundering step against interpretable features, and that a
classifier trained in English can be applied across a translation boundary without retraining.
<!-- rq5 -->

<!-- rq6 -->
**Interpretation.** Asked directly, the models cannot do what the feature classifier does.
Four of the five judges sit at chance on every language: GPT-5.5 20.6%, Grok 21.9%, Gemini
21.2%, DeepSeek 20.3%, none significant, against 59–72% for the 21-feature classifier on the
same texts. Their answers are not guesses spread evenly but fixed defaults: GPT names *itself*
for 82% of all texts whether or not it wrote them (own-text recall 0.82, false-self rate 0.82,
so no discrimination at all), while Grok, Gemini and DeepSeek almost never name themselves and
call most texts "Claude" (Grok 681 of 839). Out of the box, attribution by an LLM is a prior
about who writes essays, not a reading of the text.

Claude Opus 4.7 is the exception, as in the CompLLM result, and the exception is small but
robust. Its overall accuracy is 25.4% (213/839, binomial p < 0.001), and it is the only judge
whose own-text recall (17.3%) exceeds the rate at which it names itself on others' text (6.6%;
one-sided Fisher p < 0.001). Its self-claims are also unusually precise: when Claude says
"Claude" it is right 40% of the time against a 20% base rate, and when it says "Gemini" it is
right 81% of the time; it simply under-calls both, defaulting to "GPT" for 614 of 839 texts.
Its above-chance accuracy therefore comes from cautious discrimination rather than from
self-recognition alone (accuracy on others' text 0.27, on its own 0.17).

The self-recognition signal does not fade with resource level; if anything it is strongest
where the resource hypothesis predicted it should vanish. Own-text recall versus false-self
rate is significant in English (25% vs 3%, p = 0.002), Japanese (38% vs 16%, p = 0.02) and
Hindi (42% vs 13%, p = 0.003), where Claude's overall accuracy also peaks at 36.1% (p < 0.001).
In Spanish and Russian Claude never names itself at all (0 of 24 own texts), so the signal is
absent there rather than reversed. The correlation of own-recall with rank is positive and
non-significant (ρ = 0.45, p = 0.31): there is no gradient, and the low-resource end is where
Claude is most willing to claim its own writing.

Two caveats. First, the effect is modest in absolute terms; a 25% judge is far from a usable
attributor, and the paper's practical claim should be that interpretable features beat every
LLM judge by 35–50 points in every language, not that Claude can identify itself reliably.
Second, the judge condition disabled hidden reasoning for the four models that allow it, so
this is the instant-answer setting; Gemini kept low-effort reasoning because it cannot be
disabled, and still sat at chance, which argues against reasoning being what the others were
missing.
<!-- rq6 -->

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
* **Judge condition.** RQ6 disables hidden reasoning for the four judges that allow it
  (instant-answer condition); Gemini keeps low-effort reasoning. A reasoning-on condition was
  piloted and abandoned for cost; it may raise judge accuracy and should be tested before
  claiming that LLM judges *cannot* attribute.
* **Snapshot.** Model strings are dated snapshots served through OpenRouter in September 2026;
  fingerprints will drift with model updates.
<!-- limitations -->
