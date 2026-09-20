from pathlib import Path
p = Path(__file__).with_name("main.tex"); s = p.read_text(encoding="utf-8")
R = [
(r" Without adaptation, $n$-grams transfer at \NGTransferOff{} with \NGTransferConst{} constant-prediction cells.", r" Without adaptation, $n$-grams transfer at \NGTransferOff{}."),
(r"; whether models converge on each other as training data thins has not been tested, and the one multilingual observation points the other way~\cite{lacava2026multilingual}.", r"; whether models converge on each other as training data thins has not been tested."),
(r", and both translators keep paragraph boundaries, so those features survive translation partly by construction.", r"; both translators keep paragraph boundaries."),
(r"Per-language McNemar tests on about 120 paired predictions are underpowered for gaps near ten points (Spanish: \GapNGes{} points, Holm \GapNGesHolmP{}); the advantage is Holm-significant in \NGsigLangs{} and in the same direction everywhere else.",
 r"Per-language McNemar tests on about 120 paired predictions are underpowered for gaps near ten points (Spanish: \GapNGes{} points, Holm \GapNGesHolmP{}); the advantage is Holm-significant in \NGsigLangs{} and in the same direction elsewhere."),
]
for a, b in R:
    assert a in s, "NOT FOUND: " + a[:70]
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8"); print("trim12 applied")
