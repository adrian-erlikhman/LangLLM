# LangLLM: every number for the paper (generated)

Source of truth: `results/`. Regenerate with `python -m langllm.paper_numbers`. Macros in `paper/numbers.tex`.

## Table 1 (per language)

| Language | Rank | LR acc [cluster 95% CI] | macro-F1 | RF | char n-gram [CI] | word n-gram | judge mean of 5 | best judge | centroid sep. |
|---|---|---|---|---|---|---|---|---|---|
| English | 1 | .717 [.61, .82] | .711 | .675 | .750 [.71, .79] | .783 | .230 | .267 (Claude Opus 4.7) | 3.59 |
| Spanish | 2 | .625 [.53, .70] | .625 | .675 | .733 [.65, .80] | .783 | .207 | .217 (Grok 4.3) | 3.11 |
| Chinese | 3 | .650 [.55, .73] | .644 | .650 | .867 [.81, .93] | .558 | .208 | .233 (Claude Opus 4.7) | 3.01 |
| Russian | 4 | .650 [.52, .78] | .654 | .717 | .783 [.66, .88] | .825 | .237 | .258 (Gemini 3.5 Flash) | 2.97 |
| Japanese | 5 | .708 [.63, .78] | .707 | .733 | .792 [.71, .87] | .683 | .198 | .225 (Claude Opus 4.7) | 2.70 |
| Turkish | 6 | .592 [.50, .69] | .596 | .600 | .783 [.73, .84] | .833 | .205 | .258 (Claude Opus 4.7) | 2.84 |
| Hindi | 7 | .639 [.56, .71] | .634 | .622 | .782 [.73, .83] | .731 | .247 | .361 (Claude Opus 4.7) | 2.69 |

## Holm-corrected headline comparisons (28 tests)

| family                            | lang   |   effect |   p_raw |   p_holm | significant_holm_05   |
|:----------------------------------|:-------|---------:|--------:|---------:|:----------------------|
| features vs chance                | en     |   0.5167 |  0      |   0      | True                  |
| char n-gram vs chance             | en     |   0.55   |  0      |   0      | True                  |
| features vs char n-gram           | en     |  -0.0333 |  0.5966 |   0.5966 | False                 |
| features vs best judge (claude)   | en     |   0.45   |  0      |   0      | True                  |
| features vs chance                | es     |   0.425  |  0      |   0      | True                  |
| char n-gram vs chance             | es     |   0.5333 |  0      |   0      | True                  |
| features vs char n-gram           | es     |  -0.1083 |  0.066  |   0.198  | False                 |
| features vs best judge (deepseek) | es     |   0.4083 |  0      |   0      | True                  |
| features vs chance                | zh     |   0.45   |  0      |   0      | True                  |
| char n-gram vs chance             | zh     |   0.6667 |  0      |   0      | True                  |
| features vs char n-gram           | zh     |  -0.2167 |  0      |   0.0001 | True                  |
| features vs best judge (claude)   | zh     |   0.4167 |  0      |   0      | True                  |
| features vs chance                | ru     |   0.45   |  0      |   0      | True                  |
| char n-gram vs chance             | ru     |   0.5833 |  0      |   0      | True                  |
| features vs char n-gram           | ru     |  -0.1333 |  0.0195 |   0.0781 | False                 |
| features vs best judge (gemini)   | ru     |   0.3917 |  0      |   0      | True                  |
| features vs chance                | ja     |   0.5083 |  0      |   0      | True                  |
| char n-gram vs chance             | ja     |   0.5917 |  0      |   0      | True                  |
| features vs char n-gram           | ja     |  -0.0833 |  0.1742 |   0.3483 | False                 |
| features vs best judge (claude)   | ja     |   0.4833 |  0      |   0      | True                  |
| features vs chance                | tr     |   0.3917 |  0      |   0      | True                  |
| char n-gram vs chance             | tr     |   0.5833 |  0      |   0      | True                  |
| features vs char n-gram           | tr     |  -0.1917 |  0.0011 |   0.0065 | True                  |
| features vs best judge (claude)   | tr     |   0.3333 |  0      |   0      | True                  |
| features vs chance                | hi     |   0.4387 |  0      |   0      | True                  |
| char n-gram vs chance             | hi     |   0.5815 |  0      |   0      | True                  |
| features vs char n-gram           | hi     |  -0.1429 |  0.0137 |   0.0686 | False                 |
| features vs best judge (claude)   | hi     |   0.2773 |  0      |   0      | True                  |

## Per-judge (RQ6, single-text protocol, reasoning off)

| judge    |   n |   accuracy |   p_vs_chance |   own_recall |   false_self_rate |   self_recognition_p_fisher |   self_claim_rate |   unparsed_rate |
|:---------|----:|-----------:|--------------:|-------------:|------------------:|----------------------------:|------------------:|----------------:|
| claude   | 839 |     0.2539 |        0.0001 |       0.1726 |            0.0656 |                      0      |            0.087  |          0      |
| grok     | 839 |     0.2193 |        0.0888 |       0      |            0.0015 |                      1      |            0.0012 |          0      |
| gemini   | 839 |     0.2122 |        0.2005 |       0.0298 |            0.0432 |                      0.8444 |            0.0405 |          0.0012 |
| gpt      | 839 |     0.2062 |        0.3399 |       0.8214 |            0.8241 |                      0.5831 |            0.8236 |          0      |
| deepseek | 839 |     0.2026 |        0.4383 |       0.0655 |            0.082  |                      0.8061 |            0.0787 |          0      |

## Claude own-text recall per language (n = 24 each; Clopper-Pearson 95% CI)

- English: 25\% [10\%, 47\%]
- Spanish: 0\% [0\%, 14\%]
- Chinese: 8\% [1\%, 27\%]
- Russian: 0\% [0\%, 14\%]
- Japanese: 38\% [19\%, 59\%]
- Turkish: 8\% [1\%, 27\%]
- Hindi: 42\% [22\%, 63\%]

## Transfer matrices

Features (within-language z-scored):

|    |   en |   es |   zh |   ru |   ja |   tr |   hi |
|:---|-----:|-----:|-----:|-----:|-----:|-----:|-----:|
| en | 0.72 | 0.52 | 0.43 | 0.38 | 0.41 | 0.39 | 0.44 |
| es | 0.58 | 0.62 | 0.5  | 0.48 | 0.54 | 0.48 | 0.55 |
| zh | 0.57 | 0.48 | 0.65 | 0.38 | 0.45 | 0.37 | 0.48 |
| ru | 0.56 | 0.53 | 0.51 | 0.65 | 0.39 | 0.52 | 0.49 |
| ja | 0.48 | 0.59 | 0.48 | 0.45 | 0.71 | 0.43 | 0.5  |
| tr | 0.45 | 0.45 | 0.37 | 0.51 | 0.51 | 0.59 | 0.59 |
| hi | 0.58 | 0.58 | 0.52 | 0.5  | 0.47 | 0.56 | 0.64 |

Char n-gram, naive (vocabulary from train language only):

|    |   en |   es |   zh |   ru |   ja |   tr |   hi |
|:---|-----:|-----:|-----:|-----:|-----:|-----:|-----:|
| en | 0.75 | 0.35 | 0.21 | 0.2  | 0.2  | 0.21 | 0.24 |
| es | 0.5  | 0.73 | 0.21 | 0.21 | 0.21 | 0.22 | 0.24 |
| zh | 0.2  | 0.2  | 0.87 | 0.39 | 0.34 | 0.2  | 0.37 |
| ru | 0.2  | 0.2  | 0.35 | 0.78 | 0.32 | 0.2  | 0.4  |
| ja | 0.2  | 0.2  | 0.43 | 0.31 | 0.79 | 0.2  | 0.36 |
| tr | 0.28 | 0.26 | 0.43 | 0.45 | 0.28 | 0.78 | 0.43 |
| hi | 0.2  | 0.2  | 0.3  | 0.22 | 0.32 | 0.2  | 0.78 |

Char n-gram, fair (union vocabulary, z-scored within language; diagonal = LOPO without z-scoring, reference only):

|    |   en |   es |   zh |   ru |   ja |   tr |   hi |
|:---|-----:|-----:|-----:|-----:|-----:|-----:|-----:|
| en | 0.75 | 0.62 | 0.32 | 0.48 | 0.39 | 0.36 | 0.37 |
| es | 0.68 | 0.73 | 0.31 | 0.5  | 0.38 | 0.4  | 0.39 |
| zh | 0.32 | 0.31 | 0.87 | 0.41 | 0.54 | 0.42 | 0.17 |
| ru | 0.49 | 0.52 | 0.44 | 0.78 | 0.28 | 0.49 | 0.39 |
| ja | 0.31 | 0.42 | 0.56 | 0.3  | 0.79 | 0.33 | 0.32 |
| tr | 0.34 | 0.35 | 0.45 | 0.48 | 0.37 | 0.78 | 0.48 |
| hi | 0.34 | 0.39 | 0.4  | 0.42 | 0.32 | 0.47 | 0.78 |

Script-neutral char model (punctuation, digits, whitespace only):

|    |   en |   es |   zh |   ru |   ja |   tr |   hi |
|:---|-----:|-----:|-----:|-----:|-----:|-----:|-----:|
| en | 0.64 | 0.55 | 0.28 | 0.44 | 0.37 | 0.44 | 0.45 |
| es | 0.6  | 0.49 | 0.27 | 0.59 | 0.28 | 0.46 | 0.4  |
| zh | 0.18 | 0.21 | 0.7  | 0.22 | 0.32 | 0.25 | 0.29 |
| ru | 0.45 | 0.5  | 0.3  | 0.63 | 0.26 | 0.47 | 0.45 |
| ja | 0.28 | 0.31 | 0.47 | 0.26 | 0.5  | 0.22 | 0.22 |
| tr | 0.38 | 0.48 | 0.27 | 0.5  | 0.3  | 0.57 | 0.45 |
| hi | 0.4  | 0.49 | 0.41 | 0.52 | 0.42 | 0.5  | 0.81 |

## Translation (RQ5 and n-gram counterpart)

| translator   | lang   |   acc_translated_lopo |   ci_lo |   ci_hi |   acc_english_originals |   acc_native_same_lang |   acc_train_native_test_translated |   acc_train_english_test_translated |
|:-------------|:-------|----------------------:|--------:|--------:|------------------------:|-----------------------:|-----------------------------------:|------------------------------------:|
| google       | es     |                 0.608 |   0.517 |   0.692 |                   0.717 |                  0.625 |                              0.583 |                               0.717 |
| google       | zh     |                 0.567 |   0.475 |   0.65  |                   0.717 |                  0.65  |                              0.467 |                               0.633 |
| google       | ru     |                 0.658 |   0.575 |   0.742 |                   0.717 |                  0.65  |                              0.542 |                               0.717 |
| google       | ja     |                 0.658 |   0.575 |   0.742 |                   0.717 |                  0.708 |                              0.525 |                               0.575 |
| google       | tr     |                 0.608 |   0.517 |   0.692 |                   0.717 |                  0.592 |                              0.467 |                               0.65  |
| google       | hi     |                 0.65  |   0.567 |   0.725 |                   0.717 |                  0.639 |                              0.542 |                               0.692 |
| llm          | es     |                 0.6   |   0.516 |   0.683 |                   0.717 |                  0.625 |                              0.617 |                               0.75  |
| llm          | zh     |                 0.667 |   0.583 |   0.75  |                   0.717 |                  0.65  |                              0.483 |                               0.625 |
| llm          | ru     |                 0.608 |   0.516 |   0.7   |                   0.717 |                  0.65  |                              0.508 |                               0.658 |
| llm          | ja     |                 0.608 |   0.517 |   0.692 |                   0.717 |                  0.708 |                              0.55  |                               0.508 |
| llm          | tr     |                 0.592 |   0.5   |   0.675 |                   0.717 |                  0.592 |                              0.442 |                               0.65  |
| llm          | hi     |                 0.7   |   0.617 |   0.783 |                   0.717 |                  0.639 |                              0.583 |                               0.767 |

| translator   | lang   |   rank |   n |   acc_translated_lopo |   acc_train_english_test_translated |
|:-------------|:-------|-------:|----:|----------------------:|------------------------------------:|
| google       | es     |      2 | 120 |                 0.708 |                               0.567 |
| google       | zh     |      3 | 120 |                 0.733 |                               0.242 |
| google       | ru     |      4 | 120 |                 0.758 |                               0.217 |
| google       | ja     |      5 | 120 |                 0.675 |                               0.242 |
| google       | tr     |      6 | 120 |                 0.75  |                               0.217 |
| google       | hi     |      7 | 120 |                 0.775 |                               0.208 |
| llm          | es     |      2 | 120 |                 0.733 |                               0.6   |
| llm          | zh     |      3 | 120 |                 0.725 |                               0.2   |
| llm          | ru     |      4 | 120 |                 0.733 |                               0.217 |
| llm          | ja     |      5 | 120 |                 0.633 |                               0.283 |
| llm          | tr     |      6 | 120 |                 0.733 |                               0.225 |
| llm          | hi     |      7 | 120 |                 0.708 |                               0.258 |

## Feature-selection curve (macro-F1, nested)

| lang   |    1 |    2 |    3 |    4 |    5 |    6 |    7 |    8 |    9 |   10 |   11 |   12 |   13 |   14 |   15 |   16 |   17 |   18 |   19 |   20 |   21 |
|:-------|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|
| en     | 0.32 | 0.39 | 0.56 | 0.59 | 0.65 | 0.64 | 0.63 | 0.63 | 0.67 | 0.71 | 0.72 | 0.73 | 0.74 | 0.72 | 0.72 | 0.73 | 0.74 | 0.73 | 0.73 | 0.71 | 0.71 |
| es     | 0.3  | 0.47 | 0.56 | 0.61 | 0.63 | 0.68 | 0.62 | 0.59 | 0.61 | 0.61 | 0.59 | 0.62 | 0.64 | 0.62 | 0.64 | 0.65 | 0.64 | 0.65 | 0.63 | 0.62 | 0.62 |
| hi     | 0.32 | 0.41 | 0.47 | 0.49 | 0.5  | 0.55 | 0.53 | 0.57 | 0.58 | 0.54 | 0.56 | 0.64 | 0.64 | 0.63 | 0.63 | 0.6  | 0.6  | 0.62 | 0.63 | 0.64 | 0.63 |
| ja     | 0.36 | 0.5  | 0.63 | 0.67 | 0.75 | 0.72 | 0.79 | 0.74 | 0.73 | 0.72 | 0.71 | 0.73 | 0.73 | 0.72 | 0.67 | 0.7  | 0.69 | 0.71 | 0.71 | 0.71 | 0.71 |
| pooled | 0.3  | 0.48 | 0.53 | 0.56 | 0.57 | 0.59 | 0.58 | 0.58 | 0.58 | 0.58 | 0.59 | 0.6  | 0.62 | 0.61 | 0.61 | 0.61 | 0.6  | 0.61 | 0.62 | 0.62 | 0.61 |
| ru     | 0.31 | 0.51 | 0.62 | 0.68 | 0.68 | 0.63 | 0.62 | 0.64 | 0.63 | 0.65 | 0.63 | 0.65 | 0.62 | 0.6  | 0.63 | 0.61 | 0.62 | 0.65 | 0.67 | 0.67 | 0.65 |
| tr     | 0.25 | 0.42 | 0.53 | 0.54 | 0.51 | 0.52 | 0.45 | 0.43 | 0.49 | 0.51 | 0.53 | 0.56 | 0.59 | 0.59 | 0.59 | 0.57 | 0.58 | 0.56 | 0.59 | 0.6  | 0.6  |
| zh     | 0.43 | 0.54 | 0.63 | 0.63 | 0.63 | 0.69 | 0.65 | 0.69 | 0.69 | 0.69 | 0.7  | 0.7  | 0.69 | 0.68 | 0.66 | 0.65 | 0.65 | 0.66 | 0.65 | 0.62 | 0.64 |

Consensus orders:

- en: para_len_mean > subord_rate > func_word_ratio > zipf_slope > mean_token_len > mattr > hapax_rate > dep_depth > comma_per_1k > colon_per_1k > sent_len_mean > burstiness > semicolon_per_1k > dash_per_1k > first_person_rate > para_count > sent_len_sd > bigram_entropy > digit_rate > connective_rate > question_rate
- es: colon_per_1k > comma_per_1k > first_person_rate > para_count > para_len_mean > mattr > subord_rate > digit_rate > semicolon_per_1k > dash_per_1k > bigram_entropy > zipf_slope > connective_rate > func_word_ratio > sent_len_mean > hapax_rate > mean_token_len > sent_len_sd > burstiness > dep_depth > question_rate
- hi: comma_per_1k > bigram_entropy > para_count > zipf_slope > digit_rate > dash_per_1k > connective_rate > subord_rate > first_person_rate > mean_token_len > func_word_ratio > sent_len_mean > semicolon_per_1k > hapax_rate > para_len_mean > colon_per_1k > dep_depth > sent_len_sd > burstiness > question_rate > mattr
- ja: bigram_entropy > para_count > comma_per_1k > para_len_mean > zipf_slope > first_person_rate > func_word_ratio > connective_rate > hapax_rate > sent_len_mean > sent_len_sd > subord_rate > mattr > mean_token_len > digit_rate > burstiness > dep_depth > colon_per_1k > question_rate > dash_per_1k > semicolon_per_1k
- ru: para_count > comma_per_1k > colon_per_1k > para_len_mean > dash_per_1k > bigram_entropy > zipf_slope > subord_rate > hapax_rate > digit_rate > semicolon_per_1k > func_word_ratio > mean_token_len > first_person_rate > sent_len_mean > question_rate > connective_rate > mattr > dep_depth > sent_len_sd > burstiness
- tr: para_len_mean > para_count > connective_rate > mattr > digit_rate > sent_len_mean > dep_depth > bigram_entropy > burstiness > hapax_rate > subord_rate > func_word_ratio > mean_token_len > semicolon_per_1k > first_person_rate > colon_per_1k > dash_per_1k > sent_len_sd > question_rate > comma_per_1k > zipf_slope
- zh: bigram_entropy > mattr > comma_per_1k > para_count > zipf_slope > semicolon_per_1k > hapax_rate > connective_rate > mean_token_len > dash_per_1k > func_word_ratio > sent_len_mean > first_person_rate > para_len_mean > colon_per_1k > digit_rate > dep_depth > sent_len_sd > subord_rate > burstiness > question_rate
- pooled: para_count > para_len_mean > sent_len_mean > comma_per_1k > hapax_rate > sent_len_sd > first_person_rate > bigram_entropy > zipf_slope > mattr > func_word_ratio > connective_rate > dep_depth > digit_rate > burstiness > dash_per_1k > semicolon_per_1k > colon_per_1k > mean_token_len > subord_rate > question_rate

## Group ablation (macro-F1)

Only this group:

| group       |   en |   es |   hi |   ja |   ru |   tr |   zh |
|:------------|-----:|-----:|-----:|-----:|-----:|-----:|-----:|
| character   | 0.21 | 0.33 | 0.29 | 0.41 | 0.32 | 0.35 | 0.46 |
| lexical     | 0.54 | 0.36 | 0.33 | 0.37 | 0.35 | 0.35 | 0.55 |
| punctuation | 0.45 | 0.49 | 0.37 | 0.36 | 0.53 | 0.26 | 0.42 |
| structure   | 0.41 | 0.45 | 0.42 | 0.52 | 0.61 | 0.56 | 0.31 |
| syntactic   | 0.53 | 0.47 | 0.37 | 0.37 | 0.24 | 0.46 | 0.28 |

Without this group (delta vs all 21):

| group       |     en |     es |     hi |     ja |     ru |     tr |     zh |
|:------------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| character   |  0.033 |  0.002 | -0.016 | -0.03  |  0.005 | -0.062 | -0.017 |
| lexical     | -0.081 | -0.025 | -0.076 | -0.017 | -0.009 | -0.009 | -0.05  |
| punctuation | -0.001 | -0.026 | -0.11  | -0.083 | -0.097 | -0.006 |  0.042 |
| structure   | -0.004 | -0.055 | -0.025 | -0.051 | -0.073 | -0.058 |  0.002 |
| syntactic   | -0.062 | -0.027 | -0.087 |  0.02  | -0.023 | -0.106 | -0.008 |

## RQ2 gradient

{
 "features_glm": {
  "beta": -0.03834525956280303,
  "se": 0.041937070244030275,
  "ci95": [
   -0.12054191724110237,
   0.04385139811549631
  ],
  "p": 0.3605317207558639,
  "acc_english": 0.7166666666666667,
  "steepest_decline_compatible_acc_at_rank7": 0.5510057759631654,
  "steepest_decline_points": 16.56608907035013
 },
 "char_ngram": {
  "spearman_rho": 0.3243374865704013,
  "spearman_p": 0.477885479739931,
  "acc_english": 0.75,
  "acc_hindi": 0.7815126050420168,
  "glm_beta": 0.02532655303847206,
  "glm_se": 0.02882182634926805,
  "glm_p": 0.3795486373701096
 }
}

Language-clustered GLM: beta -0.038, SE 0.032, p $p = 0.226$; language x prompt clustered: SE 0.040, p $p = 0.343$.

## RQ3 partial eta-squared

| feature           |   eta2_model |   eta2_lang |   eta2_interaction |   eta2_prompt |   p_model |   p_lang |   p_interaction |
|:------------------|-------------:|------------:|-------------------:|--------------:|----------:|---------:|----------------:|
| mattr             |        0.098 |       0.877 |              0.178 |         0.15  |     0     |        0 |           0     |
| hapax_rate        |        0.376 |       0.927 |              0.173 |         0.257 |     0     |        0 |           0     |
| mean_token_len    |        0.112 |       0.99  |              0.206 |         0.42  |     0     |        0 |           0     |
| zipf_slope        |        0.372 |       0.933 |              0.174 |         0.223 |     0     |        0 |           0     |
| sent_len_mean     |        0.049 |       0.601 |              0.11  |         0.151 |     0     |        0 |           0     |
| sent_len_sd       |        0.116 |       0.392 |              0.052 |         0.174 |     0     |        0 |           0.011 |
| burstiness        |        0.152 |       0.071 |              0.07  |         0.078 |     0     |        0 |           0     |
| dep_depth         |        0.03  |       0.406 |              0.178 |         0.083 |     0     |        0 |           0     |
| subord_rate       |        0.014 |       0.77  |              0.117 |         0.159 |     0.029 |        0 |           0     |
| func_word_ratio   |        0.107 |       0.937 |              0.147 |         0.263 |     0     |        0 |           0     |
| first_person_rate |        0.078 |       0.031 |              0.057 |         0.126 |     0     |        0 |           0.003 |
| para_count        |        0.294 |       0.119 |              0.061 |         0.1   |     0     |        0 |           0.001 |
| para_len_mean     |        0.084 |       0.216 |              0.038 |         0.09  |     0     |        0 |           0.161 |
| question_rate     |        0.014 |       0.073 |              0.034 |         0.107 |     0.025 |        0 |           0.257 |
| connective_rate   |        0.112 |       0.796 |              0.161 |         0.193 |     0     |        0 |           0     |
| comma_per_1k      |        0.323 |       0.619 |              0.177 |         0.199 |     0     |        0 |           0     |
| colon_per_1k      |        0.213 |       0.463 |              0.28  |         0.028 |     0     |        0 |           0     |
| dash_per_1k       |        0.091 |       0.498 |              0.086 |         0.067 |     0     |        0 |           0     |
| semicolon_per_1k  |        0.04  |       0.564 |              0.049 |         0.079 |     0     |        0 |           0.019 |
| bigram_entropy    |        0.306 |       0.974 |              0.306 |         0.12  |     0     |        0 |           0     |
| digit_rate        |        0.057 |       0.07  |              0.02  |         0.277 |     0     |        0 |           0.879 |
| MEAN              |        0.145 |       0.539 |              0.127 |         0.159 |   nan     |      nan |         nan     |

## RQ4 separation

| lang   |   rank |   n |   centroid_dist |   silhouette |   between_within_ratio |   centroid_dist_ci_lo |   centroid_dist_ci_hi |   silhouette_ci_lo |   silhouette_ci_hi |   between_within_ratio_ci_lo |   between_within_ratio_ci_hi |
|:-------|-------:|----:|----------------:|-------------:|-----------------------:|----------------------:|----------------------:|-------------------:|-------------------:|-----------------------------:|-----------------------------:|
| en     |      1 | 120 |           3.592 |        0.04  |                  0.412 |                 3.123 |                 3.758 |             -0.023 |              0.033 |                        0.264 |                        0.443 |
| es     |      2 | 120 |           3.109 |        0.021 |                  0.242 |                 2.559 |                 3.196 |             -0.036 |              0.013 |                        0.126 |                        0.248 |
| zh     |      3 | 120 |           3.006 |        0.027 |                  0.225 |                 2.441 |                 3.098 |             -0.028 |              0.025 |                        0.114 |                        0.232 |
| ru     |      4 | 120 |           2.973 |        0.009 |                  0.216 |                 2.399 |                 3.106 |             -0.047 |              0.002 |                        0.097 |                        0.231 |
| ja     |      5 | 120 |           2.7   |        0.018 |                  0.211 |                 2.191 |                 2.784 |             -0.039 |              0.026 |                        0.111 |                        0.212 |
| tr     |      6 | 120 |           2.843 |        0.008 |                  0.203 |                 2.254 |                 2.948 |             -0.052 |              0.007 |                        0.084 |                        0.219 |
| hi     |      7 | 119 |           2.693 |       -0.019 |                  0.175 |                 2.105 |                 2.805 |             -0.081 |             -0.019 |                        0.067 |                        0.188 |

| pair            |   en |   es |   hi |   ja |   ru |   tr |   zh |
|:----------------|-----:|-----:|-----:|-----:|-----:|-----:|-----:|
| claude-deepseek | 2.35 | 2.73 | 2.57 | 1.67 | 2.92 | 2.42 | 1.67 |
| claude-gemini   | 3.19 | 3.78 | 3.78 | 1.96 | 2.63 | 2.19 | 2.63 |
| claude-gpt      | 3.49 | 3.38 | 3.58 | 3.18 | 3.64 | 3.79 | 2.5  |
| claude-grok     | 5.42 | 4.15 | 3.46 | 3.39 | 3.33 | 4.32 | 3.87 |
| deepseek-gemini | 2.09 | 2.11 | 2.02 | 1.81 | 2.6  | 1.28 | 2.25 |
| deepseek-gpt    | 2.14 | 2.08 | 1.41 | 2.63 | 2.43 | 2.12 | 2.81 |
| deepseek-grok   | 4.86 | 2.9  | 2.02 | 3.3  | 2.22 | 3.06 | 3.01 |
| gemini-gpt      | 3.14 | 3.67 | 2.44 | 2.76 | 3.95 | 2.69 | 3.75 |
| gemini-grok     | 3.55 | 2.55 | 2.96 | 2.49 | 2.18 | 3.25 | 3.58 |
| gpt-grok        | 5.69 | 3.75 | 2.69 | 3.8  | 3.83 | 3.32 | 3.99 |

## Feature survival under translation (mean Spearman rho over 6 languages x 2 translators)

| feature           |   spearman_rho |
|:------------------|---------------:|
| para_count        |           1    |
| para_len_mean     |           0.98 |
| digit_rate        |           0.95 |
| sent_len_mean     |           0.89 |
| burstiness        |           0.87 |
| first_person_rate |           0.84 |
| sent_len_sd       |           0.83 |
| colon_per_1k      |           0.8  |
| semicolon_per_1k  |           0.78 |
| dep_depth         |           0.77 |
| hapax_rate        |           0.73 |
| subord_rate       |           0.73 |
| zipf_slope        |           0.7  |
| comma_per_1k      |           0.68 |
| dash_per_1k       |           0.66 |
| mean_token_len    |           0.6  |
| bigram_entropy    |           0.49 |
| connective_rate   |           0.49 |
| func_word_ratio   |           0.46 |
| mattr             |           0.32 |
| question_rate     |         nan    |

## Notes from the audits

- mean |coef| ranking: paragraph count 0.62, comma rate 0.61, char-bigram entropy 0.58, paragraph length 0.54, Zipf slope 0.45, MATTR 0.42, colon rate 0.42, subordination 0.41, function-word ratio 0.40, connective rate 0.40, first-person rate 0.39, hapax rate 0.38, token length 0.36, sentence length 0.36, digit rate 0.35, dash rate 0.32, semicolon rate 0.32, dependency depth 0.28, sentence-length SD 0.24, burstiness 0.23, question rate 0.11
- RQ2: report beta with 95% CI and the steepest compatible decline; three clusterings (prompt / language / language x prompt) all give p > 0.3.
- RQ6 is the single-text protocol (Bai et al.); CompLLM's headline lineup allows reasoning and shows five responses side by side. CompLLM's single-text condition matches ours.
- 'n-grams transfer at chance' is NOT supported once n-grams get within-language adaptation (0.41 vs 0.49 for features); the naive figure (0.28, 14 constant-prediction cells) is a vocabulary-overlap failure.
- Novelty narrows to: same-definition features in every language, content held fixed, resource gradient, convergence. La Cava et al. (ACL 2026) and Sun et al. (ICML 2025) must be cited as prior multilingual / translation attribution.
- Rounding rule everywhere: half-up.
