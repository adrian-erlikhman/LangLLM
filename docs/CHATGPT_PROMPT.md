# ChatGPT prompt: refine the LangLLM paper text

Paste everything below the line into ChatGPT, then paste `paper/main.tex` after it.

---

You are editing the prose of a 5-page IEEE two-column paper for the IEEE BigData 2026 High School Symposium (reviewers: data-mining faculty and PhD students; criteria: technical quality, novelty, relevance, clarity). The paper is written in LaTeX. Every number appears as a macro like `\LRmin{}` or `\Beta{}`; the macros are generated from result files and are correct. You must not change, remove, reorder, or replace any macro, `\cite{...}`, `\ref{...}`, `\label{...}`, table, figure environment, or section heading. Do not add any number that is not already a macro. Do not add citations. Do not add claims. Do not use em dashes or en dashes anywhere; use commas, colons, or separate sentences.

Your job is prose only: make the argument clearer and more direct for a data-mining reader, tighten sentences, and keep the total length the same or shorter (the paper is exactly at the 5-page limit; every added line must be paid for by a removed line in the same paragraph).

House style to enforce:
1. One idea per sentence; prefer sentences under 25 words; active voice with "we" where the authors act.
2. Lead each paragraph with its finding, then the evidence, then the caveat. Never bury the result after the method.
3. Every result sentence names the comparison and the number in the same sentence (for example "features reach X, n-grams Y").
4. Hedge honestly, never vaguely: "no decline detected, with an interval that admits a drop of up to \SteepestDeclinePts{} points" is right; "seems robust" is wrong.
5. State what a practitioner would do with each result in one plain sentence where the section allows it (the Discussion especially): who would use this classifier, on what text, and what it cannot do.
6. Keep the pre-registration framing: questions written before data collection are called that; analyses added later are labelled as added afterwards.
7. Keep the tone of a careful engineering report, not a press release. No "novel", "groundbreaking", "leverage", "delve", "crucial", "robust" as filler.
8. Preserve all technical terms exactly: leave-one-prompt-out, prompt-clustered, Holm-corrected, partial eta squared, within-language z-scoring, exact McNemar, exact permutation.
9. British/American spelling: use American ("standardized", "labeled") consistently; the current text mixes both.
10. The abstract must stay a single paragraph and must keep every macro it currently contains, in an order that reads as: problem, data, method, main result, baseline comparison, transfer, translation, judges.

Deliver the full edited LaTeX file, unchanged outside prose, followed by a bulleted list of every sentence you rewrote with a one-line reason. If a sentence in the source seems to make a claim the macros do not support, do not fix it silently: flag it in the list instead.

Source file follows.
