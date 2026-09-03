# LangLLM

**Do LLM stylistic fingerprints survive outside English?** Interpretable stylometric
attribution of five frontier models across a seven-language resource gradient.

| | |
|---|---|
| Models | GPT-5.5 · Gemini 3.5 Flash · Claude Opus 4.7 · Grok 4.3 · DeepSeek V4 Pro (one OpenRouter key, served model strings logged) |
| Languages | English → Spanish → Chinese → Russian → Japanese → Turkish → Hindi (decreasing training-data share) |
| Design | 5 models × 12 prompts × 7 languages × 2 generations = **840 responses**; content held fixed, only style free |
| Features | 21 interpretable features defined on Universal Dependencies (Stanza), identical meaning in every language |

## Research questions

| | Question | Test |
|---|---|---|
| **RQ1** | Can the five models be told apart by interpretable features *within* each language? | Leave-one-prompt-out 5-way classification per language; logistic regression (interpretable) + random forest (ceiling); chance = 0.20 |
| **RQ2** | Does attribution accuracy fall with the language's training-data share? | Spearman ρ of accuracy vs resource rank (n = 7) + cell-level binomial GLM `correct ~ rank` with prompt-clustered SEs (n = 840) |
| **RQ3** | Is a model's style language-invariant or per-language? | Per-feature two-way ANOVA (model × language, prompt blocked) → partial η²; cross-lingual transfer matrix of a within-language z-scored classifier |
| **RQ4** | Do models converge on one generic style in low-resource languages? | Within-language model separation (mean centroid distance, silhouette, between/within trace) with bootstrap CIs, vs rank |

The full pre-specified analysis plan, including decision rules for each RQ, is in
[docs/analysis_plan.md](docs/analysis_plan.md). Literature framing is in
[docs/related_work.md](docs/related_work.md).

## Pipeline

```
prompts/schemas.json ──(1) Llama writes native prompts──▶ prompts/native/{lang}.json
                                                                │
                              (2) 5 subject models via OpenRouter ▼
                                                        data/raw/{model}.jsonl
                                                                │
                                (3) language ID + length + refusal ▼
                                                        data/validation.csv
                                                                │
                                        (4) Stanza UD → 21 features ▼
                                                  data/features/features.csv
                                                                │
                                              (5) RQ1–RQ4 ▼        (6) figures ▼
                                              results/*.csv|json   results/figures/*.png
```

### Setup

```bash
pip install -r requirements.txt
cp .env.example .env            # put your OpenRouter key in it
python -c "import stanza; [stanza.download(l, model_dir='stanza_resources', processors='tokenize,pos,lemma,depparse') for l in 'en es zh ru ja tr hi'.split()]"
python -m pytest -q             # unit tests (feature helpers, validation heuristics, schema balance)
```

### Run

```bash
python -m langllm.prompts                 # 1. 84 native prompts (Llama 4 Maverick; no translation)
python -m langllm.review                  # 1b. Qwen checks all 84 against their schema → prompts/native/REVIEW.md
python -m langllm.collect --dry-run       # 2. count cells; then drop --dry-run (resumable, ~$5–10 total)
python -m langllm.collect
python -m langllm.validate                # 3. langid / length / refusal → results/validation_summary.csv
python -m langllm.features                # 4. Stanza parse → data/features/features.csv
python -m langllm.analysis                # 5. RQ1–RQ4 → results/
python -m langllm.figures                 # 6. results/figures/F1…F7
```

Everything is resumable and idempotent: `collect` skips cells already on disk, `prompts`
skips languages already written, and the analysis is fully re-derived from `features.csv`.

### Smoke test without spending anything

```bash
python -m langllm.synthetic                                     # planted effects: model signal decays with rank
python -m langllm.analysis --features data/features/synthetic.csv
python -m langllm.figures  --features data/features/synthetic.csv
```

## Protocol details

**Prompting.** Each of the 12 English schemas fixes a topic, a stance, three sub-claims,
"prose only" and a reading-level tier (the FK tier is a *prompt control*, never a measured
feature, because Flesch–Kincaid is English-only). For every language a non-subject model
(Llama 4 Maverick) writes a native prompt *from the schema*, not by translation. All seven
versions of a prompt share topic, stance and sub-claims, so content is held fixed and only
style is free. Every prompt in every language is then reviewed by a third non-subject model
(Qwen 3.7 Plus) that extracts topic, stance and sub-claims blind and matches them to the
schema; mismatches are flagged for repair. Human sign-off is optional. English is produced by
the same route so every language shares one protocol.

**Generation.** Single user turn, no system prompt, temperature 0.7, fixed seeds per
generation index, reasoning traces excluded so every response is prose only. The *served*
model string, provider, finish reason and token usage are stored with each response.

**Validation.** Language ID (lingua, restricted to the seven languages), a word-equivalent
length window (150–900; Chinese/Japanese converted from characters), a refusal heuristic per
language, and a count of heading/bullet lines. Wrong-language, refusal and error rates are
reported per model × language in `results/validation_summary.csv` and are themselves a
finding (they bound the reliability of attribution where it matters).

**Features** (all per response, from Stanza `tokenize,pos,lemma,depparse`):

| Group | Feature | Definition |
|---|---|---|
| lexical | `mattr` | moving-average TTR, window 50 |
| | `hapax_rate` | once-only types / tokens |
| | `mean_token_len` | characters per non-punctuation token |
| | `zipf_slope` | OLS slope of log freq on log rank |
| syntactic | `sent_len_mean`, `sent_len_sd` | tokens per sentence |
| | `burstiness` | (σ−μ)/(σ+μ) of sentence lengths |
| | `dep_depth` | mean max dependency depth per sentence |
| | `subord_rate` | `acl advcl ccomp xcomp csubj` per sentence |
| | `func_word_ratio` | `ADP AUX CCONJ DET PART PRON SCONJ` / tokens |
| | `first_person_rate` | `Person=1` tokens per 1k (lexical fallback for zh/ja, which lack the feature) |
| structure | `para_count`, `para_len_mean` | newline-delimited paragraphs; tokens per paragraph |
| | `question_rate` | `? ？` per sentence |
| | `connective_rate` | `cc`, `mark`, sentence-initial ADV/CCONJ/SCONJ per 1k |
| punctuation | `comma_per_1k` … `semicolon_per_1k` | `, ， 、` · `: ：` · `— – ― --` · `; ；` per 1k tokens |
| character | `bigram_entropy` | Shannon entropy of character bigrams, bits |
| | `digit_rate` | Unicode `Nd` characters per 1k non-space characters |

Dropped as English-only: Flesch, Fog, hedges, passive rate, contractions.

**Chinese/Japanese sentence splitting.** Stanza does not split reliably on `。！？`, so those
two languages are pre-split on terminal punctuation and Stanza's splitter is disabled.

## Repository layout

```
config.yaml            models, languages + resource rank, tiers, generation/validation/analysis knobs
prompts/schemas.json   the 12 English schemas (6 for / 6 against; 4 per reading tier)
prompts/native/        one JSON per language from the writer, review_{lang}.json from the reviewer, REVIEW.md summary
langllm/               prompts → review → collect → validate → features → analysis → figures (+ synthetic, openrouter)
tests/                 pytest: helpers, validation heuristics, schema balance, one Stanza round-trip
data/                  raw responses (gitignored), validation.csv, features.csv
results/               per-RQ tables + figures
docs/                  analysis plan, related work
```

## Why it matters

Provenance tools are built and tested in English, but the demand for attribution —
disinformation, academic integrity, moderation — is mostly non-English. If fingerprints fade
with resource level, attribution fails where it matters most. If the models converge on one
style in low-resource languages, LLM use is flattening the written register of the languages
with the least data. Either result is actionable.
