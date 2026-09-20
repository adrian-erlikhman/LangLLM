from pathlib import Path
p = Path(__file__).with_name("main.tex"); s = p.read_text(encoding="utf-8")
R = [
(r" Eight features depend on the parser or sentence splitter; the other thirteen need only tokenization.", ""),
(r" The pre-specified criterion (negative coefficient, $p < 0.05$) is not met.", ""),
(r"; the other four models are as far apart in Hindi as in English, and silhouettes near zero mean no cluster structure in the full feature space in any language.", r"; the other four models are as far apart in Hindi as in English."),
(r", including Latin-script Turkish, so the loss is vocabulary rather than script; the adapted counterpart was not run on translations.", r", including Latin-script Turkish, so the loss is vocabulary rather than script."),
(r"Across seven languages, \NFeatures{} interpretable features with one computational definition in every language attribute persuasive essays to one of five frontier LLMs at \LRmin{}--\LRmax{} accuracy, \GapNGmin{}--\GapNGmax{} points below character $n$-grams within a language and \TransferOff{} against \NGFairOff{} when transferred across languages under the same unlabelled adaptation.",
 r"Across seven languages, \NFeatures{} interpretable features with one definition in every language attribute persuasive essays to one of five frontier LLMs at \LRmin{}--\LRmax{} accuracy, \GapNGmin{}--\GapNGmax{} points below character $n$-grams within a language and \TransferOff{} against \NGFairOff{} across languages under the same unlabelled adaptation."),
(r"For human authors, character $n$-grams are the single most successful feature~\cite{sapkota2015ngrams}, masking all but the most frequent words isolates a structural signal~\cite{stamatatos2017distortion}, and UD-derived syntactic features attribute human authors in several languages~\cite{gorman2022ud}.",
 r"For human authors, character $n$-grams are the most successful single feature~\cite{sapkota2015ngrams}, masking all but the most frequent words isolates a structural signal~\cite{stamatatos2017distortion}, and UD-derived syntactic features attribute authors in several languages~\cite{gorman2022ud}."),
(r"In the two-way ANOVA, language explains far more feature variance than model (mean partial $\eta^2$ \EtaLang{} against \EtaModel{}; interaction \EtaInter{}; prompt \EtaPrompt{}) and dominates every measure tied to morphology or vocabulary, while model effects are largest for \EtaModelTopFive{} and smallest for subordination, question rate and dependency depth ($\leq \EtaModelSmallMax{}$): the models differ in lexical variety, punctuation and paragraphing, and hardly at all in clause structure.",
 r"In the two-way ANOVA, language explains far more feature variance than model (mean partial $\eta^2$ \EtaLang{} against \EtaModel{}; interaction \EtaInter{}; prompt \EtaPrompt{}), while model effects are largest for \EtaModelTopFive{} and smallest for subordination, question rate and dependency depth ($\leq \EtaModelSmallMax{}$): the models differ in lexical variety, punctuation and paragraphing, hardly at all in clause structure."),
]
for a, b in R:
    assert a in s, "NOT FOUND: " + a[:70]
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8"); print("trim10 applied")
