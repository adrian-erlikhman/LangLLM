# Numbers check: review/draft_2026-09-18.txt vs results/

Recomputed with pandas from `results/*.csv|json`, `data/validation.csv`, `data/features/features.csv`, `data/raw/deepseek.jsonl`, `data/translated/*.jsonl` (script: session scratchpad `check.py`). Date: 2026-09-19.

Legend: **yes** = matches to the stated precision; **half** = value sits on an exact .xx5 and the draft's digit depends on the rounding rule; **NO** = mismatch or unsupported.

## (A) Claim-by-claim

| draft location | claim | recomputed | ok? |
|---|---|---|---|
| Abstract, Intro, Concl. | 840 essays = 5 x 7 x 12 x 2 | 840 rows in validation.csv; 839 kept | yes |
| Abstract, Intro, Concl. | five-way LR accuracy 59–72% in every language | LR 0.592 (tr) – 0.717 (en) | yes |
| Abstract, 4.2 | no decline with resource level, p = 0.36 | GLM p = 0.361 | yes |
| Abstract, 4.3 | mean partial eta2 0.54 (language) vs 0.15 (model) | 0.539 vs **0.1446** (rounds to 0.14) | **NO** (minor: 0.145 -> 0.14, or write 0.145) |
| Abstract, 4.3, Fig. 2 | trained-on-one beats chance on all 42 cross-language pairs | 42 of 42 off-diagonal > 0.20 (min 0.367) | yes |
| Abstract, 4.4 | centroid separation vs rank rho = -0.96 | -0.964, p = 0.00045 | yes |
| Abstract, 4.5 | translated-text attribution 57–70% | LOPO 0.567 (google zh) – 0.700 (llm hi) | yes |
| Abstract, 4.6 | models as judges score 20–25% | 20.3% (DeepSeek) – 25.4% (Claude) | yes |
| Intro contributions | 1,440 machine translations | 1,440 lines in data/translated (120 x 6 x 2) | yes |
| 3.2 | 84 prompts | 12 x 7 = 84 | yes |
| 3.3 | 5 x 12 x 7 x 2 = 840; one Grok Hindi response in English excluded, 839 left | validation.csv: 1 row keep=False, `grok|P06|hi|1`, lang_detected=en | yes |
| 3.3 | ten DeepSeek responses re-collected at 16,000 tokens (4,000 budget) | raw/deepseek.jsonl params: 158 at max_tokens 4000, **10 at 16000** | yes |
| 3.3 | lingua confidence >= 0.6 | min lang_conf in kept data = 1.0 | yes (consistent) |
| Table 1 English | .717 [.65–.79] F1 .711 RF .675 Judge .267 Sep 3.59 | .7167 [.6498–.7917] .7110 .675 .2667 3.592 | yes |
| Table 1 Spanish | .625 [.54–.71] .625 .675 .217 3.11 | .625 [.5417–.7083] .6247 .675 .2167 3.109 | yes |
| Table 1 Chinese | .650 [.56–.73] .644 .650 .233 3.01 | .650 [.5583–**.7250**] .6438 .650 .2333 3.006 | half (.725 -> .72 or .73) |
| Table 1 Russian | .650 [.57–.73] .654 .717 .258 2.97 | .650 [.5667–.7333] .6542 .7167 .2583 2.973 | yes |
| Table 1 Japanese | .708 [.63–.79] .707 .733 .225 2.70 | .7083 [**.6250**–.7917] .7072 .7333 .225 2.700 | half (.625 -> .62 or .63) |
| Table 1 Turkish | .592 [.51–.68] .596 .600 .258 2.84 | .5917 [.5083–.675] .5962 .600 .2583 2.843 | yes (.675 -> .68 half-up) |
| Table 1 Hindi | .639 [.55–.72] .634 .622 .361 2.69 | .6387 [.5544–.7227] .6344 .6218 .3613 2.693 | yes |
| Table 1 caption | Judge = best of five; Spanish best .217 | es: deepseek/gemini/grok tie at .2167; ru best is gemini; others claude | yes |
| Fig. 1 caption | feature classifiers stay between 0.59 and 0.78 | LR+RF: 0.592–0.733; incl. the plotted length-residualised RF: 0.592–0.775 | yes (0.78 is the residualised RF in Spanish; say so or the reader will look for it in Table 1) |
| 4.1 | all p < 1e-20 | max LR p = 6.6e-21, max RF p = 1.1e-21 | yes |
| 4.1 | every CI excludes chance | min CI lower bound 0.508 | yes |
| 4.1 | GPT-5.5 recall 67–92% | 16/24 = 66.7% (es) to 22/24 = 91.7% (ja) | yes |
| 4.1 | Grok 4.3 recall 63–88% | 15/24 = **62.5%** (ru) to 21/24 = 87.5% (en) | half (62.5 -> 62 or 63) |
| 4.1 | Claude Opus 4.7 recall 63–79% | 15/24 = **62.5%** (zh, tr) to 19/24 = 79.2% (es) | half |
| 4.1 | Gemini 3.5 Flash recall 54–75% | 13/24 = 54.2% to 18/24 = 75.0% | yes |
| 4.1 | DeepSeek V4 Pro recall 25–58% | 6/24 = 25.0% (hi) to 14/24 = 58.3% (ja) | yes |
| 4.1 | DeepSeek mistaken for Claude in English, GPT or Gemini in Hindi | en errors: claude 6, gemini 4, gpt 4; hi errors: gpt 7, gemini 5, claude 3, grok 3 | yes |
| 4.1 | "By mean absolute coefficient" fingerprint carried by paragraph count and length, comma and colon rates, lexical diversity (hapax, Zipf, bigram entropy); dep. depth, subordination, question rate contribute little | Mean abs coef averaged over 7 languages: para_count .62, comma .62, bigram_entropy .58, para_len .54, zipf .45, mattr .42, colon .42, **subord_rate .41 (8th of 21)**, ... **hapax .38 (12th)**, ... dep_depth .28, sent_len_sd .24, burstiness .23, question_rate .11 | **NO** for subordination (mid-pack by coefficient) and weak for hapax (12th). The listed pattern matches the ANOVA eta2_model column (hapax top, subord/question/dep_depth <= 0.03), not the LR coefficients. Either attribute the sentence to eta2 or reword. |
| 4.1 | Grok shortest in all seven languages; GPT-5.5 longest in six | validation_summary median_words: Grok min in 7/7; GPT max in 6/7 (Japanese: DeepSeek) | yes (by features.csv n_tokens it is 5/7: zh -> Claude, ja -> DeepSeek) |
| 4.1 | length-residualised LR 0.44–0.57 | 0.442 (zh) – 0.567 (en) | yes |
| 4.1 | length-residualised RF 0.66–0.78 | 0.658 (en) – 0.775 (es) | yes |
| 4.2 | beta = -0.038 log-odds/rank, SE 0.042, p = 0.36 | -0.0383, 0.0419, 0.361 | yes |
| 4.2 | less than one percentage point per step | at acc 0.65: -0.88 pt/step | yes |
| 4.2 | length-residualised beta = -0.053, p = 0.16 | -0.0534, 0.164 | yes |
| 4.2 | Spearman rho = -0.45, p = 0.31 | -0.450, 0.310 | yes |
| 4.2 | Japanese matches English; Hindi > Spanish and Turkish | ja .708 vs en .717; hi .639 > es .625 > tr .592 | yes |
| 4.3 | eta2 means: 0.54 lang, 0.15 model, 0.13 interaction, 0.16 prompt | 0.539, **0.145 (0.1446)**, 0.127, 0.159 | **NO** on model (0.14) |
| 4.3 | token length 0.99, function-word 0.94, hapax 0.93, Zipf 0.93, MATTR 0.88 | 0.990, 0.937, 0.927, 0.933, 0.877 | yes |
| 4.3 | model eta2: hapax 0.38, Zipf 0.37, comma 0.32, bigram 0.31, para count 0.29 | 0.376, 0.372, 0.323, 0.306, 0.294 | yes |
| 4.3 | subordination, question rate, dep. depth <= 0.03 | 0.0135, 0.0139, 0.0303 | yes |
| 4.3, Fig. 2 | cross-language 0.37–0.59, mean 0.49, within 0.65 | 0.367–0.592, 0.486, 0.654 | yes |
| 4.3 | about three quarters transfers (0.49/0.65) | 0.743 | yes |
| Fig. 2 cells | 49 values | all match at 2 dp except three exact halves: zh->es 0.475 (draft .47), ja->en 0.475 (.47), ja->zh 0.475 (.47) | half; note Table 1 rounds .725 -> .73 (half-up) while Fig. 2 rounds .475 -> .47 (half-down). Pick one rule. |
| 4.4 | centroid distance 3.59 -> 2.69, rho = -0.96, p < 0.001 | 3.592 -> 2.693, -0.964, p = 0.00045 | yes |
| 4.4 | Hindi interval entirely below the English one | hi CI hi 2.805 < en CI lo 3.123 | yes |
| 4.4 | between/within 0.41 -> 0.18, rho = -1.00 | 0.412 -> 0.175, -1.0 | yes |
| 4.4 | silhouette 0.04 -> -0.02, rho = -0.93, p = 0.003 | 0.040 -> -0.019, -0.929, p = 0.0025 | yes |
| 4.4 | GPT–Grok 5.69, DeepSeek–Grok 4.86 -> 2.69, 2.02 in Hindi | 5.687, 4.865 -> 2.692, 2.015 | yes |
| 4.4 | Claude–Grok 5.42 -> 3.46 | 5.417 -> 3.463 | yes |
| 4.4 | "the largest English gaps, GPT–Grok and DeepSeek–Grok" | ranking is GPT–Grok 5.69 > Claude–Grok 5.42 > DeepSeek–Grok 4.86 | wording: DeepSeek–Grok is third, Claude–Grok second |
| Table 2 caption | English originals 0.717; native six-language mean 0.644 | 0.7167; 0.6439 | yes |
| Table 2 | LOPO range .57–.66 (Google), .59–.70 (LLM) | .567–.658; .592–.700 | yes |
| Table 2 | LOPO mean .625 / .629 | .6250 / .6292 | yes |
| Table 2 | trained on English originals .664 / .660 | .6639 / .6597 | yes |
| Table 2 | trained on native responses .521 / .531 | .5208 / .5306 | yes |
| Table 2 | features with rho > 0.5 (of 20): 16 / 16 | 16 / 16 of 20 non-NaN (question_rate NaN in all 12 cells) | yes |
| Table 2 | model eta2 .40 -> .32 / .40 -> .30 | .4046 -> .3207 / .4046 -> .2987 | yes |
| 4.5 | every interval excludes chance, p < 0.001 | min CI lo 0.475; max p 1.1e-18 | yes |
| 4.5 | translation costs about nine points | 71.7 - 62.5 = 9.2 (Google), 71.7 - 62.9 = 8.8 (LLM) | yes |
| 4.5 | roughly what moving English -> native lower-resource costs | en - mean(six native) = 7.3 pts; en - mean(tr, hi) = 10.2 pts | yes (rough) |
| 4.5 | trained on English reads translations at 0.66 (0.77 for LLM Hindi) | .664/.660; llm hi .767 | yes |
| 4.5 | trained on native reads them at 0.52–0.53 | .521 / .531 | yes |
| 4.5, Fig. 3 | para count rho 1.00, para length 0.98, sentence length 0.89, burstiness 0.87 | 0.996, 0.980, 0.893, 0.868 (mean over 6 langs x 2 translators) | yes |
| 4.5, Fig. 3 | MATTR 0.32, function-word 0.46, bigram entropy 0.49 | 0.324, 0.460, 0.489 | yes |
| Fig. 3 ordering | 20 features bottom-to-top | identical to the recomputed ascending order | yes (dash rho averages 9 cells and semicolon 10, the rest NaN where the feature is constant, e.g. Japanese) |
| Fig. 3 caption | question rate omitted, essays contain no questions | 0 of 120 English originals have question_rate > 0 | yes |
| 4.5 | model eta2 0.40 -> 0.32 (Google), 0.30 (LLM) | as Table 2 | yes |
| 4.5 | LLM normalises semicolons and colons slightly more | semicolon rho google .88 vs llm .68; colon .84 vs .75 | yes (direction; the semicolon gap is 0.2, "slightly" is generous) |
| 4.6 | judges 20.3% (DeepSeek) to 25.4% (Claude) | 20.26%, 25.39% | yes |
| 4.6 | only Claude above chance, p < 0.001 | Claude p = 8.8e-5; next Grok p = 0.089 | yes |
| 4.6 | Claude's best language Hindi, 36% | 36.1% (43/119) | yes |
| 4.6 | GPT-5.5 names itself for 82% of texts | self_claim_rate 82.4% (691/839) | yes |
| 4.6 | Claude most often names GPT-5.5; other three most often name Claude | Claude -> gpt 614/839; Gemini -> claude 493; Grok -> claude 681; DeepSeek -> claude 497 | yes |
| 4.6 | feature classifier beats best judge by 28–48 points in every language | LR - best judge: hi 27.7, tr 33.3, ru 39.2, es 40.8, zh 41.7, en 45.0, ja 48.3 | yes (27.7 -> 28) |
| 5 Discussion | Hindi and Turkish within a few points of Spanish | hi +1.4, tr -3.3 vs es | yes |
| 5 Limitations | intervals of about +/-8 points | LR CI half-widths 0.071–0.084 | yes |

## (B) Cross-check against CompLLM (review/compllm_numbers.tex, compllm_table_selfadv.tex)

Same five models in both papers. Places where the two can be read against each other:

1. **Judge accuracy.** LangLLM: judges 20.3–25.4% overall, 20.0–26.7% in English (single text, candidate list, reasoning off, temperature 0). CompLLM: single-text 30.6%, lineup 33.7% (English, reasoning allowed in the lineup). Not contradictory once the conditions are stated, but the abstract's "score 20–25%" carries no condition; a reader who knows CompLLM will ask why the same models score 31–34% there. Suggest: add "without reasoning" to the abstract and cite [21] at the RQ6 sentence "judges allowed to reason may do better", with CompLLM's 30.6/33.7 as the reasoning-on reference.
2. **Claude's self-recognition is the sharpest tension.** CompLLM: Claude self rate 86.8% in both lineup and single-text, false alarm 8.6–9.2%, +32.9 self-advantage, "only Claude's self rate matches the classifier". LangLLM: Claude own-recall 17.3% overall, 25% in English, and Claude "most often names GPT-5.5" (614/839). Same model, same kind of question, 87% vs 17–25%. This is explainable (reasoning disabled; different prompt; different genre) but it must be explained in the text or a reviewer will call it a contradiction. Note rq6_judge_summary.csv does contain the self-recognition numbers (own_recall 17.3% vs false_self_rate 6.6%, Fisher p = 3.8e-5), so LangLLM can say Claude still shows a small but significant self-advantage.
3. **GPT's self-naming.** CompLLM single-text: GPT self 94.7%, false alarm 52.0%, self-advantage +33.6. LangLLM: GPT own recall 82.1%, false-self 82.4%, i.e. no self-advantage (Fisher p = 0.58). Direction of over-claiming agrees; the size of the self-advantage does not (+33.6 vs ~0). Same explanation as item 2; worth one sentence.
4. **Guess concentration.** CompLLM single-text: 99.3% of guesses on GPT or Claude. LangLLM: 89.1% of all judge guesses land on GPT or Claude. Consistent; could be cited as corroboration.
5. **Stylometric classifier accuracy.** CompLLM: 86.3% [80.7, 90.5] with 18 features on 190 English responses. LangLLM English: 71.7% LR / 67.5% RF with 21 UD features on 120 responses. Different feature sets, genre and n, but both are "interpretable stylometry on the same five models in English"; a reader may take 72 vs 86 as disagreement. Also a coincidence trap: CompLLM's length-free LR is 71.7%, identical to LangLLM's English LR. Suggest one sentence in 3.4 or 5 explaining why the UD set is deliberately smaller/language-neutral.
6. **Length removal.** CompLLM: length-free RF 63.9% < LR 71.7% (linear model survives length removal better). LangLLM English: residualised LR 0.567 < RF 0.658, and the draft concludes the length-independent fingerprint "is non-linear". Opposite ordering of LR and RF after length control across the two papers. Not a numeric contradiction (different procedures: feature dropping vs residualising) but the LangLLM sentence should not be phrased as a general property of these models.
7. **Reference [21] title.** "Self-attribution is not self-recognition: A peer baseline for LLM judges" cannot be verified from the two .tex snippets; check against the CompLLM manuscript.

## (C) Numbers in results/ the draft does not report

1. **RQ7 n-gram baselines (rq7_ngram_accuracy.csv).** Char n-gram LR: 0.733 (es) – 0.867 (zh), mean 0.784; word n-gram: 0.558 (zh) – 0.833 (tr), mean 0.743. Char n-grams beat the UD features in every language, but by McNemar with Holm correction (rq7_holm.csv) only in Chinese (-0.217, p_holm 9e-5) and Turkish (-0.192, p_holm 0.0065); the other five are n.s. This is the obvious reviewer question ("why not n-grams?") and it is answered in results/ but not in the draft.
2. **RQ7 n-gram transfer (rq7_ngram_transfer_matrix.csv, rq7_ngram_summary.json).** Char n-gram cross-lingual off-diagonal mean 0.277 (range 0.200–0.500; 28 of 42 above 0.20, only 19 above 0.25, most rows 0.20 exactly) vs 0.486 and 42/42 for UD features. Strongest available support for the "shared fingerprint" claim in 4.3.
3. **RQ7 n-gram on translations (rq7_ngram_translation.csv).** Char n-gram LOPO on translations 0.633–0.775 (mean 0.722) but train-on-English-originals -> translations 0.20–0.60, mean 0.28–0.30 (only Spanish above chance) vs 0.66 for UD features. Directly supports 4.5's "a classifier trained on English can be applied across a translation boundary" and shows that it is a property of the UD features, not of attribution in general.
4. **Feature-count curve (rq7_feature_curve.csv).** Pooled accuracy k=3 0.540, k=5 0.576, k=10 0.591, k=21 0.616 (max 0.622 at k=20); English reaches 0.75 at k=13. Supports the 4.4 sentence "a classifier needs only the few that keep separating the models" with a number.
5. **Group ablation (rq7_group_ablation.csv).** Removing punctuation costs up to 0.11 macro-F1 (Hindi), 0.10 (Russian), 0.08 (Japanese); removing syntax costs 0.11 (Turkish), 0.09 (Hindi); removing character features helps in English (+0.03) and Chinese punctuation removal helps (+0.04). Structure alone reaches 0.62 (ru) / 0.60 (tr). Would replace the qualitative feature-importance sentence in 4.1 that currently misreads the coefficients.
6. **Holm correction (rq7_holm.csv).** 28 tests in one family; every features-vs-chance and features-vs-best-judge comparison stays significant after Holm. The draft reports raw p only; one clause "all survive Holm correction over 28 tests" would pre-empt a multiple-comparisons objection.
7. **Self-recognition in RQ6 (rq6_judge_summary.csv).** own_recall, false_self_rate, Fisher p per judge: Claude 17.3% vs 6.6%, p = 3.8e-5; GPT 82.1% vs 82.4%, p = 0.58; Gemini 3.0% vs 4.3%; DeepSeek 6.5% vs 8.2%; Grok 0.0% vs 0.1%. Unreported, and exactly what is needed for the CompLLM reconciliation in (B) 2–3. Gemini unparsed rate 0.12% (1 answer "none") is the only parse failure.
8. **RF gradient (rq2_gradient.json, rq2_gradient_lenctl.json).** RF Spearman rho = -0.38 (p = 0.40); length-residualised RF rho = -0.02 (p = 0.97), OLS slope -0.002/rank. The draft reports only the LR rho and the GLM; the residualised RF is the flattest gradient in the files.
9. **Mean feature rho under translation (rq5_summary.json).** 0.742 (Google), 0.714 (LLM). Table 2 gives the count above 0.5 but not the mean.
10. **ANOVA p-values (rq3_anova_eta2.csv).** Model effect significant for all 21 features (max p = 0.029, subord_rate); interaction n.s. for para_len_mean, question_rate, digit_rate. Not stated.
11. **RQ4 silhouette and scatter-ratio CIs (rq4_separation.csv).** Only the centroid-distance CI is used in the text.
12. **Median length per model (validation_summary.csv).** Grok 226–387 words, GPT 330–587; the 4.1 length paragraph is qualitative only.
13. **rq1_univariate_F.csv, rq1_feature_importance_lenctl.csv, rq1_cell_correct*.csv.** Not referenced; univariate F could replace the coefficient-ranking sentence.
