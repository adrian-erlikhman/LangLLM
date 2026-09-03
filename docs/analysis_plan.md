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

## Confounds we address

- Length → residualised robustness run.
- Reasoning traces → excluded at the API; responses with non-prose lines counted.
- Prompt wording → the same schema across languages, prompt as a blocking factor everywhere.
- Model aliasing at the provider → served model string logged per response.
- Tokeniser differences across scripts → all counts on Stanza UD tokens, rates per token.

## Reporting

`results/` holds one table per test, `results/figures/` F1–F7. The paper reports RQ1 and
RQ2 from logistic regression; the random forest appears once, as a ceiling.
