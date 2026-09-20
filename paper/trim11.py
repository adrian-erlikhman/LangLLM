from pathlib import Path
p = Path(__file__).with_name("main.tex"); s = p.read_text(encoding="utf-8")
R = [
(r" and the models themselves cannot do the task, as Bai et al.~\cite{bai2025selfrecognition} found in English.", r" and the models themselves cannot do the task."),
(r"; translation combined with a paraphrase attack is untested, although paraphrase attacks leave a model's style largely intact in English~\cite{riverasoto2026attacks}.", r"; translation combined with a paraphrase attack~\cite{riverasoto2026attacks} is untested."),
(r" In plain terms, \NFeatures{} inspectable numbers identify the author about three times as often as guessing, in Hindi as in English.", r" In plain terms, \NFeatures{} inspectable numbers identify the author about three times as often as guessing."),
]
for a, b in R:
    assert a in s, "NOT FOUND: " + a[:70]
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8"); print("trim11 applied")
