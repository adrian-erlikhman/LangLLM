# LangLLM — pre-specified analysis plan

Written before data collection (2026-09-03). Anything not listed here is exploratory and
will be labelled as such.

## Design

- **Factors**: model (5) × language (7) × prompt (12) × generation (2) = 840 cells.
- **Unit of analysis**: one response. The two generations of one (model, language, prompt)
  are *not* independent; every classifier split and every clustered standard error groups
  by prompt.
- **Resource covariate**: ordinal rank 1–7 (en, es, zh, ru, ja, tr, hi), set in
  `config.yaml`. We use rank rather than a numeric share because published share estimates
  disagree by source; a sensitivity check with Common Crawl language shares is exploratory.
- **Exclusions**: responses that fail language ID (lingua, confidence < 0.6 or wrong
  language), fall outside 150–900 word-equivalents, or match a refusal pattern. Exclusion
  rates per model × language are reported. A cell with an empty model × language after
  exclusion does not stop the analysis; the language is dropped from RQ1/RQ2 and flagged.

## RQ1 — within-language attribution

- Classifier A: standardised features → multinomial logistic regression (C = 1). Primary.
- Classifier B: random forest (300 trees). Ceiling / robustness only.
- CV: leave-one-prompt-out (12 folds). Metric: accuracy and macro-F1; chance = 0.20.
- Uncertainty: 95% bootstrap CI over responses; exact binomial test vs 0.20.
- Interpretation: mean |standardised coefficient| per feature per language, and per-feature
  one-way ANOVA F by model within language.
- **Decision rule**: RQ1 is answered "yes" for a language if the logistic-regression CI
  excludes 0.20. Confusion matrices show *which* models blur.

## RQ2 — the gradient

- Spearman ρ between rank and per-language accuracy (n = 7). Low power by construction;
  reported for completeness.
- Primary: binomial GLM `correct ~ rank` on 840 cell-level outcomes, SEs clustered by
  prompt. **Decision rule**: negative rank coefficient with p < 0.05.
- Robustness: repeat with length-residualised features (each feature regressed on
  log tokens within language), to rule out "longer responses in English" as the driver.

## RQ3 — model style vs language style

- For each feature, OLS `z ~ model * language + prompt`, type-II ANOVA, partial η² for
  model, language and model × language.
- Summary: mean and median η² across the 21 features, per group (lexical, syntactic, …).
- Transfer test: features z-scored *within* language (removing the language main effect),
  logistic regression trained on language A, tested on language B. Diagonal = LOPO within
  A. **Decision rule**: style is called language-invariant to the extent off-diagonal
  accuracy exceeds 0.20; the ratio off-diagonal / diagonal is the invariance index.
- Interpretation guide: η²_model ≫ η²_interaction and transfer ≫ chance → invariant
  fingerprint; η²_interaction ≈ η²_model or transfer ≈ chance → per-language style.

## RQ4 — convergence

- Within each language, z-score features on the pooled language sample, then compute
  (a) mean pairwise Euclidean distance between the five model centroids,
  (b) silhouette of model labels, (c) between/within scatter trace ratio.
- 95% CI by stratified bootstrap within model (basic/reflected interval).
- Spearman ρ of each metric vs rank. **Decision rule**: convergence is claimed if all
  three metrics fall with rank *and* the lowest-resource CI lies below the English CI.
- Pairwise centroid distances identify which models converge on which.

## RQ5 (extension, added 2026-09-03 before any translated data existed) — translation

Suggested by Philo: does Google Translate, or translation in general, destroy the features?
- Sources: every kept English response (up to 120: 5 models × 12 prompts × 2).
- Translators: Google Translate (public endpoint) and a free non-subject, non-Gemini LLM
  (MiniMax M3, fallbacks Nemotron 3 Super, Llama 4 Maverick), into the six other languages.
- T1: LOPO attribution on translated texts per (translator, language) vs the English
  originals and vs native responses in that language. **Decision rule**: fingerprint
  "survives" a translator/language if the CI excludes 0.20; "destroyed" if it includes it.
- T2: classifier trained on native language-L responses applied to translated-into-L texts,
  and one trained on the English originals applied to translations (z-scored per domain).
- T3: per-feature Spearman ρ between original and translation across sources; mean model
  η² before vs after. Reports which feature groups carry through translation.

## RQ6 (extension, added 2026-09-03 before any judge data existed) — LLM-as-judge

Continuation of the CompLLM self-recognition protocol. Each subject model is shown each kept
original response (no metadata, no language label) and asked which of the five models wrote it,
answering with one candidate key; option order shuffled per text; temperature 0. Hidden reasoning is
*disabled* for every judge that allows it (instant-answer condition, matching an out-of-the-box
judge); Gemini 3.5 Flash cannot disable it and keeps low effort with the trace excluded — noted
as a deviation. A pilot with low-effort reasoning showed DeepSeek exhausting its budget without
answering and GPT-5.5 tripling the cost. Originals only (translations deferred for budget).
- Attribution: five-way accuracy per judge × language, exact binomial vs 0.20.
  **Decision rule**: a judge "can attribute" in a language if its CI excludes 0.20.
- Self-recognition: own-text recall vs the rate at which the judge names itself on others'
  text (false-self rate), one-sided Fisher exact per judge. **Decision rule**: self-recognition
  is claimed if own recall exceeds false-self rate with p < 0.05; "persists across languages"
  if the per-language own-recall CIs exclude 0.20 in the low-resource languages too.
- Comparison: judge accuracy vs the RQ1 feature classifier per language.
- Prediction registered from the CompLLM result: four judges at chance in every language;
  Claude above chance on its own text.

## Confounds we address

- Length → residualised robustness run.
- Reasoning traces → excluded at the API; responses with non-prose lines counted.
- Prompt wording → the same schema across languages, prompt as a blocking factor everywhere.
- Model aliasing at the provider → served model string logged per response.
- Tokeniser differences across scripts → all counts on Stanza UD tokens, rates per token.

## Reporting

`results/` holds one table per test, `results/figures/` F1–F7. The paper reports RQ1 and
RQ2 from logistic regression; the random forest appears once, as a ceiling.
