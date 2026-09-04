# URTC 2026 poster submission (deadline 4 Sep 2026, 11:59 pm EST)

**Track:** Technology of Computation (secondary: Technology of Humanity)

**Title:** Do LLM Fingerprints Survive Outside English? Interpretable Attribution of Five Frontier Models Across Seven Languages

**Authors:** Adrian Erlikhman (LACES), Michael Tarekegn (LACES), Philo Juang (UCLA)

**File:** `LangLLM_poster_URTC2026.pdf` (48 × 36 in)

## Abstract

Tools that detect AI-written text are built and tested in English, yet the need to attribute text to a specific model, for disinformation tracing, academic integrity and moderation, is largely non-English. Prior attribution work is English-only and relies on opaque embeddings. We ask whether a model's stylistic fingerprint survives outside English, whether it fades as a language's training-data share falls, whether it survives translation, and whether the models themselves can read it.

We collected 840 persuasive essays from GPT-5.5, Gemini 3.5 Flash, Claude Opus 4.7, Grok 4.3 and DeepSeek V4 Pro: 12 essay prompts × 7 languages (English, Spanish, Chinese, Russian, Japanese, Turkish, Hindi, in decreasing resource order) × 2 generations. Each prompt fixes a topic, a stance and three supporting points; a non-subject model wrote a native version of each prompt in every language, verified by a second model, so content is held constant and only style varies. Every text was parsed with Stanza on Universal Dependencies and described by 21 interpretable features (lexical diversity, sentence rhythm, dependency depth, paragraphing, punctuation mapped across scripts, character entropy) that mean the same thing in every language. All analyses were pre-specified.

Results. (1) A logistic-regression classifier attributes five ways at 59 to 72% in every language (chance 20%, leave-one-prompt-out). (2) Accuracy does not fall along the resource gradient (cell-level GLM, β = −0.04 log-odds per rank, p = 0.36); Japanese matches English and Hindi exceeds Spanish. (3) Language explains most feature variance (mean partial η² 0.54 vs 0.15 for model), yet the fingerprint is largely language-invariant: after within-language standardisation, a classifier trained on any language beats chance on every other (42 of 42 pairs, mean 0.49). (4) Models nonetheless converge stylistically as resources fall: separation between model centroids shrinks monotonically from English to Hindi (ρ = −0.96), driven by Grok's terse English register disappearing. (5) Translation by Google Translate or a free open model leaves attribution at 0.57 to 0.70, and an English-trained classifier reads the translations at 0.66, because structural features survive translation (paragraph count ρ = 1.00) while lexical ones are rewritten. (6) As a baseline, each model was asked directly which of the five wrote each text: all five sit at or near chance in all seven languages (20.3 to 25.4%), each defaulting to one fixed answer.

Interpretable features thus beat every LLM judge by 35 to 50 points in every language; the fingerprint survives low-resource languages and translation; and the written register of low-resource languages is flattening toward one shared style. Code, prompts, all 840 responses and 1,440 translations are released.
