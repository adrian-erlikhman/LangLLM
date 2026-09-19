# Bibliography and novelty check — LangLLM draft of 2026-09-18

Draft: `review/draft_2026-09-18.txt` ("Do LLM Fingerprints Survive Outside English?"). Checked 19 Sept 2026 by web search against ACL Anthology, PMLR, arXiv, publisher pages and dblp.

## 1. Reference-by-reference verification

Legend: OK = title, authors, venue and year all confirmed. Page numbers are given where the draft omits them, in case the IEEE style wants them.

| # | Status | Notes and source |
|---|--------|------------------|
| [1] Uchendu, Le, Shu, Lee, EMNLP 2020, pp. 8384–8395 | OK | https://aclanthology.org/2020.emnlp-main.673/ |
| [2] Uchendu, Ma, Le, Zhang, Lee, TURINGBENCH, Findings of EMNLP 2021 | OK | pp. 2001–2016. https://aclanthology.org/2021.findings-emnlp.172/ |
| [3] Sun, Yin, Xu, Kolter, Liu, "Idiosyncrasies in LLMs," ICML 2025 | OK, but see novelty note | PMLR 267, pp. 57854–57885. https://proceedings.mlr.press/v267/sun25z.html . Note: this paper already does five-way attribution of ChatGPT/Claude/Grok/Gemini/DeepSeek and already reports that the fingerprint survives translation (English→Chinese by GPT-4o-mini, accuracy stays 91–93%). The draft cites it only for "embedding-based classifiers ... in English"; Related Work and RQ5 must acknowledge the translation result. |
| [4] Joshi, Santy, Budhiraja, Bali, Choudhury, ACL 2020, pp. 6282–6293 | OK | https://aclanthology.org/2020.acl-main.560/ |
| [5] Nivre et al., UD v2, LREC 2020, pp. 4034–4043 | OK | https://aclanthology.org/2020.lrec-1.497/ |
| [6] Mitchell, Lee, Khazatsky, Manning, Finn, DetectGPT, ICML 2023 | OK | PMLR 202, pp. 24950–24962. https://proceedings.mlr.press/v202/mitchell23a.html |
| [7] Bao, Zhao, Teng, Yang, Zhang, Fast-DetectGPT, ICLR 2024 | OK | https://iclr.cc/virtual/2024/poster/19201 |
| [8] Hans et al., Binoculars, ICML 2024 | OK | PMLR 235. https://proceedings.mlr.press/v235/hans24a.html |
| [9] Verma, Fleisig, Tomlin, Klein, Ghostbuster, NAACL 2024 | OK | pp. 1702–1717. https://aclanthology.org/2024.naacl-long.95/ |
| [10] Macko et al., MULTITuDE, EMNLP 2023 | OK | https://aclanthology.org/2023.emnlp-main.616/ |
| [11] Wang et al., M4, EACL 2024 | OK | pp. 1369–1407; Best Resource Paper. Typo in draft: "Y. Wanget al." needs a space. https://aclanthology.org/2024.eacl-long.83/ |
| [12] Wang et al., SemEval-2024 Task 8 | OK | https://aclanthology.org/2024.semeval-1.279/ . Note: only Subtask A had a multilingual track; Subtask B (which generator) was English-only. That supports the draft's position, and is worth saying explicitly. |
| [13] Wu, Yang, Zhan, Yuan, Chao, Wong, survey, Computational Linguistics 51(1), 2025 | OK, weak use | pp. 275–338, https://aclanthology.org/2025.cl-1.8/ . It is a survey; the draft uses it as the evidence that "detection degrades outside English." Cite a primary result instead (MULTITuDE [10] itself, or GenAI Content Detection Task 1 at COLING 2025, see section 2(d)). |
| [14] Pasquini, Kornaropoulos, Ateniese, LLMmap, USENIX Security 2025 | OK | https://www.usenix.org/conference/usenixsecurity25/presentation/pasquini |
| [15] Stamatatos, JASIST 60(3), pp. 538–556, 2009 | OK | https://onlinelibrary.wiley.com/doi/abs/10.1002/asi.21001 |
| [16] Kumarage et al., arXiv:2303.03697, 2023 | Exists; arXiv only; misused | dblp lists it only as CoRR (https://dblp.org/rec/journals/corr/abs-2303-03697.html), so citing the preprint is correct. But it is a human-vs-AI *detection* paper on tweets, and the sentence it supports ("stylometric detection of AI text has so far been applied to English") is false (section 2(c)). The peer-reviewed paper that actually does stylometric *attribution* among LLMs in English is Kumarage & Liu, "Neural Authorship Attribution: Stylometric Analysis on Large Language Models," IEEE CyberC 2023, pp. 51–54, DOI 10.1109/CyberC58899.2023.00019, https://ieeexplore.ieee.org/document/10438784/ — cite that one. |
| [17] Padmakumar & He, ICLR 2024 | OK | https://proceedings.iclr.cc/paper_files/paper/2024/hash/02dec8877fb7c6aa9a79f81661baca7c-Abstract-Conference.html |
| [18] Doshi & Hauser, Science Advances 10(28), 2024 | OK | article eadn5290. https://www.science.org/doi/10.1126/sciadv.adn5290 |
| [19] Liang et al., ICML 2024 | OK | PMLR 235, pp. 29575–29620. https://proceedings.mlr.press/v235/liang24b.html |
| [20] Panickssery, Bowman, Feng, NeurIPS 2024 | OK | https://proceedings.neurips.cc/paper_files/paper/2024/hash/7f1f0218e45f5414c79c0679633e47bc-Abstract-Conference.html |
| [21] Erlikhman et al., "Self-attribution is not self-recognition," under review, 2026 | Unverifiable (self-citation) | No public record. Acceptable as "under review" only if the venue allows it; if IEEE BigData reviewing is anonymised, this citation identifies the authors and the wording should be "a companion study (anonymised)". |
| [22] Qi, Zhang, Zhang, Bolton, Manning, Stanza, ACL 2020 demos | OK | https://aclanthology.org/2020.acl-demos.14/ |
| [23] Covington & McFall, J. Quant. Linguist. 17(2), pp. 94–100, 2010 | OK | https://www.tandfonline.com/doi/abs/10.1080/09296171003643098 |
| [24] Goh & Barabási, EPL 81(4), 2008 | OK, add article no. | EPL uses article numbers: "vol. 81, no. 4, 48002, 2008". https://iopscience.iop.org/article/10.1209/0295-5075/81/48002 |

Nothing is fabricated or misattributed; no venue or year is wrong; no arXiv preprint is cited where a peer-reviewed version exists ([16] has none). Problems are the misuse of [16], the weak use of [13], the under-description of [3], and the self-citation [21].

## 2. Novelty claims against the 2023–2026 literature

### (a) "No prior study performs passive, interpretable model attribution across a resource gradient" — needs narrowing

Two direct counter-examples on multilingual *model* attribution (not just detection):

1. L. La Cava, D. Macko, R. Moro, I. Srba, A. Tagarelli, "Authorship Attribution in Multilingual Machine-Generated Texts," *Proc. ACL 2026* (Long Papers), pp. 45136–45152, San Diego, July 2026. arXiv:2508.01656 (Aug 2025). https://aclanthology.org/2026.acl-long.2091/ , https://arxiv.org/abs/2508.01656 . Passive attribution among 7 LLMs + human across 18 languages (incl. Chinese, Russian, Arabic, Spanish), 8 methods (Fast-DetectGPT, Binoculars, a 9-feature statistical ensemble, RoBERTa, XLM-R, Qwen3-4B, mdok, OTBDetector), with train-on-one-language / test-on-all transfer. It does *not* use interpretable linguistic features and does *not* order languages by resource level.
2. M. Greco, A. Shetty, A. Tagarelli, J. H. Lau, "MultiGhostBench: A Multilingual Benchmark for Long-Form LLM-Generated Text Attribution under Distribution Shifts," arXiv:2609.02379, 2 Sept 2026. https://arxiv.org/abs/2609.02379 . Five current LLMs (Gemini pro/flash, DeepSeek-v3.2, Qwen3-235B, GPT-OSS), six languages (it, es, de, en, zh, ru), metric-, model- and fingerprint-based attributors, cross-language transfer; finds statistical/fingerprint methods are "more language-dependent" than transformers. Not interpretable; "low-resource" there means few training books, not language resource level.

Also relevant: Sun et al. [3] already attribute the same five model families and show the fingerprint survives translation into Chinese (91–93%); Rao, Mohamed, Liu, Liu, "Two Birds with One Stone: Multi-Task Detection and Attribution of LLM-Generated Text," SecureComm 2025, arXiv:2508.14190, reports cross-lingual attribution patterns (transfer among Romance languages).

Rewrite: "The attribution literature is almost entirely English [1], [2], [3]" (Intro) is now false; say "mostly English; the two multilingual studies [La Cava; MultiGhostBench] use opaque fine-tuned or probability-based classifiers." Narrow the Related Work claim to: "To our knowledge, no prior study attributes text to its source model with features that have the same definition in every language, holds content fixed across languages, or tests attribution against a language-resource gradient." Drop "passive" as the distinguishing word (both counter-examples are passive).

### (b) "Whether models converge on each other where training data is thin has not been tested" — holds, with one nearby result to cite

No paper found that measures inter-model stylistic distance as a function of language resource level. Closest work, all of which should be cited so the claim reads as informed rather than unaware:

- J. Milička, A. Marklová, V. Cvrček, "Benchmark of stylistic variation in LLM-generated texts," arXiv:2509.10179, Sept 2025. https://arxiv.org/abs/2509.10179 . 16 frontier models, English and Czech, Biber multidimensional analysis; compares models with humans in a high- and a lower-resource language, but not models with each other across a gradient.
- A. Rastogi et al., "What if I ask in alia lingua? Measuring Functional Similarity Across Languages," MRL 2025 (EMNLP workshop). https://aclanthology.org/2025.mrl-main.33/ . Output similarity across 20 languages; finds a model is more similar to itself across languages than to other models in the same language, which is the content-level analogue of the draft's RQ3 result and is worth one sentence.
- Z. Sourati et al., "The Shrinking Landscape of Linguistic Diversity in the Age of Large Language Models," *Nature Human Behaviour*, 2026 (arXiv:2502.11266). https://arxiv.org/abs/2502.11266 . Homogenisation of human writing by LLMs (21–50% variance reduction); English, LLM vs human. Stronger and more recent than [17]/[18] for the Discussion.

Narrow to: "Homogenisation has been measured between people and models [17], [18], [Sourati] and, for two languages, between models and human registers [Milička]; whether models converge on *each other* as training data thins has not been tested."

### (c) "Stylometric detection of AI text has so far been applied to English [16]" — false, must be rewritten

Counter-examples, all with interpretable, language-specific feature sets:

- W. Zaitsu, M. Jin, "Distinguishing ChatGPT(-3.5, -4)-generated and human-written papers through Japanese stylometric analysis," *PLoS ONE* 18(8): e0288453, 2023. https://doi.org/10.1371/journal.pone.0288453
- W. Zaitsu, M. Jin, S. Ishihara, S. Tsuge, M. Inaba, "Stylometry can reveal artificial intelligence authorship, but humans struggle: A comparison of human and seven large language models in Japanese," *PLoS ONE* 20(10): e0335369, Oct 2025. https://doi.org/10.1371/journal.pone.0335369 . Function-word unigrams, POS bigrams, phrase patterns; random forest; seven LLMs incl. GPT-4o, o1, Claude 3.5, Gemini.
- M. S. Al-Shaibani, M. Ahmed, "Arabic machine-generated text detection: Stylometric analysis and cross-model evaluation," *Expert Systems with Applications*, 2025 (arXiv:2505.23276). https://www.sciencedirect.com/science/article/abs/pii/S0957417425042599
- Li, Zhang, "Linguistic Differences between AI and Human Comments in Weibo: Detect AI-Generated Text through Stylometric Features," CCL 2025. https://aclanthology.org/2025.ccl-1.64/
- K. Przystalski, J. K. Argasiński, I. Grabska-Gradzińska, J. K. Ochab, "Stylometry recognizes human and LLM-generated texts in short samples," *Expert Systems with Applications* 296: 129001, 2025 (arXiv:2507.00838). https://arxiv.org/abs/2507.00838 . StyloMetrix features (designed for Polish, English, German, Ukrainian, Russian); includes a 7-class multiclass setting, so it is also a small interpretable-attribution counter-example.

Rewrite to: "Stylometric detection has been applied language by language with language-specific feature sets: Japanese [Zaitsu 2023, 2025], Arabic [Al-Shaibani], Chinese [Li & Zhang], Polish and English [Przystalski]. None uses one feature set with the same definition across scripts, and none attributes among current frontier models across languages." Replace [16] with Kumarage & Liu (CyberC 2023) for the English attribution point.

### (d) "Multilingual detection degrades outside English" — supported; cite primary sources

- MULTITuDE [10]: English-only fine-tuning is "a particularly inappropriate choice" for generalising to other languages. https://aclanthology.org/2023.emnlp-main.616/
- Y. Wang et al., "GenAI Content Detection Task 1: English and Multilingual Machine-Generated Text Detection: AI vs. Human," GenAIDetect @ COLING 2025. https://aclanthology.org/2025.genaidetect-1.27/ . Detectors fine-tuned on English: F1 0.93 on English, 0.69 on non-English.
- D. Macko, J. Kopal, "CEAID: Benchmark of Multilingual Machine-Generated Text Detection Methods for Central European Languages," arXiv:2509.26051, 2025. https://arxiv.org/abs/2509.26051
- D. Macko et al., "Authorship Obfuscation in Multilingual Machine-Generated Text Detection," Findings of EMNLP 2024, pp. 6348–6368. https://aclanthology.org/2024.findings-emnlp.369/

Keep the claim; swap the survey [13] for one of these as the evidence.

### Note on the SemEval-2024 Task 8 premise
The brief suggested Subtask B (generator identification) was multilingual. It was not: Subtask A had a multilingual track; Subtask B was English-only (six generators), as was the multi-way task in M4GT-Bench (ACL 2024). The draft can use this to say that shared-task generator identification has so far been English-only.

## 3. Additional references a BigData reviewer would expect (five, plus two optional)

1. U. Sapkota, S. Bethard, M. Montes, T. Solorio, "Not All Character N-grams Are Created Equal: A Study in Authorship Attribution," NAACL-HLT 2015. https://aclanthology.org/N15-1010/ — the standard citation for why character n-grams (and punctuation/affixes) carry authorship; justifies the draft's character-bigram entropy and punctuation features and its decision not to use raw n-grams.
2. B. Murauer, G. Specht, "DT-grams: Structured Dependency Grammar Stylometry for Cross-Language Authorship Attribution," GvDB 2021, CEUR-WS Vol-3075 (arXiv:2106.05677). https://arxiv.org/abs/2106.05677 — prior use of Universal Dependencies for language-independent stylometry; the draft's "features defined on UD so they mean the same thing in every language" has a precedent here.
3. L. La Cava, D. Macko, R. Moro, I. Srba, A. Tagarelli, "Authorship Attribution in Multilingual Machine-Generated Texts," ACL 2026. https://aclanthology.org/2026.acl-long.2091/ — the closest prior work; omitting it would be the first thing a reviewer notices.
4. T. Kumarage, H. Liu, "Neural Authorship Attribution: Stylometric Analysis on Large Language Models," IEEE CyberC 2023, pp. 51–54. https://ieeexplore.ieee.org/document/10438784/ — the English stylometric-attribution baseline the draft is extending; also an IEEE venue.
5. B. Huang, C. Chen, K. Shu, "Authorship Attribution in the Era of LLMs: Problems, Methodologies, and Challenges," ACM SIGKDD Explorations 26(2), pp. 21–43, 2024. https://dl.acm.org/doi/10.1145/3715073.3715076 — the survey that defines "LLM-generated text attribution" as a problem class; a data-mining audience will know it.

Optional: Y. Wang et al., "M4GT-Bench," ACL 2024 (https://aclanthology.org/2024.acl-long.218/), for the English-only multi-way generator task; M. Greco et al., "MultiGhostBench," arXiv:2609.02379, 2026, if the authors want to show awareness of work from this month.

## 4. Edits implied for the draft

- Intro line 53–55: replace "almost entirely English" with "mostly English", cite La Cava et al. and MultiGhostBench, and characterise them as opaque.
- Related Work, "Model attribution": add one sentence on [3]'s translation result; add La Cava et al.; rewrite the "so far applied to English" sentence per 2(c); narrow the "no prior study" sentence per 2(a).
- Related Work, "Homogenization": cite Milička et al. and Sourati et al.; keep the convergence claim in its narrowed form.
- RQ5 contribution bullet and §4.5: state that [3] showed embedding-based fingerprints survive LLM translation into Chinese, and that the new result is the mechanism (which interpretable features survive) across six target languages and two translators, one of them a commercial MT system.
- Reference list: fix "Wanget al." in [11]; add article number to [24]; consider adding page numbers to [2], [6], [8], [9], [19].
