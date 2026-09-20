from pathlib import Path
p = Path(__file__).with_name("main.tex"); s = p.read_text(encoding="utf-8")
R = [
(r" Two pre-registered questions (resource gradient, convergence) return nulls. Code, prompts, texts and every result table are released.", r" Two pre-registered questions (resource gradient, convergence) return nulls."),
(r" In plain terms, \NFeatures{} numbers that a reader can inspect identify the author about three times as often as guessing, in Hindi as in English.", r" In plain terms, \NFeatures{} inspectable numbers identify the author about three times as often as guessing, in Hindi as in English."),
(r"\textbf{Dual use.} Nothing in the features is specific to machine-generated text, and human authorship attribution already uses UD-derived features~\cite{gorman2022ud}, so the release makes public a method rather than a new capability; the translation result is a caution for pseudonymous writers. We release model-generated text and results only.",
 r"\textbf{Dual use.} Nothing in the features is specific to machine-generated text, and human attribution already uses UD-derived features~\cite{gorman2022ud}, so the release makes public a method rather than a new capability; the translation result is a caution for pseudonymous writers. We release model-generated text only."),
(r"A black-box score gives no such reason, and a fine-tuned detector for each language and model version is rarely available outside English.", r"A black-box score gives no such reason, and a fine-tuned detector for each language and model version rarely exists outside English."),
(r"Most of the signal sits in a handful of nameable features that differ by language, led in the pooled ranking by paragraph count and paragraph length, which pass through machine translation almost unchanged, so non-English machine text can be attributed with a classifier whose decisions can be read.",
 r"Most of the signal sits in a handful of nameable features, led in the pooled ranking by paragraph count and length, which pass through machine translation almost unchanged, so non-English machine text can be attributed with a classifier whose decisions can be read."),
]
for a, b in R:
    assert a in s, "NOT FOUND: " + a[:70]
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8"); print("trim8 applied")
