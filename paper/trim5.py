from pathlib import Path
p = Path(__file__).with_name("main.tex"); s = p.read_text(encoding="utf-8")
R = [
(r"\textbf{Dual use.} Nothing in the features or classifier is specific to machine-generated text, and human authorship attribution already uses UD-derived features~\cite{gorman2022ud}, so releasing the code makes public a method rather than a new capability; the translation result is a caution for pseudonymous writers, since translation removes vocabulary and keeps structure. We release model-generated text and results only.",
 r"\textbf{Dual use.} Nothing in the features is specific to machine-generated text, and human authorship attribution already uses UD-derived features~\cite{gorman2022ud}, so the release makes public a method rather than a new capability; the translation result is a caution for pseudonymous writers. We release model-generated text and results only."),
(r"Claude Code (Anthropic) assisted in writing the data-collection, feature-extraction and analysis pipeline behind Sections~3 and 4, and Claude assisted in drafting and editing text throughout the paper. The authors reviewed all AI-assisted code and text and are responsible for the methods, results and conclusions. Code, prompts, responses, translations, judge calls, features, the analysis plan and result tables: \url{https://github.com/adrian-erlikhman/LangLLM}.",
 r"Claude Code (Anthropic) assisted in writing the data-collection, feature-extraction and analysis pipeline, and Claude assisted in drafting and editing text. The authors reviewed all AI-assisted code and text and are responsible for the methods, results and conclusions. Code, prompts, responses, translations, judge calls, features, the analysis plan and result tables: \url{https://github.com/adrian-erlikhman/LangLLM}."),
(r"(vii) All five subjects are closed APIs served in September 2026; open-weight models, newer versions, adversarial rewriting and a fine-tuned multilingual encoder baseline, which transfers across languages~\cite{greco2026multighost}, were not tested.",
 r"(vii) All five subjects are closed APIs served in September 2026; open-weight models, adversarial rewriting and a fine-tuned multilingual encoder baseline~\cite{greco2026multighost} were not tested."),
(r"For this genre and model snapshot, machine translation does not remove the signal, and the surviving features can be named; translation combined with a changed system prompt, temperature or a paraphrase attack is untested, although paraphrase attacks leave a model's style largely intact in English~\cite{riverasoto2026attacks}.",
 r"For this genre and model snapshot, machine translation does not remove the signal, and the surviving features can be named; translation combined with a paraphrase attack is untested, although paraphrase attacks leave a model's style largely intact in English~\cite{riverasoto2026attacks}."),
]
for a, b in R:
    assert a in s, "NOT FOUND: " + a[:70]
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8"); print("trim5 applied")
