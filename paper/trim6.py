"""Style pass after review/style_match.md (exemplar: Xie, Zhang, Zhang, Liu, IEEE BigData 2024 HSS).
Adds: field-level opener, use-case closer, questions up front, a why-it-matters paragraph naming a
person and a task, a pipeline-walk contribution statement, and 'this means' readings after key
numbers. Pays for every added line with a cut in Related Work and RQ4. Also fixes three bib entries."""
import re
from pathlib import Path
H = Path(__file__).parent
s = (H / "main.tex").read_text(encoding="utf-8")
R = [
# --- abstract: opener + closer
(r"Classifiers that attribute machine-generated text to the model that wrote it are built and evaluated mostly in English, and the cost of an interpretable representation against character $n$-grams has not been measured on content-controlled multilingual data.",
 r"Large language models now write fluently in many languages, but almost everything known about telling their outputs apart comes from English, and the cost of an interpretable representation against character $n$-grams has not been measured on content-controlled multilingual data."),
(r"Model attribution on machine-translated text stays at \TrAllMin{}--\TrAllMax{}, and the five models, asked which model wrote each text, score \JudgeMin{}--\JudgeMax{}.",
 r"Model attribution on machine-translated text stays at \TrAllMin{}--\TrAllMax{}, and the five models, asked which model wrote each text, score \JudgeMin{}--\JudgeMax{}. Non-English machine text can therefore be attributed with a classifier whose decisions can be read, which matters for provenance checks that cannot rely on a fine-tuned black box."),
# --- intro: questions up front, why-it-matters paragraph
(r"Most work on machine-generated text asks whether a text was written by a person or by a model. A second question matters for provenance: \emph{which} model wrote it, which bears on tracing influence campaigns and enforcing provider-specific rules. The model-attribution literature is mostly English~\cite{uchendu2020authorship,sun2025idiosyncrasies}, and the two multilingual studies we know of use fine-tuned or probability-based classifiers whose decisions cannot be read~\cite{lacava2026multilingual,greco2026multighost}.",
 r"""Most work on machine-generated text asks whether a text was written by a person or by a model. A second question matters for provenance: \emph{which} model wrote it. We ask two things: can five frontier models be told apart from a small set of readable features in seven languages, and what does that readability cost against character $n$-grams? The model-attribution literature is mostly English~\cite{uchendu2020authorship,sun2025idiosyncrasies}, and the two multilingual studies we know of use fine-tuned or probability-based classifiers whose decisions cannot be read~\cite{lacava2026multilingual,greco2026multighost}.

The answer matters to people who cannot act on a probability from a model they cannot inspect. A platform moderator tracing a coordinated campaign in Hindi, or a teacher asked which model wrote a Turkish essay, needs a reason that can be stated: this text has the paragraphing and punctuation habits of one model and not another. A black-box score gives no such reason, and a fine-tuned detector for each language and model version is rarely available outside English."""),
# --- contributions as a pipeline walk
(r"Our contributions are (i) a content-controlled corpus of \NCollected{} essays (5 models $\times$ 7 languages $\times$ \NPrompts{} prompts $\times$ 2 generations) with \NTranslations{} machine translations, and a \NFeatures{}-feature representation with one computational definition in every language that reaches \LRmin{}--\LRmax{} five-way accuracy in all seven languages; (ii) two baselines that bracket it: character $n$-grams, \GapNGmin{}--\GapNGmax{} points better within a language and worse across languages under equal unlabelled adaptation (\NGFairOff{} against the features' \TransferOff{}), and the models themselves at \JudgeMin{}--\JudgeMax{}, as Bai et al.~\cite{bai2025selfrecognition} found in English; (iii) an account of which features carry the signal and which survive machine translation. Two pre-registered questions (resource gradient, convergence) return nulls.",
 r"We collect \NCollected{} content-matched essays (5 models $\times$ 7 languages $\times$ \NPrompts{} prompts $\times$ 2 generations) and \NTranslations{} machine translations, describe every text with \NFeatures{} features defined the same way in every language, and find that the features attribute the author in all seven languages at a modest, measured cost against $n$-grams; most of the signal sits in a handful of nameable features that survive machine translation, and the models themselves cannot do the task, as Bai et al.~\cite{bai2025selfrecognition} found in English. Two pre-registered questions (resource gradient, convergence) return nulls. Code, prompts, texts and every result table are released."),
# --- pay for it: related work trims
(r"La Cava et al.\ attribute among seven older LLMs and human text in 18 languages with fine-tuned and probability-based detectors and find generators harder to distinguish in English~\cite{lacava2026multilingual}; MultiGhostBench attributes long-form text to five recent LLMs in six languages and finds that fine-tuned transformers retain generator information across languages while statistical detectors are more language-dependent~\cite{greco2026multighost}.",
 r"La Cava et al.\ attribute among seven older LLMs and human text in 18 languages with fine-tuned and probability-based detectors and find generators harder to distinguish in English~\cite{lacava2026multilingual}; MultiGhostBench attributes long-form text to five recent LLMs in six languages and finds fine-tuned transformers more language-independent than statistical detectors~\cite{greco2026multighost}."),
(r"LLM evaluators favour their own outputs~\cite{panickssery2024self}, and models asked to name the author of a single English text score near chance and default to GPT or Claude~\cite{bai2025selfrecognition}. RQ6 repeats that task in seven languages; a companion study examines self-recognition in English~\cite{erlikhman2026compllm}.",
 r"LLM evaluators favour their own outputs~\cite{panickssery2024self}, and models asked to name the author of a single English text score near chance and default to GPT or Claude~\cite{bai2025selfrecognition}; RQ6 repeats that task in seven languages, and a companion study examines self-recognition in English~\cite{erlikhman2026compllm}."),
# --- 'this means' readings after key numbers
(r"Table~\ref{tab:main} shows five-way accuracy of \LRmin{}--\LRmax{} in every language; every prompt-clustered interval excludes chance and every Holm-corrected binomial has $p < 10^{-4}$.",
 r"Table~\ref{tab:main} shows five-way accuracy of \LRmin{}--\LRmax{} in every language; every prompt-clustered interval excludes chance and every Holm-corrected binomial has $p < 10^{-4}$. In plain terms, \NFeatures{} numbers that a reader can inspect identify the author about three times as often as guessing, in Hindi as in English."),
(r"This is the expected result~\cite{sapkota2015ngrams}: $n$-grams see vocabulary and morphology, and the features do not.",
 r"This is the expected result~\cite{sapkota2015ngrams}: $n$-grams see vocabulary and morphology, and the features do not; a practitioner with labelled data in the target language should prefer $n$-grams, and pay the gap only when the decision must be explained or must transfer."),
# --- RQ4 trim to pay
(r" La Cava et al.\ find generators harder to separate in English~\cite{lacava2026multilingual}; with different models and features we see the opposite on centroid distance, driven by one model, and neither result supports a general convergence claim.",
 r" La Cava et al.\ find generators harder to separate in English~\cite{lacava2026multilingual}; neither their result nor ours supports a general convergence claim."),
(r"Grok's English register is the outlier that disappears outside English; the other four models are as far apart in Hindi as in English, and silhouettes near zero mean there is no cluster structure in the full feature space in any language.",
 r"Grok's English register is the outlier that disappears outside English; the other four models are as far apart in Hindi as in English, and silhouettes near zero mean no cluster structure in the full feature space in any language."),
]
for a, b in R:
    assert a in s, "NOT FOUND: " + a[:70]
    s = s.replace(a, b)
(H / "main.tex").write_text(s, encoding="utf-8")

b = (H / "references.bib").read_text(encoding="utf-8")
b = re.sub(r"@article\{gorman2022ud,.*?\n\}\n", """@article{gorman2022ud,
  author={Gorman, Robert},
  title={{Universal Dependencies} and Author Attribution of Short Texts with Syntax Alone},
  journal={Digital Humanities Quarterly},
  volume={16},
  number={2},
  year={2022},
  note={art. 000606}
}
""", b, flags=re.S)
b = re.sub(r"@inproceedings\{riverasoto2026attacks,.*?\n\}\n", """@inproceedings{riverasoto2026attacks,
  author={Rivera Soto, Rafael and Chen, Barry and Andrews, Nicholas},
  title={Attacks on Machine-Text Detectors Retain Stylistic Fingerprints},
  booktitle={Proc. ICML},
  year={2026},
  note={arXiv:2505.14608}
}
""", b, flags=re.S)
b = re.sub(r"@article\{zaitsu2026fingerprint,.*?\n\}\n", """@article{zaitsu2026fingerprint,
  author={Zaitsu, Wataru and Jin, Mingzhe and Ishihara, Shunichi and Tsuge, Satoru and Inaba, Mitsuyuki},
  title={Detecting ``Large Language Models Fingerprint'' for {J}apanese Texts Generated by Six {LLMs}},
  journal={Frontiers in Artificial Intelligence},
  volume={9},
  pages={1771115},
  year={2026}
}
""", b, flags=re.S)
(H / "references.bib").write_text(b, encoding="utf-8")
print("style pass applied; bib TODOs left:", b.count("TODO"))
