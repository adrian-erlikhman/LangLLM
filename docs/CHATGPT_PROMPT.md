# ChatGPT prompt: revise the LangLLM paper toward the register of an accepted symposium paper

Paste everything below the line into ChatGPT, then paste `paper/main.tex`. (Do not paste the bibliography; it is fixed.)

---

You are helping revise a 5-page IEEE two-column paper for the IEEE BigData 2026 High School Symposium. Read the whole file first, then edit.

**The model to write toward.** The closest accepted paper from this symposium is Xie, Zhang, Zhang and Liu, "Scoring with Large Language Models: A Study on Measuring Empathy of Responses in Dialogues," IEEE BigData 2024, pp. 7433 to 7437 (arXiv:2412.20264). Its senior author chairs this year's symposium. What it does, and what we want to sound like: it opens with a field-level sentence, states its research questions as literal questions in the first paragraph, gives a why-it-matters paragraph that names who benefits, walks through the pipeline in prose instead of a numbered contribution list, keeps method and result together in each subsection with one takeaway sentence, reports numbers plainly with chance as the anchor and then says in ordinary words what the number means, and closes with a short conclusion where the one limitation is framed as future work. Its tone is a clear engineering report written in the first person plural. Where our draft is stiffer than that, loosen it toward that register. Where our draft is more rigorous than that (pre-registration, prompt-clustered intervals, Holm correction, exact permutation tests), keep the rigor and just explain it in fewer words.

**Hard constraints.**
- Do not change, delete, reorder or invent any `\Macro{}`, `\cite{...}`, `\ref`, `\label`, table, figure environment, or section heading. Every number in the paper is a macro that is generated from result files. Do not type any number.
- Do not add citations, and do not cite the authors' other work.
- No em dashes, no en dashes. Use commas, colons or a new sentence.
- The paper is at the 5-page limit. Any sentence you lengthen must be paid for in the same paragraph. Net length must be equal or shorter.
- Keep the Acknowledgment exactly as written.

**What to fix, in priority order.**
1. Sentences that read as generated text. Cut anything that announces itself ("In this paper, we..."), any list of three adjectives, any sentence that restates the previous one, any "importantly", "notably", "robust", "novel", "leverage", "delve", "crucial", "landscape", "underscore". Replace with the plain statement.
2. Paragraph openers. Each results paragraph should open with the finding in one sentence, then the number, then the caveat.
3. Plain readings. After each headline number, one short sentence a moderator or teacher would understand. We already have one after the RQ1 accuracy; add them only where a paragraph lacks one and only if you can pay for the line.
4. The Discussion. Make the practitioner guidance explicit: when to use n-grams, when to use the features, what neither can do. One sentence each, no hedging words.
5. Consistency. American spelling throughout ("standardized", "labeled", "favor"). "n-gram" always with a hyphen and italic n as in the source.

**Output.** First the full edited `main.tex`. Then a list with one line per changed sentence: the section, the reason, and the net word change. If you believe a sentence claims more than its macros support, do not soften it yourself; put it in a separate "check this" list at the end.
