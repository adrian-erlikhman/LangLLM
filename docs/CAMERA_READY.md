# Camera-ready: response to reviews (IEEE BigData 2026 HSS, SP19343)

Paper: *Interpretable Multilingual Attribution of Frontier LLMs* (accepted 9 Oct 2026; Best Paper Finalist).
Source: `paper/main.tex` (+ `numbers.tex`, `references.bib`, `figures/fig2_transfer.pdf`, `figures/fig3_features.pdf`).
Build: `paper/build.sh`. Still 5 pages, US Letter, all fonts embedded.

Base text is the version submitted on 20–21 Sept (Michael's Overleaf project, `paper.tex`). Every number still comes
from `numbers.tex`; the macros of the submitted version are unchanged and new ones were appended.

## New analyses (`python -m langllm.camera_ready`, outputs `results/cr_*`)

| Part | What | Files |
|---|---|---|
| C1 | Nested LOPO choice of C ∈ {0.01, 0.1, 1, 10, 100} for features *and* n-grams, same grid and folds; scaler / TF-IDF refit on every inner and outer training set | `cr_tuned_accuracy.csv`, `cr_tuned_cell_correct.csv`, `cr_tuned_chosen_C.json` |
| C2 | Exact sign-flip permutation tests on the 12 per-prompt accuracies: the 28 Holm comparisons, judges (Holm over five), all 42 transfer cells per representation, paired features-vs-n-gram transfer, prompt-clustered CIs for translations | `cr_holm_prompt_level.csv`, `cr_judges_prompt_level.csv`, `cr_transfer_prompt_level.csv`, `cr_transfer_cells.csv`, `cr_translation_prompt_level.csv`, `cr_prompt_level_summary.json` |
| C3 | Fragility: leave-one-reading-level-out (train on 2 of 3 instruction tiers, test on the third) for features and n-grams; features without the two paragraph features | `cr_fragility.csv` |
| C4 | RQ4 separation intervals resampling prompts instead of texts | `cr_rq4_prompt_cluster.csv` |

## Reviewer 1

> A small summary table saying when to use interpretable features and when to use n-grams.

New **Table 2**: one-line answer per research question, plus a use-case block (target-language labels → n-grams;
explanation needed → features; cross-language use → features; labelled translations → n-grams). Discussion points to it.

## Reviewer 2

**1. Standardization and tuning.** Sec. 3.3 "Classifiers and tuning" now states: features are standardized inside each
training fold (no missing values, so no imputation); transfer/RQ4 z-scoring uses all texts of a language without labels;
L2 multinomial logistic regression, C = 1 (fixed in the plan for the features; the later n-gram baseline uses the same C);
TF-IDF settings (char_wb 1–4, min_df 2, sublinear tf, ≤ 60k terms, fit on training prompts only), set once and not tuned.
Equal-tuning check (C1): features .56–.73 (mean change < 1 point), n-grams .75–.88 (+2), gap 8–23 points (mean 15).
Tuning helps the n-grams more, so the untuned comparison does not flatter the features.

**2. "Preregistered".** Removed everywhere ("pre-specified"/"planned"). Sec. 3.3 gives the commit: plan committed
3 Sept 2026 in `82673ac` before any response; RQ5 added in `88e08a7` before any translation; RQ6 added in `60593f5` /
`c7232ff` before the judge data, after a small pilot that set the reasoning condition. Repository history is public.

**3. Independence.** All accuracy comparisons are now tested on the 12 per-prompt accuracies (exact sign-flip).
What changed in the text:
- Features vs chance: all 7 languages, Holm p ≤ 0.007 (was text-level p < 1e-4).
- Features vs n-grams: Holm-significant only in Chinese (was Chinese and Turkish; Turkish now p = 0.059). N-grams lead
  in 7–11 of 12 prompts everywhere but English (4).
- Judges: only Claude above chance (12/12 prompts, Holm over five judges p = 0.001; next p = 0.096); Claude's
  self-recognition 10/12 prompts, p = 0.015. Features beat the best judge in all 7 languages, Holm p ≤ 0.016.
- Transfer: all 42 feature cells above chance (Holm p ≤ 0.021); adapted n-grams 16/42; features ahead of n-grams on
  12/12 prompts (paired p = 0.0005).
- Translations: every prompt-clustered interval above chance (lowest .48).
- RQ4: prompt-clustered intervals; centroid distance still separates English and Hindi, scatter ratio and silhouette
  overlap, so the planned convergence rule is still not met.

**4. Closing claim and fragility.** "In this setting (one genre, fixed prompts, one sampling temperature)" in the
abstract; "in this setting" in Discussion and Conclusion. New "Fragility" paragraph (C3): on prompts with an unseen
reading-level instruction the features reach .54–.76 (mean −3 points vs LOPO; n-grams .66–.88, −5); without the two
paragraph features, .51–.69 (LOPO) and .52–.68 (unseen reading level), every prompt-clustered CI above chance.
Format instructions and temperature could not be varied without new generations, so Limitation (ii) states it.

**5. Readability.** Table 2 (shared with Reviewer 1's request).

## Other fixes found while checking

- Fig. 2 panel titles and x-label were clipped in the submitted PDF; Fig. 1b legend overlapped bars. Both fixed.
- Translation paragraph: .521/.531 are per-translator means (now said); the Spanish n-gram figure was Google-only (dropped).
- Judges: "holds in all seven languages" now excepts Claude in Hindi (.361).
- Real minus signs for negative numbers.

## Still to do (authors)

1. All three authors read the final PDF.
2. Electronic copyright form (link on the CyberChair camera-ready page).
3. PDF eXpress (conference ID 70701X) → validated PDF.
4. Upload the validated PDF on CyberChair; registration receipt; in-person choice.
