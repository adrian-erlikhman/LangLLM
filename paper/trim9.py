from pathlib import Path
p = Path(__file__).with_name("main.tex"); s = p.read_text(encoding="utf-8")
R = [
(r"(v) The transfer and translation tests share the same \NPrompts{} prompts across languages, and two generations per cell give intervals of about $\pm$\ClusterCIhalfwidth{} points. (vi) Prompt fidelity was checked by a model, not by native speakers.",
 r"(v) The transfer and translation tests share the same \NPrompts{} prompts across languages, two generations per cell give intervals of about $\pm$\ClusterCIhalfwidth{} points, and prompt fidelity was checked by a model, not by native speakers."),
(r"(vii) All five subjects are closed APIs served in September 2026; open-weight models, adversarial rewriting and a fine-tuned multilingual encoder baseline~\cite{greco2026multighost} were not tested. (viii) Judges ran without extended reasoning.",
 r"(vi) All five subjects are closed APIs served in September 2026; open-weight models, adversarial rewriting and a fine-tuned multilingual encoder baseline~\cite{greco2026multighost} were not tested, and judges ran without extended reasoning."),
(r" Future work: other genres, human-verified prompts, cross-language leave-one-prompt-out transfer, adapted $n$-grams on translations and a multilingual encoder baseline.",
 r" Future work: other genres, human-verified prompts, adapted $n$-grams on translations and a multilingual encoder baseline."),
(r"were queried through OpenRouter in September 2026, with the served model identifier logged for every response (identifiers are listed in the repository).",
 r"were queried through OpenRouter in September 2026, with the served model identifier logged for every response."),
(r"The choice of representation depends on where the classifier will be used: within one language, with labelled data in that language, character $n$-grams are the better tool by \GapNGmin{}--\GapNGmax{} points; across scripts under equal adaptation the features transfer better, and where script and vocabulary are shared, $n$-grams keep their edge.",
 r"The choice of representation depends on where the classifier will be used: within one language, with labelled data, character $n$-grams are the better tool by \GapNGmin{}--\GapNGmax{} points; across scripts under equal adaptation the features transfer better, and where script and vocabulary are shared, $n$-grams keep their edge."),
]
for a, b in R:
    assert a in s, "NOT FOUND: " + a[:70]
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8"); print("trim9 applied")
