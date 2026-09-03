# Related work — framing and the gap

> Working notes. Every citation below must be re-verified against the actual paper before
> it goes in a manuscript (titles/venues from memory; check year, authors, findings).

## 1. AI-text *detection* is mature and weakens outside English

- Zero-shot detectors: DetectGPT (Mitchell et al., ICML 2023); Binoculars (Hans et al.,
  ICML 2024); Fast-DetectGPT (Bao et al., ICLR 2024).
- Supervised / stylometric detectors: Ghostbuster (Verma et al., NAACL 2024); Kumarage
  et al. 2023 (stylometry for AI text on Twitter timelines); StyloAI (Opara, 2024).
- Multilingual benchmarks showing degradation off-English: MULTITuDE (Macko et al.,
  EMNLP 2023); M4 / M4GT-Bench (Wang et al., EACL 2024 / ACL 2024); SemEval-2024 Task 8.
- Survey: "A Survey on LLM-Generated Text Detection" (Wu et al., 2023/2025, Computational
  Linguistics).

Take-away: the *human vs machine* question has been asked in many languages; the answer is
that performance drops off English, but the *which machine* question has not travelled.

## 2. *Attribution* to a specific model is mostly English and black-box

- TuringBench (Uchendu et al., EMNLP Findings 2021) — first multi-generator attribution
  benchmark; neural-only, English.
- "Authorship attribution for neural text generation" (Uchendu et al., EMNLP 2020).
- LLMmap (Pasquini et al., 2024) — active fingerprinting via probe prompts, not passive
  stylometry.
- "Idiosyncrasies in Large Language Models" (Sun et al., 2025) — embedding-based
  classifiers separate ChatGPT/Claude/Grok/Gemini/DeepSeek outputs with high accuracy;
  English; opaque features.
- Model-attribution shared tasks (e.g. GenAI Content Detection, COLING 2025) — mostly
  English, fine-tuned transformers.

Take-away: attribution works in English with embeddings. Nobody has (a) used interpretable
features, (b) measured it across a resource gradient, or (c) separated model style from
language style.

## 3. Cross-lingual style and UD-based stylometry

- Universal Dependencies (Nivre et al., 2016/2020) makes syntactic features comparable
  across languages; Stanza (Qi et al., ACL 2020) provides the parsers.
- Cross-lingual authorship attribution with UD/syntactic features (e.g. work on
  language-independent stylometry) — establishes that syntactic profiles transfer.
- MATTR (Covington & McFall, 2010); burstiness (Goh & Barabási, 2008).

## 4. Homogenisation / register flattening

- Padmakumar & He (ICLR 2024): writing with LLMs reduces content diversity.
- Doshi & Hauser (Science Advances, 2024): generative AI raises individual creativity but
  reduces collective diversity.
- Liang et al. (2024): monitoring AI-modified content at scale — rising LLM-style markers in
  scientific and review text.
- Work on LLM "default register"/AI-isms (e.g. "delve" studies) — mostly English.

Take-away: convergence has been shown *within* English between human and LLM text. Whether
*models converge on each other* in low-resource languages is untested — this is RQ4.

## The gap, in one sentence

No study measures model attribution with interpretable, language-comparable features across
a resource gradient, decomposes feature variance into model vs language vs interaction, or
tests whether models collapse to one style where training data is thin.
